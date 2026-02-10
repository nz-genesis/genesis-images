# nz-litellm

## Build Model Confirmation

This image follows the genesis-images build model:
- **Build CI:** GitHub Actions only
- **Registry:** ghcr.io/nz-genesis/nz-litellm
- **Local builds:** For debugging only

## Recovery Status

- **Status:** ✅ RECOVERY_COMPLETE
- **Remediation:** lightrag dependency intentionally removed
- **Reason:** Known instability and incorrect previous assembly
- **Approval:** Human Final Authority (2026-02-10)
- **CI Run:** 21860377741 (SUCCESS)

## Remediation Status
- **Status**: REMEDIATED
- **Decision**: lightrag dependency intentionally removed
- **Reason**: Known instability and incorrect previous assembly
- **Approval**: Human Final Authority (2026-02-10)

**Status:** FIXED (lightrag dependency removed)  
**Published:** 2025-12-05  
**Image:** `ghcr.io/nz-genesis/nz-litellm:latest`  
**Digest:** `sha256:378ef3706e0989e9a416f9e3bc4539ac5646f3cc0fcf125ca0d4c0e73072b8ab`  
**Size:** 515 MB  

## Purpose

LiteLLM API wrapper for Genesis Project.

## Scope

### Does Include

- LiteLLM proxy service
- FastAPI-based API endpoints
- Health check endpoint (`/health`)
- OpenAI-compatible chat completions (`/v1/chat/completions`)

### Does NOT Include

- ❌ RAG components (out of scope for this service)
- ❌ Qdrant vector database drivers
- ❌ PostgreSQL database drivers

## Important Notes

ℹ️ **LiteLLM-only Service:** This is a lightweight proxy that forwards LLM requests to a LiteLLM backend.

No RAG or vector database functionality is included.

## Canonical References

- **Registry:** `ghcr.io/nz-genesis/nz-litellm`
- **Base Image:** `python:3.11-slim`
- **Entrypoint:** `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Exposed Port:** `8000`
- **Health Check:** `curl -f http://127.0.0.1:8000/health`

## Usage

```bash
# Pull image
docker pull ghcr.io/nz-genesis/nz-litellm:latest

# Run with environment
docker run -p 8000:8000 \
  -e LITELLM_API_URL=http://litellm:4000 \
  ghcr.io/nz-genesis/nz-litellm:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LITELLM_API_URL` | Yes | `http://localhost:4000` | LiteLLM proxy URL |
| `LOG_LEVEL` | No | `INFO` | Logging level |

---

*README is documentation only. See registry for canonical image specification.*
