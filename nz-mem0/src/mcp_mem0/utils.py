# FILE: src/mcp_mem0/utils.py
import uuid
import time

def now_ts() -> int:
    return int(time.time())

def new_trace_id(prefix: str = "trace") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"
