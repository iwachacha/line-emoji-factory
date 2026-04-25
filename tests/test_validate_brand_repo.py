from __future__ import annotations

import subprocess

import yaml

from conftest import PYTHON, ROOT, create_brand_repo, run_cmd_args, write_yaml


def run_brand_repo(brand, *extra):
    return subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-brand-repo.py", brand, *extra),
        text=True,
        capture_output=True,
    )


def test_validate_brand_repo_is_manifest_driven(tmp_path):
    brand = create_brand_repo(tmp_path, release_id="release-002")
    result = run_brand_repo(brand, "--release-id", "release-002")
    assert result.returncode == 0, result.stderr


def test_missing_required_snapshot_fails(tmp_path):
    brand = create_brand_repo(tmp_path)
    manifest_path = brand / "brand-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    del manifest["snapshots"]["asset_validation_rules"]
    write_yaml(manifest_path, manifest)

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "asset_validation_rules" in result.stderr


def test_fixed_ip_missing_ip_file_fails(tmp_path):
    brand = create_brand_repo(tmp_path, brand_type="fixed_ip")
    (brand / "brand" / "ip" / "ip-style-bible.md").unlink()

    result = run_brand_repo(brand)
    assert result.returncode != 0
    assert "ip-style-bible.md" in result.stderr


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
