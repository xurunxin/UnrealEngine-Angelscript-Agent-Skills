# Contributing

This repository maintains modular Agent Skills, a source-grounded Wiki, examples, and validation tools for UnrealEngine-Angelscript and EmmsUI.

## Change the smallest owned surface

- Put routing and high-frequency workflow rules in `skills/<name>/SKILL.md`.
- Put detailed, conditional knowledge in `wiki/` or `references/`.
- Put executable examples in `examples/`.
- Put deterministic checks in `tools/` and regression coverage in `tests/`.
- Do not copy large portions of upstream documentation. Summarize, link, and lock the source commit in `sources.lock.json`.

## Mutable facts

Before changing claims about Unreal, UE-AS, EmmsUI, build commands, APIs, hot reload, Cook, packaging, or editor behavior:

1. record the exact repository, branch/tag, and commit;
2. prefer official documentation and source code;
3. distinguish source-level evidence from runtime validation;
4. update `sources.lock.json`, the compatibility Wiki, and tests when the claim affects executable guidance;
5. never describe a build, PIE run, Cook, package, or performance result as passed without current observable evidence.

## Skill routing contract

Each Skill must own one recognizable job. Its frontmatter description should say what it produces, when it activates, and the nearest task it does not own. Use the router for ambiguous or cross-domain tasks; load a clear specialist directly. Avoid loading every Skill for every task.

## Required validation

Run from the repository root:

```bash
python tools/validate_kit.py .
python -m unittest discover -s tests -v
python -m py_compile tools/*.py tests/*.py
```

Also run the smallest relevant Unreal/UE-AS/EmmsUI smoke test when a change affects runtime behavior. Record anything not executed.

## Pull requests

Keep one coherent change per pull request. Include exact source versions, evidence, compatibility risks, and remaining unverified assumptions. Do not commit Unreal binaries, DerivedDataCache, project `Saved/`, credentials, proprietary project assets, or full engine source.
