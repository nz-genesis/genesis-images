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
| nz-mem0 | 🔲 Pending | ghcr.io/nz-genesis/nz-mem0 |
| nz-intent-adapter | 🔲 Pending | ghcr.io/nz-genesis/nz-intent-adapter |
| nz-stack-core | 🔲 Pending | ghcr.io/nz-genesis/nz-stack-core |
| genesis-core | 🔲 Pending | ghcr.io/nz-genesis/genesis-core |

## CI/CD

All builds are managed through GitHub Actions workflows in `.github/workflows/`:
- `guard-nz-image-structure.yml` — Structural validation
- `build-*.yml` — Image-specific build workflows

## Recovery Status

- **Total Images:** 5
- **Completed:** 1 (nz-litellm)
- **Remaining:** 4
