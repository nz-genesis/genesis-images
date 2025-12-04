# nz-mem0 — image README

This image contains the NZ-MEM0 service (Genesis L2 Working Memory).

## Build & push (CI)
Use the canonical CI workflow to build, tag and push image to Gitea Registry.
Do not use Portainer to build images — Portainer only deploys the image.

## Runtime
- Service runs on port 8090
- Expects config from environment / Portainer `.env` or secrets
- Data directory: `/data` (named volume)

## Healthchecks (smoke tests)
- HTTP: GET /health → 200
- Startup: entrypoint validates import of `main` before exec

## Notes
All configuration files are embedded into the image (per IMAGE_DEPLOYMENT_PROTOCOL).
