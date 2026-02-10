# =============================================================================
# genesis-core - Build-only Docker Image
# =============================================================================
# RECONSTRUCTED FROM: ghcr.io/nz-genesis/genesis-core:latest
# IMAGE DIGEST: sha256:cf7d9e0a45c47b067fd6fe8eb51e0b4876b76f58b27773f983de36889b1ce1c7
# RECOVERY DATE: 2026-02-10
# =============================================================================
# This image is used exclusively for building the genesis-core Go project.
# It performs `go build ./...` and does not include any runtime components,
# ports, or entrypoints.
# =============================================================================

# -----------------------------------------------------------------------------
# BASE IMAGE LAYER (FROM golang:1.21-alpine)
# -----------------------------------------------------------------------------
# Layer history from golang:1.21-alpine base:
# - ADD file:99093095d62d0421541d882f9ceeddb2981fe701ec0aa9d2c08480712d5fed21 in /
# - CMD ["/bin/sh"]
# - RUN apk add --no-cache ca-certificates
# - ENV GOLANG_VERSION=1.21.13
# - ENV GOTOOLCHAIN=local
# - ENV GOPATH=/go
# - ENV PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# - COPY /target/ / #
# - RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 1777 "$GOPATH"
# - WORKDIR /go
# -----------------------------------------------------------------------------

FROM golang:1.21-alpine AS builder

# Set working directory
WORKDIR /build

# Copy source code from parent directory (genesis-core project)
# Layer: COPY ../ . # buildkit
COPY ../ .

# Build the project
# Layer: RUN /bin/sh -c go build ./... # buildkit
RUN go build ./...

# =============================================================================
# FINAL IMAGE METADATA
# =============================================================================
# This is a build-only image
# No runtime, ports, CMD, or ENTRYPOINT are included
# =============================================================================
