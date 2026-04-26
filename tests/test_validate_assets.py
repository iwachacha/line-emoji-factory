from __future__ import annotations

import subprocess
import zipfile

from PIL import Image, ImageDraw

from conftest import PYTHON, ROOT, run_cmd_args, write_apng, write_png


def test_submission_filenames_are_strict(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))
    write_png(images / "tab.png", (96, 74))

    ok = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8", "--stage", "submission"),
        text=True,
        capture_output=True,
    )
    assert ok.returncode == 0, ok.stderr

    (images / "001.png").rename(images / "first.png")
    bad = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8", "--stage", "submission"),
        text=True,
        capture_output=True,
    )
    assert bad.returncode != 0
    assert "invalid submission filename" in bad.stderr


def test_production_allows_arbitrary_filenames(tmp_path):
    images = tmp_path / "images"
    for name in ("ok.png", "thanks.png", "yes.png", "no.png", "hmm.png", "wow.png", "sorry.png", "bye.png"):
        write_png(images / name, (180, 180))

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8", "--stage", "production"),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr


def test_submission_requires_tab_image(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8", "--stage", "submission"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "tab image does not exist" in result.stderr


def test_wrong_size_fails(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        size = (179, 180) if index == 1 else (180, 180)
        write_png(images / f"{index:03}.png", size)

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "expected 180x180" in result.stderr


def test_fully_transparent_and_no_alpha_fail(tmp_path):
    transparent = tmp_path / "transparent"
    for index in range(1, 9):
        write_png(transparent / f"{index:03}.png", (180, 180), fully_transparent=True)

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", transparent, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "fully transparent" in result.stderr

    no_alpha = tmp_path / "no-alpha"
    for index in range(1, 9):
        write_png(no_alpha / f"{index:03}.png", (180, 180), alpha=False)

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", no_alpha, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "transparent background not detected" in result.stderr


def test_near_empty_static_image_fails(tmp_path):
    images = tmp_path / "tiny"
    for index in range(1, 9):
        path = images / f"{index:03}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle((85, 85, 95, 95), fill=(30, 30, 30, 255))
        image.save(path, dpi=(72, 72))

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "visible content is too small" in result.stderr


def test_line_upload_zip_rejects_non_images(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))
    write_png(images / "tab.png", (96, 74))
    zip_path = tmp_path / "images.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        for image in images.glob("*.png"):
            archive.write(image, image.name)
        archive.writestr("metadata.yaml", "title: bad\n")

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            images,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--zip",
            zip_path,
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "must contain only image files" in result.stderr


def test_line_upload_zip_size_limit_is_checked(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))
    write_png(images / "tab.png", (96, 74))
    zip_path = tmp_path / "oversize.zip"
    with zip_path.open("wb") as handle:
        handle.truncate(20_000_001)

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            images,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--zip",
            zip_path,
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "exceeds 20MB" in result.stderr


def test_visual_quality_warnings_cover_duplicates_and_low_detail(tmp_path):
    images = tmp_path / "quality"
    images.mkdir()
    base = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.rectangle((30, 30, 150, 150), fill=(30, 30, 30, 255))
    base.save(images / "001.png", dpi=(72, 72))

    near = base.copy()
    near.putpixel((90, 90), (31, 31, 31, 255))
    near.save(images / "002.png", dpi=(72, 72))

    base.save(images / "003.png", dpi=(72, 72))
    for index in range(4, 9):
        image = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        shade = 20 + index
        draw.rectangle((30, 30, 150, 150), fill=(shade, shade, shade, 255))
        image.save(images / f"{index:03}.png", dpi=(72, 72))

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "duplicate image content" in result.stderr
    assert "near-duplicate image content" in result.stderr
    assert "low contrast visible content" in result.stderr
    assert "low color variety" in result.stderr


def test_visual_quality_near_duplicate_ignores_clear_color_variants(tmp_path):
    images = tmp_path / "color-variants"
    images.mkdir()
    colors = [
        (41, 178, 166, 255),
        (245, 190, 66, 255),
        (83, 183, 102, 255),
        (239, 116, 108, 255),
        (76, 137, 211, 255),
        (145, 111, 214, 255),
        (223, 75, 88, 255),
        (127, 137, 145, 255),
    ]
    for index, color in enumerate(colors, start=1):
        image = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((28, 28, 152, 152), fill=color, outline=(30, 30, 30, 255), width=8)
        draw.rectangle((58, 132, 122, 158), fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=3)
        image.save(images / f"{index:03}.png", dpi=(72, 72))

    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-assets.py", images, "--expected-count", "8"),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "near-duplicate image content" not in result.stderr


def test_contact_sheet_preview_is_generated(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))
    write_png(images / "tab.png", (96, 74))
    contact_sheet = tmp_path / "report" / "contact-sheet.png"
    chat_sheet = tmp_path / "report" / "chat-preview.png"
    report_json = tmp_path / "report" / "asset-validation.json"

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            images,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--preview-contact-sheet",
            contact_sheet,
            "--preview-chat-sheet",
            chat_sheet,
            "--report-json",
            report_json,
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert contact_sheet.exists()
    assert chat_sheet.exists()
    assert report_json.exists()
    with Image.open(contact_sheet) as preview:
        assert preview.size[0] >= 180 + 96 + 48 + 32
        assert preview.size[1] >= 180 * 8
    with Image.open(chat_sheet) as preview:
        assert preview.size[0] >= 260
        assert preview.size[1] >= 72 * 8


def test_animation_apng_validation(tmp_path):
    images = tmp_path / "animation"
    for index in range(1, 9):
        write_apng(images / f"{index:03}.png", frame_count=5, duration=100, loop=1)
    write_png(images / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            images,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "animation",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr

    bad = tmp_path / "animation-bad"
    for index in range(1, 9):
        write_apng(bad / f"{index:03}.png", frame_count=4, duration=100, loop=0)
    write_png(bad / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            bad,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "animation",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "APNG frame count" in result.stderr
    assert "APNG loop count" in result.stderr

    no_alpha = tmp_path / "animation-no-alpha"
    for index in range(1, 9):
        write_apng(no_alpha / f"{index:03}.png", frame_count=5, duration=100, loop=1, alpha=False)
    write_png(no_alpha / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            no_alpha,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "animation",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "transparent background not detected" in result.stderr

    too_long = tmp_path / "animation-too-long"
    for index in range(1, 9):
        write_apng(too_long / f"{index:03}.png", frame_count=5, duration=900, loop=1)
    write_png(too_long / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            too_long,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "animation",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "APNG duration exceeds 4 seconds" in result.stderr

    static_files = tmp_path / "animation-static"
    for index in range(1, 9):
        write_png(static_files / f"{index:03}.png", (180, 180))
    write_png(static_files / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            static_files,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "animation",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "APNG animation not detected" in result.stderr


def test_static_sticker_submission_assets_validate(tmp_path):
    images = tmp_path / "stickers"
    for index in range(1, 9):
        write_png(images / f"{index:02}.png", (300, 240))
    write_png(images / "main.png", (240, 240))
    write_png(images / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            images,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "static-sticker",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr


def test_static_sticker_rejects_oversize_odd_and_missing_main(tmp_path):
    odd = tmp_path / "odd"
    for index in range(1, 9):
        size = (301, 240) if index == 1 else (300, 240)
        write_png(odd / f"{index:02}.png", size)
    write_png(odd / "main.png", (240, 240))
    write_png(odd / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            odd,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "static-sticker",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "must be even numbers" in result.stderr

    oversize = tmp_path / "oversize"
    for index in range(1, 9):
        size = (372, 320) if index == 1 else (300, 240)
        write_png(oversize / f"{index:02}.png", size)
    write_png(oversize / "tab.png", (96, 74))

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-assets.py",
            oversize,
            "--expected-count",
            "8",
            "--stage",
            "submission",
            "--asset-type",
            "static-sticker",
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "expected no larger than 370x320" in result.stderr
    assert "main image does not exist" in result.stderr
