from __future__ import annotations

import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_cmd_args(*args: str | Path) -> list[str]:
    return [str(arg) for arg in args]


def write_png(path: Path, size: tuple[int, int], *, fully_transparent: bool = False, alpha: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "RGBA" if alpha else "RGB"
    background = (0, 0, 0, 0) if alpha else (255, 255, 255)
    image = Image.new(mode, size, background)
    if not fully_transparent:
        draw = ImageDraw.Draw(image)
        fill = (30, 30, 30, 255) if alpha else (30, 30, 30)
        draw.ellipse((24, 24, size[0] - 24, size[1] - 24), fill=fill)
    image.save(path, dpi=(72, 72))


def valid_metadata() -> dict:
    return {
        "schema_version": "1.0",
        "locale": "ja",
        "creator_name": "Test Creator",
        "title": "Test Emoji",
        "description": "Small reactions for testing.",
        "copyright": "Test Creator",
        "suggest_tags": ["test"],
    }


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def create_brand_repo(
    root: Path,
    *,
    release_id: str = "release-001",
    count: int = 8,
    brand_type: str = "generic",
    with_assets: bool = False,
    with_tab: bool = True,
) -> Path:
    brand = root / "brand"
    release = brand / "releases" / release_id
    paths = [
        brand / "brand",
        brand / "brand" / "ip",
        brand / "market",
        brand / "references" / "shared",
        release / "prompts",
        release / "production" / "finals",
        release / "production" / "tab",
        release / "qa",
        release / "submission",
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

    files = [
        "brand/brand-setting.md",
        "brand/brand-positioning.md",
        "brand/brand-production-brief.md",
        "brand/brand-system-prompt.md",
        "brand/ip/ip-style-bible.md",
        "brand/ip/reference-asset-register.md",
        "brand/ip/ip-approval-log.md",
        "brand/ip/character-expression-matrix.md",
        "market/market-observation-log.md",
        "market/category-gap-map.md",
        "references/shared/line-platform-baseline.md",
        "references/shared/structure-constraints.md",
        "references/shared/emoji-product-rules.md",
        "references/shared/review-risk-rules.md",
        "references/shared/evaluation-model.md",
        "references/shared/quality-control-workflow.md",
        "references/shared/usage-validation-workflow.md",
        "references/shared/asset-validation-rules.md",
        "references/shared/submission-metadata-rules.md",
        f"releases/{release_id}/release-spec.md",
        f"releases/{release_id}/production-handoff.md",
        f"releases/{release_id}/release-log.md",
        f"releases/{release_id}/qa/release-checklist.md",
        f"releases/{release_id}/qa/quality-ledger.md",
        f"releases/{release_id}/qa/usage-validation.md",
        f"releases/{release_id}/qa/release-retrospective.md",
        f"releases/{release_id}/submission/submission-checklist.md",
        f"releases/{release_id}/submission/submission-audit-report.md",
    ]
    for file_name in files:
        (brand / file_name).write_text("ok\n", encoding="utf-8")

    write_yaml(release / "submission" / "metadata.yaml", valid_metadata())

    manifest = {
        "schema_version": "1.0",
        "factory_base_version": "2026-04-25",
        "template_schema_version": "1.0",
        "brand": {
            "slug": "test-brand",
            "name": "Test Brand",
            "type": brand_type,
            "stage": "design-ready",
            "owner": "tests",
        },
        "product": {
            "item_type": "static-emoji",
            "package_type": "emoji",
            "initial_set_count": count,
            "animation": False,
        },
        "market": {
            "observation_log": "market/market-observation-log.md",
            "category_gap_map": "market/category-gap-map.md",
        },
        "production": {
            "profile": "rough-to-final",
            "release_root": "releases",
            "active_release": release_id,
            "final_asset_dir": f"releases/{release_id}/production/finals",
            "prompt_bundle_dir": f"releases/{release_id}/prompts",
        },
        "quality": {
            "release_checklist_path": f"releases/{release_id}/qa/release-checklist.md",
            "quality_ledger_path": f"releases/{release_id}/qa/quality-ledger.md",
            "usage_validation_path": f"releases/{release_id}/qa/usage-validation.md",
            "retrospective_path": f"releases/{release_id}/qa/release-retrospective.md",
            "release_log_path": f"releases/{release_id}/release-log.md",
        },
        "submission": {
            "metadata_path": f"releases/{release_id}/submission/metadata.yaml",
            "checklist_path": f"releases/{release_id}/submission/submission-checklist.md",
            "audit_report_path": f"releases/{release_id}/submission/submission-audit-report.md",
            "line_upload_dir": f"releases/{release_id}/submission/line-upload",
            "internal_archive_dir": f"releases/{release_id}/submission/internal-archive",
        },
        "strategy": {
            "split_reason": "tests",
            "release_policy": "manual",
            "sync_policy": "snapshot",
            "premium_horizon": "unknown",
        },
        "snapshots": {
            "line_platform_baseline": "references/shared/line-platform-baseline.md",
            "structure_constraints": "references/shared/structure-constraints.md",
            "emoji_product_rules": "references/shared/emoji-product-rules.md",
            "review_risk_rules": "references/shared/review-risk-rules.md",
            "evaluation_model": "references/shared/evaluation-model.md",
            "quality_control_workflow": "references/shared/quality-control-workflow.md",
            "usage_validation_workflow": "references/shared/usage-validation-workflow.md",
            "asset_validation_rules": "references/shared/asset-validation-rules.md",
            "submission_metadata_rules": "references/shared/submission-metadata-rules.md",
        },
        "source": {
            "factory_repo": "line-emoji-factory",
            "brand_setting_path": "brand/brand-setting.md",
            "brand_positioning_path": "brand/brand-positioning.md",
            "production_brief_path": "brand/brand-production-brief.md",
            "system_prompt_path": "brand/brand-system-prompt.md",
            "active_release_spec_path": f"releases/{release_id}/release-spec.md",
        },
        "ip": {
            "style_bible": "brand/ip/ip-style-bible.md",
            "reference_asset_register": "brand/ip/reference-asset-register.md",
            "approval_log": "brand/ip/ip-approval-log.md",
            "character_expression_matrix": "brand/ip/character-expression-matrix.md",
        },
        "releases": [
            {
                "id": release_id,
                "status": "draft",
                "spec": f"releases/{release_id}/release-spec.md",
                "handoff": f"releases/{release_id}/production-handoff.md",
                "checklist": f"releases/{release_id}/qa/release-checklist.md",
                "submission": f"releases/{release_id}/submission",
            }
        ],
    }
    write_yaml(brand / "brand-manifest.yaml", manifest)

    if with_assets:
        for index in range(1, count + 1):
            write_png(release / "production" / "finals" / f"source-{index}.png", (180, 180))
        if with_tab:
            write_png(release / "production" / "tab" / "source-tab.png", (96, 74))

    return brand
