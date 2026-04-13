"""
PersonaWrite AI — RAG Engine
Retrieval-Augmented Generation using sentence-transformers + FAISS.

Provides document chunking, embedding, and similarity retrieval so that
the generator can inject relevant user-document context into prompts.

This module is entirely self-contained. If any dependency is missing or
an error occurs, it degrades gracefully (returns empty context).
"""

from __future__ import annotations

import hashlib
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# --------------- lazy imports (avoid crash if deps missing) ---------------

_faiss = None
_model = None
_model_load_attempted = False


def _ensure_deps():
    """Import heavy libraries on first use so the app starts fast."""
    global _faiss
    if _faiss is None:
        try:
            import faiss  # type: ignore
            _faiss = faiss
        except ImportError:
            logger.warning("faiss-cpu is not installed — RAG disabled.")
            raise


def _get_model():
    """Load the sentence-transformer model once and cache it."""
    global _model, _model_load_attempted
    if _model is not None:
        return _model
    if _model_load_attempted:
        return None
    _model_load_attempted = True
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model
    except Exception as e:
        logger.warning("Failed to load sentence-transformers model: %s", e)
        return None


# ========================= TEXT CHUNKING =========================

def _chunk_text(text: str, min_words: int = 200, max_words: int = 300) -> List[str]:
    """
    Split *text* into chunks of roughly *min_words*–*max_words* words.
    Splits on sentence boundaries ('. ') to keep chunks readable.
    """
    if not text or not text.strip():
        return []

    sentences = text.replace("\n", " ").split(". ")
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        words = sentence.split()
        word_count = len(words)

        if current_len + word_count > max_words and current:
            chunks.append(". ".join(current) + ".")
            current = []
            current_len = 0

        current.append(sentence)
        current_len += word_count

    if current:
        chunks.append(". ".join(current) + ".")

    return chunks


# ========================= CONTENT HASH =========================

def _content_hash(texts: List[str]) -> str:
    """Deterministic hash of a list of texts — used to detect changes."""
    h = hashlib.sha256()
    for t in texts:
        h.update(t.encode("utf-8", errors="ignore"))
    return h.hexdigest()


# ========================= RAG INDEX (in-memory cache) =========================

class RAGIndex:
    """
    Holds a FAISS index + the source chunks so we can retrieve by
    similarity without re-encoding every generation call.
    """

    def __init__(self):
        self._index = None          # faiss.IndexFlatIP
        self._chunks: List[str] = []
        self._hash: Optional[str] = None  # hash of source texts

    # ---- public API --------------------------------------------------------

    def build(self, texts: List[str]) -> bool:
        """
        Build (or rebuild) the index from a list of raw document texts.
        Returns True on success, False on failure.
        If the content hasn't changed since the last build, this is a no-op.
        """
        if not texts:
            return False

        new_hash = _content_hash(texts)
        if new_hash == self._hash and self._index is not None:
            return True  # already up-to-date

        try:
            _ensure_deps()
            model = _get_model()
            if model is None:
                return False

            combined = "\n".join(texts)
            chunks = _chunk_text(combined)
            if not chunks:
                return False

            import numpy as np
            embeddings = model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)
            # Normalize for cosine similarity via inner-product search
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1
            embeddings = embeddings / norms

            dim = embeddings.shape[1]
            index = _faiss.IndexFlatIP(dim)
            index.add(embeddings.astype("float32"))

            self._index = index
            self._chunks = chunks
            self._hash = new_hash
            logger.info("RAG index built: %d chunks, dim=%d", len(chunks), dim)
            return True

        except Exception as e:
            logger.warning("RAG index build failed: %s", e)
            return False

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Return the *top_k* most relevant chunks for *query*.
        Returns [] on any error or if the index is empty.
        """
        if self._index is None or not self._chunks:
            return []

        try:
            model = _get_model()
            if model is None:
                return []

            import numpy as np
            q_emb = model.encode([query], show_progress_bar=False, convert_to_numpy=True)
            norms = np.linalg.norm(q_emb, axis=1, keepdims=True)
            norms[norms == 0] = 1
            q_emb = q_emb / norms

            k = min(top_k, len(self._chunks))
            _, indices = self._index.search(q_emb.astype("float32"), k)

            results = []
            for idx in indices[0]:
                if 0 <= idx < len(self._chunks):
                    results.append(self._chunks[idx])
            return results

        except Exception as e:
            logger.warning("RAG retrieval failed: %s", e)
            return []


# ========================= MODULE-LEVEL SINGLETON =========================

_rag_index = RAGIndex()


def build_rag_index(texts: List[str]) -> bool:
    """Build / refresh the global RAG index from user-uploaded texts."""
    return _rag_index.build(texts)


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> List[str]:
    """
    Retrieve the most relevant document chunks for a query.
    Safe to call even if the index was never built — returns [].
    """
    return _rag_index.retrieve(query, top_k)
