from __future__ import annotations

import subprocess

from PIL import Image

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


def test_contact_sheet_preview_is_generated(tmp_path):
    images = tmp_path / "images"
    for index in range(1, 9):
        write_png(images / f"{index:03}.png", (180, 180))
    write_png(images / "tab.png", (96, 74))
    contact_sheet = tmp_path / "report" / "contact-sheet.png"

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
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert contact_sheet.exists()
    with Image.open(contact_sheet) as preview:
        assert preview.size[0] >= 180 + 48 + 32 + 24
        assert preview.size[1] >= 180 * 8


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
