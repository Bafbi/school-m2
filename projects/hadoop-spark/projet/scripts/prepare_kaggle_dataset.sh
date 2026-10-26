#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CURATED_DIR="${CURATED_DIR:-$ROOT_DIR/data/curated}"
RAW_DIR="${RAW_DIR:-$ROOT_DIR/data/raw/minestom}"
STAGING_DIR="${STAGING_DIR:-$ROOT_DIR/data/kaggle/minecraft-item-complexity-minestom}"
KAGGLE_SLUG="${KAGGLE_SLUG:-minecraft-item-complexity}"
KAGGLE_TITLE="${KAGGLE_TITLE:-Minecraft Item Complexity}"
KAGGLE_LICENSE="${KAGGLE_LICENSE:-CC0-1.0}"
MISE_JAVA_ALIAS="${MISE_JAVA_ALIAS:-spark}"

if [[ ! -d "$CURATED_DIR" ]]; then
  echo "Curated directory not found: $CURATED_DIR" >&2
  echo "Run: mise run ingest-data" >&2
  exit 1
fi

if [[ ! -f "$ROOT_DIR/kaggle.json" ]]; then
  echo "kaggle.json not found at project root: $ROOT_DIR/kaggle.json" >&2
  exit 1
fi

KAGGLE_USERNAME="$(python3 - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path("kaggle.json").read_text(encoding="utf-8"))
print(cfg.get("username", ""))
PY
)"

if [[ -z "$KAGGLE_USERNAME" ]]; then
  echo "Could not read username from kaggle.json" >&2
  exit 1
fi

DATASET_ID="${KAGGLE_DATASET_ID:-$KAGGLE_USERNAME/$KAGGLE_SLUG}"

mkdir -p "$STAGING_DIR"
rsync -a --delete "$CURATED_DIR/" "$STAGING_DIR/curated/"

if command -v uv >/dev/null 2>&1; then
  if command -v mise >/dev/null 2>&1; then
    mise exec "java@${MISE_JAVA_ALIAS}" -- uv run --project .. --python 3.12 python "$ROOT_DIR/scripts/generate_table_counts.py" \
      --curated-dir "$CURATED_DIR" \
      --output-csv "$STAGING_DIR/table_counts.csv"
  else
    uv run --project .. --python 3.12 python "$ROOT_DIR/scripts/generate_table_counts.py" \
      --curated-dir "$CURATED_DIR" \
      --output-csv "$STAGING_DIR/table_counts.csv"
  fi
else
  python3 "$ROOT_DIR/scripts/generate_table_counts.py" \
    --curated-dir "$CURATED_DIR" \
    --output-csv "$STAGING_DIR/table_counts.csv"
fi

if [[ -f "$RAW_DIR/_manifest.json" ]]; then
  cp "$RAW_DIR/_manifest.json" "$STAGING_DIR/minestom_manifest.json"
fi

cat > "$STAGING_DIR/README.md" <<EOF
# Minecraft Item Complexity Dataset (Minestom + Spark)

This dataset is generated from MinestomDataGenerator outputs and normalized with PySpark.

## Included content

- Curated parquet tables in ./curated
- Table-level summary in ./table_counts.csv
- Generation provenance manifest in ./minestom_manifest.json

## Core tables

- dim_item
- dim_block
- bridge_item_block
- dim_entity
- dim_dimension
- dim_biome
- tag_members_raw
- fact_loot_table
- fact_loot_entry
- fact_loot_condition
- fact_biome_feature
- fact_biome_spawner
- fact_ore_opportunity
- meta_manifest

## Notes

- Recipes are not fully represented in Minestom exports and require an additional source.
- Ore signal is a biome-feature proxy based on feature names containing "ore".
EOF

cat > "$STAGING_DIR/dataset-metadata.json" <<EOF
{
  "title": "$KAGGLE_TITLE",
  "id": "$DATASET_ID",
  "licenses": [
    {
      "name": "$KAGGLE_LICENSE"
    }
  ]
}
EOF

echo "Kaggle dataset staging prepared at: $STAGING_DIR"
echo "Dataset id: $DATASET_ID"
