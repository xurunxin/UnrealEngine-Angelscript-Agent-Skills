# UE-AS Project Context Discovery Map

**Load when:** creating, refreshing, or auditing `.agents/ueas-project-context.md`.

## Evidence map

| Fact | Primary evidence | Secondary evidence | Never infer from |
|---|---|---|---|
| Project root | unique `*.uproject` | workspace/project instructions | nearest `Content/` directory |
| Unreal version | `Engine/Build/Build.version` | build logs | folder name alone |
| Engine ref | Git HEAD/branch/dirty state | version lock, CI | latest upstream |
| UE-AS presence | `Engine/Plugins/Angelscript/Angelscript.uplugin` and source | build modules | plugin name in documentation |
| UE-AS ref | actual engine checkout Git ref | submodule/lock record | docs commit |
| EmmsUI location | actual `EmmsUI.uplugin` selected by project | `.uproject` plugin list | first search result |
| EmmsUI ref | plugin checkout Git ref | project lock | current `master` |
| Script roots | existing directories plus project/config declarations | build scripts | conventional `Script/` only |
| Modules | `.uproject`, `.uplugin`, `*.Build.cs` | target files | folder names |
| Targets | `*.Target.cs` | CI/build commands | assumed Editor-only workflow |
| Binding boundary | `FAngelscriptBinds`, `ScriptMixin`, module dependencies | docs/tests | API absence alone |
| Runtime compatibility | executed build/script/runtime/cook evidence | CI artifacts | matching symbols or dates |

## Minimal scan

```text
<Project>/*.uproject
<Project>/Config/**/*.ini
<Project>/Source/**/*.Build.cs
<Project>/Source/**/*.Target.cs
<Project>/Plugins/**/**/*.uplugin
<Project>/Plugins/**/Source/**/*.Build.cs
<Project>/Script/**/*.as
<Engine>/Engine/Build/Build.version
<Engine>/Engine/Plugins/Angelscript/Angelscript.uplugin
<Engine>/Engine/Plugins/Angelscript/Source/**
<EmmsUI>/EmmsUI.uplugin
<EmmsUI>/Source/**
```

Do not recursively ingest generated directories such as `Binaries/`, `DerivedDataCache/`,
`Intermediate/`, `Saved/`, or packaged output unless a specific failure requires their evidence.

## Ambiguity rules

### Multiple `.uproject` files

Return all candidates with relative path and any explicit workspace reference. Stop automatic selection.

### Multiple Engine checkouts

Prefer an explicit project/build reference. `EngineAssociation` may identify a registered build but is
not always a filesystem path. Record unresolved candidates rather than choosing by version number.

### Multiple Angelscript/EmmsUI plugins

Record each location and the project/plugin enablement evidence. A project plugin can shadow an engine
plugin; never describe one as active without observing the project configuration or build output.

### Git unavailable

Record file versions and paths, set ref fields to `unknown`, and preserve a follow-up action. Do not turn
file timestamps into commit identity.

## Version-sensitive source signals

Signals such as the following can help choose smoke tests:

```text
Iterate()
if_handle_then_const
angelscript.UseNewIterators
MirroredValue
OnObjectsReinstanced
```

They are not compatibility certificates. Report them as `source-signal-present` and require the relevant
build, script compile, UI interaction, hot-reload, and Cook gates.

## Privacy

The context file should be useful in source control. Replace user-specific absolute paths with variables
such as `<ENGINE_ROOT>` or documented relative paths unless the repository intentionally tracks them.
Never store credentials, tokens, private repository URLs containing secrets, or machine-specific caches.
