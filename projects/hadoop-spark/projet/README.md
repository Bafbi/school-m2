# Minecraft Dataset Generation (Minestom)

This project uses [MinestomDataGenerator](https://github.com/Minestom/MinestomDataGenerator) to generate raw Minecraft JSON data for Spark ingestion.

## Prerequisites

- Java 25
- Git
- Bash

Your workspace already declares tools in `mise.toml`:

- `java = "25"`
- `gradle = "9"`
- `python = "3.12"`

And Java aliases:

- `java@generator` -> Java 25 (for Minestom generator)
- `java@spark` -> Java 21 (for Spark ingestion)

## Generate data (one command)

```bash
mise run generate-data
```

Output is written to:

- `data/raw/minestom/`
- `data/raw/minestom/_manifest.json` (reproducibility metadata)

## Pinning and reproducibility

The generation source and revision are controlled by `minestom-generator.env`:

- `MINESTOM_REPO_URL`
- `MINESTOM_REF`

By default, `MINESTOM_REF` is pinned to a commit hash. Update it intentionally when you want to refresh to a newer dataset.

## Notes

- The Minestom generator requires EULA acceptance; the script runs with `-Peula=true`.
- The script mirrors generated files from Minestom `src/main/resources` into this project.

## Build curated Spark tables

After generating raw data, create normalized Parquet tables:

```bash
mise run ingest-data
```

Optional arguments:

- `--raw-dir data/raw/minestom`
- `--output-dir data/curated`

Direct script usage is also available:

- `./scripts/generate_minestom_data.sh`
- `./scripts/run_minestom_ingestion.sh`

To execute both in sequence:

```bash
mise run refresh-data
```

## Validate curated data (Phase 1)

Run a first-pass validation and quality profile on curated tables:

```bash
mise run validate-data
```

This produces:

- `data/curated/validation_profile.csv`

Included checks:

- table readability (`spark.read.parquet`)
- row count and column count
- overall null-cell percentage (`null_pct`)
- duplicate count on obvious identifier columns when present
- missing expected-table warnings

Current curated outputs:

- `meta_manifest`
- `dim_item`, `dim_block`, `bridge_item_block`, `dim_entity`, `dim_dimension`, `dim_biome`
- `tag_members_raw`
- `fact_loot_table`, `fact_loot_entry`, `fact_loot_condition`
- `fact_biome_feature`, `fact_biome_spawner`, `fact_ore_opportunity`

## Publish to Kaggle

The project includes a full staging + publish flow for Kaggle datasets.

### One-command release (recommended)

Run the full pipeline from generation to Kaggle publish:

```bash
mise run dataset-release
```

With a custom Kaggle version message:

```bash
mise run dataset-release-msg -- "Refresh from Minestom commit <hash>"
```

### 1) Prepare dataset staging

```bash
mise run kaggle-prepare
```

This creates:

- `data/kaggle/minecraft-item-complexity-minestom/curated/`
- `data/kaggle/minecraft-item-complexity-minestom/table_counts.csv`
- `data/kaggle/minecraft-item-complexity-minestom/minestom_manifest.json`
- `data/kaggle/minecraft-item-complexity-minestom/dataset-metadata.json`
- `data/kaggle/minecraft-item-complexity-minestom/README.md`

### 2) Publish (create or version)

```bash
mise run kaggle-publish
```

With a custom Kaggle version message:

```bash
mise run kaggle-publish-msg -- "Refresh from Minestom commit <hash>"
```

Behavior:

- If dataset does not exist: creates it.
- If dataset exists: uploads a new version.
- Curated tables are uploaded in Kaggle-compatible directory mode as `curated.zip`.
- `table_counts.csv` provides a quick, previewable summary on Kaggle's Data tab.

Requirements:

- `kaggle.json` at project root.
- Kaggle client installed in uv environment (`uv add kaggle`).

Optional environment variables:

- `KAGGLE_SLUG`
- `KAGGLE_TITLE`
- `KAGGLE_LICENSE`
- `VERSION_MESSAGE`
