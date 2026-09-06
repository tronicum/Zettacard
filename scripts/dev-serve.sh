#!/usr/bin/env bash
# Local static server for the Zettacard PWA.
#
# netlify.toml sets `publish = "app"` - app/ IS the site root in
# production, not a subdirectory of it. Running `python3 -m http.server`
# from the repo root instead serves the repo root, so /app.html, /data/*,
# /assets/* etc. all 404 (that's exactly what tripped up local testing
# just now). This script serves app/ itself as the document root, so
# local URLs match production ones exactly.
#
# Usage:
#   scripts/dev-serve.sh          # port 8080
#   scripts/dev-serve.sh 9000     # custom port
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${1:-8080}"

if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Usage: scripts/dev-serve.sh [port]" >&2
  exit 1
fi

if lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
  echo "Port $PORT is already in use - killing the existing listener..."
  lsof -ti tcp:"$PORT" | xargs kill -9 2>/dev/null || true
  sleep 0.3
fi

echo "Serving app/ (the Netlify publish root) at http://localhost:$PORT/"
echo "  App:      http://localhost:$PORT/app.html"
echo "  Landing:  http://localhost:$PORT/index.html"
echo "  Impressum: http://localhost:$PORT/impressum.html"
echo "(Ctrl-C to stop)"
exec python3 -m http.server "$PORT" --directory app
