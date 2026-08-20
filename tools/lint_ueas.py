#!/usr/bin/env python3
"""Conservative static lint for UE-AS and EmmsUI project patterns.

This is a heuristic review aid, not a compiler. Findings are warnings unless a
clear structural mismatch (such as unbalanced mm Begin/End in one file) is seen.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

BEGIN_END_PAIRS = {
    "BeginHorizontalBox": "EndHorizontalBox",
    "BeginVerticalBox": "EndVerticalBox",
    "BeginScrollBox": "EndScrollBox",
    "BeginBorder": "EndBorder",
    "BeginSizeBox": "EndSizeBox",
}


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add(findings: list[dict[str, Any]], path: Path, text: str, match: re.Match[str],
        code: str, severity: str, message: str) -> None:
    findings.append({
        "path": str(path),
        "line": line_number(text, match.start()),
        "code": code,
        "severity": severity,
        "message": message,
        "excerpt": match.group(0)[:160],
    })


def lint_file(path: Path, root: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings: list[dict[str, Any]] = []
    rel = path.relative_to(root)

    patterns = [
        (
            re.compile(r"\w+\s*->\s*\w+"),
            "ueas.cpp_pointer_syntax",
            "high",
            "C++ pointer member syntax found; UE-AS UObject access normally uses '.'."
        ),
        (
            re.compile(r"\bStaticClass\s*\(\s*\)"),
            "ueas.static_class",
            "medium",
            "StaticClass() may be deprecated/disallowed by project settings; prefer class literals when supported."
        ),
        (
            re.compile(r"\bGetUnderlyingWidget\s*\("),
            "emmsui.underlying_widget",
            "medium",
            "Underlying UWidget changes bypass EmmsUI diff/reset and the object may be rebuilt."
        ),
        (
            re.compile(r"\bGameplay::GetAllActorsOfClass\s*\("),
            "ueas.global_actor_scan",
            "medium",
            "Review call frequency; never run an unbounded world scan every Draw/Tick without caching."
        ),
        (
            re.compile(r"\bUFUNCTION\s*\([^)]*\bReliable\b[^)]*\)"),
            "network.reliable_rpc",
            "info",
            "Confirm frequency and backpressure for Reliable RPC."
        ),
        (
            re.compile(r"\bmm::EditableText(?:Box)?\s*\(\s*[A-Za-z_]\w*\s*\)"),
            "emmsui.input_state",
            "info",
            "Confirm the referenced input value is persistent across Draws."
        ),
        (
            re.compile(
                r"UFUNCTION\s*\([^)]*\)\s*[^;{}]{0,500}?"
                r"\([^)]*\bSelf\b[^)]*\)",
                re.IGNORECASE,
            ),
            "ueas.reflected_self_parameter",
            "high",
            "Reflected/Blueprint function parameters cannot be named Self on the current UE-AS baseline."
        ),
    ]

    for pattern, code, severity, message in patterns:
        for match in pattern.finditer(text):
            add(findings, rel, text, match, code, severity, message)

    # Editor types outside obvious Editor-only locations.
    if not any(part in {"Editor", "Dev", "Examples"} for part in rel.parts):
        for match in re.finditer(
            r"\b(?:UMMEditorUtilityTab|UScriptEditorSubsystem|UDetailsView|"
            r"UMMClassDetailCustomization|UMMScriptStructDetailCustomization)\b",
            text,
        ):
            before = text[:match.start()]
            guarded = before.rfind("#if EDITOR") > before.rfind("#endif")
            if not guarded:
                add(
                    findings, rel, text, match,
                    "ueas.editor_type_runtime_path", "high",
                    "Editor-only type appears outside an Editor directory and outside a visible #if EDITOR guard."
                )

    # Simple per-file panel count. It cannot reason across wrappers, so warn only.
    for begin, end in BEGIN_END_PAIRS.items():
        begin_count = len(re.findall(rf"\bmm::{begin}\s*\(", text))
        end_count = len(re.findall(rf"\bmm::{end}\s*\(", text))
        if begin_count != end_count:
            findings.append({
                "path": str(rel),
                "line": 1,
                "code": "emmsui.begin_end_count",
                "severity": "high",
                "message": f"{begin} count {begin_count} != {end} count {end_count}.",
            })

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("script_root", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--fail-on", choices=["none", "high", "medium"], default="none")
    args = parser.parse_args()

    root = args.script_root.resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    findings: list[dict[str, Any]] = []
    files = sorted(root.rglob("*.as"))
    for path in files:
        findings.extend(lint_file(path, root))

    report = {
        "schema_version": 1,
        "files_scanned": len(files),
        "findings": findings,
        "note": "Heuristic only; confirm every finding against the pinned UE-AS/EmmsUI compiler and project conventions."
    }
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")

    threshold = {"none": 999, "high": 3, "medium": 2}[args.fail_on]
    rank = {"info": 1, "medium": 2, "high": 3}
    return 1 if any(rank.get(f["severity"], 0) >= threshold for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
