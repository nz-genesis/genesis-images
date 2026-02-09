#!/usr/bin/env bash
set -e

ORG="nz-genesis"

echo "[INFO] Starting Massive Rebrand (Removing 'v70.0' from descriptions)..."

# Функция для обновления описания
update_desc() {
    local repo=$1
    local desc=$2
    echo "[UPDATE] $repo -> $desc"
    gh repo edit "$ORG/$repo" --description "$desc" >/dev/null
}

# 1. CORE & AGENTS
update_desc "genesis-agents" "Core AI Agents System: Planner, Evaluator, Rotator & Meta-agents orchestration."
update_desc "genesis-skills" "Skill Registry & Runtime: Atomic capabilities execution environment."
update_desc "genesis-schemas" "Data Contracts & Schemas: JSON/Pydantic definitions for system-wide interoperability."
update_desc "genesis-memory" "Memory Bus: Vector (Qdrant), Relational (Postgres) and Ephemeral (Redis) storage layers."
update_desc "genesis-supermonorepo" "Genesis Platform Monorepo: Aggregates core logic and reasoning banks."

# 2. INFRA & DEVOPS
update_desc "genesis-infra" "Infrastructure as Code: LXC, Proxmox, Networking & Proxy configurations."
update_desc "genesis-images" "Container Registry Sources: Dockerfiles for System Services and AI Agents."
update_desc "genesis-services" "Service Orchestration: Docker Swarm/Portainer stacks and compositions."
update_desc "genesis-ci-templates" "CI/CD Pipelines: Reusable GitHub Actions workflows and automation templates."
update_desc "genesis-mirror-scripts" "Repository Mirroring: Automation for GitHub <-> Gitea synchronization."

# 3. SECURITY & DATA
update_desc "genesis-security-model" "Security & Governance: RBAC policies, IAM, Audit logs and Zero-Trust definitions."
update_desc "genesis-minio-schema" "Object Storage Layout: MinIO bucket policies, retention and lifecycle rules."
update_desc "genesis-backup-and-recovery" "Disaster Recovery: Backup strategies, snapshots and restoration playbooks."
update_desc "genesis-release-manifest" "Release Management: Version manifests, changelogs and compatibility matrices."

# 4. DOCS & PUBLIC
update_desc "genesis-docs" "Platform Documentation: Architecture blueprints, API specs and Developer guides."
update_desc "genesis-assets" "Static Assets: Design resources, media files and binary artifacts."
update_desc "genesis-public" "Public Showcase: Demos, examples and community-facing resources."
update_desc "genesis-lab" "R&D Laboratory: Experimental prototypes and sandbox environment."

echo "[SUCCESS] All repositories have been renamed to Clean Architecture standards."
