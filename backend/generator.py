def generate_with_style(prompt: str, style_profile: dict) -> str:
    avg_len = style_profile.get("avg_sentence_length", 10)
    formality = style_profile.get("formality_score", 0)
    common_words = style_profile.get("common_words", {})

    # Safely extract a frequent word
    frequent_word = ""
    if isinstance(common_words, dict) and len(common_words) > 0:
        frequent_word = list(common_words.keys())[0]

    # Tone decision
    if formality > 0.05:
        opening = "Dear Professor,"
        closing = "Sincerely,"
    else:
        opening = "Hi Professor,"
        closing = "Thanks so much,"

    body = f"\n\nThank you for your guidance regarding this matter."
    if frequent_word:
        body += f" I truly appreciate your {frequent_word}."

    return f"{opening}\n{body}\n\n{closing}"

