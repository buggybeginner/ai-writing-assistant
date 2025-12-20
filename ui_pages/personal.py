import streamlit as st
import pandas as pd

from backend.document_processor import DocumentProcessor
from backend.style_analyzer import StyleAnalyzer
from backend.generator import generate_side_by_side
from backend.profile_storage import save_style_profile, load_style_profile


def show():
    st.title("👤 Personal Writing Style AI")

    # ---------------- USER (SIMPLE DEMO USER) ----------------
    username = "demo_user"

    # ---------------- INIT BACKEND ----------------
    processor = DocumentProcessor()
    analyzer = StyleAnalyzer()

    # ---------------- SESSION STATE ----------------
    if "uploaded_texts" not in st.session_state:
        st.session_state.uploaded_texts = []

    if "style_profile" not in st.session_state:
        st.session_state.style_profile = None

    # ===================== UPLOAD =====================
    st.header("📁 Upload Your Writing Samples")

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
                    st.warning(f"Unsupported file: {file.name}")
                    continue

                st.session_state.uploaded_texts.append(text)

            except Exception as e:
                st.error(f"Failed to read {file.name}: {e}")

        st.success(f"{len(st.session_state.uploaded_texts)} files processed successfully")

    # ===================== ANALYZE =====================
    st.header("🧠 Analyze Writing Style")

    analyze_clicked = st.button("Analyze My Writing Style")

    if analyze_clicked:
        if not st.session_state.uploaded_texts:
            st.warning("Please upload at least one document before analyzing.")
        else:
            combined_text = "\n".join(st.session_state.uploaded_texts)
            profile = analyzer.analyze(combined_text)

            save_style_profile(username, profile)
            st.session_state.style_profile = profile

            st.success("✅ Style profile created & saved!")

    # ===================== METRICS =====================
    if st.session_state.style_profile is not None and st.session_state.uploaded_texts:
        profile = st.session_state.style_profile

        st.subheader("📊 Writing Style Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Sentence Length", profile["avg_sentence_length"])
        col2.metric("Vocabulary Richness", profile["vocabulary_richness"])
        col3.metric("Formality Score", profile["formality_score"])

        metrics_df = pd.DataFrame({
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

        st.bar_chart(metrics_df.set_index("Metric"))

        st.markdown("**Common Words:**")
        st.write(list(profile["common_words"].keys()))

    # ===================== GENERATE =====================
    st.header("✍️ Generate Text (Side-by-Side)")

    prompt = st.text_area(
        "Enter your prompt:",
        "Write a thank-you email to my professor.",
        height=150
    )

    preset_style = st.selectbox(
        "Choose preset personality",
        ["casual", "academic", "professional"]
    )

    if st.button("Generate Side-by-Side"):
        if not st.session_state.style_profile:
            st.warning("Please analyze your writing style first.")
        elif not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating outputs..."):
                outputs = generate_side_by_side(
                    prompt=prompt,
                    preset=preset_style,
                    style_profile=st.session_state.style_profile
                )

            st.subheader("🧩 Side-by-Side Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎭 Preset Personality")
                st.success(outputs["preset"])

            with col2:
                st.markdown("### 👤 Personal AI Twin")
                st.success(outputs["personal"])
