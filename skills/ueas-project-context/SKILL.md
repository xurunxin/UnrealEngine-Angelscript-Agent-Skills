---
name: ueas-project-context
description: >-
  Create or refresh a verified `.agents/ueas-project-context.md` for an
  UnrealEngine-Angelscript project by discovering the actual Unreal source build,
  UE-AS and EmmsUI refs, project modules, Script roots, bindings, and validation
  gates. Use when onboarding an unfamiliar project, after syncing or upgrading the
  engine/plugins, or when project facts are missing or stale. Do not use for generic
  Unreal questions or a narrowly scoped code change whose project context is already current.
compatibility: Requires read access to the project and its source-engine checkout; Git metadata is optional but preferred.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS Project Context

## 产物

创建或刷新：

```text
<Project>/.agents/ueas-project-context.md
```

这个文件是项目事实缓存，不是第二份长篇教程。它让后续 Skill 知道当前项目实际使用的
Unreal、UE-AS、EmmsUI、模块、Script roots、网络拓扑与验证要求，避免根据目录名、最新
上游或通用 Unreal 经验猜测。

需要确定扫描位置和证据来源时，加载
[`references/discovery-map.md`](references/discovery-map.md)。创建文件时使用
[`templates/ueas-project-context.md`](templates/ueas-project-context.md)。

## 使用边界

使用本 Skill：

- 第一次接手一个 UE-AS 项目；
- `.agents/ueas-project-context.md` 不存在；
- UE-AS 引擎、EmmsUI、项目插件或默认分支刚刚更新；
- 同一工作区存在多个 `.uproject`、多个 Engine checkout 或多个 EmmsUI 副本；
- 任务依赖模块、Target、Script root、Cook、Dedicated Server 或 Binding 事实；
- 现有上下文中的 commit、版本或文件证据已经失效。

不要使用本 Skill：

- 只解释通用 UE/AngelScript 概念；
- 项目事实已明确且任务只属于一个专题 Skill；
- 仅需审查一个已给出的补丁，且补丁不改变项目基线；
- 用它替代真实编译、PIE、Dedicated Server、Cook 或 Package 验证。

## 模式

- `create`：上下文不存在，从项目和引擎证据创建。
- `refresh`：重新读取可变事实，保留人工确认的稳定约定。
- `review`：检查上下文是否过期、矛盾、缺证据或混用上游与项目基线。

## 真值顺序

1. 用户明确指定的项目、引擎和 ref；
2. 当前运行实际读取到的 `.uproject`、`Build.version`、`.uplugin`、Git ref 和配置；
3. 项目锁文件、子模块、构建记录与 CI 配置；
4. 当前官方文档和上游源码；
5. 社区 Skill、帖子和示例；
6. 明确标注的假设。

`upstream latest` 不能覆盖项目锁定 ref。提交时间接近、协议符号相同或静态探针通过，只能
说明源码信号，不等于完整运行兼容。

## 工作流

### 1. 确定唯一项目根

查找 `.uproject`，同时记录工作区边界。

- 找到一个：以它的父目录为项目根。
- 找到多个：列出候选及证据，停止自动选择；除非用户或已有项目配置明确指定。
- 找不到：报告缺失，不把任意 `Script/` 或 `Content/` 目录当项目根。

不得按“最近修改”“目录名最像”或第一个搜索结果静默选择。

### 2. 识别实际 Unreal 源码构建

读取：

- `.uproject` 的 `EngineAssociation`；
- `<Engine>/Engine/Build/Build.version`；
- 引擎 Git branch、commit、dirty 状态（可用时）；
- 项目脚本、构建脚本或环境文件中明确记录的 Engine root。

确认这是包含 UE-AS 修改的源码引擎，而不是仅根据目录名推断。记录引擎路径时允许在共享
文档中使用占位符或相对描述，避免泄露私有绝对路径。

### 3. 识别 UE-AS 插件与源码 ref

优先核对：

```text
<Engine>/Engine/Plugins/Angelscript/Angelscript.uplugin
<Engine>/Engine/Plugins/Angelscript/Source/
```

记录插件来源、实际 commit、是否 dirty、主要模块和版本敏感信号。若项目另有同名插件，
必须报告重复来源，不能假定哪一个生效。

### 4. 识别 EmmsUI

在项目与引擎插件目录中查找 `EmmsUI.uplugin`，记录：

- 生效位置与是否存在重复副本；
- Git ref/commit 与 dirty 状态；
- Runtime/Editor 模块；
- 项目是否实际启用；
- ListView、mutable input、Editor Tab reinstancing 等版本敏感能力的源码证据。

源码能力存在只写 `source-signal-present`；完成目标项目编译和 smoke 后才能写 `passed`。

### 5. 扫描项目结构

读取并归纳：

- `.uproject` 模块和插件；
- `Source/**/*.Build.cs`、`*.Target.cs`；
- 项目与插件 `Script/` 目录、额外 Script roots；
- `Config/*.ini` 中 Angelscript、测试、地图和 Cook 相关设置；
- 自定义插件、Editor 模块和 ThirdParty 模块；
- 现有 `AGENTS.md`、编码规范、测试说明与版本锁。

只记录会改变实现、路由或验收的事实，不把所有文件清单灌入上下文。

### 6. 识别 C++ Binding 边界

搜索项目模块中与以下内容相关的实现：

```text
FAngelscriptBinds
ScriptMixin
AngelscriptCode
AngelscriptBinds
AS_FORCE_LINK
```

记录 Binding 所属模块、初始化顺序、Runtime/Editor 边界和已有测试。不要因为某个原生 API
在脚本中不可见就立即设计手工绑定；先确认自动反射或 Mixin 是否已经覆盖。

### 7. 记录项目约定与风险

至少覆盖：

- 反射默认策略和 Blueprint 边界；
- Soft/Structural Hot Reload 的允许范围；
- 网络拓扑、Authority 和 Dedicated Server 要求；
- EmmsUI 的使用位置与 Widget identity 约束；
- Cook/Package、Static JIT、Precompiled Script 的发布 Gate；
- 当前已知 Blocker 与人工决定。

不能从代码可靠推断的团队约定标为 `unknown`，不虚构。

### 8. 写入上下文

使用模板生成小而可维护的文件。每个可变事实至少包含：

```yaml
value: ""
status: confirmed | inferred | unknown | stale
source: "file/ref/tool observation"
observed_at: "YYYY-MM-DD"
```

对路径和 commit 使用可复制值；对兼容性使用分层状态：

```text
not-checked
source-signals-aligned
build-passed
script-compile-passed
runtime-smoke-passed
cook-passed
package-launch-passed
```

不得跨级推断。

## 过期规则

发生以下任一变化时刷新：

- `.uproject`、`.uplugin`、`Build.version`、Git ref 变化；
- Engine、UE-AS 或 EmmsUI 工作区变脏；
- 模块、Target、Script root、Binding 或测试配置变化；
- 网络拓扑、目标平台或发布方式变化；
- 上下文中的来源路径不再存在；
- 用户明确指出事实已更新。

人工确认的设计原则可以保留，但必须与新的项目证据重新核对。

## 完成门

只有满足以下条件才可声称上下文已创建或刷新：

- 唯一项目根已确认；
- Engine/UE-AS/EmmsUI 的“确认、未知或重复”状态均已记录；
- 模块、Script roots、Binding 与主要验证 Gate 已覆盖；
- 每个可变事实有来源或明确 `unknown`；
- 没有把上游最新 ref 当成项目 ref；
- 文件已实际写入并重新读取检查。

## 输出

```yaml
Result:
  mode: create | refresh | review
  context_path: .agents/ueas-project-context.md
  project_root_status: confirmed | ambiguous | missing
  engine_ref: null
  ueas_ref: null
  emmsui_ref: null
  duplicate_candidates: []
  facts_confirmed: []
  facts_unknown: []
  stale_facts_replaced: []
  evidence: []
  runtime_gates:
    build: not-run
    script_compile: not-run
    pie: not-run
    dedicated_server: not-run
    cook: not-run
    package_launch: not-run
  next_handoff:
    skill: ueas-router
    completion_gate: "route using the refreshed project facts"
```
