---
name: emmsui-runtime
description: Use when building EmmsUI in-game, viewport or world-space UI. Do not use for Editor tabs or C++ plugin extensions.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# EmmsUI Runtime

## 心智模型

每次 Draw 重新声明想要的 UI；EmmsUI 内部复用 UMG Widget，比较属性，更新层级，并删除本帧不再使用的节点。参阅 [`../../wiki/20-EmmsUI-Mental-Model.md`](../../wiki/20-EmmsUI-Mental-Model.md)。

## 选择 Draw Context

- 独立 UI 类：继承 `UMMWidget`，覆盖 `DrawWidget`;
- 已有 UMMWidget：`mm::BeginDraw(Widget)` / `mm::EndDraw()`;
- Viewport 覆盖层：`mm::BeginDrawViewportOverlay(n"StableId")`;
- 3D/WidgetComponent：组件 WidgetClass 设为 `UMMWidget`，对实例 BeginDraw；
- 弹窗：使用 `UMMPopupWindow`。

所有 Begin/End 必须严格配对。早退前先结束作用域；优先通过小函数缩短 Draw。

## 状态

持久状态放在：

- `UMMWidget` 类成员；
- Owner/ViewModel/Subsystem；
- 按稳定业务键索引的集合。

输入 helper 通过引用回写：

```angelscript
FString SearchText;

void DrawSearch()
{
    mm<UEditableTextBox> Search = mm::EditableTextBox(SearchText);
    if (Search.WasTextChanged())
        RefreshFilter(SearchText);
}
```

不要把 `FString SearchText;` 声明在每帧 Draw 的临时块中，除非只需要瞬时值。

## 布局

- `BeginX/EndX`：多子节点容器；
- `WithinX`：只包装下一个 Widget；
- Slot 属性必须在目标 Widget 之前声明；
- 属性本帧省略时会恢复到捕获的默认值；
- 只有需要复用 Panel 句柄时才使用 `BeginExistingWidget`。

## 事件

- `if (mm::Button("Save"))` 或 `WasClicked()`：Draw 周期动作；
- `OnClicked(this, n"HandleSave")`：即时委托；
- 有参数的 `WasX(out ...)` 只适合最近事件的边沿读取，不是事件队列。

## 身份稳定

普通节点主要按类型、父元素和出现顺序复用。避免在同一父节点中条件插入/重排多个同类型、带内部状态的控件。把条件分支包在不同 Panel，或使用 ListView/TreeView。

## 禁止的 Draw 副作用

- 同步加载大资产；
- 每帧扫描全部 Actors/Assets；
- 每帧写磁盘；
- 每帧发 RPC；
- 每帧创建持久 UObject 数据模型；
- 依赖 `GetUnderlyingWidget()` 的不可复位改动。

## 完成标准

验证输入焦点、动态分支、窗口缩放、热重载、Overlay 消失、Widget 销毁和运行时性能。
