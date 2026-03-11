#!/usr/bin/env sh
set -e

echo "[start] running alembic upgrade head..."
alembic -c /app/alembic.ini upgrade head

echo "[start] starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
