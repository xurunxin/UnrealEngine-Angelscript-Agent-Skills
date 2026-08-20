# Changelog

## 0.2.0 — 2026-08-20

- 新增 `ueas-project-context`，从实际 `.uproject`、源码引擎、UE-AS/EmmsUI ref、模块、Target、Script roots 和 Binding 生成 `.agents/ueas-project-context.md`。
- 重写 `ueas-router`：先判断项目上下文状态，默认只选择一个 Primary Skill，按真实依赖增加 Supporting Skill。
- 重写 `ueas-reflection-blueprint`：以真实反射消费者为依据，缩小 Blueprint 写权限，并区分普通热重载与反射 ABI 结构变化。
- 为全部 Skills 增加正向触发与最近排除边界，并统一 0.2.0 metadata。
- 新增 `agents/openai.yaml`，覆盖 Router、Project Context 和 Reflection Skill。
- 新增基于 PyYAML 的严格 Skill/frontmatter/link 校验器。
- 新增 Routing 与 Behavior Evals，覆盖项目歧义、项目 ref、最小反射面、最小路由、兼容性证据分层和 EmmsUI identity。
- 新增可选的 Engine/EmmsUI 源码引用存在性检查。
- 新增生态比对、质量 Gate、生态来源锁与确定性 Release Metadata 生成脚本。
- 增加 skills.sh / Skills CLI 安装说明。
- GitHub Actions 扩展为 Python 3.11/3.13 矩阵，并运行全部静态验证和单元测试。

## 0.1.1 — 2026-08-20

- 将用户可访问的 UE-AS 快照更新到 `546c4d6a…` / Unreal Engine 5.8.1。
- 移除已失效的“UE 5.5.4 与 EmmsUI 相差约 15 个月”兼容性警告。
- 将当前组合状态改为“新 `Iterate()` 协议信号对齐、运行时未验证”。
- 记录 UE-AS `1a06a2bf...` 与 EmmsUI `c9985c1...` 的对应 iterator 实现。
- 修复兼容性探针只扫描 `Source/`、从而漏掉 `ThirdParty` 协变模板标志的问题。
- 新增当前对齐组合、历史已淘汰组合、旧引擎和反射参数 `Self` 的回归检查。

## 0.1.0 — 2026-08-20

- 初始发布。
- 14 个按需加载 Skills。
- 30+ Wiki/参考页面。
- UE-AS 与 EmmsUI 原创示例。
- 兼容性探针、文档验证器、CI 模板。
