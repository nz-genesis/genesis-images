# nz-litellm - LiteLLM API wrapper for Genesis Project
# RECOVERED from published image: ghcr.io/nz-genesis/nz-litellm:latest
# Published: 2025-12-05
# Digest: sha256:378ef3706e0989e9a416f9e3bc4539ac5646f3cc0fcf125ca0d4c0e73072b8ab

FROM python:3.11-slim

LABEL maintainer="Nick Zhukoff <3327263@gmail.com>"
LABEL org.opencontainers.image.title="nz-litellm"
LABEL org.opencontainers.image.description="LLM API wrapper for Genesis Project"
LABEL org.opencontainers.image.source="https://github.com/nz-genesis/genesis-images"
LABEL org.opencontainers.image.created="2025-12-05T14:56:32.919757939Z"
LABEL org.opencontainers.image.revision="sha256:378ef3706e0989e9a416f9e3bc4539ac5646f3cc0fcf125ca0d4c0e73072b8ab"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
