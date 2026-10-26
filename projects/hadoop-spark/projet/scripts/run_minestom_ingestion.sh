#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MISE_JAVA_ALIAS="${MISE_JAVA_ALIAS:-spark}"
UV_PYTHON_VERSION="${UV_PYTHON_VERSION:-3.12}"

cd "$ROOT_DIR"

if command -v mise >/dev/null 2>&1; then
  mise exec "java@${MISE_JAVA_ALIAS}" -- uv run --project .. --python "$UV_PYTHON_VERSION" python ./scripts/run_minestom_ingestion.py "$@"
else
  uv run --project .. --python "$UV_PYTHON_VERSION" python ./scripts/run_minestom_ingestion.py "$@"
fi
