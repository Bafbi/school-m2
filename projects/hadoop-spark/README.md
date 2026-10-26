# hadoop-spark — Minecraft item complexity analysis (Big Data)

M2 Big Data project. The question: how complex is a Minecraft item, really? The
pipeline builds a dataset out of the game's own registries and then explores it
with Spark.

## Pipeline

```
projet/scripts/generate_minestom_data.sh      Minestom fork → raw Minecraft JSON
projet/scripts/run_minestom_ingestion.py      JSON → normalised tables
projet/scripts/validate_curated_tables.py     checks on the curated schema
projet/data/curated/                          analysis-ready parquet (star schema:
                                              dim_item, dim_block, dim_biome, …
                                              fact_loot_entry, fact_ore_opportunity, …)
projet_spark.ipynb                            the analysis on top of it
```

`projet/README.md` documents the `mise run` entry points and the Java 25 / Java 21
split (generator vs Spark). `lab/` is the separate Hadoop-with-Docker lab
(`docker-compose.yml` + `hadoop.env`).

## Not in the repo

- `projet/data/raw/` — the raw Minestom dump, rebuilt by the scripts above.
- `projet/kaggle.json` — dataset-publishing credentials.

## Notes

- The curated parquet tables are committed so the notebook can be opened and run
  without rebuilding the whole generator chain first.
- `projet/projet_spark.ipynb` is a trimmed Colab export of the same analysis; the
  root notebook is the full one. The version handed in lives in
  [`../spark-project`](../spark-project).
