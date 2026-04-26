#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_SKILLS = {
    "line-emoji-producer",
    "line-emoji-doc-auditor",
    "line-emoji-improvement-auditor",
    "line-emoji-factory-evolver",
    "line-emoji-skill-builder",
}
CANONICAL_SKILLS = {
    "line-emoji-router",
    "line-emoji-market-scout",
    "line-emoji-brand-distiller",
    "line-emoji-set-architect",
    "line-emoji-production-director",
    "line-emoji-asset-validator",
    "line-emoji-submission-auditor",
    "line-emoji-release-packager",
    "line-emoji-ip-governor",
    "line-emoji-post-release-analyst",
    "line-emoji-factory-auditor",
}
OLD_ROOT_TEMPLATES = {
    "templates/brand-repo-manifest-template.yaml",
    "templates/brand-repo-blueprint.md",
    "templates/brand-repo-readme-template.md",
}
REQUIRED_REPO_TEMPLATES = {
    "templates/repo/brand-repo-manifest-template.yaml",
    "templates/repo/brand-repo-blueprint.md",
    "templates/repo/brand-repo-readme-template.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def script_is_wrapper(path: Path) -> bool:
    if not path.exists():
        return True
    text = read(path)
    forbidden = ("New-Item -ItemType Directory", "Write-Template", "Copy-Item", "brand/ip")
    return "tools/init-brand-repo.ps1" in text and not any(token in text for token in forbidden)


def main() -> int:
    errors: list[str] = []

    for doc_name in ("AGENTS.md", "PROJECT_MAP.md"):
        text = read(ROOT / doc_name)
        for skill in OLD_SKILLS:
            if skill in text:
                errors.append(f"{doc_name}: references old canonical skill {skill}")
        for skill in CANONICAL_SKILLS:
            expected = f"skills/{skill}/SKILL.md"
            if expected not in text:
                errors.append(f"{doc_name}: missing canonical skill reference {expected}")

    for skill in OLD_SKILLS:
        path = ROOT / "skills" / skill
        if path.exists():
            skill_file = path / "SKILL.md"
            text = read(skill_file)
            if "Deprecated" not in text and "deprecated" not in text:
                errors.append(f"skills/{skill}: old skill directory exists without a deprecated stub")

    for rel_path in OLD_ROOT_TEMPLATES:
        if (ROOT / rel_path).exists():
            errors.append(f"{rel_path}: old root template must be deleted or moved out of canonical scope")

    for rel_path in REQUIRED_REPO_TEMPLATES:
        if not (ROOT / rel_path).exists():
            errors.append(f"{rel_path}: missing canonical repo template")

    if not script_is_wrapper(ROOT / "scripts" / "init-brand-repo.ps1"):
        errors.append("scripts/init-brand-repo.ps1: must be a thin wrapper around tools/init-brand-repo.ps1")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("canonical drift check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
