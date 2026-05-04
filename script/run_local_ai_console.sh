#!/bin/bash
set -euo pipefail

PORT=${PORT:-11004}

cd /project/ai-hub

if [ -f ".venv/bin/uvicorn" ]; then
    UVICORN_BIN=".venv/bin/uvicorn"
else
    echo "Warning: .venv not found. Using system python."
    UVICORN_BIN="python3 -m uvicorn"
fi

DESKTOP_LAN_IP=$(hostname -I | awk '{print $1}' || echo "<DESKTOP_LAN_IP>")

echo "Local AI Web Console"
echo "URL: http://localhost:$PORT"
echo "LAN URL: http://$DESKTOP_LAN_IP:$PORT"
echo "Press Ctrl+C to stop"

PYTHONPATH=/project/ai-hub $UVICORN_BIN app.local_ai_console.main:app --host 0.0.0.0 --port $PORT
