# Decision Tables

## Need UPROPERTY?

| Question | Yes | No |
|---|---|---|
| Editor/Blueprint must see it? | UPROPERTY | plain field |
| Replication? | UPROPERTY Replicated | plain field |
| Unreal serialization/asset default? | UPROPERTY | plain field |
| Only script GC? | not required solely for GC | plain field |
| BindWidget? | UPROPERTY BindWidget | n/a |

## Need UFUNCTION?

| Question | Yes | No |
|---|---|---|
| Blueprint calls/overrides? | UFUNCTION | plain function |
| Dynamic delegate? | UFUNCTION | plain function |
| Timer by name? | UFUNCTION | plain function |
| RPC/OnRep? | UFUNCTION | plain function |
| Script-only helper? | no | plain function |

## Actor vs Component vs Subsystem

| Need | Choice |
|---|---|
| World entity/transform | Actor |
| Reusable behavior on Actor | Component |
| World service | WorldSubsystem |
| Session service | GameInstanceSubsystem |
| Per player local service | LocalPlayerSubsystem |
| Editor global tool | EditorSubsystem |

## EmmsUI event

| Requirement | Choice |
|---|---|
| One action per Draw | `WasX` |
| Every event, immediate | `OnX` |
| Need event args once | `WasX(out...)` |
| Multiple same-frame events | `OnX` or explicit queue |
| Need FEventReply | immediate binding / target helper |

## UI technology

| Need | Choice |
|---|---|
| Designer animation/assets | UMG |
| UE-AS code tool | EmmsUI |
| C++ Slate debug, modern UE | SlateIM candidate |
| Cross-engine debug widgets | ImGui |
| Deep Editor control | Slate C++ |

## Version mismatch

| Finding | Action |
|---|---|
| EmmsUI newer than UE‑AS | probe + compile minimal |
| iterator fails | pin older EmmsUI or backport protocol |
| input state bug | backport mutable state commit |
| Tab reload bug | backport reinstance commit |
| C++ binding API changed | adapt plugin on isolated branch |
