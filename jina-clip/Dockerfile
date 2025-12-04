# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Сразу скачиваем requirements, БЕЗ моделей
COPY requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt || true

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Минимальные runtime-зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Установим Python-пакеты (МИНИМАЛЬНО)
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pillow==10.1.0 \
    numpy==1.24.3 \
    torch==2.1.0 \
    transformers==4.36.0 \
    requests==2.31.0

# Копируем сервер
COPY server.py /app/server.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Моделям выделяем место в volume /data
ENV HF_HOME=/data/huggingface
ENV TORCH_HOME=/data/torch

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
