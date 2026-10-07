---
name: ueas-router
description: Use when a UE-AS or EmmsUI task is ambiguous or spans domains. Route to relevant specialists; do not use for a clear specialist task.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS / EmmsUI Router

为当前任务选择需要的专题并继续执行。任务已经明确时直接使用对应 Skill；跨域任务按实际依赖补充专题，不预加载全部 Wiki，也不要求固定格式的路由报告。

## 项目事实

需要项目版本、路径或运行模式时，复用 `<Project>/.agents/ueas-project-context.md` 中仍有效的事实。缺失或变化影响本任务时，使用 `ueas-project-context` 创建或刷新相关部分。独立概念问题、已提供充分事实的代码解释不需要项目扫描。

项目锁定 ref 和当前工作区证据优先于上游 latest。多个项目或插件副本无法通过用户指定路径、配置或运行证据消歧时，先报告候选并确认目标。

## 任务路由

| 任务信号 | Primary Skill | 最近边界 |
|---|---|---|
| 项目根、Engine/UE-AS/EmmsUI ref、模块与 Script roots | `../ueas-project-context/SKILL.md` | 不负责具体功能实现 |
| 安装、源码构建、升级、IDE、版本固定 | `../ueas-bootstrap/SKILL.md` | 项目事实缓存由 Project Context 负责 |
| 语法、类/结构体、值/引用、默认值 | `../ueas-core-scripting/SKILL.md` | 不负责 Gameplay 架构或 Binding |
| Actor、Component、Subsystem、输入、Gameplay | `../ueas-gameplay/SKILL.md` | 反射/网络各自交接 |
| UPROPERTY/UFUNCTION、Blueprint、Delegate、Timer、BindWidget | `../ueas-reflection-blueprint/SKILL.md` | 原生 API 不可见交给 C++ Binding |
| Replicated、RPC、OnRep、Authority、Dedicated Server | `../ueas-networking/SKILL.md` | 普通单机状态交给 Gameplay |
| Unit/Integration/Coverage、异常、调试、CI | `../ueas-testing-debugging/SKILL.md` | 不代替领域实现 Skill |
| 自动绑定、ScriptMixin、FAngelscriptBinds、Static JIT 边界 | `../ueas-cpp-bindings/SKILL.md` | 已反射 API 不需要手工绑定 |
| simulate-cooked、Cook、Shipping、缓存、性能 | `../ueas-packaging-performance/SKILL.md` | 不负责 storefront 发布 |
| 非 EmmsUI Editor 菜单、资产工具、Editor subsystem | `../ueas-editor-tools/SKILL.md` | EmmsUI UI 交给对应 Skill |
| UMMWidget、Overlay、WidgetComponent、运行时 mm:: UI | `../emmsui-runtime/SKILL.md` | Editor Tab 不属于 Runtime |
| EmmsUI Editor Tab、Details、Popup、Context Menu | `../emmsui-editor-tools/SKILL.md` | C++ helper 扩展不属于本 Skill |
| 修改 EmmsUI C++ helper、属性状态、事件或模块 | `../emmsui-extension/SKILL.md` | 现有 helper 组合不需要扩展 |
| 审查 diff、迁移、事故或兼容风险 | `../ueas-review/SKILL.md` | 新功能实现交给领域 Skill |

## 跨专题边界

- Gameplay 需要 Blueprint 消费者时补充 Reflection；跨网络角色时补充 Networking。
- EmmsUI 按 Runtime 或 Editor 场景选用；确认现有 helper 缺能力后才进入 Extension。
- 实现需要专门诊断或新增验证时补充 Testing；进入 Cook、缓存或 Shipping 才加载 Packaging。
- 版本变化先更新项目事实；不要将最新上游 ref 当作已安装版本。

## 执行与证据

UE-AS 需要含引擎修改的源码构建，不能当普通 Launcher 引擎插件安装。专属 API、热重载、反射、Editor 隔离、网络和 UI 身份约束由对应专题提供。

在用户已授权范围内完成实现并持续修复可逆问题。仅请求路由时给出选择及理由；请求实现时路由是过程，不能以待交接计划结束。报告实际执行的编译、运行或发布检查；缺环境写 `not-run`，静态信号写 `source-signal-present` 或 `source-signals-aligned`，不能据此声称 runtime/Cook 成功。
