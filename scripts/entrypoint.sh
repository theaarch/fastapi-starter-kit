#!/usr/bin/env bash
set -euo pipefail

echo "==> Running database migrations via Alembic..."
alembic upgrade head

echo "==> Starting application..."
exec "$@"
