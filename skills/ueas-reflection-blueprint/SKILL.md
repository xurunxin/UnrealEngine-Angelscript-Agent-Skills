---
name: ueas-reflection-blueprint
description: Use Unreal reflection from Angelscript deliberately: UPROPERTY, UFUNCTION, Blueprint overrides and events, delegates, timers, accessors, UMG, serialization, and GC boundaries.
---


# UE‑AS Reflection and Blueprint

## 决策规则

先问“这个成员是否必须被 Unreal 反射系统看到？”

需要时才加：

- 编辑器 Details；
- Blueprint 调用/覆盖；
- 序列化或资产默认值；
- 属性复制；
- 动态委托；
- Timer/UFunction 按名调用；
- `BindWidget`；
- 反射式工具/API。

仅供脚本内部使用时，保持普通成员/函数。

## UPROPERTY

项目默认配置可能让裸 `UPROPERTY()` 等价于可编辑且 BlueprintReadWrite。生产代码建议显式缩小权限：

```angelscript
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Scanner")
float32 ScanRadius = 500.0f;
```

注意：在 UE‑AS 中，脚本 UObject 引用即使不是 UPROPERTY 也由脚本 GC 正确追踪；UPROPERTY 的主要价值是 Unreal 反射，不是“否则必然被 GC”。

## UFUNCTION

- `UFUNCTION()`：进入 Unreal 反射，通常默认 BlueprintCallable；
- `NotBlueprintCallable`：需要反射但不允许手工 BP 调用；
- `BlueprintOverride`：覆盖 C++ 的 Blueprint event；
- `BlueprintEvent`：允许 Blueprint 子类覆盖脚本定义；
- `CallInEditor`：Details 按钮或菜单操作；
- RPC/Authority：交给网络 Skill。

当前 UE‑AS 基线会拒绝 BlueprintCallable/BlueprintEvent 参数名 `Self`，因为它是 Unreal 反射保留名。使用 `Target`、`Object` 或领域名称，不要通过修改生成代码绕过。

普通脚本函数热重载通常更轻，因此不要批量加 UFUNCTION。

## Accessor

使用脚本属性访问器隐藏实现，同时保留自然语法：

```angelscript
float GetHealthPercent() const property
{
    return MaximumHealth > 0.0 ? CurrentHealth / MaximumHealth : 0.0;
}
```

写访问器前检查项目是否启用隐式 Get 访问；目标设置可能不同。

## 委托与事件

- `delegate`：单播；
- `event`：多播；
- `BindUFunction` / `AddUFunction` 的目标必须是 `UFUNCTION`；
- 函数名使用 `n"Handler"`；
- 销毁或重绑定时移除监听，避免重复注册。

## Timer

Timer 回调必须是 `UFUNCTION`。同一对象同一函数名的 Timer 身份可能唯一；并发 Timer 不要共用同一个按名回调。

## UMG 混合

复杂视觉界面可用 Widget Blueprint 设计，脚本类继承 `UUserWidget`，以 `UPROPERTY(BindWidget)` 取得命名控件。代码驱动工具界面优先评估 EmmsUI。

## Super 限制

`Super::Function()` 只支持脚本父类调用。对 C++ `BlueprintNativeEvent` 的原生父实现无法用同样方式调用。设计 API 时避免依赖这一能力；将原生必要逻辑放在非事件函数中，再由事件包装。

## 验证

- Blueprint 子类是否仍可编译；
- 资产默认值是否保留；
- 热重载是否触发结构重实例化；
- 委托是否重复绑定；
- Timer 是否覆盖；
- Cook 是否引用 Editor-only 类型；
- 反射暴露是否超过需求。
