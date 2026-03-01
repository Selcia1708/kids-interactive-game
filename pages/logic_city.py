import streamlit as st
import random

# ─── Motivational Feedback ─────────────────────────────────────────────────────
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

def show_correct_feedback(streak=1):
    if streak >= 5:   msg, icon = "🔥 UNSTOPPABLE! 5+ Streak!", "🏆"
    elif streak >= 3: msg, icon = f"🔥 x{streak} Streak! Logic master!", "🌟"
    else:
        choices = [("✅ Correct! You cracked it!","🔮"),("✅ Logic genius!","🧩"),("✅ Pattern master!","⭐")]
        msg, icon = random.choice(choices)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.15),rgba(16,185,129,0.08));
        border:2px solid rgba(74,222,128,0.4);border-radius:16px;padding:16px;
        text-align:center;margin:12px 0'>
        <div style='font-size:36px'>{icon}</div>
        <div style='color:#4ade80;font-size:18px;font-weight:900'>{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Pattern Sequences ─────────────────────────────────────────────────────────
PATTERNS = {
    "easy": [
        {"seq": ["🔴","🔵","🔴","🔵","🔴","?"],   "ans": "🔵", "opts": ["🔵","🟡","🟢","🔴"]},
        {"seq": ["⭐","⭐","🌙","⭐","⭐","?"],      "ans": "🌙", "opts": ["🌙","☀️","⭐","❤️"]},
        {"seq": ["🐱","🐶","🐱","🐶","🐱","?"],    "ans": "🐶", "opts": ["🐶","🐱","🐭","🐰"]},
        {"seq": ["1","2","3","4","5","?"],          "ans": "6",  "opts": ["6","7","8","9"]},
        {"seq": ["🍎","🍊","🍌","🍎","🍊","?"],    "ans": "🍌", "opts": ["🍌","🍇","🍎","🍓"]},
    ],
    "medium": [
        {"seq": ["2","4","6","8","10","?"],         "ans": "12", "opts": ["11","12","13","14"]},
        {"seq": ["🔺","🔺","🔹","🔺","🔺","?"],    "ans": "🔹", "opts": ["🔹","🔺","🔶","⬛"]},
        {"seq": ["A","B","C","A","B","?"],           "ans": "C",  "opts": ["C","D","A","B"]},
        {"seq": ["5","10","15","20","25","?"],       "ans": "30", "opts": ["28","29","30","35"]},
        {"seq": ["1","3","5","7","9","?"],           "ans": "11", "opts": ["10","11","12","13"]},
    ],
    "hard": [
        {"seq": ["1","1","2","3","5","?"],           "ans": "8",  "opts": ["7","8","9","10"]},
        {"seq": ["2","4","8","16","32","?"],         "ans": "64", "opts": ["48","56","64","72"]},
        {"seq": ["Z","Y","X","W","V","?"],            "ans": "U",  "opts": ["U","T","S","V"]},
        {"seq": ["🟥","🟧","🟨","🟩","🟦","?"],    "ans": "🟪", "opts": ["🟪","🟫","⬛","🟥"]},
        {"seq": ["3","6","12","24","48","?"],        "ans": "96", "opts": ["72","84","96","100"]},
    ]
}

RIDDLES = [
    {"r": "I have hands but can't clap. What am I? 🕐",        "ans": "Clock",    "opts": ["Clock","Robot","Glove","Puppet"]},
    {"r": "I'm tall when young, short when old. What am I? 🕯", "ans": "Candle",   "opts": ["Tree","Candle","Person","Mountain"]},
    {"r": "What has teeth but can't bite? 🔑",                  "ans": "Comb",     "opts": ["Comb","Key","Saw","Fork"]},
    {"r": "I have cities but no houses. What am I? 🗺",         "ans": "Map",      "opts": ["Map","Globe","Atlas","Dream"]},
    {"r": "The more you take, the more you leave. What? 👣",    "ans": "Footsteps","opts": ["Footsteps","Money","Time","Sand"]},
    {"r": "What gets wetter as it dries? 🧺",                   "ans": "Towel",    "opts": ["Towel","Rain","Sponge","Cloud"]},
    {"r": "What can travel around the world without moving?",    "ans": "Stamp",    "opts": ["Stamp","Email","Bird","Wind"]},
]

SORTING_GAMES = [
    {
        "title": "Sort Animals by Size 🐾",
        "items": ["🐘 Elephant","🐭 Mouse","🦁 Lion","🐟 Fish"],
        "correct": ["🐭 Mouse","🐟 Fish","🦁 Lion","🐘 Elephant"],
        "hint": "Smallest to Largest"
    },
    {
        "title": "Sort Numbers: Smallest First 🔢",
        "items": ["42","7","156","23"],
        "correct": ["7","23","42","156"],
        "hint": "Ascending order"
    }
]

def get_diff():
    s = st.session_state.skill_scores.get("logic", 0)
    return "hard" if s >= 70 else "medium" if s >= 40 else "easy"

def award_logic(stars, xp, badge=None):
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.skill_scores["logic"] = min(
        st.session_state.skill_scores["logic"] + stars * 4, 100
    )
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

# ─── Main ──────────────────────────────────────────────────────────────────────
def show_logic():
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px'>
        <div style='font-size:56px'>🧩</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Logic City</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Train your brain with puzzles & patterns!</div>
    </div>
    """, unsafe_allow_html=True)

    skill = st.session_state.skill_scores.get("logic", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px'>
        <div style='background:rgba(255,255,255,0.1); border-radius:50px; height:12px; max-width:400px; margin:0 auto'>
            <div style='width:{skill}%; height:12px; border-radius:50px;
                background:linear-gradient(90deg,#a18cd1,#fbc2eb)'></div>
        </div>
        <div style='color:#fff; font-weight:700; margin-top:6px'>{skill}% Mastered</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔮 Pattern Game", "🧠 Riddles", "📊 Sort & Order"])

    ls = st.session_state.quiz_state

    # ── Tab 1: Pattern Recognition ─────────────────────────────────────────────
    with tab1:
        diff  = get_diff()
        pool  = PATTERNS[diff]

        if "lg_idx" not in ls:
            ls["lg_idx"]      = random.randint(0, len(pool)-1)
            ls["lg_answered"] = False
            ls["lg_selected"] = None
            ls["lg_score"]    = ls.get("lg_score", 0)

        p = pool[ls["lg_idx"]]
        seq_display = "  →  ".join(p["seq"])

        st.markdown(f"""
        <div class='question-box'>
            <div style='font-size:11px; color:rgba(255,255,255,0.4); margin-bottom:8px'>
                DIFFICULTY: {diff.upper()} | SCORE: ⭐{ls.get('lg_score',0)}
            </div>
            <div style='font-size:14px; color:rgba(255,255,255,0.6); margin-bottom:8px'>What comes next in the pattern?</div>
            <div style='font-size:28px; letter-spacing:4px; margin-bottom:4px'>{seq_display}</div>
        </div>
        """, unsafe_allow_html=True)

        pcols = st.columns(4)
        for i, opt in enumerate(p["opts"]):
            with pcols[i]:
                if not ls["lg_answered"]:
                    if st.button(opt, key=f"lg_opt_{i}", use_container_width=True):
                        ls["lg_selected"] = opt
                        ls["lg_answered"] = True
                        if opt == p["ans"]:
                            ls["lg_score"] = ls.get("lg_score", 0) + 1
                            award_logic(1, 15, "🔮 Pattern Master" if ls["lg_score"] >= 5 else None)
                        st.rerun()
                else:
                    css = "answer-correct" if opt == p["ans"] else (
                          "answer-wrong"   if opt == ls["lg_selected"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if ls["lg_answered"]:
            if ls["lg_selected"] == p["ans"]:
                show_correct_feedback(ls.get("lg_streak", 1))
            else:
                show_wrong_feedback(p["ans"], "Look at the gap between each item — is it repeating or increasing?")

            if st.button("➡️ Next Pattern", use_container_width=True, key="lg_next"):
                diff2 = get_diff()
                pool2 = PATTERNS[diff2]
                ls["lg_idx"]      = random.randint(0, len(pool2)-1)
                ls["lg_answered"] = False
                ls["lg_selected"] = None
                st.rerun()

    # ── Tab 2: Riddles ─────────────────────────────────────────────────────────
    with tab2:
        if "riddle_idx" not in ls:
            ls["riddle_idx"]      = random.randint(0, len(RIDDLES)-1)
            ls["riddle_answered"] = False
            ls["riddle_selected"] = None
            ls["riddle_score"]    = ls.get("riddle_score", 0)
            ls["riddle_hint"]     = False

        r = RIDDLES[ls["riddle_idx"]]

        st.markdown(f"""
        <div class='question-box' style='font-size:20px; line-height:1.6'>
            <div style='font-size:13px; color:rgba(255,255,255,0.4); margin-bottom:8px'>
                🎯 RIDDLE | SCORE: ⭐{ls.get('riddle_score',0)}
            </div>
            {r['r']}
        </div>
        """, unsafe_allow_html=True)

        rcols = st.columns(2)
        for i, opt in enumerate(r["opts"]):
            with rcols[i % 2]:
                if not ls["riddle_answered"]:
                    if st.button(opt, key=f"rd_opt_{i}", use_container_width=True):
                        ls["riddle_selected"] = opt
                        ls["riddle_answered"] = True
                        if opt == r["ans"]:
                            ls["riddle_score"] = ls.get("riddle_score", 0) + 1
                            award_logic(2, 20, "🧠 Riddle King" if ls["riddle_score"] >= 4 else None)
                        st.rerun()
                else:
                    css = "answer-correct" if opt == r["ans"] else (
                          "answer-wrong"   if opt == ls["riddle_selected"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if ls["riddle_answered"]:
            if ls["riddle_selected"] == r["ans"]:
                show_correct_feedback(1)
            else:
                show_wrong_feedback(r["ans"], "Think about what the object does, not what it looks like!")

            if st.button("🔮 Next Riddle", use_container_width=True, key="logic_next_riddle"):
                used = ls.get("riddle_used", [])
                used.append(ls["riddle_idx"])
                remaining = [i for i in range(len(RIDDLES)) if i not in used]
                if not remaining:
                    used = []
                    remaining = list(range(len(RIDDLES)))
                ls["riddle_idx"]      = random.choice(remaining)
                ls["riddle_used"]     = used
                ls["riddle_answered"] = False
                ls["riddle_selected"] = None
                st.rerun()

    # ── Tab 3: Sort & Order ────────────────────────────────────────────────────
    with tab3:
        st.markdown("<div style='color:#fff; font-weight:800; font-size:18px; margin-bottom:16px'>📊 Put them in the right order!</div>", unsafe_allow_html=True)

        if "sort_idx" not in ls:
            ls["sort_idx"]   = 0
            ls["sort_order"] = []

        sg = SORTING_GAMES[ls["sort_idx"] % len(SORTING_GAMES)]
        st.markdown(f"""
        <div style='color:#ffd700; font-weight:800; font-size:16px; margin-bottom:4px'>{sg['title']}</div>
        <div style='color:rgba(255,255,255,0.5); font-size:13px; margin-bottom:16px'>Hint: {sg['hint']}</div>
        """, unsafe_allow_html=True)

        items = sg["items"]
        selections = []
        for rank in range(1, len(items)+1):
            sel = st.selectbox(f"Position {rank}", ["-- Select --"] + items, key=f"sort_{rank}_{ls['sort_idx']}")
            selections.append(sel)

        if st.button("✅ Check Order!", use_container_width=True, key="logic_check_order"):
            if "-- Select --" in selections:
                st.warning("Please fill all positions!")
            elif selections == sg["correct"]:
                award_logic(3, 25, "📊 Sort Savant")
                st.balloons()
                st.success("🎉 Perfect order! You're a sorting superstar!")
                ls["sort_idx"] += 1
                for r in range(1, len(items)+1):
                    if f"sort_{r}_{ls['sort_idx']-1}" in st.session_state:
                        del st.session_state[f"sort_{r}_{ls['sort_idx']-1}"]
                st.rerun()
            else:
                st.error(f"Not quite! Correct order: {' → '.join(sg['correct'])}")