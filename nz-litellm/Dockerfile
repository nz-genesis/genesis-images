FROM python:3.11-slim

WORKDIR /app

# Install LiteLLM proxy with all production dependencies
# - litellm[proxy]: LiteLLM proxy server with FastAPI
# - prisma: ORM for PostgreSQL database connection
# - python-dotenv: Load environment variables from .env files
RUN pip install --no-cache-dir 'litellm[proxy]' prisma python-dotenv

# Copy LiteLLM configuration file
COPY litellm_config.yaml .

# Expose API port
EXPOSE 8000

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start LiteLLM proxy server
CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]
