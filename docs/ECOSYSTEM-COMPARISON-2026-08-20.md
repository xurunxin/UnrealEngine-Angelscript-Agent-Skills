# UE-AS Agent Skills Ecosystem Comparison

Observed: 2026-08-20

## Finding

GitHub and skills.sh contain several strong general Unreal Engine Skill collections, but the search did
not find another maintained Skill suite focused on the combined workflow of Hazelight
UnrealEngine-Angelscript and EmmsUI. This repository should therefore stay narrow: reuse general Unreal
knowledge by reference or handoff, while owning UE-AS language/reflection/hot-reload/binding/cook details
and EmmsUI immediate-mode behavior.

## Compared sources

| Source | Strength | Adopted | Deliberately not copied |
|---|---|---|---|
| EpicGames `unreal-engine-skills-for-claude-code-plugin` | Novel, durable, tool-agnostic and parsimonious Skill authoring; live-editor skill separation | concise descriptions, tool-independent domain instructions, `agents/openai.yaml` | MCP-specific execution as a hard dependency |
| quodsoler `unreal-engine-skills` | project context before domain work; broad UE 5.x topic coverage | `.agents/ueas-project-context.md`, ambiguity stops, context refresh | duplicating 27 general Unreal C++ Skills |
| kevinpbuckley `unreal-engine-skills` | source-grounded citations and golden eval tasks | source-reference checker, routing and behavior evals, layered evidence | fixed local engine paths or C++-only assumptions |
| DSTN2000 `claude-unreal-engine-skill` | zero-assumption preflight and project discovery | unique `.uproject`/engine/plugin discovery | one monolithic always-on Unreal Skill |
| gamedev-skills `awesome-gamedev-agent-skills` | router plus cross-client interface metadata | smallest-skill routing, `agents/openai.yaml` | broad game-development discipline catalog |
| skills.sh `unreal-development` and Unreal catalog entries | easy installation and public discovery | standard `skills/<name>/SKILL.md`, documented `npx skills add` commands | treating install count or audit badges as API truth |

## skills.sh search summary

Searches for `UnrealEngine Angelscript`, `EmmsUI`, and related terms returned general Unreal Engine
Skills such as `unreal-development`, `unreal-engine`, and the quodsoler UE topic collection. No exact
UE-AS + EmmsUI peer was found in the observed index.

The most useful recurring patterns were:

- resolve project context before implementation;
- route to one focused Skill rather than loading a whole catalog;
- keep platform/tool invocation outside durable domain guidance;
- verify source paths against an exact engine version;
- measure Skill value with realistic acceptance tasks;
- distinguish static checks, compilation, runtime and packaging evidence.

## Resulting ownership boundary

This repository owns:

- source-built UE-AS bootstrap and version pinning;
- UE-AS language and Unreal-specific semantics;
- minimal reflection/Blueprint interop;
- soft versus structural hot reload;
- UE-AS networking and script test conventions;
- automatic/Mixin/manual C++ bindings and Static JIT boundary;
- simulate-cooked, precompiled scripts and shipping gates;
- EmmsUI Runtime, Editor and extension internals;
- UE-AS/EmmsUI compatibility evidence and project context.

General Unreal topics such as Niagara, Mass, animation systems, audio, GAS architecture or ordinary
C++ gameplay should be handed to a general Unreal Skill unless the task crosses a UE-AS-specific boundary.

## Source integrity

External material is research input, not executable authority. The exact observed commits are recorded in
[`sources/ecosystem-skills.lock.json`](../sources/ecosystem-skills.lock.json). Project source and the
current official repositories remain higher-priority facts.
