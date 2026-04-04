import subprocess
from utils.text_cleaner import sanitize_text

# ===================== MODEL =====================
# You can upgrade to "mistral:latest" for better quality
OLLAMA_MODEL = "tinyllama:latest"


# ===================== OLLAMA CALL =====================
def _call_ollama(prompt: str) -> str:
    """
    Calls Ollama locally and returns generated text
    """
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout:
            return sanitize_text(result.stdout.strip())
        else:
            return "⚠️ No output received from Ollama."

    except subprocess.CalledProcessError as e:
        return f"⚠️ Ollama error: {e.stderr or str(e)}"

    except Exception as e:
        return f"⚠️ Unexpected error: {e}"


# ===================== STYLE BUILDER =====================
def build_style_description(style_profile: dict) -> str:
    """
    Converts numeric style metrics into natural language instructions
    """
    avg_len = style_profile.get("avg_sentence_length", 12)
    vocab = style_profile.get("vocabulary_richness", 0.5)
    formality = style_profile.get("formality_score", 0.5)

    # Sentence style
    if avg_len > 20:
        sentence_style = "long and descriptive sentences"
    elif avg_len > 12:
        sentence_style = "moderately detailed sentences"
    else:
        sentence_style = "short and simple sentences"

    # Vocabulary style
    if vocab > 0.7:
        vocab_style = "rich and expressive vocabulary"
    elif vocab > 0.4:
        vocab_style = "balanced vocabulary"
    else:
        vocab_style = "simple vocabulary"

    # Tone
    if formality > 0.7:
        tone = "formal and professional tone"
    elif formality > 0.4:
        tone = "neutral tone"
    else:
        tone = "casual and friendly tone"

    return f"Write in a {tone}, using {sentence_style} and {vocab_style}."


# ===================== PRESET GENERATION =====================
def generate_preset(prompt: str, preset: str) -> str:
    preset_styles = {
        "casual": "Write in a casual, friendly, conversational tone.",
        "professional": "Write in a professional, formal business tone.",
        "academic": "Write in a formal academic and scholarly style."
    }

    style_instruction = preset_styles.get(preset, "")

    full_prompt = f"""
You are a writing assistant.

Task:
{prompt}

Instructions:
{style_instruction}

Write the final response only.
Do NOT explain anything.
Do NOT mention style or instructions.
"""

    return _call_ollama(sanitize_text(full_prompt))


# ===================== PERSONAL STYLE GENERATION =====================
def generate_with_style(prompt: str, style_profile: dict) -> str:
    style_description = build_style_description(style_profile)

    full_prompt = f"""
You are a writing assistant.

Task:
{prompt}

Instructions:
{style_description}

Write the final response only.
Do NOT explain anything.
Do NOT mention style, analysis, or metrics.
"""

    return _call_ollama(sanitize_text(full_prompt))


# ===================== SIDE-BY-SIDE =====================
def generate_side_by_side(prompt: str, preset: str, style_profile: dict) -> dict:
    return {
        "preset": generate_preset(prompt, preset),
        "personal": generate_with_style(prompt, style_profile)
    }