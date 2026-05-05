#!/bin/bash
# Start OpenClaw Bridge Server
# Port: 11005 (11004 is used by AI Hub Local Console)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export OPENCLAW_HOST="0.0.0.0"
export OPENCLAW_PORT="11005"
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
export OPENCLAW_WORKSPACE_ROOT="/project"

cd "$PROJECT_DIR"

echo "Starting OpenClaw Bridge Server..."
echo "  Host: $OPENCLAW_HOST"
echo "  Port: $OPENCLAW_PORT"
echo "  Ollama: $OLLAMA_BASE_URL"
echo ""

exec .venv/bin/uvicorn app.openclaw.main:app \
    --host "$OPENCLAW_HOST" \
    --port "$OPENCLAW_PORT" \
    --reload
