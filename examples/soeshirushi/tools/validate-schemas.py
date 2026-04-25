#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml


def load_data(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def validate_one(schema_path: Path, data_path: Path) -> list[str]:
    errors: list[str] = []
    schema = load_data(schema_path)
    data = load_data(data_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{data_path}: {where}: {error.message}")
    return errors


def check_schemas(schema_dir: Path) -> list[str]:
    errors: list[str] = []
    for schema_path in sorted(schema_dir.glob("*.schema.json")):
        try:
            schema = load_data(schema_path)
            jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{schema_path}: invalid schema: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JSON/YAML data with JSON Schema.")
    parser.add_argument("--schema", type=Path, help="Schema file.")
    parser.add_argument("--data", type=Path, help="YAML or JSON data file.")
    parser.add_argument("--check-schemas", type=Path, help="Directory containing *.schema.json files.")
    args = parser.parse_args()

    errors: list[str] = []
    if args.check_schemas:
        errors.extend(check_schemas(args.check_schemas))
    elif args.schema and args.data:
        errors.extend(validate_one(args.schema, args.data))
    else:
        parser.error("Use --check-schemas or both --schema and --data.")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
