#!/usr/bin/env bash
#
# migrate_v70.0.sh — Genesis v70.0 Repository Migration (Revision R3)
# Исправление: добавлен флаг --accept-visibility-change-consequences
#

set -euo pipefail

ORG="nz-genesis"
LOG_FILE="/opt/genesis/ops/migrate_v70.log"
mkdir -p /opt/genesis/ops

log() {
    echo -e "$1"
    echo -e "$(date '+%Y-%m-%d %H:%M:%S')  $1" >> "$LOG_FILE"
}

log "[INFO] ================= Genesis v70.0 Migration R3 started ================"
log "[INFO] Checking GitHub Auth..."

gh auth status || {
    log "[ERROR] gh authentication failed."
    exit 1
}

log "[INFO] Checking organization membership via reliable API path..."

if ! gh api user/memberships/orgs | jq -e ".[] | select(.organization.login==\"$ORG\")" >/dev/null; then
    log "[ERROR] You are NOT a member or admin of organization $ORG"
    exit 1
else
    log "[INFO] Membership confirmed: access to $ORG OK."
fi

log "[INFO] Fetching repository list from $ORG..."

REPOS=$(gh repo list "$ORG" --json name,visibility --limit 200 | jq -rc '.[]')

log "[INFO] Found repositories:"
echo "$REPOS" | jq -r '.name + " (" + .visibility + ")"' | tee -a "$LOG_FILE"

# -------------------------
# Target structure v70.0
# -------------------------

declare -A SHOULD_BE_PRIVATE=(
  ["genesis-docs"]=1
  ["genesis-assets"]=1
  ["genesis-mirror-scripts"]=1
  ["genesis-ci-templates"]=1
  ["genesis-release-manifest"]=1
  ["genesis-security-model"]=1
  ["genesis-backup-and-recovery"]=1
  ["genesis-infra"]=1
  ["genesis-services"]=1
  ["genesis-images"]=1
  ["genesis-minio-schema"]=1
  ["genesis-memory"]=1
  ["genesis-schemas"]=1
  ["genesis-skills"]=1
  ["genesis-agents"]=1
  ["genesis-supermonorepo"]=1
  ["genesis-lab"]=1
)

declare -A SHOULD_BE_PUBLIC=(
  ["genesis-public"]=1
)

log "[INFO] Starting visibility corrections..."

correct_visibility() {
    local name="$1"
    local current_vis="$2"

    if [[ ${SHOULD_BE_PUBLIC[$name]+yes} ]]; then
        if [[ "$current_vis" != "public" ]]; then
            log "[ACTION] Setting PUBLIC visibility → $name"
            gh repo edit "$ORG/$name" \
                --visibility public \
                --accept-visibility-change-consequences
        else
            log "[OK] $name already public"
        fi
    fi

    if [[ ${SHOULD_BE_PRIVATE[$name]+yes} ]]; then
        if [[ "$current_vis" != "private" ]]; then
            log "[ACTION] Setting PRIVATE visibility → $name"
            gh repo edit "$ORG/$name" \
                --visibility private \
                --accept-visibility-change-consequences
        else
            log "[OK] $name already private"
        fi
    fi
}

echo "$REPOS" | while read -r repo; do
    NAME=$(echo "$repo" | jq -r '.name')
    VIS=$(echo "$repo" | jq -r '.visibility')
    correct_visibility "$NAME" "$VIS"
done

log "[INFO] Visibility correction phase complete."

# -----------------------------
# Team permissions
# -----------------------------

log "[INFO] Setting team permissions (core-admins → admin)..."

CORE_ADMINS_TEAM="core-admins"

for repo in $(echo "$REPOS" | jq -r '.name'); do
    log "[ACTION] Grant admin to $CORE_ADMINS_TEAM on $repo"
    gh api \
      --method PUT \
      -H "Accept: application/vnd.github+json" \
      "orgs/$ORG/teams/$CORE_ADMINS_TEAM/repos/$ORG/$repo" \
      -f permission=admin \
      >/dev/null || log "[WARN] Failed to assign permissions for $repo"
done

log "[INFO] Team permissions updated."
log "[INFO] ================= Migration Complete (R3) ================"
log "[INFO] Log saved to $LOG_FILE"

echo ""
echo "---------------------------------------------------------------"
echo "  Migration Completed Successfully (v70.0 R3)"
echo "  Log file: $LOG_FILE"
echo "---------------------------------------------------------------"
