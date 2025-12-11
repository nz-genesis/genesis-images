FROM python:3.11-slim

WORKDIR /app

# Установить litellm с proxy dependencies
RUN pip install --no-cache-dir 'litellm[proxy]'

# Скопировать конфиг
COPY litellm_config.yaml .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start LiteLLM proxy
CMD ["litellm", "--host", "0.0.0.0", "--port", "8000"]
