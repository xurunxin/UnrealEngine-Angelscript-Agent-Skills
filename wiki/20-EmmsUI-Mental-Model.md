# 20. EmmsUI 心智模型

## 外部 API：即时式

Draw 每次执行时声明当前帧想要的 UI：

```angelscript
void DrawWidget(float DeltaTime)
{
    mm::Text(f"Health: {Health}");
    if (mm::Button("Heal"))
        Health = Math::Min(Health + 10.0, MaximumHealth);
}
```

代码的控制流就是 UI 的控制流。条件、循环和函数组合直接决定本帧树。

## 内部实现：保留式 UMG

EmmsUI 不是每帧 `NewObject` 所有控件。内部大致流程：

1. `BeginDraw` 建立隐式层级栈；
2. `AddWidget` 根据身份寻找可复用 Element；
3. helper 把属性写入 Pending；
4. 事件监听读取上一次 Draw 周期后发生的事件；
5. `EndDraw`：
   - 删除未使用 Element；
   - 交换 Available/Pending 池；
   - 差分属性；
   - 必要时重建 UWidget；
   - 差分子节点顺序；
   - 更新 Slot 和 Event Listener。

## 核心类型

### `mm<T>`

脚本可见的轻量 Handle，内部包含：

- 根 `UMMWidget`；
- `FEmmsWidgetElement*`。

它不是长期稳定 UObject 引用。底层 UWidget 可能因属性要求重建。

### `FEmmsWidgetElement`

保存：

- 当前 UMGWidget；
- Parent；
- Active/Pending children；
- Widget attributes；
- Slot attributes；
- default child slot attributes；
- Event listeners。

### `FEmmsAttributeState`

四种值：

- `DefaultValue`：第一次覆盖前捕获的 UWidget 默认值；
- `CurrentValue`：上一轮声明值；
- `PendingValue`：本轮声明值；
- `MirroredValue`：从真实 UWidget 读取的交互状态。

## 属性为什么会自动恢复

本帧：

```angelscript
Text.SetColorAndOpacity(Red);
```

下一帧不再调用 Setter，EmmsUI 发现 Pending 为空，就把属性恢复到首次覆盖前的默认值。这使条件式样式自然成立：

```angelscript
if (bWarning)
    Label.SetColorAndOpacity(Red);
```

## Widget 重建

某些 BlueprintReadOnly / 只在构造期可改的属性会被标为 RequiresWidgetRebuild。变化时 EmmsUI：

- 移除旧 Widget；
- 建立新 Widget；
- 重新应用 Active attributes；
- 迁移 Event Listener；
- 重新挂载 children。

所以 `GetUnderlyingWidget()` 不能假设永久有效。

## 设计结论

- Draw 是声明，不是对象初始化；
- 业务状态在模型，Widget 是投影；
- Widget 顺序与父节点影响身份；
- 只通过 EmmsUI 属性 API 才能获得自动差分/复位；
- 复杂保留式行为仍可访问 UWidget，但由调用方承担完整生命周期。
