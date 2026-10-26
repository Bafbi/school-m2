#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate CSV summary for curated parquet tables")
    parser.add_argument("--curated-dir", required=True, help="Directory containing curated parquet table folders")
    parser.add_argument("--output-csv", required=True, help="Output CSV path")
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


def write_fallback(output_csv: Path, table_dirs: list[Path], note: str) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["table_name", "row_count", "column_count", "note"])
        for table_dir in table_dirs:
            writer.writerow([table_dir.name, "", "", note])


def main() -> None:
    args = parse_args()
    curated_dir = Path(args.curated_dir)
    output_csv = Path(args.output_csv)

    if not curated_dir.exists() or not curated_dir.is_dir():
        raise SystemExit(f"Curated directory not found: {curated_dir}")

    table_dirs = list_table_dirs(curated_dir)

    try:
        from pyspark.sql import SparkSession
    except ModuleNotFoundError:
        write_fallback(output_csv, table_dirs, "pyspark not available")
        return

    spark = (
        SparkSession.builder.appName("CuratedTableSummary")
        .master("local[1]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    rows: list[tuple[str, int | str, int | str, str]] = []
    try:
        for table_dir in table_dirs:
            try:
                dataframe = spark.read.parquet(str(table_dir))
                rows.append((table_dir.name, dataframe.count(), len(dataframe.columns), ""))
            except Exception as error:
                rows.append((table_dir.name, "", "", f"read_error: {error.__class__.__name__}"))
    finally:
        spark.stop()

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["table_name", "row_count", "column_count", "note"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
