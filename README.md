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
| nz-litellm | ✅ RECOVERY_COMPLETE | ghcr.io/nz-genesis/nz-litellm |
| nz-mem0 | ✅ RECOVERY_COMPLETE | ghcr.io/nz-genesis/nz-mem0 |
| nz-intent-adapter | 🔲 Pending | ghcr.io/nz-genesis/nz-intent-adapter |
| nz-stack-core | 🔲 Pending | ghcr.io/nz-genesis/nz-stack-core |
| genesis-core | 🔲 Pending | ghcr.io/nz-genesis/genesis-core |

## CI/CD

All builds are managed through GitHub Actions workflows in `.github/workflows/`:
- `guard-nz-image-structure.yml` — Structural validation
- `build-*.yml` — Image-specific build workflows

## Recovery Status

- **Total Images:** 5
- **Completed:** 2 (nz-litellm, nz-mem0)
- **Remaining:** 3

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
