"""
main.py — Основной FastAPI сервис "nz-skill-runner".
- Авторизация через X-API-Key (API_TOKEN в .env).
- /skills -> предоставляет "меню" всех доступных Скиллов.
- /skills/{name} -> предоставляет полное содержимое одного Скилла.
- /skills/{name}/execute -> выполняет код Скилла в безопасной "песочнице".
- /refresh-skills -> перезагружает кэш Скиллов в памяти (репозиторий обновляется на хосте).
"""
import os
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Security, Path
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from skill_loader import skills_registry
import code_executor
from mcp_client import write_execution_result

# Настройка логирования
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s - [%(levelname)s] - [nz-skill-runner] - %(message)s")
logger = logging.getLogger("nz-skill-runner")

app = FastAPI(title="NZ Skill Runner", version="1.0.0")

# Настройка безопасности API
API_TOKEN = os.getenv("API_TOKEN")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    """Проверяет переданный API-ключ."""
    if not API_TOKEN or api_key != API_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

# Модель для входящего запроса на выполнение
class ExecuteRequest(BaseModel):
    parameters: Dict[str, Any] = {}
    capture_to_memory: bool = True

# Действие при старте приложения
@app.on_event("startup")
async def startup_event():
    """При старте загружаем все Скиллы в память."""
    logger.info("Startup: загрузка Скиллов из директории...")
    skills_registry.load_skills()

# --- Эндпоинты API ---

@app.get("/skills", summary="Получить 'меню' доступных Скиллов", tags=["Skills"])
async def get_skills_menu() -> List[Dict[str, Any]]:
    """Возвращает краткий список всех загруженных Скиллов (name, description, tags)."""
    return skills_registry.get_menu()

@app.get("/skills/{skill_name:path}", summary="Получить полное содержимое Скилла", tags=["Skills"])
async def get_skill_content(skill_name: str = Path(..., description="Полное имя Скилла, например 'core/example'")) -> Dict[str, Any]:
    """Возвращает полное содержимое одного Скилла, включая инструкции и метаданные."""
    return skills_registry.get_skill(skill_name)

@app.post("/skills/{skill_name:path}/execute", summary="Выполнить скрипт из Скилла", tags=["Execution"], dependencies=[Depends(get_api_key)])
async def execute_skill_code(skill_name: str, request: ExecuteRequest):
    """Выполняет код, связанный со Скиллом, в безопасной Docker-песочнице."""
    skill = skills_registry.get_skill(skill_name)
    script_path = skill.get("script_path")
    if not script_path or not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Исполняемый скрипт для этого Скилла не найден.")
    
    result = await code_executor.run_in_container(script_path, request.parameters)
    
    if request.capture_to_memory and result.get("status") == "success":
        mcp_payload = {"skill_name": skill_name, "parameters": request.parameters, "result": result}
        mcp_response = write_execution_result(mcp_payload)
        result["mcp_push"] = mcp_response
        
    return result

@app.post("/refresh-skills", summary="Перезагрузить Скиллы из директории", tags=["Management"], dependencies=[Depends(get_api_key)])
async def refresh_skills():
    """
    Перезагружает реестр Скиллов в памяти. 
    Предполагается, что репозиторий на хосте уже обновлен через 'git pull'.
    """
    logger.info("Получен запрос на обновление Скиллов. Перезагрузка из директории...")
    skills_registry.load_skills()
    return {"status": "success", "message": "Реестр Скиллов успешно перезагружен."}

@app.get("/health", summary="Проверка состояния", tags=["Management"])
async def health_check():
    """Простой эндпоинт для healthcheck."""
    return {"status": "ok", "skills_loaded": len(skills_registry.get_menu())}
     # v1.0.1 - Triggering CI build # Final trigger v119.0
# Final trigger v123.0
# Final trigger v124.0
# Final trigger v124.2
