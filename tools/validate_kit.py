#!/usr/bin/env python3
"""Validate the UE-AS Agent Kit without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {
            ".md", ".json", ".py", ".ps1", ".sh", ".as", ".h", ".cpp"
        }:
            yield path


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(text.replace("\r\n", "\n"))
    if not match:
        return None

    result: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "README.md",
        "AGENTS.md",
        "sources.lock.json",
        "skills/ueas-router/SKILL.md",
        "wiki/Home.md",
    ]
    for rel in required:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    skill_names: dict[str, Path] = {}
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found")

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        rel = path.relative_to(root)
        if frontmatter is None:
            errors.append(f"{rel}: missing or invalid YAML-like frontmatter")
            continue

        allowed = {"name", "description"}
        extra = set(frontmatter) - allowed
        if extra:
            warnings.append(f"{rel}: non-standard frontmatter keys: {sorted(extra)}")

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if not name:
            errors.append(f"{rel}: missing frontmatter name")
        if not description:
            errors.append(f"{rel}: missing frontmatter description")
        if name and name != path.parent.name:
            errors.append(
                f"{rel}: name '{name}' does not match directory '{path.parent.name}'"
            )
        if name in skill_names:
            errors.append(
                f"duplicate skill name '{name}': "
                f"{skill_names[name].relative_to(root)} and {rel}"
            )
        elif name:
            skill_names[name] = path

    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)

        if path.suffix.lower() == ".md":
            fences = len(FENCE_RE.findall(text))
            if fences % 2 != 0:
                errors.append(f"{rel}: unbalanced fenced code blocks ({fences})")

            for target in LINK_RE.findall(text):
                target = target.strip().split(maxsplit=1)[0].strip("<>")
                if (
                    not target
                    or target.startswith(("#", "http://", "https://", "mailto:", "sandbox:"))
                ):
                    continue
                target_path = target.split("#", 1)[0]
                if not target_path:
                    continue
                resolved = (path.parent / target_path).resolve()
                try:
                    resolved.relative_to(root.resolve())
                except ValueError:
                    errors.append(f"{rel}: link escapes kit root: {target}")
                    continue
                if not resolved.exists():
                    errors.append(f"{rel}: broken relative link: {target}")

        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON: {exc}")

    source_lock = root / "sources.lock.json"
    if source_lock.exists():
        data = json.loads(source_lock.read_text(encoding="utf-8"))
        if not data.get("sources"):
            errors.append("sources.lock.json: no sources")
        for source in data.get("sources", []):
            if source.get("kind", "").startswith("git") and not source.get("commit"):
                if source.get("id") not in {"vscode-ueas"}:
                    warnings.append(
                        f"sources.lock.json: git source {source.get('id')} has no commit"
                    )

    manifest_path = root / "MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in manifest.get("files", []):
            rel = item.get("path")
            expected = item.get("sha256")
            if not rel or not expected:
                errors.append("MANIFEST.json: entry missing path or sha256")
                continue
            path = root / rel
            if not path.is_file():
                errors.append(f"MANIFEST.json: missing file {rel}")
            elif sha256(path) != expected:
                errors.append(f"MANIFEST.json: hash mismatch {rel}")

    sums_path = root / "SHA256SUMS"
    if sums_path.exists():
        for line_number, line in enumerate(
            sums_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.strip():
                continue
            try:
                expected, rel = line.split("  ", 1)
            except ValueError:
                errors.append(f"SHA256SUMS:{line_number}: invalid format")
                continue
            path = root / rel
            if not path.is_file():
                errors.append(f"SHA256SUMS:{line_number}: missing {rel}")
            elif sha256(path) != expected:
                errors.append(f"SHA256SUMS:{line_number}: hash mismatch {rel}")

    if len(skill_files) < 8:
        warnings.append(f"only {len(skill_files)} skills found; routing may be too coarse")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Kit root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2

    errors, warnings = validate(root)
    print(f"Validated: {root}")
    print(f"Skills: {len(list((root / 'skills').glob('*/SKILL.md')))}")
    print(f"Markdown: {len(list(root.rglob('*.md')))}")
    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
