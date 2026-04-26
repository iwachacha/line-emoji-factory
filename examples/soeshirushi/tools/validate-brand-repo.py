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
    "active_series_plan_path",
    "approval_log",
    "asset_log",
    "asset_validation_rules",
    "audit_report_path",
    "brand_canon_path",
    "brand_creation_rules",
    "brand_distillation_workflow",
    "category_gap_map",
    "character_data",
    "character_expression_matrix",
    "checklist",
    "checklist_path",
    "emoji_product_rules",
    "evaluation_model",
    "final_asset_dir",
    "handoff",
    "item_generation_workflow",
    "line_platform_baseline",
    "line_upload_dir",
    "main_asset_dir",
    "main_asset_path",
    "metadata_path",
    "observation_log",
    "production_brief_path",
    "prompt_bundle_dir",
    "production_profile_rules",
    "production_pipeline_workflow",
    "product_catalog_path",
    "quality_control_workflow",
    "quality_ledger_path",
    "reference_asset_register",
    "release_checklist_path",
    "release_log_path",
    "retrospective_path",
    "review_risk_keywords",
    "review_risk_rules",
    "series_development_workflow",
    "series_plan",
    "spec",
    "structure_constraints",
    "sticker_product_rules",
    "style_bible",
    "submission_metadata_rules",
    "submission",
    "system_prompt_path",
    "tab_asset_dir",
    "tab_asset_path",
    "internal_archive_dir",
    "item_seed_data",
    "usage_validation_path",
    "usage_validation_workflow",
    "visual_asset_quality_rules",
    "brand_taxonomy",
    "brief",
    "startup_brief_path",
    "prompt_library",
    "set_architecture_workflow",
}

STANDARD_PRODUCTION_PROFILE_OUTPUTS = {
    "brand_canon_stage": {"brand_canon", "ip_guardrails", "allowed_variations", "prohibited_drift"},
    "series_planning_stage": {
        "product_catalog_review",
        "series_plan",
        "inheritance_points",
        "novelty_points",
        "cannibalization_notes",
    },
    "rough_stage": {"style_anchor", "character_anchor", "rough_board", "failure_notes"},
    "item_finalization_stage": {
        "item_specs",
        "four_candidate_minimum",
        "candidate_comparison",
        "final_assets",
        "correction_notes",
        "export_check",
    },
    "product_qa_stage": {
        "contact_sheet",
        "chat_preview",
        "asset_validation_report",
        "duplicate_and_usage_overlap_notes",
        "unresolved_watch_items",
    },
    "release_ledger_stage": {
        "release_log_update",
        "quality_ledger_update",
        "product_catalog_update",
        "next_series_watch",
    },
    "revision_stage": {"revision_notes", "fixed_assets", "unresolved_watch_items"},
}
ROUGH_INTENT_OUTPUTS = {"per_item_intent", "per_emoji_intent"}
STANDARD_STARTUP_PROFILE_OUTPUTS = {
    "structure_gate_stage": {"structure_judgment", "item_type_hypothesis", "transformation_notes"},
    "brand_core_stage": {"brand_setting", "brand_canon", "brand_positioning"},
    "product_seed_stage": {"product_hypothesis", "first_series_seed", "expansion_queue"},
    "prompt_seed_stage": {"prompt_library", "negative_prompt", "variable_boundaries"},
    "handoff_stage": {"owner_files", "next_actions", "unresolved_watch"},
}
ITEM_PACKAGE_TYPES = {
    "static-emoji": "emoji",
    "animation-emoji": "emoji",
    "static-sticker": "sticker",
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
        item_type = str(release.get("item_type") or manifest.get("product", {}).get("item_type", "static-emoji"))
        submission_path = release.get("submission")
        if submission_path:
            submission = brand_repo / str(submission_path)
            metadata = submission / "metadata.yaml"
            if not submission.exists():
                errors.append(f"release {rid}: submission directory does not exist: {release.get('submission')}")
            elif not metadata.exists():
                errors.append(f"release {rid}: missing submission metadata: {metadata.relative_to(brand_repo).as_posix()}")

        release_root = brand_repo / "releases" / str(rid)
        for rel_dir in ("prompts", "production/finals", "production/tab"):
            target = release_root / rel_dir
            if not target.exists():
                errors.append(f"release {rid}: missing directory: {target.relative_to(brand_repo).as_posix()}")
        if item_type == "static-sticker":
            target = release_root / "production/main"
            if not target.exists():
                errors.append(f"release {rid}: missing directory: {target.relative_to(brand_repo).as_posix()}")

    return errors


def validate_product_contract(manifest: dict) -> list[str]:
    errors: list[str] = []
    product = manifest.get("product", {})
    product_item_type = str(product.get("item_type", ""))
    product_package_type = str(product.get("package_type", ""))
    supported = product.get("supported_item_types", [])
    if product_item_type in ITEM_PACKAGE_TYPES and product_package_type != ITEM_PACKAGE_TYPES[product_item_type]:
        errors.append(
            f"product.package_type must match product.item_type: {product_package_type} != {ITEM_PACKAGE_TYPES[product_item_type]}"
        )
    if supported and product_item_type and product_item_type not in supported:
        errors.append("product.item_type must be listed in product.supported_item_types")

    for release in manifest.get("releases", []):
        rid = release.get("id", "<unknown>")
        item_type = str(release.get("item_type") or product_item_type)
        package_type = str(release.get("package_type") or product_package_type)
        if supported and item_type not in supported:
            errors.append(f"release {rid}: item_type {item_type} is not listed in product.supported_item_types")
        expected_package = ITEM_PACKAGE_TYPES.get(item_type)
        if expected_package and package_type != expected_package:
            errors.append(f"release {rid}: package_type must match item_type: {package_type} != {expected_package}")
    return errors


def validate_production_profile_contract(manifest: dict) -> list[str]:
    errors: list[str] = []
    production_profile = manifest.get("production_profile", {})
    if not production_profile:
        return errors
    profile_name = production_profile.get("name")
    production_name = manifest.get("production", {}).get("profile")
    if profile_name and production_name and profile_name != production_name:
        errors.append(
            f"production.profile must match production_profile.name: {production_name} != {profile_name}"
        )

    for stage_name, required_outputs in STANDARD_PRODUCTION_PROFILE_OUTPUTS.items():
        outputs = set(production_profile.get(stage_name, {}).get("required_outputs", []))
        missing = sorted(required_outputs - outputs)
        if missing:
            errors.append(f"production_profile.{stage_name}: missing required outputs: {', '.join(missing)}")
    rough_outputs = set(production_profile.get("rough_stage", {}).get("required_outputs", []))
    if not (rough_outputs & ROUGH_INTENT_OUTPUTS):
        errors.append("production_profile.rough_stage: missing required output: per_item_intent")
    return errors


def validate_startup_profile_contract(manifest: dict) -> list[str]:
    errors: list[str] = []
    startup_profile = manifest.get("startup_profile", {})
    for stage_name, required_outputs in STANDARD_STARTUP_PROFILE_OUTPUTS.items():
        outputs = set(startup_profile.get(stage_name, {}).get("required_outputs", []))
        missing = sorted(required_outputs - outputs)
        if missing:
            errors.append(f"startup_profile.{stage_name}: missing required outputs: {', '.join(missing)}")
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
        submission = release.get("submission")
        if not submission:
            continue
        metadata = brand_repo / str(submission) / "metadata.yaml"
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
    parser = argparse.ArgumentParser(description="Validate a manifest-driven LINE emoji or sticker brand repo.")
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
        errors.extend(validate_product_contract(manifest))
        errors.extend(validate_startup_profile_contract(manifest))
        errors.extend(validate_production_profile_contract(manifest))
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
