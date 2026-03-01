import streamlit as st
import random

STORY_STARTERS = [
    "One rainy morning, a tiny dragon found a glowing egg in the forest...",
    "The robot opened its eyes for the first time and saw a world full of colors...",
    "Deep under the ocean, a mermaid discovered a door that led to the sky...",
    "A young inventor built a machine that could talk to animals...",
    "When the stars disappeared one night, only one brave child knew why...",
    "The magic backpack could hold anything — even things bigger than itself...",
]

WORD_PROMPTS = [
    ["Castle","Dragon","Moonlight","Secret","Adventure"],
    ["Ocean","Treasure","Storm","Compass","Brave"],
    ["Forest","Fairy","Spell","Laughter","Magic"],
    ["Space","Robot","Planet","Discovery","Friend"],
    ["Mountain","Eagle","Quest","Legend","Courage"],
]

DRAW_PROMPTS = [
    {"prompt":"Draw a friendly monster who loves eating rainbows 🌈","icon":"👾"},
    {"prompt":"Draw your dream treehouse with at least 3 special features 🌳","icon":"🏠"},
    {"prompt":"Design a superhero — what's their power? 🦸","icon":"⚡"},
    {"prompt":"Draw an underwater city with its own transportation 🌊","icon":"🏙"},
    {"prompt":"Create a new planet — what does it look like? 🪐","icon":"🌌"},
]

EMOTION_PROMPTS = [
    {"situation":"Your best friend is moving to another city. How do you feel?","icon":"😢"},
    {"situation":"You worked really hard on a project and got a great result! How do you feel?","icon":"🎉"},
    {"situation":"Someone takes credit for your idea. What would you do?","icon":"😤"},
    {"situation":"You see a new kid at school sitting alone. What do you do?","icon":"🤝"},
    {"situation":"You make a mistake in front of everyone. How do you handle it?","icon":"😅"},
]

RHYME_PAIRS = [
    ("Star","Far"), ("Moon","Soon"), ("Tree","Free"),
    ("Day","Play"), ("Night","Bright"), ("Rain","Train"),
    ("Sky","Fly"), ("Sun","Fun"), ("Sea","Be"),
]

def award_creative(stars, xp, badge=None):
    st.session_state.stars += stars
    st.session_state.xp    += xp
    st.session_state.skill_scores["creativity"] = min(
        st.session_state.skill_scores["creativity"] + stars * 3, 100
    )
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

def show_creative():
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px'>
        <div style='font-size:56px'>🎨</div>
        <div style='color:#fff; font-size:32px; font-weight:900'>Creative Island</div>
        <div style='color:rgba(255,255,255,0.6); font-size:15px'>Express yourself through art, stories & imagination!</div>
    </div>
    """, unsafe_allow_html=True)

    skill = st.session_state.skill_scores.get("creativity", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px'>
        <div style='background:rgba(255,255,255,0.1);border-radius:50px;height:12px;max-width:400px;margin:0 auto'>
            <div style='width:{skill}%;height:12px;border-radius:50px;background:linear-gradient(90deg,#fa709a,#fee140)'></div>
        </div>
        <div style='color:#fff;font-weight:700;margin-top:6px'>{skill}% Mastered</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📖 Story Builder", "🎨 Drawing Prompts", "❤️ Emotion Explorer", "🎵 Rhyme Time"])
    cs = st.session_state.quiz_state

    # ── Tab 1: Story Builder ───────────────────────────────────────────────────
    with tab1:
        if "story_starter" not in cs:
            cs["story_starter"]   = random.choice(STORY_STARTERS)
            cs["story_words"]     = random.choice(WORD_PROMPTS)
            cs["story_submitted"] = False

        st.markdown(f"""
        <div class='question-box' style='text-align:left;font-size:16px;line-height:1.8'>
            <div style='color:#ffd700;font-size:12px;font-weight:800;margin-bottom:8px'>✨ YOUR STORY BEGINS...</div>
            <i>{cs['story_starter']}</i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='color:#fff;font-weight:700;margin-bottom:8px'>🎲 Try using these words in your story:</div>", unsafe_allow_html=True)
        word_html = " ".join([f"<span class='badge badge-blue'>{w}</span>" for w in cs["story_words"]])
        st.markdown(word_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        story_text = st.text_area(
            "Continue the story here... ✍️",
            placeholder="Write at least 3 sentences to continue the adventure...",
            height=180,
            key="story_input"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Submit My Story!", use_container_width=True):
                if len(story_text.strip()) >= 30:
                    words_used = sum(1 for w in cs["story_words"] if w.lower() in story_text.lower())
                    bonus = words_used
                    award_creative(2 + bonus, 20 + bonus*5, "📖 Story Weaver")
                    st.balloons()
                    st.success(f"🎉 Amazing story! You used {words_used}/5 prompt words! +{2+bonus} stars!")
                    cs["story_submitted"] = True
                else:
                    st.warning("Write a bit more — at least 3 sentences!")
        with col2:
            if st.button("🔀 New Story Prompt", use_container_width=True):
                cs.pop("story_starter", None)
                cs.pop("story_words", None)
                cs.pop("story_submitted", None)
                st.rerun()

        if cs.get("story_submitted") and story_text:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.06);border-left:4px solid #ffd700;
                border-radius:8px;padding:16px;margin-top:16px;color:#fff;font-size:14px;line-height:1.7'>
                <b style='color:#ffd700'>📜 Your Story:</b><br><br>
                <i>{cs['story_starter']}</i><br><br>{story_text}
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Drawing Prompts ─────────────────────────────────────────────────
    with tab2:
        if "draw_idx" not in cs: cs["draw_idx"] = 0
        dp = DRAW_PROMPTS[cs["draw_idx"] % len(DRAW_PROMPTS)]

        st.markdown(f"""
        <div class='question-box' style='font-size:18px;line-height:1.7'>
            <div style='font-size:56px;margin-bottom:12px'>{dp['icon']}</div>
            <div style='color:#ffd700;font-size:12px;font-weight:800;margin-bottom:8px'>🎨 DRAWING CHALLENGE</div>
            {dp['prompt']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:16px'>Use paper & crayons, or a drawing app — then come back and tell us what you drew!</div>", unsafe_allow_html=True)

        drawing_desc = st.text_input("Describe what you drew in a sentence:", placeholder="I drew a blue monster with three eyes who...")
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            if st.button("🎨 I Finished Drawing!", use_container_width=True):
                if drawing_desc.strip():
                    award_creative(2, 15, "🎨 Creative Artist")
                    st.success("🎉 Wonderful! Your creativity earns 2 Stars! Keep creating!")
                    cs["draw_idx"] += 1
                    st.rerun()
                else:
                    st.warning("Tell us what you drew first!")
        with dcol2:
            if st.button("🔀 Different Prompt", use_container_width=True):
                cs["draw_idx"] += 1
                st.rerun()

        st.markdown("<br><div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>🏆 Drawing Tips:</div>", unsafe_allow_html=True)
        tips = ["Start with basic shapes — circles, squares, triangles",
                "Add details last — eyes, hair, patterns",
                "Use bright colors to make it pop!",
                "Don't worry about 'perfect' — creativity is unique!"]
        for tip in tips:
            st.markdown(f"<div style='color:rgba(255,255,255,0.7);font-size:13px;margin-bottom:6px'>✏️ {tip}</div>", unsafe_allow_html=True)

    # ── Tab 3: Emotion Explorer ────────────────────────────────────────────────
    with tab3:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:8px'>❤️ How would YOU feel?</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:16px'>Understanding emotions helps us be better friends & people!</div>", unsafe_allow_html=True)

        if "emo_idx" not in cs: cs["emo_idx"] = 0
        ep = EMOTION_PROMPTS[cs["emo_idx"] % len(EMOTION_PROMPTS)]

        st.markdown(f"""
        <div class='question-box' style='font-size:17px;line-height:1.7'>
            <div style='font-size:48px;margin-bottom:12px'>{ep['icon']}</div>
            {ep['situation']}
        </div>
        """, unsafe_allow_html=True)

        emotions = ["😊 Happy","😢 Sad","😤 Frustrated","😮 Surprised","😰 Anxious","💪 Determined","🤗 Grateful","😌 Calm"]
        selected_emo = st.multiselect("How would you feel? (Pick all that apply)", emotions, key=f"emo_{cs['emo_idx']}")

        response = st.text_area("What would you do in this situation?", placeholder="I would...", height=100, key=f"emo_resp_{cs['emo_idx']}")

        ecol1, ecol2 = st.columns(2)
        with ecol1:
            if st.button("💭 Share My Thoughts", use_container_width=True):
                if selected_emo and response.strip():
                    award_creative(1, 15, "❤️ Empathy Champion")
                    st.success(f"🌟 Great emotional awareness! You identified: {', '.join(selected_emo)}")
                    st.info("💡 There are no wrong answers here — all feelings are valid!")
                else:
                    st.warning("Select emotions and write your response first!")
        with ecol2:
            if st.button("➡️ Next Situation", use_container_width=True):
                cs["emo_idx"] = cs.get("emo_idx",0) + 1
                st.rerun()

    # ── Tab 4: Rhyme Time ──────────────────────────────────────────────────────
    with tab4:
        st.markdown("<div style='color:#fff;font-weight:800;font-size:18px;margin-bottom:8px'>🎵 Complete the Rhyme!</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:16px'>Poetry and rhymes build language skills in a fun way!</div>", unsafe_allow_html=True)

        if "rhyme_idx" not in cs: cs["rhyme_idx"] = 0
        r = RHYME_PAIRS[cs["rhyme_idx"] % len(RHYME_PAIRS)]

        wrong_opts = [p[1] for p in RHYME_PAIRS if p[1] != r[1]]
        opts = [r[1]] + random.sample(wrong_opts, 3)
        random.shuffle(opts)

        st.markdown(f"""
        <div class='question-box' style='font-size:24px'>
            <div style='font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:8px'>FIND THE RHYME</div>
            🌟 <b style='color:#ffd700'>{r[0]}</b> rhymes with... ?
        </div>
        """, unsafe_allow_html=True)

        rcols = st.columns(4)
        for i, opt in enumerate(opts):
            with rcols[i]:
                if st.button(opt, key=f"rhyme_{i}_{cs['rhyme_idx']}", use_container_width=True):
                    if opt == r[1]:
                        award_creative(1, 10, "🎵 Rhyme Wizard")
                        st.success(f"🎵 Yes! **{r[0]}** and **{r[1]}** rhyme!")
                    else:
                        st.error(f"Not quite! **{r[0]}** rhymes with **{r[1]}**")
                    cs["rhyme_idx"] += 1
                    st.rerun()

        st.markdown("<br><div style='color:#fff;font-weight:800;font-size:16px;margin-bottom:12px'>✍️ Write Your Own Rhyme!</div>", unsafe_allow_html=True)
        own_rhyme = st.text_area("Write 2 lines that rhyme:", placeholder="The sun shines so bright,\nIt fills the world with light!", height=90)
        if st.button("🌟 Submit My Rhyme!", use_container_width=True):
            if len(own_rhyme.strip()) > 10:
                award_creative(2, 20)
                st.balloons()
                st.success("🎉 Beautiful rhyme! +2 Stars for your creativity!")
            else:
                st.warning("Write at least 2 lines!")