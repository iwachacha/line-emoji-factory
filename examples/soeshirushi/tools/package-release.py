#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import yaml


ALLOWED_TARGETS = {"line-upload", "internal-archive", "both"}
ALLOWED_COUNTS = {8, 16, 24, 32, 40}
ITEM_SPECS = {
    "static-emoji": {
        "package_type": "emoji",
        "asset_type": "static-emoji",
        "content_name_width": 3,
        "zip_max_bytes": 20_000_000,
        "companions": [
            {
                "key": "tab_image",
                "source": Path("production/tab/source-tab.png"),
                "submission": "tab.png",
                "cli": "--tab-image",
                "label": "tab image",
            }
        ],
    },
    "static-sticker": {
        "package_type": "sticker",
        "asset_type": "static-sticker",
        "content_name_width": 2,
        "zip_max_bytes": 60_000_000,
        "companions": [
            {
                "key": "main_image",
                "source": Path("production/main/source-main.png"),
                "submission": "main.png",
                "cli": "--main-image",
                "label": "main image",
            },
            {
                "key": "tab_image",
                "source": Path("production/tab/source-tab.png"),
                "submission": "tab.png",
                "cli": "--tab-image",
                "label": "tab image",
            },
        ],
    },
}
UNSUPPORTED_PACKAGE_ITEM_TYPES = {
    "animation-emoji": "animation emoji packaging is not supported yet; validate APNG assets with validate-assets.py",
}


def run(cmd: list[str], cwd: Path) -> None:
    completed = subprocess.run(cmd, cwd=cwd, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(brand_repo: Path) -> dict:
    manifest_path = brand_repo / "brand-manifest.yaml"
    if not manifest_path.exists():
        return {}
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    return data or {}


def manifest_release(manifest: dict, release_id: str) -> dict:
    for release in manifest.get("releases", []):
        if release.get("id") == release_id:
            return release
    return {}


def resolve_release_id(manifest: dict, requested: str | None) -> str:
    if requested:
        return requested
    active_release = manifest.get("production", {}).get("active_release")
    if active_release:
        return str(active_release)
    releases = manifest.get("releases", [])
    if releases:
        return str(releases[0]["id"])
    return "release-001"


def resolve_expected_count(manifest: dict, release_info: dict, cli_count: int | None, actual_count: int) -> int:
    manifest_count = release_info.get("set_count", manifest.get("product", {}).get("initial_set_count"))
    if cli_count is not None and manifest_count is not None and cli_count != int(manifest_count):
        raise ValueError(
            f"--expected-count {cli_count} does not match manifest product.initial_set_count {manifest_count}"
        )
    count = int(manifest_count or cli_count or actual_count)
    if count not in ALLOWED_COUNTS:
        raise ValueError(f"content image count must be one of {sorted(ALLOWED_COUNTS)}, got {count}")
    return count


def resolve_item_type(manifest: dict, release_info: dict, cli_item_type: str | None, cli_asset_type: str | None) -> str:
    product = manifest.get("product", {})
    product_item_type = str(product.get("item_type", "static-emoji"))
    item_type = str(cli_item_type or release_info.get("item_type") or product_item_type)
    supported = product.get("supported_item_types")
    if supported and item_type not in supported:
        raise ValueError(f"release item_type {item_type} is not listed in product.supported_item_types")
    if item_type in UNSUPPORTED_PACKAGE_ITEM_TYPES:
        raise ValueError(UNSUPPORTED_PACKAGE_ITEM_TYPES[item_type])
    if item_type not in ITEM_SPECS:
        raise ValueError(f"unsupported package item_type: {item_type}")

    spec = ITEM_SPECS[item_type]
    package_type = str(release_info.get("package_type") or product.get("package_type") or spec["package_type"])
    if package_type != spec["package_type"]:
        raise ValueError(f"package_type {package_type} does not match item_type {item_type}")

    if cli_asset_type == "animation" and "animation" not in item_type:
        raise ValueError(f"--asset-type animation does not match manifest item_type {item_type}")
    if cli_asset_type == "static" and "animation" in item_type:
        raise ValueError(f"--asset-type static does not match manifest item_type {item_type}")
    return item_type


def resolve_metadata_path(brand_repo: Path, manifest: dict, release_info: dict, release_id: str) -> Path:
    release_submission = release_info.get("submission")
    if release_submission:
        path = brand_repo / release_submission / "metadata.yaml"
        if path.exists():
            return path

    path = brand_repo / "releases" / release_id / "submission" / "metadata.yaml"
    if path.exists():
        return path

    active_release = manifest.get("production", {}).get("active_release")
    fallback = manifest.get("submission", {}).get("metadata_path")
    if fallback and active_release == release_id:
        return brand_repo / fallback

    return path


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def ensure_clean(target: Path, clean: bool) -> None:
    if clean and target.exists():
        shutil.rmtree(target)
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"output directory already contains files; rerun with --clean: {target}")


def copy_submission_images(
    finals: list[Path],
    companion_sources: dict[str, Path],
    item_type: str,
    images_dir: Path,
    release_dir: Path,
) -> dict:
    spec = ITEM_SPECS[item_type]
    images_dir.mkdir(parents=True, exist_ok=True)
    content_images: list[dict] = []
    for index, source in enumerate(finals, start=1):
        target = images_dir / f"{index:0{spec['content_name_width']}}.png"
        shutil.copy2(source, target)
        content_images.append(
            {
                "slot": index,
                "source": rel(source, release_dir),
                "submission": rel(target, release_dir),
            }
        )

    asset_map = {
        "release_id": release_dir.name,
        "item_type": item_type,
        "content_images": content_images,
        "companion_images": {},
    }
    for companion in spec["companions"]:
        source = companion_sources[companion["key"]]
        target = images_dir / companion["submission"]
        shutil.copy2(source, target)
        entry = {
            "source": rel(source, release_dir),
            "submission": rel(target, release_dir),
        }
        asset_map[companion["key"]] = entry
        asset_map["companion_images"][companion["key"]] = entry
    return asset_map


def make_line_zip(line_upload_dir: Path, images: list[Path]) -> Path:
    package_path = line_upload_dir / "images.zip"
    if package_path.exists():
        package_path.unlink()
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for image in sorted(images):
            archive.write(image, image.name)
    return package_path


def asset_map_from_submission(line_images_dir: Path, release_id: str, item_type: str) -> dict:
    companion_filenames = {companion["submission"] for companion in ITEM_SPECS[item_type]["companions"]}
    content_images = []
    for image in sorted(line_images_dir.glob("*.png")):
        if image.name in companion_filenames:
            continue
        content_images.append(
            {
                "slot": int(image.stem) if image.stem.isdigit() else None,
                "source": None,
                "submission": f"submission/line-upload/images/{image.name}",
            }
        )
    asset_map = {
        "release_id": release_id,
        "item_type": item_type,
        "content_images": content_images,
        "companion_images": {},
    }
    for companion in ITEM_SPECS[item_type]["companions"]:
        image = line_images_dir / companion["submission"]
        entry = {
            "source": None,
            "submission": f"submission/line-upload/images/{companion['submission']}",
        } if image.exists() else None
        asset_map[companion["key"]] = entry
        if entry:
            asset_map["companion_images"][companion["key"]] = entry
    return asset_map


def write_report(
    report_path: Path,
    brand_repo: Path,
    release_id: str,
    item_type: str,
    target: str,
    images_zip: Path | None,
    internal_zip: Path | None,
    expected_count: int,
) -> None:
    created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    lines = [
        "# Package Report",
        "",
        "## Target",
        f"- Brand repo: `{brand_repo.as_posix()}`",
        f"- Release: `{release_id}`",
        f"- Item type: `{item_type}`",
        f"- Target: `{target}`",
        f"- Created at: `{created_at}`",
        "",
        "## Files",
        f"- Content image count: `{expected_count}`",
        f"- Line upload ZIP: `{images_zip.as_posix() if images_zip else 'not generated'}`",
        f"- Internal archive ZIP: `{internal_zip.as_posix() if internal_zip else 'not generated yet'}`",
        "",
        "## Validation",
        "- Metadata validation: passed",
        "- Asset validation: passed",
        "- Result: passed",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_checksums(checksum_path: Path, files: list[Path]) -> None:
    lines = [f"{sha256(file_path)}  {file_path.name}" for file_path in files if file_path.exists()]
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_internal_zip(
    internal_dir: Path,
    line_zip: Path,
    metadata: Path,
    report: Path,
    asset_map: Path,
    checksums: Path,
    manifest: Path,
    release_spec: Path,
) -> Path:
    package_path = internal_dir / "package.zip"
    if package_path.exists():
        package_path.unlink()
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(line_zip, "line-upload/images.zip")
        archive.write(metadata, "metadata.yaml")
        archive.write(report, "package-report.md")
        archive.write(asset_map, "asset-map.json")
        archive.write(checksums, "package-checksums.txt")
        if manifest.exists():
            archive.write(manifest, "snapshots/brand-manifest.yaml")
        if release_spec.exists():
            archive.write(release_spec, "snapshots/release-spec.md")
    return package_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a LINE emoji or sticker release for submission.")
    parser.add_argument("brand_repo", type=Path)
    parser.add_argument("--release-id")
    parser.add_argument("--target", choices=sorted(ALLOWED_TARGETS), default="both")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--expected-count", type=int, help="Deprecated. Use manifest product.initial_set_count.")
    parser.add_argument("--item-type", choices=sorted(ITEM_SPECS), help="Override manifest item type for this package run.")
    parser.add_argument("--asset-type", choices=["static", "animation"], help="Deprecated. Use manifest product.item_type.")
    parser.add_argument("--factory-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    brand_repo = args.brand_repo.resolve()
    manifest = load_manifest(brand_repo)
    release_id = resolve_release_id(manifest, args.release_id)
    release_info = manifest_release(manifest, release_id)
    release_dir = brand_repo / "releases" / release_id
    finals_dir = release_dir / "production" / "finals"
    submission_dir = release_dir / "submission"
    line_upload_dir = submission_dir / "line-upload"
    line_images_dir = line_upload_dir / "images"
    internal_dir = submission_dir / "internal-archive"
    metadata = resolve_metadata_path(brand_repo, manifest, release_info, release_id)
    release_spec = brand_repo / release_info.get("spec", f"releases/{release_id}/release-spec.md")

    if not finals_dir.exists():
        print(f"finals directory does not exist: {finals_dir}", file=sys.stderr)
        return 1
    if not metadata.exists():
        print(f"metadata does not exist: {metadata}", file=sys.stderr)
        return 1

    finals = sorted(path for path in finals_dir.iterdir() if path.is_file() and path.suffix.lower() == ".png")
    try:
        item_type = resolve_item_type(manifest, release_info, args.item_type, args.asset_type)
        spec = ITEM_SPECS[item_type]
        companion_sources = {
            companion["key"]: release_dir / companion["source"]
            for companion in spec["companions"]
        }
        for companion in spec["companions"]:
            source = companion_sources[companion["key"]]
            if not source.exists():
                raise ValueError(f"{companion['label']} does not exist: {source}")
        expected_count = resolve_expected_count(manifest, release_info, args.expected_count, len(finals))
        if len(finals) != expected_count:
            raise ValueError(f"expected {expected_count} final PNG files, found {len(finals)}")
        if args.target in {"line-upload", "both"}:
            ensure_clean(line_upload_dir, args.clean)
        if args.target in {"internal-archive", "both"}:
            ensure_clean(internal_dir, args.clean)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    factory_root = args.factory_root.resolve()
    run([sys.executable, str(args.factory_root / "tools" / "validate-metadata.py"), str(metadata)], args.factory_root)
    production_validation_cmd = [
        sys.executable,
        str(factory_root / "tools" / "validate-assets.py"),
        str(finals_dir),
        "--expected-count",
        str(expected_count),
        "--stage",
        "production",
        "--asset-type",
        spec["asset_type"],
    ]
    for companion in spec["companions"]:
        production_validation_cmd.extend([companion["cli"], str(companion_sources[companion["key"]])])
    run(production_validation_cmd, factory_root)

    asset_map: dict | None = None
    images_zip: Path | None = None
    if args.target in {"line-upload", "both"}:
        asset_map = copy_submission_images(finals, companion_sources, item_type, line_images_dir, release_dir)
        run(
            [
                sys.executable,
                str(factory_root / "tools" / "validate-assets.py"),
                str(line_images_dir),
                "--expected-count",
                str(expected_count),
                "--stage",
                "submission",
                "--asset-type",
                spec["asset_type"],
            ],
            factory_root,
        )
        images_zip = make_line_zip(line_upload_dir, list(line_images_dir.glob("*.png")))
        if images_zip.stat().st_size > spec["zip_max_bytes"]:
            print(f"line upload zip exceeds {spec['zip_max_bytes'] // 1_000_000}MB: {images_zip}", file=sys.stderr)
            return 1
        run(
            [
                sys.executable,
                str(factory_root / "tools" / "validate-assets.py"),
                str(line_images_dir),
                "--expected-count",
                str(expected_count),
                "--stage",
                "submission",
                "--asset-type",
                spec["asset_type"],
                "--zip",
                str(images_zip),
            ],
            factory_root,
        )

    if args.target == "internal-archive" and images_zip is None:
        images_zip = line_upload_dir / "images.zip"
        if not images_zip.exists():
            print(f"line upload zip does not exist: {images_zip}", file=sys.stderr)
            return 1

    internal_zip: Path | None = None
    if args.target in {"internal-archive", "both"}:
        internal_dir.mkdir(parents=True, exist_ok=True)
        if asset_map is None:
            asset_map = asset_map_from_submission(line_images_dir, release_id, item_type)
        asset_map_path = internal_dir / "asset-map.json"
        asset_map_path.write_text(json.dumps(asset_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report_path = internal_dir / "package-report.md"
        checksum_path = internal_dir / "package-checksums.txt"
        internal_zip_path = internal_dir / "package.zip"
        write_report(report_path, brand_repo, release_id, item_type, args.target, images_zip, internal_zip_path, expected_count)
        write_checksums(checksum_path, [images_zip, metadata, asset_map_path, report_path])
        internal_zip = make_internal_zip(
            internal_dir,
            images_zip,
            metadata,
            report_path,
            asset_map_path,
            checksum_path,
            brand_repo / "brand-manifest.yaml",
            release_spec,
        )
        write_checksums(checksum_path, [images_zip, metadata, asset_map_path, report_path, internal_zip])
        if internal_zip.stat().st_size > spec["zip_max_bytes"]:
            print(f"warning: internal archive exceeds {spec['zip_max_bytes'] // 1_000_000}MB: {internal_zip}", file=sys.stderr)

    if images_zip:
        print(f"line upload zip created: {images_zip}")
        print(f"line upload sha256: {sha256(images_zip)}")
    if internal_zip:
        print(f"internal archive created: {internal_zip}")
        print(f"internal archive sha256: {sha256(internal_zip)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
