"""
PersonaWrite AI — Text Generator (Groq API)
Improved Version: Cleaner Output + Better Prompting
"""

import os
from dotenv import load_dotenv
from groq import Groq
from utils.text_cleaner import sanitize_text

# ===================== ENV & CLIENT =====================

load_dotenv()

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
]

_groq_client = None


def _get_client():
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. Add it in .env file."
            )
        _groq_client = Groq(api_key=api_key)
    return _groq_client


# ===================== INPUT CLEANING =====================

def clean_prompt(prompt: str) -> str:
    """
    Fix common user prompt issues like:
    [Name], [Professor], etc.
    """
    if not prompt:
        return ""

    # Remove brackets
    prompt = prompt.replace("[", "").replace("]", "")

    # Fix common placeholder words
    prompt = prompt.replace("your name", "my name")
    prompt = prompt.replace("professor's name", "Professor")

    return prompt.strip()


# ===================== GROQ CALL =====================

def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        client = _get_client()
    except RuntimeError as e:
        return f"⚠️ {e}"

    user_prompt = clean_prompt(user_prompt)

    last_error = None

    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.6,  # more controlled output
                max_tokens=800,
                top_p=0.9,
            )

            text = response.choices[0].message.content

            if text:
                return sanitize_text(text.strip())

            last_error = "Empty response"

        except Exception as e:
            last_error = str(e)
            continue

    return f"⚠️ Groq API error: {last_error}"


# ===================== STYLE BUILDER =====================

def build_style_description(style_profile: dict) -> str:
    avg_len = style_profile.get("avg_sentence_length", 12)
    vocab = style_profile.get("vocabulary_richness", 0.5)
    formality = style_profile.get("formality_score", 0.5)

    if avg_len > 20:
        sentence_style = "long and detailed sentences"
    elif avg_len > 12:
        sentence_style = "moderate length sentences"
    else:
        sentence_style = "short and simple sentences"

    if vocab > 0.7:
        vocab_style = "rich and expressive vocabulary"
    elif vocab > 0.4:
        vocab_style = "clear and balanced vocabulary"
    else:
        vocab_style = "simple vocabulary"

    if formality > 0.7:
        tone = "formal and professional"
    elif formality > 0.4:
        tone = "neutral and polite"
    else:
        tone = "casual and friendly"

    return (
        f"Write using a {tone} tone. "
        f"Use {sentence_style}. "
        f"Use {vocab_style}."
    )


# ===================== PRESET =====================

PRESET_SYSTEM_PROMPTS = {
    "casual": (
        "You are a friendly human writer. Write casually and naturally like a student."
    ),
    "professional": (
        "You are a professional email writer. Keep tone polite, structured, and clear."
    ),
    "academic": (
        "You are an academic writer. Use formal tone, structured sentences, and clarity."
    ),
}


def generate_preset(prompt: str, preset: str) -> str:
    system_prompt = PRESET_SYSTEM_PROMPTS.get(
        preset,
        "Write naturally and clearly."
    )

    # 🔥 STRONG CONTROL RULES
    system_prompt += (
        "\n\nSTRICT RULES:\n"
        "- Write a complete email.\n"
        "- Do NOT use placeholders like [Name].\n"
        "- Use a real name if needed.\n"
        "- Always include:\n"
        "  Greeting → Body → Closing\n"
        "- No explanations.\n"
    )

    return call_llm(system_prompt, prompt)


# ===================== PERSONAL STYLE =====================

def generate_with_style(prompt: str, style_profile: dict) -> str:
    style_description = build_style_description(style_profile)

    system_prompt = (
        "You are a human writer who mimics a person's writing style.\n"
        f"{style_description}\n\n"
        "STRICT RULES:\n"
        "- Write a complete email.\n"
        "- Do NOT use placeholders like [Name].\n"
        "- Always use a realistic professor name.\n"
        "- Keep structure clean and readable.\n"
        "- No explanations.\n"
    )

    return call_llm(system_prompt, prompt)


# ===================== SIDE-BY-SIDE =====================

def generate_side_by_side(prompt: str, preset: str, style_profile: dict) -> dict:
    return {
        "preset": generate_preset(prompt, preset),
        "personal": generate_with_style(prompt, style_profile),
    }