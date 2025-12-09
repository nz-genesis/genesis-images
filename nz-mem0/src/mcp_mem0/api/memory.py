# FILE: src/mcp_mem0/api/memory.py
from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

router = APIRouter()

class StoreReq(BaseModel):
    session_id: str
    key: str
    value: Dict[str, Any]
    # ✅ УБРАЛИ: ttl, embed, trace_id (MemoryStore их не поддерживает)

class QueryReq(BaseModel):
    session_id: Optional[str] = None
    key: Optional[str] = None
    text_query: Optional[str] = None
    top_k: Optional[int] = 5

@router.post("/memory/store")
async def memory_store(req: StoreReq, request: Request):
    store = request.app.state.store
    try:
        # ✅ ИСПРАВЛЕНО: убраны ttl, embed, trace_id
        rec_id = store.store(
            session_id=req.session_id,
            key=req.key,
            value=req.value
        )
        return {"status": "ok", "id": rec_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/get")
async def memory_get(session_id: str, key: str, request: Request):
    store = request.app.state.store
    try:
        res = store.get(session_id=session_id, key=key)
        if res is None:
            raise HTTPException(status_code=404, detail="not found")
        return {"status": "ok", "result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/memory/search")
async def memory_search(q: QueryReq, request: Request):
    store = request.app.state.store
    try:
        res = store.search(
            session_id=q.session_id,
            key=q.key,
            text_query=q.text_query,
            top_k=q.top_k
        )
        return {"status": "ok", "results": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/recent")
async def memory_recent(session_id: str, limit: int = 20, request: Request = ...):
    # ✅ ИСПРАВЛЕНО: добавлен type hint для request
    store = request.app.state.store
    try:
        results = store.recent(session_id=session_id, limit=limit)
        return {"status": "ok", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory/delete")
async def memory_delete(session_id: str, key: str, request: Request):
    # ✅ ИСПРАВЛЕНО: добавлен type hint для request
    store = request.app.state.store
    try:
        ok = store.delete(session_id=session_id, key=key)
        return {"status": "ok", "deleted": ok}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
