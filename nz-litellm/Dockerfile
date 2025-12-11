FROM python:3.11

WORKDIR /app

# 1. Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies (INCLUDING prisma package)
RUN pip install --no-cache-dir \
    'litellm[proxy]' \
    prisma \
    python-dotenv

# 3. Find and copy schema.prisma from installed litellm package
RUN python -c "import site; import os; \
    pkg_path = os.path.join(site.getsitepackages()[0], 'litellm'); \
    schema = os.path.join(pkg_path, 'proxy', 'schema.prisma'); \
    os.system(f'cp {schema} /app/schema.prisma')"

# 4. Generate Prisma client using the copied schema
RUN python -m prisma generate --schema /app/schema.prisma

COPY litellm_config.yaml .

EXPOSE 8000

# HEALTHCHECK: проверка TCP соединения к 8000 порту, без /health и без API key
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('127.0.0.1', 8000), timeout=5)" || exit 1

CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]
