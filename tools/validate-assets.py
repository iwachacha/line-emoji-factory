#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


CONTENT_SIZE = (180, 180)
TAB_SIZE = (96, 74)
MAX_IMAGE_BYTES = 1_000_000
MAX_ANIMATION_BYTES = 300_000
MAX_ZIP_BYTES = 20_000_000
ALLOWED_COUNTS = {8, 16, 24, 32, 40}
SUBMISSION_TAB_NAME = "tab.png"
ANIMATION_MIN_FRAMES = 5
ANIMATION_MAX_FRAMES = 20
ANIMATION_MAX_DURATION_MS = 4_000
ANIMATION_MIN_LOOP = 1
ANIMATION_MAX_LOOP = 4
CONTACT_SHEET_PREVIEWS = (180, 48, 32, 24)


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
            if getattr(image, "is_animated", False):
                errors.append(f"{path}: APNG animation detected in static {label}")
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


def validate_animation_image(path: Path, expected_size: tuple[int, int], label: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if path.suffix.lower() != ".png":
        errors.append(f"{path}: {label} must be APNG with .png extension")
        return errors, warnings
    if path.stat().st_size > MAX_ANIMATION_BYTES:
        errors.append(f"{path}: APNG exceeds 300KB")
    try:
        with Image.open(path) as image:
            frame_count = int(getattr(image, "n_frames", 1))
            if not getattr(image, "is_animated", False) or frame_count <= 1:
                errors.append(f"{path}: APNG animation not detected")
            if frame_count < ANIMATION_MIN_FRAMES or frame_count > ANIMATION_MAX_FRAMES:
                errors.append(
                    f"{path}: APNG frame count must be {ANIMATION_MIN_FRAMES}-{ANIMATION_MAX_FRAMES}, got {frame_count}"
                )

            loop = image.info.get("loop")
            if loop is None:
                errors.append(f"{path}: APNG loop count missing")
            else:
                try:
                    loop_count = int(loop)
                    if loop_count < ANIMATION_MIN_LOOP or loop_count > ANIMATION_MAX_LOOP:
                        errors.append(
                            f"{path}: APNG loop count must be {ANIMATION_MIN_LOOP}-{ANIMATION_MAX_LOOP}, got {loop_count}"
                        )
                except (TypeError, ValueError):
                    errors.append(f"{path}: APNG loop count is not an integer")

            total_duration_ms = 0
            visible_frames = 0
            transparent_background_frames = 0
            for frame_index in range(frame_count):
                image.seek(frame_index)
                if image.size != expected_size:
                    errors.append(
                        f"{path}: frame {frame_index + 1} expected {expected_size[0]}x{expected_size[1]}, "
                        f"got {image.size[0]}x{image.size[1]}"
                    )
                duration = image.info.get("duration", 0) or 0
                total_duration_ms += int(duration)
                alpha = alpha_extrema(image)
                if alpha is None:
                    if image.convert("RGBA").getbbox():
                        visible_frames += 1
                elif alpha[0] < 255:
                    transparent_background_frames += 1
                    if alpha[1] > 0:
                        visible_frames += 1

            if total_duration_ms <= 0:
                errors.append(f"{path}: APNG duration metadata missing")
            elif total_duration_ms > ANIMATION_MAX_DURATION_MS:
                errors.append(f"{path}: APNG duration exceeds 4 seconds")
            if visible_frames == 0:
                errors.append(f"{path}: APNG is fully transparent")
            if transparent_background_frames == 0:
                errors.append(f"{path}: transparent background not detected")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path}: cannot read APNG: {exc}")
    return errors, warnings


def submission_expected_names(expected_count: int) -> set[str]:
    return {f"{index:03}.png" for index in range(1, expected_count + 1)}


def checkerboard(size: tuple[int, int], block: int = 8) -> Image.Image:
    image = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], block):
        for x in range(0, size[0], block):
            if (x // block + y // block) % 2:
                draw.rectangle((x, y, x + block - 1, y + block - 1), fill=(224, 224, 224, 255))
    return image


def first_frame(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.seek(0)
        return image.convert("RGBA")


def write_contact_sheet(images: list[Path], output: Path) -> None:
    if not images:
        return
    padding = 12
    gap = 12
    row_height = CONTACT_SHEET_PREVIEWS[0]
    width = (padding * 2) + sum(CONTACT_SHEET_PREVIEWS) + (gap * (len(CONTACT_SHEET_PREVIEWS) - 1))
    height = (padding * 2) + (row_height * len(images)) + (gap * (len(images) - 1))
    sheet = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    for row_index, path in enumerate(images):
        source = first_frame(path)
        x = padding
        y = padding + row_index * (row_height + gap)
        for preview_size in CONTACT_SHEET_PREVIEWS:
            preview = source.copy()
            preview.thumbnail((preview_size, preview_size), Image.Resampling.LANCZOS)
            cell = checkerboard((preview_size, row_height))
            paste_x = (preview_size - preview.width) // 2
            paste_y = (row_height - preview.height) // 2
            cell.alpha_composite(preview, (paste_x, paste_y))
            sheet.alpha_composite(cell, (x, y))
            x += preview_size + gap

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output)


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
    parser.add_argument("--preview-contact-sheet", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

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
            if args.asset_type == "animation":
                image_errors, image_warnings = validate_animation_image(image_path, CONTENT_SIZE, "content image")
            else:
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

        if args.preview_contact_sheet:
            try:
                write_contact_sheet(content_images, args.preview_contact_sheet)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{args.preview_contact_sheet}: cannot write contact sheet: {exc}")

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
