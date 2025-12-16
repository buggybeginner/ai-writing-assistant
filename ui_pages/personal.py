import streamlit as st
from backend.document_processor import DocumentProcessor
from backend.style_analyzer import StyleAnalyzer
from backend.generator import generate_with_style


def show():
    st.title("👤 Personal Writing Style AI")

    # Initialize backend
    processor = DocumentProcessor()
    analyzer = StyleAnalyzer()

    # Session state
    if "style_profile" not in st.session_state:
        st.session_state.style_profile = None

    # ===================== UPLOAD =====================
    st.header("📁 Upload Your Writing Samples")

    uploaded_files = st.file_uploader(
        "Upload TXT files (emails, essays, notes)",
        type=["txt"],
        accept_multiple_files=True
    )

    texts = []

    if uploaded_files:
        for file in uploaded_files:
            content = file.read().decode("utf-8", errors="ignore")
            texts.append(content)

        st.success(f"{len(texts)} files uploaded")

    # ===================== ANALYZE =====================
    st.header("🧠 Analyze Writing Style")

    if st.button("Analyze My Writing Style"):
        if not texts:
            st.warning("Please upload at least one text file.")
        else:
            combined_text = "\n".join(texts)
            profile = analyzer.analyze(combined_text)
            st.session_state.style_profile = profile
            st.success("Style profile created!")

    # ===================== STYLE METRICS =====================
    if st.session_state.style_profile:
        st.subheader("📊 Your Writing Style Profile")

        profile = st.session_state.style_profile

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Sentence Length", profile["avg_sentence_length"])
        col2.metric("Vocabulary Richness", profile["vocabulary_richness"])
        col3.metric("Formality Score", profile["formality_score"])

        st.write("**Common Words:**")
        st.write(list(profile["common_words"].keys()))

    # ===================== GENERATE =====================
    st.header("✍️ Generate Text in Your Style")

    prompt = st.text_area(
        "What do you want the AI to write?",
        "Write a thank-you email to my professor."
    )

    if st.button("Generate in My Style"):
        if not st.session_state.style_profile:
            st.warning("Analyze your writing style first.")
        else:
            output = generate_with_style(prompt, st.session_state.style_profile)
            st.subheader("📝 Generated Output")
            st.success(output)
