FROM python:3.11-slim

WORKDIR /app

# 1. Install dependencies
RUN pip install --no-cache-dir 'litellm[proxy]' prisma python-dotenv

# 2. Generate Prisma Client binaries
# LiteLLM includes schema.prisma, we need to generate the client from it
RUN prisma generate --schema /usr/local/lib/python3.11/site-packages/litellm/proxy/schema.prisma

COPY litellm_config.yaml .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]
