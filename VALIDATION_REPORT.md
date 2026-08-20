# Validation Report

Generated: 2026‑08‑20  
Package: 0.1.1

## Artifact checks

- `python tools/validate_kit.py .` — PASS
  - 14 Skills
  - 63 Markdown files
  - 0 warnings
  - 0 errors
- Python syntax compile for `tools/*.py` and `tests/*.py` — PASS
- `python -m unittest discover -s tests -v` — PASS
  - 4 tests
  - aligned UE‑AS/EmmsUI iterator signals remain informational
  - a new EmmsUI iterator with a missing engine signal produces a warning
  - an older engine baseline with current-feature EmmsUI produces warnings
  - reflected `UFUNCTION` parameter `Self` is detected by the static linter
- `lint_ueas.py` executed against included examples — PASS as a heuristic scan
  - 13 `.as` files scanned
  - 6 expected review findings: 1 medium, 5 informational
  - no high-severity finding
- Relative Markdown links — PASS
- JSON parsing — PASS
- Frontmatter uniqueness — PASS
- Manifest and SHA‑256 verification — PASS
- ZIP integrity and packaged manifest verification — PASS

## Source-update correction

The package now locks the observed engine snapshot to UE 5.8.1 / `546c4d6a…`. UE‑AS `1a06a2bf…` and EmmsUI `c9985c11…` contain corresponding new `Iterate()` protocol implementations, so the historical UE 5.5.4 source-gap warning is no longer applied to the current baseline.

The compatibility status is `source-signals-aligned-runtime-unverified`, not “runtime compatible”.

## Not executed in this environment

- Unreal Engine source build;
- target project C++ compile;
- AngelScript Editor compile;
- PIE hot reload;
- VS Code debugger;
- Dedicated Server integration tests;
- simulate-cooked against the target project;
- Cook/Package;
- platform runtime profiling.

The package must not be used to claim those runtime checks passed. Run the supplied compatibility probe and CI templates inside the exact locked UE‑AS project.
