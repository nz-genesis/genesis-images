import os
import logging
import litellm
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .config import *
from .init_collections import init_qdrant, init_postgres

# ----------- LITELLM CLIENT -----------
def get_litellm_client():
    """Создаёт конфиг для litellm клиента."""
    return {
        "api_base": os.environ.get("OPENAI_API_BASE", LITELLM_URL),
        "api_key": os.environ.get("OPENAI_API_KEY", "none")
    }


# ----------- ЛОГГЕЛ -----------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - [%(levelname)s] - [nz-litellm] - %(message)s"
)
logger = logging.getLogger("nz-litellm")

# ----------- FASTAPI -----------
app = FastAPI(title="NZ LiteLLM", version="2.2.0")

# ----------- ИНИЦИАЛИЗАЦИЯ -----------
logger.info("Проверка доступности Qdrant (для будущих версий)…")
qdrant_ok = init_qdrant()

logger.info("Проверка PostgreSQL…")
postgres_ok = init_postgres(POSTGRES_URL)

# Устанавливаем переменные окружения для litellm
os.environ["OPENAI_API_BASE"] = LITELLM_URL
os.environ["OPENAI_API_KEY"] = "none"

# ----------- API-МОДЕЛИ -----------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]

# ----------- ENDPOINTS -----------
@app.post("/v1/chat/completions")
async def chat(request: ChatCompletionRequest):
    query = request.messages[-1].content
    try:
        # Используем litellm напрямую
        client_config = get_litellm_client()
        response = litellm.completion(
            model=request.model or DEFAULT_MODEL,
            messages=[{"role": "user", "content": query}],
            api_base=client_config["api_base"],
            api_key=client_config["api_key"]
        )
        return {
            "id": f"chatcmpl-{os.urandom(16).hex()}",
            "object": "chat.completion",
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response.choices[0].message.content},
                "finish_reason": "stop"
            }]
        }
    except Exception as e:
        logger.exception("Ошибка при обработке запроса.")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "qdrant_available_for_future_use": qdrant_ok,
        "postgres_connected": postgres_ok
    }
