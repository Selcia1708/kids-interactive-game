import streamlit as st
import random
import operator
import time as time_mod

# ─── Adaptive Question Generator ───────────────────────────────────────────────
OPS = {
    "easy":   [(operator.add, "+", 1, 10),  (operator.sub, "-", 1, 10)],
    "medium": [(operator.add, "+", 10, 50), (operator.sub, "-", 10, 50), (operator.mul, "×", 2, 10)],
    "hard":   [(operator.mul, "×", 5, 12),  (operator.truediv, "÷", 1, 10), (operator.add, "+", 50, 200)]
}

def get_diff():
    s = st.session_state.skill_scores.get("math", 0)
    return "hard" if s >= 70 else "medium" if s >= 40 else "easy"

def gen_question(diff):
    op_fn, op_sym, lo, hi = random.choice(OPS[diff])
    if op_sym == "÷":
        b = random.randint(2, 10)
        a = b * random.randint(1, 10)
    else:
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if op_sym == "-" and b > a:
            a, b = b, a
    ans = int(op_fn(a, b))
    wrong = set()
    while len(wrong) < 3:
        delta = random.choice([-5,-3,-2,-1,1,2,3,5,10,-10])
        w = ans + delta
        if w != ans and w >= 0:
            wrong.add(w)
    opts = [ans] + list(wrong)[:3]
    random.shuffle(opts)
    return {"q": f"{a} {op_sym} {b} = ?", "ans": ans, "opts": opts, "sym": op_sym, "a": a, "b": b}

def award_math(stars, xp, badge=None):
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.skill_scores["math"] = min(
        st.session_state.skill_scores["math"] + stars * 4, 100
    )
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

# ─── Feedback helpers ──────────────────────────────────────────────────────────
MOTIVATIONAL_MSGS = [
    ("🌟","So close! You've got this!","Every mistake is a step forward!"),
    ("💪","Don't give up!","Champions keep trying!"),
    ("🚀","Almost there!","One more try — you'll get it!"),
    ("🧠","Great effort!","Your brain is growing stronger!"),
    ("🌈","Keep going!","Mistakes make us smarter!"),
    ("🎯","Stay focused!","The answer is closer than you think!"),
]

def show_wrong_feedback(correct_answer, hint=None):
    icon, title, subtitle = random.choice(MOTIVATIONAL_MSGS)
    hint_html = f"<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-top:8px'>💡 Hint: {hint}</div>" if hint else ""
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(248,113,113,0.15),rgba(239,68,68,0.08));
        border:2px solid rgba(248,113,113,0.4);border-radius:16px;padding:20px;
        text-align:center;margin:12px 0'>
        <div style='font-size:44px;margin-bottom:8px'>{icon}</div>
        <div style='color:#f87171;font-size:20px;font-weight:900;margin-bottom:4px'>{title}</div>
        <div style='color:rgba(255,255,255,0.7);font-size:14px;margin-bottom:12px'>{subtitle}</div>
        <div style='background:rgba(255,255,255,0.08);border-radius:10px;padding:10px 16px;color:#fff;font-size:15px'>
            ✅ The correct answer was: <b style='color:#4ade80;font-size:20px'> {correct_answer}</b>
        </div>
        {hint_html}
    </div>
    """, unsafe_allow_html=True)

def show_correct_feedback(streak):
    if streak >= 5:
        msg, icon = "🔥 UNSTOPPABLE! 5+ Streak!", "🏆"
    elif streak >= 3:
        msg, icon = f"🔥 x{streak} Streak! You're on fire!", "🌟"
    else:
        choices = [("✅ Correct! Math genius!","⚡"), ("✅ Nailed it!","🎯"),
                   ("✅ Well done, astronaut!","🚀"), ("✅ Brilliant!","🌟")]
        msg, icon = random.choice(choices)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.15),rgba(16,185,129,0.08));
        border:2px solid rgba(74,222,128,0.4);border-radius:16px;padding:16px;
        text-align:center;margin:12px 0'>
        <div style='font-size:36px'>{icon}</div>
        <div style='color:#4ade80;font-size:18px;font-weight:900'>{msg}</div>
    </div>
    """, unsafe_allow_html=True)

def show_number_visual(n):
    dots = "🔵" * min(n, 20)
    extra = f" <span style='color:rgba(255,255,255,0.5)'>+{n-20} more</span>" if n > 20 else ""
    st.markdown(f"<div style='font-size:22px;letter-spacing:4px;margin:12px 0'>{dots}{extra}</div>", unsafe_allow_html=True)

# ─── Main ──────────────────────────────────────────────────────────────────────
def show_math():
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px'>
        <div style='font-size:56px'>🪐</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Math Galaxy</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Conquer numbers across the galaxy!</div>
    </div>
    """, unsafe_allow_html=True)

    skill = st.session_state.skill_scores.get("math", 0)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:20px'>
        <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:12px;max-width:400px;margin:0 auto'>
            <div style='width:{skill}%;height:12px;border-radius:50px;background:linear-gradient(90deg,#4facfe,#00f2fe)'></div>
        </div>
        <div style='color:#fff;font-weight:700;margin-top:6px'>{skill}% Mastered</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧮 Math Quiz","🔢 Number Sense","⏱ Speed Round"])
    ms = st.session_state.quiz_state

    # ── Tab 1: Adaptive Math Quiz ──────────────────────────────────────────────
    with tab1:
        # Generate fresh question only when needed
        if "math_q" not in ms:
            diff = get_diff()
            ms["math_q"]        = gen_question(diff)
            ms["math_answered"] = False
            ms["math_selected"] = None
            ms["math_diff"]     = diff
            ms["math_streak"]   = ms.get("math_streak", 0)
            ms["math_score"]    = ms.get("math_score",  0)

        q = ms["math_q"]
        emoji_map = {"+":"➕","-":"➖","×":"✖️","÷":"➗"}
        op_emoji  = emoji_map.get(q["sym"], "🔢")

        st.markdown(f"""
        <div class='question-box'>
            <div style='font-size:48px;margin-bottom:12px'>{op_emoji}</div>
            <div style='font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:8px'>
                Difficulty: {ms['math_diff'].upper()} | Streak: 🔥{ms.get('math_streak',0)} | Score: ⭐{ms.get('math_score',0)}
            </div>
            <div style='font-size:36px;font-weight:900'>{q['q']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Stable option order per question
        opts = q["opts"]
        cols = st.columns(2)
        for i, opt in enumerate(opts):
            with cols[i % 2]:
                if not ms["math_answered"]:
                    if st.button(str(opt), key=f"math_opt_{ms['math_score']}_{i}", use_container_width=True):
                        ms["math_selected"] = opt
                        ms["math_answered"] = True
                        if opt == q["ans"]:
                            ms["math_streak"] = ms.get("math_streak",0) + 1
                            ms["math_score"]  = ms.get("math_score",0)  + 1
                            award_math(2 if ms["math_streak"]>=3 else 1, 15,
                                       "🧮 Math Whiz" if ms["math_score"]>=5 else None)
                        else:
                            ms["math_streak"] = 0
                        st.rerun()
                else:
                    css = "answer-correct" if opt==q["ans"] else (
                          "answer-wrong"   if opt==ms["math_selected"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if ms["math_answered"]:
            if ms["math_selected"] == q["ans"]:
                show_correct_feedback(ms.get("math_streak", 1))
            else:
                # Generate a helpful math hint
                sym = q["sym"]
                a, b = q.get("a",0), q.get("b",0)
                if sym == "+":   hint = f"Try counting {a} and then adding {b} more."
                elif sym == "-": hint = f"Start at {a} and count back {b} steps."
                elif sym == "×": hint = f"Think of {a} groups of {b} objects."
                elif sym == "÷": hint = f"{a} shared equally among {b} groups."
                else:            hint = None
                show_wrong_feedback(q["ans"], hint)

            if st.button("➡️ Next Problem", use_container_width=True, key="math_next"):
                ms.pop("math_q", None)
                st.rerun()

    # ── Tab 2: Number Sense ────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:16px'>🔢 Count the dots and enter the number!</div>", unsafe_allow_html=True)

        if "ns_num" not in ms:
            limit = 15 if get_diff()=="easy" else 30
            ms["ns_num"] = random.randint(1, limit)
            ms["ns_answered"] = False

        if not ms.get("ns_answered"):
            show_number_visual(ms["ns_num"])
            st.markdown("<br>", unsafe_allow_html=True)
            user_ans = st.number_input("How many dots?", min_value=0, max_value=100, step=1, key="ns_input")
            if st.button("✅ Check!", use_container_width=True):
                ms["ns_answered"] = True
                ms["ns_user"]     = user_ans
                if user_ans == ms["ns_num"]:
                    award_math(1, 10, "👁 Number Ninja" if st.session_state.skill_scores["math"]>=30 else None)
                st.rerun()
        else:
            show_number_visual(ms["ns_num"])
            if ms["ns_user"] == ms["ns_num"]:
                show_correct_feedback(1)
                st.success(f"🎉 Correct! There are **{ms['ns_num']}** dots!")
            else:
                show_wrong_feedback(ms["ns_num"])
            if st.button("🔢 Next Dots!", use_container_width=True):
                ms.pop("ns_num",      None)
                ms.pop("ns_answered", None)
                ms.pop("ns_user",     None)
                st.rerun()

    # ── Tab 3: Speed Round — FIXED ─────────────────────────────────────────────
    with tab3:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:8px'>⏱ 60-Second Speed Round!</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:16px'>Answer as many as you can in 60 seconds!</div>", unsafe_allow_html=True)

        if "speed_active" not in ms:
            ms["speed_active"] = False
            ms["speed_score"]  = 0
            ms["speed_q"]      = None
            ms["speed_start"]  = None

        if not ms["speed_active"]:
            # Show previous best if available
            if ms["speed_score"] > 0:
                st.markdown(f"<div style='color:#ffd700;font-weight:800;text-align:center;margin-bottom:12px'>🏆 Last Score: {ms['speed_score']} correct!</div>", unsafe_allow_html=True)
            if st.button("🚀 Start Speed Round!", use_container_width=True):
                ms["speed_active"] = True
                ms["speed_score"]  = 0
                ms["speed_q"]      = gen_question("easy")
                ms["speed_start"]  = time_mod.time()          # ← FIXED: import at top
                ms["speed_wrong"]  = 0
                st.rerun()
        else:
            # ── Safety check: start time must exist ──
            if ms["speed_start"] is None:
                ms["speed_start"] = time_mod.time()

            elapsed   = time_mod.time() - ms["speed_start"]
            remaining = max(0, 60 - int(elapsed))

            # Progress bar for timer
            timer_pct = int((remaining / 60) * 100)
            timer_color = "#4ade80" if remaining > 20 else "#fbbf24" if remaining > 10 else "#f87171"
            st.markdown(f"""
            <div style='margin-bottom:16px'>
                <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
                    <span class='stat-chip' style='background:{timer_color}22;border:1px solid {timer_color}'>
                        ⏱ {remaining}s left
                    </span>
                    <span class='stat-chip'>✅ {ms['speed_score']} correct</span>
                    <span class='stat-chip'>❌ {ms.get('speed_wrong',0)} wrong</span>
                </div>
                <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:8px'>
                    <div style='width:{timer_pct}%;height:8px;border-radius:50px;background:{timer_color};transition:width 0.5s'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if remaining == 0:
                ms["speed_active"] = False
                total   = ms["speed_score"] + ms.get("speed_wrong", 0)
                acc_pct = int((ms["speed_score"] / total * 100)) if total > 0 else 0
                stars   = ms["speed_score"] // 3
                award_math(stars, ms["speed_score"] * 5,
                           "⚡ Speed Demon" if ms["speed_score"] >= 10 else None)
                st.balloons()
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,rgba(99,102,241,0.2),rgba(168,85,247,0.2));
                    border:2px solid rgba(168,85,247,0.4);border-radius:20px;padding:24px;text-align:center'>
                    <div style='font-size:56px'>🏁</div>
                    <div style='color:#fff;font-size:24px;font-weight:900;margin-bottom:8px'>Time's Up!</div>
                    <div style='font-size:48px;color:#ffd700;font-weight:900'>{ms['speed_score']}</div>
                    <div style='color:rgba(255,255,255,0.6);font-size:15px;margin-bottom:12px'>correct answers</div>
                    <div style='display:flex;justify-content:center;gap:12px'>
                        <span class='stat-chip'>🎯 {acc_pct}% Accuracy</span>
                        <span class='stat-chip'>⭐ +{stars} Stars</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                ms.pop("speed_q", None)
                return

            # ── Question display ──
            if ms["speed_q"] is None:
                ms["speed_q"] = gen_question("easy")

            q = ms["speed_q"]
            st.markdown(f"""
            <div class='question-box' style='padding:20px'>
                <div style='font-size:32px;font-weight:900'>{q['q']}</div>
            </div>
            """, unsafe_allow_html=True)

            scols = st.columns(4)
            for i, opt in enumerate(q["opts"]):
                with scols[i]:
                    btn_key = f"sp_{ms['speed_score']}_{ms.get('speed_wrong',0)}_{i}"
                    if st.button(str(opt), key=btn_key, use_container_width=True):
                        if opt == q["ans"]:
                            ms["speed_score"] += 1
                        else:
                            ms["speed_wrong"] = ms.get("speed_wrong",0) + 1
                        ms["speed_q"] = gen_question("easy" if get_diff()=="easy" else "medium")
                        st.rerun()

            if st.button("🛑 Stop Round", use_container_width=True):
                ms["speed_active"] = False
                ms["speed_start"]  = None
                st.rerun()