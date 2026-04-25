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

FORBIDDEN_WORDS = [
    "キャンペーン",
    "割引",
    "セール",
    "無料",
    "プレゼント",
    "Twitter",
    "Instagram",
    "TikTok",
    "YouTube",
]

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji submission metadata.")
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "schemas" / "submission-metadata.schema.json")
    args = parser.parse_args()

    data = yaml.safe_load(args.metadata.read_text(encoding="utf-8"))
    schema = yaml.safe_load(args.schema.read_text(encoding="utf-8"))

    errors: list[str] = []
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        where = ".".join(str(part) for part in exc.path) or "<root>"
        errors.append(f"{where}: {exc.message}")

    for key, limit in LIMITS.items():
        value = str(data.get(key, ""))
        length = line_length(value)
        if length > limit:
            errors.append(f"{key}: {length} exceeds LINE count limit {limit}")
        if EMOJI_RE.search(value):
            errors.append(f"{key}: emoji characters are not allowed")

    copyright_value = str(data.get("copyright", ""))
    if not re.fullmatch(r"[A-Za-z0-9 ]+", copyright_value):
        errors.append("copyright: use only ASCII letters, numbers, and spaces")

    combined = "\n".join(str(data.get(key, "")) for key in ("creator_name", "title", "description"))
    for word in FORBIDDEN_WORDS:
        if word and word in combined:
            errors.append(f"metadata: review-risk word found: {word}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("metadata validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
