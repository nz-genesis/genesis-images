#!/usr/bin/env bash
set -e

ORG="nz-genesis"

echo "[INFO] =============== Genesis v70.0 — Apply Team Permissions (R7 FINAL FIX) =============="

apply_perm() {
    local team=$1
    local perm=$2
    local repo=$3

    echo "[ACTION] $team → $perm → $repo"

    gh api \
      --method PUT \
      "orgs/$ORG/teams/$team/repos/$ORG/$repo" \
      -f permission="$perm" >/dev/null 2>&1

    if [ $? -ne 0 ]; then
        echo "[WARN] Failed: team=$team repo=$repo perm=$perm"
    fi
}

# === МАТРИЦА ДОСТУПА (GitHub: pull/push/admin) ===

# devs → push на все code-репозитории
for r in genesis-agents genesis-skills genesis-schemas genesis-memory genesis-images genesis-supermonorepo genesis-mirror-scripts genesis-ci-templates genesis-minio-schema genesis-lab genesis-services; do
    apply_perm devs push $r
done

# infra → push только на инфраструктуру
for r in genesis-infra genesis-backup-and-recovery genesis-mirror-scripts genesis-release-manifest; do
    apply_perm infra push $r
done

# infra → pull на всё остальное
for r in genesis-docs genesis-assets genesis-agents genesis-skills genesis-schemas genesis-memory genesis-images genesis-minio-schema genesis-supermonorepo genesis-services genesis-lab genesis-public; do
    apply_perm infra pull $r
done

# docs → push только genesis-docs
apply_perm docs push genesis-docs

# docs → pull на всё остальное
for r in genesis-public genesis-assets genesis-agents genesis-skills genesis-schemas genesis-memory genesis-images genesis-minio-schema genesis-supermonorepo genesis-services genesis-lab genesis-release-manifest genesis-backup-and-recovery genesis-ci-templates genesis-security-model genesis-infra; do
    apply_perm docs pull $r
done

# security → pull для всех секретов и схем
for r in genesis-security-model genesis-minio-schema genesis-release-manifest genesis-backup-and-recovery genesis-agents genesis-skills genesis-schemas genesis-memory genesis-images genesis-services genesis-infra genesis-ci-templates genesis-assets genesis-lab genesis-public genesis-docs genesis-supermonorepo; do
    apply_perm security pull $r
done

echo "[INFO] ================= Permissions Applied Successfully (R7 FINAL FIX) ================="
