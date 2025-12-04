# ---------------------------------------------------------
# NZ-MEM0 — Genesis image (CPU-optimized)
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


RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip wheel --wheel-dir /build/wheels -r /build/requirements.txt


# ---------------------------------------------------------
# Runtime stage
# ---------------------------------------------------------
FROM python:3.11-slim as runtime


# --- ВАЖНО: рабочая директория для uvicorn должна быть /app/src ---
WORKDIR /app/src


COPY --from=0 /build/wheels /wheels

# ⚡ ПЕРВОЕ: Устанавливаем CPU-версию PyTorch ДО остальных зависимостей
# Это критично! Причина:
#   - sentence-transformers тянет torch как зависимость
#   - Без явного указания CPU-версии он потянет CUDA-версию (~5 ГБ)
#   - Это вызывает "No space left on device" на GitHub Actions (14 ГБ всего)
# Экономия: ~4-5 ГБ временных файлов при сборке
RUN python -m pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# ВТОРОЕ: Ставим все остальные зависимости из wheels
RUN python -m pip install --no-cache-dir /wheels/*.whl \
    && rm -rf /wheels


COPY ./src /app/src
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh


RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh


# Проверяем наличие main.py именно в правильной папке
RUN test -f /app/src/main.py || (echo "❌ ERROR: main.py not found in /app/src" && exit 1) \
    && addgroup --system app || true \
    && adduser --system --ingroup app --no-create-home app || true \
    && mkdir -p /var/log/nz-mem0 /data \
    && chown -R app:app /app /var/log/nz-mem0 /data


USER app


EXPOSE 8090


ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]

