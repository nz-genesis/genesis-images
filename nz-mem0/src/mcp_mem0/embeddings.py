"""
Embeddings backend wrapper.
Primary: sentence-transformers (SentenceTransformer)
Fallback: deterministic hashing -> numeric vector (stable)
"""

from typing import List, Any
import hashlib
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_AVAILABLE = True
except Exception:
    SentenceTransformer = None  # type: ignore
    _SENTENCE_AVAILABLE = False

class EmbeddingBackend:
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2", dim: int = 384):
        self.model_name = model
        self.dim = dim
        self.model = None
        if _SENTENCE_AVAILABLE:
            try:
                self.model = SentenceTransformer(model)
                # override dim if model reveals it
                try:
                    self.dim = self.model.get_sentence_embedding_dimension()
                except Exception:
                    pass
            except Exception:
                self.model = None

    def encode(self, text: str) -> List[float]:
        """
        Returns embedding vector (list[float]).
        If model not available — deterministic fallback vector based on sha256.
        """
        if self.model:
            vec = self.model.encode([text], show_progress_bar=False)[0]
            return [float(x) for x in vec]

        # fallback deterministic vector: use sha256 -> bytes -> map to floats
        h = hashlib.sha256(text.encode("utf-8")).digest()
        arr = np.frombuffer(h, dtype=np.uint8).astype(np.float32)
        # repeat/trim to desired dim
        if arr.size < self.dim:
            reps = int(np.ceil(self.dim / arr.size))
            arr = np.tile(arr, reps)[: self.dim]
        else:
            arr = arr[: self.dim]
        # normalize to [-1,1]
        vec = (arr / 255.0) * 2.0 - 1.0
        return [float(x) for x in vec]
