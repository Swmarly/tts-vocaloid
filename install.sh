#!/usr/bin/env bash
set -euo pipefail

# Simple installer script for tts2sv and the optional Electron GUI.
# Usage: ./install.sh [venv_path]
# Defaults to creating a virtual environment in .venv.

VENV_DIR="${1:-.venv}"
PYTHON_BIN="${PYTHON:-python3}"
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: Python executable '$PYTHON_BIN' not found. Set the PYTHON environment variable if Python is installed elsewhere." >&2
  exit 1
fi

echo "Creating virtual environment at $VENV_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"

# shellcheck disable=SC1091
source "$VENV_DIR"/bin/activate

python -m pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"
pip install -e "$PROJECT_ROOT"

deactivate

echo "Python environment ready. To use it later, run 'source $VENV_DIR/bin/activate'."

if command -v npm >/dev/null 2>&1; then
  echo "Installing Electron GUI dependencies"
  (cd "$PROJECT_ROOT/electron-app" && npm install)
  echo "Electron GUI dependencies installed. Launch with 'npm start' inside electron-app after activating the virtualenv if needed."
else
  cat <<'MSG'
Warning: npm was not found on your PATH, so the Electron GUI dependencies were not installed.
Install Node.js (https://nodejs.org/) and rerun 'npm install' inside electron-app to enable the GUI.
MSG
fi

echo "Setup complete."
