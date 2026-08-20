from __future__ import annotations

import importlib.util
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


checker = load_module("check_source_refs", ROOT / "scripts" / "check_source_refs.py")


class SourceReferenceTests(unittest.TestCase):
    def test_existing_engine_and_emmsui_refs_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "refs.md").write_text(
                "`Engine/Source/Runtime/Core/Public/CoreMinimal.h` and "
                "`Plugins/EmmsUI/Source/EmmsUI/Public/EmmsUI.h`",
                encoding="utf-8",
            )
            engine = root / "EngineRoot"
            engine_file = engine / "Engine/Source/Runtime/Core/Public/CoreMinimal.h"
            engine_file.parent.mkdir(parents=True)
            engine_file.write_text("", encoding="utf-8")
            emmsui = root / "EmmsUI"
            emmsui_file = emmsui / "Source/EmmsUI/Public/EmmsUI.h"
            emmsui_file.parent.mkdir(parents=True)
            emmsui_file.write_text("", encoding="utf-8")
            (emmsui / "EmmsUI.uplugin").write_text("{}", encoding="utf-8")

            errors, stats = checker.check(
                root,
                engine_root=engine,
                emmsui_root=emmsui,
                require_roots=True,
            )
            self.assertEqual([], errors)
            self.assertEqual(2, stats["existence_checked"])

    def test_missing_source_ref_fails_when_roots_are_provided(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "refs.md").write_text(
                "`Engine/Plugins/Angelscript/Source/Missing.h`",
                encoding="utf-8",
            )
            engine = root / "EngineRoot"
            (engine / "Engine").mkdir(parents=True)
            emmsui = root / "EmmsUI"
            emmsui.mkdir()
            (emmsui / "EmmsUI.uplugin").write_text("{}", encoding="utf-8")
            errors, _ = checker.check(
                root,
                engine_root=engine,
                emmsui_root=emmsui,
                require_roots=True,
            )
            self.assertTrue(any("does not exist" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
