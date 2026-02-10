# nz-mem0 - Working Memory Service for Genesis Project
# RECOVERED from forensic analysis of published image: ghcr.io/nz-genesis/nz-mem0:latest
# Published: 2025-12-09
# Version: 0.1.0
# Size: 7.9 GB (overly large due to CUDA dependencies)
# Status: NEEDS_FIX - see README.md for issues

FROM python:3.11-slim

LABEL maintainer="Nick Zhukoff <3327263@gmail.com>"
LABEL org.opencontainers.image.title="nz-mem0"
LABEL org.opencontainers.image.description="Working Memory Service for Genesis Project - FastAPI + SQLAlchemy + Qdrant"
LABEL org.opencontainers.image.source="https://github.com/nz-genesis/genesis-images"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.created="2025-12-09T00:00:00.000000000Z"

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        curl \
        libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA (NOTE: This causes 7.9 GB image size)
# For smaller image, use CPU-only version: --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir \
    torch==2.1.2 \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu118

# Copy requirements first for better layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD curl -f http://127.0.0.1:8090/health || exit 1

# Use entrypoint script for proper initialization
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8090"]
