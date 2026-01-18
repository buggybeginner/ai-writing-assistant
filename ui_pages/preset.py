import streamlit as st
import time
from backend.generator import generate_with_style

def show():

    # ---------------- SESSION STATE ----------------
    if "prompt_text" not in st.session_state:
        st.session_state.prompt_text = ""

    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""

    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "casual"

    # ---------------- HEADER ----------------
    st.markdown("""
        <div class="home-hero">
            <h1>🎭 Preset Personalities</h1>
            <p>Choose from carefully crafted writing styles</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- DATA ----------------
    PERSONALITIES = {
        "casual": {
            "name": "Casual Friendly",
            "icon": "😊",
            "desc": "Warm and conversational tone.",
            "profile": {"avg_sentence_length": 10, "formality_score": 0.2, "vocabulary_richness": 0.4}
        },
        "corporate": {
            "name": "Corporate Professional",
            "icon": "💼",
            "desc": "Formal business communication.",
            "profile": {"avg_sentence_length": 16, "formality_score": 0.7, "vocabulary_richness": 0.6}
        },
        "academic": {
            "name": "Formal Academic",
            "icon": "🎓",
            "desc": "Scholarly academic writing.",
            "profile": {"avg_sentence_length": 22, "formality_score": 0.9, "vocabulary_richness": 0.8}
        },
        "motivational": {
            "name": "Motivational Speaker",
            "icon": "🚀",
            "desc": "Energetic and inspiring tone.",
            "profile": {"avg_sentence_length": 14, "formality_score": 0.4, "vocabulary_richness": 0.7}
        }
    }

    col1, col2 = st.columns([1, 1.2], gap="large")

    # ================= LEFT =================
    with col1:
        st.subheader("🎨 Choose Your Style")

        for pid, pdata in PERSONALITIES.items():
            is_active = st.session_state.selected_personality == pid

            if st.button(
                f"{pdata['icon']} {pdata['name']}",
                key=f"style_{pid}",
                use_container_width=True
            ):
                st.session_state.selected_personality = pid

        current = PERSONALITIES[st.session_state.selected_personality]
        st.markdown(f"""
            <div class="info-card-active">
                <strong>{current['icon']} {current['name']}</strong>
                <p>{current['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

    # ================= RIGHT =================
    with col2:
        st.subheader("✍️ Write with Your Style")

        st.markdown("**Quick Prompts**")

        q1, q2 = st.columns(2)

        with q1:
            if st.button("Social media post"):
                st.session_state.prompt_text = "Write a social media post for a product launch."
            if st.button("Motivational message"):
                st.session_state.prompt_text = "Write a motivational message for a team."

        with q2:
            if st.button("Professional email"):
                st.session_state.prompt_text = "Write a professional email to a client."
            if st.button("Academic abstract"):
                st.session_state.prompt_text = "Write an academic paper abstract."

        st.text_area(
            "What would you like to write about?",
            key="prompt_text",
            height=180
        )

        style_name = PERSONALITIES[st.session_state.selected_personality]["name"]

        if st.button(f"✨ Generate with {style_name}", use_container_width=True):
            if not st.session_state.prompt_text.strip():
                st.warning("Please enter a prompt.")
            else:
                with st.spinner("Generating..."):
                    time.sleep(0.6)
                    st.session_state.generated_text = generate_with_style(
                        st.session_state.prompt_text,
                        PERSONALITIES[st.session_state.selected_personality]["profile"]
                    )

        if st.session_state.generated_text:
            st.markdown("### 📝 Generated Output")
            st.success(st.session_state.generated_text)

    st.markdown("<div class='page-footer'>✨ Powered by PersonaWrite AI ✨</div>", unsafe_allow_html=True)