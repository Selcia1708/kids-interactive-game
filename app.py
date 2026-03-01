import streamlit as st
from pathlib import Path
import time as time_mod

st.set_page_config(page_title="Kids Learning Universe", page_icon="🌟",
                   layout="wide", initial_sidebar_state="collapsed")

# ─── DB bootstrap ──────────────────────────────────────────────────────────────
try:
    from database.db import (init_db, save_profile, load_profile, save_progress,
                              log_session, log_achievement, get_all_profiles,
                              get_leaderboard, verify_parent, register_parent,
                              get_child_full_stats)
    init_db()
    DB_OK = True
except Exception as e:
    DB_OK = False
    print(f"DB IMPORT/INIT ERROR: {e}")

SKILL_GAIN_NORMAL = 1
SKILL_GAIN_STREAK = 2
XP_PER_CORRECT    = 8
XP_PER_STAR       = 5

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
    html,body,[class*="css"]{font-family:'Nunito',sans-serif;}
    .stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;}
    .main .block-container{padding-top:1rem;}
    #MainMenu,footer,header{visibility:hidden;}
    .planet-card{background:rgba(255,255,255,0.08);border:2px solid rgba(255,255,255,0.15);
        border-radius:24px;padding:28px 20px;text-align:center;cursor:pointer;
        transition:all 0.3s ease;backdrop-filter:blur(10px);margin-bottom:16px;}
    .planet-card:hover{transform:translateY(-6px);border-color:rgba(255,255,255,0.4);
        background:rgba(255,255,255,0.14);box-shadow:0 12px 40px rgba(0,0,0,0.3);}
    .planet-icon{font-size:56px;margin-bottom:10px;}
    .planet-name{color:#fff;font-size:18px;font-weight:800;margin-bottom:6px;}
    .planet-desc{color:rgba(255,255,255,0.65);font-size:13px;}
    .planet-locked{opacity:0.4;cursor:not-allowed;}
    .universe-title{text-align:center;color:#fff;font-size:42px;font-weight:900;
        text-shadow:0 0 30px rgba(255,200,100,0.5);margin-bottom:4px;}
    .universe-sub{text-align:center;color:rgba(255,255,255,0.6);font-size:16px;margin-bottom:32px;}
    .stButton>button{background:linear-gradient(135deg,#f093fb,#f5576c);color:white;
        font-family:'Nunito',sans-serif;font-weight:800;font-size:16px;border:none;
        border-radius:50px;padding:12px 36px;width:100%;cursor:pointer;transition:all 0.3s;
        box-shadow:0 4px 20px rgba(245,87,108,0.4);}
    .stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(245,87,108,0.6);}
    .stTextInput>div>div>input,.stSelectbox>div>div{
        background:rgba(255,255,255,0.08)!important;border:1px solid rgba(255,255,255,0.2)!important;
        border-radius:12px!important;color:white!important;font-family:'Nunito',sans-serif!important;}
    .stat-chip{display:inline-block;background:rgba(255,255,255,0.1);border-radius:50px;
        padding:6px 18px;color:#fff;font-size:14px;font-weight:700;margin:4px;}
    .question-box{background:rgba(255,255,255,0.08);border:2px solid rgba(255,255,255,0.15);
        border-radius:20px;padding:32px;color:#fff;font-size:22px;font-weight:700;
        text-align:center;margin-bottom:24px;}
    .answer-btn{background:rgba(255,255,255,0.1);border:2px solid rgba(255,255,255,0.2);
        border-radius:14px;color:#fff;padding:16px;text-align:center;
        font-size:16px;font-weight:700;margin-bottom:12px;}
    .answer-correct{border-color:#4ade80!important;background:rgba(74,222,128,0.2)!important;}
    .answer-wrong  {border-color:#f87171!important;background:rgba(248,113,113,0.2)!important;}
    .badge{display:inline-block;font-size:13px;font-weight:800;padding:4px 14px;border-radius:50px;margin:2px;}
    .badge-gold {background:linear-gradient(135deg,#f6d365,#fda085);color:#fff;}
    .badge-blue {background:linear-gradient(135deg,#4facfe,#00f2fe);color:#fff;}
    .badge-green{background:linear-gradient(135deg,#43e97b,#38f9d7);color:#fff;}
    .notif{position:fixed;top:70px;right:20px;z-index:9999;
        background:linear-gradient(135deg,#43e97b,#38f9d7);color:#1a1a2e;
        padding:12px 20px;border-radius:12px;font-weight:800;font-size:15px;
        box-shadow:0 8px 24px rgba(0,0,0,0.3);animation:fadeIn 0.4s ease;}
    @keyframes fadeIn{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}
    .daily-badge{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:12px;
        padding:12px 20px;color:#fff;font-weight:800;font-size:14px;margin-bottom:12px;}
    </style>""", unsafe_allow_html=True)

def init_session():
    defaults = {
        "logged_in": False, "child_name": "", "child_age": 6,
        "current_world": "home", "stars": 0, "xp": 0,
        "skill_scores": {"phonics":0,"math":0,"logic":0,"science":0,"creativity":0},
        "worlds_unlocked": ["phonics","math","logic","science","creativity"],
        "badges": [], "quiz_state": {}, "profile_id": None,
        "session_start": time_mod.time(), "daily_streak": 1,
        "show_notif": None, "total_questions": 0, "correct_answers": 0,
        "parent_logged_in": False, "parent_email": None,
        "parent_child_name": None, "parent_child_age": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def auto_save():
    if DB_OK and st.session_state.get("profile_id"):
        try:
            save_progress(
                st.session_state.profile_id,
                st.session_state.stars,
                st.session_state.xp,
                st.session_state.skill_scores,
                st.session_state.badges,
            )
        except Exception as e:
            print(f"auto_save error: {e}")

def global_award(skill: str, stars: int, xp: int, badge: str = None, streak: bool = False):
    gain = SKILL_GAIN_STREAK if streak else SKILL_GAIN_NORMAL
    st.session_state.skill_scores[skill] = min(
        st.session_state.skill_scores.get(skill, 0) + gain, 100
    )
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.total_questions = st.session_state.get("total_questions", 0) + 1
    st.session_state.correct_answers = st.session_state.get("correct_answers", 0) + 1
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)
        if DB_OK and st.session_state.get("profile_id"):
            try: log_achievement(st.session_state.profile_id, badge)
            except: pass
    auto_save()

def show_notification():
    if st.session_state.get("show_notif"):
        st.markdown(f"<div class='notif'>{st.session_state.show_notif}</div>",
                    unsafe_allow_html=True)
        st.session_state.show_notif = None

def show_auth():
    st.markdown("""
    <div style='text-align:center;padding:30px 0 10px'>
        <div style='font-size:64px'>🌌</div>
        <div class='universe-title'>Kids Learning Universe</div>
        <div class='universe-sub'>A magical world where learning never stops ✨</div>
    </div>""", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        tab_child, tab_parent = st.tabs(["🚀 Kid's Login", "👨‍👩‍👧 Parent Login"])

        with tab_child:
            st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:12px'>Enter your details to continue your adventure!</div>",
                        unsafe_allow_html=True)
            name   = st.text_input("What's your name, explorer?", placeholder="e.g. Aarav", key="child_name_input")
            age    = st.selectbox("How old are you?", list(range(3, 13)), index=3, key="child_age_input")
            avatar = st.selectbox("Pick your avatar",
                                  ["🧑‍🚀 Astronaut", "🧙 Wizard", "🦸 Superhero", "🧜 Mermaid"],
                                  key="child_avatar_input")

            if st.button("🌟 Begin My Adventure!", use_container_width=True, key="child_login_btn"):
                if not name.strip():
                    st.error("Please enter your name!")
                else:
                    av  = avatar.split()[0]
                    pid = None
                    if DB_OK:
                        try:
                            pid   = save_profile(name.strip(), age, av)
                            saved = load_profile(name.strip(), age)
                            if saved:
                                st.session_state.stars        = saved["stars"]
                                st.session_state.xp           = saved["xp"]
                                st.session_state.skill_scores = saved["skill_scores"]
                                st.session_state.badges       = saved["badges"]
                        except Exception as e:
                            print(f"save_profile error: {e}")
                    st.session_state.logged_in     = True
                    st.session_state.child_name    = name.strip()
                    st.session_state.child_age     = age
                    st.session_state.avatar        = av
                    st.session_state.profile_id    = pid
                    st.session_state.current_world = "home"
                    st.session_state.show_notif    = (
                        f"🎉 Welcome back, {name.strip()}!" if pid
                        else f"🚀 Welcome, {name.strip()}!"
                    )
                    st.rerun()

        with tab_parent:
            p_mode = st.radio("Account Mode", ["🔐 Login", "📝 Register"],
                              horizontal=True, label_visibility="collapsed", key="p_mode_radio")

            if p_mode == "🔐 Login":
                p_email = st.text_input("Parent Email", key="p_login_email")
                p_pwd   = st.text_input("Password", type="password", key="p_login_pwd")

                if st.button("🔐 Parent Login", use_container_width=True, key="parent_login_btn"):
                    if not DB_OK:
                        st.error("Database not available.")
                    elif not p_email or not p_pwd:
                        st.warning("Enter email and password.")
                    else:
                        parent = verify_parent(p_email, p_pwd)
                        if parent:
                            st.session_state.parent_logged_in  = True
                            st.session_state.parent_email      = p_email
                            st.session_state.parent_child_name = parent["child_name"]
                            st.session_state.parent_child_age  = parent["child_age"]
                            st.session_state.current_world     = "parent_dashboard"
                            st.session_state.logged_in         = True
                            st.session_state.child_name        = parent["child_name"] or "Child"
                            st.rerun()
                        else:
                            st.error("❌ Incorrect email or password.")

            else:
                r_email      = st.text_input("Your Email",       key="r_email")
                r_pwd        = st.text_input("Choose Password",  type="password", key="r_pwd")
                r_pwd2       = st.text_input("Confirm Password", type="password", key="r_pwd2")
                r_child_name = st.text_input("Child's Name",     key="r_child_name")
                r_child_age  = st.selectbox("Child's Age", list(range(3, 13)), key="r_child_age")

                if st.button("📝 Create Parent Account", use_container_width=True, key="register_btn"):
                    if not all([r_email, r_pwd, r_pwd2, r_child_name]):
                        st.warning("Please fill all fields.")
                    elif r_pwd != r_pwd2:
                        st.error("Passwords don't match.")
                    elif len(r_pwd) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif not DB_OK:
                        st.error("Database not available.")
                    else:
                        ok = register_parent(r_email, r_pwd, r_child_name, r_child_age)
                        if ok:
                            st.success("✅ Account created! Please log in.")
                        else:
                            st.error("Email already registered.")

def show_parent_dashboard():
    import plotly.graph_objects as go

    child_name = st.session_state.parent_child_name or "Your Child"
    child_age  = st.session_state.parent_child_age  or 0

    st.markdown(f"""
    <div style='text-align:center;padding:10px 0 20px'>
        <div style='font-size:48px'>👨‍👩‍👧</div>
        <div style='color:#fff;font-size:28px;font-weight:900'>Parent Dashboard</div>
        <div style='color:rgba(255,255,255,0.6);font-size:14px'>
            Monitoring <b style='color:#ffd700'>{child_name}</b>'s learning journey
        </div>
    </div>""", unsafe_allow_html=True)

    stats = None
    if DB_OK:
        try:
            stats = get_child_full_stats(child_name, child_age)
        except Exception as e:
            print(f"get_child_full_stats error: {e}")

    if not stats:
        st.warning(f"No data found for **{child_name}** (age {child_age}). "
                   "Make sure the child has logged in and played at least once.")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Go to Kid's Login", use_container_width=True, key="pd_goto_child_nodata"):
                st.session_state.parent_logged_in = False
                st.session_state.logged_in        = False
                st.session_state.current_world    = "home"
                st.rerun()
        with col2:
            if st.button("🚪 Parent Logout", use_container_width=True, key="pd_logout_nodata"):
                _parent_logout()
        return

    stars    = stats["stars"]
    xp       = stats["xp"]
    badges   = stats["badges"]
    skills   = stats["skill_scores"]
    sessions = stats.get("sessions", [])

    k1, k2, k3, k4 = st.columns(4)
    for col, icon, val, label, clr in [
        (k1, "⭐", stars,              "Stars Earned",  "#f6d365"),
        (k2, "⚡", xp,                 "XP Points",     "#4facfe"),
        (k3, "🏅", len(badges),        "Badges",        "#43e97b"),
        (k4, "🌍", len([v for v in skills.values() if v > 0]), "Worlds Active", "#fa709a"),
    ]:
        with col:
            st.markdown(f"""
            <div class='planet-card' style='padding:20px'>
                <div style='font-size:32px'>{icon}</div>
                <div style='color:{clr};font-size:28px;font-weight:900'>{val}</div>
                <div style='color:rgba(255,255,255,0.6);font-size:12px'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>🕸 Skill Radar</div>",
                    unsafe_allow_html=True)
        cats = list(skills.keys()); vals = list(skills.values())
        fig = go.Figure(go.Scatterpolar(
            r=vals+[vals[0]], theta=[c.capitalize() for c in cats]+[cats[0].capitalize()],
            fill='toself', fillcolor='rgba(240,147,251,0.25)',
            line=dict(color='#f093fb', width=2), marker=dict(size=6, color='#f5576c')
        ))
        fig.update_layout(
            polar=dict(bgcolor='rgba(255,255,255,0.05)',
                       radialaxis=dict(visible=True, range=[0,100],
                                       color='rgba(255,255,255,0.4)',
                                       gridcolor='rgba(255,255,255,0.1)'),
                       angularaxis=dict(color='#fff', gridcolor='rgba(255,255,255,0.1)')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='Nunito'), showlegend=False,
            height=320, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>📈 Skill Levels</div>",
                    unsafe_allow_html=True)
        clr_map = {"phonics":"#f093fb","math":"#4facfe","logic":"#a18cd1",
                   "science":"#43e97b","creativity":"#fa709a"}
        for skill, val in skills.items():
            lv = "🔰 Beginner" if val < 30 else "⚡ Intermediate" if val < 70 else "🏆 Advanced"
            c  = clr_map.get(skill, "#fff")
            st.markdown(f"""
            <div style='margin-bottom:14px'>
                <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
                    <span style='color:#fff;font-weight:700;font-size:14px'>{skill.capitalize()}</span>
                    <span style='color:rgba(255,255,255,0.5);font-size:12px'>{lv} · {val}%</span>
                </div>
                <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:8px'>
                    <div style='width:{val}%;height:8px;border-radius:50px;background:{c}'></div>
                </div>
            </div>""", unsafe_allow_html=True)

    if sessions:
        st.markdown("<br><div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>📅 Recent Sessions</div>",
                    unsafe_allow_html=True)
        for s in sessions[:8]:
            mins = s.get("duration_s", 0) // 60
            secs = s.get("duration_s", 0) % 60
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.06);border-radius:12px;padding:12px 16px;
                margin-bottom:8px;color:#fff;display:flex;justify-content:space-between'>
                <span>🌍 <b>{s.get('world','—').capitalize()}</b></span>
                <span>⭐ {s.get('score',0)}</span>
                <span>⏱ {mins}m {secs}s</span>
                <span style='color:rgba(255,255,255,0.4);font-size:12px'>{str(s.get('played_at',''))[:10]}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br><div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>💡 Recommendations</div>",
                unsafe_allow_html=True)
    for skill, val in skills.items():
        if val == 0:    msg = f"🌍 {skill.capitalize()} hasn't been explored yet — encourage your child!"
        elif val < 40:  msg = f"📈 {skill.capitalize()} is at {val}% — more practice sessions recommended."
        elif val >= 80: msg = f"🏆 {skill.capitalize()} is nearly mastered ({val}%) — try harder levels!"
        else: continue
        st.markdown(f"<div style='background:rgba(255,255,255,0.06);border-left:4px solid #f093fb;"
                    f"border-radius:8px;padding:12px 16px;margin-bottom:8px;color:#fff;font-size:14px'>{msg}</div>",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        from utils.report import generate_pdf_report
        pdf = generate_pdf_report(
            child_name, child_age,
            stats.get("avatar", "🧑‍🚀"),
            stars, xp, skills, badges,
            sessions=sessions,
            achievements=stats.get("achievements", [])
        )
        if pdf:
            st.download_button(
                "📄 Download Full Progress Report (PDF)",
                data=pdf,
                file_name=f"{child_name}_progress_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except Exception:
        st.info("Install reportlab to enable PDF reports: pip install reportlab")

    st.markdown("<br>", unsafe_allow_html=True)
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("🚀 Go to Kid's Login", use_container_width=True, key="pd_goto_child"):
            st.session_state.parent_logged_in = False
            st.session_state.logged_in        = False
            st.session_state.current_world    = "home"
            st.rerun()
    with nav2:
        if st.button("🚪 Parent Logout", use_container_width=True, key="pd_logout"):
            _parent_logout()

def _parent_logout():
    for k in ["parent_logged_in","parent_email","parent_child_name",
              "parent_child_age","logged_in","child_name","current_world"]:
        st.session_state.pop(k, None)
    st.rerun()

def show_sidebar():
    if st.session_state.get("parent_logged_in"):
        return
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:16px 0'>
            <div style='font-size:48px'>{st.session_state.get('avatar','🧑‍🚀')}</div>
            <div style='color:#fff;font-weight:900;font-size:18px'>{st.session_state.child_name}</div>
            <div style='color:rgba(255,255,255,0.5);font-size:13px'>Age {st.session_state.child_age}</div>
        </div>""", unsafe_allow_html=True)

        level       = max(1, st.session_state.xp // 200 + 1)
        xp_in_level = st.session_state.xp % 200
        xp_pct      = min(int(xp_in_level / 200 * 100), 100)

        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06);border-radius:12px;padding:12px;margin-bottom:12px'>
            <div style='color:#ffd700;font-size:13px;font-weight:800;margin-bottom:8px'>📊 MY STATS</div>
            <div style='color:#fff;font-size:14px'>⭐ Stars: <b>{st.session_state.stars}</b></div>
            <div style='color:#fff;font-size:14px'>⚡ XP: <b>{st.session_state.xp}</b></div>
            <div style='color:#fff;font-size:14px'>🎮 Level: <b>{level}</b></div>
            <div style='color:#fff;font-size:14px'>🏅 Badges: <b>{len(st.session_state.badges)}</b></div>
            <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:6px;margin-top:8px'>
                <div style='width:{xp_pct}%;height:6px;border-radius:50px;
                    background:linear-gradient(90deg,#f6d365,#fda085)'></div>
            </div>
            <div style='color:rgba(255,255,255,0.4);font-size:11px;margin-top:4px'>
                Level {level}→{level+1}: {xp_in_level}/200 XP
            </div>
        </div>""", unsafe_allow_html=True)

        total   = st.session_state.total_questions
        correct = st.session_state.correct_answers
        acc     = int((correct / total) * 100) if total > 0 else 0
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06);border-radius:12px;padding:12px;margin-bottom:12px'>
            <div style='color:#4facfe;font-size:13px;font-weight:800;margin-bottom:8px'>🎯 ACCURACY</div>
            <div style='color:#fff;font-size:14px'>Questions: <b>{total}</b></div>
            <div style='color:#fff;font-size:14px'>Correct: <b>{correct}</b></div>
            <div style='color:#4ade80;font-size:16px;font-weight:900'>{acc}%</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        for label, world in [("🌌 Universe Map", "home"),
                              ("📊 Dashboard",    "dashboard"),
                              ("🏆 Leaderboard",  "leaderboard")]:
            if st.button(label, key=f"nav_{world}", use_container_width=True):
                st.session_state.current_world = world
                st.rerun()

        st.markdown("---")
        try:
            import sys, os
            sys.path.insert(0, os.path.dirname(__file__))
            from utils.report import generate_pdf_report
            pdf = generate_pdf_report(
                st.session_state.child_name, st.session_state.child_age,
                st.session_state.get("avatar", "🧑‍🚀"),
                st.session_state.stars, st.session_state.xp,
                st.session_state.skill_scores, st.session_state.badges
            )
            if pdf:
                st.download_button("📄 My Report", data=pdf,
                    file_name=f"{st.session_state.child_name}_report.pdf",
                    mime="application/pdf", use_container_width=True)
        except Exception:
            pass

        if st.button("💾 Save", use_container_width=True):
            auto_save()
            st.success("✅ Saved!")
        if st.button("🚪 Log Out", use_container_width=True):
            auto_save()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

WORLDS = [
    {"id":"phonics",    "icon":"🌎","name":"Planet Phonics",    "desc":"Reading & Language",        "color":"#f093fb,#f5576c","skill":"phonics"},
    {"id":"math",       "icon":"🪐","name":"Math Galaxy",        "desc":"Numbers & Problem Solving", "color":"#4facfe,#00f2fe","skill":"math"},
    {"id":"science",    "icon":"🔬","name":"Science Lab World",  "desc":"Curiosity & Experiments",   "color":"#43e97b,#38f9d7","skill":"science"},
    {"id":"creativity", "icon":"🎨","name":"Creative Island",    "desc":"Art & Storytelling",        "color":"#fa709a,#fee140","skill":"creativity"},
    {"id":"logic",      "icon":"🧩","name":"Logic City",         "desc":"Puzzles & Reasoning",       "color":"#a18cd1,#fbc2eb","skill":"logic"},
]

def show_world_map():
    import random
    name   = st.session_state.child_name
    av     = st.session_state.get("avatar", "🧑‍🚀")
    xp     = st.session_state.xp
    level  = max(1, xp // 200 + 1)
    xp_pct = min(int((xp % 200) / 200 * 100), 100)

    st.markdown(f"""
    <div class='universe-title'>🌌 The Learning Universe</div>
    <div class='universe-sub'>Welcome back, {av} <b style='color:#ffd700'>{name}</b>!</div>
    <div style='text-align:center;margin-bottom:8px'>
        <span class='stat-chip'>⭐ {st.session_state.stars}</span>
        <span class='stat-chip'>⚡ {xp} XP</span>
        <span class='stat-chip'>🎮 Level {level}</span>
        <span class='stat-chip'>🏅 {len(st.session_state.badges)} Badges</span>
    </div>
    <div style='max-width:400px;margin:0 auto 24px'>
        <div style='color:rgba(255,255,255,0.5);font-size:12px;text-align:center;margin-bottom:4px'>
            Level {level}→{level+1} ({xp % 200}/200 XP)
        </div>
        <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:10px'>
            <div style='width:{xp_pct}%;height:10px;border-radius:50px;
                background:linear-gradient(90deg,#f6d365,#fda085)'></div>
        </div>
    </div>""", unsafe_allow_html=True)

    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("🔄 Switch Account", use_container_width=True, key="world_map_switch"):
            auto_save()
            st.session_state.logged_in     = False
            st.session_state.current_world = "home"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    random.seed(name + time_mod.strftime("%Y%m%d"))
    daily = random.choice(WORLDS)
    st.markdown(f"<div class='daily-badge'>🎯 <b>Daily Challenge:</b> Play <b>{daily['name']}</b> for +5 Bonus Stars!</div>",
                unsafe_allow_html=True)

    cols = st.columns(3)
    for i, w in enumerate(WORLDS):
        pct = min(st.session_state.skill_scores.get(w["skill"], 0), 100)
        with cols[i % 3]:
            st.markdown(f"""
            <div class='planet-card'>
                <div class='planet-icon'>{w['icon']}</div>
                <div class='planet-name'>{w['name']}</div>
                <div class='planet-desc'>{w['desc']}</div>
                <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:8px;margin-top:10px'>
                    <div style='width:{pct}%;height:8px;border-radius:50px;
                        background:linear-gradient(90deg,{w["color"]})'></div>
                </div>
                <div style='color:rgba(255,255,255,0.5);font-size:12px;margin-top:6px'>{pct}% mastered</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Enter {w['name'].split()[0]}", key=f"btn_{w['id']}"):
                st.session_state.current_world = w["id"]
                st.session_state.session_start = time_mod.time()
                st.rerun()

    if st.session_state.badges:
        st.markdown("<br><div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:8px'>🏅 My Badges</div>",
                    unsafe_allow_html=True)
        st.markdown("".join([f"<span class='badge badge-gold'>{b}</span>"
                              for b in st.session_state.badges]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:12px'>🏆 Top Explorers</div>",
                unsafe_allow_html=True)

    board = []
    if DB_OK:
        try:
            board = get_leaderboard(3)
        except Exception as e:
            print(f"Home leaderboard error: {e}")

    RANK_ICONS  = ["🥇", "🥈", "🥉"]
    RANK_COLORS = ["#ffd700", "#c0c0c0", "#cd7f32"]

    if board:
        for i, entry in enumerate(board):
            is_me   = entry["name"].lower() == name.lower()
            border  = "border:2px solid #f093fb" if is_me else "border:1px solid rgba(255,255,255,0.1)"
            you_tag = "<span style='background:#f093fb;color:#fff;font-size:10px;font-weight:800;padding:2px 8px;border-radius:50px;margin-left:8px'>YOU</span>" if is_me else ""
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                background:rgba(255,255,255,0.05);{border};
                border-radius:12px;padding:10px 16px;margin-bottom:6px'>
                <div style='display:flex;align-items:center;gap:10px'>
                    <span style='font-size:20px'>{RANK_ICONS[i]}</span>
                    <span style='font-size:22px'>{entry.get('avatar','🧑‍🚀')}</span>
                    <span style='color:{RANK_COLORS[i]};font-weight:800;font-size:15px'>
                        {entry['name']}{you_tag}
                    </span>
                </div>
                <div>
                    <span class='stat-chip'>⭐ {entry['stars']}</span>
                    <span class='stat-chip'>⚡ {entry['xp']} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:rgba(255,255,255,0.4);font-style:italic;font-size:14px'>No players yet — be the first on the leaderboard!</div>",
                    unsafe_allow_html=True)

    _, lb_col, _ = st.columns([2, 3, 2])
    with lb_col:
        if st.button("🏆 View Full Leaderboard", use_container_width=True, key="home_lb_btn"):
            st.session_state.current_world = "leaderboard"
            st.rerun()

def back_btn(world_id=None):
    if st.button("← Back to Universe"):
        if DB_OK and st.session_state.get("profile_id") and world_id:
            try:
                dur = int(time_mod.time() - st.session_state.get("session_start", time_mod.time()))
                log_session(st.session_state.profile_id, world_id, st.session_state.stars, dur)
            except: pass
        auto_save()
        st.session_state.current_world = "home"
        st.session_state.quiz_state    = {}
        st.rerun()

def main():
    load_css()
    init_session()

    if not st.session_state.logged_in:
        show_auth()
        return

    if st.session_state.get("parent_logged_in"):
        show_parent_dashboard()
        return

    show_notification()
    show_sidebar()
    w = st.session_state.current_world

    if w == "home":
        show_world_map()
    elif w == "phonics":
        back_btn("phonics")
        from pages.phonics         import show_phonics;    show_phonics()
    elif w == "math":
        back_btn("math")
        from pages.math_galaxy     import show_math;       show_math()
    elif w == "logic":
        back_btn("logic")
        from pages.logic_city      import show_logic;      show_logic()
    elif w == "science":
        back_btn("science")
        from pages.science_lab     import show_science;    show_science()
    elif w == "creativity":
        back_btn("creativity")
        from pages.creative_island import show_creative;   show_creative()
    elif w == "dashboard":
        if st.button("← Back to Universe"):
            st.session_state.current_world = "home"
            st.rerun()
        from pages.dashboard       import show_dashboard;  show_dashboard()
    elif w == "leaderboard":
        if st.button("← Back to Universe"):
            st.session_state.current_world = "home"
            st.rerun()
        from pages.leaderboard     import show_leaderboard; show_leaderboard()

if __name__ == "__main__":
    main()