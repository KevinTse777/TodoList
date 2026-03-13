#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[deploy] docker compose up -d --build"
docker compose up -d --build

echo "[deploy] services"
docker compose ps

echo "[deploy] backend logs (last 80 lines)"
docker compose logs --tail=80 backend

echo "[deploy] done"
echo "frontend: http://<server-ip>:5173"
echo "backend docs: http://<server-ip>:18000/docs"
