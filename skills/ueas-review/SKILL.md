---
name: ueas-review
description: >-
  Review UnrealEngine-Angelscript and EmmsUI changes for correctness, reflection surface, hot reload, cooked builds, networking, UI identity, performance, and version compatibility. Use when reviewing an existing diff, migration, or incident. Do not use as the primary implementation Skill for a new feature.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---


# UE‑AS / EmmsUI Review

## 审查顺序

1. 版本与目标分支；
2. 功能正确性；
3. UE 反射与生命周期；
4. 热重载；
5. Editor/Cook 边界；
6. 网络；
7. EmmsUI 身份、状态、事件；
8. 性能；
9. 测试与发布证据。

## UE‑AS 检查

- 是否误用了普通 AngelScript/C++ 语法；
- UPROPERTY/UFUNCTION 是否确有需要；
- BlueprintCallable/BlueprintEvent 参数是否错误命名为 `Self`；
- 默认值是否声明式；
- Blueprint 是否能跳过核心不变量；
- Delegate/Timer handler 是否为 UFUNCTION；
- `n""` 是否用于稳定 FName；
- World Context 和 Subsystem 生命周期是否正确；
- `float` 精度是否明确；
- Editor-only 类型是否泄漏；
- 是否依赖不支持的 Interface 或 C++ BlueprintNativeEvent Super；
- 结构性改动是否说明重实例化风险。

## 网络检查

- Authority/Ownership；
- Reliable 频率；
- 持久状态与一次事件是否混淆；
- OnRep 的服务器本地表现；
- Dedicated Server 测试。

## EmmsUI 检查

- Begin/End 成对；
- 状态是否持久；
- 同类兄弟顺序是否稳定；
- Slot 属性是否在目标 Widget 前；
- `Was...`/`On...` 语义是否合适；
- ListView 是否虚拟化；
- Draw 是否含重任务/同步加载；
- `GetUnderlyingWidget()` 修改是否复位；
- 设置的属性是否会每帧触发重建；
- Editor 引用是否 Weak；
- 目标 UE‑AS 是否支持当前迭代/绑定协议；当前锁定组合源码信号对齐，但必须检查实际 SHA 与编译证据。

## 严重级别

- **阻断**：编译/Cook 失败、权限漏洞、网络权威错误、对象生命周期破坏、版本 API 不存在；
- **高**：状态错位、重复事件、Reliable 洪泛、热重载数据破坏、Editor-only 泄漏；
- **中**：过度反射、Tick/Draw 性能、缺测试、可维护性；
- **低**：命名、格式、文档。

## 输出

每个发现包含：位置、触发条件、实际影响、证据、最小修复、验证步骤。不要把风格偏好伪装成缺陷。
