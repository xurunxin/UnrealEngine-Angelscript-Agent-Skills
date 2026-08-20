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


validator = load_module("validate_skills", ROOT / "scripts" / "validate_skills.py")


class SkillValidationTests(unittest.TestCase):
    def make_repo(self, root: Path, skill_text: str) -> None:
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(skill_text, encoding="utf-8")

    def test_folded_yaml_description_and_boundary_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(
                root,
                """---
name: sample-skill
description: >-
  Produce a sample artifact. Use when testing a Skill validator.
  Do not use for unrelated production work.
metadata:
  version: \"1.0.0\"
---

# Sample
""",
            )
            errors, _, stats = validator.validate_repo(root)
            self.assertEqual([], errors)
            self.assertEqual(1, stats.skills)

    def test_plain_scalar_colon_is_rejected_by_real_yaml_parser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(
                root,
                """---
name: sample-skill
description: Use deliberately: this colon makes the YAML scalar invalid. Use when testing. Do not use elsewhere.
---

# Sample
""",
            )
            errors, _, _ = validator.validate_repo(root)
            self.assertTrue(any("invalid YAML frontmatter" in error for error in errors))

    def test_directory_name_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(
                root,
                """---
name: another-name
description: Use when testing names. Do not use for other work.
---

# Sample
""",
            )
            errors, _, _ = validator.validate_repo(root)
            self.assertTrue(any("does not match directory" in error for error in errors))

    def test_link_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(
                root,
                """---
name: sample-skill
description: Use when testing links. Do not use for other work.
---

# Sample

[bad](../../../outside.md)
""",
            )
            errors, _, _ = validator.validate_repo(root)
            self.assertTrue(any("escapes repository root" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
