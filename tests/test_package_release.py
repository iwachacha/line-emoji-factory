from __future__ import annotations

import json
import subprocess
import zipfile

import yaml

from conftest import PYTHON, ROOT, create_brand_repo, create_two_release_brand_repo, run_cmd_args


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
    assert "snapshots/brand-canon.md" in names
    assert "snapshots/product-catalog.md" in names
    assert "snapshots/series-plan.md" in names


def test_package_release_clean_removes_stale_submission_files(tmp_path):
    brand = create_brand_repo(tmp_path, with_assets=True)
    submission = brand / "releases" / "release-001" / "submission"
    stale_image = submission / "line-upload" / "images" / "999.png"
    stale_image.parent.mkdir(parents=True, exist_ok=True)
    stale_image.write_bytes(b"stale")
    stale_note = submission / "line-upload" / "metadata.yaml"
    stale_note.write_text("stale: true\n", encoding="utf-8")

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
    assert not stale_image.exists()
    assert not stale_note.exists()

    with zipfile.ZipFile(submission / "line-upload" / "images.zip") as archive:
        names = set(archive.namelist())
    assert "999.png" not in names
    assert "metadata.yaml" not in names


def test_package_release_requires_tab_image(tmp_path):
    brand = create_brand_repo(tmp_path, with_assets=True, with_tab=False)

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "package-release.py", brand, "--release-id", "release-001", "--clean"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "tab image does not exist" in result.stderr


def test_release_002_package_uses_release_002_metadata(tmp_path):
    brand = create_two_release_brand_repo(tmp_path, with_assets=True)
    release_001 = brand / "releases" / "release-001"
    release_002 = brand / "releases" / "release-002"
    release_001_metadata = yaml.safe_load((release_001 / "submission" / "metadata.yaml").read_text(encoding="utf-8"))
    release_002_metadata = yaml.safe_load((release_002 / "submission" / "metadata.yaml").read_text(encoding="utf-8"))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "package-release.py",
            brand,
            "--release-id",
            "release-002",
            "--target",
            "both",
            "--clean",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr

    internal_zip = release_002 / "submission" / "internal-archive" / "package.zip"
    with zipfile.ZipFile(internal_zip) as archive:
        packaged_metadata = yaml.safe_load(archive.read("metadata.yaml").decode("utf-8"))
    print(f"release-001 metadata title: {release_001_metadata['title']}")
    print(f"release-002 metadata title: {release_002_metadata['title']}")
    print(f"release-002 package internal archive metadata title: {packaged_metadata['title']}")
    assert packaged_metadata["title"] == "Release Two Emoji"
    print("release-002 title assertion passed")


def test_package_release_supports_static_stickers(tmp_path):
    brand = create_brand_repo(tmp_path, item_type="static-sticker", with_assets=True)

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
    with zipfile.ZipFile(line_zip) as archive:
        names = set(archive.namelist())
    assert "01.png" in names
    assert "08.png" in names
    assert "main.png" in names
    assert "tab.png" in names
    assert "001.png" not in names

    asset_map = json.loads((submission / "internal-archive" / "asset-map.json").read_text(encoding="utf-8"))
    assert asset_map["item_type"] == "static-sticker"
    assert asset_map["content_images"][0]["submission"].endswith("01.png")
    assert asset_map["main_image"]["submission"].endswith("main.png")
    assert asset_map["tab_image"]["submission"].endswith("tab.png")
