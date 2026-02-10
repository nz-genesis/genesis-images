# FILE: src/mcp_mem0/tools/mem_add.py
"""
Tool: mem0.add
Params:
  session_id (str), key (str), value (dict), ttl (optional int), embed (optional list[float])
"""
from typing import Dict, Any

def mem_add(store, params: Dict[str, Any]):
    session_id = params.get("session_id")
    key = params.get("key")
    value = params.get("value")
    ttl = params.get("ttl")
    embed = params.get("embed")
    trace_id = params.get("trace_id", None)
    if not session_id or not key or value is None:
        raise ValueError("session_id, key and value are required")
    rec_id = store.store(session_id=session_id, key=key, value=value, ttl=ttl, embed=embed, trace_id=trace_id)
    return {"status": "ok", "id": rec_id}
