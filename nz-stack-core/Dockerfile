# Registry-first recovery: ghcr.io/nz-genesis/nz-stack-core:latest
# Image digest: sha256:2ce64f59d677d5aa62bd7ad60ce5c0021dbac093da63bd1b291b685c24042cc7
# Recovered from GHCR on 2026-02-10

FROM python:3.11-slim

# Labels
LABEL org.opencontainers.image.title="nz-stack-core" \
      org.opencontainers.image.description="GENESIS Stack Core (Thinking Layer)" \
      maintainer="Nick Zhukoff"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    TZ=Europe/Kyiv

# Working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# Expose port
EXPOSE 8081

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8081/health',timeout=2) else sys.exit(1)"

# Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
