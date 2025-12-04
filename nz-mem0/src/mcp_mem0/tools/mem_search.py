# FILE: src/mcp_mem0/tools/mem_search.py
from typing import Dict, Any

def mem_search(store, params: Dict[str, Any]):
    session_id = params.get("session_id")
    key = params.get("key")
    text_query = params.get("text_query")
    top_k = params.get("top_k", 5)
    results = store.search(session_id=session_id, key=key, text_query=text_query, top_k=top_k)
    return {"status": "ok", "results": results}
