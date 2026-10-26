#!/usr/bin/env python3
import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

try:
    from pyspark.sql import SparkSession
except ModuleNotFoundError as error:
    raise SystemExit(
        "Missing dependency: pyspark. Install it with `pip install pyspark` "
        "or run this script from a notebook/kernel where PySpark is already available."
    ) from error


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_parquet(spark: SparkSession, rows: list[dict], output_dir: Path, table_name: str) -> None:
    target = output_dir / table_name
    if rows:
        temp_dir = output_dir / ".tmp_jsonl"
        temp_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", delete=False, dir=temp_dir, suffix=f"_{table_name}.jsonl", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            temp_file = Path(handle.name)

        try:
            spark.read.json(str(temp_file)).write.mode("overwrite").parquet(str(target))
        finally:
            if temp_file.exists():
                temp_file.unlink()
    else:
        spark.createDataFrame([], "id string").limit(0).write.mode("overwrite").parquet(str(target))


def normalize_items(item_map: dict[str, dict]) -> list[dict]:
    def component_value(payload: dict, component_key: str) -> Any:
        components = payload.get("components")
        if not isinstance(components, dict):
            return None

        value = components.get(component_key)
        if isinstance(value, dict) and "value" in value:
            return value.get("value")
        return value

    def is_fire_resistant(payload: dict) -> bool:
        components = payload.get("components")
        if not isinstance(components, dict):
            return False

        damage_resistant = components.get("minecraft:damage_resistant")
        if not isinstance(damage_resistant, dict):
            return False

        damage_types = damage_resistant.get("types")
        if isinstance(damage_types, str):
            return damage_types == "#minecraft:is_fire"
        if isinstance(damage_types, list):
            return "#minecraft:is_fire" in damage_types
        return False

    rows = []
    for item_id, payload in item_map.items():
        rows.append(
            {
                "item_id": item_id,
                "numeric_id": payload.get("id"),
                "translation_key": payload.get("translationKey"),
                "max_stack_size": component_value(payload, "minecraft:max_stack_size"),
                "max_damage": component_value(payload, "minecraft:max_damage"),
                "is_fire_resistant": is_fire_resistant(payload),
                "is_enchantable": component_value(payload, "minecraft:enchantable"),
                "corresponding_block_id": payload.get("correspondingBlock"),
            }
        )
    return rows


def normalize_blocks(block_map: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    block_rows = []
    bridge_rows = []
    for block_id, payload in block_map.items():
        corresponding_item = payload.get("correspondingItem")
        block_rows.append(
            {
                "block_id": block_id,
                "numeric_id": payload.get("id"),
                "hardness": payload.get("hardness"),
                "explosion_resistance": payload.get("explosionResistance"),
                "friction": payload.get("friction"),
                "is_air": payload.get("air", False),
                "is_solid": payload.get("solid"),
                "corresponding_item_id": corresponding_item,
            }
        )
        if corresponding_item:
            bridge_rows.append(
                {
                    "item_id": corresponding_item,
                    "block_id": block_id,
                }
            )
    return block_rows, bridge_rows


def normalize_entity_types(entity_map: dict[str, dict]) -> list[dict]:
    rows = []
    for entity_id, payload in entity_map.items():
        rows.append(
            {
                "entity_id": entity_id,
                "numeric_id": payload.get("id"),
                "width": payload.get("width"),
                "height": payload.get("height"),
                "eye_height": payload.get("eyeHeight"),
                "category": payload.get("category"),
                "is_fire_immune": payload.get("fireImmune", False),
            }
        )
    return rows


def normalize_dimensions(dimension_map: dict[str, dict]) -> list[dict]:
    rows = []
    for dimension_id, payload in dimension_map.items():
        rows.append(
            {
                "dimension_id": dimension_id,
                "min_y": payload.get("min_y"),
                "height": payload.get("height"),
                "logical_height": payload.get("logical_height"),
                "coordinate_scale": payload.get("coordinate_scale"),
                "is_ultrawarm": payload.get("ultrawarm"),
                "is_natural": payload.get("natural"),
                "has_skylight": payload.get("has_skylight"),
                "has_ceiling": payload.get("has_ceiling"),
                "bed_works": payload.get("attributes", {}).get("minecraft:gameplay/bed_rule", {}).get("can_sleep") == "always"
                if isinstance(payload.get("attributes"), dict)
                else None,
                "respawn_anchor_works": payload.get("attributes", {}).get("minecraft:gameplay/respawn_anchor_works")
                if isinstance(payload.get("attributes"), dict)
                else None,
            }
        )
    return rows


def normalize_biomes(biome_map: dict[str, dict]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    biome_rows: list[dict] = []
    feature_rows: list[dict] = []
    spawner_rows: list[dict] = []
    ore_rows: list[dict] = []

    for biome_id, payload in biome_map.items():
        biome_rows.append(
            {
                "biome_id": biome_id,
                "temperature": payload.get("temperature"),
                "downfall": payload.get("downfall"),
                "has_precipitation": payload.get("hasPrecipitation"),
                "temperature_modifier": payload.get("temperatureModifier"),
                "category": payload.get("category"),
            }
        )

        features = payload.get("features", [])
        if isinstance(features, list):
            for step_index, step_features in enumerate(features):
                if not isinstance(step_features, list):
                    continue
                for feature_name in step_features:
                    feature_rows.append(
                        {
                            "biome_id": biome_id,
                            "step_index": step_index,
                            "feature_name": feature_name,
                        }
                    )
                    lowered = str(feature_name).lower()
                    if "ore" in lowered:
                        ore_rows.append(
                            {
                                "biome_id": biome_id,
                                "feature_name": feature_name,
                                "ore_signal": 1,
                            }
                        )

        spawners = payload.get("spawners", {})
        if isinstance(spawners, dict):
            for spawn_group, entries in spawners.items():
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    spawner_rows.append(
                        {
                            "biome_id": biome_id,
                            "spawn_group": spawn_group,
                            "entity_id": entry.get("type"),
                            "weight": entry.get("weight"),
                            "min_count": entry.get("minCount"),
                            "max_count": entry.get("maxCount"),
                        }
                    )

    return biome_rows, feature_rows, spawner_rows, ore_rows


def normalize_tags(tag_domain: str, tag_map: dict[str, dict]) -> list[dict]:
    rows = []
    for tag_id, payload in tag_map.items():
        values = payload.get("values", [])
        if not isinstance(values, list):
            continue
        for value in values:
            value_str = str(value)
            is_tag_reference = value_str.startswith("#")
            rows.append(
                {
                    "tag_domain": tag_domain,
                    "tag_id": tag_id,
                    "member_ref": value_str,
                    "member_id": value_str[1:] if is_tag_reference else value_str,
                    "is_tag_reference": is_tag_reference,
                }
            )
    return rows


def flatten_loot_tables(source_name: str, loot_map: dict[str, dict]) -> tuple[list[dict], list[dict], list[dict]]:
    table_rows: list[dict] = []
    entry_rows: list[dict] = []
    condition_rows: list[dict] = []

    for table_id, table_payload in loot_map.items():
        loot_type = table_payload.get("type")
        pools = table_payload.get("pools", [])
        table_rows.append(
            {
                "source_name": source_name,
                "table_id": table_id,
                "loot_type": loot_type,
                "pool_count": len(pools) if isinstance(pools, list) else 0,
            }
        )

        if not isinstance(pools, list):
            continue

        for pool_index, pool in enumerate(pools):
            entries = pool.get("entries", []) if isinstance(pool, dict) else []
            if not isinstance(entries, list):
                continue

            for entry_index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    continue

                entry_id = f"{source_name}:{table_id}:{pool_index}:{entry_index}"
                entry_name = entry.get("name")
                entry_rows.append(
                    {
                        "entry_id": entry_id,
                        "source_name": source_name,
                        "table_id": table_id,
                        "pool_index": pool_index,
                        "entry_index": entry_index,
                        "entry_type": entry.get("type"),
                        "entry_name": entry_name,
                        "weight": entry.get("weight"),
                        "quality": entry.get("quality"),
                        "item_id": entry_name if isinstance(entry_name, str) and entry_name.startswith("minecraft:") else None,
                    }
                )

                conditions = entry.get("conditions", [])
                if isinstance(conditions, list):
                    for condition_index, condition in enumerate(conditions):
                        condition_rows.append(
                            {
                                "entry_id": entry_id,
                                "condition_index": condition_index,
                                "condition_json": json.dumps(condition, ensure_ascii=False),
                            }
                        )

    return table_rows, entry_rows, condition_rows


def normalize_manifest(manifest_data: dict[str, Any]) -> list[dict]:
    return [manifest_data]


def build_curated_tables(raw_dir: Path, output_dir: Path, spark: SparkSession) -> None:
    item_map = read_json(raw_dir / "item.json")
    block_map = read_json(raw_dir / "block.json")
    entity_map = read_json(raw_dir / "entity_type.json")
    dimension_map = read_json(raw_dir / "dimension_type.json")
    biome_map = read_json(raw_dir / "worldgen" / "biome.json")
    tag_item_map = read_json(raw_dir / "tags" / "item.json")
    tag_block_map = read_json(raw_dir / "tags" / "block.json")
    manifest_data = read_json(raw_dir / "_manifest.json")

    output_dir.mkdir(parents=True, exist_ok=True)

    dim_item = normalize_items(item_map)
    dim_block, bridge_item_block = normalize_blocks(block_map)
    dim_entity = normalize_entity_types(entity_map)
    dim_dimension = normalize_dimensions(dimension_map)
    dim_biome, fact_biome_feature, fact_biome_spawner, fact_ore_opportunity = normalize_biomes(biome_map)
    tag_members_raw = normalize_tags("item", tag_item_map) + normalize_tags("block", tag_block_map)

    loot_files = {
        "block": raw_dir / "loot_tables" / "block_loot_tables.json",
        "chest": raw_dir / "loot_tables" / "chest_loot_tables.json",
        "entity": raw_dir / "loot_tables" / "entity_loot_tables.json",
        "gameplay": raw_dir / "loot_tables" / "gameplay_loot_tables.json",
    }

    fact_loot_table: list[dict] = []
    fact_loot_entry: list[dict] = []
    fact_loot_condition: list[dict] = []

    for source_name, loot_path in loot_files.items():
        loot_map = read_json(loot_path)
        table_rows, entry_rows, condition_rows = flatten_loot_tables(source_name, loot_map)
        fact_loot_table.extend(table_rows)
        fact_loot_entry.extend(entry_rows)
        fact_loot_condition.extend(condition_rows)

    write_parquet(spark, normalize_manifest(manifest_data), output_dir, "meta_manifest")
    write_parquet(spark, dim_item, output_dir, "dim_item")
    write_parquet(spark, dim_block, output_dir, "dim_block")
    write_parquet(spark, bridge_item_block, output_dir, "bridge_item_block")
    write_parquet(spark, dim_entity, output_dir, "dim_entity")
    write_parquet(spark, dim_dimension, output_dir, "dim_dimension")
    write_parquet(spark, dim_biome, output_dir, "dim_biome")
    write_parquet(spark, fact_biome_feature, output_dir, "fact_biome_feature")
    write_parquet(spark, fact_biome_spawner, output_dir, "fact_biome_spawner")
    write_parquet(spark, fact_ore_opportunity, output_dir, "fact_ore_opportunity")
    write_parquet(spark, tag_members_raw, output_dir, "tag_members_raw")
    write_parquet(spark, fact_loot_table, output_dir, "fact_loot_table")
    write_parquet(spark, fact_loot_entry, output_dir, "fact_loot_entry")
    write_parquet(spark, fact_loot_condition, output_dir, "fact_loot_condition")
    shutil.rmtree(output_dir / ".tmp_jsonl", ignore_errors=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build curated parquet tables from Minestom raw dataset")
    parser.add_argument("--raw-dir", default="data/raw/minestom", help="Directory containing Minestom raw JSON files")
    parser.add_argument("--output-dir", default="data/curated", help="Directory where curated parquet tables will be written")
    parser.add_argument("--app-name", default="MinestomIngestion", help="Spark application name")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)

    spark = SparkSession.builder.appName(args.app_name).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    try:
        build_curated_tables(raw_dir=raw_dir, output_dir=output_dir, spark=spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
