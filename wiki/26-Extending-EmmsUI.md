# 26. 扩展 EmmsUI

## 先理解自动生成

`EmmsScriptBinds.cpp` 遍历原生 `UWidget`：

- 可见/可编辑 property → `SetX` / `GetX`；
- Delegate/Event → `WasX` / `OnX`；
- `UPanelSlot` property → Slot setter；
- bool 名去掉 `b`；
- ScriptName/Bind Database 参与命名。

新增原生 UWidget 后，很多 API 无需修改 EmmsUI 即自动出现。

## 何时写 helper

- 一行创建复合 Widget；
- 设置多个属性；
- 双向输入；
- 特殊 Brush/Material；
- ListView/TreeView；
- 事件需要更友好语义；
- 基础属性 API 不适合每帧声明。

## helper 流程

```cpp
FEmmsWidgetHandle UMyHelpers::StatusBadge(...)
{
    FEmmsWidgetHandle Widget = UEmmsStatics::AddWidget(UMyStatusWidget::StaticClass());
    if (Widget.Element == nullptr)
        return Widget;

    // FindOrAdd AttributeState
    // SetPendingValue
    // Configure events
    return Widget;
}
```

不要把示意代码原样复制；使用目标源码已有 helper 的模板和静态 Attr spec 初始化方式。

## Attribute Specification

需要定义：

- Property / BitField；
- ScriptUsage；
- AttributeProperty；
- Compare；
- Assign；
- Reset；
- RequiresWidgetRebuild；
- HasObjectReferences。

### 默认/当前/待定/镜像

输入 helper 必须区分：

- 用户刚改变真实 Widget；
- 程序刚改变模型；
- 上一轮声明值；
- 初始 Widget 默认值。

2026 年 mutable state 修复可作为参考基线。

## GC

属性值可能包含：

- UObject；
- TObjectPtr；
- 含对象引用的 struct。

FEmmsAttributeValue 使用原生 property initialize/copy/destroy，并在 ARO 中添加引用。新自定义存储不能忽略 GC。

## Event Listener

重建 Widget 时 listener 必须迁移。DelegateProperty 使用 set，Multicast 使用 add；防止重复。即时 Delegate 的 Active/Pending 每 Draw 交换。

## Editor/Runtime

- Runtime helper 不依赖 `UnrealEd`、`PropertyEditor`；
- Details/Editor Tab 放 `EmmsUIEditor`；
- `Target.bCompileAgainstEditor` 只用于必要的条件依赖；
- Cook 验证 Runtime module。

## 新 API 检查表

- 脚本名字；
- overload；
- default args；
- null；
- const/ref；
- attribute reset；
- input conflict；
- event multiplicity；
- rebuild；
- GC；
- hot reload；
- docs；
- tests；
- Cook；
- target UE‑AS protocol。
