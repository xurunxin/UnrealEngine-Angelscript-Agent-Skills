# UE-AS / EmmsUI Agent Routing

只在任务涉及 UE-AS/EmmsUI 特有能力时使用本套 Skills。职责明确且相关项目事实有效时直接读取对应专题 `skills/<name>/SKILL.md`；跨域或未定位的问题读取 `skills/ueas-router/SKILL.md`。普通 Unreal C++ 的 UPROPERTY/UFUNCTION 使用不会单独触发本套 Skills。

修改本仓库文档时，只读取受影响入口、链接参考及索引；涉及发布元数据时读取 `scripts/generate_release_metadata.py` 和 `docs/QUALITY-GATES.md`。不要为技能文案维护扫描不存在的 UE 项目。

## 项目上下文门

项目实现需要路径、版本或配置事实时，复用 `.agents/ueas-project-context.md`。以下情况影响当前任务时加载 `skills/ueas-project-context/SKILL.md`：

- 上下文不存在；
- Engine、UE-AS 或 EmmsUI ref 已变化；
- `.uproject`、模块、Target、Script roots、Binding 或目标平台已变化；
- 工作区存在多个项目、Engine checkout 或插件副本；
- 任务依赖尚未确认的项目事实。

多个候选存在时禁止按名称、时间或搜索顺序自动选择。

## 执行不变量

1. 项目锁定 ref 和当前工作区证据高于上游 latest 与社区示例；
2. 默认只加载一个 Primary Skill，按真实依赖增加 Supporting Skill；
3. 普通脚本成员/函数优先，只为真实 Unreal 反射消费者增加宏；
4. 函数体热重载与字段、继承、反射签名、默认组件变化分层处理；
5. Editor-only 代码必须在编译边界隔离；
6. 网络逻辑在真实 client/server 模式验证；
7. EmmsUI 状态由持久模型持有，Draw 结构和身份敏感的兄弟顺序保持稳定；
8. 发布路径分别记录 simulate-cooked、Cook、Package 和打包程序启动证据。

## 证据语言

没有实际执行时使用 `planned` 或 `not-run`。匹配源码符号只能写 `source-signal-present` 或 `source-signals-aligned`，不能写 `runtime compatible`。成功命令不能替代产物、运行或感知质量检查。

已授权实现中，路由、上下文采集和检查是中间步骤；继续完成并修复可逆工作，直到相关验收通过或存在明确环境阻塞。仅概念解释、审查或计划请求保持其原有范围。
