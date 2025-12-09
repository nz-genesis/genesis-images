# FILE: src/mcp_mem0/api/memory.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

router = APIRouter()

class StoreReq(BaseModel):
    session_id: str
    key: str
    value: Dict[str, Any]

class QueryReq(BaseModel):
    session_id: Optional[str] = None
    text_query: Optional[str] = None
    top_k: Optional[int] = 5

@router.post("/memory/store")
async def memory_store(req: StoreReq, request: Request):
    """Store a memory record."""
    store = request.app.state.store
    try:
        result = store.store(
            session_id=req.session_id,
            key=req.key,
            value=req.value
        )
        return {"status": "ok", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/get")
async def memory_get(session_id: str, key: str, request: Request):
    """Retrieve a memory record by session_id and key."""
    store = request.app.state.store
    try:
        # ✅ ИСПРАВЛЕНО: get → retrieve
        res = store.retrieve(session_id=session_id, key=key)
        if res is None:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "result": res}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/memory/search")
async def memory_search(q: QueryReq, request: Request):
    """Search memories using vector similarity."""
    store = request.app.state.store
    try:
        # ✅ ИСПРАВЛЕНО: убран параметр key, переименован text_query → query
        if not q.text_query:
            raise HTTPException(status_code=400, detail="text_query is required")
        
        res = store.search(
            session_id=q.session_id or "",
            query=q.text_query,
            limit=q.top_k or 5
        )
        return {"status": "ok", "results": res}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/recent")
async def memory_recent(session_id: str, limit: int = 20, request: Request = ...):
    """Get recent memories for a session."""
    store = request.app.state.store
    try:
        # ✅ ДОБАВЛЕНО: реализация через SQL запрос
        # Temporary implementation using retrieve pattern
        # TODO: Add native recent() method to MemoryStore
        
        from sqlalchemy import select, desc
        from src.mcp_mem0.memory import MemoryRecord
        import json
        
        session_db = store.SessionLocal()
        try:
            stmt = (
                select(MemoryRecord)
                .where(MemoryRecord.session_id == session_id)
                .order_by(desc(MemoryRecord.updated_at))
                .limit(limit)
            )
            records = session_db.execute(stmt).scalars().all()
            
            results = [
                {
                    "key": r.key,
                    "value": json.loads(r.value),
                    "timestamp": r.updated_at,
                }
                for r in records
            ]
            
            return {"status": "ok", "results": results}
        finally:
            session_db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory/delete")
async def memory_delete(session_id: str, key: str, request: Request):
    """Delete a memory record."""
    store = request.app.state.store
    try:
        # ✅ delete уже правильное имя метода
        ok = store.delete(session_id=session_id, key=key)
        if not ok:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "deleted": ok}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
