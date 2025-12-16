from backend.style_analyzer import StyleAnalyzer

class StyleProfileBuilder:
    def __init__(self):
        self.analyzer = StyleAnalyzer()

    def build_profile(self, texts: list[str]) -> dict:
        profiles = [self.analyzer.analyze(t) for t in texts]

        if not profiles:
            return {}

        profile = {
            "avg_sentence_length": round(
                sum(p["avg_sentence_length"] for p in profiles) / len(profiles), 2
            ),
            "vocabulary_richness": round(
                sum(p["vocabulary_richness"] for p in profiles) / len(profiles), 2
            ),
            "formality_score": round(
                sum(p["formality_score"] for p in profiles) / len(profiles), 2
            ),
            "common_words": self._merge_common_words(profiles),
            "sample_count": len(profiles)
        }

        return profile

    def _merge_common_words(self, profiles):
        word_freq = {}

        for p in profiles:
            for word, count in p["common_words"].items():
                word_freq[word] = word_freq.get(word, 0) + count

        # return top 5 most frequent
        return sorted(word_freq, key=word_freq.get, reverse=True)[:5]
