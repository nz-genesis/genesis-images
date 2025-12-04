"""
Configuration for nz-mem0 using pydantic v2 + pydantic-settings.
This file exposes `Settings` and `get_settings()` cached factory.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    NZ-MEM0 configuration (Pydantic v2 + pydantic-settings)
    Fully compatible with Genesis architecture.
    """

    # ---------------------------
    # Core Server Settings
    # ---------------------------
    host: str = Field(default="0.0.0.0", description="Bind host")
    port: int = Field(default=8090, description="Bind port")

    # ---------------------------
    # Storage / DB
    # ---------------------------
    MEM0_DATABASE_URL: Optional[str] = Field(
        default=None,
        description="SQLAlchemy DB URL (optional). If absent use sqlite file at db_path."
    )
    db_path: str = Field(default="/data/mem0.db", description="Fallback sqlite file path")

    # ---------------------------
    # Qdrant (vector DB) / embeddings
    # ---------------------------
    MEM0_QDRANT_URL: Optional[str] = Field(
        default=None,
        description="qdrant HTTP/grpc endpoint, ex: http://qdrant:6333 or grpc://..."
    )
    MEM0_QDRANT_API_KEY: Optional[str] = Field(default=None, description="Qdrant API key if required")
    MEM0_EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model id or path"
    )

    # ---------------------------
    # Logging / behavior
    # ---------------------------
    LOG_LEVEL: str = Field(default="info", description="app log level")
    API_KEY: Optional[str] = Field(default=None, description="Optional service API key")

    # ---------------------------
    # Audit / Telemetry (legacy mem0 fields preserved)
    # ---------------------------
    AUDIT_ENABLED: bool = Field(default=False, description="Enable auditing of memory operations")
    AUDIT_LOG_PATH: str = Field(default="/data/audit.log", description="Path to audit log file")

    # ---------------------------
    # Runtime / feature toggles
    # ---------------------------
    MEM0_USE_QDRANT: bool = Field(default=False, description="If true, attempt to use Qdrant backend")
    MEM0_DISABLE_EMBEDDINGS: bool = Field(default=False, description="Disable embedding generation (test)")

    # ---------------------------
    # Pydantic Settings Config
    # ---------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MEM0_",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings factory used across the application.
    Use get_settings() instead of creating Settings() multiple times.
    """
    return Settings()
