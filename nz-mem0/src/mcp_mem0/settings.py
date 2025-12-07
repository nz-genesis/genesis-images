"""
nz-mem0 Settings Configuration
Pydantic v2 settings with environment variable support
"""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings managed via Pydantic v2 BaseSettings.
    All values can be overridden via environment variables.
    """

    # FastAPI Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8090"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database Configuration (PostgreSQL)
    MEM0_DATABASE_URL: Optional[str] = os.getenv(
        "MEM0_DATABASE_URL",
        "sqlite:///./mem0.db",  # Fallback to SQLite for local development
    )
    MEM0_DATABASE_POOL_SIZE: int = int(os.getenv("MEM0_DATABASE_POOL_SIZE", "10"))
    MEM0_DATABASE_MAX_OVERFLOW: int = int(os.getenv("MEM0_DATABASE_MAX_OVERFLOW", "20"))

    # Qdrant Vector Store Configuration
    MEM0_QDRANT_URL: Optional[str] = os.getenv("MEM0_QDRANT_URL", "http://localhost:6333")
    MEM0_QDRANT_API_KEY: Optional[str] = os.getenv("MEM0_QDRANT_API_KEY", None)
    MEM0_QDRANT_COLLECTION: str = os.getenv("MEM0_QDRANT_COLLECTION", "mem0_vectors")

    # Redis Cache (Optional)
    MEM0_REDIS_URL: Optional[str] = os.getenv("MEM0_REDIS_URL", None)

    # Embeddings Configuration
    MEM0_EMBEDDING_MODEL: str = os.getenv(
        "MEM0_EMBEDDING_MODEL",
        "all-MiniLM-L6-v2",  # Small, efficient model for CPU
    )
    MEM0_EMBEDDING_DIMENSION: int = int(os.getenv("MEM0_EMBEDDING_DIMENSION", "384"))
    MEM0_EMBEDDING_BATCH_SIZE: int = int(os.getenv("MEM0_EMBEDDING_BATCH_SIZE", "32"))

    # Memory Store Configuration
    MEM0_MEMORY_BATCH_SIZE: int = int(os.getenv("MEM0_MEMORY_BATCH_SIZE", "32"))
    MEM0_MEMORY_SEARCH_LIMIT: int = int(os.getenv("MEM0_MEMORY_SEARCH_LIMIT", "10"))
    MEM0_MEMORY_SIMILARITY_THRESHOLD: float = float(
        os.getenv("MEM0_MEMORY_SIMILARITY_THRESHOLD", "0.7")
    )

    # API Security (Optional)
    API_KEY: Optional[str] = os.getenv("API_KEY", None)
    API_KEY_HEADER: str = "X-API-Key"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True

    def __init__(self, **data):
        """Initialize settings and validate."""
        super().__init__(**data)
        self._validate()

    def _validate(self):
        """Validate settings on initialization."""
        if not self.MEM0_QDRANT_URL:
            print("⚠️  Warning: MEM0_QDRANT_URL not set, using default http://localhost:6333")

        if not self.MEM0_DATABASE_URL:
            print("⚠️  Warning: MEM0_DATABASE_URL not set, using SQLite fallback")

        if self.DEBUG:
            print("🔍 Debug mode enabled")


# Global settings instance
settings = Settings()