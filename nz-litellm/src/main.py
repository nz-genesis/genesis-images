import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from lightrag.components.model_client import OpenAIClient
from .config import *
from .init_collections import init_qdrant, init_postgres
from .retriever_fallback import FallbackRetriever
from .rag_manager import RAGManager

# ----------- ЛОГГЕР -----------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - [%(levelname)s] - [nz-lightrag] - %(message)s"
)
logger = logging.getLogger("nz-lightrag")

# ----------- FASTAPI -----------
app = FastAPI(title="NZ LightRAG v2.1", version="2.1.0")

# ----------- ИНИЦИАЛИЗАЦИЯ -----------
logger.info("Проверка доступности Qdrant (для будущих версий)…")
qdrant_ok = init_qdrant()

logger.info("Проверка PostgreSQL…")
postgres_ok = init_postgres(POSTGRES_URL)

# ✅ Правильная инициализация клиента LLM
# В этой версии lightrag не принимает base_url напрямую,
# поэтому задаём его через переменную окружения.
os.environ["OPENAI_API_BASE"] = LITELLM_URL
os.environ["OPENAI_API_KEY"] = "none"

llm_client = OpenAIClient()  # без аргументов

retriever = FallbackRetriever(
    postgres_url=POSTGRES_URL if postgres_ok else None,
    llm_client=llm_client
)

rag = RAGManager(
    llm_client=llm_client,
    model_name=DEFAULT_MODEL,
    retriever=retriever,
    system_prompt="Ты – эксперт по документации Genesis. Отвечай только на основе фактов."
)

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
        response = rag.ask(query)
        return {
            "id": f"chatcmpl-{os.urandom(16).hex()}",
            "object": "chat.completion",
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response.data},
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
