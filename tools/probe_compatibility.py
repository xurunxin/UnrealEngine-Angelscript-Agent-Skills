#!/usr/bin/env python3
"""Static compatibility probe for UnrealEngine-Angelscript + EmmsUI.

This tool intentionally does not claim runtime compatibility. It records exact
versions and checks version-sensitive source signals before a real C++ build,
script compile, hot-reload test, simulate-cooked run, and Cook.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

TEXT_EXTENSIONS = {
    ".h", ".hpp", ".cpp", ".inl", ".cs", ".json", ".uplugin", ".uproject",
    ".ini", ".as", ".md", ".txt",
}
MAX_FILE_SIZE = 5 * 1024 * 1024

KNOWN_UEAS_COMMIT = "546c4d6af141f1e820be1b2976211a756ca2639d"
KNOWN_UNREAL_VERSION = "5.8.1"
KNOWN_EMMSUI_COMMIT = "c5d4e303f1fc8a1545de4d336be19e69dc8518c0"
HISTORICAL_UEAS_COMMIT = "7a77e74edb9d8a16f53caa56754e08589f2ee486"


def git_commit(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        value = result.stdout.strip()
        return value if re.fullmatch(r"[0-9a-fA-F]{40}", value) else None
    except (OSError, subprocess.SubprocessError):
        return None


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def iter_source_files(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        return
    ignored = {".git", "Binaries", "DerivedDataCache", "Intermediate", "Saved"}
    for current, dirs, files in os.walk(root):
        dirs[:] = [directory for directory in dirs if directory not in ignored]
        current_path = Path(current)
        for name in files:
            path = current_path / name
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                if path.stat().st_size <= MAX_FILE_SIZE:
                    yield path
            except OSError:
                continue


def contains(root: Path, needle: str, *, limit: int = 1) -> list[str]:
    matches: list[str] = []
    for path in iter_source_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if needle in text:
            matches.append(str(path.relative_to(root)))
            if len(matches) >= limit:
                break
    return matches


def find_uproject(project_root: Path) -> list[str]:
    return sorted(str(path.relative_to(project_root)) for path in project_root.glob("*.uproject"))


def add_finding(
    findings: list[dict[str, Any]],
    level: str,
    code: str,
    message: str,
    evidence: Any = None,
) -> None:
    item: dict[str, Any] = {"level": level, "code": code, "message": message}
    if evidence is not None:
        item["evidence"] = evidence
    findings.append(item)


def parse_version(value: str | None) -> tuple[int, int, int] | None:
    if not value:
        return None
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def build_report(
    engine: Path,
    emmsui: Path | None = None,
    project: Path | None = None,
) -> dict[str, Any]:
    """Build a static report. Paths should already be resolved by the caller."""

    findings: list[dict[str, Any]] = []
    facts: dict[str, Any] = {
        "engine_root": str(engine),
        "engine_git_commit": git_commit(engine),
    }

    build_version_path = engine / "Engine" / "Build" / "Build.version"
    build_version = read_json(build_version_path)
    facts["unreal_build_version"] = build_version
    version: str | None = None
    if build_version is None:
        add_finding(
            findings,
            "blocker",
            "engine.build_version_missing",
            "Could not read Engine/Build/Build.version.",
        )
    else:
        version = ".".join(
            str(build_version.get(key, "?"))
            for key in ("MajorVersion", "MinorVersion", "PatchVersion")
        )
        facts["unreal_version"] = version
        add_finding(findings, "info", "engine.version", f"Unreal Engine {version}")

    as_plugin_root = engine / "Engine" / "Plugins" / "Angelscript"
    as_plugin = as_plugin_root / "Angelscript.uplugin"
    facts["angelscript_plugin"] = str(as_plugin)
    if not as_plugin.is_file():
        add_finding(
            findings,
            "blocker",
            "ueas.plugin_missing",
            "Engine/Plugins/Angelscript/Angelscript.uplugin was not found.",
        )
    else:
        add_finding(findings, "info", "ueas.plugin_found", "Angelscript plugin found.")

    # Scan the complete plugin so compiler flags in ThirdParty/ are visible.
    feature_checks = {
        "if_handle_then_const": contains(as_plugin_root, "if_handle_then_const"),
        "covariant_template_flag": contains(
            as_plugin_root, "asOBJ_TEMPLATE_SUBTYPE_COVARIANT"
        ),
        "force_link_bindings": contains(as_plugin_root, "AS_FORCE_LINK"),
        "new_iterator_method": contains(as_plugin_root, "Iterate()"),
        "new_iterator_switch": contains(
            as_plugin_root, "angelscript.UseNewIterators"
        ),
    }
    facts["ueas_feature_signals"] = feature_checks
    for key, matches in feature_checks.items():
        add_finding(
            findings,
            "info",
            f"ueas.feature.{key}",
            f"{key}: {'found' if matches else 'not found by heuristic scan'}; "
            "absence alone is not proof of incompatibility.",
            matches,
        )

    engine_has_new_iterators = bool(
        feature_checks["new_iterator_method"]
        or feature_checks["new_iterator_switch"]
    )
    facts["ueas_new_iterator_protocol_detected"] = engine_has_new_iterators

    if emmsui is not None:
        facts["emmsui_root"] = str(emmsui)
        facts["emmsui_git_commit"] = git_commit(emmsui)
        uplugin = emmsui / "EmmsUI.uplugin"
        plugin_data = read_json(uplugin)
        facts["emmsui_uplugin"] = plugin_data
        if plugin_data is None:
            add_finding(
                findings,
                "blocker",
                "emmsui.uplugin_missing",
                "Could not read EmmsUI.uplugin.",
            )
        else:
            module_names = [module.get("Name") for module in plugin_data.get("Modules", [])]
            facts["emmsui_modules"] = module_names
            if not {"EmmsUI", "EmmsUIEditor"}.issubset(set(module_names)):
                add_finding(
                    findings,
                    "warning",
                    "emmsui.modules_unexpected",
                    "Expected EmmsUI runtime and EmmsUIEditor modules.",
                    module_names,
                )

        emmsui_signals = {
            "new_iterator_protocol": contains(
                emmsui, "if_handle_then_const Iterate() const"
            )
            or contains(emmsui, "Iterate() const"),
            "mutable_input_state": contains(emmsui, "MirroredValue"),
            "editor_tab_reinstancing": contains(emmsui, "OnObjectsReinstanced"),
            "typed_mm_template": contains(emmsui, "mm<class T>"),
        }
        facts["emmsui_feature_signals"] = emmsui_signals
        emmsui_has_new_iterators = bool(emmsui_signals["new_iterator_protocol"])
        facts["emmsui_new_iterator_protocol_detected"] = emmsui_has_new_iterators

        if engine_has_new_iterators and emmsui_has_new_iterators:
            facts["iterator_protocol_state"] = "source-signals-aligned"
            add_finding(
                findings,
                "info",
                "compat.iterator_protocol_aligned",
                "Both UE-AS and EmmsUI expose the new Iterate() protocol signals. "
                "This removes the old source-gap warning, but a minimal ListView "
                "script compile is still required.",
                {
                    "ueas": feature_checks["new_iterator_method"]
                    or feature_checks["new_iterator_switch"],
                    "emmsui": emmsui_signals["new_iterator_protocol"],
                },
            )
            if feature_checks["covariant_template_flag"]:
                add_finding(
                    findings,
                    "info",
                    "compat.iterator_source_signals_present",
                    "The UE-AS scan found the covariant template signal used by "
                    "the current EmmsUI iterator/template design.",
                    feature_checks["covariant_template_flag"],
                )
            else:
                add_finding(
                    findings,
                    "warning",
                    "compat.iterator_source_signals_incomplete",
                    "Both sides expose Iterate(), but the heuristic UE-AS scan did "
                    "not find the covariant template flag used by current EmmsUI. "
                    "Treat the exact ListView compile as a blocking gate.",
                )
        elif emmsui_has_new_iterators:
            facts["iterator_protocol_state"] = "emmsui-new-engine-signal-missing"
            add_finding(
                findings,
                "warning",
                "compat.iterator_protocol_engine_missing",
                "EmmsUI exposes the new Iterate() protocol, but the heuristic "
                "UE-AS scan did not find the matching engine protocol. Compile a "
                "minimal ListView range-for before proceeding.",
                emmsui_signals["new_iterator_protocol"],
            )
        elif engine_has_new_iterators:
            facts["iterator_protocol_state"] = "engine-new-emmsui-legacy-or-unobserved"
            add_finding(
                findings,
                "warning",
                "compat.iterator_protocol_emmsui_legacy",
                "UE-AS exposes the new iterator protocol, while EmmsUI does not. "
                "The plugin may be an older snapshot; verify its list iterator binds.",
            )
        else:
            facts["iterator_protocol_state"] = "legacy-or-unobserved"
            add_finding(
                findings,
                "info",
                "compat.iterator_protocol_legacy_or_unobserved",
                "Neither side exposed the new iterator signal in the heuristic scan. "
                "Treat the pair as version-specific and compile a minimal ListView.",
            )

        if not emmsui_signals["mutable_input_state"]:
            add_finding(
                findings,
                "warning",
                "emmsui.mutable_input_legacy",
                "MirroredValue was not found; editable text/slider/checkbox "
                "two-way state may use legacy behavior.",
            )

        if not emmsui_signals["editor_tab_reinstancing"]:
            add_finding(
                findings,
                "warning",
                "emmsui.tab_reload_legacy",
                "OnObjectsReinstanced was not found. Test open editor tabs across "
                "structural script hot reload.",
            )

        engine_commit = facts.get("engine_git_commit")
        emmsui_commit = facts.get("emmsui_git_commit")
        if (
            engine_commit == KNOWN_UEAS_COMMIT
            and emmsui_commit == KNOWN_EMMSUI_COMMIT
            and version == KNOWN_UNREAL_VERSION
        ):
            facts["known_snapshot"] = "source-signals-aligned-runtime-unverified"
            add_finding(
                findings,
                "info",
                "compat.known_source_aligned_pair",
                "Observed the Agent Kit 0.1.1 baseline: UE-AS 546c4d6 on UE "
                "5.8.1 with EmmsUI c5d4e30. Their iterator protocol source signals "
                "are aligned; runtime compatibility still requires build and test evidence.",
            )
        elif (
            engine_commit == HISTORICAL_UEAS_COMMIT
            and emmsui_commit == KNOWN_EMMSUI_COMMIT
        ):
            add_finding(
                findings,
                "warning",
                "compat.historical_unverified_pair",
                "This is the superseded UE-AS 5.5.4 plus current EmmsUI pair. "
                "Do not inherit the 0.1.1 source-aligned status.",
            )

        engine_version = parse_version(version)
        if (
            engine_version is not None
            and engine_version < (5, 8, 0)
            and emmsui_has_new_iterators
        ):
            add_finding(
                findings,
                "warning",
                "compat.older_engine_new_emmsui",
                "The engine is older than the observed UE 5.8.x baseline while "
                "EmmsUI uses the new iterator protocol. Backports may work, but the "
                "exact ListView compile test is required before integration.",
            )

    if project is not None:
        facts["project_root"] = str(project)
        facts["uprojects"] = find_uproject(project)
        if not facts["uprojects"]:
            add_finding(
                findings,
                "warning",
                "project.uproject_missing",
                "No .uproject found at project root.",
            )

        script_root = project / "Script"
        facts["script_root_exists"] = script_root.is_dir()
        if not script_root.is_dir():
            add_finding(
                findings,
                "warning",
                "project.script_root_missing",
                "Project Script/ directory was not found.",
            )
        else:
            facts["script_file_count"] = len(list(script_root.rglob("*.as")))

        config_text = ""
        config_root = project / "Config"
        for path in config_root.glob("*.ini") if config_root.is_dir() else []:
            try:
                config_text += path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass
        facts["config_signals"] = {
            "angelscript_settings": "AngelscriptSettings" in config_text,
            "test_settings": "AngelscriptTestSettings" in config_text,
            "integration_test_root": "IntegrationTestMapRoot" in config_text,
        }

    counts = {
        level: sum(1 for finding in findings if finding["level"] == level)
        for level in ("blocker", "warning", "info")
    }
    return {
        "schema_version": 2,
        "tool": "probe_compatibility.py",
        "facts": facts,
        "findings": findings,
        "summary": counts,
        "conclusion": (
            "Static source-signal probe only. A zero-blocker result or a known "
            "source-aligned pair still requires C++ build, script compile, EmmsUI "
            "input/ListView/Tab hot-reload tests, simulate-cooked, and Cook."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine-root", type=Path, required=True)
    parser.add_argument("--emmsui-root", type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--strict", action="store_true", help="Warnings return non-zero")
    args = parser.parse_args()

    engine = args.engine_root.resolve()
    emmsui = args.emmsui_root.resolve() if args.emmsui_root else None
    project = args.project_root.resolve() if args.project_root else None

    report = build_report(engine, emmsui, project)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")

    counts = report["summary"]
    if counts["blocker"]:
        return 2
    if args.strict and counts["warning"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
