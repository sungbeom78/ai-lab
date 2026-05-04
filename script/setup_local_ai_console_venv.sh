#!/bin/bash
set -euo pipefail

cd /project/ai-hub

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in /project/ai-hub/.venv..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

echo "Installing requirements..."
./.venv/bin/python -m pip install -r app/local_ai_console/requirements.txt

echo "Setup complete."
echo "You can now run the console using:"
echo "./script/run_local_ai_console.sh"
