# genesis-core Build Image

Build-only Docker image for the genesis-core Go project.

## Purpose

This image is used exclusively for building the genesis-core project. It performs `go build ./...` and does not include any runtime components, ports, or entrypoints.

## Usage

```dockerfile
FROM ghcr.io/nz-genesis/genesis-core:latest AS builder

# Use for multi-stage builds in other projects
COPY --from=ghcr.io/nz-genesis/genesis-core:latest /build/bin/ /usr/local/bin/
```

## Notes

- This is a **build-only** image
- No runtime environment is included
- No ports are exposed
- No CMD or ENTRYPOINT is defined
# CI trigger: 2026-02-08T14:02:00+00:00
