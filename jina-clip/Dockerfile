# Simplified: use pre-built ONNX model if available, or basic FastAPI setup
FROM python:3.11-slim

LABEL maintainer="Nick Zhukoff <3327263@gmail.com>"
LABEL org.opencontainers.image.title="jina-clip"
LABEL org.opencontainers.image.description="Jina CLIP embedding service for Genesis"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pillow==10.1.0 \
    numpy==1.24.3 \
    onnxruntime==1.17.0 \
    requests==2.31.0 \
    jina[all]>=0.1.0

# Copy server code
COPY server.py /app/server.py

# Create models directory
RUN mkdir -p /app/models

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
