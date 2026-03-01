import streamlit as st

try:
    from database.db import get_leaderboard, get_session_history
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

RANK_COLORS = ["#ffd700", "#c0c0c0", "#cd7f32"]
RANK_ICONS  = ["🥇", "🥈", "🥉"]
RANK_BG     = [
    "linear-gradient(135deg,rgba(246,211,101,0.15),rgba(253,160,133,0.15))",
    "linear-gradient(135deg,rgba(192,192,192,0.15),rgba(160,160,160,0.1))",
    "linear-gradient(135deg,rgba(205,127,50,0.15),rgba(180,100,30,0.1))",
]

def show_leaderboard():
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px'>
        <div style='font-size:56px'>🏆</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Hall of Fame</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Top explorers in the Learning Universe!</div>
    </div>
    """, unsafe_allow_html=True)

    name   = st.session_state.child_name
    stars  = st.session_state.stars
    xp     = st.session_state.xp
    badges = st.session_state.badges
    avatar = st.session_state.get("avatar", "🧑‍🚀")

    tab1, tab2 = st.tabs(["🏆 Leaderboard", "📅 My Sessions"])

    # ── Tab 1: Leaderboard ─────────────────────────────────────────────────────
    with tab1:

        # Current player card
        st.markdown(f"""
        <div class='planet-card' style='max-width:420px;margin:0 auto 28px;
            background:linear-gradient(135deg,rgba(240,147,251,0.15),rgba(245,87,108,0.15));
            border-color:#f093fb'>
            <div style='font-size:40px'>{avatar}</div>
            <div style='color:#fff;font-weight:900;font-size:20px'>
                {name} <span style='color:#ffd700'>(You)</span>
            </div>
            <div style='margin-top:10px'>
                <span class='stat-chip'>⭐ {stars}</span>
                <span class='stat-chip'>⚡ {xp} XP</span>
                <span class='stat-chip'>🏅 {len(badges)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Load real leaderboard from DB
        board = []
        if DB_AVAILABLE:
            try:
                board = get_leaderboard(10)
            except Exception as e:
                print(f"Leaderboard fetch error: {e}")

        if not board:
            st.markdown("""
            <div style='text-align:center;color:rgba(255,255,255,0.5);
                font-size:14px;padding:40px 0'>
                No players on the leaderboard yet.<br>
                Start exploring worlds to appear here!
            </div>
            """, unsafe_allow_html=True)
            return

        # Column headers
        st.markdown("""
        <div style='display:grid;grid-template-columns:60px 1fr auto;
            gap:12px;padding:8px 20px;
            color:rgba(255,255,255,0.4);font-size:12px;
            font-weight:800;text-transform:uppercase;letter-spacing:1px'>
            <span>Rank</span>
            <span>Explorer</span>
            <span>Stats</span>
        </div>
        """, unsafe_allow_html=True)

        for i, entry in enumerate(board):
            rank_color = RANK_COLORS[i] if i < 3 else "rgba(255,255,255,0.75)"
            rank_icon  = RANK_ICONS[i]  if i < 3 else f"#{i+1}"
            bg         = RANK_BG[i] if i < 3 else "rgba(255,255,255,0.05)"
            is_current = entry["name"].lower() == name.lower()
            border     = "border:2px solid #f093fb" if is_current else "border:1px solid rgba(255,255,255,0.1)"
            you_badge  = "<span style='background:#f093fb;color:#fff;font-size:10px;font-weight:800;padding:2px 8px;border-radius:50px;margin-left:8px'>YOU</span>" if is_current else ""

            st.markdown(f"""
            <div style='display:grid;grid-template-columns:60px 1fr auto;
                gap:12px;align-items:center;
                background:{bg};
                {border};
                border-radius:16px;padding:14px 20px;margin-bottom:8px'>
                <div style='font-size:24px;text-align:center'>{rank_icon}</div>
                <div style='display:flex;align-items:center;gap:10px'>
                    <span style='font-size:28px'>{entry.get('avatar','🧑‍🚀')}</span>
                    <span style='color:{rank_color};font-weight:800;font-size:16px'>
                        {entry['name']}{you_badge}
                    </span>
                </div>
                <div style='text-align:right'>
                    <span class='stat-chip'>⭐ {entry['stars']}</span>
                    <span class='stat-chip'>⚡ {entry['xp']} XP</span>
                    <span class='stat-chip'>🏅 {entry['badge_count']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Find current user's rank
        user_rank = next((i+1 for i, e in enumerate(board)
                          if e["name"].lower() == name.lower()), None)
        if user_rank:
            st.markdown(f"""
            <div style='text-align:center;color:rgba(255,255,255,0.5);
                font-size:13px;margin-top:16px'>
                You are ranked <b style='color:#ffd700'>#{user_rank}</b>
                out of {len(board)} explorers
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center;color:rgba(255,255,255,0.4);
                font-size:13px;margin-top:16px'>
                Keep playing to appear on the leaderboard!
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: My Sessions ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:16px'>📅 My Learning Sessions</div>",
                    unsafe_allow_html=True)

        pid = st.session_state.get("profile_id")

        if not DB_AVAILABLE:
            st.info("Database not connected. Sessions will appear here once connected.")
            return

        if not pid:
            st.info("Log in with a saved profile to see your session history.")
            return

        try:
            sessions = get_session_history(pid, limit=20)
            if not sessions:
                st.markdown("""
                <div style='text-align:center;color:rgba(255,255,255,0.4);
                    font-size:14px;padding:40px 0'>
                    No sessions yet — start exploring the universe!
                </div>
                """, unsafe_allow_html=True)
                return

            # Summary stats
            total_sessions = len(sessions)
            total_stars    = sum(s.get("score", 0) for s in sessions)
            total_time_s   = sum(s.get("duration_s", 0) for s in sessions)
            total_mins     = total_time_s // 60

            s1, s2, s3 = st.columns(3)
            for col, icon, val, label, clr in [
                (s1, "🎮", total_sessions, "Total Sessions", "#4facfe"),
                (s2, "⭐", total_stars,    "Stars Earned",   "#f6d365"),
                (s3, "⏱", f"{total_mins}m","Time Played",   "#43e97b"),
            ]:
                with col:
                    st.markdown(f"""
                    <div class='planet-card' style='padding:16px'>
                        <div style='font-size:24px'>{icon}</div>
                        <div style='color:{clr};font-size:22px;font-weight:900'>{val}</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:12px'>{label}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # World colour map
            world_colors = {
                "phonics":    "#f093fb",
                "math":       "#4facfe",
                "logic":      "#a18cd1",
                "science":    "#43e97b",
                "creativity": "#fa709a",
            }

            for s in sessions:
                world   = s.get("world", "—").lower()
                clr     = world_colors.get(world, "#fff")
                mins    = s.get("duration_s", 0) // 60
                secs    = s.get("duration_s", 0) % 60
                date    = str(s.get("played_at", ""))[:10]
                score   = s.get("score", 0)

                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.05);
                    border-left:4px solid {clr};
                    border-radius:12px;padding:12px 18px;
                    margin-bottom:8px;
                    display:flex;justify-content:space-between;
                    align-items:center;color:#fff'>
                    <span style='font-weight:800;font-size:15px;color:{clr}'>
                        {world.capitalize()}
                    </span>
                    <span class='stat-chip'>⭐ {score}</span>
                    <span class='stat-chip'>⏱ {mins}m {secs}s</span>
                    <span style='color:rgba(255,255,255,0.4);font-size:12px'>{date}</span>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            print(f"Session history error: {e}")
            st.info("Could not load session history. Please try again.")