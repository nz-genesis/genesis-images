#!/bin/bash
# entrypoint.sh - nz-mem0 startup script
set -e

echo "🚀 Starting nz-mem0 v0.1.0..."

# Smoke tests
echo "📋 Running smoke tests..."

# Test: Python imports
python3 << 'EOF'
import sys
try:
    from src.main import app
    print("✅ src.main.app imports OK")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

try:
    from src.mcp_mem0.settings import Settings
    print("✅ Settings imports OK")
except Exception as e:
    print(f"❌ Settings import error: {e}")
    sys.exit(1)

try:
    from src.mcp_mem0.memory import MemoryStore
    print("✅ MemoryStore imports OK")
except Exception as e:
    print(f"❌ MemoryStore import error: {e}")
    sys.exit(1)
EOF

echo "✅ All smoke tests passed!"

# Start uvicorn with FastAPI app
echo "🌐 Starting uvicorn server on 0.0.0.0:8090..."
exec uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8090 \
    --log-level info