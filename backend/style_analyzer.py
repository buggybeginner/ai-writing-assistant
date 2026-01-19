import re
from collections import Counter
from typing import Union, List


class StyleAnalyzer:
    def analyze(self, texts: Union[str, List[str]]) -> dict:
        # ---------------- NORMALIZE INPUT ----------------
        if isinstance(texts, str):
            texts = [texts]

        words = []
        sentences = []

        for text in texts:
            if not text:
                continue

            text = text.strip()

            # Sentence split
            sents = re.split(r'[.!?]+', text)
            sents = [s.strip() for s in sents if s.strip()]
            sentences.extend(sents)

            # Word extraction (real words only)
            words.extend(re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()))

        # ---------------- SAFETY ----------------
        sentence_count = max(len(sentences), 1)
        word_count = max(len(words), 1)

        # ---------------- BASIC METRICS ----------------
        avg_sentence_length = round(word_count / sentence_count, 2)
        vocabulary_richness = round(len(set(words)) / word_count, 3)

        # ---------------- FORMALITY WORDS (EXPANDED) ----------------
        formal_words = {
            "therefore", "however", "moreover", "further", "hence",
            "regarding", "sincerely", "respectfully", "additionally",
            "approximately", "consequently", "professional", "organization",
            "responsibilities", "experience", "skills", "objective",
            "summary", "education", "certification"
        }

        informal_words = {
            "hey", "hi", "thanks", "cool", "awesome", "lol",
            "stuff", "things", "kinda", "gonna", "wanna"
        }

        formal_count = sum(1 for w in words if w in formal_words)
        informal_count = sum(1 for w in words if w in informal_words)

        # ---- FIXED FORMALITY SCORE (CV SAFE) ----
        formality_score = round(
            (formal_count + 1) / (formal_count + informal_count + 5),
            3
        )

        # ---------------- COMMON WORDS ----------------
        common_words = dict(Counter(words).most_common(10))

        # ---------------- PERSONALITY DETECTION ----------------
        personality = self.detect_personality(
            words,
            avg_sentence_length,
            formality_score
        )

        # ---------------- RETURN ----------------
        return {
            "avg_sentence_length": avg_sentence_length,
            "vocabulary_richness": vocabulary_richness,
            "formality_score": formality_score,
            "common_words": common_words,
            "personality": personality,
            "sentence_count": sentence_count,
            "word_count": word_count
        }

    # ==========================================================
    # 🧠 PERSONALITY DETECTION (WRITING PERSONA)
    # ==========================================================
    def detect_personality(self, words, avg_sentence_length, formality_score):
        words_set = set(words)

        professional_words = {
            "experience", "skills", "responsibilities",
            "organization", "management", "professional",
            "role", "position", "career"
        }

        academic_words = {
            "research", "study", "analysis", "methodology",
            "results", "discussion", "theory", "literature"
        }

        casual_words = {
            "hey", "hi", "thanks", "cool", "awesome",
            "fun", "happy", "lol"
        }

        assertive_words = {
            "led", "achieved", "executed", "delivered",
            "managed", "developed", "implemented", "owned"
        }

        scores = {
            "Professional": (
                formality_score * 0.6 +
                avg_sentence_length / 25 +
                len(words_set & professional_words) * 0.03
            ),
            "Academic": (
                avg_sentence_length / 22 +
                len(words_set & academic_words) * 0.04
            ),
            "Casual Friendly": (
                len(words_set & casual_words) * 0.06 +
                (1 - formality_score)
            ),
            "Confident Assertive": (
                len(words_set & assertive_words) * 0.05 +
                formality_score * 0.3
            ),
            "Neutral Informational": 0.4
        }

        return max(scores, key=scores.get)
