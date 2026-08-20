# 05. Actor、Component 与 Subsystem

## Actor

```angelscript
class AInteractionBeacon : AActor
{
    UPROPERTY(DefaultComponent, RootComponent)
    USceneComponent Root;

    UPROPERTY(DefaultComponent, Attach = Root)
    USphereComponent Trigger;

    UPROPERTY(EditDefaultsOnly, Category = "Interaction")
    float32 Radius = 200.0f;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        Trigger.SetSphereRadius(Radius);
    }
}
```

默认组件通过属性声明，而不是运行时构造。需要覆盖 C++ 默认组件时查阅 `OverrideComponent` 与目标版本 API。

## Component

组件适合可复用行为：

- Interaction；
- Health；
- Inventory；
- Input；
- Targeting；
- UI Presenter。

避免让组件直接查找全局单例。通过 Owner、Subsystem 或显式依赖建立上下文。

## 生命周期

常见 BlueprintOverride：

- `ConstructionScript`
- `BeginPlay`
- `Tick`
- `EndPlay`
- Component 激活/停用事件

目标 API 名称可能经过 Blueprint 前缀简化。以 LSP 为准。

## Subsystem

```angelscript
class UQuestWorldSubsystem : UScriptWorldSubsystem
{
    TMap<FName, FQuestRuntimeState> States;

    static UQuestWorldSubsystem Get()
    {
        return UQuestWorldSubsystem::Get();
    }
}
```

不要盲目写自己的 `Get()` 包装，先检查目标引擎提供的自动静态访问。

选择表：

| 生命周期 | Base |
|---|---|
| 每个 World | `UScriptWorldSubsystem` |
| 每个 GameInstance | `UScriptGameInstanceSubsystem` |
| 每个 LocalPlayer | `UScriptLocalPlayerSubsystem` |
| Editor | `UScriptEditorSubsystem` |
| Engine 全局 | `UScriptEngineSubsystem` |

## World Context

静态库与 Subsystem 获取可能需要 World Context。无效上下文在 Editor、CDO、Commandlet 或 Dedicated Server 中很常见。项目设置可对无效 World Context 发出警告。

## Enhanced Input

把输入放 Component 时：

1. 确认 Owner 是 PlayerController/Pawn；
2. 获取 `UEnhancedInputLocalPlayerSubsystem`；
3. 添加 Mapping Context；
4. Push/Pop InputComponent；
5. handler 是 UFUNCTION；
6. EndPlay 清理。

不要在服务器路径假设 LocalPlayer 存在。

## Tick

Tick 的替代：

- Delegate/Event；
- Timer；
- Gameplay Message；
- State change；
- Subsystem 统一调度；
- UI invalidation；
- 显式请求刷新。

启用 Tick 时记录频率和停用条件。
