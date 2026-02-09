#!/usr/bin/env bash
set -e

# Настройки
ORG="nz-genesis"
TARGET_DIR="/opt/genesis/work" # Или /src, если планировали туда
mkdir -p "$TARGET_DIR"

echo "[INFO] =============== Genesis v70.0 — Clone Repositories (LXC Hydration) =============="
echo "[INFO] Target Directory: $TARGET_DIR"

# Список всех 18 репозиториев v70.0
REPOS=(
    "genesis-agents"
    "genesis-skills"
    "genesis-schemas"
    "genesis-memory"
    "genesis-images"
    "genesis-supermonorepo"
    "genesis-mirror-scripts"
    "genesis-ci-templates"
    "genesis-minio-schema"
    "genesis-lab"
    "genesis-services"
    "genesis-infra"
    "genesis-backup-and-recovery"
    "genesis-release-manifest"
    "genesis-security-model"
    "genesis-docs"
    "genesis-assets"
    "genesis-public"
)

cd "$TARGET_DIR"

for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
        echo "[SKIP] $repo already exists in $TARGET_DIR"
    else
        echo "[ACTION] Cloning $repo..."
        gh repo clone "$ORG/$repo"
        
        # Опционально: Настройка локального git user, если в контейнере он не задан
        # git -C "$repo" config user.name "Genesis Bot"
        # git -C "$repo" config user.email "bot@nz-genesis.com"
    fi
done

echo "[INFO] ================= All Repositories Cloned Successfully ==================="
ls -la "$TARGET_DIR"
