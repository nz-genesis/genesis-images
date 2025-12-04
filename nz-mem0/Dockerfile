# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Установим build-tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

# Сначала ставим torch CPU явно!
# Это предотвращает скачивание CUDA версий зависимостями
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Потом всё остальное, но говорим pip'у не обновлять torch
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir /build/wheels -r requirements.txt \
    --find-links https://download.pytorch.org/whl/cpu

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app/src

# Минимальные системные библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка из wheels (Mount bind)
RUN --mount=type=bind,from=builder,source=/build/wheels,target=/wheels \
    pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl

COPY ./src /app/src
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    addgroup --system app && \
    adduser --system --ingroup app app && \
    mkdir -p /var/log/nz-mem0 /data && \
    chown -R app:app /app /var/log/nz-mem0 /data

USER app
EXPOSE 8090
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
