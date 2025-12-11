FROM python:3.11-slim

WORKDIR /app

# 1. Install build dependencies & Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies (ИСКЛЮЧАЕМ prisma Python package)
RUN pip install --no-cache-dir 'litellm[proxy]' python-dotenv

# 3. Generate Prisma Client using npx (Node.js native, NO Python wrapper)
RUN npx prisma@5 generate --schema /usr/local/lib/python3.11/site-packages/litellm/proxy/schema.prisma

COPY litellm_config.yaml .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]