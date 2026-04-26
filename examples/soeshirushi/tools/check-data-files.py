#!/usr/bin/env python
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".venv", "__pycache__"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_files(suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in suffixes:
            files.append(path)
    return files


def check_yaml(errors: list[str]) -> None:
    for path in iter_files({".yaml", ".yml"}):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{rel(path)}: invalid YAML: {exc}")


def check_schema_json(errors: list[str]) -> None:
    for path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}: invalid JSON: {exc}")


def check_requirements(errors: list[str]) -> None:
    path = ROOT / "requirements-dev.txt"
    if not path.exists():
        errors.append("requirements-dev.txt: missing")
        return
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for line in lines:
        if line.startswith("#"):
            continue
        if len(line.split()) != 1 or "," in line or ";" in line:
            errors.append(f"requirements-dev.txt: expected one dependency per line, got {line}")


def main() -> int:
    errors: list[str] = []
    check_yaml(errors)
    check_schema_json(errors)
    check_requirements(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("data file check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
