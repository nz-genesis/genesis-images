#!/usr/bin/env bash
# FILE: src/start.sh
set -euo pipefail
export PYTHONUNBUFFERED=1

: "${MEM0_BIND:=0.0.0.0}"
: "${MEM0_PORT:=8090}"

exec uvicorn main:app --host "${MEM0_BIND}" --port "${MEM0_PORT}" --log-level info
