# Validation Report

Generated: 2026-08-20
Package: 0.2.0

## Repository checks

The following commands are the release gate:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python tools/validate_kit.py .
python scripts/validate_evals.py
python scripts/check_source_refs.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tools tests
```

Expected coverage:

- 15 Agent Skills;
- strict YAML frontmatter through PyYAML;
- name/directory equality, description trigger and exclusion boundaries;
- Skill activation line budget;
- `agents/openai.yaml` schema;
- Markdown fences and local links;
- package structure, JSON, source lock and compatibility fixtures;
- routing and behavior eval fixture integrity;
- source-reference safe format, with optional real-source existence checks;
- compatibility probe and UE-AS static-lint regressions;
- deterministic release metadata.

## Evidence interpretation

Passing repository checks means the Skill package is structurally valid and its deterministic tests pass. It does not mean a target Unreal project is compatible.

The current locked UE-AS and EmmsUI refs have corresponding new iterator protocol source signals. This remains:

```text
source-signals-aligned-runtime-unverified
```

## Target-project gates not executed here

- Unreal Engine Development Editor build;
- target project C++ build;
- AngelScript compile and tests;
- Soft and Structural Hot Reload;
- PIE runtime smoke;
- Dedicated Server/client integration;
- EmmsUI input/ListView/TreeView/Editor Tab smoke;
- Static JIT and precompiled script cache;
- simulate-cooked;
- Cook;
- Package;
- packaged executable launch.

A project release must attach its own observable evidence for each applicable gate.
