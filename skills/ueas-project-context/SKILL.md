---
name: ueas-project-context
description: Use when UE-AS project facts are missing or stale to verify the engine, plugins and Script roots. Do not use for context-independent questions.
compatibility: Requires read access to the project and its source-engine checkout; Git metadata is optional but preferred.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS Project Context

创建、刷新或审查 `<Project>/.agents/ueas-project-context.md`，供后续任务复用已核实事实。缓存只保留会影响实现、路由和验收的内容；未知信息明确标注，不以填满模板为目标。

## 按任务取证

- `create`：目标项目尚无上下文，使用 [模板](templates/ueas-project-context.md) 和 [项目采集流程](references/project-discovery.md)。
- `refresh`：只复核变化及本任务依赖的事实，保留已确认的稳定约定；需要定位路径时读取 [discovery map](references/discovery-map.md)。
- `review`：检查来源有效性、冲突和未知项；仅审查请求无需重写文件。

明确项目路径或现有配置可以直接确定目标。多个 `.uproject`、Engine 或插件副本无法消歧时，报告候选和缺失证据，不按名称、时间或搜索顺序猜测。没有项目文件时记录阻塞，不把任意 Script/Content 目录当项目根。

## 事实与范围

用户指定的项目和 ref、实际 checkout/config、项目锁与构建记录优先于当前上游文档和社区示例。实际值与用户期望冲突时分别记录；未经升级，不把 upstream latest 写为项目 ref。

记录适用的 Engine/UE-AS/EmmsUI 来源与 commit、模块/Target、Script roots、Binding、运行拓扑和验证要求。缺失、重复或未启用组件也应明确记录。共享文档中的私有绝对路径可使用占位符。每个可变事实保留 `value`、`status`（confirmed/inferred/unknown/stale）、`source` 和 `observed_at`。

## 何时刷新

`.uproject`、`.uplugin`、Build.version、ref/相关 dirty 文件、模块、Target、Script roots、Binding、测试配置或目标平台变化会使相关缓存过期。来源路径消失或用户指出变化时同样复核。与任务无关的变化无需触发全项目扫描。

## 完成

创建/刷新后重新读取实际文件，确认目标唯一、适用事实有来源或 unknown，旧 ref 未被上游值覆盖。`source-signals-aligned`、build、script compile、runtime smoke、Cook、package launch 分层记录，未执行写 `not-run`。

如果上下文维护是实现任务的一部分，完成后直接继续该任务；需要用户解决的项目歧义只阻塞依赖它的操作。报告更新范围和未确认项即可，不要求重复输出整份缓存。
