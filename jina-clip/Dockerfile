# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Pre-download and convert Jina CLIP to ONNX quantized
RUN pip install --no-cache-dir \
    optimum[onnxruntime] \
    transformers \
    pillow \
    numpy

# Clone Jina CLIP and convert to ONNX
RUN git clone https://huggingface.co/jinaai/jina-clip-v2 /jina-model && \
    cd /jina-model && \
    python -c " \
from optimum.onnxruntime import ORTModelForFeatureExtraction; \
from transformers import AutoTokenizer; \
print('Converting Jina CLIP v2 to ONNX...'); \
model = ORTModelForFeatureExtraction.from_pretrained('jinaai/jina-clip-v2', export=True); \
model.save_pretrained('/models/jina-clip-v2-onnx'); \
tokenizer = AutoTokenizer.from_pretrained('jinaai/jina-clip-v2'); \
tokenizer.save_pretrained('/models/jina-clip-v2-onnx'); \
print('✅ ONNX model saved'); \
"

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install runtime dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy ONNX model from builder
COPY --from=builder /models/jina-clip-v2-onnx /app/models/jina-clip-v2-onnx

# Install Python dependencies (optimized for CPU)
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pillow==10.1.0 \
    numpy==1.24.3 \
    onnxruntime==1.17.0 \
    requests==2.31.0

# Copy server code
COPY server.py /app/server.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
