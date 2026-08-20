---
name: ueas-gameplay
description: >-
  Design and implement Unreal gameplay with Angelscript Actors, Components, Subsystems, Enhanced Input, timers, data flow, and maintainable C++/Blueprint boundaries. Use when implementing UE-AS gameplay architecture or behavior. Do not use for isolated reflection, networking, packaging, or generic C++-only tasks.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---


# UE‑AS Gameplay

## 适用范围

Actor、ActorComponent、默认组件、Subsystem、输入、Gameplay 业务结构与跨层职责。

## 架构优先级

1. **数据与规则**：普通 struct/class、纯函数、可单测；
2. **生命周期适配**：Actor/Component/Subsystem；
3. **UE 反射接口**：仅暴露设计师或系统确实需要的表面；
4. **Blueprint Hook**：表现层扩展，不承载核心不变量；
5. **C++**：性能、平台、第三方库与缺失绑定。

参阅 [`../../wiki/05-Actors-Components-and-Subsystems.md`](../../wiki/05-Actors-Components-and-Subsystems.md) 与 [`../../wiki/30-Architecture-and-Best-Practices.md`](../../wiki/30-Architecture-and-Best-Practices.md)。

## Actor 与组件

声明式默认组件：

```angelscript
class AScannerActor : AActor
{
    UPROPERTY(DefaultComponent, RootComponent)
    USceneComponent Root;

    UPROPERTY(DefaultComponent, Attach = Root)
    UStaticMeshComponent Mesh;

    UPROPERTY(DefaultComponent, Attach = Root)
    USceneComponent ScanOrigin;
}
```

不要在 Tick 中反复查找固定组件。可选引用在 BeginPlay/初始化阶段解析并缓存；跨关卡对象用 Weak/Soft 引用按语义选择。

## Subsystem 选择

- World 生命周期与关卡关联：`UScriptWorldSubsystem`
- GameInstance 跨地图会话：`UScriptGameInstanceSubsystem`
- LocalPlayer 本地用户：`UScriptLocalPlayerSubsystem`
- Editor 工具：`UScriptEditorSubsystem`
- Engine 全局：`UScriptEngineSubsystem`

不要把所有系统放进 EngineSubsystem。明确创建/销毁时机、World Context 与多人实例数量。

## 输入

Enhanced Input 绑定可以放在 PlayerController/Character，也可以放在专用 ActorComponent。独立组件更易复用与测试，但必须明确：

- Owner 类型；
- Local Player Subsystem 获取方式；
- Mapping Context 增删生命周期；
- 绑定函数需要的 `UFUNCTION`；
- Dedicated Server 不执行本地输入路径。

## Tick 预算

默认不启用无条件 Tick。优先：

- 事件；
- Timer；
- Subsystem 集中调度；
- 明确频率的更新；
- 激活时 Tick、闲置时禁用。

Timer 按对象 + 函数名标识；同一函数重复设 Timer 可能覆盖旧 Timer。需要多个并发实例时使用不同回调或显式调度结构。

## Blueprint Hook 模式

核心逻辑不可被 Blueprint 跳过：

```angelscript
void ApplyDamageResult(const FDamageResult& Result)
{
    CommitHealth(Result);
    BP_OnDamageCommitted(Result);
}

UFUNCTION(BlueprintEvent, NotBlueprintCallable)
void BP_OnDamageCommitted(const FDamageResult& Result)
{
}
```

## 完成标准

- 生命周期与 World Context 明确；
- 默认组件声明式创建；
- 不必要 Tick 已去除；
- 业务规则可单测；
- Blueprint 不能绕过关键不变量；
- Editor、Standalone、Client/Server 的执行路径被区分；
- 同类实现与项目约定一致。
