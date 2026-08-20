#!/usr/bin/env python3
"""Check UE-AS/EmmsUI source-path references for safe format and optional existence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

SOURCE_RE = re.compile(
    r"(?P<path>(?:Engine/(?:Source|Plugins/Angelscript)|Plugins/EmmsUI)/"
    r"[A-Za-z0-9_.+\-/]+(?:\.(?:h|hpp|cpp|inl|cs|ini|uplugin|ush|usf|as))?)"
)
TRAILING = ".,;:)]}`'\""


def markdown_files(root: Path) -> Iterable[Path]:
    for base in (root / "skills", root / "wiki", root / "docs", root / "references"):
        if not base.exists():
            continue
        yield from base.rglob("*.md")


def resolve_ref(ref: str, engine_root: Path | None, emmsui_root: Path | None) -> Path | None:
    if ref.startswith("Engine/"):
        return engine_root / ref if engine_root else None
    if ref.startswith("Plugins/EmmsUI/"):
        suffix = ref.removeprefix("Plugins/EmmsUI/")
        return emmsui_root / suffix if emmsui_root else None
    return None


def check(
    root: Path,
    *,
    engine_root: Path | None = None,
    emmsui_root: Path | None = None,
    require_roots: bool = False,
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    stats = {"references": 0, "existence_checked": 0, "files": 0}

    if require_roots:
        if engine_root is None or not (engine_root / "Engine").is_dir():
            errors.append("--require-roots needs --engine-root pointing to a directory containing Engine/")
        if emmsui_root is None or not (emmsui_root / "EmmsUI.uplugin").is_file():
            errors.append("--require-roots needs --emmsui-root pointing to the EmmsUI plugin root")
        if errors:
            return errors, stats

    for path in markdown_files(root):
        stats["files"] += 1
        text = path.read_text(encoding="utf-8")
        for match in SOURCE_RE.finditer(text):
            ref = match.group("path").rstrip(TRAILING)
            stats["references"] += 1
            rel = path.relative_to(root)
            if ".." in Path(ref).parts:
                errors.append(f"{rel}: source reference escapes its root: {ref}")
                continue
            if "//" in ref or "\\" in ref:
                errors.append(f"{rel}: use normalized forward-slash source references: {ref}")
                continue
            resolved = resolve_ref(ref, engine_root, emmsui_root)
            if resolved is not None:
                stats["existence_checked"] += 1
                if not resolved.exists():
                    errors.append(f"{rel}: referenced source path does not exist: {ref}")

    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--engine-root", type=Path)
    parser.add_argument("--emmsui-root", type=Path)
    parser.add_argument("--require-roots", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    engine_root = args.engine_root.resolve() if args.engine_root else None
    emmsui_root = args.emmsui_root.resolve() if args.emmsui_root else None
    errors, stats = check(
        root,
        engine_root=engine_root,
        emmsui_root=emmsui_root,
        require_roots=args.require_roots,
    )
    print(f"[source-refs] markdown files: {stats['files']}")
    print(f"[source-refs] references: {stats['references']}")
    print(f"[source-refs] existence checked: {stats['existence_checked']}")
    if stats["references"] and not stats["existence_checked"]:
        print("[source-refs] format-only mode; provide source roots for existence checks")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"[source-refs] errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
