# 22. EmmsUI 布局、属性与 Slot

## Panel

```angelscript
mm::BeginVerticalBox();
    mm::Text("A");
    mm::Text("B");
mm::EndVerticalBox();
```

`Begin/End` 支持多个子节点。

## Within

```angelscript
mm::WithinBorder(FLinearColor::Black);
mm::Text("Wrapped");
```

`Within` Panel 只接收下一 Widget，随后自动退出隐式父层级。适合单层装饰。

## Slot 属性的时序

```angelscript
mm::Slot_Fill(0.5);
mm::HAlign_Fill();
mm::Text("Half width");
```

Pending Slot 属性应用到 **下一个加入当前 Panel 的 Widget**。放在 Widget 之后不会回溯。

## 默认子 Slot

某些 Begin helper 可设置默认 Padding/Alignment，作用于该 Panel 后续 children。显式 child slot 属性可覆盖。

## Widget 属性

`mm<T>` 自动生成：

```angelscript
mm<UTextBlock> Label = mm::Text("Ready");
Label.SetAutoWrapText(true);
Label.SetColorAndOpacity(FSlateColor(...));
```

实际方法由目标 UWidget 的反射属性决定。使用 LSP，不从 C++ 字段名盲猜。

## getter

`GetX()` 从底层 UWidget 读取并维护 MirroredValue。getter 适合真实 UMG 状态，但不要把它当业务模型持久层。

## 属性复位

条件式 setter：

```angelscript
if (bSelected)
    Border.SetBrushColor(SelectedColor);
```

条件消失后恢复默认。若直接：

```angelscript
Border.GetUnderlyingWidget().SetSomething(...);
```

EmmsUI 不知道这次改动，通常不会自动复位。

## 只读属性与重建

自动绑定把 BlueprintReadOnly 或非 BlueprintVisible 的可编辑属性视为可能需要 Widget rebuild。避免每帧切换这些属性。需要高频变化时：

- 找运行时 Setter；
- 写专用 AssignValueFunction；
- 修改 Widget 设计；
- 或创建不同类型/样式节点。

## Tooltip

Pending tooltip 通常应用到下一个 Widget。像 Slot 属性一样注意顺序。

## 布局稳定

EmmsUI 层级变化后会调用 layout invalidation/prepass。频繁重排大子树会增加 Slate/UMG 开销。把变化限制在局部 Panel。
