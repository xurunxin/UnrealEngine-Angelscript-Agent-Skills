---
name: ueas-router
description: >-
  Route a version-sensitive or cross-cutting UnrealEngine-Angelscript and EmmsUI
  request to the smallest useful specialist Skill set while preserving project facts
  and evidence gates. Use when the task is ambiguous, spans multiple UE-AS domains,
  or depends on unknown engine/plugin context. Do not use for a single clearly scoped
  specialist task after the project context is already current.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS / EmmsUI Router

## 产物

输出一个最小路由决定，而不是把全部 Skill 和 Wiki 注入上下文：

```yaml
Route:
  project_context: current | stale | missing | not-needed
  primary_skill: ""
  supporting_skills: []
  references_to_load: []
  evidence_required: []
  excluded_skills: []
```

## 何时使用

使用本 Router：

- 请求只说“UE-AS/EmmsUI 出问题”但未定位层级；
- 同时涉及升级、反射、网络、Binding、UI、热重载或发布中的两个以上领域；
- 版本、项目根、插件来源、Script roots 或目标运行模式未知；
- 需要从研究、实现、验证到迁移形成跨 Skill 交接；
- 审查现有改动，但风险分布尚不清楚。

不要使用本 Router：

- 已知项目上下文且任务明确属于一个专题 Skill；
- 纯通用 Unreal/C++ 问题，不涉及 UE-AS 或 EmmsUI 特有边界；
- 只需要解释一个已提供的代码片段且无需项目事实。

## 第一步：判断项目上下文

检查 `<Project>/.agents/ueas-project-context.md`：

- `current`：来源仍有效，任务依赖的字段已确认；直接路由。
- `stale`：Engine/UE-AS/EmmsUI ref、模块、Script roots、Binding 或目标平台已改变；先加载 `ueas-project-context` 的 `refresh` 模式。
- `missing`：任务依赖项目事实但文件不存在；先加载 `ueas-project-context` 的 `create` 模式。
- `not-needed`：任务是稳定概念解释，或用户已提供完成任务所需的精确事实。

不得因为仓库名、版本目录或上游最新提交看起来合理就把上下文标为 current。

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

## 多 Skill 规则

默认只选一个 Primary Skill。只有存在真实输入/输出依赖时才增加 Supporting Skill：

- `project-context → bootstrap`：先确认当前基线，再设计升级；
- `gameplay → reflection`：Gameplay 产物确实需要 Blueprint/Editor 消费；
- `gameplay → networking`：状态必须跨 Authority/客户端；
- `runtime/editor EmmsUI → extension`：现有 helper 明确缺能力且源码证据已确认；
- `任意实现 → testing`：需要新增领域验证；
- `任意发布相关实现 → packaging`：进入 Cook/Shipping 路径。

不要把“可能相关”当依赖。Runtime EmmsUI、Editor EmmsUI 和 EmmsUI Extension 不应默认同时加载。

## 全局不变量

- UE-AS 是修改过的 Unreal 源码引擎加插件，不是普通项目插件。
- 项目锁定 ref 与工作区证据高于上游 latest 和社区示例。
- `source-signals-aligned` 不等于 build、runtime 或 Cook 通过。
- 普通脚本成员/函数优先；只有跨 Unreal 反射边界时才添加宏。
- 函数体热重载与反射/字段/继承结构变化必须分开处理。
- Editor-only 类型不能泄漏到 cooked Runtime 签名与资产依赖。
- 网络行为必须在真实 client/server 模式验证。
- EmmsUI 状态由持久模型持有，Draw 结构和同类兄弟顺序保持稳定。
- 任何发布结论必须给出 simulate-cooked、Cook、Package 和启动证据的实际状态。

## 证据语言

允许：

```text
planned
not-run
source-signal-present
source-signals-aligned
build-passed
script-compile-passed
runtime-smoke-passed
cook-passed
package-launch-passed
```

禁止把计划、静态检查、成功命令或 Worker 总结升级成未观察到的运行结论。

## 输出契约

```yaml
Result:
  project_context: current | stale | missing | not-needed
  primary_skill: ""
  supporting_skills: []
  facts_used: []
  assumptions: []
  evidence_required: []
  excluded_skills:
    - skill: ""
      reason: ""
  runtime_gates:
    build: not-run
    script_compile: not-run
    pie: not-run
    dedicated_server: not-run
    cook: not-run
    package_launch: not-run
  next_handoff:
    skill: null
    completion_gate: "observable pass condition"
```
