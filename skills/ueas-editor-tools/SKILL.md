---
name: ueas-editor-tools
description: Build Unreal Editor automation and tools in Angelscript with editor-only compilation, menu extensions, CallInEditor actions, asset operations, prompts, UMG, and subsystem lifetimes.
---


# UE‑AS Editor Tools

## 编译边界

完整工具脚本放入 `Script/**/Editor/`，或用：

```angelscript
#if EDITOR
// editor-only types
#endif
```

当前 UE‑AS 基线会把 Editor 目录脚本生成的 UASClass/UASStruct 标为 Editor-only；这改善了 Blueprint 编译，但不允许运行时类型的字段或函数签名引用 Editor-only 类型。每次修改后仍要运行 simulate-cooked。

## 可用模式

- `CallInEditor` Details 按钮；
- `UScriptActorMenuExtension`；
- `UScriptAssetMenuExtension`；
- `UScriptEditorMenuExtension`；
- Toolbar/Menu extension point；
- `UScriptEditorSubsystem`；
- Scriptable Editor Widget/UMG；
- EmmsUI Editor Tab、详情定制、弹窗和上下文菜单。

## 事务与资产安全

任何修改关卡 Actor、资产或属性的工具都要考虑：

- `Modify()` / Transaction / Undo；
- Dirty 标记；
- 保存由用户确认；
- 批量操作的取消与进度；
- 只处理显式选择或筛选结果；
- 软引用与加载；
- World/Level 切换；
- 异常后恢复。

不要在 Tick 中重复执行有副作用操作。UI Draw 只收集输入；实际任务由显式按钮、队列或状态机启动。

## 引用生命周期

编辑器 Tab 持有 Actor/资产时优先 Weak/Soft 引用。强引用可能让已关闭关卡对象继续存活，阻止 World 正常销毁。

## 操作设计

复杂参数使用反射 struct + Prompt，而不是几十个临时输入框。把业务操作写成独立函数并可单测；UI 仅做参数采集、确认和进度呈现。

## 验证矩阵

- 新开 Editor；
- 工具打开/关闭多次；
- 切换关卡；
- Script hot reload；
- Undo/Redo；
- 取消操作；
- 空选择、失效对象、只读资产；
- simulate-cooked；
- 重启后无残留注册/重复菜单。

## 何时切换到 EmmsUI

频繁变化、代码驱动、工具型 UI：EmmsUI。
复杂动画、视觉资产、设计师编辑：UMG。
深度 Slate 交互或性能/可访问性要求：C++ Slate。
