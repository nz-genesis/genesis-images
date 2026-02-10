import os

# LiteLLM Configuration
LITELLM_API_URL = os.getenv("LITELLM_API_URL", "http://localhost:4000")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "groq/llama3-8b-8192")

# Optional (for future use)
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
POSTGRES_URL = os.getenv("POSTGRES_URL")
COLLECTION_NAME = "genesis-knowledge"
