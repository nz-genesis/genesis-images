#!/usr/bin/env bash
set -euo pipefail

# entrypoint for nz-mem0
# responsibilities:
#  - load .env if present
#  - run a quick python import sanity check
#  - exec the CMD (uvicorn ...) as PID 1

# load .env if exists (simple)
ENV_FILE="/app/.env"
if [ -f "${ENV_FILE}" ]; then
  # shellcheck disable=SC1090
  set -o allexport
  # shellcheck disable=SC1090
  . "${ENV_FILE}"
  set +o allexport
fi

echo "Starting nz-mem0 (bind=${HOST:-0.0.0.0}, port=${PORT:-8090})"

# quick import check to produce readable error early (smoke-test relies on this)
python - <<'PY'
import sys
try:
    import importlib
    importlib.import_module("main")
except Exception as e:
    print("ERROR: import of 'main' failed:", file=sys.stderr)
    raise
PY

# exec passed CMD (uvicorn main:app ...)
exec "$@"
