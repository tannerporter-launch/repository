#!/usr/bin/env bash
# Usage: ./deploy.sh root@DROPLET_IP   (first run also installs Docker)
set -euo pipefail
HOST="${1:?usage: ./deploy.sh user@droplet-ip}"
DIR=/opt/client-dashboard
ssh "$HOST" "command -v docker >/dev/null || curl -fsSL https://get.docker.com | sh; mkdir -p $DIR"
rsync -az --delete --exclude .env --exclude data --exclude __pycache__ --exclude tests ./ "$HOST:$DIR/"
ssh "$HOST" "cd $DIR && test -f .env || { echo 'Create $DIR/.env from .env.example first'; exit 1; }; docker compose up -d --build"
echo "Deployed. Check: https://\$DOMAIN/health"
