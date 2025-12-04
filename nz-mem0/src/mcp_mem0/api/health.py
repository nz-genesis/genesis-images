# FILE: src/mcp_mem0/api/health.py
from fastapi import APIRouter
import os
from ..config import Settings

router = APIRouter()

@router.get("/health")
async def health():
    s = Settings()
    return {"status": "ok", "service": "nz-mem0", "tz": s.TZ}
