# syntax=docker/dockerfile:1.7

# ============================================================================
# nz-mem0 v0.1.0 - Production-Ready Multi-Stage Dockerfile
# ============================================================================
# Author: Nick Zhukoff
# Purpose: FastAPI service for NZ-Genesis L2 Working Memory
# Build: docker build -t nz-mem0:0.1.0 .
# Run: docker run -p 8090:8090 nz-mem0:0.1.0
# ============================================================================

FROM python:3.11-slim as builder

WORKDIR /build

COPY requirements.txt .

# Install build dependencies and create wheels (WITHOUT --no-deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ============================================================================
# RUNTIME STAGE
# ============================================================================

FROM python:3.11-slim

LABEL maintainer="Nick Zhukoff"
LABEL version="0.1.0"
LABEL description="nz-mem0: NZ-Genesis L2 Working Memory Service"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /build/wheels /tmp/wheels
RUN pip install --no-cache-dir --no-index /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

# Copy application
COPY src /app/src
COPY .env.example /app/.env.example
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create data directory
RUN mkdir -p /data && chmod 755 /data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8090/health || exit 1

EXPOSE 8090
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "-m", "src.main"]
