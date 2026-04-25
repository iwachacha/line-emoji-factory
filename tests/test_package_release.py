from __future__ import annotations

import json
import subprocess
import zipfile

from conftest import PYTHON, ROOT, create_brand_repo, run_cmd_args


def test_package_release_splits_line_upload_and_internal_archive(tmp_path):
    brand = create_brand_repo(tmp_path, with_assets=True)

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "package-release.py",
            brand,
            "--release-id",
            "release-001",
            "--target",
            "both",
            "--clean",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr

    submission = brand / "releases" / "release-001" / "submission"
    line_zip = submission / "line-upload" / "images.zip"
    internal_zip = submission / "internal-archive" / "package.zip"
    assert line_zip.exists()
    assert internal_zip.exists()

    with zipfile.ZipFile(line_zip) as archive:
        names = set(archive.namelist())
    assert "metadata.yaml" not in names
    assert "package-report.md" not in names
    assert "001.png" in names
    assert "008.png" in names
    assert "tab.png" in names

    asset_map = json.loads((submission / "internal-archive" / "asset-map.json").read_text(encoding="utf-8"))
    assert asset_map["content_images"][0]["submission"].endswith("001.png")
    assert asset_map["tab_image"]["submission"].endswith("tab.png")

    with zipfile.ZipFile(internal_zip) as archive:
        names = set(archive.namelist())
    assert "metadata.yaml" in names
    assert "asset-map.json" in names
    assert "package-report.md" in names
    assert "line-upload/images.zip" in names


def test_package_release_requires_tab_image(tmp_path):
    brand = create_brand_repo(tmp_path, with_assets=True, with_tab=False)

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "package-release.py", brand, "--release-id", "release-001", "--clean"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "tab image does not exist" in result.stderr
