#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PATH_RE = re.compile(r"`([^`]+)`")
KNOWN_ROOT_FILES = {"AGENTS.md", "PROJECT_MAP.md", "README.md", "requirements-dev.txt"}
KNOWN_PREFIXES = {
    ".github/",
    "docs/",
    "examples/",
    "rules/",
    "schemas/",
    "scripts/",
    "skills/",
    "templates/",
    "tools/",
    "workflows/",
}


def is_path_candidate(value: str) -> bool:
    if any(char in value for char in "*$|"):
        return False
    normalized = value.replace("\\", "/")
    if normalized in KNOWN_ROOT_FILES:
        return True
    return any(normalized.startswith(prefix) for prefix in KNOWN_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that PROJECT_MAP.md path references exist.")
    parser.add_argument("--project-map", type=Path, default=Path("PROJECT_MAP.md"))
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    root = args.root.resolve()
    project_map = args.project_map if args.project_map.is_absolute() else root / args.project_map
    errors: list[str] = []

    if not project_map.exists():
        print(f"missing project map: {project_map}", file=sys.stderr)
        return 1

    for line_no, line in enumerate(project_map.read_text(encoding="utf-8").splitlines(), start=1):
        for match in PATH_RE.finditer(line):
            value = match.group(1).strip()
            if not is_path_candidate(value):
                continue
            candidate = root / value.replace("/", "/")
            if not candidate.exists():
                errors.append(f"{project_map}:{line_no}: missing path reference: {value}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("project map path validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
