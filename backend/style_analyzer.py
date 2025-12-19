import re
from collections import Counter

class StyleAnalyzer:
    def analyze(self, texts: list[str]) -> dict:
        words = []
        sentences = []

        for text in texts:
            text = text.strip()
            sents = re.split(r'[.!?]+', text)
            sents = [s.strip() for s in sents if s.strip()]
            sentences.extend(sents)
            words.extend(re.findall(r'\b\w+\b', text.lower()))

        # Metrics
        avg_sentence_length = round(len(words) / max(len(sentences), 1), 2)
        vocabulary_richness = round(len(set(words)) / max(len(words), 1), 3)

        formal_words = {
            "therefore", "however", "sincerely", "regards",
            "further", "express", "moreover", "hence"
        }
        formality_score = round(
            sum(1 for w in words if w in formal_words) / max(len(words), 1),
            3
        )

        common_words = dict(Counter(words).most_common(10))

        return {
            "avg_sentence_length": avg_sentence_length,
            "vocabulary_richness": vocabulary_richness,
            "formality_score": formality_score,
            "common_words": common_words,
            "sentence_count": len(sentences),
            "word_count": len(words),
        }
