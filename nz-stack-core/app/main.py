"""
nz-stack-core

Thinking Layer сервиса GENESIS (Phase 3.3)

Назначение:
- приём INTENT
- базовая валидация
- заглушка policy
- заглушка деривации EXECUTION_REQUEST

ВАЖНО:
- execution здесь НЕ выполняется
- sandbox НЕ вызывается
- memory напрямую НЕ используется
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="nz-stack-core",
    version="0.1.0",
)


class Intent(BaseModel):
    """
    Минимальная форма INTENT (skeleton).

    Это НЕ финальная схема.
    Расширяется аддитивно в Phase 3.4+.
    """
    intent_id: str
    source: str
    payload: dict


@app.get("/health")
def health():
    """
    Healthcheck для Portainer и orchestration.
    """
    return {"status": "ok"}


@app.post("/intent")
def receive_intent(intent: Intent):
    """
    Точка приёма INTENT.

    На этапе skeleton:
    - policy = always allow
    - execution НЕ вызывается
    - возвращается заглушка execution_request_id
    """

    # Заглушка policy
    allowed = True

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Intent rejected by policy"
        )

    # Заглушка деривации EXECUTION_REQUEST
    execution_request_id = f"exec-{intent.intent_id}"

    return {
        "status": "accepted",
        "intent_id": intent.intent_id,
        "execution_request_id": execution_request_id,
    }
