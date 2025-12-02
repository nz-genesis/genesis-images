"""
mcp_client: отправляет результаты выполнения в "Когнитивное Ядро" (n8n или MCP-шлюз).
MCP_URL задаётся в .env (например: http://192.168.31.203:5678/webhook/mcp-receiver).
"""
import os
import requests
import logging
from typing import Any, Dict

logger = logging.getLogger("nz-skill-runner.mcp_client")

MCP_URL = os.getenv("MCP_URL")
MCP_TIMEOUT = int(os.getenv("MCP_TIMEOUT", "10"))

def write_execution_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Отправляет результат выполнения Скилла для последующей обработки и сохранения в "Память"."""
    if not MCP_URL:
        logger.warning("MCP_URL не задан. Результат не будет отправлен в Когнитивное Ядро.")
        return {"status": "skipped", "reason": "MCP_URL not configured"}

    url = f"{MCP_URL.rstrip('/')}/executions"
    try:
        resp = requests.post(url, json=payload, timeout=MCP_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.exception("Не удалось отправить результат выполнения в MCP")
        return {"status": "error", "error": str(e)}