# nz-mem0 — Forensic Analysis Report

| Field | Value |
|---|---|
| **Image** | `ghcr.io/nz-genesis/nz-mem0:latest` |
| **Version** | 0.1.0 |
| **Size** | 7.9 GB (7,933,522,071 bytes) |
| **Last Published** | 2025-12-09 |
| **Status** | **NEEDS_FIX** |
| **Remediation Required** | **Y** |
| **Analysis Date** | 2026-02-10 |

---

## 1. Overview

nz-mem0 — Working Memory Service для nz-genesis. FastAPI-приложение с SQLAlchemy (PostgreSQL/SQLite) + Qdrant (vector search) + embeddings.

**Базовый запуск работает**: smoke tests проходят, `/health` endpoint отвечает 200 OK. Однако при реальном использовании (store/search/tools) обнаружены множественные проблемы совместимости интерфейсов.

---

## 2. Architecture

```
entrypoint.sh → uvicorn → src.main:app (FastAPI)
├── /health          → api/health.py (uses config.Settings)
├── /memory/*        → api/memory.py (uses app.state.store = MemoryStore)
│   ├── POST /memory/store
│   ├── GET  /memory/get
│   ├── POST /memory/search
│   ├── GET  /memory/recent
│   └── DELETE /memory/delete
├── /tools/*         → api/tools.py (uses app.state.mcp)
│   ├── GET  /tools/
│   └── POST /tools/invoke
└── Core:
    ├── memory.py       → MemoryStore (SQLAlchemy + QdrantStore + EmbeddingBackend)
    ├── qdrant_store.py → QdrantStore (qdrant-client wrapper)
    ├── embeddings.py   → EmbeddingBackend (sentence-transformers / sha256 fallback)
    ├── sqlite_store.py → SQLiteStore (alternative lightweight store, unused)
    ├── settings.py     → Settings (pydantic-settings, used by main/memory)
    ├── config.py       → Settings (pydantic-settings, used by api/health) ← DUPLICATE
    ├── audit.py        → AuditLogger
    └── tools/          → mem_add, mem_search, mem_delete (MCP tool wrappers)
```

---

## 3. Dependencies (installed in image)

| Package | Version | Notes |
|---|---|---|
| fastapi | 0.104.1 | ✅ |
| uvicorn | 0.24.0 | ✅ |
| pydantic | 2.5.0 | ✅ |
| pydantic-settings | 2.1.0 | ✅ |
| SQLAlchemy | 2.0.23 | ✅ |
| psycopg2-binary | 2.9.9 | ✅ (PostgreSQL driver) |
| qdrant-client | 1.7.0 | ✅ |
| numpy | 1.24.3 | ✅ |
| torch | 2.1.2 | ⚠️ 5+ GB, причина огромного размера образа |
| sentence-transformers | — | ❌ **НЕ УСТАНОВЛЕН** (fallback на sha256 хеш) |
| nvidia-* (CUDA) | various | ⚠️ ~2 GB CUDA libs, бесполезны без GPU |

### Критическое замечание по размеру

Образ 7.9 GB из-за:
- `torch` (2.1.2) с CUDA: ~5 GB
- `nvidia-*` CUDA библиотеки: ~2 GB
- `sentence-transformers` **не установлен** — torch установлен зря

---

## 4. Import Test Results

| Module | Status |
|---|---|
| `src.main.app` | ✅ OK |
| `src.mcp_mem0.settings.Settings` | ✅ OK |
| `src.mcp_mem0.memory.MemoryStore` | ✅ OK |
| `src.mcp_mem0.embeddings.EmbeddingBackend` | ✅ OK |
| `src.mcp_mem0.qdrant_store.QdrantStore` | ✅ OK |
| `src.mcp_mem0.config.Settings` | ✅ OK |
| `src.mcp_mem0.api.health` | ✅ OK |
| `sentence_transformers` | ❌ NOT INSTALLED |

---

## 5. Runtime Test

```
✅ Smoke tests passed (entrypoint.sh)
✅ Uvicorn starts on 0.0.0.0:8090
✅ /health returns 200 OK
✅ MemoryStore initializes (SQLite fallback)
⚠️ Qdrant connection fails silently (no Qdrant server)
⚠️ Embeddings use sha256 fallback (no sentence-transformers)
```

---

## 6. Issues Found

### CRITICAL (блокируют функциональность)

#### C1: `api/health.py` — AttributeError на `Settings.TZ`
- **Файл**: `src/mcp_mem0/api/health.py:11`
- **Проблема**: `return {"status": "ok", "service": "nz-mem0", "tz": s.TZ}` — `config.Settings` не имеет поля `TZ`
- **Эффект**: GET `/health/health` вернёт 500 (дублирует корневой `/health` из main.py который работает)
- **Severity**: MEDIUM (основной health check в main.py работает)

#### C2: `api/tools.py` — TypeError на dict
- **Файл**: `src/mcp_mem0/api/tools.py:16`
- **Проблема**: `mcp.list_tools()` и `mcp.invoke()` вызываются на `app.state.mcp` который является `dict`, а не объектом с методами
- **Эффект**: GET `/tools/` и POST `/tools/invoke` вернут 500
- **Severity**: HIGH (tools API полностью нерабочий)

#### C3: `tools/mem_add.py` — signature mismatch
- **Файл**: `src/mcp_mem0/tools/mem_add.py:18`
- **Проблема**: Передаёт `ttl`, `embed`, `trace_id` в `store.store()` который принимает только `session_id`, `key`, `value`
- **Эффект**: TypeError при вызове mem_add tool
- **Severity**: HIGH

#### C4: `tools/mem_search.py` — signature mismatch
- **Файл**: `src/mcp_mem0/tools/mem_search.py:9`
- **Проблема**: Передаёт `key`, `text_query`, `top_k` в `store.search()` который принимает `session_id`, `query`, `limit`
- **Эффект**: TypeError при вызове mem_search tool
- **Severity**: HIGH

#### C5: `qdrant_store.search_vector` — missing payload in results
- **Файл**: `src/mcp_mem0/qdrant_store.py:56`
- **Проблема**: Возвращает `{"id": ..., "score": ...}` без `payload`, но `memory.search()` ожидает `result.get("payload", {})`
- **Эффект**: Vector search не вернёт полезных результатов (пустые payload → пустые enriched_results)
- **Severity**: HIGH

### MODERATE (влияют на качество/стабильность)

#### M1: Дублирование Settings
- **Файлы**: `settings.py` vs `config.py`
- **Проблема**: Два разных класса Settings с разными полями и env_prefix. `settings.py` используется в main/memory, `config.py` — в api/health
- **Эффект**: Путаница конфигурации, разное поведение

#### M2: Global `MemoryStore()` at import time
- **Файл**: `src/mcp_mem0/memory.py:336`
- **Проблема**: `memory_store = MemoryStore()` создаётся при импорте модуля, инициируя подключение к БД
- **Эффект**: Двойная инициализация (global + lifespan), потенциальные ошибки при отсутствии БД

#### M3: SQLite с pool_size/max_overflow
- **Файл**: `src/mcp_mem0/memory.py:53-55`
- **Проблема**: `create_engine(sqlite_url, pool_size=10, max_overflow=20)` — SQLite не поддерживает connection pooling
- **Эффект**: Warning от SQLAlchemy

#### M4: `sentence-transformers` не установлен
- **Проблема**: torch (5 GB) установлен, но sentence-transformers — нет. Embeddings используют sha256 fallback
- **Эффект**: Семантический поиск не работает (детерминистические хеши вместо реальных embeddings)

### LOW (не блокируют, но требуют внимания)

#### L1: Образ 7.9 GB — чрезмерный размер
- torch + CUDA libs занимают ~7 GB, при этом sentence-transformers не установлен
- Без GPU CUDA бесполезен
- Можно уменьшить до ~500 MB используя CPU-only torch или убрав torch целиком

#### L2: `sqlite_store.py` — неиспользуемый модуль
- Альтернативная реализация хранилища, не подключена ни к одному роутеру

#### L3: `api/__init__.py` отсутствует
- Может вызвать проблемы с импортами в некоторых конфигурациях (но работает в текущем образе)

---

## 7. Severity Summary

| Severity | Count | Details |
|---|---|---|
| CRITICAL/HIGH | 5 | C1-C5: tools API broken, signature mismatches, missing payload |
| MODERATE | 4 | M1-M4: duplicate settings, global init, SQLite pooling, missing embeddings |
| LOW | 3 | L1-L3: image size, dead code, missing __init__ |
| **TOTAL** | **12** | |

---

## 8. Diagnosis

### Наиболее вероятные источники проблем:

1. **Несогласованность интерфейсов между слоями** — tools/ и api/ написаны под один API MemoryStore, а сам MemoryStore был рефакторен (видны комментарии `✅ ИСПРАВЛЕНО`). Рефакторинг memory.py не был синхронизирован с tools/.

2. **Два конкурирующих Settings класса** — `settings.py` (старый, с os.getenv) и `config.py` (новый, с pydantic v2 SettingsConfigDict). Миграция не завершена.

### Корневая причина:
Образ собран в процессе активной разработки. Часть модулей была обновлена (memory.py, qdrant_store.py, api/memory.py), а часть осталась в старом состоянии (tools/, api/health.py, api/tools.py).

---

## 9. Remediation Plan (PENDING APPROVAL)

### Phase 1: Critical fixes (tools API)
1. Fix `api/health.py` — убрать `s.TZ`, использовать `settings.py` Settings
2. Fix `api/tools.py` — реализовать MCP registry object или отключить endpoint
3. Fix `tools/mem_add.py` — привести сигнатуру к `store.store(session_id, key, value)`
4. Fix `tools/mem_search.py` — привести к `store.search(session_id, query, limit)`
5. Fix `qdrant_store.search_vector` — включить `payload` в результаты

### Phase 2: Consolidation
6. Удалить `config.py`, унифицировать на `settings.py`
7. Убрать global `memory_store = MemoryStore()` из memory.py
8. Добавить проверку SQLite при создании engine (не передавать pool_size)

### Phase 3: Image optimization
9. Установить `sentence-transformers` ИЛИ убрать torch
10. Пересобрать образ без CUDA (CPU-only) — уменьшение с 7.9 GB до ~500 MB
11. Удалить или интегрировать `sqlite_store.py`

---

## 10. Files Extracted

```
genesis-images/nz-mem0/
├── .env.example
├── entrypoint.sh
├── README.md (this file)
└── src/
    ├── __init__.py
    ├── main.py
    └── mcp_mem0/
        ├── __init__.py
        ├── audit.py
        ├── config.py
        ├── embeddings.py
        ├── memory.py
        ├── qdrant_store.py
        ├── settings.py
        ├── sqlite_store.py
        ├── utils.py
        ├── api/
        │   ├── __init__.py
        │   ├── health.py
        │   ├── memory.py
        │   └── tools.py
        └── tools/
            ├── __init__.py
            ├── mem_add.py
            ├── mem_delete.py
            └── mem_search.py
```
