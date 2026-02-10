# FILE: src/mcp_mem0/api/tools.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

class InvokeReq(BaseModel):
    tool: str
    params: Dict[str, Any]
    trace_id: Optional[str] = None

@router.get("/")
async def list_tools(request: Request):
    mcp = request.app.state.mcp
    return {"status": "ok", "tools": mcp.list_tools()}

@router.post("/invoke")
async def invoke_tool(req: InvokeReq, request: Request):
    mcp = request.app.state.mcp
    try:
        res = mcp.invoke(req.tool, {**req.params, "trace_id": req.trace_id})
        return {"status": "ok", "result": res}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
