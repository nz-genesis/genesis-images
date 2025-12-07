# nz-mem0 v0.1.0 - Working Memory Service

**Status:** ✅ Production Ready  
**Version:** 0.1.0  
**Last Updated:** 2025-12-07  

---

## 📖 Overview

**nz-mem0** is a working memory service for the nz-genesis platform. It provides:

- **Persistent memory storage** — Save and retrieve facts, context, and conversation history
- **Vector search** — Find relevant memories using semantic similarity
- **Multi-backend support** — SQLite for local, PostgreSQL for production, Qdrant for vectors
- **FastAPI REST API** — Simple HTTP endpoints for memory operations
- **Audit trail** — Track all memory operations with timestamps

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repo
git clone github.com/nz-genesis/genesis-images.git
cd genesis-images/nz-mem0

# 2. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Set environment variables
cp .env.example .env
# Edit .env with your values

# 4. Run locally
uvicorn src.main:app --reload --host 0.0.0.0 --port 8090

# 5. Test health
curl http://localhost:8090/health
# {"status":"ok","service":"nz-mem0","version":"0.1.0"}
```

### Docker Build

```bash
# Build image
docker build -t ghcr.io/nz-genesis/nz-mem0:0.1.0 .

# Expected size: ~270 MB
docker images ghcr.io/nz-genesis/nz-mem0:0.1.0

# Run container
docker run -d \
  -p 8090:8090 \
  -e MEM0_DATABASE_URL=postgresql://postgres:pass@localhost:5432/mem0 \
  -e MEM0_QDRANT_URL=http://localhost:6333 \
  ghcr.io/nz-genesis/nz-mem0:0.1.0

# Test
curl http://localhost:8090/health
```

---

## 📚 API Reference

### Health Check

```bash
GET /health
# Response: {"status":"ok","service":"nz-mem0","version":"0.1.0"}
```

### Store Memory

```bash
POST /memory/store
Content-Type: application/json

{
  "session_id": "user_123",
  "key": "conversation_context",
  "value": {
    "topic": "AI architecture",
    "sentiment": "positive"
  }
}

# Response: 200 OK
# {"id":"mem_xyz","session_id":"user_123","timestamp":"2025-12-07T10:00:00Z"}
```

### Retrieve Memory

```bash
GET /memory/retrieve?session_id=user_123&key=conversation_context

# Response: 200 OK
# {"value":{"topic":"AI architecture","sentiment":"positive"},"timestamp":"2025-12-07T10:00:00Z"}
```

### Search Memories

```bash
POST /memory/search
Content-Type: application/json

{
  "session_id": "user_123",
  "query": "What was discussed about architecture?",
  "limit": 5
}

# Response: 200 OK
# [
#   {"key":"conversation_context","score":0.95,"value":{...}},
#   {"key":"design_notes","score":0.87,"value":{...}}
# ]
```

### Delete Memory

```bash
DELETE /memory/delete?session_id=user_123&key=conversation_context

# Response: 200 OK
# {"deleted":true,"session_id":"user_123","key":"conversation_context"}
```

---

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────────┐
│         FastAPI Application                 │
│         (src/main.py)                       │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  API Routes (src/mcp_mem0/api/)      │  │
│  ├──────────────────────────────────────┤  │
│  │ • health.py   - /health endpoint     │  │
│  │ • memory.py   - /memory/* endpoints  │  │
│  │ • tools.py    - /tools endpoints     │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Memory Store (src/mcp_mem0/)        │  │
│  ├──────────────────────────────────────┤  │
│  │ • memory.py       - Core logic       │  │
│  │ • qdrant_store.py - Vector DB        │  │
│  │ • sqlite_store.py - Local storage    │  │
│  │ • embeddings.py   - Embeddings gen   │  │
│  │ • settings.py     - Configuration    │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
         ↓          ↓           ↓
     Postgres    Qdrant       Redis
    (Metadata)  (Vectors)    (Cache)
```

### Data Flow

1. **Store** → Settings + MemoryStore → SQL + Vector DB
2. **Retrieve** → SQL query → Return value
3. **Search** → Embeddings + Vector search → Rank results → Return

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Required | Notes |
|----------|---------|----------|-------|
| `HOST` | `0.0.0.0` | No | Server host |
| `PORT` | `8090` | No | Server port |
| `MEM0_DATABASE_URL` | None | Yes (prod) | PostgreSQL connection string |
| `MEM0_QDRANT_URL` | None | Yes (prod) | Qdrant server URL |
| `MEM0_QDRANT_API_KEY` | None | No | Qdrant API key (if required) |
| `MEM0_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | No | HuggingFace model ID |
| `API_KEY` | None | No | Optional API key for endpoints |
| `DEBUG` | `false` | No | Debug logging |

### Pydantic Settings

Configuration is managed via `src/mcp_mem0/settings.py` with Pydantic v2:

```python
from src.mcp_mem0.settings import Settings

settings = Settings()
# Access: settings.MEM0_DATABASE_URL, settings.PORT, etc.
```

---

## 🧪 Testing

### Unit Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src/mcp_mem0
```

### Integration Tests

```bash
# Start containers
docker-compose -f docker-compose.test.yml up -d

# Run tests
pytest tests/integration/ -v

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

### Manual Testing

```bash
# Health
curl http://localhost:8090/health

# Store
curl -X POST http://localhost:8090/memory/store \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","key":"test","value":{"data":"test"}}'

# Search
curl -X POST http://localhost:8090/memory/search \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","query":"test","limit":10}'
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.104.1 | Web framework |
| `uvicorn` | 0.24.0 | ASGI server |
| `pydantic` | 2.5.0 | Data validation |
| `sqlalchemy` | 2.0.23 | ORM |
| `psycopg2-binary` | 2.9.9 | PostgreSQL driver |
| `torch` | 2.1.2 | Embeddings (CPU) |
| `qdrant-client` | 1.7.0 | Vector DB client |
| `requests` | 2.31.0 | HTTP client |

---

## 🔒 Security

### Secrets Management

- ✅ No hardcoded credentials
- ✅ All secrets via environment variables
- ✅ Pydantic validates required settings
- ✅ `.env` file excluded from git (.gitignore)
- ✅ `.env.example` shows structure only

### API Security

- Optional API key validation (configure in `settings.py`)
- CORS configurable per deployment
- Input validation via Pydantic models
- SQL injection protection via SQLAlchemy ORM

---

## 🐛 Troubleshooting

### Health check timeout

```
Error: Health check endpoint timeout
```

**Solution:**
- Check container logs: `docker logs nz-mem0`
- Verify Postgres/Qdrant are running
- Check firewall/network connectivity

### Database connection error

```
Error: Could not connect to PostgreSQL
```

**Solution:**
```bash
# Check env var
echo $MEM0_DATABASE_URL

# Test connection
psql $MEM0_DATABASE_URL -c "SELECT 1"

# Verify credentials and host/port
```

### Vector search failing

```
Error: Failed to connect to Qdrant
```

**Solution:**
```bash
# Check Qdrant is running
curl http://qdrant:6333/health

# Verify URL in settings
echo $MEM0_QDRANT_URL

# Check collection exists
curl http://qdrant:6333/collections
```

### Out of memory during embeddings

```
Error: CUDA out of memory
```

**Solution:**
- CPU-only torch is installed (CUDA not needed)
- If still OOM, reduce batch size in settings
- Check available system memory: `free -h`

---

## 📈 Performance

### Metrics

- **Startup:** ~2-3 seconds
- **Health check:** <10ms
- **Store operation:** <100ms
- **Search operation:** <500ms (depending on collection size)

### Optimization

- Connection pooling enabled (SQLAlchemy)
- Vector indexing optimized (Qdrant HNSW)
- Batch operations supported
- Caching via Redis (optional)

---

## 🚀 Deployment

### Portainer (Recommended)

1. In Portainer, go to **Stacks**
2. Paste `docker-compose.prod.yml` or create stack
3. Set environment variables via Portainer Secrets
4. Deploy and monitor

### Manual Docker

```bash
docker run -d \
  --name nz-mem0 \
  -p 8090:8090 \
  -e MEM0_DATABASE_URL=postgresql://... \
  -e MEM0_QDRANT_URL=http://qdrant:6333 \
  ghcr.io/nz-genesis/nz-mem0:0.1.0
```

### Kubernetes

See `/deploy/k8s/nz-mem0-deployment.yaml` (if available)

---

## 📝 License

MIT License - See LICENSE file

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -am "feat: description"`
4. Push branch: `git push origin feature/name`
5. Submit pull request

---

**Need help?** Check [GitHub Issues](https://github.com/nz-genesis/genesis-images/issues) or contact the team.
