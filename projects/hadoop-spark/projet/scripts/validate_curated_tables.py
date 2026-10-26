#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate curated parquet tables and compute a lightweight quality profile")
    parser.add_argument("--curated-dir", default="data/curated", help="Directory containing curated parquet table folders")
    parser.add_argument("--output-csv", default="", help="Optional path to write validation results as CSV")
    parser.add_argument("--app-name", default="CuratedDataValidation", help="Spark application name")
    parser.add_argument("--show", type=int, default=3, help="Number of sample rows to show for each sample table")
    parser.add_argument(
        "--expected-tables",
        default="",
        help="Comma-separated expected table names. Missing tables are reported as warnings.",
    )
    return parser.parse_args()


def list_table_dirs(curated_dir: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in curated_dir.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        ],
        key=lambda path: path.name,
    )


def find_duplicate_key(columns: list[str]) -> str:
    preferred = [
        "item_id",
        "block_id",
        "entity_id",
        "dimension_id",
        "biome_id",
        "entry_id",
        "table_id",
        "tag_id",
    ]
    for key in preferred:
        if key in columns:
            return key

    for column in columns:
        if column.endswith("_id"):
            return column

    return ""


def compute_null_profile(dataframe) -> tuple[int, int, float]:
    from pyspark.sql import functions as F

    row_count = dataframe.count()
    column_count = len(dataframe.columns)

    if row_count == 0 or column_count == 0:
        return row_count, column_count, 0.0

    null_exprs = [F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias(column) for column in dataframe.columns]
    null_totals = dataframe.agg(*null_exprs).collect()[0].asDict()
    total_null_cells = int(sum(int(value or 0) for value in null_totals.values()))
    total_cells = row_count * column_count
    null_pct = (total_null_cells / total_cells) * 100 if total_cells else 0.0
    return row_count, column_count, round(null_pct, 4)


def validate_table(spark, table_dir: Path) -> tuple[dict[str, object], object]:
    dataframe = spark.read.parquet(str(table_dir))
    row_count, column_count, null_pct = compute_null_profile(dataframe)

    duplicate_key = find_duplicate_key(dataframe.columns)
    duplicate_count = ""
    if duplicate_key and row_count > 0:
        distinct_count = dataframe.select(duplicate_key).distinct().count()
        duplicate_count = row_count - distinct_count

    return (
        {
            "table_name": table_dir.name,
            "status": "ok",
            "row_count": row_count,
            "column_count": column_count,
            "null_pct": null_pct,
            "duplicate_key": duplicate_key,
            "duplicate_count": duplicate_count,
            "note": "",
        },
        dataframe,
    )


def write_csv(output_csv: Path, rows: list[dict[str, object]]) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "table_name",
                "status",
                "row_count",
                "column_count",
                "null_pct",
                "duplicate_key",
                "duplicate_count",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, object]]) -> None:
    ok_rows = [row for row in rows if row["status"] == "ok"]
    warning_rows = [row for row in rows if row["status"] == "warning"]
    failed_rows = [row for row in rows if row["status"] == "error"]

    print(f"Tables discovered: {len(rows)}")
    print(f"Readable tables: {len(ok_rows)}")
    print(f"Warnings: {len(warning_rows)}")
    print(f"Failed tables: {len(failed_rows)}")

    if failed_rows:
        print("\nFailed tables:")
        for row in failed_rows:
            print(f"- {row['table_name']}: {row['note']}")


def show_samples(rows: list[dict[str, object]], tables: dict[str, object], show: int) -> None:
    samples = ["meta_manifest", "dim_item", "fact_loot_entry"]
    for table_name in samples:
        if table_name not in tables:
            continue
        print(f"\n=== {table_name} (show {show}) ===")
        tables[table_name].show(show, truncate=False)


def add_missing_table_rows(rows: list[dict[str, object]], expected_tables: list[str]) -> None:
    if not expected_tables:
        return

    present = {str(row["table_name"]) for row in rows}
    for table_name in expected_tables:
        if table_name in present:
            continue
        rows.append(
            {
                "table_name": table_name,
                "status": "warning",
                "row_count": "",
                "column_count": "",
                "null_pct": "",
                "duplicate_key": "",
                "duplicate_count": "",
                "note": "missing_table",
            }
        )


def main() -> None:
    args = parse_args()
    curated_dir = Path(args.curated_dir)

    if not curated_dir.exists() or not curated_dir.is_dir():
        raise SystemExit(f"Curated directory not found: {curated_dir}")

    table_dirs = list_table_dirs(curated_dir)
    if not table_dirs:
        raise SystemExit(f"No curated table directories found in: {curated_dir}")

    expected_tables = [name.strip() for name in args.expected_tables.split(",") if name.strip()]

    try:
        from pyspark.sql import SparkSession
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Missing dependency: pyspark. Install it with `pip install pyspark` "
            "or run this script from a notebook/kernel where PySpark is already available."
        ) from error

    spark = SparkSession.builder.appName(args.app_name).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    rows: list[dict[str, object]] = []
    loaded_tables: dict[str, object] = {}

    try:
        for table_dir in table_dirs:
            try:
                result, dataframe = validate_table(spark, table_dir)
                rows.append(result)
                loaded_tables[table_dir.name] = dataframe
            except Exception as error:
                rows.append(
                    {
                        "table_name": table_dir.name,
                        "status": "error",
                        "row_count": "",
                        "column_count": "",
                        "null_pct": "",
                        "duplicate_key": "",
                        "duplicate_count": "",
                        "note": f"{error.__class__.__name__}: {error}",
                    }
                )

        add_missing_table_rows(rows, expected_tables)
    finally:
        print_summary(rows)
        show_samples(rows, loaded_tables, args.show)
        if args.output_csv:
            write_csv(Path(args.output_csv), rows)
            print(f"\nValidation CSV written to: {args.output_csv}")
        spark.stop()


if __name__ == "__main__":
    main()
