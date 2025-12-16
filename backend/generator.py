import random

def generate_with_style(prompt: str, style_profile: dict) -> str:
    """
    Rule-based + style-aware text generation
    (Mentor-acceptable baseline)
    """

    avg_len = style_profile.get("avg_sentence_length", 12)
    formality = style_profile.get("formality_score", 0)
    vocab = style_profile.get("vocabulary_richness", 0.4)

    # ---------------- OPENING ----------------
    if formality > 0.5:
        opening = "Dear Professor,"
        closing = "Sincerely,"
    else:
        opening = "Hi Professor,"
        closing = "Best regards,"

    # ---------------- BODY TEMPLATES ----------------
    formal_templates = [
        "I hope this message finds you well. I am writing to express my sincere gratitude for your guidance and support.",
        "Thank you for taking the time to assist me and for providing valuable insights throughout the course."
    ]

    casual_templates = [
        "I just wanted to take a moment to say thank you for all your help.",
        "I really appreciate the time and effort you put into explaining things so clearly."
    ]

    # Pick based on formality
    if formality > 0.5:
        body_sentences = formal_templates
    else:
        body_sentences = casual_templates

    # Adjust length
    target_sentences = max(2, int(avg_len / 6))
    body = " ".join(random.sample(body_sentences, min(len(body_sentences), target_sentences)))

    # ---------------- FINAL OUTPUT ----------------
    output = f"""{opening}

{body}

Thank you once again for your support.

{closing}
"""

    return output.strip()
