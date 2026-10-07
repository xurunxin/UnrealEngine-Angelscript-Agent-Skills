# UnrealEngine-Angelscript Agent Skills

**版本：0.3.0**

面向 **UnrealEngine-Angelscript（UE-AS）+ EmmsUI** 项目的模块化 Agent Skills、Wiki、示例与验证工具。目标不是让 Agent 记住一份长文，而是让它：

1. 先确认项目实际使用的 Unreal、UE-AS 与 EmmsUI ref；
2. 把可变项目事实写入 `.agents/ueas-project-context.md`；
3. 按任务只加载一个主要 Skill，必要时再增加最小 Supporting Skill；
4. 遵守 UE-AS 的反射、热重载、网络、Binding、测试和发布边界；
5. 正确理解 EmmsUI 是“即时式声明前端 + 被保留和复用的 UMG Widget 树”；
6. 将静态源码信号、编译、运行、Cook 和 Package 证据分层报告。

## 安装

### skills.sh / Skills CLI

安装全部 Skills：

```bash
npx skills add xurunxin/UnrealEngine-Angelscript-Agent-Skills
```

只安装 Router：

```bash
npx skills add xurunxin/UnrealEngine-Angelscript-Agent-Skills --skill ueas-router
```

只安装项目上下文 Skill：

```bash
npx skills add xurunxin/UnrealEngine-Angelscript-Agent-Skills --skill ueas-project-context
```

CLI 行为会随版本变化；命令仅作为当前分发入口，Skill 正文不依赖某个具体 Agent 客户端。

### 作为项目内知识包

也可以将仓库放入项目，例如：

```text
<Project>/
  .agent/
    ueas-agent-kit/
  .agents/
    ueas-project-context.md
  Script/
  Content/
```

项目级 `AGENTS.md` 可引用：

```markdown
UE-AS/EmmsUI 任务明确时直接读取对应专题 Skill；跨域或未定位问题读取
`.agent/ueas-agent-kit/skills/ueas-router/SKILL.md`。
只有本任务依赖的项目事实缺失或失效时才加载
`.agent/ueas-agent-kit/skills/ueas-project-context/SKILL.md`，复用其余有效事实。
```

## Skills 路由

| 任务 | 首选 Skill |
|---|---|
| 跨域、模糊、版本敏感任务的最小路由 | `ueas-router` |
| 创建/刷新项目、引擎、插件、模块与 Script roots 上下文 | `ueas-project-context` |
| 源码引擎、首次安装、升级、IDE、版本固定 | `ueas-bootstrap` |
| 基础语法、类、结构体、默认值、代码组织 | `ueas-core-scripting` |
| Actor、Component、Subsystem、输入、Gameplay 架构 | `ueas-gameplay` |
| UPROPERTY、UFUNCTION、Blueprint、Delegate、Timer、UMG | `ueas-reflection-blueprint` |
| RPC、属性复制、OnRep、多人联机 | `ueas-networking` |
| 单元/集成测试、覆盖率、调试、CI | `ueas-testing-debugging` |
| 自动绑定、Mixin、C++ 暴露到脚本、Static JIT 边界 | `ueas-cpp-bindings` |
| simulate-cooked、Cook、Package、缓存、性能 | `ueas-packaging-performance` |
| 非 EmmsUI Editor 菜单、资产工具、Editor subsystem | `ueas-editor-tools` |
| EmmsUI 运行时 UI、Overlay、WidgetComponent | `emmsui-runtime` |
| EmmsUI Editor Tab、Details、Popup、Context Menu | `emmsui-editor-tools` |
| 扩展 EmmsUI C++ helper、属性、事件和模块 | `emmsui-extension` |
| 审查已有 UE-AS / EmmsUI 改动 | `ueas-review` |

入口始终是 [`skills/ueas-router/SKILL.md`](skills/ueas-router/SKILL.md)。

## 项目上下文

首次接手项目或同步 Engine/UE-AS/EmmsUI 后，使用
[`ueas-project-context`](skills/ueas-project-context/SKILL.md) 创建或刷新：

```text
<Project>/.agents/ueas-project-context.md
```

它会记录实际 `.uproject`、源码引擎版本/ref、UE-AS/EmmsUI ref、模块、Target、Script roots、Binding 边界和验证矩阵。多个 `.uproject`、多个 Engine checkout 或重复插件存在时必须报告歧义，不能自动猜选。

## Wiki 入口

从 [`wiki/Home.md`](wiki/Home.md) 开始。高频页面：

- [`wiki/00-Project-Context-and-Discovery.md`](wiki/00-Project-Context-and-Discovery.md)
- [`wiki/02-Install-and-Version-Pinning.md`](wiki/02-Install-and-Version-Pinning.md)
- [`wiki/06-Reflection-Blueprint-and-Cpp-Interop.md`](wiki/06-Reflection-Blueprint-and-Cpp-Interop.md)
- [`wiki/07-Hot-Reload-and-State.md`](wiki/07-Hot-Reload-and-State.md)
- [`wiki/09-Testing-CI-and-Cooked-Simulation.md`](wiki/09-Testing-CI-and-Cooked-Simulation.md)
- [`wiki/20-EmmsUI-Mental-Model.md`](wiki/20-EmmsUI-Mental-Model.md)
- [`wiki/23-EmmsUI-State-Events-and-Identity.md`](wiki/23-EmmsUI-State-Events-and-Identity.md)
- [`wiki/26-Extending-EmmsUI.md`](wiki/26-Extending-EmmsUI.md)
- [`wiki/31-Version-Compatibility.md`](wiki/31-Version-Compatibility.md)
- [`docs/ECOSYSTEM-COMPARISON-2026-08-20.md`](docs/ECOSYSTEM-COMPARISON-2026-08-20.md)

## 0.2.0 生态比对结论

GitHub 与 skills.sh 上存在多套高质量通用 Unreal Engine Skills，但本次检索没有发现另一套同时深入覆盖 **Hazelight UnrealEngine-Angelscript + EmmsUI** 的同类知识包。

0.2.0 借鉴而不复制以下模式：

- Epic Unreal Agent Skills：Skill 应新颖、耐久、工具无关、节省上下文；
- quodsoler：先建立项目上下文，再执行专题任务；
- kevinpbuckley：源码路径验证与 golden task 回归；
- DSTN2000：零假设项目发现；
- gamedev-skills：Router 与 `agents/openai.yaml`；
- skills.sh：标准 `skills/<name>/SKILL.md` 分发布局。

本仓库继续只拥有 UE-AS/EmmsUI 特有边界；Niagara、Mass、Animation、Audio、GAS 等普通 Unreal 领域应交给通用 Unreal Skills，除非任务跨入 UE-AS 的反射、Binding、热重载或 Cook 语义。

详细比对见 [`docs/ECOSYSTEM-COMPARISON-2026-08-20.md`](docs/ECOSYSTEM-COMPARISON-2026-08-20.md)。

## 当前锁定研究快照

核心源码基线记录在 `sources.lock.json`：

- UE-AS 文档：`3864c72fa3c1ef67413dfaad24417bad01879b4d`；
- 用户 UE-AS 引擎：`546c4d6af141f1e820be1b2976211a756ca2639d`；
- Unreal Engine：`5.8.1`；
- EmmsUI：`c5d4e303f1fc8a1545de4d336be19e69dc8518c0`。

生态研究快照记录在 `sources/ecosystem-skills.lock.json`。

当前 UE-AS 与 EmmsUI 的新 `Iterate()` 协议在源码信号层面对齐。正确状态是：

```text
source-signals-aligned-runtime-unverified
```

它不等于完整 C++ build、AngelScript compile、EmmsUI runtime、热重载或 Cook 已通过。

## 验证仓库

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python tools/validate_kit.py .
python scripts/validate_evals.py
python scripts/check_source_refs.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tools tests
```

具备精确 UE-AS Engine 与 EmmsUI checkout 时，再运行：

```bash
python scripts/check_source_refs.py \
  --engine-root "<UE-AS_ENGINE_ROOT>" \
  --emmsui-root "<PROJECT>/Plugins/EmmsUI" \
  --require-roots
```

仓库验证只证明 Skill、链接、Fixture、脚本和引用格式正确。目标项目仍需完成 C++ build、脚本编译、PIE、Dedicated Server、EmmsUI smoke、simulate-cooked、Cook、Package 和打包程序启动检查。完整 Gate 见 [`docs/QUALITY-GATES.md`](docs/QUALITY-GATES.md)。

## 使用原则

- 项目源码、锁定 ref 和当前运行证据高于上游 latest 与社区示例。
- 不把普通 AngelScript 与 UE-AS 定制语法混为一谈。
- 不把 UE-AS 当作可直接复制到 Launcher 引擎的普通项目插件。
- 普通脚本成员/函数优先；只为真实 Unreal 反射消费者增加宏。
- Blueprint 可调用/事件函数参数不要命名为 `Self`。
- 函数体热重载与字段、反射签名、继承、默认组件变化必须分层处理。
- `source-signals-aligned`、`build-passed`、`runtime-smoke-passed` 和 `cook-passed` 不可互相替代。
- EmmsUI 状态放在持久模型中；同父容器内身份敏感的同类兄弟保持稳定结构与顺序。
- 不以“Editor 能运行”代替 simulate-cooked、Cook、Package 和打包程序启动。

## 研究与执行边界

本仓库包含源码级研究、静态工具和测试模板，但不分发 Epic Unreal Engine 源码。本次 0.3.0 仓库验证没有在此环境运行目标 UE 项目的完整引擎构建、PIE、Dedicated Server、Cook 或平台包；这些状态必须保持 `not-run`，直到目标项目提供可观察证据。

0.3.0 的 Astra 指令优化、文本规模和验证范围见 [迁移说明](docs/astra-migration.md)。
