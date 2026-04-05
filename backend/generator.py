"""
PersonaWrite AI — Text Generator (Groq API)

Uses the Groq Python SDK with automatic model fallback.
Primary model  : llama-3.1-8b-instant   (fast, actively supported)
Fallback model : llama-3.1-70b-versatile (higher quality, actively supported)
"""

import os
from dotenv import load_dotenv
from groq import Groq
from utils.text_cleaner import sanitize_text

# ===================== ENV & CLIENT =====================

load_dotenv()  # loads .env from project root

# Ordered list of models to try — first success wins.
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
]

_groq_client = None


def _get_client() -> Groq:
    """Lazy-init Groq client so the import alone never crashes."""
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. "
                "Add it to your .env file: GROQ_API_KEY=gsk_..."
            )
        _groq_client = Groq(api_key=api_key)
    return _groq_client


# ===================== GROQ CALL =====================

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Send a chat completion request to Groq with automatic model fallback.

    Tries each model in GROQ_MODELS in order. If a model fails (deprecated,
    rate-limited, etc.), the next model is attempted. Only returns an error
    when every model has been exhausted.

    Args:
        system_prompt: High-level persona / instructions for the model.
        user_prompt:   The specific writing task.

    Returns:
        Sanitized generated text, or a readable error message prefixed with ⚠️.
    """
    try:
        client = _get_client()
    except RuntimeError as e:
        return f"⚠️ {e}"

    last_error = None

    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9,
            )

            text = response.choices[0].message.content
            if text:
                return sanitize_text(text.strip())
            # Empty response — try next model
            last_error = "No output received from model."

        except Exception as e:
            last_error = _friendly_error(e)
            # Continue to the next model in the fallback list
            continue

    # Every model failed
    return f"⚠️ Groq API error: {last_error}"


def _friendly_error(exc: Exception) -> str:
    """
    Convert a raw Groq exception into a short, human-readable message.
    Strips away JSON dumps and internal details the user doesn't need.
    """
    error_str = str(exc)

    if "model_decommissioned" in error_str:
        return "The requested model has been retired. Trying alternatives…"
    if "rate_limit" in error_str.lower():
        return "Rate limit reached — please wait a moment and try again."
    if "authentication" in error_str.lower() or "401" in error_str:
        return "Invalid API key. Please check your GROQ_API_KEY."
    if "timeout" in error_str.lower():
        return "Request timed out. Please try again."

    # Fallback: keep it short
    return f"Unexpected error — {error_str[:200]}"


# ===================== STYLE BUILDER =====================

def build_style_description(style_profile: dict) -> str:
    """
    Converts numeric style metrics into natural language writing instructions.
    The output is used as part of the system prompt — never shown to the user.
    """
    avg_len = style_profile.get("avg_sentence_length", 12)
    vocab = style_profile.get("vocabulary_richness", 0.5)
    formality = style_profile.get("formality_score", 0.5)

    # Sentence style
    if avg_len > 20:
        sentence_style = "long, detailed sentences with subordinate clauses"
    elif avg_len > 12:
        sentence_style = "moderately detailed sentences"
    else:
        sentence_style = "short, punchy sentences"

    # Vocabulary
    if vocab > 0.7:
        vocab_style = "rich, expressive, and varied vocabulary"
    elif vocab > 0.4:
        vocab_style = "clear, balanced vocabulary"
    else:
        vocab_style = "simple, everyday vocabulary"

    # Tone
    if formality > 0.7:
        tone = "formal and polished"
    elif formality > 0.4:
        tone = "neutral and approachable"
    else:
        tone = "casual and friendly"

    return (
        f"Mirror the following writing style exactly: "
        f"Use a {tone} tone. "
        f"Prefer {sentence_style}. "
        f"Use {vocab_style}."
    )


# ===================== PRESET GENERATION =====================

PRESET_SYSTEM_PROMPTS = {
    "casual": (
        "You are a warm, friendly writer. "
        "Write in a relaxed, conversational tone as if chatting with a close friend. "
        "Use contractions, simple words, and a natural flow."
    ),
    "professional": (
        "You are a seasoned business writer. "
        "Write in a polished, professional tone suitable for corporate communication. "
        "Be clear, concise, and confident without being stiff."
    ),
    "academic": (
        "You are a scholarly writer. "
        "Write in a formal academic style with precise language, well-structured arguments, "
        "and an objective, analytical tone."
    ),
}


def generate_preset(prompt: str, preset: str) -> str:
    """Generate text using a preset writing personality."""
    system_prompt = PRESET_SYSTEM_PROMPTS.get(
        preset,
        "You are a helpful writing assistant. Write naturally and clearly."
    )

    # Append universal guardrails to the system prompt
    system_prompt += (
        "\n\nIMPORTANT RULES:\n"
        "- Output ONLY the requested text. No explanations, labels, or meta-commentary.\n"
        "- Do NOT mention the writing style, tone, or any instructions you received.\n"
        "- Write as a real human would — natural, coherent, and engaging."
    )

    return call_llm(system_prompt, prompt)


# ===================== PERSONAL STYLE GENERATION =====================

def generate_with_style(prompt: str, style_profile: dict) -> str:
    """Generate text that mirrors the user's analyzed writing style."""
    style_description = build_style_description(style_profile)

    system_prompt = (
        "You are a writing assistant that perfectly adapts to a specific personal writing style. "
        f"{style_description}"
        "\n\nIMPORTANT RULES:\n"
        "- Output ONLY the requested text. No explanations, labels, or meta-commentary.\n"
        "- Do NOT mention style metrics, analysis, scores, or any instructions you received.\n"
        "- Write as a real human would — natural, coherent, and engaging."
    )

    return call_llm(system_prompt, prompt)


# ===================== SIDE-BY-SIDE =====================

def generate_side_by_side(prompt: str, preset: str, style_profile: dict) -> dict:
    """Generate both preset and personal-style versions for comparison."""
    return {
        "preset": generate_preset(prompt, preset),
        "personal": generate_with_style(prompt, style_profile),
    }