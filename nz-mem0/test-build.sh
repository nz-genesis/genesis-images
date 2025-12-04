#!/bin/bash
set -e

echo "=========================================================="
echo "   NZ-MEM0 — isolated wheel build test (python:3.11-slim)"
echo "=========================================================="

# auto-detect correct project root
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MEM0_DIR="$PROJECT_ROOT/custom/nz-mem0"

echo ">>> PROJECT_ROOT = $PROJECT_ROOT"
echo ">>> MEM0_DIR     = $MEM0_DIR"

# check directory exists
if [ ! -d "$MEM0_DIR" ]; then
    echo "❌ ERROR: Directory not found: $MEM0_DIR"
    exit 1
fi

# check requirements exists
if [ ! -f "$MEM0_DIR/requirements.txt" ]; then
    echo "❌ ERROR: requirements.txt NOT FOUND in $MEM0_DIR"
    ls -la "$MEM0_DIR"
    exit 1
fi

echo ">>> requirements.txt found OK"
echo ">>> launching python:3.11-slim container..."

docker run --rm \
    -v "$MEM0_DIR":/work \
    -w /work \
    python:3.11-slim \
    bash -c "
        set -e
        echo '>>> Inside container, current directory:'; pwd
        echo '>>> File list:'; ls -la .
        
        echo '>>> Upgrading pip...'
        pip install --upgrade pip
        
        echo '>>> Resolving dependencies (pip wheel)...'
        pip wheel --wheel-dir /tmp/wheels -r requirements.txt
        
        echo '>>> SUCCESS: Wheel build completed OK'
    " || {
        echo "❌ FAILURE: wheel build failed"
        exit 1
    }

echo "=========================================================="
echo "    ✔ NZ-MEM0: pip wheel build test passed successfully"
echo "=========================================================="
