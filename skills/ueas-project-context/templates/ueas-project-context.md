# UE-AS Project Context

*Last refreshed: YYYY-MM-DD*

## Scope

- **Project root:** `<PROJECT_ROOT>`
- **Primary `.uproject`:** `Project.uproject`
- **Context status:** `confirmed | partial | ambiguous`
- **Evidence snapshot:** `<commit or workspace state>`

## Engine and plugin baseline

| Component | Value | Status | Evidence |
|---|---|---|---|
| Unreal version | unknown | unknown | `Engine/Build/Build.version` |
| Engine branch/commit | unknown | unknown | Git observation or lock |
| Engine dirty state | unknown | unknown | Git observation |
| UE-AS plugin path | unknown | unknown | `Angelscript.uplugin` |
| UE-AS branch/commit | unknown | unknown | Git observation or lock |
| EmmsUI plugin path | not-present | confirmed | project/plugin scan |
| EmmsUI branch/commit | not-present | confirmed | Git observation or lock |

## Project structure

### Modules and targets

| Name | Type | Source | Important dependencies |
|---|---|---|---|
| | Runtime/Editor/Developer/ThirdParty | | |

### Script roots

| Path | Purpose | Cooked? | Evidence |
|---|---|---|---|
| `Script/` | runtime scripts | yes/unknown | directory/config |

### Custom bindings

| Module/file | Surface | Runtime/Editor | Tests |
|---|---|---|---|
| none observed | | | |

## Project conventions

- **Reflection policy:** unknown
- **Blueprint extension boundary:** unknown
- **Hot-reload policy:** unknown
- **Editor-only isolation:** unknown
- **Networking topology:** standalone/unknown
- **Dedicated Server required:** unknown
- **Target platforms:** unknown
- **EmmsUI usage:** not-present/unknown
- **Widget identity rules:** stable sibling structure unless target ref proves explicit IDs

## Validation matrix

| Gate | Status | Evidence |
|---|---|---|
| Engine/Editor build | not-run | |
| AngelScript compile | not-run | |
| Soft hot reload | not-run | |
| Structural hot reload | not-run | |
| PIE runtime smoke | not-run | |
| Dedicated Server/client | not-run | |
| EmmsUI input/list/editor smoke | not-run | |
| Simulate cooked | not-run | |
| Cook | not-run | |
| Package launch | not-run | |

## Known risks and decisions

- `unknown`

## Staleness triggers

Refresh after Engine/UE-AS/EmmsUI ref changes, module or Script-root changes, binding changes, target
platform changes, or when any evidence path no longer resolves.
