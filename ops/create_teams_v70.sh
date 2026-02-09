#!/usr/bin/env bash
set -e

ORG="nz-genesis"

echo "[INFO] Creating Genesis v70.0 teams in GitHub..."

declare -A TEAMS
TEAMS["devs"]="Genesis Developers: code, schemas, agents, skills."
TEAMS["docs"]="Documentation team: docs, public, infra docs."
TEAMS["infra"]="Infra & DevOps: CI, LXC dev, backup, services deployment."
TEAMS["security"]="Security & Compliance: RBAC, secrets, trust model."

for TEAM in "${!TEAMS[@]}"; do
  DESC="${TEAMS[$TEAM]}"

  echo "[ACTION] Creating team: $TEAM"

  gh api \
    --method POST \
    -H "Accept: application/vnd.github+json" \
    "/orgs/$ORG/teams" \
    -f name="$TEAM" \
    -f description="$DESC" \
    -f privacy="closed" \
    >/dev/null || echo "[WARN] Team already exists: $TEAM"
done

echo "[INFO] All teams processed."
