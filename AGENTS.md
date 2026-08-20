# UE-AS / EmmsUI Agent Routing

当任务涉及以下任一内容时，先读取 `skills/ueas-router/SKILL.md`：

- `.as` 文件、`Script/` 目录；
- UnrealEngine-Angelscript、AngelscriptCode、AngelscriptEditor；
- `UPROPERTY`、`UFUNCTION`、`BlueprintOverride`、`BlueprintEvent`；
- `UMMWidget`、`mm::`、`mm<T>`、EmmsUI；
- UE-AS 的测试、网络、预编译脚本、Static JIT 或 C++ Binding。

## 项目上下文门

优先读取 `.agents/ueas-project-context.md`。以下情况先加载 `skills/ueas-project-context/SKILL.md`：

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
