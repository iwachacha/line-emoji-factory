from __future__ import annotations

import subprocess

from conftest import PYTHON, ROOT, run_cmd_args, valid_metadata, write_yaml


def run_metadata(path):
    return subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-metadata.py", path),
        text=True,
        capture_output=True,
    )


def test_valid_metadata_passes(tmp_path):
    path = tmp_path / "metadata.yaml"
    write_yaml(path, valid_metadata())
    result = run_metadata(path)
    assert result.returncode == 0, result.stderr


def test_too_long_title_emoji_and_bad_copyright_fail(tmp_path):
    data = valid_metadata()
    data["title"] = "A" * 41
    data["description"] = "hello 😊"
    data["copyright"] = "テスト"
    path = tmp_path / "metadata.yaml"
    write_yaml(path, data)

    result = run_metadata(path)
    assert result.returncode != 0
    assert "title" in result.stderr
    assert "emoji characters are not allowed" in result.stderr
    assert "copyright" in result.stderr


def test_promotion_keyword_is_warning(tmp_path):
    data = valid_metadata()
    data["description"] = "Free campaign reaction set."
    path = tmp_path / "metadata.yaml"
    write_yaml(path, data)

    result = run_metadata(path)
    assert result.returncode == 0, result.stderr
    assert "warning:" in result.stderr
    assert "review-risk keyword" in result.stderr

    strict = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "validate-metadata.py", path, "--warnings-as-errors"),
        text=True,
        capture_output=True,
    )
    assert strict.returncode != 0
    assert "review-risk keyword" in strict.stderr


def test_external_service_keyword_is_error(tmp_path):
    data = valid_metadata()
    data["description"] = "Works with Discord reactions."
    path = tmp_path / "metadata.yaml"
    write_yaml(path, data)

    result = run_metadata(path)
    assert result.returncode != 0
    assert "hard-ng keyword" in result.stderr
    assert "Discord" in result.stderr


def test_review_risk_keywords_can_be_externalized(tmp_path):
    data = valid_metadata()
    data["description"] = "Includes a custom-watch term."
    metadata_path = tmp_path / "metadata.yaml"
    keywords_path = tmp_path / "keywords.yaml"
    write_yaml(metadata_path, data)
    write_yaml(keywords_path, {"keywords": ["custom-watch"]})

    result = subprocess.run(
        run_cmd_args(
            PYTHON,
            ROOT / "tools" / "validate-metadata.py",
            metadata_path,
            "--risk-keywords",
            keywords_path,
        ),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "custom-watch" in result.stderr
