# 23. EmmsUI 状态、事件与身份

## 状态分层

### 业务状态

由 Actor/Component/Subsystem/ViewModel 持有：

```angelscript
bool bAutoRefresh;
FString Query;
TArray<FResult> Results;
```

### UMG 内部状态

焦点、光标、滚动、选择、编辑中的文本。EmmsUI 通过复用 Widget 和 MirroredValue 尽量保留。

### Draw 临时状态

只在当前函数计算，不跨帧需要。

## 双向输入

当前 EmmsUI helper 的目标语义：

1. 如果 UWidget 自上一轮发生用户输入，把值回写到传入引用；
2. 如果程序模型变了，把新值写到 UWidget；
3. 避免两者互相覆盖造成光标跳动。

因此输入值必须持久：

```angelscript
class UFilterPanel : UMMWidget
{
    FString Filter;

    void DrawFilter()
    {
        mm::EditableTextBox(Filter);
    }
}
```

## 事件捕获

EmmsUI 为 Delegate/Event 安装 `UEmmsEventListener`。

### `WasX`

- 检查 TriggerCount 是否高于 consumed；
- 同一 Draw cycle 多次调用仍可返回 true；
- 参数缓冲区保存最近一次触发参数；
- Draw 结束后参数被析构。

适合：

```angelscript
if (Button.WasClicked())
    ExecuteOncePerDraw();
```

### `OnX`

每轮 Draw 声明要绑定的 UFUNCTION Delegate；Pending/Active 列表交换。适合：

- 每次事件都要处理；
- 事件可能一帧多次；
- 需要即时 EventReply；
- 复杂参数。

## 身份算法

源码中 child identifier：

```text
WidgetType + ParentElement + HashIdent
```

公开普通 `AddWidget` 默认 HashIdent 为 0。同一个 identifier 的多个 Widget 以可用列表的出现顺序复用。

### 推断出的风险

```angelscript
if (bShowExtra)
    mm::EditableTextBox(Extra);

mm::EditableTextBox(Name);
```

当 `bShowExtra` 切换时，两个相同类型输入的出现顺序发生变化，底层 Widget 可能被另一个逻辑字段复用，焦点/选择/内部状态可能错位。

### 对策

- 条件分支包入不同父 Panel；
- 不在同一父中重排有状态的同类型 siblings；
- 使用不同 Widget 类型/包装类型；
- 用 ListView；
- 业务值持久化并验证焦点；
- 检查目标 EmmsUI 是否已加入显式 ID API，不能假设。

## Handle 生命周期

`mm<T>` 只在当前/相近 Draw 上下文使用。不要长期保存 Handle 并假设 Element 不变。需要长期引用时保存业务 ID，再在 Draw 中重新取得 Widget。
