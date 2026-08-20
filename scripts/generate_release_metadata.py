#!/usr/bin/env python3
"""Generate deterministic MANIFEST.json, SHA256SUMS, and simple catalog indexes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

import yaml

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
EXCLUDED_NAMES = {"MANIFEST.json", "SHA256SUMS"}
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
EXCLUDED_SUFFIXES = {".zip", ".bundle", ".pyc"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def artifact_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name in EXCLUDED_NAMES or path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        yield path


def parse_skill(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"invalid frontmatter mapping: {path}")
    return data


def generate(root: Path, version: str, date: str) -> None:
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    wiki_files = sorted((root / "wiki").glob("*.md"))
    examples = [path for path in (root / "examples").rglob("*") if path.is_file()]

    catalog = []
    for path in skill_files:
        data = parse_skill(path)
        catalog.append({
            "name": data["name"],
            "path": path.relative_to(root).as_posix(),
            "description": data["description"],
        })
    (root / "skill-index.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "entrypoint": "skills/ueas-router/SKILL.md",
                "skills": catalog,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    files = []
    for path in artifact_files(root):
        files.append({
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": digest(path),
        })

    manifest = {
        "schema_version": 2,
        "artifact": "UnrealEngine-Angelscript-Agent-Skills",
        "version": version,
        "generated_at": date,
        "language": ["zh-CN", "en-US-code-identifiers"],
        "entrypoints": {
            "readme": "README.md",
            "agent": "AGENTS.md",
            "router": "skills/ueas-router/SKILL.md",
            "project_context": "skills/ueas-project-context/SKILL.md",
            "wiki": "wiki/Home.md",
        },
        "source_locks": ["sources.lock.json", "sources/ecosystem-skills.lock.json"],
        "validation": {
            "skills": "python scripts/validate_skills.py",
            "package": "python tools/validate_kit.py .",
            "evals": "python scripts/validate_evals.py",
            "source_refs": "python scripts/check_source_refs.py",
            "unit_tests": "python -m unittest discover -s tests -v",
        },
        "counts": {
            "files": len(files),
            "skills": len(skill_files),
            "wiki_markdown": len(wiki_files),
            "examples": len(examples),
        },
        "integrity_file": "SHA256SUMS",
    }
    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    checksum_lines = [f"{item['sha256']}  {item['path']}" for item in files]
    (root / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--version", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    generate(args.root.resolve(), args.version, args.date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
