# FILE: src/mcp_mem0/audit.py
import logging
from .utils import now_ts, new_trace_id

logger = logging.getLogger("nz-mem0.audit")

class AuditLogger:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def log(self, action: str, payload: dict, trace_id: str | None = None):
        if not self.enabled:
            return
        if trace_id is None:
            trace_id = new_trace_id("audit")
        rec = {"trace_id": trace_id, "action": action, "payload": payload, "ts": now_ts()}
        # for now, simple structured log; in prod you can push to Postgres/MinIO
        logger.info("AUDIT %s", rec)
        return rec
