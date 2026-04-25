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
SUBMISSION_TAB_NAME = "tab.png"


def alpha_extrema(image: Image.Image) -> tuple[int, int] | None:
    if image.mode in {"RGBA", "LA"}:
        return image.getchannel("A").getextrema()
    if image.mode == "P" and "transparency" in image.info:
        return image.convert("RGBA").getchannel("A").getextrema()
    return None


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
            alpha = alpha_extrema(image)
            if alpha is None:
                errors.append(f"{path}: transparent background not detected")
            elif alpha[0] == 255:
                errors.append(f"{path}: transparent background not detected")
            elif alpha[1] == 0:
                errors.append(f"{path}: image is fully transparent")
            dpi = image.info.get("dpi")
            if dpi and (dpi[0] < 71.9 or dpi[1] < 71.9):
                warnings.append(f"{path}: dpi below 72: {dpi}")
            if not dpi:
                warnings.append(f"{path}: dpi metadata missing; confirm export settings before submission")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path}: cannot read image: {exc}")
    return errors, warnings


def submission_expected_names(expected_count: int) -> set[str]:
    return {f"{index:03}.png" for index in range(1, expected_count + 1)}


def validate_zip(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: zip file does not exist"]
    if path.stat().st_size > MAX_ZIP_BYTES:
        errors.append(f"{path}: exceeds 20MB")
    if not zipfile.is_zipfile(path):
        errors.append(f"{path}: not a valid zip file")
        return errors
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
    for name in names:
        filename = Path(name).name
        if not filename.lower().endswith(".png"):
            errors.append(f"{path}: line upload zip must contain only image files, found {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji image assets.")
    parser.add_argument("images_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--tab-image", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--stage", choices=["production", "submission"], default="production")
    parser.add_argument("--asset-type", choices=["static", "animation"], default="static")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if args.asset_type == "animation":
        errors.append("animation emoji asset validation is not supported yet")

    if not args.images_dir.exists():
        errors.append(f"{args.images_dir}: directory does not exist")
    else:
        tab_image = args.tab_image
        if args.stage == "submission" and tab_image is None:
            tab_image = args.images_dir / SUBMISSION_TAB_NAME

        content_images = sorted(
            path
            for path in args.images_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".png"
            and (tab_image is None or path.resolve() != tab_image.resolve())
            and path.name.lower() != SUBMISSION_TAB_NAME
        )
        count = len(content_images)
        expected_count = args.expected_count
        if expected_count is not None and count != expected_count:
            errors.append(f"{args.images_dir}: expected {expected_count} content images, found {count}")
        elif expected_count is None and count not in ALLOWED_COUNTS:
            errors.append(f"{args.images_dir}: content image count must be one of {sorted(ALLOWED_COUNTS)}, found {count}")
            expected_count = count

        if args.stage == "submission" and expected_count is not None:
            expected_names = submission_expected_names(expected_count)
            actual_names = {path.name for path in content_images}
            wrong_names = sorted(actual_names - expected_names)
            missing_names = sorted(expected_names - actual_names)
            for name in wrong_names:
                errors.append(f"{args.images_dir}: invalid submission filename: {name}")
            for name in missing_names:
                errors.append(f"{args.images_dir}: missing submission filename: {name}")

        for image_path in content_images:
            image_errors, image_warnings = validate_image(image_path, CONTENT_SIZE, "content image")
            errors.extend(image_errors)
            warnings.extend(image_warnings)

        if tab_image:
            if not tab_image.exists():
                errors.append(f"{tab_image}: tab image does not exist")
            else:
                image_errors, image_warnings = validate_image(tab_image, TAB_SIZE, "tab image")
                errors.extend(image_errors)
                warnings.extend(image_warnings)

    if args.tab_image and not args.images_dir.exists():
        image_errors, image_warnings = validate_image(args.tab_image, TAB_SIZE, "tab image")
        errors.extend(image_errors)
        warnings.extend(image_warnings)

    if args.zip_path:
        errors.extend(validate_zip(args.zip_path))

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
