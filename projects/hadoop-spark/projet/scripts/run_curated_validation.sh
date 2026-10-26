#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MISE_JAVA_ALIAS="${MISE_JAVA_ALIAS:-spark}"
UV_PYTHON_VERSION="${UV_PYTHON_VERSION:-3.12}"
CURATED_DIR="${CURATED_DIR:-$ROOT_DIR/data/curated}"
OUTPUT_CSV="${OUTPUT_CSV:-$ROOT_DIR/data/curated/validation_profile.csv}"
EXPECTED_TABLES="${EXPECTED_TABLES:-meta_manifest,dim_item,dim_block,bridge_item_block,dim_entity,dim_dimension,dim_biome,fact_biome_feature,fact_biome_spawner,fact_ore_opportunity,tag_members_raw,fact_loot_table,fact_loot_entry,fact_loot_condition}"

cd "$ROOT_DIR"

if [[ ! -d "$CURATED_DIR" ]]; then
  echo "Curated directory not found: $CURATED_DIR" >&2
  echo "Run: mise run ingest-data" >&2
  exit 1
fi

if command -v mise >/dev/null 2>&1; then
  mise exec "java@${MISE_JAVA_ALIAS}" -- uv run --project .. --python "$UV_PYTHON_VERSION" python ./scripts/validate_curated_tables.py \
    --curated-dir "$CURATED_DIR" \
    --output-csv "$OUTPUT_CSV" \
    --expected-tables "$EXPECTED_TABLES" \
    "$@"
else
  uv run --project .. --python "$UV_PYTHON_VERSION" python ./scripts/validate_curated_tables.py \
    --curated-dir "$CURATED_DIR" \
    --output-csv "$OUTPUT_CSV" \
    --expected-tables "$EXPECTED_TABLES" \
    "$@"
fi
