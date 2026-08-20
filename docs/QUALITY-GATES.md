# Quality Gates

This repository separates static Skill quality from Unreal runtime evidence.

## Repository gates

Run on every change:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python tools/validate_kit.py .
python scripts/validate_evals.py
python scripts/check_source_refs.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tools tests
```

These checks prove that frontmatter parses, routes are internally consistent, references resolve,
JSON fixtures are valid, and Python tooling compiles. They do not prove an Unreal project builds.

## Source-reference gate

A runner with the exact engine and EmmsUI source can additionally run:

```bash
python scripts/check_source_refs.py \
  --engine-root "<UE-AS_ENGINE_ROOT>" \
  --emmsui-root "<PROJECT>/Plugins/EmmsUI" \
  --require-roots
```

This verifies cited paths against the locked source checkouts. It is intentionally optional on public
GitHub-hosted runners because Epic engine source is not available there.

## Project runtime gates

Apply only inside the exact target project and record evidence separately:

1. Development Editor C++ build.
2. AngelScript compile/test commandlet.
3. Soft hot reload smoke.
4. Structural hot reload/reinstancing smoke.
5. PIE runtime smoke.
6. Dedicated Server plus client integration, when networking is in scope.
7. EmmsUI input, ListView/TreeView, overlay and Editor Tab smoke, when relevant.
8. Simulate-cooked script compile.
9. Cook and Package.
10. Launch the packaged executable and inspect the target flow.

A successful earlier gate cannot be reported as a later gate. `source-signals-aligned` is not
`runtime-compatible`, and a successful Cook is not a successful package launch.

## Skill change gate

A changed Skill should include:

- two positive routing cases;
- one near-boundary case;
- at least one behavior case for a high-risk rule;
- updated source lock when external research materially changes guidance;
- explicit `not-run` status for unavailable Unreal checks.
