#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


EMOJI_CONTENT_SIZE = (180, 180)
STICKER_CONTENT_MAX_SIZE = (370, 320)
STICKER_MAIN_SIZE = (240, 240)
TAB_SIZE = (96, 74)
MAX_IMAGE_BYTES = 1_000_000
MAX_ANIMATION_BYTES = 300_000
EMOJI_MAX_ZIP_BYTES = 20_000_000
STICKER_MAX_ZIP_BYTES = 60_000_000
ALLOWED_COUNTS = {8, 16, 24, 32, 40}
SUBMISSION_TAB_NAME = "tab.png"
SUBMISSION_MAIN_NAME = "main.png"
ANIMATION_MIN_FRAMES = 5
ANIMATION_MAX_FRAMES = 20
ANIMATION_MAX_DURATION_MS = 4_000
ANIMATION_MIN_LOOP = 1
ANIMATION_MAX_LOOP = 4
CONTACT_SHEET_PREVIEWS = (180, 48, 32, 24)
MIN_VISIBLE_BBOX_RATIO = 0.15
WARN_VISIBLE_BBOX_RATIO = 0.35
WARN_MARGIN_RATIO = 0.35
LOW_CONTRAST_RANGE = 24
LOW_COLOR_VARIETY_COUNT = 3
NEAR_DUPLICATE_HASH_DISTANCE = 5
NEAR_DUPLICATE_MEAN_ABS_DIFF = 4.0

ASSET_TYPE_ALIASES = {
    "static": "static-emoji",
    "animation": "animation-emoji",
}
SUPPORTED_ASSET_TYPES = {"static-emoji", "animation-emoji", "static-sticker"}


def normalize_asset_type(asset_type: str) -> str:
    normalized = ASSET_TYPE_ALIASES.get(asset_type, asset_type)
    if normalized not in SUPPORTED_ASSET_TYPES:
        raise ValueError(f"unsupported asset type: {asset_type}")
    return normalized


def zip_limit(asset_type: str) -> int:
    if asset_type == "static-sticker":
        return STICKER_MAX_ZIP_BYTES
    return EMOJI_MAX_ZIP_BYTES


def content_filename_width(asset_type: str) -> int:
    return 2 if asset_type == "static-sticker" else 3


def companion_names(asset_type: str) -> set[str]:
    names = {SUBMISSION_TAB_NAME}
    if asset_type == "static-sticker":
        names.add(SUBMISSION_MAIN_NAME)
    return names


def alpha_extrema(image: Image.Image) -> tuple[int, int] | None:
    if image.mode in {"RGBA", "LA"}:
        return image.getchannel("A").getextrema()
    if image.mode == "P" and "transparency" in image.info:
        return image.convert("RGBA").getchannel("A").getextrema()
    return None


def validate_static_image(
    path: Path,
    label: str,
    *,
    expected_size: tuple[int, int] | None = None,
    max_size: tuple[int, int] | None = None,
    require_even_size: bool = False,
) -> tuple[list[str], list[str]]:
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
            if expected_size and image.size != expected_size:
                errors.append(f"{path}: expected {expected_size[0]}x{expected_size[1]}, got {image.size[0]}x{image.size[1]}")
            if max_size:
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    errors.append(
                        f"{path}: expected no larger than {max_size[0]}x{max_size[1]}, "
                        f"got {image.size[0]}x{image.size[1]}"
                    )
                if image.size[0] <= 0 or image.size[1] <= 0:
                    errors.append(f"{path}: image dimensions must be positive")
            if require_even_size and (image.size[0] % 2 != 0 or image.size[1] % 2 != 0):
                errors.append(f"{path}: sticker image width and height must be even numbers")
            if image.mode not in {"RGB", "RGBA", "P", "LA"}:
                errors.append(f"{path}: unsupported color mode {image.mode}")
            alpha = alpha_extrema(image)
            if alpha is None:
                errors.append(f"{path}: transparent background not detected")
            elif alpha[0] == 255:
                errors.append(f"{path}: transparent background not detected")
            elif alpha[1] == 0:
                errors.append(f"{path}: image is fully transparent")
            else:
                bbox = image.convert("RGBA").getchannel("A").getbbox()
                if bbox is None:
                    errors.append(f"{path}: image is fully transparent")
                else:
                    left, top, right, bottom = bbox
                    bbox_area = (right - left) * (bottom - top)
                    canvas_area = image.size[0] * image.size[1]
                    bbox_ratio = bbox_area / canvas_area
                    if bbox_ratio < MIN_VISIBLE_BBOX_RATIO:
                        errors.append(f"{path}: visible content is too small ({bbox_ratio:.1%} of canvas)")
                    elif bbox_ratio < WARN_VISIBLE_BBOX_RATIO:
                        warnings.append(f"{path}: visible content is small ({bbox_ratio:.1%} of canvas)")
                    margins = (
                        left / image.size[0],
                        top / image.size[1],
                        (image.size[0] - right) / image.size[0],
                        (image.size[1] - bottom) / image.size[1],
                    )
                    if max(margins) > WARN_MARGIN_RATIO:
                        warnings.append(f"{path}: transparent margin exceeds {WARN_MARGIN_RATIO:.0%}")
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


def validate_content_image(path: Path, asset_type: str) -> tuple[list[str], list[str]]:
    if asset_type == "animation-emoji":
        return validate_animation_image(path, EMOJI_CONTENT_SIZE, "content image")
    if asset_type == "static-sticker":
        return validate_static_image(
            path,
            "content image",
            max_size=STICKER_CONTENT_MAX_SIZE,
            require_even_size=True,
        )
    return validate_static_image(path, "content image", expected_size=EMOJI_CONTENT_SIZE)


def validate_tab_image(path: Path) -> tuple[list[str], list[str]]:
    return validate_static_image(path, "tab image", expected_size=TAB_SIZE)


def validate_main_image(path: Path) -> tuple[list[str], list[str]]:
    return validate_static_image(path, "main image", expected_size=STICKER_MAIN_SIZE)


def submission_expected_names(expected_count: int, asset_type: str) -> set[str]:
    width = content_filename_width(asset_type)
    return {f"{index:0{width}}.png" for index in range(1, expected_count + 1)}


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


def visual_pixel_hash(path: Path) -> str:
    image = first_frame(path)
    digest = hashlib.sha256()
    digest.update(image.tobytes())
    digest.update(str(image.size).encode("ascii"))
    return digest.hexdigest()


def average_hash(path: Path, size: int = 8) -> int:
    image = first_frame(path)
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.alpha_composite(image)
    grayscale = background.convert("L").resize((size, size), Image.Resampling.LANCZOS)
    pixels = list(grayscale.getdata())
    average = sum(pixels) / len(pixels)
    bits = 0
    for pixel in pixels:
        bits = (bits << 1) | int(pixel >= average)
    return bits


def hamming_distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def composited_rgb(path: Path) -> Image.Image:
    image = first_frame(path)
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.alpha_composite(image)
    return background.convert("RGB")


def mean_absolute_rgb_difference(left: Path, right: Path) -> float:
    left_image = composited_rgb(left)
    right_image = composited_rgb(right)
    if left_image.size != right_image.size:
        right_image = right_image.resize(left_image.size, Image.Resampling.LANCZOS)

    total = 0
    count = left_image.size[0] * left_image.size[1] * 3
    for left_pixel, right_pixel in zip(left_image.getdata(), right_image.getdata(), strict=True):
        total += abs(left_pixel[0] - right_pixel[0])
        total += abs(left_pixel[1] - right_pixel[1])
        total += abs(left_pixel[2] - right_pixel[2])
    return total / count


def visual_quality_warnings(path: Path) -> list[str]:
    warnings: list[str] = []
    try:
        image = first_frame(path)
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: cannot inspect visual quality: {exc}"]

    visible_luminance: list[int] = []
    visible_colors: set[tuple[int, int, int]] = set()
    for red, green, blue, alpha in image.getdata():
        if alpha == 0:
            continue
        visible_colors.add((red, green, blue))
        visible_luminance.append(round((0.2126 * red) + (0.7152 * green) + (0.0722 * blue)))

    if not visible_luminance:
        return warnings

    luminance_range = max(visible_luminance) - min(visible_luminance)
    if luminance_range < LOW_CONTRAST_RANGE:
        warnings.append(f"{path}: low contrast visible content (luminance range {luminance_range})")
    if len(visible_colors) < LOW_COLOR_VARIETY_COUNT:
        warnings.append(f"{path}: low color variety ({len(visible_colors)} visible colors)")
    return warnings


def collection_quality_warnings(images: list[Path]) -> list[str]:
    warnings: list[str] = []
    visual_hashes: dict[str, Path] = {}
    perceptual_hashes: list[tuple[Path, int]] = []
    warned_near_duplicates: set[Path] = set()

    for path in images:
        warnings.extend(visual_quality_warnings(path))
        try:
            digest = visual_pixel_hash(path)
            if digest in visual_hashes:
                warnings.append(f"{path}: duplicate image content matches {visual_hashes[digest]}")
            else:
                visual_hashes[digest] = path
            perceptual_hashes.append((path, average_hash(path)))
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"{path}: cannot inspect duplicate quality: {exc}")

    for index, (path, signature) in enumerate(perceptual_hashes):
        for other_path, other_signature in perceptual_hashes[index + 1 :]:
            if other_path in warned_near_duplicates:
                continue
            if visual_pixel_hash(path) == visual_pixel_hash(other_path):
                continue
            distance = hamming_distance(signature, other_signature)
            mean_abs_diff = mean_absolute_rgb_difference(path, other_path)
            if distance <= NEAR_DUPLICATE_HASH_DISTANCE and mean_abs_diff <= NEAR_DUPLICATE_MEAN_ABS_DIFF:
                warnings.append(f"{other_path}: near-duplicate image content resembles {path} (hash distance {distance})")
                warned_near_duplicates.add(other_path)
    return warnings


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


def validate_zip(path: Path, asset_type: str, expected_count: int | None = None) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: zip file does not exist"]
    max_zip_bytes = zip_limit(asset_type)
    if path.stat().st_size > max_zip_bytes:
        errors.append(f"{path}: exceeds {max_zip_bytes // 1_000_000}MB")
    if not zipfile.is_zipfile(path):
        errors.append(f"{path}: not a valid zip file")
        return errors
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
    for name in names:
        filename = Path(name).name
        if not filename.lower().endswith(".png"):
            errors.append(f"{path}: line upload zip must contain only image files, found {name}")
    if expected_count is not None:
        filenames = {Path(name).name for name in names}
        expected_names = submission_expected_names(expected_count, asset_type) | companion_names(asset_type)
        extra = sorted(filenames - expected_names)
        missing = sorted(expected_names - filenames)
        for name in extra:
            errors.append(f"{path}: unexpected image filename in line upload zip: {name}")
        for name in missing:
            errors.append(f"{path}: missing image filename in line upload zip: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji or sticker image assets.")
    parser.add_argument("images_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--tab-image", type=Path)
    parser.add_argument("--main-image", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--stage", choices=["production", "submission"], default="production")
    parser.add_argument(
        "--asset-type",
        choices=["static", "animation", "static-emoji", "animation-emoji", "static-sticker"],
        default="static-emoji",
    )
    parser.add_argument("--preview-contact-sheet", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        asset_type = normalize_asset_type(args.asset_type)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not args.images_dir.exists():
        errors.append(f"{args.images_dir}: directory does not exist")
    else:
        tab_image = args.tab_image
        main_image = args.main_image
        if args.stage == "submission" and tab_image is None:
            tab_image = args.images_dir / SUBMISSION_TAB_NAME
        if args.stage == "submission" and asset_type == "static-sticker" and main_image is None:
            main_image = args.images_dir / SUBMISSION_MAIN_NAME

        content_images = sorted(
            path
            for path in args.images_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".png"
            and (tab_image is None or path.resolve() != tab_image.resolve())
            and (main_image is None or path.resolve() != main_image.resolve())
            and path.name.lower() != SUBMISSION_TAB_NAME
            and path.name.lower() != SUBMISSION_MAIN_NAME
        )
        count = len(content_images)
        expected_count = args.expected_count
        if expected_count is not None and count != expected_count:
            errors.append(f"{args.images_dir}: expected {expected_count} content images, found {count}")
        elif expected_count is None and count not in ALLOWED_COUNTS:
            errors.append(f"{args.images_dir}: content image count must be one of {sorted(ALLOWED_COUNTS)}, found {count}")
            expected_count = count

        if args.stage == "submission" and expected_count is not None:
            expected_names = submission_expected_names(expected_count, asset_type)
            actual_names = {path.name for path in content_images}
            wrong_names = sorted(actual_names - expected_names)
            missing_names = sorted(expected_names - actual_names)
            for name in wrong_names:
                errors.append(f"{args.images_dir}: invalid submission filename: {name}")
            for name in missing_names:
                errors.append(f"{args.images_dir}: missing submission filename: {name}")

        for image_path in content_images:
            image_errors, image_warnings = validate_content_image(image_path, asset_type)
            errors.extend(image_errors)
            warnings.extend(image_warnings)
        warnings.extend(collection_quality_warnings(content_images))

        if tab_image:
            if not tab_image.exists():
                errors.append(f"{tab_image}: tab image does not exist")
            else:
                image_errors, image_warnings = validate_tab_image(tab_image)
                errors.extend(image_errors)
                warnings.extend(image_warnings)
        elif args.stage == "submission" or asset_type == "static-sticker":
            errors.append("tab image does not exist")

        if asset_type == "static-sticker":
            if main_image is None:
                errors.append("main image does not exist")
            elif not main_image.exists():
                errors.append(f"{main_image}: main image does not exist")
            else:
                image_errors, image_warnings = validate_main_image(main_image)
                errors.extend(image_errors)
                warnings.extend(image_warnings)

        if args.preview_contact_sheet:
            try:
                write_contact_sheet(content_images, args.preview_contact_sheet)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{args.preview_contact_sheet}: cannot write contact sheet: {exc}")

    if args.tab_image and not args.images_dir.exists():
        image_errors, image_warnings = validate_tab_image(args.tab_image)
        errors.extend(image_errors)
        warnings.extend(image_warnings)

    if args.main_image and not args.images_dir.exists():
        image_errors, image_warnings = validate_main_image(args.main_image)
        errors.extend(image_errors)
        warnings.extend(image_warnings)

    if args.zip_path:
        errors.extend(validate_zip(args.zip_path, asset_type, args.expected_count if args.stage == "submission" else None))

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
