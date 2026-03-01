import streamlit as st
import random

# ─── Question Bank ─────────────────────────────────────────────────────────────
PHONICS_QUESTIONS = {
    "easy": [
        {"q": "Which word starts with the sound 'B'?",       "opts": ["Cat","Ball","Dog","Fish"],      "ans": "Ball",  "img": "🎱"},
        {"q": "Which word rhymes with 'CAT'?",               "opts": ["Dog","Hat","Sun","Cup"],        "ans": "Hat",   "img": "🎩"},
        {"q": "What letter does 'Apple' start with?",        "opts": ["B","C","A","D"],                "ans": "A",     "img": "🍎"},
        {"q": "Which word starts with 'S'?",                 "opts": ["Panda","Tiger","Snake","Lion"], "ans": "Snake", "img": "🐍"},
        {"q": "Which word rhymes with 'SUN'?",               "opts": ["Moon","Run","Star","Cloud"],    "ans": "Run",   "img": "☀️"},
        {"q": "What letter does 'Dog' start with?",          "opts": ["C","D","E","F"],                "ans": "D",     "img": "🐶"},
        {"q": "Which word starts with the sound 'M'?",       "opts": ["Tiger","Moon","Sun","Rain"],    "ans": "Moon",  "img": "🌙"},
        {"q": "What letter does 'Fish' start with?",         "opts": ["E","F","G","H"],                "ans": "F",     "img": "🐟"},
    ],
    "medium": [
        {"q": "Which word has the long 'A' sound?",          "opts": ["Cat","Bat","Cake","Map"],       "ans": "Cake",  "img": "🎂"},
        {"q": "How many syllables in 'BUTTERFLY'?",          "opts": ["1","2","3","4"],                "ans": "3",     "img": "🦋"},
        {"q": "Which word ends with the 'ight' sound?",      "opts": ["Bright","Boat","Brown","Blue"], "ans": "Bright","img": "💡"},
        {"q": "What vowel is in the middle of 'SHIP'?",      "opts": ["A","E","I","O"],                "ans": "I",     "img": "🚢"},
        {"q": "Which word has a silent letter?",             "opts": ["Cat","Knife","Dog","Run"],      "ans": "Knife", "img": "🔪"},
        {"q": "How many syllables in 'RAINBOW'?",            "opts": ["1","2","3","4"],                "ans": "2",     "img": "🌈"},
        {"q": "Which word has the short 'E' sound?",         "opts": ["Bed","Ride","Coat","Cube"],     "ans": "Bed",   "img": "🛏️"},
    ],
    "hard": [
        {"q": "Which word uses the 'ph' sound for F?",       "opts": ["Phone","Fence","Fine","Face"],  "ans": "Phone", "img": "📱"},
        {"q": "How many syllables in 'ENCYCLOPEDIA'?",       "opts": ["4","5","6","7"],                "ans": "6",     "img": "📚"},
        {"q": "What does the prefix 'UN' mean?",             "opts": ["Again","Not","Before","Under"], "ans": "Not",   "img": "❌"},
        {"q": "Which word is a compound word?",              "opts": ["Sunflower","Running","Happy","Bright"], "ans": "Sunflower","img": "🌻"},
        {"q": "Which word contains a diphthong?",            "opts": ["Rain","Cat","Sit","Top"],       "ans": "Rain",  "img": "🌧️"},
        {"q": "What does the suffix '-ful' mean?",           "opts": ["Without","Full of","Before","Again"], "ans": "Full of","img": "🌟"},
    ]
}

WORD_MATCH = [
    ("🐱","CAT"),("🐶","DOG"),("🌙","MOON"),("⭐","STAR"),
    ("🌊","WAVE"),("🔥","FIRE"),("🌸","ROSE"),("🌈","RAINBOW"),
    ("🍎","APPLE"),("🐘","ELEPHANT"),("🚀","ROCKET"),("🎈","BALLOON"),
    ("🌻","SUNFLOWER"), ("🎂","CAKE"), ("🌳","TREE"), ("☁️","CLOUD")
]

MOTIVATIONAL_MSGS = [
    ("🌟", "So close! You've got this!", "Every mistake is a step forward!"),
    ("💪", "Don't give up!", "Champions keep trying!"),
    ("🚀", "Almost there!", "One more try — you'll get it!"),
    ("🧠", "Great effort!", "Your brain is growing stronger!"),
    ("🌈", "Keep going!", "Mistakes make us smarter!"),
    ("⭐", "You're learning!", "Every explorer makes mistakes!"),
    ("🎯", "Stay focused!", "The answer is closer than you think!"),
]

def get_difficulty():
    score = st.session_state.skill_scores.get("phonics", 0)
    return "hard" if score >= 70 else "medium" if score >= 40 else "easy"

def award(stars, xp, badge=None):
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.skill_scores["phonics"] = min(
        st.session_state.skill_scores["phonics"] + stars * 4, 100
    )
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

def show_wrong_feedback(correct_answer):
    """Show motivational message with bold wrong answer callout."""
    icon, title, subtitle = random.choice(MOTIVATIONAL_MSGS)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(248,113,113,0.15),rgba(239,68,68,0.08));
        border:2px solid rgba(248,113,113,0.4); border-radius:16px; padding:20px;
        text-align:center; margin:12px 0'>
        <div style='font-size:44px; margin-bottom:8px'>{icon}</div>
        <div style='color:#f87171; font-size:20px; font-weight:900; margin-bottom:4px'>{title}</div>
        <div style='color:rgba(255,255,255,0.7); font-size:14px; margin-bottom:12px'>{subtitle}</div>
        <div style='background:rgba(255,255,255,0.08); border-radius:10px; padding:10px 16px;
            color:#fff; font-size:15px'>
            ✅ The correct answer was: <b style='color:#4ade80; font-size:18px'> {correct_answer}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_correct_feedback(streak):
    """Show celebration message for correct answers."""
    if streak >= 5:
        msg, icon = "🔥 UNSTOPPABLE! 5+ Streak!", "🏆"
    elif streak >= 3:
        msg, icon = f"🔥 x{streak} Streak! On fire!", "🌟"
    else:
        msgs = ["✅ Correct! Brilliant!", "✅ Nailed it!", "✅ Great job, explorer!", "✅ You're a star!"]
        msg, icon = random.choice(msgs), "✨"
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.15),rgba(16,185,129,0.08));
        border:2px solid rgba(74,222,128,0.4); border-radius:16px; padding:16px;
        text-align:center; margin:12px 0'>
        <div style='font-size:36px'>{icon}</div>
        <div style='color:#4ade80; font-size:18px; font-weight:900'>{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Main ──────────────────────────────────────────────────────────────────────
def show_phonics():
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px'>
        <div style='font-size:56px'>🌎</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Planet Phonics</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Master reading, sounds & words!</div>
    </div>
    """, unsafe_allow_html=True)

    skill = st.session_state.skill_scores.get("phonics", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px'>
        <div style='color:rgba(255,255,255,0.5);font-size:13px;margin-bottom:6px'>Phonics Mastery</div>
        <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:12px;max-width:400px;margin:0 auto'>
            <div style='width:{skill}%;height:12px;border-radius:50px;
                background:linear-gradient(90deg,#f093fb,#f5576c)'></div>
        </div>
        <div style='color:#fff;font-weight:700;margin-top:6px'>{skill}% Mastered</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🎯 Sound Quiz","🔤 Word Match","📖 Story Mode"])
    qs = st.session_state.quiz_state

    # ── Tab 1: Sound Quiz ──────────────────────────────────────────────────────
    with tab1:
        diff = get_difficulty()
        pool = PHONICS_QUESTIONS[diff]

        # ── Reset / init question state cleanly ──
        if "ph_q_idx" not in qs or qs.get("ph_diff") != diff:
            qs["ph_used"]      = []
            qs["ph_q_idx"]     = 0
            qs["ph_diff"]      = diff
            qs["ph_answered"]  = False
            qs["ph_selected"]  = None
            qs["ph_streak"]    = qs.get("ph_streak", 0)
            qs["ph_score"]     = qs.get("ph_score",  0)

        # Guard index
        if qs["ph_q_idx"] >= len(pool):
            qs["ph_q_idx"] = 0

        q = pool[qs["ph_q_idx"]]

        # Shuffle options once per question (stable seed)
        rng = random.Random(qs["ph_q_idx"] * 137 + len(diff))
        opts = q["opts"][:]
        rng.shuffle(opts)

        st.markdown(f"""
        <div class='question-box'>
            <div style='font-size:48px;margin-bottom:12px'>{q['img']}</div>
            <div style='font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:8px'>
                Difficulty: {diff.upper()} | Streak: 🔥{qs.get('ph_streak',0)} | Score: ⭐{qs.get('ph_score',0)}
            </div>
            {q['q']}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, opt in enumerate(opts):
            with cols[i % 2]:
                if not qs["ph_answered"]:
                    if st.button(opt, key=f"ph_opt_{qs['ph_q_idx']}_{i}", use_container_width=True):
                        qs["ph_selected"] = opt
                        qs["ph_answered"] = True
                        if opt == q["ans"]:
                            qs["ph_streak"] = qs.get("ph_streak",0) + 1
                            qs["ph_score"]  = qs.get("ph_score",0)  + 1
                            stars = 2 if qs["ph_streak"] >= 3 else 1
                            award(stars, 15, "📖 Phonics Star" if qs["ph_score"] >= 5 else None)
                        else:
                            qs["ph_streak"] = 0
                        st.rerun()
                else:
                    css = "answer-correct" if opt == q["ans"] else (
                          "answer-wrong"   if opt == qs["ph_selected"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if qs["ph_answered"]:
            if qs["ph_selected"] == q["ans"]:
                show_correct_feedback(qs.get("ph_streak", 1))
            else:
                show_wrong_feedback(q["ans"])

            if st.button("➡️ Next Question", use_container_width=True, key="ph_next"):
                used = qs.get("ph_used", [])
                used.append(qs["ph_q_idx"])
                new_diff = get_difficulty()
                new_pool = PHONICS_QUESTIONS[new_diff]
                # Reset used list when all questions exhausted
                remaining = [i for i in range(len(new_pool)) if i not in used or new_diff != diff]
                if not remaining or new_diff != diff:
                    used = []
                    remaining = list(range(len(new_pool)))
                qs["ph_q_idx"]   = random.choice(remaining)
                qs["ph_used"]    = used
                qs["ph_diff"]    = new_diff
                qs["ph_answered"] = False
                qs["ph_selected"] = None
                st.rerun()

    # ── Tab 2: Word Match ──────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:16px'>🔤 Match the Emoji to the Word!</div>", unsafe_allow_html=True)

        if "wm_pairs" not in qs:
            qs["wm_pairs"]   = random.sample(WORD_MATCH, 5)
            qs["wm_answers"] = {}

        pairs  = qs["wm_pairs"]
        answers = qs["wm_answers"]
        words  = [p[1] for p in pairs]
        random.Random(99).shuffle(words)

        cols = st.columns(2)
        for i, (emoji, word) in enumerate(pairs):
            with cols[i % 2]:
                st.markdown(f"<div style='color:#fff;font-size:24px;margin-bottom:4px'>{emoji}</div>", unsafe_allow_html=True)
                chosen = st.selectbox(f"Match {emoji}", ["-- Select --"] + words, key=f"wm_{i}")
                if chosen != "-- Select --":
                    answers[emoji] = chosen
                    if chosen == word:
                        st.markdown("<span style='color:#4ade80;font-size:12px'>✓ Correct!</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:#f87171;font-size:12px'>✗ Try again</span>", unsafe_allow_html=True)

        if st.button("✅ Check Answers", use_container_width=True):
            score = sum(1 for emoji, word in pairs if answers.get(emoji) == word)
            if score == len(pairs):
                award(3, 30, "🏆 Word Wizard")
                st.balloons()
                st.success(f"🎉 Perfect! {score}/{len(pairs)} correct! +3 Stars!")
            else:
                award(score, score * 5)
                wrong_ones = [f"{e}→{w}" for e, w in pairs if answers.get(e) != w]
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,rgba(248,113,113,0.15),rgba(239,68,68,0.08));
                    border:2px solid rgba(248,113,113,0.4);border-radius:16px;padding:20px;text-align:center'>
                    <div style='font-size:40px'>💪</div>
                    <div style='color:#f87171;font-weight:900;font-size:18px'>You got {score}/{len(pairs)}!</div>
                    <div style='color:rgba(255,255,255,0.7);font-size:13px;margin-top:6px'>Keep practicing — you're getting better!</div>
                </div>
                """, unsafe_allow_html=True)
            qs.pop("wm_pairs",   None)
            qs.pop("wm_answers", None)

    # ── Tab 3: Story Mode ──────────────────────────────────────────────────────
    with tab3:
        stories = [
            {"title":"The Little Star ⭐","text":"Once upon a time, a little star named **Blink** lived in the sky. Every night, Blink would shine bright to help kids find their way home.","q":"What was the star's name?","opts":["Twinkle","Blink","Spark","Flash"],"ans":"Blink"},
            {"title":"The Brave Ant 🐜",  "text":"Buda was the **smallest** ant in the colony but had the **biggest** heart. One day, Buda carried a crumb 100 times bigger than himself!","q":"What did Buda carry?","opts":["A leaf","A crumb","A rock","A seed"],"ans":"A crumb"},
            {"title":"The Magic Tree 🌳", "text":"Deep in the forest grew a tree whose leaves changed color with every **season**. In winter, its leaves turned pure **silver**.","q":"What color were the leaves in winter?","opts":["Gold","Red","Silver","Blue"],"ans":"Silver"},
            {"title":"The Cloud Painter ☁️","text":"High above, a cloud painter named **Nimbus** painted shapes in the sky every morning. One day, he painted a giant **dragon**.","q":"What did Nimbus paint one day?","opts":["A dragon","A castle","A ship","A bird"],"ans":"A dragon"},
            {"title":"The Big Elephant 🐘","text":"In the woods, A big Elephant named as **Jumbo** lived and it tends to eat a lot of **leaves**. People in the forest loved him for his cuteness and innocence.", "q":"What did the big elephant eat?", "opts":["Flowers","Leaves","Fruits","Vegetables"],"ans":"Leaves"}
        ]

        if "story_idx" not in qs:
            qs["story_idx"]    = 0
            qs["story_ans"]    = None
            qs["story_answered"] = False

        story = stories[qs["story_idx"] % len(stories)]

        st.markdown(f"""
        <div class='question-box' style='text-align:left;font-size:16px;line-height:1.7'>
            <div style='font-size:20px;font-weight:900;margin-bottom:12px'>{story['title']}</div>
            {story['text']}
        </div>
        <div style='color:#fff;font-weight:700;font-size:17px;margin-bottom:12px'>❓ {story['q']}</div>
        """, unsafe_allow_html=True)

        scols = st.columns(2)
        for i, opt in enumerate(story["opts"]):
            with scols[i % 2]:
                if not qs.get("story_answered"):
                    if st.button(opt, key=f"story_{qs['story_idx']}_{i}"):
                        qs["story_ans"]      = opt
                        qs["story_answered"] = True
                        if opt == story["ans"]:
                            award(2, 20, "📚 Story Reader")
                        st.rerun()
                else:
                    css = "answer-correct" if opt == story["ans"] else (
                          "answer-wrong"   if opt == qs["story_ans"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if qs.get("story_answered"):
            if qs["story_ans"] == story["ans"]:
                show_correct_feedback(1)
            else:
                show_wrong_feedback(story["ans"])

        if st.button("📖 Next Story", key="story_next"):
            qs["story_idx"]    = qs.get("story_idx", 0) + 1
            qs["story_ans"]    = None
            qs["story_answered"] = False
            st.rerun()