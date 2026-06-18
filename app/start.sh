#!/usr/bin/env bash
# Start the YouTube to Reference Assets UI.
# Usage: bash app/start.sh
# Then open the printed http://127.0.0.1 address in your browser.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${YT_UI_PORT:-8765}"

# Open the browser after a short delay, best effort, ignored if it fails.
( sleep 1.2
  URL="http://127.0.0.1:${PORT}"
  if command -v open >/dev/null 2>&1; then open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
  fi ) >/dev/null 2>&1 &

exec python3 "${DIR}/server.py"
