import re
from collections import Counter

class StyleAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text: str) -> dict:
        # Clean text
        text = text.strip()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = re.findall(r'\b\w+\b', text.lower())

        # Metrics
        avg_sentence_length = round(len(words) / max(len(sentences), 1), 2)
        vocabulary_richness = round(len(set(words)) / max(len(words), 1), 2)

        # Very simple formality heuristic
        formal_words = {"therefore", "however", "sincerely", "regards", "further", "express"}
        formality_score = round(
            sum(1 for w in words if w in formal_words) / max(len(words), 1),
            2
        )

        common_words = Counter(words).most_common(5)

        return {
            "avg_sentence_length": avg_sentence_length,
            "vocabulary_richness": vocabulary_richness,
            "formality_score": formality_score,
            "common_words": dict(common_words),
            "sentence_count": len(sentences),
            "word_count": len(words),
        }
