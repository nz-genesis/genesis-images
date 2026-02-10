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
    tools = mcp.get("tools", {})
    return {"status": "ok", "tools": list(tools.keys())}

@router.post("/invoke")
async def invoke_tool(req: InvokeReq, request: Request):
    mcp = request.app.state.mcp
    tools = mcp.get("tools", {})
    try:
        tool_func = tools.get(req.tool)
        if tool_func is None:
            raise KeyError(f"Tool '{req.tool}' not found")
        res = tool_func(request.app.state.store, {**req.params, "trace_id": req.trace_id})
        return {"status": "ok", "result": res}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
