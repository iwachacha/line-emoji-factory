from __future__ import annotations

import subprocess

from conftest import PYTHON, ROOT, run_cmd_args, write_png


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
