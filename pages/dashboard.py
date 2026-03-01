import streamlit as st
import plotly.graph_objects as go

try:
    from database.db import get_leaderboard
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

def show_dashboard():
    name   = st.session_state.child_name
    stars  = st.session_state.stars
    xp     = st.session_state.xp
    badges = st.session_state.badges
    skills = st.session_state.skill_scores

    st.markdown(f"""
    <div style='text-align:center; padding: 10px 0 24px'>
        <div style='font-size:48px'>📊</div>
        <div style='color:#fff; font-size:28px; font-weight:900'>{name}'s Learning Dashboard</div>
        <div style='color:rgba(255,255,255,0.6); font-size:14px'>Track progress, celebrate growth!</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    for col, icon, val, label, color in [
        (k1, "⭐", stars,       "Stars Earned",  "#f6d365"),
        (k2, "⚡", xp,          "XP Points",     "#4facfe"),
        (k3, "🏅", len(badges), "Badges",        "#43e97b"),
        (k4, "🌍", len([v for v in skills.values() if v > 0]), "Worlds Active", "#fa709a"),
    ]:
        with col:
            st.markdown(f"""
            <div class='planet-card' style='padding:20px'>
                <div style='font-size:32px'>{icon}</div>
                <div style='color:{color}; font-size:28px; font-weight:900'>{val}</div>
                <div style='color:rgba(255,255,255,0.6); font-size:12px'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skill Radar + Skill Bars ───────────────────────────────────────────────
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>🕸 Skill Radar</div>",
                    unsafe_allow_html=True)
        categories = list(skills.keys())
        values     = list(skills.values())
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=[c.capitalize() for c in categories] + [categories[0].capitalize()],
            fill='toself',
            fillcolor='rgba(240,147,251,0.25)',
            line=dict(color='#f093fb', width=2),
            marker=dict(size=6, color='#f5576c')
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(255,255,255,0.05)',
                radialaxis=dict(visible=True, range=[0, 100],
                                color='rgba(255,255,255,0.4)',
                                gridcolor='rgba(255,255,255,0.1)'),
                angularaxis=dict(color='#fff', gridcolor='rgba(255,255,255,0.1)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='Nunito'),
            showlegend=False,
            height=320,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>📈 Skill Levels</div>",
                    unsafe_allow_html=True)
        color_map = {
            "phonics": "#f093fb", "math": "#4facfe", "logic": "#a18cd1",
            "science": "#43e97b", "creativity": "#fa709a"
        }
        for skill, val in skills.items():
            level = "🔰 Beginner" if val < 30 else "⚡ Intermediate" if val < 70 else "🏆 Advanced"
            color = color_map.get(skill, "#fff")
            st.markdown(f"""
            <div style='margin-bottom:14px'>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px'>
                    <span style='color:#fff; font-weight:700; font-size:14px'>{skill.capitalize()}</span>
                    <span style='color:rgba(255,255,255,0.5); font-size:12px'>{level} · {val}%</span>
                </div>
                <div style='background:rgba(255,255,255,0.1); border-radius:50px; height:8px'>
                    <div style='width:{val}%; height:8px; border-radius:50px; background:{color}'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Bar Chart ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>📊 Subject Performance</div>",
                unsafe_allow_html=True)
    fig2 = go.Figure(go.Bar(
        x=[s.capitalize() for s in skills.keys()],
        y=list(skills.values()),
        marker=dict(
            color=['#f093fb', '#4facfe', '#a18cd1', '#43e97b', '#fa709a'],
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ),
        text=[f"{v}%" for v in skills.values()],
        textposition='outside',
        textfont=dict(color='#fff', family='Nunito', size=13)
    ))
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color='#fff', family='Nunito'),
        yaxis=dict(range=[0, 110], gridcolor='rgba(255,255,255,0.1)',
                   zerolinecolor='rgba(255,255,255,0.1)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        height=280,
        margin=dict(t=30, b=10, l=10, r=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Badges ─────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>🏅 Badges Earned</div>",
                unsafe_allow_html=True)
    if badges:
        b_cols = st.columns(min(len(badges), 4))
        for i, badge in enumerate(badges):
            with b_cols[i % 4]:
                st.markdown(f"""
                <div class='planet-card' style='padding:16px; text-align:center'>
                    <div style='font-size:28px'>{badge.split()[0]}</div>
                    <div style='color:#ffd700; font-size:13px; font-weight:700; margin-top:4px'>{badge}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:rgba(255,255,255,0.4); font-style:italic'>No badges yet — keep exploring the universe! 🚀</div>",
                    unsafe_allow_html=True)

    # ── Mini Leaderboard Preview ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>🏆 Leaderboard Preview</div>",
                unsafe_allow_html=True)

    board = []
    if DB_AVAILABLE:
        try:
            board = get_leaderboard(5)
        except Exception as e:
            print(f"Dashboard leaderboard error: {e}")

    if board:
        RANK_ICONS  = ["🥇", "🥈", "🥉", "#4", "#5"]
        RANK_COLORS = ["#ffd700", "#c0c0c0", "#cd7f32",
                       "rgba(255,255,255,0.7)", "rgba(255,255,255,0.7)"]
        for i, entry in enumerate(board):
            is_me   = entry["name"].lower() == name.lower()
            border  = "border:2px solid #f093fb" if is_me else "border:1px solid rgba(255,255,255,0.08)"
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

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏆 View Full Leaderboard", use_container_width=True, key="dash_view_lb"):
            st.session_state.current_world = "leaderboard"
            st.rerun()
    else:
        st.markdown("<div style='color:rgba(255,255,255,0.4);font-style:italic'>No leaderboard data yet — start playing to appear here!</div>",
                    unsafe_allow_html=True)

    # ── Recommendations ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#fff; font-weight:800; font-size:16px; margin-bottom:12px'>💡 Smart Recommendations</div>",
                unsafe_allow_html=True)
    recs = []
    for skill, val in skills.items():
        if val == 0:
            recs.append(f"🌍 Start exploring <b>{skill.capitalize()}</b> — this world is waiting for you!")
        elif val < 40:
            recs.append(f"📈 Keep practicing <b>{skill.capitalize()}</b> — you're building great momentum!")
        elif val >= 80:
            recs.append(f"🏆 <b>{skill.capitalize()}</b> — You're a master! Try the harder challenges!")

    for r in recs[:3]:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); border-left:4px solid #f093fb;
            border-radius:8px; padding:12px 16px; margin-bottom:8px; color:#fff; font-size:14px'>
            {r}
        </div>
        """, unsafe_allow_html=True)