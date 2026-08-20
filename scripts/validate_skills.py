#!/usr/bin/env python3
"""Strict validation for Agent Skills frontmatter, routing metadata, and links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

import yaml

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ALLOWED_TOP_LEVEL = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
POSITIVE_MARKERS = ("use when", "用于", "适用于", "当任务", "when ")
NEGATIVE_MARKERS = ("do not use", "don't use", "不要用于", "不适用于", "skip for")


class ValidationStats:
    def __init__(self, skills: int, markdown_files: int, openai_metadata_files: int) -> None:
        self.skills = skills
        self.markdown_files = markdown_files
        self.openai_metadata_files = openai_metadata_files


def read_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "missing YAML frontmatter delimited by ---", text
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}", text
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping", text
    return data, None, text


def iter_markdown(root: Path) -> Iterable[Path]:
    ignored = {".git", ".venv", "__pycache__", "node_modules"}
    for path in root.rglob("*.md"):
        if any(part in ignored for part in path.parts):
            continue
        yield path


def resolve_local_link(source: Path, root: Path, raw_target: str) -> tuple[Path | None, str | None]:
    target = raw_target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None, None
    if " " in target and not target.startswith("<"):
        target = target.split(" ", 1)[0]
    target = unquote(target.strip("<>"))
    target = target.split("#", 1)[0]
    if not target:
        return None, None
    candidate = (source.parent / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return candidate, "link escapes repository root"
    return candidate, None


def validate_openai_metadata(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(root)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"{rel}: invalid YAML: {exc}"]
    if not isinstance(data, dict) or not isinstance(data.get("interface"), dict):
        return [f"{rel}: expected an interface mapping"]
    interface = data["interface"]
    for key in ("display_name", "short_description"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{rel}: interface.{key} must be a non-empty string")
    default_prompt = interface.get("default_prompt")
    if default_prompt is not None and not isinstance(default_prompt, str):
        errors.append(f"{rel}: interface.default_prompt must be a string")
    return errors


def validate_repo(root: Path) -> tuple[list[str], list[str], ValidationStats]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skills_root = root / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    names: dict[str, Path] = {}

    if not skill_files:
        errors.append("no skills found under skills/<name>/SKILL.md")

    for path in skill_files:
        rel = path.relative_to(root)
        frontmatter, error, text = read_frontmatter(path)
        if error:
            errors.append(f"{rel}: {error}")
            continue
        assert frontmatter is not None

        extra = sorted(set(frontmatter) - ALLOWED_TOP_LEVEL)
        if extra:
            errors.append(f"{rel}: unsupported top-level frontmatter fields: {extra}")

        name = frontmatter.get("name")
        description = frontmatter.get("description")
        compatibility = frontmatter.get("compatibility")
        metadata = frontmatter.get("metadata")

        if not isinstance(name, str) or not name:
            errors.append(f"{rel}: name must be a non-empty string")
        else:
            if len(name) > 64:
                errors.append(f"{rel}: name exceeds 64 characters")
            if not NAME_RE.fullmatch(name):
                errors.append(f"{rel}: name must use lowercase letters, digits, and single hyphens")
            if name != path.parent.name:
                errors.append(f"{rel}: name '{name}' does not match directory '{path.parent.name}'")
            if name in names:
                errors.append(
                    f"duplicate skill name '{name}': {names[name].relative_to(root)} and {rel}"
                )
            names[name] = path

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{rel}: description must be a non-empty string")
        else:
            normalized = description.strip().lower()
            if len(description) > 1024:
                errors.append(f"{rel}: description exceeds 1024 characters")
            if not any(marker in normalized for marker in POSITIVE_MARKERS):
                errors.append(f"{rel}: description must state when the Skill should be used")
            if not any(marker in normalized for marker in NEGATIVE_MARKERS):
                errors.append(f"{rel}: description must state the nearest task it should not own")

        if compatibility is not None:
            if not isinstance(compatibility, str):
                errors.append(f"{rel}: compatibility must be a string")
            elif len(compatibility) > 500:
                errors.append(f"{rel}: compatibility exceeds 500 characters")

        if metadata is not None:
            if not isinstance(metadata, dict):
                errors.append(f"{rel}: metadata must be a mapping")
            else:
                for key, value in metadata.items():
                    if not isinstance(key, str) or not isinstance(value, (str, int, float, bool)):
                        errors.append(
                            f"{rel}: metadata must contain scalar string-keyed values; bad key {key!r}"
                        )

        body_lines = text.count("\n") + 1
        if body_lines > 500:
            errors.append(f"{rel}: {body_lines} lines exceeds the 500-line activation limit")
        elif body_lines > 350:
            warnings.append(f"{rel}: {body_lines} lines exceeds the 350-line repository target")

        openai_path = path.parent / "agents" / "openai.yaml"
        if openai_path.exists():
            errors.extend(validate_openai_metadata(openai_path, root))

    markdown_files = sorted(iter_markdown(root))
    for path in markdown_files:
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2:
            errors.append(f"{rel}: unbalanced fenced code blocks")
        for raw in LINK_RE.findall(text):
            candidate, link_error = resolve_local_link(path, root, raw)
            if link_error:
                errors.append(f"{rel}: {link_error}: {raw}")
            elif candidate is not None and not candidate.exists():
                errors.append(f"{rel}: broken local link: {raw}")

    openai_files = sorted(root.glob("skills/*/agents/openai.yaml"))
    return errors, warnings, ValidationStats(
        skills=len(skill_files),
        markdown_files=len(markdown_files),
        openai_metadata_files=len(openai_files),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root)
    errors, warnings, stats = validate_repo(root)

    print(f"[validate-skills] skills: {stats.skills}")
    print(f"[validate-skills] markdown: {stats.markdown_files}")
    print(f"[validate-skills] agents/openai.yaml: {stats.openai_metadata_files}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"[validate-skills] warnings: {len(warnings)}; errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
