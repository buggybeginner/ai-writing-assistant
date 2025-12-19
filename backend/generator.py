import random

# ===================== PRESET GENERATION =====================
def generate_preset(prompt: str, preset: str) -> str:
    preset_prompts = {
        "casual": "Write in a casual and friendly tone.",
        "formal": "Write in a formal and professional tone.",
        "academic": "Write in an academic and scholarly style."
    }

    instruction = preset_prompts.get(preset, "")
    
    return f"{instruction}\n\n{prompt}"


# ===================== PERSONAL STYLE GENERATION =====================
def generate_with_style(prompt: str, style_profile: dict) -> str:
    """
    Intent-aware + style-aware text generation
    """

    prompt_lower = prompt.lower()
    formality = style_profile.get("formality_score", 0)

    # ---------- INTENT DETECTION ----------
    if "social media" in prompt_lower or "post" in prompt_lower:
        intent = "social"
    elif "email" in prompt_lower:
        intent = "email"
    elif "abstract" in prompt_lower or "paper" in prompt_lower:
        intent = "academic"
    elif "motivational" in prompt_lower or "team" in prompt_lower:
        intent = "motivation"
    else:
        intent = "general"

    # ---------- TEMPLATES ----------
    templates = {
        "social": [
            "🚀 Big news! We're excited to launch something we've been working hard on.",
            "✨ The wait is over! Our new product is finally here."
        ],
        "email": [
            "I hope this message finds you well. Thank you for your support.",
            "I truly appreciate your guidance and assistance."
        ],
        "academic": [
            "This paper presents a detailed analysis of the proposed methodology.",
            "The results demonstrate the effectiveness of the approach."
        ],
        "motivation": [
            "Believe in yourself and keep pushing forward.",
            "Every challenge is an opportunity to grow."
        ],
        "general": [
            "Thank you for your time and consideration.",
            "I appreciate your effort and support."
        ]
    }

    body = " ".join(
        random.sample(templates[intent], min(2, len(templates[intent])))
    )

    # ---------- STYLE TONE ----------
    if formality > 0.6:
        opening = "Dear Sir/Madam,"
        closing = "Sincerely,"
    else:
        opening = "Hi there!"
        closing = "Best regards,"

    return f"""{opening}

{body}

{closing}"""


# ===================== SIDE-BY-SIDE OUTPUT =====================
def generate_side_by_side(prompt: str, preset: str, style_profile: dict) -> dict:
    preset_output = generate_preset(prompt, preset)
    personal_output = generate_with_style(prompt, style_profile)

    return {
        "preset": preset_output,
        "personal": personal_output
    }
