# UE‑AS + EmmsUI Wiki

本 Wiki 面向两类读者：

- 需要快速建立正确心智模型的开发者；
- 需要按证据修改项目的 Coding Agent。

## 建议阅读路线

### 第一次使用 UE‑AS

1. [系统模型](01-System-Model.md)
2. [安装与版本固定](02-Install-and-Version-Pinning.md)
3. [项目布局与加载](03-Project-Layout-and-Loading.md)
4. [语言速查](04-Language-Cheatsheet.md)
5. [Actor、Component 与 Subsystem](05-Actors-Components-and-Subsystems.md)
6. [反射、Blueprint 与 C++](06-Reflection-Blueprint-and-Cpp-Interop.md)
7. [热重载与状态](07-Hot-Reload-and-State.md)
8. [测试、CI 与 Cook 模拟](09-Testing-CI-and-Cooked-Simulation.md)

### 第一次使用 EmmsUI

1. [EmmsUI 心智模型](20-EmmsUI-Mental-Model.md)
2. [绘制上下文](21-EmmsUI-Draw-Contexts.md)
3. [布局、属性与 Slot](22-EmmsUI-Layout-Attributes-and-Slots.md)
4. [状态、事件与身份](23-EmmsUI-State-Events-and-Identity.md)
5. [列表、树、Details 与 Paint](24-EmmsUI-Lists-Trees-Details-and-Paint.md)
6. [性能与陷阱](27-EmmsUI-Performance-and-Pitfalls.md)

### 维护插件

1. [C++ 绑定](11-Cpp-Bindings.md)
2. [扩展 EmmsUI](26-Extending-EmmsUI.md)
3. [版本兼容性](31-Version-Compatibility.md)
4. [代码审查清单](34-Code-Review-Checklist.md)

## 快速决策

| 问题 | 结论 |
|---|---|
| UE‑AS 能否装到普通 Launcher 引擎？ | 不能只靠插件；需要包含引擎改动的源码构建。 |
| UObject 引用必须 UPROPERTY 才不会 GC？ | UE‑AS 脚本引用由脚本 GC 管理；UPROPERTY 用于 Unreal 反射。 |
| 所有函数都应 UFUNCTION？ | 否。仅反射、Blueprint、RPC、Delegate、Timer 等边界需要。 |
| Blueprint 函数参数能否叫 `Self`？ | 当前基线不能；这是 Unreal 反射保留名，改为 `Target` 等领域名称。 |
| 所有 UI 都应用 EmmsUI？ | 否。工具/调试/代码驱动 UI 很适合；复杂视觉与动画常更适合 UMG。 |
| EmmsUI 是否每帧新建所有 UWidget？ | 否。声明每帧执行，底层 Widget 会复用和差分更新。 |
| `WasClicked()` 是否等价事件队列？ | 否。它是 Draw 周期的触发消费；需要每个事件时使用即时委托。 |
| Editor 能运行是否代表可打包？ | 否。必须 simulate-cooked + Cook/Package。 |
| 当前锁定 UE‑AS 5.8.1 与 EmmsUI 是否对齐？ | 新 iterator 源码信号已对齐；实际兼容仍需目标 build、脚本、热重载和 Cook 证据。 |

## 当前基线

- UE‑AS：`546c4d6af141f1e820be1b2976211a756ca2639d` / UE 5.8.1；
- EmmsUI：`c5d4e303f1fc8a1545de4d336be19e69dc8518c0`；
- UE‑AS 新 iterator：`1a06a2bf...`；
- EmmsUI 匹配 ListView iterator：`c9985c1...`。

先运行 [版本兼容性](31-Version-Compatibility.md) 中的探针与 smoke matrix，不从“同一时期”推导“已运行通过”。

## 来源与置信度

- 官方行为：来自 Hazelight 文档和源码；
- 源码对齐：双方存在对应协议实现，但尚未等同于目标项目运行证据；
- 源码推断：明确标记为“推断”，需目标版本验证；
- 社区信号：用于选型，不覆盖官方行为；
- 项目事实：目标项目代码、配置和锁定 commit 优先级最高。

见 [Source Map](../references/source-map.md)。
