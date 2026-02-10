# FILE: src/mcp_mem0/tools/mem_delete.py
from typing import Dict, Any

def mem_delete(store, params: Dict[str, Any]):
    session_id = params.get("session_id")
    key = params.get("key")
    if not session_id or not key:
        raise ValueError("session_id and key are required")
    ok = store.delete(session_id=session_id, key=key)
    return {"status": "ok", "deleted": ok}
