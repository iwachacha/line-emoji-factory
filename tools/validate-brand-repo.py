#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import jsonschema
import yaml


PATH_KEYS = {
    "active_release_spec_path",
    "approval_log",
    "asset_validation_rules",
    "audit_report_path",
    "category_gap_map",
    "character_expression_matrix",
    "checklist",
    "checklist_path",
    "emoji_product_rules",
    "evaluation_model",
    "final_asset_dir",
    "handoff",
    "line_platform_baseline",
    "metadata_path",
    "observation_log",
    "production_brief_path",
    "prompt_bundle_dir",
    "quality_control_workflow",
    "quality_ledger_path",
    "reference_asset_register",
    "release_checklist_path",
    "release_log_path",
    "retrospective_path",
    "review_risk_rules",
    "spec",
    "structure_constraints",
    "style_bible",
    "submission_metadata_rules",
    "submission",
    "system_prompt_path",
    "tab_asset_dir",
    "tab_asset_path",
    "usage_validation_path",
    "usage_validation_workflow",
}


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc


def collect_paths(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in PATH_KEYS and isinstance(child, str):
                yield child
            else:
                yield from collect_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from collect_paths(child)


def validate_schema(manifest: dict, schema_path: Path, manifest_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{manifest_path}: {'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path))
    ]


def validate_paths(brand_repo: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in sorted(set(collect_paths(manifest))):
        target = brand_repo / rel_path
        if not target.exists():
            errors.append(f"manifest reference does not exist: {rel_path}")
    return errors


def selected_releases(manifest: dict, release_id: str | None) -> list[dict]:
    releases = manifest.get("releases", [])
    if release_id is None:
        return list(releases)
    return [release for release in releases if release.get("id") == release_id]


def validate_release_contracts(brand_repo: Path, manifest: dict, release_id: str | None) -> list[str]:
    errors: list[str] = []
    releases = selected_releases(manifest, release_id)
    if release_id and not releases:
        return [f"release id is not listed in manifest: {release_id}"]

    for release in releases:
        rid = release.get("id", "<unknown>")
        submission = brand_repo / str(release.get("submission", ""))
        metadata = submission / "metadata.yaml"
        if not submission.exists():
            errors.append(f"release {rid}: submission directory does not exist: {release.get('submission')}")
        elif not metadata.exists():
            errors.append(f"release {rid}: missing submission metadata: {metadata.relative_to(brand_repo).as_posix()}")

        release_root = brand_repo / "releases" / str(rid)
        for rel_dir in ("prompts", "production/finals", "production/tab", "qa"):
            target = release_root / rel_dir
            if not target.exists():
                errors.append(f"release {rid}: missing directory: {target.relative_to(brand_repo).as_posix()}")

    return errors


def run_validator(cmd: list[str], cwd: Path) -> list[str]:
    completed = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if completed.returncode == 0:
        return []
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part.strip())
    return [output.strip() or f"command failed: {' '.join(cmd)}"]


def validate_metadata_files(brand_repo: Path, manifest: dict, release_id: str | None, factory_root: Path) -> list[str]:
    errors: list[str] = []
    for release in selected_releases(manifest, release_id):
        rid = release.get("id", "<unknown>")
        metadata = brand_repo / str(release.get("submission", "")) / "metadata.yaml"
        if metadata.exists():
            errors.extend(
                f"release {rid}: {error}"
                for error in run_validator(
                    [sys.executable, str(factory_root / "tools" / "validate-metadata.py"), str(metadata)],
                    factory_root,
                )
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a manifest-driven LINE emoji brand repo.")
    parser.add_argument("brand_repo", type=Path)
    parser.add_argument("--release-id")
    parser.add_argument("--factory-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skip-placeholders", action="store_true")
    args = parser.parse_args()

    brand_repo = args.brand_repo.resolve()
    factory_root = args.factory_root.resolve()
    manifest_path = brand_repo / "brand-manifest.yaml"
    schema_path = factory_root / "schemas" / "brand-manifest.schema.json"

    errors: list[str] = []
    if not brand_repo.exists():
        print(f"Brand repo path does not exist: {brand_repo}", file=sys.stderr)
        return 1

    try:
        manifest = load_yaml(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError(f"{manifest_path}: manifest root must be an object")
        errors.extend(validate_schema(manifest, schema_path, manifest_path))
        errors.extend(validate_paths(brand_repo, manifest))
        errors.extend(validate_release_contracts(brand_repo, manifest, args.release_id))
        errors.extend(validate_metadata_files(brand_repo, manifest, args.release_id, factory_root))
    except ValueError as exc:
        errors.append(str(exc))

    if not args.skip_placeholders:
        placeholder_tool = factory_root / "tools" / "check-placeholders.py"
        errors.extend(run_validator([sys.executable, str(placeholder_tool), str(brand_repo)], factory_root))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"brand repo validation passed: {brand_repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
