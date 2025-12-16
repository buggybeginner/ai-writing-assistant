import streamlit as st
import pandas as pd
from backend.document_processor import DocumentProcessor
from backend.style_analyzer import StyleAnalyzer
from backend.generator import generate_with_style


def show():
    st.title("👤 Personal Writing Style AI")

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
        st.session_state.uploaded_texts = []  # reset on new upload

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

    if st.button("Analyze My Writing Style"):
        if not st.session_state.uploaded_texts:
            st.warning("Please upload at least one file.")
        else:
            combined_text = "\n".join(st.session_state.uploaded_texts)
            profile = analyzer.analyze(combined_text)
            st.session_state.style_profile = profile
            st.success("Style profile created!")

    # ===================== METRICS + CHART =====================
    if st.session_state.style_profile:
        profile = st.session_state.style_profile

        st.subheader("📊 Writing Style Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Sentence Length", round(profile["avg_sentence_length"], 2))
        col2.metric("Vocabulary Richness", round(profile["vocabulary_richness"], 2))
        col3.metric("Formality Score", round(profile["formality_score"], 2))

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
        st.write(list(profile["common_words"].keys())[:20])

    # ===================== GENERATE =====================
    st.header("✍️ Generate Text in Your Style")

    prompt = st.text_area(
        "What do you want the AI to write?",
        "Write a thank-you email to my professor.",
        height=150
    )

    if st.button("Generate in My Style"):
        if not st.session_state.style_profile:
            st.warning("Analyze your writing style first.")
        elif not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating..."):
                output = generate_with_style(prompt, st.session_state.style_profile)

            st.subheader("📝 Generated Output")
            st.success(output)
