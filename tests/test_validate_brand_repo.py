from __future__ import annotations

import subprocess

import yaml

from conftest import PYTHON, ROOT, create_brand_repo, create_two_release_brand_repo, run_cmd_args, write_yaml


def run_brand_repo(brand, *extra):
    return subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-brand-repo.py", brand, *extra),
        text=True,
        capture_output=True,
    )


def test_validate_brand_repo_is_manifest_driven(tmp_path):
    brand = create_two_release_brand_repo(tmp_path)
    result = run_brand_repo(brand, "--release-id", "release-002")
    assert result.returncode == 0, result.stderr


def test_startup_brand_contract_passes_without_release_skeleton(tmp_path):
    brand = create_brand_repo(tmp_path, repo_profile="startup")
    assert not (brand / "releases").exists()
    manifest = yaml.safe_load((brand / "brand-manifest.yaml").read_text(encoding="utf-8"))
    assert "production_pipeline_workflow" not in manifest["snapshots"]
    assert "production_profile_rules" not in manifest["snapshots"]

    result = run_brand_repo(brand)
    assert result.returncode == 0, result.stderr


def test_startup_animation_emoji_hypothesis_is_allowed(tmp_path):
    brand = create_brand_repo(tmp_path, item_type="animation-emoji", repo_profile="startup")

    result = run_brand_repo(brand)
    assert result.returncode == 0, result.stderr


def test_generic_brand_does_not_require_ip_files(tmp_path):
    brand = create_brand_repo(tmp_path, brand_type="generic")
    assert not (brand / "brand" / "ip").exists()

    result = run_brand_repo(brand)
    assert result.returncode == 0, result.stderr


def test_static_sticker_brand_contract_passes(tmp_path):
    brand = create_brand_repo(tmp_path, item_type="static-sticker")

    result = run_brand_repo(brand)
    assert result.returncode == 0, result.stderr


def test_release_item_type_must_match_package_type(tmp_path):
    brand = create_brand_repo(tmp_path, item_type="static-sticker")
    manifest_path = brand / "brand-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["releases"][0]["package_type"] = "emoji"
    write_yaml(manifest_path, manifest)

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "package_type must match item_type" in result.stderr


def test_missing_required_snapshot_fails(tmp_path):
    brand = create_brand_repo(tmp_path)
    manifest_path = brand / "brand-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    del manifest["snapshots"]["brand_taxonomy"]
    write_yaml(manifest_path, manifest)

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "brand_taxonomy" in result.stderr


def test_fixed_ip_missing_ip_file_fails(tmp_path):
    brand = create_brand_repo(tmp_path, brand_type="fixed_ip")
    (brand / "brand" / "ip" / "ip-style-bible.md").unlink()

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "ip-style-bible.md" in result.stderr


def test_fixed_ip_complete_fixture_passes(tmp_path):
    brand = create_brand_repo(tmp_path, brand_type="fixed_ip")

    result = run_brand_repo(brand)
    assert result.returncode == 0, result.stderr


def test_production_profile_contract_is_validated(tmp_path):
    brand = create_brand_repo(tmp_path)
    manifest_path = brand / "brand-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["production_profile"]["rough_stage"]["required_outputs"].remove("rough_board")
    write_yaml(manifest_path, manifest)

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "production_profile.rough_stage" in result.stderr
    assert "rough_board" in result.stderr


def test_startup_profile_contract_is_validated(tmp_path):
    brand = create_brand_repo(tmp_path, repo_profile="startup")
    manifest_path = brand / "brand-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["startup_profile"]["product_seed_stage"]["required_outputs"].remove("first_series_seed")
    write_yaml(manifest_path, manifest)

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "startup_profile.product_seed_stage" in result.stderr
    assert "first_series_seed" in result.stderr
