import os

# Обязательные (должны быть установлены пользователем)
QDRANT_HOST = os.getenv("QDRANT_HOST")
if not QDRANT_HOST:
    raise ValueError("QDRANT_HOST environment variable must be set")

QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise ValueError("POSTGRES_URL environment variable must be set")

# Опциональные с безопасными дефолтами
LITELLM_API_URL = os.getenv("LITELLM_API_URL", "http://localhost:4000")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "groq/llama3-8b-8192")
COLLECTION_NAME = "genesis-knowledge"
