import streamlit as st
import time
from backend.generator import generate_with_style

def show():

    # ---------------- SESSION STATE ----------------
    if "prompt_text" not in st.session_state:
        st.session_state.prompt_text = ""

    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""

    # ---------------- HEADER ----------------
    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <h1>🎭 Preset Personalities</h1>
        <p style="color:#64748b;">Choose from carefully crafted writing styles</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- PERSONALITIES ----------------
    PERSONALITIES = {
        "casual": {
            "name": "Casual Friendly",
            "icon": "😊",
            "desc": "Warm and conversational tone.",
            "profile": {
                "avg_sentence_length": 10,
                "formality_score": 0.2,
                "vocabulary_richness": 0.4
            }
        },
        "corporate": {
            "name": "Corporate Professional",
            "icon": "💼",
            "desc": "Formal business communication.",
            "profile": {
                "avg_sentence_length": 16,
                "formality_score": 0.7,
                "vocabulary_richness": 0.6
            }
        },
        "academic": {
            "name": "Formal Academic",
            "icon": "🎓",
            "desc": "Scholarly academic writing.",
            "profile": {
                "avg_sentence_length": 22,
                "formality_score": 0.9,
                "vocabulary_richness": 0.8
            }
        },
        "motivational": {
            "name": "Motivational Speaker",
            "icon": "🚀",
            "desc": "Energetic and inspiring tone.",
            "profile": {
                "avg_sentence_length": 14,
                "formality_score": 0.4,
                "vocabulary_richness": 0.7
            }
        }
    }

    col1, col2 = st.columns([1, 2])

    # ================= LEFT =================
    with col1:
        st.subheader("🎨 Choose Your Style")

        selected_style = st.radio(
            "Select a personality",
            options=list(PERSONALITIES.keys()),
            format_func=lambda x: f"{PERSONALITIES[x]['icon']} {PERSONALITIES[x]['name']}",
            key="selected_style"
        )

        st.markdown(
            f"### {PERSONALITIES[selected_style]['icon']} {PERSONALITIES[selected_style]['name']}"
        )
        st.write(PERSONALITIES[selected_style]["desc"])

    # ================= RIGHT =================
    with col2:
        st.subheader("✍️ Write with Your Style")

        # -------- QUICK PROMPTS --------
        st.markdown("💡 **Quick Prompts**")

        prompt_cols = st.columns(2)
        prompts = [
            "Social media post for product launch",
            "Professional email to a client",
            "Motivational message for the team",
            "Academic paper abstract"
        ]

        for i, prompt in enumerate(prompts):
            with prompt_cols[i % 2]:
                if st.button(prompt, key=f"prompt_{i}"):
                    st.session_state.prompt_text = prompt

        # -------- TEXT AREA --------
        st.text_area(
            "What would you like to write about?",
            key="prompt_text",
            height=160
        )

        st.caption(f"Characters: {len(st.session_state.prompt_text)}/500")

        # -------- GENERATE --------
        if st.button(f"✨ Generate with {PERSONALITIES[selected_style]['name']}"):
            if not st.session_state.prompt_text.strip():
                st.warning("Please enter some text.")
            else:
                with st.spinner("Generating..."):
                    time.sleep(0.8)
                    st.session_state.generated_text = generate_with_style(
                        st.session_state.prompt_text,
                        PERSONALITIES[selected_style]["profile"]  # ✅ FIX
                    )

        # -------- OUTPUT --------
        if st.session_state.generated_text:
            st.markdown("### 📝 Generated Output")
            st.success(st.session_state.generated_text)