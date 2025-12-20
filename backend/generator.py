import subprocess
import json

OLLAMA_MODEL = "llama3"


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
        return result.stdout.strip()
    except Exception as e:
        return f"⚠️ Ollama error: {e}"


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

{style_instruction}

Task:
{prompt}

Write the full response. Do NOT explain your style.
"""

    return _call_ollama(full_prompt)


# ===================== PERSONAL STYLE GENERATION =====================
def generate_with_style(prompt: str, style_profile: dict) -> str:
    avg_len = style_profile.get("avg_sentence_length", 12)
    vocab = style_profile.get("vocabulary_richness", 0.5)
    formality = style_profile.get("formality_score", 0.5)

    style_description = f"""
The user’s writing style has:
- Average sentence length: {avg_len}
- Vocabulary richness: {vocab}
- Formality score: {formality}

Mimic this style closely.
"""

    full_prompt = f"""
You are an AI that writes exactly like the user.

{style_description}

Task:
{prompt}

Write naturally. Do NOT mention analysis or metrics.
"""

    return _call_ollama(full_prompt)


# ===================== SIDE-BY-SIDE =====================
def generate_side_by_side(prompt: str, preset: str, style_profile: dict) -> dict:
    return {
        "preset": generate_preset(prompt, preset),
        "personal": generate_with_style(prompt, style_profile)
    }
