"""
nz-mem0 MemoryStore Implementation
SQLAlchemy + Qdrant for persistent and vector storage
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Optional

from sqlalchemy import Column, String, Text, create_engine, select, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.mcp_mem0.embeddings import EmbeddingBackend
from src.mcp_mem0.qdrant_store import QdrantStore
from src.mcp_mem0.settings import Settings

logger = logging.getLogger(__name__)

Base = declarative_base()
settings = Settings()


class MemoryRecord(Base):
    """SQLAlchemy model for memory records."""

    __tablename__ = "memories"

    session_id = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text)  # JSON serialized
    embedding = Column(String(10000))  # Vector as JSON
    created_at = Column(String(50))  # ISO format timestamp
    updated_at = Column(String(50))  # ISO format timestamp


class MemoryStore:
    """
    Core memory store combining SQL and vector databases.

    Features:
    - Persistent storage in PostgreSQL/SQLite
    - Vector search via Qdrant
    - Automatic embeddings generation
    - Session-based isolation
    """

    def __init__(self):
        """Initialize memory store with database engines."""
        # Create database engine
        self.engine = create_engine(
            settings.MEM0_DATABASE_URL,
            pool_size=settings.MEM0_DATABASE_POOL_SIZE,
            max_overflow=settings.MEM0_DATABASE_MAX_OVERFLOW,
            echo=settings.DEBUG,
        )

        # Create tables
        Base.metadata.create_all(self.engine)

        # Session factory
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Initialize vector store
        self.vector_store = QdrantStore(
            url=settings.MEM0_QDRANT_URL,
            api_key=settings.MEM0_QDRANT_API_KEY,
            collection_name=settings.MEM0_QDRANT_COLLECTION,
        )

        # Initialize embeddings generator
        self.embeddings = EmbeddingBackend(
            model=settings.MEM0_EMBEDDING_MODEL,
            dim=settings.MEM0_EMBEDDING_DIMENSION,
        )

        logger.info("✅ MemoryStore initialized")

    def store(
        self,
        session_id: str,
        key: str,
        value: Dict[str, Any],
        ttl: Optional[int] = None,
        embed: Optional[List[float]] = None,
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Store a memory record.

        Args:
            session_id: User/session identifier
            key: Memory key
            value: Memory value (any JSON-serializable object)

        Returns:
            Dictionary with stored record metadata
        """
        try:
            # Serialize value to JSON
            value_json = json.dumps(value)

            # Generate embedding
            embedding_vector = self.embeddings.encode(value_json)

            # Create memory record
            now = datetime.utcnow().isoformat()
            record = MemoryRecord(
                session_id=session_id,
                key=key,
                value=value_json,
                embedding=json.dumps(embedding_vector),
                created_at=now,
                updated_at=now,
            )

            # Store in SQL database
            session = self.SessionLocal()
            try:
                session.merge(record)  # Insert or update
                session.commit()
            finally:
                session.close()

            # Store in vector database
            vector_id = f"{session_id}:{key}"
            vector_id_hash = hash(vector_id) % (10**9)  # ✅ ИСПРАВЛЕНО: Convert to int
            
            self.vector_store.upsert_vector(  # ✅ ИСПРАВЛЕНО: upsert → upsert_vector
                item_id=vector_id_hash,
                vector=embedding_vector,
                payload={
                    "vector_id": vector_id,  # Keep original ID
                    "session_id": session_id,
                    "key": key,
                    "timestamp": now,
                },
            )

            logger.info(f"✅ Stored memory: {session_id}/{key}")

            return {
                "id": vector_id,
                "session_id": session_id,
                "key": key,
                "timestamp": now,
            }

        except Exception as e:
            logger.error(f"❌ Error storing memory: {e}")
            raise

    def retrieve(
        self,
        session_id: str,
        key: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific memory record.

        Args:
            session_id: User/session identifier
            key: Memory key

        Returns:
            Memory value or None if not found
        """
        try:
            session = self.SessionLocal()
            try:
                stmt = select(MemoryRecord).where(
                    (MemoryRecord.session_id == session_id)
                    & (MemoryRecord.key == key)
                )
                record = session.execute(stmt).scalar_one_or_none()

                if not record:
                    logger.warning(f"⚠️  Memory not found: {session_id}/{key}")
                    return None

                return {
                    "key": record.key,
                    "value": json.loads(record.value),
                    "timestamp": record.updated_at,
                }

            finally:
                session.close()

        except Exception as e:
            logger.error(f"❌ Error retrieving memory: {e}")
            raise

    def search(
        self,
        session_id: str,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search memories using vector similarity.

        Args:
            session_id: User/session identifier
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of matching memories sorted by relevance
        """
        try:
            # Generate query embedding
            query_vector = self.embeddings.encode(query)

            # Search in vector store
            results = self.vector_store.search_vector(  # ✅ ИСПРАВЛЕНО: search → search_vector
                query_vector=query_vector,
                limit=limit,
            )

            # Filter by session_id and enrich with SQL data
            enriched_results = []
            for result in results:
                payload = result.get("payload", {})
                result_session_id = payload.get("session_id")
                result_key = payload.get("key")
                
                # Filter by session_id
                if result_session_id != session_id:
                    continue

                # Retrieve full record from SQL
                if result_key:
                    memory = self.retrieve(session_id, result_key)
                    if memory:
                        enriched_results.append({
                            **memory,
                            "score": result.get("score", 0),
                        })

            logger.info(f"✅ Found {len(enriched_results)} memories for query")
            return enriched_results

        except Exception as e:
            logger.error(f"❌ Error searching memories: {e}")
            raise

    def recent(
        self,
        session_id: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get recent memories for a session.

        Args:
            session_id: User/session identifier
            limit: Maximum number of results

        Returns:
            List of recent memories ordered by timestamp (newest first)
        """
        try:
            session = self.SessionLocal()
            try:
                stmt = (
                    select(MemoryRecord)
                    .where(MemoryRecord.session_id == session_id)
                    .order_by(desc(MemoryRecord.updated_at))
                    .limit(limit)
                )
                records = session.execute(stmt).scalars().all()

                results = [
                    {
                        "key": r.key,
                        "value": json.loads(r.value),
                        "timestamp": r.updated_at,
                    }
                    for r in records
                ]

                logger.info(f"✅ Retrieved {len(results)} recent memories")
                return results

            finally:
                session.close()

        except Exception as e:
            logger.error(f"❌ Error retrieving recent memories: {e}")
            raise

    def delete(self, session_id: str, key: str) -> bool:
        """
        Delete a memory record.

        Args:
            session_id: User/session identifier
            key: Memory key

        Returns:
            True if deleted, False if not found
        """
        try:
            # Delete from SQL
            session = self.SessionLocal()
            try:
                stmt = select(MemoryRecord).where(
                    (MemoryRecord.session_id == session_id)
                    & (MemoryRecord.key == key)
                )
                record = session.execute(stmt).scalar_one_or_none()

                if not record:
                    logger.warning(f"⚠️  Memory not found: {session_id}/{key}")
                    return False

                session.delete(record)
                session.commit()
            finally:
                session.close()

            # Delete from vector store
            vector_id = f"{session_id}:{key}"
            vector_id_hash = hash(vector_id) % (10**9)  # ✅ ИСПРАВЛЕНО: Convert to int
            
            self.vector_store.delete_vector(vector_id_hash)  # ✅ ИСПРАВЛЕНО: delete → delete_vector

            logger.info(f"✅ Deleted memory: {session_id}/{key}")
            return True

        except Exception as e:
            logger.error(f"❌ Error deleting memory: {e}")
            raise


# Global instance
memory_store = MemoryStore()
