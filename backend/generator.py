import random

def generate_with_style(prompt: str, style_profile: dict) -> str:
    """
    Intent-aware + style-aware text generation
    """

    prompt_lower = prompt.lower()

    avg_len = style_profile.get("avg_sentence_length", 12)
    formality = style_profile.get("formality_score", 0)

    # ---------------- INTENT DETECTION ----------------
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

    # ---------------- TEMPLATES ----------------
    templates = {
        "social": [
            "🚀 Big news! We're excited to launch something we've been working hard on. Stay tuned!",
            "✨ The wait is over! Our new product is finally here — check it out today!"
        ],
        "email": [
            "I hope this message finds you well. I am writing to discuss an important matter.",
            "Thank you for taking the time to review this email. I look forward to your response."
        ],
        "academic": [
            "This paper presents a comprehensive analysis of the proposed methodology.",
            "The results demonstrate the effectiveness of the approach under various conditions."
        ],
        "motivation": [
            "Believe in yourself and keep pushing forward — success is closer than you think!",
            "Every challenge is an opportunity to grow. Let’s give it our best!"
        ],
        "general": [
            "Thank you for your time and consideration.",
            "I appreciate your support and effort."
        ]
    }

    selected_templates = templates[intent]

    body = " ".join(
        random.sample(
            selected_templates,
            min(2, len(selected_templates))
        )
    )

    # ---------------- STYLE TONE ----------------
    if formality > 0.6:
        opening = "Dear Sir/Madam,"
        closing = "Sincerely,"
    else:
        opening = "Hi there!"
        closing = "Best regards,"

    # ---------------- FINAL OUTPUT ----------------
    return f"""{opening}

{body}

{closing}
"""