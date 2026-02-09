#!/usr/bin/env bash
set -e

# ============================================================================
# Genesis v0.1.0 — Clone & Link All Repositories
# Purpose: Hydrate /opt/genesis/dev with all 18 repos from nz-genesis org
# Establishes git remote tracking, local branches, and base configuration
# ============================================================================

ORG="nz-genesis"
DEV_DIR="/opt/genesis/dev"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║ Genesis v0.1.0 — Repository Hydration Script                             ║"
echo "║ Target: $DEV_DIR                                  ║"
echo "║ Timestamp: $TIMESTAMP                                      ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

mkdir -p "$DEV_DIR"
cd "$DEV_DIR"

REPOS=(
    "genesis-agents" "genesis-skills" "genesis-schemas" "genesis-memory" 
    "genesis-images" "genesis-supermonorepo" "genesis-mirror-scripts" 
    "genesis-ci-templates" "genesis-minio-schema" "genesis-lab" 
    "genesis-services" "genesis-infra" "genesis-backup-and-recovery" 
    "genesis-release-manifest" "genesis-security-model" "genesis-docs" 
    "genesis-assets" "genesis-public"
)

TOTAL_REPOS=${#REPOS[@]}
CLONED_COUNT=0
SKIPPED_COUNT=0
FAILED_COUNT=0

LOG_FILE="/opt/genesis/ops/logs/clone_dev_${TIMESTAMP}.log"
mkdir -p /opt/genesis/ops/logs
touch "$LOG_FILE"

echo "[$(date '+%H:%M:%S')] ▶ Starting clone operation..." | tee -a "$LOG_FILE"
echo "[$(date '+%H:%M:%S')] Target directory: $DEV_DIR" | tee -a "$LOG_FILE"
echo "[$(date '+%H:%M:%S')] Total repositories: $TOTAL_REPOS" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

for i in "${!REPOS[@]}"; do
    repo="${REPOS[$i]}"
    progress=$((i + 1))
    repo_path="$DEV_DIR/$repo"
    
    echo "─────────────────────────────────────────────────────────────────────────────"
    echo "[$(date '+%H:%M:%S')] [$progress/$TOTAL_REPOS] Processing: $repo"
    
    if [ -d "$repo_path" ]; then
        echo "  ⏭️  [SKIP] Repository already exists"
        echo "[$(date '+%H:%M:%S')] [$progress/$TOTAL_REPOS] SKIP: $repo" >> "$LOG_FILE"
        ((SKIPPED_COUNT++))
        continue
    fi
    
    echo "  ⬇️  [CLONE] Cloning from origin..."
    if gh repo clone "$ORG/$repo" "$repo" 2>>"$LOG_FILE"; then
        ((CLONED_COUNT++))
        
        cd "$repo_path"
        
        if ! git config user.name >/dev/null; then
            git config user.name "Genesis Developer"
            echo "    ✓ Git user configured"
        fi
        
        CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
        if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
            if git show-ref --verify --quiet refs/heads/main; then
                git checkout main 2>/dev/null
            elif git show-ref --verify --quiet refs/heads/master; then
                git checkout master 2>/dev/null
            fi
        fi
        
        REMOTE_BRANCHES=$(git branch -r | grep -v HEAD | sed 's/origin\///' || true)
        for branch in $REMOTE_BRANCHES; do
            if ! git show-ref --verify --quiet refs/heads/"$branch"; then
                git branch --track "$branch" "origin/$branch" 2>/dev/null || true
            fi
        done
        
        REMOTE_URL=$(git config --get remote.origin.url)
        COMMIT_HASH=$(git rev-parse --short HEAD)
        echo "    ✓ Remote: $REMOTE_URL"
        echo "    ✓ Branch: $(git rev-parse --abbrev-ref HEAD)"
        echo "    ✓ Commit: $COMMIT_HASH"
        
        echo "[$(date '+%H:%M:%S')] [$progress/$TOTAL_REPOS] SUCCESS: $repo" >> "$LOG_FILE"
        
        cd "$DEV_DIR"
        echo "  ✅ [DONE] $repo configured"
    else
        ((FAILED_COUNT++))
        echo "[$(date '+%H:%M:%S')] [$progress/$TOTAL_REPOS] FAILED: $repo" >> "$LOG_FILE"
        echo "  ❌ [ERROR] Failed to clone $repo"
        cd "$DEV_DIR"
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║ OPERATION COMPLETE                                                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "  ✅ Cloned:  $CLONED_COUNT repositories"
echo "  ⏭️  Skipped: $SKIPPED_COUNT repositories"
echo "  ❌ Failed:  $FAILED_COUNT repositories"
echo ""
echo "📂 Dev Environment Structure:"
ls -la "$DEV_DIR" | tail -n +4 | awk '{print "  " $0}'
echo ""
echo "📋 Repository List:"
cd "$DEV_DIR"
for repo in "${REPOS[@]}"; do
    if [ -d "$repo/.git" ]; then
        BRANCH=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        COMMIT=$(cd "$repo" && git rev-parse --short HEAD 2>/dev/null || echo "none")
        echo "  ✓ $repo (branch: $BRANCH, commit: $COMMIT)"
    else
        echo "  ✗ $repo (not cloned)"
    fi
done
echo ""
echo "📝 Log: $LOG_FILE"
echo "✨ Ready for v0.1.0 development"
