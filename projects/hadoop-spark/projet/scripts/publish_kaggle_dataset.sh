#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGING_DIR="${STAGING_DIR:-$ROOT_DIR/data/kaggle/minecraft-item-complexity-minestom}"
VERSION_MESSAGE="${VERSION_MESSAGE:-Update dataset from Minestom + Spark pipeline}"

if [[ ! -d "$STAGING_DIR" ]]; then
  echo "Staging directory not found: $STAGING_DIR" >&2
  echo "Run: ./scripts/prepare_kaggle_dataset.sh" >&2
  exit 1
fi

if [[ ! -f "$ROOT_DIR/kaggle.json" ]]; then
  echo "kaggle.json not found at project root" >&2
  exit 1
fi

if ! uv run --project .. python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('kaggle') else 1)" >/dev/null 2>&1; then
  echo "Kaggle python package not available in uv environment." >&2
  echo "Run: uv add kaggle" >&2
  exit 1
fi

if [[ ! -f "$STAGING_DIR/dataset-metadata.json" ]]; then
  echo "dataset-metadata.json not found in staging directory" >&2
  exit 1
fi

export STAGING_DIR

DATASET_ID="$(python3 - <<'PY'
import os
import json
from pathlib import Path
metadata_path = Path(os.environ["STAGING_DIR"]) / "dataset-metadata.json"
meta = json.loads(metadata_path.read_text(encoding="utf-8"))
print(meta.get("id", ""))
PY
)"

if [[ -z "$DATASET_ID" ]]; then
  echo "Dataset id missing in dataset-metadata.json" >&2
  exit 1
fi

TMP_KAGGLE_DIR="$ROOT_DIR/.cache/kaggle"
mkdir -p "$TMP_KAGGLE_DIR"
cp "$ROOT_DIR/kaggle.json" "$TMP_KAGGLE_DIR/kaggle.json"
chmod 600 "$TMP_KAGGLE_DIR/kaggle.json"

export KAGGLE_CONFIG_DIR="$TMP_KAGGLE_DIR"

if uv run --project .. kaggle datasets status "$DATASET_ID" >/dev/null 2>&1; then
  uv run --project .. kaggle datasets version -p "$STAGING_DIR" --dir-mode zip -m "$VERSION_MESSAGE"
else
  uv run --project .. kaggle datasets create -p "$STAGING_DIR" --dir-mode zip
fi

echo "Kaggle publish completed for: $DATASET_ID"
