import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@postgres:5432/genesis")

LITELLM_URL = os.getenv("LITELLM_API_URL", "http://192.168.31.205:4000")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "groq/llama3-8b-8192")

COLLECTION_NAME = "genesis-knowledge"
