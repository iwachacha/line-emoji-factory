#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PLACEHOLDER_PATTERNS = [
    re.compile(r"\[[A-Z][A-Z0-9_ -]{2,}\]"),
    re.compile(r"\byour-brand-slug\b"),
    re.compile(r"\bYOUR_BRAND_NAME\b"),
    re.compile(r"\[CREATOR_NAME\]|\[TITLE\]|\[DESCRIPTION\]|\[COPYRIGHT\]"),
]

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "tools", "schemas"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".ps1", ".py", ".txt"}


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated artifacts for unresolved placeholders.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    for file_path in iter_files(args.path):
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.search(line):
                    errors.append(f"{file_path}:{line_no}: unresolved placeholder: {line.strip()}")
                    break

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("placeholder check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
