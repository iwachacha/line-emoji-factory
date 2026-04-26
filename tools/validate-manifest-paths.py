#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


PATH_KEYS = {
    "active_series_plan_path",
    "asset_log",
    "observation_log",
    "category_gap_map",
    "character_data",
    "final_asset_dir",
    "prompt_bundle_dir",
    "release_checklist_path",
    "quality_ledger_path",
    "usage_validation_path",
    "retrospective_path",
    "release_log_path",
    "metadata_path",
    "images_dir",
    "line_upload_dir",
    "internal_archive_dir",
    "item_generation_workflow",
    "main_asset_dir",
    "main_asset_path",
    "checklist_path",
    "audit_report_path",
    "asset_validation_rules",
    "approval_log",
    "brand_canon_path",
    "brand_creation_rules",
    "brand_distillation_workflow",
    "brand_setting_path",
    "brand_positioning_path",
    "brand_taxonomy",
    "brief",
    "character_expression_matrix",
    "production_brief_path",
    "production_profile_rules",
    "production_pipeline_workflow",
    "product_catalog_path",
    "prompt_library",
    "item_seed_data",
    "system_prompt_path",
    "startup_brief_path",
    "set_architecture_workflow",
    "active_release_spec_path",
    "reference_asset_register",
    "style_bible",
    "line_platform_baseline",
    "structure_constraints",
    "emoji_product_rules",
    "sticker_product_rules",
    "review_risk_rules",
    "review_risk_keywords",
    "series_development_workflow",
    "series_plan",
    "evaluation_model",
    "visual_asset_quality_rules",
    "quality_control_workflow",
    "usage_validation_workflow",
    "submission_metadata_rules",
}


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate referenced paths in brand-manifest.yaml.")
    parser.add_argument("brand_repo", type=Path)
    args = parser.parse_args()

    brand_repo = args.brand_repo.resolve()
    manifest = brand_repo / "brand-manifest.yaml"
    if not manifest.exists():
        print(f"missing manifest: {manifest}", file=sys.stderr)
        return 1

    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    errors: list[str] = []
    for rel_path in sorted(set(collect_paths(data))):
        target = brand_repo / rel_path
        if not target.exists():
            errors.append(f"manifest reference does not exist: {rel_path}")

    for release in data.get("releases", []):
        for key in ("spec", "handoff", "checklist", "submission"):
            rel_path = release.get(key)
            if rel_path and not (brand_repo / rel_path).exists():
                errors.append(f"release {release.get('id')} {key} does not exist: {rel_path}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("manifest path validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
