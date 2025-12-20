import re
from collections import Counter
from typing import Union, List

class StyleAnalyzer:
    def analyze(self, texts: Union[str, List[str]]) -> dict:
        # ✅ Normalize input
        if isinstance(texts, str):
            texts = [texts]

        words = []
        sentences = []

        for text in texts:
            text = text.strip()

            # Sentence split
            sents = re.split(r'[.!?]+', text)
            sents = [s.strip() for s in sents if s.strip()]
            sentences.extend(sents)

            # Word extraction (REAL words only)
            words.extend(re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()))

        # Safety checks
        sentence_count = max(len(sentences), 1)
        word_count = max(len(words), 1)

        avg_sentence_length = round(len(words) / sentence_count, 2)
        vocabulary_richness = round(len(set(words)) / word_count, 3)

        formal_words = {
            "therefore", "however", "sincerely", "regards",
            "further", "express", "moreover", "hence"
        }

        formality_score = round(
            sum(1 for w in words if w in formal_words) / word_count,
            3
        )

        # ✅ REAL common words
        common_words = dict(Counter(words).most_common(10))

        return {
            "avg_sentence_length": avg_sentence_length,
            "vocabulary_richness": vocabulary_richness,
            "formality_score": formality_score,
            "common_words": common_words,
            "sentence_count": len(sentences),
            "word_count": len(words),
        }
