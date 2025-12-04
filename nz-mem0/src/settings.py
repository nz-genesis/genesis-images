"""
Full Settings for nz-mem0 (restored stable config, Genesis L2).
This Settings object exposes fields that existing code expects (including
uppercase attributes like AUDIT_ENABLED and MEM0_QDRANT_URL).
Uses pydantic-settings when available (pydantic v2+ compatible).
"""

import os
from functools import lru_cache
from typing import Optional

# Prefer pydantic-settings (BaseSettings moved there in newer pydantic).
# Fallback to pydantic.BaseSettings if available (for older environments).
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except Exception:
    # If fallback required, import from pydantic (best-effort).
    from pydantic import BaseModel as _BaseModel  # type: ignore
    class BaseSettings(_BaseModel):  # minimal fallback (rare)
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

    # Provide a minimal SettingsConfigDict for compatibility usage in code below
    SettingsConfigDict = dict

from pydantic import Field


class Settings(BaseSettings):
    """
    NZ-MEM0 configuration (stable, backward-compatible).
    Field names intentionally include uppercase constants because other modules
    in project read .AUDIT_ENABLED, .MEM0_QDRANT_URL, etc.
    """

    # ---------------------------
    # Core Server Settings
    # ---------------------------
    host: str = Field(default="0.0.0.0", description="Bind address")
    port: int = Field(default=8090, description="HTTP port")

    # ---------------------------
    # Storage / DB
    # ---------------------------
    # Generic DB URL (overrides sqlite path)
    MEM0_DATABASE_URL: Optional[str] = Field(default=None, description="SQLAlchemy DB URL (optional)")
    # Local sqlite fallback path (used when MEM0_DATABASE_URL is not set)
    DB_PATH: str = Field(default="/data/mem0.db", description="Fallback sqlite file path")

    # ---------------------------
    # Qdrant / Vector DB
    # ---------------------------
    MEM0_QDRANT_URL: Optional[str] = Field(default=None, description="Qdrant HTTP/GRPC endpoint (optional)")
    MEM0_QDRANT_API_KEY: Optional[str] = Field(default=None, description="Qdrant API key (if required)")

    # ---------------------------
    # Logging
    # ---------------------------
    LOG_LEVEL: str = Field(default="info", description="Log level")

    # ---------------------------
    # Embeddings / Models
    # ---------------------------
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Default embedding model")

    # ---------------------------
    # Security
    # ---------------------------
    API_KEY: Optional[str] = Field(default=None, description="Optional API key for simple auth")

    # ---------------------------
    # Audit / Telemetry (names kept for backwards compatibility)
    # ---------------------------
    AUDIT_ENABLED: bool = Field(default=False, description="Enable audit logging")
    AUDIT_LOG_PATH: str = Field(default="/data/audit.log", description="Path to audit log file")

    # ---------------------------
    # Other runtime toggles
    # ---------------------------
    MEM0_ENABLE_EMBEDDINGS: bool = Field(default=True, description="Enable embeddings features")
    MEM0_DEBUG_MODE: bool = Field(default=False, description="Enable debug mode (dev only)")

    # ---------------------------
    # Pydantic settings metadata (works with pydantic-settings)
    # ---------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",   # we intentionally support both MEM0_ and non-prefixed envs
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
