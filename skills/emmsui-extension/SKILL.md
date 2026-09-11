---
name: emmsui-extension
description: Use when extending EmmsUI C++ helpers, state, events or bindings. Do not use when existing helpers can compose the required UI.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# Extending EmmsUI

## 先判断是否真的需要 C++ helper

`mm<T>` 会为原生 UWidget 的可见/可编辑反射属性自动生成 `SetX/GetX`，为 Delegate/Event 自动生成 `WasX/OnX`。先尝试：

```angelscript
mm<UMyWidget> Widget = mm::Widget(UMyWidget);
Widget.SetSomeProperty(Value);
if (Widget.WasSomeEvent())
{
}
```

只有组合语义、双向状态、特殊 SlateBrush/Material、虚拟化、定制事件回复或性能需要时新增 helper。

## 内部模型

- `FEmmsWidgetIdentifier`：Widget 类型 + 父 Element + Hash；
- `FEmmsWidgetElement`：UMG Widget、Slot、Active/Pending children、属性与监听器；
- `FEmmsAttributeState`：Default、Current、Pending、Mirrored；
- `UMMWidget`：Draw 调度、复用池、属性/层级更新；
- `UEmmsEventListener`：拦截 UMG delegate，记录触发与参数；
- `EmmsScriptBinds.cpp`：注册 `mm<T>` 和反射生成 API。

详见 [`../../wiki/26-Extending-EmmsUI.md`](../../wiki/26-Extending-EmmsUI.md)。

## 新 helper 设计

1. 使用 `UEmmsStatics::AddWidget` 获取或复用节点；
2. 通过 AttributeState 设置 Pending 值，而不是直接长期修改 UWidget；
3. 若 helper 是输入控件，处理双向状态：
   - 当前 UWidget 输入；
   - 上一帧 mirrored 输入；
   - 上一帧声明属性；
   - 本帧模型值；
4. 为对象/Struct 属性正确处理 GC references；
5. 属性只读/构造时决定是否 `bRequiresWidgetRebuild`；
6. 事件明确提供 `Was...`、`On...` 或两者；
7. 增加脚本文档 metadata；
8. 编写脚本示例与自动化测试。

## 模块边界

运行时 helper 放 `EmmsUI`；Editor Tab、Details、PropertyEditor/UnrealEd 依赖放 `EmmsUIEditor`。Runtime module 不得无条件依赖 Editor module。

## 高风险点

- 直接 UWidget 改动未恢复；
- 对 FText/FSlateBrush/UObject 属性做裸 `memcpy`；
- Pending/Current 值析构或 GC 不完整；
- 每帧触发 rebuild；
- Listener 迁移到重建 Widget 后重复绑定；
- 缺失 EndDraw 导致全局隐式栈污染；
- 静态全局状态跨 World/PIE；
- 目标 UE‑AS 与 EmmsUI 的 iterator protocol 单侧更新；当前锁定组合源码信号已对齐，但未来 commit 仍需重新探测和编译。

## 验证矩阵

- 第一次创建与后续复用；
- 属性设置、变化、下一帧省略；
- Widget 重建；
- 条件分支和顺序变化；
- 输入与程序值同时变化；
- 同帧多事件；
- GC；
- Script hot reload；
- Editor Tab hot reload；
- Cook/Shipping；
- ListView 大数据与性能。

## 输出契约

插件修改必须附一份“脚本 API 前后对比”、目标 commit、测试和回滚方式。
