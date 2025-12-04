# FILE: src/mcp_mem0/server.py
"""
MCPServer - internal manager that registers and invokes tools (mem_add, mem_search, mem_delete).
Exposes a simple Python API used by FastAPI endpoints and optionally by external MCP clients.
"""
from typing import Any, Dict
import logging
from .memory import MemoryStore
from .tools import mem_add, mem_search, mem_delete

logger = logging.getLogger("nz-mem0.mcp")

class MCPServer:
    def __init__(self, store: MemoryStore, settings=None):
        self.store = store
        self.settings = settings
        # registry of tools
        self.tools = {
            "mem0.add": mem_add,
            "mem0.search": mem_search,
            "mem0.delete": mem_delete,
        }

    def list_tools(self):
        return list(self.tools.keys())

    def invoke(self, tool_name: str, params: Dict[str, Any]):
        if tool_name not in self.tools:
            raise KeyError(f"tool not found: {tool_name}")
        fn = self.tools[tool_name]
        # tool functions accept store and params
        return fn(self.store, params)
