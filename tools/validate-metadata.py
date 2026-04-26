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

DEFAULT_RISK_KEYWORDS = {
    "hard_ng": {
        "external_services": [
            "Discord",
            "Slack",
            "WhatsApp",
            "Telegram",
            "Messenger",
            "Facebook",
            "Instagram",
            "TikTok",
            "YouTube",
            "Twitter",
            "X",
        ]
    },
    "review": {
        "promotion": [
            "発売",
            "新発売",
            "予約",
            "セール",
            "キャンペーン",
            "期間限定",
            "無料",
            "プレゼント",
            "割引",
            "campaign",
            "discount",
            "free",
            "giveaway",
            "sale",
        ],
        "personal_targeting": ["専用", "さんへ", "ちゃんへ", "くんへ"],
        "corporate_logo_like": ["ロゴ", "公式"],
    },
}

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


def flatten_keyword_groups(value) -> list[tuple[str, str]]:
    keywords: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for category, child in value.items():
            for child_category, keyword in flatten_keyword_groups(child):
                label = str(category) if not child_category else f"{category}.{child_category}"
                keywords.append((label, keyword))
    elif isinstance(value, list):
        for item in value:
            keyword = str(item).strip()
            if keyword:
                keywords.append(("", keyword))
    elif value is not None:
        keyword = str(value).strip()
        if keyword:
            keywords.append(("", keyword))
    return keywords


def load_risk_keywords(path: Path | None) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    data = DEFAULT_RISK_KEYWORDS if path is None else load_yaml(path)
    if not isinstance(data, dict):
        return [], flatten_keyword_groups(data)
    if "keywords" in data:
        return [], flatten_keyword_groups(data.get("keywords", []))
    hard_ng = flatten_keyword_groups(data.get("hard_ng", {}))
    review = flatten_keyword_groups(data.get("review", {}))
    return hard_ng, review


def discover_risk_keyword_path(metadata_path: Path, cli_path: Path | None) -> Path | None:
    if cli_path is not None:
        if not cli_path.exists():
            raise ValueError(f"{cli_path}: risk keyword file does not exist")
        return cli_path

    candidates: list[Path] = []
    for parent in [metadata_path.parent, *metadata_path.parents]:
        candidates.append(parent / "rules" / "review-risk-keywords.yaml")
        candidates.append(parent / "references" / "shared" / "review-risk-keywords.yaml")
        if (parent / "brand-manifest.yaml").exists():
            break
    candidates.append(Path(__file__).resolve().parents[1] / "rules" / "review-risk-keywords.yaml")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def validate_schema(data: dict, schema_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]


def keyword_found(keyword: str, text: str) -> bool:
    if keyword.isascii():
        if len(keyword) == 1:
            return re.search(rf"(?<![A-Za-z0-9]){re.escape(keyword)}(?![A-Za-z0-9])", text, re.IGNORECASE) is not None
        return keyword.lower() in text.lower()
    return keyword in text


def validate_metadata(
    data: dict,
    hard_ng_keywords: list[tuple[str, str]],
    review_keywords: list[tuple[str, str]],
) -> tuple[list[str], list[str]]:
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
    if copyright_value and not re.fullmatch(r"[A-Za-z0-9]+", copyright_value):
        errors.append("copyright: use only ASCII letters and numbers")

    combined = "\n".join(str(data.get(key, "")) for key in ("creator_name", "title", "description"))
    for category, keyword in hard_ng_keywords:
        if keyword_found(keyword, combined):
            label = f" ({category})" if category else ""
            errors.append(f"metadata: hard-ng keyword found{label}: {keyword}")
    for category, keyword in review_keywords:
        if keyword_found(keyword, combined):
            label = f" ({category})" if category else ""
            warnings.append(f"metadata: review-risk keyword found{label}: {keyword}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LINE emoji submission metadata.")
    parser.add_argument("metadata", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas" / "submission-metadata.schema.json",
    )
    parser.add_argument("--risk-keywords", type=Path)
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    try:
        data = load_yaml(args.metadata)
        if not isinstance(data, dict):
            raise ValueError(f"{args.metadata}: metadata root must be an object")
        risk_path = discover_risk_keyword_path(args.metadata.resolve(), args.risk_keywords)
        hard_ng_keywords, review_keywords = load_risk_keywords(risk_path)
        errors = validate_schema(data, args.schema)
        metadata_errors, warnings = validate_metadata(data, hard_ng_keywords, review_keywords)
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
