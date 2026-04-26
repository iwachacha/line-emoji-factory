#!/usr/bin/env python
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".venv", "__pycache__"}
CRITICAL_MARKDOWN = {
    Path("README.md"): 20,
    Path("AGENTS.md"): 20,
    Path("PROJECT_MAP.md"): 20,
}
SOURCE_MARKDOWN_DIRS = {
    "docs",
    "rules",
    "workflows",
    "skills",
    "templates",
}
YAML_DIRS = {
    ".github",
    "examples",
    "rules",
    "templates",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def tracked_like_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def in_root_dir(path: Path, names: set[str]) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in names


def check_python(path: Path, errors: list[str]) -> None:
    lines = read_lines(path)
    if len(lines) < 5:
        errors.append(f"{rel(path)}: Python file is too short; possible collapsed source")
    if lines and lines[0].startswith("#!") and (" import " in lines[0] or "from __future__" in lines[0]):
        errors.append(f"{rel(path)}: shebang and code appear collapsed on line 1")

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        errors.append(f"{rel(path)}: syntax error: {exc}")
        return

    if path.parent == ROOT / "tools":
        has_main = any(isinstance(node, ast.FunctionDef) and node.name == "main" for node in tree.body)
        if not has_main:
            errors.append(f"{rel(path)}: tool file does not define main()")


def check_yaml(path: Path, errors: list[str]) -> None:
    lines = read_lines(path)
    if len(lines) < 2:
        errors.append(f"{rel(path)}: YAML file is too short; possible collapsed source")
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{rel(path)}: invalid YAML: {exc}")


def check_json(path: Path, errors: list[str]) -> None:
    lines = read_lines(path)
    if path.parent == ROOT / "schemas" and len(lines) <= 1:
        errors.append(f"{rel(path)}: JSON schema must be multi-line for reviewability")
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(path)}: invalid JSON: {exc}")


def check_markdown(path: Path, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    min_lines = CRITICAL_MARKDOWN.get(relative)
    if min_lines is None and in_root_dir(path, SOURCE_MARKDOWN_DIRS):
        min_lines = 3
    if min_lines is not None and len(read_lines(path)) < min_lines:
        errors.append(f"{rel(path)}: too few lines; possible collapsed documentation")


def check_requirements(path: Path, errors: list[str]) -> None:
    lines = [line.strip() for line in read_lines(path) if line.strip() and not line.strip().startswith("#")]
    if len(lines) < 3:
        errors.append("requirements-dev.txt: expected one dependency per line")
    for line in lines:
        if len(line.split()) > 1 or "," in line or ";" in line:
            errors.append(f"requirements-dev.txt: dependency line must contain one package only: {line}")


def main() -> int:
    errors: list[str] = []
    for path in tracked_like_files():
        suffix = path.suffix.lower()
        if suffix == ".py":
            check_python(path, errors)
        elif suffix in {".yaml", ".yml"} and in_root_dir(path, YAML_DIRS):
            check_yaml(path, errors)
        elif suffix == ".json" and path.parent == ROOT / "schemas":
            check_json(path, errors)
        elif suffix == ".md":
            check_markdown(path, errors)

    workflow_dir = ROOT / ".github" / "workflows"
    for workflow in sorted(workflow_dir.glob("*.yml")):
        if len(read_lines(workflow)) < 2:
            errors.append(f"{rel(workflow)}: workflow file is too short; possible collapsed source")

    requirements = ROOT / "requirements-dev.txt"
    if requirements.exists():
        check_requirements(requirements, errors)
    else:
        errors.append("requirements-dev.txt: missing")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("source integrity check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
