"""
code_executor: выполнение указанного скрипта в изолированном контейнере (через DinD).
Принципы безопасности: network_disabled=True, read_only bind, no-new-privileges, cap_drop, tmpfs.
"""
import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import docker
from docker.errors import APIError

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("nz-skill-runner.code_executor")

# Конфигурация "песочницы" из переменных окружения
DEFAULT_IMAGE = os.getenv("EXECUTOR_IMAGE", "python:3.11-slim")
DEFAULT_MEM_LIMIT = os.getenv("EXECUTOR_MEM_LIMIT", "256m")
DEFAULT_CPU_QUOTA = int(os.getenv("EXECUTOR_CPU_QUOTA", "50000"))
DEFAULT_TIMEOUT = int(os.getenv("EXECUTOR_TIMEOUT", "30"))
MAX_LOG_CHARS = 200000

# Пул потоков для выполнения блокирующих Docker-операций
_executor = ThreadPoolExecutor(max_workers=int(os.getenv("EXECUTOR_MAX_WORKERS", "4")))

try:
    docker_client = docker.from_env()
except Exception:
    docker_client = None

def _sync_run_container(script_name: str, skill_dir: str, parameters: Dict[str, Any],
                        image: str, mem_limit: str, cpu_quota: Optional[int],
                        timeout: int) -> Dict[str, Any]:
    """Синхронная функция, которая реально выполняет Docker-операции."""
    if docker_client is None:
        return {"status": "error", "message": "Docker client не инициализирован."}

    env_vars = {"INPUT_PARAMS": json.dumps(parameters)}
    workdir = "/app"
    binds = {skill_dir: {"bind": workdir, "mode": "ro"}}
    
    container = None
    try:
        container = docker_client.containers.run(
            image=image,
            command=["python", script_name],
            environment=env_vars,
            volumes=binds,
            working_dir=workdir,
            detach=True,
            remove=False, # Удалим вручную после сбора логов
            network_disabled=True,
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
            read_only=True,
            tmpfs={workdir + "/tmp": ""},
            user=os.getenv("EXECUTOR_USER", "65534"),
            mem_limit=mem_limit,
            cpu_quota=cpu_quota,
        )
        
        try:
            result = container.wait(timeout=timeout)
            exit_code = result.get("StatusCode", -1)
        except Exception:
            logger.warning(f"Контейнер {container.short_id} превысил таймаут ({timeout}s), принудительное завершение.")
            try:
                container.kill()
            except APIError:
                pass # Контейнер мог уже завершиться
            exit_code = -1

        stdout = container.logs(stdout=True, stderr=False).decode('utf-8', errors='replace')[:MAX_LOG_CHARS]
        stderr = container.logs(stdout=False, stderr=True).decode('utf-8', errors='replace')[:MAX_LOG_CHARS]
        
        parsed_output = None
        try:
            parsed_output = json.loads(stdout)
        except json.JSONDecodeError:
            pass

        return {
            "status": "success" if exit_code == 0 else "error",
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "parsed_output": parsed_output
        }

    except Exception as e:
        logger.exception("Ошибка во время выполнения контейнера.")
        return {"status": "error", "message": str(e)}
    finally:
        if container:
            try:
                container.remove(force=True)
            except APIError:
                pass

async def run_in_container(script_path: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Асинхронная обертка для запуска Docker-операций в отдельном потоке."""
    skill_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)

    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(
            _executor, _sync_run_container, script_name, skill_dir, parameters,
            DEFAULT_IMAGE, DEFAULT_MEM_LIMIT, DEFAULT_CPU_QUOTA, DEFAULT_TIMEOUT
        )
        return result
    except Exception as e:
        logger.exception("Исключение при запуске во внешнем потоке.")
        return {"status": "error", "message": str(e)}