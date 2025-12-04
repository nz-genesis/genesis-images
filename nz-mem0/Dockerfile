# ---------------------------------------------------------
# NZ-MEM0 — Genesis image (Maximum Space Saving)
# ---------------------------------------------------------
FROM python:3.11-slim

LABEL maintainer="genesis-team"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---------------------------------------------------------
# Build stage
# ---------------------------------------------------------
WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        git \
        libpq-dev \
        ca-certificates \
        curl \
        adduser \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /build/requirements.txt
COPY ./src /build/src

# Создаем wheels
RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip wheel --wheel-dir /build/wheels -r /build/requirements.txt

# ---------------------------------------------------------
# Runtime stage
# ---------------------------------------------------------
FROM python:3.11-slim as runtime

WORKDIR /app/src

# 1. Ставим системные зависимости (если нужны для runtime, например libpq)
# Для slim образа это часто не нужно, если wheels собраны правильно,
# но для надежности можно оставить минимальный набор.
# В данном случае попробуем без лишних apt-get в runtime, чтобы сэкономить место.

# 2. Ставим CPU-версию PyTorch ПЕРВОЙ
# Используем --no-cache-dir чтобы не хранить кэш
RUN python -m pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 3. Монтируем wheels из build-stage (НЕ КОПИРУЕМ!) и устанавливаем
# Это ключевой момент: файлы не занимают место на диске образа
RUN --mount=type=bind,from=0,source=/build/wheels,target=/wheels \
    python -m pip install --no-cache-dir /wheels/*.whl

COPY ./src /app/src
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

# Проверка и создание пользователя
RUN test -f /app/src/main.py || (echo "❌ ERROR: main.py not found in /app/src" && exit 1) \
    && addgroup --system app || true \
    && adduser --system --ingroup app --no-create-home app || true \
    && mkdir -p /var/log/nz-mem0 /data \
    && chown -R app:app /app /var/log/nz-mem0 /data

USER app

EXPOSE 8090

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
