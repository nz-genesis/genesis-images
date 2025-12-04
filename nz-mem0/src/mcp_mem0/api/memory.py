# FILE: src/mcp_mem0/api/memory.py
from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

router = APIRouter()

class StoreReq(BaseModel):
    session_id: str
    key: str
    value: Dict[str, Any]
    ttl: Optional[int] = None
    embed: Optional[List[float]] = None
    trace_id: Optional[str] = None

class QueryReq(BaseModel):
    session_id: Optional[str] = None
    key: Optional[str] = None
    text_query: Optional[str] = None
    top_k: Optional[int] = 5

@router.post("/memory/store")
async def memory_store(req: StoreReq, request: Request):
    store = request.app.state.store
    try:
        rec_id = store.store(session_id=req.session_id, key=req.key, value=req.value, ttl=req.ttl, embed=req.embed, trace_id=req.trace_id)
        return {"status": "ok", "id": rec_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/get")
async def memory_get(session_id: str, key: str, request: Request):
    store = request.app.state.store
    res = store.get(session_id=session_id, key=key)
    if res is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"status": "ok", "result": res}

@router.post("/memory/search")
async def memory_search(q: QueryReq, request: Request):
    store = request.app.state.store
    res = store.search(session_id=q.session_id, key=q.key, text_query=q.text_query, top_k=q.top_k)
    return {"status": "ok", "results": res}

@router.get("/memory/recent")
async def memory_recent(session_id: str, limit: int = 20, request=...):
    store = request.app.state.store
    return {"status": "ok", "results": store.recent(session_id=session_id, limit=limit)}

@router.delete("/memory/delete")
async def memory_delete(session_id: str, key: str, request):
    store = request.app.state.store
    ok = store.delete(session_id=session_id, key=key)
    return {"status": "ok", "deleted": ok}
