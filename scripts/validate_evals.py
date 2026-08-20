#!/usr/bin/env python3
"""Validate routing and behavior eval fixtures for the UE-AS Skill suite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def skill_names(root: Path) -> set[str]:
    return {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}


def validate(root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    known = skill_names(root)
    seen_ids: set[str] = set()
    counts = {"routing": 0, "behavior": 0}

    routing_path = root / "evals" / "routing-cases.json"
    behavior_path = root / "evals" / "behavior-cases.json"

    try:
        routing = load_json(routing_path)
        behavior = load_json(behavior_path)
    except ValueError as exc:
        return [str(exc)], counts

    if not isinstance(routing, dict) or not isinstance(routing.get("cases"), list):
        errors.append(f"{routing_path}: expected object with cases array")
    else:
        categories = {"positive", "boundary", "unrelated"}
        for index, case in enumerate(routing["cases"]):
            prefix = f"{routing_path}: cases[{index}]"
            if not isinstance(case, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            case_id = case.get("id")
            prompt = case.get("prompt")
            expected = case.get("expected_skill")
            category = case.get("category")
            rationale = case.get("rationale")
            if not isinstance(case_id, str) or not case_id:
                errors.append(f"{prefix}: missing id")
            elif case_id in seen_ids:
                errors.append(f"{prefix}: duplicate id '{case_id}'")
            else:
                seen_ids.add(case_id)
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{prefix}: prompt must be non-empty")
            if expected != "none" and expected not in known:
                errors.append(f"{prefix}: unknown expected_skill '{expected}'")
            if category not in categories:
                errors.append(f"{prefix}: invalid category '{category}'")
            if category == "boundary":
                boundary_for = case.get("boundary_for")
                if boundary_for not in known:
                    errors.append(f"{prefix}: boundary_for must name an existing Skill")
            if not isinstance(rationale, str) or not rationale.strip():
                errors.append(f"{prefix}: rationale must be non-empty")
            counts["routing"] += 1

    if not isinstance(behavior, dict) or not isinstance(behavior.get("cases"), list):
        errors.append(f"{behavior_path}: expected object with cases array")
    else:
        for index, case in enumerate(behavior["cases"]):
            prefix = f"{behavior_path}: cases[{index}]"
            if not isinstance(case, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            case_id = case.get("id")
            skill = case.get("skill")
            prompt = case.get("prompt")
            assertions = case.get("assertions")
            forbidden = case.get("forbidden_behaviors")
            if not isinstance(case_id, str) or not case_id:
                errors.append(f"{prefix}: missing id")
            elif case_id in seen_ids:
                errors.append(f"{prefix}: duplicate id '{case_id}'")
            else:
                seen_ids.add(case_id)
            if skill not in known:
                errors.append(f"{prefix}: unknown skill '{skill}'")
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{prefix}: prompt must be non-empty")
            if not isinstance(assertions, list) or len(assertions) < 2 or not all(
                isinstance(value, str) and value.strip() for value in assertions
            ):
                errors.append(f"{prefix}: assertions must contain at least two non-empty strings")
            if not isinstance(forbidden, list) or not forbidden or not all(
                isinstance(value, str) and value.strip() for value in forbidden
            ):
                errors.append(f"{prefix}: forbidden_behaviors must contain non-empty strings")
            counts["behavior"] += 1

    focus = {"ueas-router", "ueas-project-context", "ueas-reflection-blueprint"}
    routed = {
        case.get("expected_skill")
        for case in routing.get("cases", [])
        if isinstance(case, dict) and case.get("category") == "positive"
    }
    behaved = {
        case.get("skill")
        for case in behavior.get("cases", [])
        if isinstance(case, dict)
    }
    for name in sorted(focus):
        if name not in routed:
            errors.append(f"missing positive routing case for focus Skill '{name}'")
        if name not in behaved:
            errors.append(f"missing behavior case for focus Skill '{name}'")

    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    errors, counts = validate(Path(args.root).resolve())
    print(f"[validate-evals] routing cases: {counts['routing']}")
    print(f"[validate-evals] behavior cases: {counts['behavior']}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"[validate-evals] errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
