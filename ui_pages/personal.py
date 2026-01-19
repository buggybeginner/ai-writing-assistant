import streamlit as st
import pandas as pd
from datetime import datetime

from backend.document_processor import DocumentProcessor
from backend.style_analyzer import StyleAnalyzer
from backend.generator import generate_side_by_side
from backend.profile_storage import save_style_profile


def show():
    # ---------------- USER ----------------
    username = "demo_user"

    processor = DocumentProcessor()
    analyzer = StyleAnalyzer()

    # ---------------- SESSION STATE ----------------
    if "uploaded_texts" not in st.session_state:
        st.session_state.uploaded_texts = []

    if "style_profile" not in st.session_state:
        st.session_state.style_profile = None

    # ✅ REQUIRED FOR DASHBOARD
    if "generation_history" not in st.session_state:
        st.session_state.generation_history = []

    # ---------------- HEADER ----------------
    st.markdown("""
        <div class="home-hero">
            <h1>👤 Personal Writing Style AI</h1>
            <p>Train AI on your unique writing style ✨</p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # 📁 UPLOAD CARD
    # ==========================================================
    st.markdown('<div class="figma-card upload-card">', unsafe_allow_html=True)
    st.markdown("<h3>📁 Upload Your Writing Samples</h3>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload writing samples (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.session_state.uploaded_texts = []

        for file in uploaded_files:
            try:
                if file.type == "text/plain":
                    text = file.read().decode("utf-8", errors="ignore")
                elif file.type == "application/pdf":
                    text = processor.read_pdf(file)
                elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = processor.read_docx(file)
                else:
                    continue

                st.session_state.uploaded_texts.append(text)

            except Exception as e:
                st.error(f"Failed to read {file.name}: {e}")

        st.success(f"✅ {len(st.session_state.uploaded_texts)} file(s) processed")

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # 🧠 ANALYZE CARD
    # ==========================================================
    st.markdown('<div class="figma-card analyze-card">', unsafe_allow_html=True)
    st.markdown("<h3>🧠 Analyze Writing Style</h3>", unsafe_allow_html=True)

    if st.button("✨ Analyze My Writing Style", use_container_width=True):
        if not st.session_state.uploaded_texts:
            st.warning("Please upload at least one document.")
        else:
            combined_text = "\n".join(st.session_state.uploaded_texts)
            profile = analyzer.analyze(combined_text)

            save_style_profile(username, profile)
            st.session_state.style_profile = profile
            st.success("🎉 Style profile created successfully!")

    if st.session_state.style_profile:
        profile = st.session_state.style_profile

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Sentence Length", profile["avg_sentence_length"])
        col2.metric("Vocabulary Richness", profile["vocabulary_richness"])
        col3.metric("Formality Score", profile["formality_score"])

        df = pd.DataFrame({
            "Metric": [
                "Avg Sentence Length",
                "Vocabulary Richness",
                "Formality Score"
            ],
            "Value": [
                profile["avg_sentence_length"],
                profile["vocabulary_richness"],
                profile["formality_score"]
            ]
        })

        st.bar_chart(df.set_index("Metric"))

        # ✅ COMMON WORDS DISPLAY (NO DESIGN CHANGE)
        if "common_words" in profile:
            st.markdown("### 🔤 Most Common Words")
            st.write(", ".join(profile["common_words"]))

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # ✍️ GENERATE SIDE-BY-SIDE CARD
    # ==========================================================
    st.markdown('<div class="figma-card generate-card">', unsafe_allow_html=True)
    st.markdown("<h3>✍️ Generate Text (Side-by-Side)</h3>", unsafe_allow_html=True)

    prompt = st.text_area(
        "Enter your prompt",
        "Write a thank-you email to my professor.",
        height=140
    )

    preset_style = st.selectbox(
        "Choose preset personality",
        ["casual", "academic", "professional"]
    )

    if st.button("⚡ Generate Side-by-Side", use_container_width=True):
        if not st.session_state.style_profile:
            st.warning("Please analyze your writing style first.")
        elif not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating comparison..."):
                outputs = generate_side_by_side(
                    prompt=prompt,
                    preset=preset_style,
                    style_profile=st.session_state.style_profile
                )

            # ✅ SAVE TO DASHBOARD HISTORY
            st.session_state.generation_history.append({
                "input": prompt,
                "personality": f"Personal vs {preset_style}",
                "output": {
                    "preset": outputs["preset"],
                    "personal": outputs["personal"]
                },
                "timestamp": datetime.now()
            })

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎭 Preset Personality")
                st.success(outputs["preset"])

            with col2:
                st.markdown("### 👤 Your Writing Style")
                st.success(outputs["personal"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='page-footer'>✨ Powered by PersonaWrite AI ✨</div>", unsafe_allow_html=True)
