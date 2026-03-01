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
    hint_html = f"<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-top:8px'>💡 {hint}</div>" if hint else ""
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
    elif streak >= 3: msg, icon = f"🔥 x{streak} Streak! Science genius!", "🌟"
    else:
        choices = [("✅ Correct! Great scientist!","🔬"),("✅ Nailed it, explorer!","🚀"),("✅ Brilliant!","⭐")]
        msg, icon = random.choice(choices)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.15),rgba(16,185,129,0.08));
        border:2px solid rgba(74,222,128,0.4);border-radius:16px;padding:16px;
        text-align:center;margin:12px 0'>
        <div style='font-size:36px'>{icon}</div>
        <div style='color:#4ade80;font-size:18px;font-weight:900'>{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Question Bank ─────────────────────────────────────────────────────────────
SCIENCE_QUESTIONS = {
    "easy": [
        {"q": "What do plants need to grow?",       "opts": ["Sunlight & Water","Only Soil","Just Air","Darkness"],      "ans": "Sunlight & Water", "img": "🌱"},
        {"q": "What gives the sky its blue color?", "opts": ["Water","Light scattering","Paint","Clouds"],               "ans": "Light scattering",  "img": "🌤"},
        {"q": "What do caterpillars turn into?",    "opts": ["Birds","Bees","Butterflies","Spiders"],                    "ans": "Butterflies",       "img": "🦋"},
        {"q": "Which planet do we live on?",        "opts": ["Mars","Venus","Earth","Jupiter"],                          "ans": "Earth",             "img": "🌍"},
        {"q": "What is the closest star to Earth?", "opts": ["Moon","Sun","Venus","Mars"],                               "ans": "Sun",               "img": "☀️"},
        {"q": "What gas do humans breathe in?",     "opts": ["Carbon Dioxide","Nitrogen","Oxygen","Hydrogen"],           "ans": "Oxygen",            "img": "💨"},
    ],
    "medium": [
        {"q": "What force pulls objects toward Earth?",         "opts": ["Magnetism","Gravity","Friction","Wind"],           "ans": "Gravity",        "img": "🍎"},
        {"q": "What are clouds made of?",                       "opts": ["Cotton","Water droplets","Smoke","Gas"],           "ans": "Water droplets", "img": "☁️"},
        {"q": "Which animal is a mammal?",                      "opts": ["Shark","Eagle","Dolphin","Frog"],                  "ans": "Dolphin",        "img": "🐬"},
        {"q": "What process do plants use to make food?",       "opts": ["Respiration","Photosynthesis","Digestion","Osmosis"], "ans": "Photosynthesis","img": "🍃"},
        {"q": "How many bones does an adult human have?",       "opts": ["106","206","306","406"],                           "ans": "206",            "img": "🦴"},
    ],
    "hard": [
        {"q": "What is the chemical symbol for water?",         "opts": ["WA","HO","H2O","W2O"],                             "ans": "H2O",            "img": "💧"},
        {"q": "Which planet has the most moons?",               "opts": ["Jupiter","Saturn","Uranus","Neptune"],              "ans": "Saturn",         "img": "🪐"},
        {"q": "What is the powerhouse of the cell?",            "opts": ["Nucleus","Ribosome","Mitochondria","Vacuole"],      "ans": "Mitochondria",   "img": "🔬"},
        {"q": "Light travels at approximately how many km/s?",  "opts": ["100,000","300,000","500,000","1,000,000"],          "ans": "300,000",        "img": "💡"},
        {"q": "What layer of Earth do we live on?",             "opts": ["Mantle","Core","Crust","Magma"],                   "ans": "Crust",          "img": "🌋"},
    ]
}

EXPERIMENTS = [
    {"title": "🌈 Color Mixing Lab", "desc": "Discover what happens when you mix colors!", "type": "color_mix"},
    {"title": "⚖️ Sink or Float?",   "desc": "Predict if objects sink or float in water!", "type": "sink_float"},
    {"title": "🌡️ Hot or Cold?",     "desc": "Sort materials by how they conduct heat!",   "type": "hot_cold"},
]

# ─── Color Mix Data ────────────────────────────────────────────────────────────
# Each entry: c1, c2, result, emoji, 3 UNIQUE wrong distractors
# Distractors are carefully chosen — plausible but wrong for that specific mix.
COLOR_MIX = [
    {"c1":"🔴 Red",         "c2":"🔵 Blue",        "result":"Purple",     "emoji":"🟣",
     "wrong":["Green","Orange","Brown"]},
    {"c1":"🔴 Red",         "c2":"🟡 Yellow",      "result":"Orange",     "emoji":"🟠",
     "wrong":["Purple","Pink","Brown"]},
    {"c1":"🔵 Blue",        "c2":"🟡 Yellow",      "result":"Green",      "emoji":"🟢",
     "wrong":["Purple","Orange","Teal"]},
    {"c1":"🔴 Red",         "c2":"⚪ White",       "result":"Pink",       "emoji":"🩷",
     "wrong":["Purple","Peach","Magenta"]},
    {"c1":"🔵 Blue",        "c2":"⚪ White",       "result":"Light Blue", "emoji":"🩵",
     "wrong":["Cyan","Teal","Lavender"]},
    {"c1":"🟡 Yellow",      "c2":"⚪ White",       "result":"Cream",      "emoji":"🟨",
     "wrong":["Beige","Peach","Ivory"]},
    {"c1":"🔴 Red",         "c2":"⚫ Black",       "result":"Dark Red",   "emoji":"🟥",
     "wrong":["Maroon","Brown","Purple"]},
    {"c1":"🔵 Blue",        "c2":"⚫ Black",       "result":"Dark Blue",  "emoji":"🟦",
     "wrong":["Navy","Indigo","Purple"]},
    {"c1":"🟡 Yellow",      "c2":"⚫ Black",       "result":"Dark Green", "emoji":"🟩",
     "wrong":["Olive","Brown","Khaki"]},
    {"c1":"🟣 Purple",      "c2":"⚪ White",       "result":"Violet",     "emoji":"🟣",
     "wrong":["Lavender","Lilac","Pink"]},
    {"c1":"🔵 Blue",        "c2":"🟠 Orange",      "result":"Brown",      "emoji":"🟫",
     "wrong":["Grey","Green","Maroon"]},
    {"c1":"🔴 Red",         "c2":"🟢 Green",       "result":"Brown",      "emoji":"🟫",
     "wrong":["Black","Olive","Orange"]},
    {"c1":"⚫ Black",       "c2":"⚪ White",       "result":"Grey",       "emoji":"🩶",
     "wrong":["Silver","Beige","Lavender"]},
    {"c1":"🟡 Yellow",      "c2":"🟫 Brown",       "result":"Gold",       "emoji":"🟨",
     "wrong":["Amber","Tan","Khaki"]},
    {"c1":"🟣 Purple",      "c2":"🔴 Red",         "result":"Magenta",    "emoji":"🟥",
     "wrong":["Maroon","Crimson","Orange"]},
    {"c1":"🔵 Blue",        "c2":"🟣 Purple",      "result":"Indigo",     "emoji":"🟦",
     "wrong":["Violet","Navy","Dark Blue"]},
]

SINK_FLOAT = [
    {"item":"🪨 Rock",  "ans":"Sinks",  "reason":"Rocks are dense and heavy"},
    {"item":"🪵 Wood",  "ans":"Floats", "reason":"Wood is less dense than water"},
    {"item":"🪙 Coin",  "ans":"Sinks",  "reason":"Metal is denser than water"},
    {"item":"🍎 Apple", "ans":"Floats", "reason":"Apples have air pockets inside"},
    {"item":"🏐 Ball",  "ans":"Floats", "reason":"Air-filled objects float"},
    {"item":"⚙️ Bolt",  "ans":"Sinks",  "reason":"Metal bolts are very dense"},
    {"item":"🧊 Ice",   "ans":"Floats", "reason":"Ice is less dense than liquid water"},
    {"item":"🧲 Magnet","ans":"Sinks",  "reason":"Magnets are made of heavy metal"},
]

HOT_COLD = [
    {"m":"🪨 Rock",    "heat":"Conductor", "reason":"Rocks absorb and transfer heat well"},
    {"m":"🧤 Wool",    "heat":"Insulator",  "reason":"Wool fibres trap air and keep heat in"},
    {"m":"🔩 Metal",   "heat":"Conductor", "reason":"Metals have free electrons that carry heat quickly"},
    {"m":"🪵 Wood",    "heat":"Insulator",  "reason":"Wood has tiny air pockets making it a poor conductor"},
    {"m":"🟤 Copper",  "heat":"Conductor", "reason":"Copper is excellent at conducting heat — used in cookware & wires"},
    {"m":"📄 Paper",   "heat":"Insulator",  "reason":"Paper is a poor conductor and burns before transferring heat"},
    {"m":"🧴 Plastic", "heat":"Insulator",  "reason":"Plastic melts rather than conducting heat, making it a poor conductor"},
    {"m":"💎 Glass",   "heat":"Insulator",  "reason":"Glass is a poor conductor — that's why we use it for windows"},
    {"m":"🥄 Silver",  "heat":"Conductor", "reason":"Silver is the best natural conductor of heat and electricity"},
]

def get_diff():
    s = st.session_state.skill_scores.get("science", 0)
    return "hard" if s >= 70 else "medium" if s >= 40 else "easy"

def award_science(stars, xp, badge=None):
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.skill_scores["science"] = min(
        st.session_state.skill_scores["science"] + stars * 4, 100
    )
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

# ─── Main ──────────────────────────────────────────────────────────────────────
def show_science():
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px'>
        <div style='font-size:56px'>🔬</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Science Lab World</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Experiment, discover & understand nature!</div>
    </div>
    """, unsafe_allow_html=True)

    skill = st.session_state.skill_scores.get("science", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px'>
        <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:12px;max-width:400px;margin:0 auto'>
            <div style='width:{skill}%;height:12px;border-radius:50px;
                background:linear-gradient(90deg,#43e97b,#38f9d7)'></div>
        </div>
        <div style='color:#fff;font-weight:700;margin-top:6px'>{skill}% Mastered</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔭 Science Quiz","🧪 Experiments","🌍 Solar System"])
    ss = st.session_state.quiz_state

    # ── Tab 1: Science Quiz ────────────────────────────────────────────────────
    with tab1:
        diff = get_diff()
        pool = SCIENCE_QUESTIONS[diff]

        if "sci_idx" not in ss or ss.get("sci_diff") != diff:
            ss["sci_idx"]      = 0
            ss["sci_used"]     = []
            ss["sci_diff"]     = diff
            ss["sci_answered"] = False
            ss["sci_selected"] = None
            ss["sci_score"]    = ss.get("sci_score",  0)
            ss["sci_streak"]   = ss.get("sci_streak", 0)

        if ss["sci_idx"] >= len(pool):
            ss["sci_idx"] = 0

        q = pool[ss["sci_idx"]]
        rng = random.Random(ss["sci_idx"] * 91 + len(diff))
        opts = q["opts"][:]
        rng.shuffle(opts)

        st.markdown(f"""
        <div class='question-box'>
            <div style='font-size:48px;margin-bottom:12px'>{q['img']}</div>
            <div style='font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:8px'>
                {diff.upper()} | 🔥{ss.get('sci_streak',0)} Streak | ⭐{ss.get('sci_score',0)}
            </div>
            {q['q']}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, opt in enumerate(opts):
            with cols[i % 2]:
                if not ss["sci_answered"]:
                    if st.button(opt, key=f"sci_{ss['sci_idx']}_{i}", use_container_width=True):
                        ss["sci_selected"] = opt
                        ss["sci_answered"] = True
                        if opt == q["ans"]:
                            ss["sci_streak"] = ss.get("sci_streak",0) + 1
                            ss["sci_score"]  = ss.get("sci_score",0)  + 1
                            award_science(2 if ss["sci_streak"]>=3 else 1, 15,
                                          "🔬 Science Genius" if ss["sci_score"]>=5 else None)
                        else:
                            ss["sci_streak"] = 0
                        st.rerun()
                else:
                    css = "answer-correct" if opt==q["ans"] else ("answer-wrong" if opt==ss["sci_selected"] else "")
                    st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

        if ss["sci_answered"]:
            if ss["sci_selected"] == q["ans"]:
                show_correct_feedback(ss.get("sci_streak", 1))
            else:
                show_wrong_feedback(q["ans"])

            if st.button("➡️ Next Question", use_container_width=True, key="sci_next"):
                used = ss.get("sci_used", [])
                used.append(ss["sci_idx"])
                new_diff = get_diff()
                new_pool = SCIENCE_QUESTIONS[new_diff]
                remaining = [i for i in range(len(new_pool)) if i not in used or new_diff != diff]
                if not remaining or new_diff != diff:
                    used = []
                    remaining = list(range(len(new_pool)))
                ss["sci_idx"]      = random.choice(remaining)
                ss["sci_used"]     = used
                ss["sci_diff"]     = new_diff
                ss["sci_answered"] = False
                ss["sci_selected"] = None
                st.rerun()

    # ── Tab 2: Experiments ─────────────────────────────────────────────────────
    with tab2:
        exp_choice = st.selectbox("Choose your experiment", [e["title"] for e in EXPERIMENTS])
        exp = next(e for e in EXPERIMENTS if e["title"] == exp_choice)
        st.markdown(f"<div style='color:rgba(255,255,255,0.6);font-size:14px;margin-bottom:20px'>{exp['desc']}</div>",
                    unsafe_allow_html=True)

        # ── Color Mixing Lab ───────────────────────────────────────────────────
        if exp["type"] == "color_mix":
            st.markdown("<div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>🎨 Mix two colors — what do you get?</div>", unsafe_allow_html=True)

            if "cm_idx"      not in ss: ss["cm_idx"]      = 0
            if "cm_answered" not in ss: ss["cm_answered"] = False
            if "cm_selected" not in ss: ss["cm_selected"] = None

            # Cycle through COLOR_MIX entries
            cm_entry = COLOR_MIX[ss["cm_idx"] % len(COLOR_MIX)]

            # ── Display the two colours being mixed ──
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f"""
                <div class='planet-card' style='padding:20px'>
                    <div style='font-size:40px'>{cm_entry['emoji'] if cm_entry['c1'].startswith(('🔴','🔵','🟡','⚪','⚫','🟣','🟠','🟢','🟫')) else '🎨'}</div>
                    <div style='color:#fff;font-weight:800;font-size:16px;margin-top:6px'>{cm_entry['c1']}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown("<div style='color:#fff;font-size:36px;text-align:center;padding-top:28px'>➕</div>",
                            unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='planet-card' style='padding:20px'>
                    <div style='font-size:40px'>🎨</div>
                    <div style='color:#fff;font-weight:800;font-size:16px;margin-top:6px'>{cm_entry['c2']}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("""
            <div style='color:#fff;font-weight:700;font-size:20px;text-align:center;margin:20px 0 8px'>
                = ❓ What color do you get?
            </div>
            """, unsafe_allow_html=True)

            # ── Build 4 options: correct + 3 unique wrong distractors ──
            correct  = cm_entry["result"]
            wrongs   = cm_entry["wrong"][:3]          # always exactly 3 per entry
            all_opts = [correct] + wrongs
            # Stable shuffle so options don't jump on rerun
            rng_cm   = random.Random(ss["cm_idx"] * 53)
            rng_cm.shuffle(all_opts)

            ccols = st.columns(2)
            for i, opt in enumerate(all_opts):
                with ccols[i % 2]:
                    if not ss["cm_answered"]:
                        if st.button(opt, key=f"cm_opt_{ss['cm_idx']}_{i}", use_container_width=True):
                            ss["cm_selected"] = opt
                            ss["cm_answered"] = True
                            if opt == correct:
                                award_science(1, 10, "🌈 Color Scientist")
                            st.rerun()
                    else:
                        css = "answer-correct" if opt == correct else (
                              "answer-wrong"   if opt == ss["cm_selected"] else "")
                        st.markdown(f"<div class='answer-btn {css}'>{opt}</div>", unsafe_allow_html=True)

            # ── Feedback ──
            if ss["cm_answered"]:
                if ss["cm_selected"] == correct:
                    st.balloons()
                    show_correct_feedback(1)
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.06);border-radius:12px;padding:12px 16px;
                        color:#fff;font-size:14px;text-align:center;margin-top:8px'>
                        🎨 <b>{cm_entry['c1']}</b> + <b>{cm_entry['c2']}</b>
                        = <b style='color:#ffd700'>{cm_entry['emoji']} {correct}</b>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    show_wrong_feedback(correct, f"{cm_entry['c1']} + {cm_entry['c2']} = {cm_entry['emoji']} {correct}")

                if st.button("🎨 Next Mix!", use_container_width=True, key="cm_next"):
                    ss["cm_idx"]      += 1
                    ss["cm_answered"]  = False
                    ss["cm_selected"]  = None
                    st.rerun()

        # ── Sink or Float ──────────────────────────────────────────────────────
        elif exp["type"] == "sink_float":
            st.markdown("<div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>🌊 Will it sink or float?</div>",
                        unsafe_allow_html=True)

            if "sf_idx"      not in ss: ss["sf_idx"]      = 0
            if "sf_answered" not in ss: ss["sf_answered"] = False

            sf = SINK_FLOAT[ss["sf_idx"] % len(SINK_FLOAT)]

            st.markdown(f"""
            <div class='question-box'>
                <div style='font-size:56px'>{sf['item'].split()[0]}</div>
                <div style='margin-top:12px'>Drop <b>{sf['item']}</b> in water...<br>
                <span style='font-size:20px;font-weight:900'>Will it Sink or Float?</span></div>
            </div>
            """, unsafe_allow_html=True)

            if not ss["sf_answered"]:
                sc1, sc2 = st.columns(2)
                for label, col in [("⬇️ Sinks", sc1), ("⬆️ Floats", sc2)]:
                    with col:
                        if st.button(label, key=f"sf_{ss['sf_idx']}_{label}", use_container_width=True):
                            chosen = "Sinks" if "Sinks" in label else "Floats"
                            ss["sf_chosen"]  = chosen
                            ss["sf_answered"] = True
                            if chosen == sf["ans"]:
                                award_science(1, 10)
                            st.rerun()
            else:
                if ss["sf_chosen"] == sf["ans"]:
                    show_correct_feedback(1)
                    st.success(f"✅ **{sf['item']}** {sf['ans'].lower()}! {sf['reason']}.")
                else:
                    show_wrong_feedback(sf["ans"], sf["reason"])
                if st.button("🌊 Next Object!", use_container_width=True):
                    ss["sf_idx"]     += 1
                    ss["sf_answered"] = False
                    ss.pop("sf_chosen", None)
                    st.rerun()

        # ── Hot or Cold ────────────────────────────────────────────────────────
        elif exp["type"] == "hot_cold":
            st.markdown("<div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>🌡️ Is it a Heat Conductor or Insulator?</div>",
                        unsafe_allow_html=True)

            if "hc_idx"      not in ss: ss["hc_idx"]      = 0
            if "hc_answered" not in ss: ss["hc_answered"] = False

            hc = HOT_COLD[ss["hc_idx"] % len(HOT_COLD)]

            st.markdown(f"""
            <div class='question-box'>
                <div style='font-size:48px'>{hc['m'].split()[0]}</div>
                <div style='margin-top:12px'>Is <b>{hc['m']}</b> a heat<br>
                <span style='font-size:20px;font-weight:900'>Conductor or Insulator?</span></div>
            </div>
            """, unsafe_allow_html=True)

            if not ss["hc_answered"]:
                h1, h2 = st.columns(2)
                for label, col in [("🔥 Conductor", h1), ("❄️ Insulator", h2)]:
                    with col:
                        if st.button(label, key=f"hc_{ss['hc_idx']}_{label}", use_container_width=True):
                            chosen = "Conductor" if "Conductor" in label else "Insulator"
                            ss["hc_chosen"]  = chosen
                            ss["hc_answered"] = True
                            if chosen == hc["heat"]:
                                award_science(1, 10)
                            st.rerun()
            else:
                if ss["hc_chosen"] == hc["heat"]:
                    show_correct_feedback(1)
                    st.success(f"✅ Correct! **{hc['m']}** is a **{hc['heat']}**. {hc['reason']}.")
                else:
                    show_wrong_feedback(hc["heat"], hc["reason"])
                if st.button("🌡️ Next Material!", use_container_width=True):
                    ss["hc_idx"]     += 1
                    ss["hc_answered"] = False
                    ss.pop("hc_chosen", None)
                    st.rerun()

    # ── Tab 3: Solar System ────────────────────────────────────────────────────
    with tab3:
        PLANETS = [
            {"name":"Mercury","icon":"⚫","fact":"Smallest planet, closest to Sun",              "temp":"430°C / -180°C","moons":0},
            {"name":"Venus",  "icon":"🟡","fact":"Hottest planet — hotter than Mercury!",        "temp":"465°C",         "moons":0},
            {"name":"Earth",  "icon":"🌍","fact":"Only planet with known life!",                 "temp":"15°C avg",      "moons":1},
            {"name":"Mars",   "icon":"🔴","fact":"Has the tallest volcano — Olympus Mons",       "temp":"-65°C avg",     "moons":2},
            {"name":"Jupiter","icon":"🟠","fact":"Largest planet — 1,300 Earths fit inside!",    "temp":"-110°C",        "moons":95},
            {"name":"Saturn", "icon":"🪐","fact":"Has spectacular rings of ice & rock",          "temp":"-140°C",        "moons":146},
            {"name":"Uranus", "icon":"🔵","fact":"Rotates on its side — totally unique!",        "temp":"-195°C",        "moons":28},
            {"name":"Neptune","icon":"🟣","fact":"Strongest winds in the solar system",          "temp":"-200°C",        "moons":16},
        ]
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:16px'>🌌 Explore the Solar System!</div>",
                    unsafe_allow_html=True)
        pcols = st.columns(4)
        for i, p in enumerate(PLANETS):
            with pcols[i % 4]:
                st.markdown(f"""
                <div class='planet-card' style='padding:16px'>
                    <div style='font-size:32px'>{p['icon']}</div>
                    <div style='color:#fff;font-weight:800;font-size:15px'>{p['name']}</div>
                    <div style='color:rgba(255,255,255,0.5);font-size:11px;margin-top:6px'>{p['fact']}</div>
                    <div style='color:#ffd700;font-size:11px;margin-top:4px'>🌡 {p['temp']}</div>
                    <div style='color:rgba(255,255,255,0.4);font-size:11px'>🌕 {p['moons']} moon(s)</div>
                </div>
                """, unsafe_allow_html=True)