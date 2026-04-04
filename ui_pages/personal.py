import streamlit as st
import pandas as pd
from datetime import datetime

from backend.document_processor import DocumentProcessor
from backend.style_analyzer import StyleAnalyzer
from backend.generator import generate_side_by_side
from backend.profile_storage import save_style_profile
from backend.voice_assistant import listen_speech, clean_text
from utils.text_cleaner import sanitize_text

import os
import json


# ================= MATURITY FUNCTIONS =================
def maturity_score(p):
    return round(
        40 * p["vocabulary_richness"] +
        40 * p["formality_score"] +
        20 * min(p["avg_sentence_length"] / 20, 1),
        2
    )


def maturity_feedback(score):
    if score >= 75:
        return "🌟 Excellent writing. Strong vocabulary and professional tone."
    elif score >= 55:
        return "👍 Good writing. Try improving vocabulary and sentence variety."
    else:
        return "🛠 Basic writing. Focus on vocabulary and clearer sentence structure."


# ================= FILE STORAGE =================
HISTORY_FILE = "data/history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    os.makedirs("data", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, default=str)


# ================= SESSION STATE INIT =================
def _init_session_state():
    """Initialize all session state keys with defaults (runs once)."""
    defaults = {
        "uploaded_texts": [],
        "style_profile": None,
        "generation_history": load_history(),
        "prompt": "Write a thank-you email to my professor.",
        "generated_outputs": None,         # {"preset": ..., "personal": ...}
        "selected_style": "casual",
        "voice_status": None,              # None | "success" | "error"
        "voice_message": "",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ================= MAIN =================
def show():
    _init_session_state()

    username = "demo_user"
    processor = DocumentProcessor()
    analyzer = StyleAnalyzer()

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

    # ================= DISPLAY PROFILE =================
    if st.session_state.style_profile:
        profile = st.session_state.style_profile

        score = maturity_score(profile)
        profile["maturity_score"] = score

        st.markdown("### 🧬 Writing Maturity Score")

        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.metric("Score", f"{score}/100")

        with col_b:
            st.info(maturity_feedback(score))

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

        if "common_words" in profile:
            st.markdown("### 🔤 Most Common Words")
            st.write(", ".join(profile["common_words"]))

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # ✍️ GENERATE CARD
    # ==========================================================
    st.markdown('<div class="figma-card generate-card">', unsafe_allow_html=True)
    st.markdown("<h3>✍️ Generate Text (Side-by-Side)</h3>", unsafe_allow_html=True)

    # ---------- VOICE INPUT ----------
    if st.button("🎤 Speak Prompt", use_container_width=True):
        with st.spinner("🎤 Recording… speak now (8 seconds)"):
            voice_text = listen_speech(duration=8)

        if voice_text:
            st.session_state.prompt = voice_text
            st.session_state.voice_status = "success"
            st.rerun()  # Rerun so text_area renders with new value
        else:
            st.session_state.voice_status = "error"

    # Show voice error only (success is visible in the textbox itself)
    if st.session_state.voice_status == "error":
        st.warning("Could not understand speech. Please try again or type your prompt below.")

    # ---------- PROMPT TEXT AREA (single source of truth) ----------
    # key="prompt" binds directly to st.session_state["prompt"]
    # Voice input updates this key, so textbox always reflects voice input
    prompt = st.text_area(
        "✍️ Enter your prompt (or use voice above)",
        height=140,
        key="prompt",
    )

    # ---------- PRESET SELECTOR ----------
    preset_style = st.selectbox(
        "Choose preset personality",
        ["casual", "academic", "professional"],
        index=["casual", "academic", "professional"].index(
            st.session_state.selected_style
        ),
        key="preset_selector",
    )
    st.session_state.selected_style = preset_style

    # ---------- GENERATE BUTTON ----------
    if st.button("⚡ Generate Side-by-Side", use_container_width=True):
        if not st.session_state.style_profile:
            st.warning("Please analyze your writing style first.")
        elif not st.session_state.get("prompt", "").strip():
            st.warning("Please enter a prompt.")
        else:
            # Clean the prompt before generation (voice cleaner + ANSI stripper)
            cleaned_prompt = sanitize_text(clean_text(st.session_state["prompt"].strip()))

            with st.spinner("Generating comparison…"):
                outputs = generate_side_by_side(
                    prompt=cleaned_prompt,
                    preset=preset_style,
                    style_profile=st.session_state.style_profile,
                )

            # Persist outputs in session state
            st.session_state.generated_outputs = outputs

            # Clear previous TTS audio (new generation = new audio needed)
            st.session_state.tts_audio_preset = None
            st.session_state.tts_audio_personal = None

            # Clear voice status so old messages don't linger
            st.session_state.voice_status = None
            st.session_state.voice_message = ""

            # Save to history
            score = maturity_score(st.session_state.style_profile)
            new_entry = {
                "input": cleaned_prompt,
                "personality": f"Personal vs {preset_style}",
                "maturity_score": score,
                "output": {
                    "preset": outputs["preset"],
                    "personal": outputs["personal"],
                },
                "timestamp": datetime.now().isoformat(),
            }
            st.session_state.generation_history.append(new_entry)
            save_history(st.session_state.generation_history)

    # ==========================================================
    # 📊 DISPLAY OUTPUTS (always rendered from session state)
    # ==========================================================
    if st.session_state.generated_outputs:
        outputs = st.session_state.generated_outputs

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎭 Preset Personality")
            st.success(outputs["preset"])

        with col2:
            st.markdown("### 👤 Your Writing Style")
            st.success(outputs["personal"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-footer'>✨ Powered by PersonaWrite AI ✨</div>", unsafe_allow_html=True)