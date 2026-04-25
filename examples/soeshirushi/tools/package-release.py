#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


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


def copy_images(finals_dir: Path, images_dir: Path) -> list[Path]:
    images_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for source in sorted(finals_dir.glob("*.png")):
        target = images_dir / source.name
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def make_zip(submission_dir: Path, images: list[Path], metadata: Path) -> Path:
    package_path = submission_dir / "package.zip"
    if package_path.exists():
        package_path.unlink()
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(metadata, metadata.name)
        for image in images:
            archive.write(image, f"images/{image.name}")
    return package_path


def append_release_log(release_log: Path, release_id: str, package_path: Path, checksum: str) -> None:
    line = (
        "\n## Package Entry\n"
        f"- Release: {release_id}\n"
        f"- Package: {package_path.as_posix()}\n"
        f"- SHA256: {checksum}\n"
    )
    release_log.parent.mkdir(parents=True, exist_ok=True)
    with release_log.open("a", encoding="utf-8") as handle:
        handle.write(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a LINE emoji release for submission.")
    parser.add_argument("brand_repo", type=Path)
    parser.add_argument("--release-id", default="release-001")
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--factory-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    brand_repo = args.brand_repo.resolve()
    release_dir = brand_repo / "releases" / args.release_id
    finals_dir = release_dir / "production" / "finals"
    submission_dir = release_dir / "submission"
    images_dir = submission_dir / "images"
    metadata = submission_dir / "metadata.yaml"
    release_log = release_dir / "release-log.md"

    if not finals_dir.exists():
        print(f"finals directory does not exist: {finals_dir}", file=sys.stderr)
        return 1
    if not metadata.exists():
        print(f"metadata does not exist: {metadata}", file=sys.stderr)
        return 1

    images = copy_images(finals_dir, images_dir)
    if len(images) != args.expected_count:
        print(f"expected {args.expected_count} final PNG files, found {len(images)}", file=sys.stderr)
        return 1

    run([sys.executable, str(args.factory_root / "tools" / "validate-metadata.py"), str(metadata)], args.factory_root)
    run(
        [
            sys.executable,
            str(args.factory_root / "tools" / "validate-assets.py"),
            str(images_dir),
            "--expected-count",
            str(args.expected_count),
        ],
        args.factory_root,
    )

    package_path = make_zip(submission_dir, images, metadata)
    if package_path.stat().st_size > 20_000_000:
        print(f"package exceeds 20MB: {package_path}", file=sys.stderr)
        return 1
    checksum = sha256(package_path)
    checksum_path = submission_dir / "package-checksums.txt"
    checksum_path.write_text(f"{checksum}  {package_path.name}\n", encoding="utf-8")
    append_release_log(release_log, args.release_id, package_path, checksum)
    print(f"package created: {package_path}")
    print(f"sha256: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
