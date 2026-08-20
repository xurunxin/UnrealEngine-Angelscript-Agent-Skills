# 研究报告与 0.2.0 结论

## 1. 系统边界

### UE-AS 不是普通项目插件

UnrealEngine-Angelscript 同时包含 Unreal Engine 源码修改与 Angelscript 插件。正确起点是固定一个 UE-AS 源码引擎 ref、构建 Editor，并在项目中使用真实 `Script/` roots。把某个插件目录复制到 Launcher 引擎或 `Project/Plugins` 不是完整安装方案。

### 合理职责分层

- C++：底层引擎扩展、性能关键算法、平台能力、第三方库和必要 Binding；
- UE-AS：Gameplay 编排、Actor/Component/Subsystem、易变业务规则和部分 Editor 工具；
- Blueprint：资产装配、设计师配置、动画与窄表现 Hook；
- EmmsUI：代码驱动、频繁迭代的 Runtime/Editor 工具 UI；
- UMG/Slate：复杂视觉、动画、无障碍和成熟资产工作流。

### EmmsUI 是即时式 API + 保留式 UMG 后端

每次 Draw 重新声明 UI，但底层通过类型、父 Element 和身份规则复用 Widget，并维护属性状态与事件监听。即时式控制流不等于每帧新建所有 UObject，也不取消 UMG 生命周期、焦点、布局和重建成本。

## 2. 当前源码基线

| 组件 | 观察快照 | 状态 |
|---|---|---|
| UE-AS 文档 | `3864c72…` | 文档基线 |
| UE-AS 引擎 | `546c4d6…` / UE 5.8.1 | 用户同步后的项目基线 |
| EmmsUI | `c5d4e303…` | 当前观察主分支 |

UE-AS `1a06a2bf...` 与 EmmsUI `c9985c1...` 存在匹配的新 `Iterate()` 协议实现。因此可以确认源码信号对齐，但不能据此确认完整 ABI、项目插件组合、输入状态、热重载、Cook 或 Package 通过。

正确状态：

```text
source-signals-aligned-runtime-unverified
```

## 3. GitHub 与 skills.sh 比对

本次检索重点包括 Unreal Engine、AngelScript、UnrealEngine-Angelscript、EmmsUI 和 Agent Skills。skills.sh 返回了 `unreal-development`、`unreal-engine` 以及 quodsoler 的多项 UE 专题 Skills，但未发现另一套同时覆盖 UE-AS 与 EmmsUI 的同类套件。

### 高价值模式

- **Epic Unreal Agent Skills**：Skill 应提供工具无法直接发现的知识，保持新颖、耐久、工具无关和精简；
- **quodsoler**：建立项目上下文文件，让后续 Skills 不重复猜测版本、模块和插件；
- **kevinpbuckley**：以精确 UE 版本、真实源码路径和 golden tasks 约束 API 漂移；
- **DSTN2000**：零假设发现 `.uproject`、插件和项目模式；
- **gamedev-skills**：Router 只选择最小 Skill 集，并提供 `agents/openai.yaml`；
- **skills.sh**：标准目录支持一条命令安装和公开发现。

### 不应照搬

- 不把通用 UE C++ 内容复制成第二套 Niagara、GAS、Animation、Audio、Mass 文档；
- 不让 MCP、Claude Code、Codex 或某个编辑器工具名成为 Skill 的硬依赖；
- 不以 installs、stars 或第三方安全徽章作为 API 正确性证据；
- 不把固定机器绝对路径写入可复用 Skill；
- 不用一个超大 Unreal Skill 吞掉全部专题路由。

详细来源、commit 与采用范围见 `sources/ecosystem-skills.lock.json` 和 `docs/ECOSYSTEM-COMPARISON-2026-08-20.md`。

## 4. 0.2.0 架构升级

### 项目上下文成为第一道版本门

新增 `ueas-project-context`，生成 `.agents/ueas-project-context.md`。它把项目根、Engine/UE-AS/EmmsUI ref、dirty state、模块、Target、Script roots、Binding、网络拓扑与验证 Gate 作为项目事实缓存。

多个 `.uproject`、多个 Engine checkout 或重复插件存在时必须报告歧义。上游 latest 与项目 ref 分开记录，不能自动覆盖。

### Router 只加载最小 Skill 集

Router 先判断项目上下文为 `current/stale/missing/not-needed`，再选择一个 Primary Skill。只有真实产物依赖才增加 Supporting Skill。Runtime EmmsUI、Editor EmmsUI 和 C++ Extension 不再默认一起加载。

### 反射按消费者设计

`ueas-reflection-blueprint` 要求先标记 `script-only/editor-details/blueprint-read/blueprint-write/serialization/replication/delegate/timer/BindWidget` 等真实消费者。内部缓存与 helper 保持普通脚本成员；Blueprint 写权限优先通过命令函数和窄 Hook，而不是批量 `BlueprintReadWrite`。

### 证据分层

仓库统一使用：

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

任何阶段都不能跨级报告。

## 5. 质量系统

0.2.0 引入：

- PyYAML 严格 frontmatter 校验；
- 全部 Skill 正向触发与最近排除边界；
- Markdown 链接与仓库逃逸检查；
- Router/Project Context/Reflection Routing Evals；
- 多项目歧义、项目 ref、最小反射面、最小路由、兼容性和 EmmsUI identity Behavior Evals；
- 可选的 Engine/EmmsUI 源码引用存在性检查；
- 确定性 Manifest、Skill Index 和 SHA256SUMS 生成。

这些验证只能证明仓库静态质量，不替代目标 Unreal 项目的 Build 与 Runtime Gate。

## 6. 持续最佳实践

- 普通脚本成员/函数优先，只在真实 Unreal 反射边界增加宏；
- 默认值区分脚本初始化、CDO、Blueprint Defaults 和实例覆盖；
- Blueprint 只覆盖窄表现 Hook，核心不变量在不可绕过的入口执行；
- Editor-only 类型在目录、预处理、模块和 cooked 签名处同时隔离；
- 高频可丢 RPC 明确 `Unreliable`，持久状态依赖复制属性；
- EmmsUI 同父同类节点结构与顺序保持稳定，业务状态放持久模型；
- `Was...` 是 Draw 周期触发消费，不是完整事件队列；
- 双向输入引用必须指向持久状态；
- 发布必须经过 simulate-cooked、Cook、Package 和打包程序启动。

## 7. 本环境未执行

- UE 5.8.1 / UE-AS 全量引擎构建；
- 目标项目 C++ 与 AngelScript 编译；
- Soft/Structural Hot Reload；
- PIE 与 Dedicated Server；
- EmmsUI 输入、ListView/TreeView、Overlay 和 Editor Tab smoke；
- Static JIT 与 Precompiled Script；
- Cook、Package 和打包程序启动。

这些状态保持 `not-run`，不能从仓库静态验证推导。
