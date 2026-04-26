#!/usr/bin/env python
from __future__ import annotations

import argparse
import filecmp
import sys
from pathlib import Path

import yaml


STANDALONE_TOOL_FILES = [
    "tools/validate-schemas.py",
    "tools/validate-assets.py",
    "tools/validate-metadata.py",
    "tools/check-source-integrity.py",
    "tools/check-data-files.py",
    "tools/check-canonical-drift.py",
    "tools/check-placeholders.py",
    "tools/validate-manifest-paths.py",
    "tools/package-release.py",
    "tools/sync-shared-snapshots.ps1",
]
STANDALONE_SHARED_FILES = {
    "rules/review-risk-keywords.yaml": "references/shared/review-risk-keywords.yaml",
}


def load_manifest(example: Path) -> dict:
    manifest_path = example / "brand-manifest.yaml"
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing manifest: {manifest_path}") from None
    if not isinstance(data, dict):
        raise ValueError(f"{manifest_path}: manifest root must be an object")
    return data


def compare_file(factory_root: Path, example: Path, rel_path: str) -> list[str]:
    source = factory_root / rel_path
    target = example / rel_path
    if not source.exists():
        return [f"factory source missing: {rel_path}"]
    if not target.exists():
        return [f"example copy missing: {rel_path}"]
    if not filecmp.cmp(source, target, shallow=False):
        return [f"example copy drifted: {rel_path}"]
    return []


def compare_schemas(factory_root: Path, example: Path) -> list[str]:
    errors: list[str] = []
    for schema in sorted((factory_root / "schemas").glob("*.schema.json")):
        rel_path = schema.relative_to(factory_root).as_posix()
        errors.extend(compare_file(factory_root, example, rel_path))
    return errors


def compare_tools(factory_root: Path, example: Path) -> list[str]:
    errors: list[str] = []
    for rel_path in STANDALONE_TOOL_FILES:
        errors.extend(compare_file(factory_root, example, rel_path))
    return errors


def compare_shared_files(factory_root: Path, example: Path) -> list[str]:
    errors: list[str] = []
    for source_rel, target_rel in STANDALONE_SHARED_FILES.items():
        source = factory_root / source_rel
        target = example / target_rel
        if not source.exists():
            errors.append(f"factory source missing: {source_rel}")
            continue
        if not target.exists():
            errors.append(f"example shared copy missing: {target_rel}")
            continue
        if not filecmp.cmp(source, target, shallow=False):
            errors.append(f"example shared copy drifted: {target_rel}")
    return errors


def snapshot_source(factory_root: Path, snapshot_rel_path: str) -> Path | None:
    filename = Path(snapshot_rel_path).name
    for root_rel in ("rules", "workflows"):
        candidate = factory_root / root_rel / filename
        if candidate.exists():
            return candidate
    return None


def compare_manifest_snapshots(factory_root: Path, example: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    snapshots = manifest.get("snapshots", {})
    if not isinstance(snapshots, dict):
        return ["brand-manifest.yaml: snapshots must be an object"]

    for key, rel_path in sorted(snapshots.items()):
        if not isinstance(rel_path, str):
            errors.append(f"brand-manifest.yaml: snapshots.{key} must be a path string")
            continue
        source = snapshot_source(factory_root, rel_path)
        target = example / rel_path
        if source is None:
            errors.append(f"snapshot source missing for snapshots.{key}: {rel_path}")
            continue
        if not target.exists():
            errors.append(f"example snapshot missing: {rel_path}")
            continue
        if not filecmp.cmp(source, target, shallow=False):
            errors.append(f"example snapshot drifted: {rel_path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that a standalone example brand repo is not stale.")
    parser.add_argument("example", type=Path)
    parser.add_argument("--factory-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    factory_root = args.factory_root.resolve()
    example = args.example.resolve()
    errors: list[str] = []

    if not example.exists():
        print(f"example path does not exist: {example}", file=sys.stderr)
        return 1

    try:
        manifest = load_manifest(example)
        errors.extend(compare_schemas(factory_root, example))
        errors.extend(compare_tools(factory_root, example))
        errors.extend(compare_shared_files(factory_root, example))
        errors.extend(compare_manifest_snapshots(factory_root, example, manifest))
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"example drift check passed: {example}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
