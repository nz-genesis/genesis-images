FROM python:3.11-slim

WORKDIR /app

# 1. Install dependencies (Node.js НЕ нужен - LiteLLM includes pre-built Prisma Client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
RUN pip install --no-cache-dir 'litellm[proxy]' python-dotenv

COPY litellm_config.yaml .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]