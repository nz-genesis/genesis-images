# FILE: src/mcp_mem0/tools/mem_search.py
"""
Tool: mem0.search
Params:
  session_id (str), query (str), limit (optional int)
"""
from typing import Dict, Any

def mem_search(store, params: Dict[str, Any]):
    session_id = params.get("session_id")
    query = params.get("query") or params.get("text_query")
    limit = params.get("limit", params.get("top_k", 5))
    if not session_id or not query:
        raise ValueError("session_id and query are required")
    results = store.search(session_id=session_id, query=query, limit=limit)
    return {"status": "ok", "results": results}
