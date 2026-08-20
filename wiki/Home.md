# UE-AS + EmmsUI Wiki

本 Wiki 面向需要快速建立正确心智模型的开发者，以及需要按项目证据修改代码的 Coding Agent。

## 建议阅读路线

### 第一次接手项目

1. [项目上下文与证据发现](00-Project-Context-and-Discovery.md)
2. [系统模型](01-System-Model.md)
3. [安装与版本固定](02-Install-and-Version-Pinning.md)
4. [项目布局与加载](03-Project-Layout-and-Loading.md)
5. [测试、CI 与 Cook 模拟](09-Testing-CI-and-Cooked-Simulation.md)

### 第一次使用 UE-AS

1. [语言速查](04-Language-Cheatsheet.md)
2. [Actor、Component 与 Subsystem](05-Actors-Components-and-Subsystems.md)
3. [反射、Blueprint 与 C++](06-Reflection-Blueprint-and-Cpp-Interop.md)
4. [热重载与状态](07-Hot-Reload-and-State.md)
5. [网络](08-Networking.md)
6. [C++ Binding](11-Cpp-Bindings.md)

### 第一次使用 EmmsUI

1. [EmmsUI 心智模型](20-EmmsUI-Mental-Model.md)
2. [绘制上下文](21-EmmsUI-Draw-Contexts.md)
3. [布局、属性与 Slot](22-EmmsUI-Layout-Attributes-and-Slots.md)
4. [状态、事件与身份](23-EmmsUI-State-Events-and-Identity.md)
5. [列表、树、Details 与 Paint](24-EmmsUI-Lists-Trees-Details-and-Paint.md)
6. [性能与陷阱](27-EmmsUI-Performance-and-Pitfalls.md)

### 维护与升级

1. [扩展 EmmsUI](26-Extending-EmmsUI.md)
2. [版本兼容性](31-Version-Compatibility.md)
3. [社区与生态](33-Community-and-Ecosystem.md)
4. [代码审查清单](34-Code-Review-Checklist.md)
5. [生态比对报告](../docs/ECOSYSTEM-COMPARISON-2026-08-20.md)
6. [质量 Gate](../docs/QUALITY-GATES.md)

## 快速决策

| 问题 | 结论 |
|---|---|
| 工作区有多个 `.uproject`，能否自动选第一个？ | 不能；列出候选并要求项目证据。 |
| 上游更新了，项目上下文能否直接写 latest SHA？ | 不能；项目 checkout/lock 是当前事实，上游只作为升级候选。 |
| UE-AS 能否只装到普通 Launcher 引擎？ | 不能只靠插件；需要包含引擎修改的源码构建。 |
| UObject 引用必须 UPROPERTY 才不会 GC？ | UE-AS 脚本引用由脚本运行时追踪；UPROPERTY 用于 Unreal 反射边界。 |
| 所有函数都应 UFUNCTION？ | 否。只有 Blueprint、RPC、Delegate、Timer 或反射式 API 等消费者需要。 |
| Blueprint 函数参数能否叫 `Self`？ | 当前基线不能；改用 `Target` 等领域名称。 |
| 所有 UI 都应用 EmmsUI？ | 否。代码驱动工具/调试 UI 很适合，复杂视觉与动画常更适合 UMG。 |
| EmmsUI 是否每帧新建所有 UWidget？ | 否。声明每帧执行，底层 Widget 会复用和差分更新。 |
| `WasClicked()` 是否等价完整事件队列？ | 否。它是 Draw 周期触发消费，需要每个事件时使用即时委托。 |
| 相同 `Iterate()` 是否证明 UE-AS/EmmsUI 完全兼容？ | 否，只能写源码信号对齐，仍需 Build、Script、Runtime、Hot Reload 和 Cook Gate。 |
| Editor 能运行是否代表可打包？ | 否，必须 simulate-cooked、Cook、Package 并启动打包程序。 |

## 当前基线

- UE-AS：`546c4d6af141f1e820be1b2976211a756ca2639d` / UE 5.8.1；
- EmmsUI：`c5d4e303f1fc8a1545de4d336be19e69dc8518c0`；
- UE-AS 新 iterator：`1a06a2bf...`；
- EmmsUI 匹配 ListView iterator：`c9985c1...`。

先运行 [版本兼容性](31-Version-Compatibility.md) 中的探针与 smoke matrix，不从“同一时期”或“相同符号”推导运行兼容。

## 来源与置信度

- 项目事实：目标项目代码、配置、锁定 ref 和当前工具输出，优先级最高；
- 官方行为：Hazelight 文档和源码；
- 源码对齐：双方存在对应协议实现，但不等于目标项目运行证据；
- 源码推断：明确标记为推断，需目标版本验证；
- 社区/skills.sh 信号：用于发现模式与路由边界，不覆盖官方或项目行为。

见 [Source Map](../references/source-map.md) 和 [生态来源锁](../sources/ecosystem-skills.lock.json)。
