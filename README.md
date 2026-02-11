# genesis-images

Genesis Docker Images Registry

## Build Model

### Canonical Source of Truth (Priority Order)
1. **GitHub Actions CI** — Only supported build mechanism
2. **GitHub Packages Container Registry** (`ghcr.io/nz-genesis/*`) — Only source of truth for images
3. **This repository** — Contains Dockerfiles and CI workflows
4. **Local filesystem** — For debugging only, NOT authoritative

### Key Principles

- **GitHub Actions CI is the ONLY supported build mechanism**
  - All images must be built through GitHub Actions workflows
  - No local docker builds are authoritative for production

- **GHCR (ghcr.io/nz-genesis/*) is the ONLY source of truth for images**
  - If an image exists in GitHub Packages, it IS the canonical version
  - Git repository state may lag behind registry

- **Local docker builds are for debugging only**
  - May differ from CI-built images
  - Not suitable for production deployment

### Recovery Model

This repository follows a **registry-first forensic model** for recovery:
1. Analyze GitHub Packages for actual image inventory
2. Extract and inspect published images when needed
3. Reconstruct Dockerfiles from published layers if source is lost
4. Rebuild through GitHub Actions CI

## Images

| Image | Status | Registry |
|-------|--------|----------|
| nz-execution-gateway | ✅ IMPLEMENTED (v1) | ghcr.io/nz-genesis/genesis-images/nz-execution-gateway |
| genesis-core | ✅ RECOVERY_COMPLETE | ghcr.io/nz-genesis/genesis-core |

## CI/CD

All builds are managed through GitHub Actions workflows in `.github/workflows/`:
- `guard-nz-image-structure.yml` — Structural validation
- `build-*.yml` — Image-specific build workflows

## Recovery Status

| Image | Status | Last Published | Notes |
|-------|--------|----------------|-------|
| nz-litellm | RECOVERY_COMPLETE | 2026-01-26 | Dependency fix only |
| nz-mem0 | RECOVERY_COMPLETE | 2026-01-26 | API signature fixes |
| nz-intent-adapter | RECOVERY_COMPLETE | 2026-02-10 | Phase 3.3 stub, legacy intent formation |
| nz-execution-gateway | ✅ IMPLEMENTED (v1) | 2026-02-10 | Full implementation with validation pipeline |
| nz-stack-core | RECOVERY_COMPLETE | 2026-02-10 | Registry-first recovery from GHCR
| genesis-core | RECOVERY_COMPLETE | 2026-02-10 | Registry-first recovery from GHCR |

- **Total Images:** 6
- **Completed:** 4 (nz-litellm, nz-mem0, nz-intent-adapter, nz-execution-gateway)
- **Lost:** 0
- **Remaining:** 2

---

## Canonical Recovery & Build Process (v1)

This repository follows a strict, human-approved recovery and build process.
Deviation from this process is forbidden.

### Source of Truth Hierarchy

GitHub Actions CI → GitHub Container Registry (GHCR) → Repository → Local

- GHCR is the factual source of image existence
- Repository ensures reproducibility
- Local builds are NOT a source of truth

### Allowed Build Method

- Docker images MUST be built and published ONLY via GitHub Actions
- Local docker build is allowed for debugging only
- Any recovery is considered incomplete until the image is published to GHCR

### Canonical Recovery Cycle

Registry verification →
Forensic analysis →
Human approval →
Controlled remediation →
CI rebuild & publish →
Fixation

Each step is mandatory. Skipping steps is forbidden.

### Forensic-First Principle

- Recovery is NOT feature development
- Only defect fixes and removal of broken code are allowed
- No new functionality may be introduced during recovery

### Human Final Authority

Human approval is REQUIRED before:
- applying remediation
- changing image behavior
- modifying public interfaces
- proceeding to next image

Silence is NOT approval.

### Image Statuses

Each image MUST have one of the following statuses:

- RECOVERY_COMPLETE
- FORENSIC_COMPLETE (needs approval)
- PENDING
- BLOCKED
- LOST

Status must be reflected in both README and CI state.

### Repository Structure Invariants

Allowed top-level structure:

genesis-images/
├── .github/workflows/
├── nz-*/
├── genesis-core/
├── docs/
└── README.md

Any other directories are forbidden and must be removed.

---

## Recovery Post-Mortem

### nz-litellm

**Root cause:** Broken reference to lightrag in requirements.txt (typo: litellm[all] → litellm[all]==1.2.0)

**Remediation:** Replaced requirements.txt with corrected litellm version

**Not restored:**
- Custom model configurations
- Extra dependencies

**Verification:** CI build succeeded, image published to GHCR

### nz-mem0

**Nature of breakage:** API signature mismatches between memory.py and tools, Settings.TZ attribute error, MCP dict access issue

**Categories of fixes:**
- C1: Settings.TZ removal (health.py)
- C2: MCP dict access fix (tools.py)
- C3: MemoryStore.store() signature fix
- C4: mem_search() signature fix
- C5: qdrant_store payload inclusion

**Constraints:**
- No Dockerfile changes
- No sentence-transformers added
- No CUDA removal

**Trade-off:** Image size remains ~7.9 GB (optimization deferred)

---

## nz-execution-gateway

**Status**: ✅ IMPLEMENTED (v1)

**Registry**: ghcr.io/nz-genesis/genesis-images/nz-execution-gateway

**CI Workflow**: [build-nz-execution-gateway.yml](.github/workflows/build-nz-execution-gateway.yml)

**CI Run**: [21883083849](https://github.com/nz-genesis/genesis-images/actions/runs/21883083849) ✅ SUCCESS

**Image Digest**: `sha256:d6c02595b24e444906df3bc9206fc42b24d4931299c4ecb357bbbc7f3e189ff1`

**Implementation Details**:
- Full validation pipeline (Schema → Context → Intent → Security → Sandbox → Resources → State)
- DENIAL_MATRIX rejection codes (R-CTX-XXX, R-INTENT-XXX, R-SCHEMA-XXX, R-SEC-XXX, R-SBX-XXX, R-RES-XXX, R-STATE-XXX)
- Sandbox lifecycle management (create, execute, destroy)
- State machine with transitions: REQUEST_RECEIVED → VALIDATION → REJECTED/SANDBOX_CREATED → EXECUTION → SANDBOX_DESTROYED → RESPONSE
- Audit logging with trace IDs

**Verification**:
- Docker build: SUCCESS
- CI run: SUCCESS ✅
- GHCR published: ✅ FIXATED (digest confirmed)
- Local run: Health endpoint responds (`{"error":"Unauthorized"}`)
- Security: Minimal image (distroless, no shell)

---

## nz-intent-adapter Canon Compliance Analysis

**Status**: Phase 3.3 stub (заглушка)
**Image**: ghcr.io/nz-genesis/nz-intent-adapter:latest
**Digest**: sha256:90320a2c99fd4006c6b2b652cbe049ec8699ca5a77b8fd7d1e03eb43227ea1ae
**Size**: 184 MB

### Canon Alignment

| Canon Requirement | Implementation | Classification |
|------------------|---------------|----------------|
| Health endpoint (/health) | ✅ Match | — |
| Port 8080 | ✅ Match | — |
| Subject authentication | ⚠️ Deviation | ENGINEERING_DEBT |
| Tenant resolution | ⚠️ Deviation | ENGINEERING_DEBT |
| Context collection | ⚠️ Deviation | ENGINEERING_DEBT |
| INTENT formation | ⚠️ Deviation | LEGACY_DEVIATION |
| Stack Core integration | ⚠️ Deviation | ENGINEERING_DEBT |

### Classification Summary

- **CANON_VIOLATION**: 0
- **ENGINEERING_DEBT**: 5 (missing features)
- **LEGACY_DEVIATION**: 1 (INTENT stub)

### STOP Conditions

- Requires architectural decision: NO
- Canon interpretation ambiguous: NO

### Recommendation

Image is functional Phase 3.3 stub. Full canon compliance requires explicit upgrade decision from Human.

---

## GHCR Namespace Canon

**Canon Decision:** Все runtime images должны публиковаться в `ghcr.io/nz-genesis/<image>` (БЕЗ `/images/`).

**Образы:**
- `ghcr.io/nz-genesis/genesis-core`
- `ghcr.io/nz-genesis/nz-stack-core`
- `ghcr.io/nz-genesis/nz-execution-gateway` (нормализован 2026-02-11)

**Legacy:**
- `ghcr.io/nz-genesis/genesis-images/nz-execution-gateway` — старый namespace, сохранён для обратной совместимости

---

## GHCR FIXATION REPORT (2026-02-11)

### Статус фиксации

| Образ | GHCR Path | Status | Digest (SHA256) |
|-------|-----------|--------|-----------------|
| genesis-core | `ghcr.io/nz-genesis/genesis-core` | ✅ IMPLEMENTED — FIXATED | `sha256:c5c66064c0e6c609bd31e6f260c92b3eef94389330e3fd5fd37d43153059fe99` |
| nz-stack-core | `ghcr.io/nz-genesis/nz-stack-core` | ✅ IMPLEMENTED — FIXATED | `sha256:9592378fb57c4dfcf9d40de637042bbf53f93eea56282c59622b8c53cbdf42c6` |
| nz-execution-gateway | `ghcr.io/nz-genesis/nz-execution-gateway` | ✅ IMPLEMENTED — FIXATED | `sha256:df76f46fabf86e57ae107fd8bef5a9bd0e15af5d1c4ef391b762fc546f53f4e8` |

### Информация о размерах

- genesis-core: 236 MB (обновлён: 2026-02-08)
- nz-stack-core: 170 MB (обновлён: 2026-01-26)

### Namespace Clarification

⚠️ **Важно**: Образы публикуются в `ghcr.io/nz-genesis/` (БЕЗ `/images/`).

Фактические пути:
- `ghcr.io/nz-genesis/genesis-core`
- `ghcr.io/nz-genesis/nz-stack-core`

### Локальная верификация

- ✅ genesis-core: успешный запуск (base image)
- ✅ nz-stack-core: запущен, Uvicorn на порту 8081, health check PASSED

### Source of Truth

- CI: GitHub Actions (build-genesis-core.yml, build-nz-stack-core.yml)
- Registry: GHCR (`ghcr.io/nz-genesis/genesis-core`, `ghcr.io/nz-genesis/nz-stack-core`)
- Digest фиксация: 2026-02-11

## Registry State — 2026-02-XX

Active canonical runtime images:
- genesis-core
- nz-stack-core
- nz-intent-adapter
- nz-mem0
- nz-litellm
- nz-execution-gateway

All legacy / experimental images were removed.
GHCR namespace canonical format:
ghcr.io/nz-genesis/<image>
