FROM python:3.11-slim

LABEL maintainer="Nick Zhukoff <3327263@gmail.com>"
LABEL org.opencontainers.image.title="nz-lightrag"
LABEL org.opencontainers.image.description="RAG and Knowledge Graph API Server for Genesis Project"

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
