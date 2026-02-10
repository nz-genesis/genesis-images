"""
nz-mem0 FastAPI Application Entry Point
Version: 0.1.0
"""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.mcp_mem0.settings import Settings
from src.mcp_mem0.api import health, memory, tools
from src.mcp_mem0.memory import MemoryStore  # ✅ ДОБАВЛЕНО


# Initialize settings
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup ✅ ДОБАВЛЕНО: Инициализация state
    print("🚀 Starting nz-mem0 v0.1.0...")
    print(f"📡 Database: {settings.MEM0_DATABASE_URL[:50]}...")
    print(f"🔍 Qdrant: {settings.MEM0_QDRANT_URL}")
    
    try:
        # Initialize MemoryStore ✅ КРИТИЧНО
        print("🔧 Initializing MemoryStore...")
        app.state.store = MemoryStore()
        print("✅ MemoryStore initialized successfully")
        
        # Initialize MCP state
        print("🔧 Initializing MCP...")
        app.state.mcp = {
            "tools": {},
            "config": {},
        }
        print("✅ MCP initialized successfully")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down nz-mem0...")
    try:
        if hasattr(app.state, 'store') and app.state.store:
            # Cleanup если нужно
            pass
    except Exception as e:
        print(f"⚠️ Error during shutdown: {e}")


# Create FastAPI app
app = FastAPI(
    title="nz-mem0",
    description="Working Memory Service for nz-genesis",
    version="0.1.0",
    lifespan=lifespan,
)


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "ok",
        "service": "nz-mem0",
        "version": "0.1.0",
    }


# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(memory.router, prefix="/memory", tags=["memory"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    """
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else None,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
    )
