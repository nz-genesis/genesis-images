"""
Memory backend manager for nz-mem0.
Compatible with Genesis L2 Settings (MEM0_DATABASE_URL, Qdrant, sqlite fallback).
"""

import os
import json
from typing import Optional, Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .sqlite_store import SQLiteStore
from .qdrant_store import QdrantStore
from .embeddings import EmbeddingBackend


class MemoryStore:
    """
    Core memory manager. Initializes:
      • SQL backend (SQLite or SQLAlchemy DB)
      • Qdrant vector backend (optional)
      • Embeddings backend
    """

    def __init__(self, settings):
        self.settings = settings

        self.sql_engine: Optional[Engine] = None
        self.sql_store: Optional[SQLiteStore] = None
        self.qdrant: Optional[QdrantStore] = None
        self.embeddings: Optional[EmbeddingBackend] = None

        self._init_backends()

    # ---------------------------------------------------------
    # Backend initialization
    # ---------------------------------------------------------
    def _init_backends(self):
        # -----------------------------------------------------
        # SQL BACKEND
        # -----------------------------------------------------
        db_url = self.settings.MEM0_DATABASE_URL

        if db_url:
            # SQLAlchemy mode
            self.sql_engine = create_engine(db_url)
            self.sql_store = SQLiteStore(engine=self.sql_engine)
        else:
            # SQLite fallback
            sqlite_path = self.settings.DB_PATH
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)

            self.sql_engine = create_engine(f"sqlite:///{sqlite_path}")
            self.sql_store = SQLiteStore(engine=self.sql_engine)

        # -----------------------------------------------------
        # QDRANT BACKEND (optional)
        # -----------------------------------------------------
        if self.settings.MEM0_QDRANT_URL:
            self.qdrant = QdrantStore(
                url=self.settings.MEM0_QDRANT_URL,
                api_key=self.settings.MEM0_QDRANT_API_KEY,
            )

        # -----------------------------------------------------
        # EMBEDDINGS BACKEND
        # -----------------------------------------------------
        if self.settings.MEM0_ENABLE_EMBEDDINGS:
            self.embeddings = EmbeddingBackend(model=self.settings.EMBEDDING_MODEL)

    # ---------------------------------------------------------
    # Basic operations
    # ---------------------------------------------------------
    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Add memory item:
          • SQL record
          • Optional embedding + vector index
        """
        item_id = self.sql_store.add(text=text, metadata=metadata)

        # Vector index update
        if self.qdrant and self.embeddings:
            embedding = self.embeddings.encode(text)
            self.qdrant.upsert_vector(item_id=item_id, vector=embedding)

        return {"id": item_id, "text": text, "metadata": metadata}

    def search(self, query: str, limit: int = 5) -> Dict:
        """
        Hybrid vector + SQL search:
          • If Qdrant+embeddings available → vector search first
          • Else → SQL-only fallback
        """
        if self.qdrant and self.embeddings:
            query_vec = self.embeddings.encode(query)
            vector_hits = self.qdrant.search_vector(query_vec, limit=limit)
            sql_items = self.sql_store.get_many([h["id"] for h in vector_hits])
            return sql_items

        # fallback: SQL LIKE search
        return self.sql_store.search_text(query, limit=limit)

    def get(self, item_id: int) -> Optional[Dict]:
        return self.sql_store.get(item_id)

    def delete(self, item_id: int) -> bool:
        self.sql_store.delete(item_id)
        if self.qdrant:
            self.qdrant.delete_vector(item_id)
        return True

    # ---------------------------------------------------------
    # Bulk export (debug/dev)
    # ---------------------------------------------------------
    def export_all(self) -> Dict:
        return {
            "items": self.sql_store.export_all(),
        }
