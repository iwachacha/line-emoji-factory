#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from PIL import Image


CONTENT_SIZE = (180, 180)
TAB_SIZE = (96, 74)
MAX_IMAGE_BYTES = 1_000_000
MAX_ZIP_BYTES = 20_000_000
ALLOWED_COUNTS = {8, 16, 24, 32, 40}


def has_transparency(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return image.getextrema()[-1][0] < 255
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def validate_image(path: Path, expected_size: tuple[int, int], label: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if path.suffix.lower() != ".png":
        errors.append(f"{path}: {label} must be PNG/APNG")
        return errors, warnings
    if path.stat().st_size > MAX_IMAGE_BYTES:
        errors.append(f"{path}: exceeds 1MB")
    try:
        with Image.open(path) as image:
            if image.size != expected_size:
                errors.append(f"{path}: expected {expected_size[0]}x{expected_size[1]}, got {image.size[0]}x{image.size[1]}")
            if image.mode not in {"RGB", "RGBA", "P", "LA"}:
                errors.append(f"{path}: unsupported color mode {image.mode}")
            if not has_transparency(image):
                errors.append(f"{path}: transparent background not detected")
            dpi = image.info.get("dpi")
            if dpi and (dpi[0] < 72 or dpi[1] < 72):
                warnings.append(f"{path}: dpi below 72: {dpi}")
            if not dpi:
                warnings.append(f"{path}: dpi metadata missing; confirm export settings before submission")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path}: cannot read image: {exc}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji image assets.")
    parser.add_argument("images_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--tab-image", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not args.images_dir.exists():
        errors.append(f"{args.images_dir}: directory does not exist")
    else:
        content_images = sorted(path for path in args.images_dir.iterdir() if path.is_file() and path.suffix.lower() == ".png")
        count = len(content_images)
        expected_count = args.expected_count
        if expected_count is not None and count != expected_count:
            errors.append(f"{args.images_dir}: expected {expected_count} content images, found {count}")
        elif expected_count is None and count not in ALLOWED_COUNTS:
            errors.append(f"{args.images_dir}: content image count must be one of {sorted(ALLOWED_COUNTS)}, found {count}")

        for image_path in content_images:
            image_errors, image_warnings = validate_image(image_path, CONTENT_SIZE, "content image")
            errors.extend(image_errors)
            warnings.extend(image_warnings)

    if args.tab_image:
        image_errors, image_warnings = validate_image(args.tab_image, TAB_SIZE, "tab image")
        errors.extend(image_errors)
        warnings.extend(image_warnings)

    if args.zip_path:
        if not args.zip_path.exists():
            errors.append(f"{args.zip_path}: zip file does not exist")
        else:
            if args.zip_path.stat().st_size > MAX_ZIP_BYTES:
                errors.append(f"{args.zip_path}: exceeds 20MB")
            if not zipfile.is_zipfile(args.zip_path):
                errors.append(f"{args.zip_path}: not a valid zip file")

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("asset validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
