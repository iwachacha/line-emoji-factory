#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import jsonschema
import yaml


LIMITS = {
    "creator_name": 50,
    "title": 40,
    "description": 160,
    "copyright": 50,
}

DEFAULT_REVIEW_RISK_KEYWORDS = [
    "campaign",
    "discount",
    "free",
    "giveaway",
    "instagram",
    "sale",
    "tiktok",
    "twitter",
    "youtube",
    "キャンペーン",
    "セール",
    "プレゼント",
    "無料",
    "割引",
]

EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0000FE0F"
    "]"
)


def line_length(value: str) -> int:
    total = 0
    for char in value:
        if ord(char) < 128:
            total += 1
        elif unicodedata.east_asian_width(char) in {"F", "W", "A"}:
            total += 2
        else:
            total += 1
    return total


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"{path}: file does not exist") from None
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc


def load_review_keywords(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return DEFAULT_REVIEW_RISK_KEYWORDS
    data = load_yaml(path)
    if isinstance(data, dict):
        values = data.get("keywords", [])
    else:
        values = data or []
    return [str(value) for value in values if str(value).strip()]


def validate_schema(data: dict, schema_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]


def validate_metadata(data: dict, keywords: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key, limit in LIMITS.items():
        value = str(data.get(key, ""))
        length = line_length(value)
        if length > limit:
            errors.append(f"{key}: {length} exceeds LINE count limit {limit}")
        if EMOJI_RE.search(value):
            errors.append(f"{key}: emoji characters are not allowed")

    copyright_value = str(data.get("copyright", ""))
    if copyright_value and not re.fullmatch(r"[A-Za-z0-9 ]+", copyright_value):
        errors.append("copyright: use only ASCII letters, numbers, and spaces")

    combined = "\n".join(str(data.get(key, "")) for key in ("creator_name", "title", "description")).lower()
    for keyword in keywords:
        if keyword.lower() in combined:
            warnings.append(f"metadata: review-risk keyword found: {keyword}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji submission metadata.")
    parser.add_argument("metadata", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas" / "submission-metadata.schema.json",
    )
    parser.add_argument(
        "--risk-keywords",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "rules" / "review-risk-keywords.yaml",
    )
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    try:
        data = load_yaml(args.metadata)
        if not isinstance(data, dict):
            raise ValueError(f"{args.metadata}: metadata root must be an object")
        keywords = load_review_keywords(args.risk_keywords)
        errors = validate_schema(data, args.schema)
        metadata_errors, warnings = validate_metadata(data, keywords)
        errors.extend(metadata_errors)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if args.warnings_as_errors:
        errors.extend(warnings)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("metadata validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
