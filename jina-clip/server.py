#!/usr/bin/env python3
"""
Jina CLIP v2 FastAPI Server
- Multilingual multimodal embeddings
- Text & image embedding support
- Lazy model loading
- CPU-optimized for Intel N100
- Async endpoints with health checks
"""

import os
import logging
from typing import Optional, List
from pathlib import Path
from datetime import datetime
import time
import io

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import requests
from pydantic import BaseModel

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

HF_HOME = Path(os.getenv("HF_HOME", "/data/huggingface"))
MODEL_NAME = "jinaai/jina-clip-v2"
BATCH_SIZE = 4
MAX_IMAGE_SIZE = (512, 512)
EMBEDDING_DIM = 1024
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TextRequest(BaseModel):
    text: str
    truncate_dim: Optional[int] = None

class ImageRequest(BaseModel):
    image_url: str
    truncate_dim: Optional[int] = None

class BatchTextRequest(BaseModel):
    texts: List[str]
    task: Optional[str] = "text-image"
    truncate_dim: Optional[int] = None

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dim: int
    model: str
    latency_ms: float

class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dim: int
    count: int
    model: str
    latency_ms: float

# ============================================================================
# APP SETUP
# ============================================================================

app = FastAPI(
    title="Jina CLIP v2 Server",
    version="1.0.0",
    description="Multilingual multimodal embeddings API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# GLOBAL STATE
# ============================================================================

class ModelState:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.loaded = False
        self.load_time = None
        self.error = None

state = ModelState()

class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.total_embeddings = 0
        self.total_errors = 0
        self.start_time = datetime.now()
        self.request_times = []

    def record(self, latency_ms: float):
        self.total_requests += 1
        self.request_times.append(latency_ms)
        if len(self.request_times) > 1000:
            self.request_times = self.request_times[-1000:]

    @property
    def avg_latency_ms(self) -> float:
        return sum(self.request_times) / len(self.request_times) if self.request_times else 0.0

    @property
    def uptime_seconds(self) -> int:
        return int((datetime.now() - state.start_time).total_seconds())

metrics = Metrics()

# ============================================================================
# MODEL LOADING
# ============================================================================

async def load_model():
    """Load Jina CLIP v2 model lazily on first request"""
    global state
    
    if state.loaded:
        return
    
    logger.info("🔄 Loading Jina CLIP v2 (first request, 30-60s)...")
    start = time.time()
    
    try:
        # Set Hugging Face cache
        os.environ["HF_HOME"] = str(HF_HOME)
        
        logger.info("📖 Loading model and tokenizer...")
        state.model = AutoModel.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            device_map="cpu"
        )
        state.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        )
        
        state.loaded = True
        state.load_time = time.time() - start
        logger.info(f"✅ Model loaded in {state.load_time:.2f}s")
        
    except Exception as e:
        state.error = str(e)
        logger.error(f"❌ Failed to load model: {e}")
        raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/embed/text", response_model=EmbeddingResponse)
async def embed_text(request: TextRequest):
    """Embed a single text"""
    start = time.time()
    
    try:
        if not state.loaded:
            await load_model()
        
        embeddings = state.model.encode_text([request.text])
        
        if request.truncate_dim and request.truncate_dim < EMBEDDING_DIM:
            embeddings = embeddings[:, :request.truncate_dim]
        
        latency = (time.time() - start) * 1000
        metrics.record(latency)
        metrics.total_embeddings += 1
        
        return EmbeddingResponse(
            embedding=embeddings[0].tolist(),
            dim=embeddings.shape[1],
            model=MODEL_NAME,
            latency_ms=latency
        )
    
    except Exception as e:
        metrics.total_errors += 1
        logger.error(f"Text embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed/image", response_model=EmbeddingResponse)
async def embed_image(request: ImageRequest):
    """Embed image from URL"""
    start = time.time()
    
    try:
        if not state.loaded:
            await load_model()
        
        # Download image
        response = requests.get(request.image_url, timeout=10)
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
        image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        embeddings = state.model.encode_image([image])
        
        if request.truncate_dim and request.truncate_dim < EMBEDDING_DIM:
            embeddings = embeddings[:, :request.truncate_dim]
        
        latency = (time.time() - start) * 1000
        metrics.record(latency)
        metrics.total_embeddings += 1
        
        return EmbeddingResponse(
            embedding=embeddings[0].tolist(),
            dim=embeddings.shape[1],
            model=MODEL_NAME,
            latency_ms=latency
        )
    
    except Exception as e:
        metrics.total_errors += 1
        logger.error(f"Image embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed/batch", response_model=BatchEmbeddingResponse)
async def embed_batch(request: BatchTextRequest):
    """Batch embed multiple texts"""
    start = time.time()
    
    try:
        if not state.loaded:
            await load_model()
        
        embeddings = state.model.encode_text(request.texts)
        
        if request.truncate_dim and request.truncate_dim < EMBEDDING_DIM:
            embeddings = embeddings[:, :request.truncate_dim]
        
        latency = (time.time() - start) * 1000
        metrics.record(latency)
        metrics.total_embeddings += len(request.texts)
        
        return BatchEmbeddingResponse(
            embeddings=[e.tolist() for e in embeddings],
            dim=embeddings.shape[1],
            count=len(request.texts),
            model=MODEL_NAME,
            latency_ms=latency
        )
    
    except Exception as e:
        metrics.total_errors += 1
        logger.error(f"Batch embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed/image/upload", response_model=EmbeddingResponse)
async def embed_image_upload(file: UploadFile = File(...)):
    """Embed uploaded image file"""
    start = time.time()
    
    try:
        if not state.loaded:
            await load_model()
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        embeddings = state.model.encode_image([image])
        
        latency = (time.time() - start) * 1000
        metrics.record(latency)
        metrics.total_embeddings += 1
        
        return EmbeddingResponse(
            embedding=embeddings[0].tolist(),
            dim=embeddings.shape[1],
            model=MODEL_NAME,
            latency_ms=latency
        )
    
    except Exception as e:
        metrics.total_errors += 1
        logger.error(f"Image upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HEALTH & MONITORING
# ============================================================================

@app.get("/health")
async def health():
    """Health check for Docker/Portainer"""
    if state.error:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": state.error,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    return {
        "status": "healthy",
        "model_loaded": state.loaded,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics"""
    return {
        "total_requests": metrics.total_requests,
        "total_embeddings": metrics.total_embeddings,
        "total_errors": metrics.total_errors,
        "avg_latency_ms": metrics.avg_latency_ms,
        "uptime_seconds": metrics.uptime_seconds,
        "model_loaded": state.loaded,
    }

@app.get("/info")
async def info():
    """Server information"""
    return {
        "name": "Jina CLIP v2 Server",
        "version": "1.0.0",
        "model": MODEL_NAME,
        "embedding_dim": EMBEDDING_DIM,
        "max_image_size": MAX_IMAGE_SIZE,
    }

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    logger.info("🚀 Jina CLIP v2 Server starting...")
    logger.info(f"📦 HF_HOME: {HF_HOME}")
    logger.info(f"🔌 Listening on {HOST}:{PORT}")

@app.on_event("shutdown")
async def shutdown():
    logger.info("🛑 Server shutting down...")
    logger.info(f"📊 Total requests: {metrics.total_requests}")
    logger.info(f"❌ Total errors: {metrics.total_errors}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        workers=1,
        log_level="info"
    )