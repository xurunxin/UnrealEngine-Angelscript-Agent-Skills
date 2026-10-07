# 按名回调与 Widget 边界

## Accessor

脚本 property accessor 可隐藏实现并保持自然语法：

```angelscript
float GetHealthPercent() const property
{
    return MaximumHealth > 0.0 ? CurrentHealth / MaximumHealth : 0.0;
}
```

使用前核对目标项目的隐式 Getter/Setter 设置。需要 Blueprint 访问时，再为具体消费者设计
反射函数；不要假设脚本 accessor 自动形成所需 Blueprint API。

## Delegate 与 Timer

- `delegate` 为单播，`event` 为多播；
- `BindUFunction` / `AddUFunction` 的按名目标必须进入反射；
- Handler 使用稳定函数名，例如 `n"HandleChanged"`；
- 生命周期结束、目标变化或重新初始化时解除绑定；
- 重复热重载/初始化后检查是否多次注册；
- Timer 回调只暴露实际需要的函数，多个并发 Timer 不要错误共享同一身份。

## UMG 与 EmmsUI 边界

- Widget Blueprint 视觉树需要脚本字段连接时使用 `UPROPERTY(BindWidget)`；
- `BindWidget` 名称、类型或父类变化属于结构性 ABI 变化；
- 代码驱动的 Runtime/Editor UI 分别交给 `emmsui-runtime` 或 `emmsui-editor-tools`；
- 只有现有 EmmsUI helper 无法表达需求时才交给 `emmsui-extension`。

## Super 限制

`Super::Function()` 适用于脚本父类。不要假设它能调用所有 C++ `BlueprintNativeEvent` 的原生
父实现。必须执行的原生逻辑应放在非事件函数，由事件包装或 Hook 调用。
