from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load_module("probe_compatibility", ROOT / "tools" / "probe_compatibility.py")
lint = load_module("lint_ueas", ROOT / "tools" / "lint_ueas.py")


class CompatibilityProbeTests(unittest.TestCase):
    def make_fixture(
        self,
        root: Path,
        *,
        engine_minor: int = 8,
        engine_iterators: bool = True,
    ) -> tuple[Path, Path, Path]:
        engine = root / "EngineRoot"
        plugin = engine / "Engine" / "Plugins" / "Angelscript"
        (engine / "Engine" / "Build").mkdir(parents=True)
        (engine / "Engine" / "Build" / "Build.version").write_text(
            json.dumps(
                {"MajorVersion": 5, "MinorVersion": engine_minor, "PatchVersion": 1}
            ),
            encoding="utf-8",
        )
        (plugin / "Source").mkdir(parents=True)
        (plugin / "ThirdParty" / "include").mkdir(parents=True)
        (plugin / "Angelscript.uplugin").write_text("{}", encoding="utf-8")
        source_signals = "AS_FORCE_LINK if_handle_then_const"
        if engine_iterators:
            source_signals += " Iterate() angelscript.UseNewIterators"
        (plugin / "Source" / "Signals.cpp").write_text(
            source_signals,
            encoding="utf-8",
        )
        # Regression target: this signal is deliberately outside Source/.
        (plugin / "ThirdParty" / "include" / "Signals.h").write_text(
            "asOBJ_TEMPLATE_SUBTYPE_COVARIANT",
            encoding="utf-8",
        )

        emmsui = root / "EmmsUI"
        (emmsui / "Source").mkdir(parents=True)
        (emmsui / "EmmsUI.uplugin").write_text(
            json.dumps({"Modules": [{"Name": "EmmsUI"}, {"Name": "EmmsUIEditor"}]}),
            encoding="utf-8",
        )
        (emmsui / "Source" / "Signals.cpp").write_text(
            "if_handle_then_const Iterate() const MirroredValue "
            "OnObjectsReinstanced mm<class T>",
            encoding="utf-8",
        )

        project = root / "Project"
        (project / "Script").mkdir(parents=True)
        (project / "Config").mkdir(parents=True)
        (project / "Project.uproject").write_text("{}", encoding="utf-8")
        (project / "Script" / "Smoke.as").write_text("void Smoke() {}", encoding="utf-8")
        (project / "Config" / "DefaultEngine.ini").write_text(
            "AngelscriptSettings AngelscriptTestSettings IntegrationTestMapRoot",
            encoding="utf-8",
        )
        return engine, emmsui, project

    def test_aligned_iterator_signals_are_informational(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine, emmsui, project = self.make_fixture(Path(directory))
            report = probe.build_report(engine, emmsui, project)
            codes = {finding["code"]: finding["level"] for finding in report["findings"]}
            self.assertEqual("info", codes["compat.iterator_protocol_aligned"])
            self.assertEqual(0, report["summary"]["blocker"])
            self.assertEqual(0, report["summary"]["warning"])

            matches = report["facts"]["ueas_feature_signals"][
                "covariant_template_flag"
            ]
            self.assertTrue(matches)
            self.assertTrue(matches[0].startswith("ThirdParty/"))

    def test_new_emmsui_iterator_warns_when_engine_signal_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine, emmsui, project = self.make_fixture(
                Path(directory), engine_iterators=False
            )
            report = probe.build_report(engine, emmsui, project)
            codes = {finding["code"] for finding in report["findings"]}
            self.assertIn("compat.iterator_protocol_engine_missing", codes)
            self.assertGreater(report["summary"]["warning"], 0)

    def test_older_engine_with_current_emmsui_warns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine, emmsui, project = self.make_fixture(
                Path(directory), engine_minor=5
            )
            report = probe.build_report(engine, emmsui, project)
            codes = {finding["code"] for finding in report["findings"]}
            self.assertIn("compat.older_engine_new_emmsui", codes)
            self.assertGreater(report["summary"]["warning"], 0)


class LintTests(unittest.TestCase):
    def test_reflected_self_parameter_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "Bad.as"
            script.write_text(
                "UFUNCTION(BlueprintCallable)\nvoid DoThing(int Self) {}\n",
                encoding="utf-8",
            )
            findings = lint.lint_file(script, root)
            self.assertIn(
                "ueas.reflected_self_parameter",
                {finding["code"] for finding in findings},
            )


if __name__ == "__main__":
    unittest.main()
