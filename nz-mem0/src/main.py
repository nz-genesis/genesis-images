"""
Main FastAPI application for nz-mem0.
Creates MemoryStore from settings and exposes minimal API for health + memory operations.
"""

import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional

from mcp_mem0.memory import MemoryStore
from mcp_mem0.settings import get_settings  # NOTE: you've provided settings.py; adjust import path if different

# configure basic logging
logger = logging.getLogger("nz-mem0")
logger.setLevel("INFO")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logger.addHandler(handler)

app = FastAPI(title="nz-mem0", version="0.1.0")

# create settings and store on startup
@app.on_event("startup")
async def startup_event():
    logger.info("nz-mem0 startup — initializing backends")
    settings = get_settings()
    # attach settings and store to app.state for handlers
    app.state.settings = settings
    try:
        app.state.store = MemoryStore(settings=settings)
    except Exception as exc:
        logger.exception("MemoryStore initialization failed")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("nz-mem0 shutdown — cleaning up")
    store = getattr(app.state, "store", None)
    if store:
        # place for graceful teardown (if needed)
        pass

# --------------------
# Health
# --------------------
@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})

# --------------------
# Memory endpoints
# --------------------
@app.post("/memory/add")
def add_memory(payload: Dict[str, Any]):
    """
    Body: { "text": "...", "metadata": {...} }
    """
    store: MemoryStore = app.state.store
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="text required")
    metadata = payload.get("metadata")
    out = store.add(text=text, metadata=metadata)
    return out

@app.get("/memory/get/{item_id}")
def get_memory(item_id: int):
    store: MemoryStore = app.state.store
    item = store.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.post("/memory/search")
def search_memory(payload: Dict[str, Any]):
    """
    Body: { "query": "...", "limit": 5 }
    """
    store: MemoryStore = app.state.store
    q = payload.get("query")
    if not q:
        raise HTTPException(status_code=400, detail="query required")
    limit = int(payload.get("limit", 5))
    results = store.search(query=q, limit=limit)
    return {"results": results}

# simple listing endpoint (for debug)
@app.get("/memory/list")
def list_memory(limit: Optional[int] = 50):
    store: MemoryStore = app.state.store
    return {"items": store.sql_store.get_last(limit=limit)}
