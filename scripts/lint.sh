#!/usr/bin/env bash
set -euo pipefail

# Navigate to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

MODE="${1:-check}"

if [ "$MODE" = "--fix" ] || [ "$MODE" = "fix" ]; then
    echo "==> Auto-fixing lint issues and formatting code..."
    uv run ruff check --fix .
    uv run ruff format .
    echo "==> Code formatting and fixes applied successfully!"
else
    echo "==> Running Ruff lint checks..."
    uv run ruff check .
    echo "==> Running Ruff format checks..."
    uv run ruff format --check .
    echo "==> All lint and format checks passed!"
fi
