---
name: emmsui-editor-tools
description: >-
  Create hot-reloadable Unreal Editor tabs, detail customizations, popup windows, prompts, context menus, lists, trees, and asset tools with EmmsUI. Use when the UI belongs to Unreal Editor workflows. Do not use for runtime in-game UI or for changing EmmsUI C++ internals.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---


# EmmsUI Editor Tools

## 主要入口

- `UMMEditorUtilityTab`
- `UMMClassDetailCustomization`
- `UMMScriptStructDetailCustomization`
- `UMMPopupWindow`
- `FMMContextMenu`
- 反射 Struct Prompt
- `UDetailsView`
- ListView / TreeView

所有类型放在 Editor-only 编译边界。

## Editor Tab

状态在 Tab 对象成员中持有。打开时初始化，Draw 时只呈现/处理输入，关闭时解绑外部事件。当前 EmmsUI 主分支包含对象重实例化迁移逻辑；旧版本在脚本热重载后可能留下旧 Tab/Slate 引用，升级或回移修复前必须测试。

Actor/World 引用使用 `TWeakObjectPtr`；切换关卡后重新验证。

## 列表与树

ListView 只为可见条目提供 Entry；Draw 时遍历 Entry，而不是把整个数据集创建成 UWidget：

```angelscript
mm<UListView> List = mm::ListView(Items.Num());
for (UMMListViewEntryWidget Entry : List)
{
    DrawEntry(Entry, Items[Entry.ItemIndex]);
}
```

目标引擎必须支持当前 EmmsUI 使用的迭代协议。当前锁定的 UE‑AS 5.8.1 与 EmmsUI 在新 `Iterate()` 协议源码信号上对齐，但仍需兼容探针和最小 ListView 编译；其他 SHA 不能继承该判断。

## Details

- Class Detail：在 `CustomizeDetails` 创建 Immediate Row，Tick/Draw 填充；
- Struct Detail：用 `GetStructValue` / `SetStructValue`；
- 修改对象时保证 Transaction/Modify；
- 不把 UI 缓存的值当作权威数据；每次从被定制对象/结构读取模型。

## Context Menu 与 Popup

上下文菜单选项的回调是 UFUNCTION；使用 `n"Handler"`。长任务不要阻塞菜单回调，转入队列/状态机并提供取消与进度。

## 热重载测试

1. Tab 打开；
2. 修改函数体；
3. 修改脚本字段；
4. 重命名类/Tab；
5. 关闭并重开；
6. 切换关卡；
7. Editor 退出。

检查重复 Delegate、旧对象强引用、Slate 内容丢失和 OnTabOpened/Closed 次数。

## 完成标准

工具支持 Undo/Redo、失效引用、空选择、取消、重复打开和脚本热重载，并通过 simulate-cooked。
