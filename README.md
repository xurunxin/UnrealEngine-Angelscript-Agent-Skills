# UnrealEngine‑Angelscript Agent Kit

**版本：0.1.1**

面向 **UnrealEngine‑Angelscript（UE‑AS）+ EmmsUI** 项目的模块化 Skills 与 Wiki。目标不是让 Agent 记住一份长文，而是让它：

1. 先识别项目实际使用的 Unreal、UE‑AS 与 EmmsUI 版本；
2. 按任务只加载需要的 Skill；
3. 遵守 UE‑AS 的反射、热重载、网络、测试与发布边界；
4. 正确理解 EmmsUI 是“即时式声明前端 + 被保留和复用的 UMG Widget 树”，而不是每帧无条件重建全部 UObject；
5. 在修改源码前给出可验证的最小方案，并运行对应的编译、测试或兼容性检查。

## 快速使用

将整个目录放入项目，例如：

```text
<Project>/
  .agent/
    ueas-agent-kit/
  Script/
  Content/
```

Agent 的项目级入口可以引用：

```markdown
当任务涉及 `.as`、UnrealEngine‑Angelscript、AngelscriptCode、EmmsUI、`UMMWidget`
或 `mm::` 时，先读取 `.agent/ueas-agent-kit/skills/ueas-router/SKILL.md`。
```

也可以直接复制本包根目录的 `AGENTS.md` 片段到项目说明中。

## Skills 路由

| 任务 | 首选 Skill |
|---|---|
| 环境、源码引擎、版本固定、首次安装 | `ueas-bootstrap` |
| 基础语法、类、结构体、默认值、代码组织 | `ueas-core-scripting` |
| Actor、Component、Subsystem、输入、Gameplay 架构 | `ueas-gameplay` |
| UPROPERTY、UFUNCTION、Blueprint、委托、计时器、UMG | `ueas-reflection-blueprint` |
| RPC、属性复制、OnRep、多人联机测试 | `ueas-networking` |
| 单元测试、集成测试、覆盖率、调试、CI | `ueas-testing-debugging` |
| 自动绑定、Mixin、C++ 暴露到脚本 | `ueas-cpp-bindings` |
| Cook、simulate-cooked、预编译缓存、性能与发布 | `ueas-packaging-performance` |
| 编辑器菜单、工具、详情面板、Editor-only 脚本 | `ueas-editor-tools` |
| EmmsUI 运行时 UI、Overlay、WidgetComponent | `emmsui-runtime` |
| EmmsUI 编辑器标签页、详情定制、弹窗、上下文菜单 | `emmsui-editor-tools` |
| 扩展 EmmsUI C++ helper、属性、事件、模块 | `emmsui-extension` |
| 审查已有 UE‑AS / EmmsUI 改动 | `ueas-review` |

入口始终是 [`skills/ueas-router/SKILL.md`](skills/ueas-router/SKILL.md)。

## Wiki 入口

从 [`wiki/Home.md`](wiki/Home.md) 开始。高频页面：

- [`wiki/02-Install-and-Version-Pinning.md`](wiki/02-Install-and-Version-Pinning.md)
- [`wiki/06-Reflection-Blueprint-and-Cpp-Interop.md`](wiki/06-Reflection-Blueprint-and-Cpp-Interop.md)
- [`wiki/07-Hot-Reload-and-State.md`](wiki/07-Hot-Reload-and-State.md)
- [`wiki/09-Testing-CI-and-Cooked-Simulation.md`](wiki/09-Testing-CI-and-Cooked-Simulation.md)
- [`wiki/20-EmmsUI-Mental-Model.md`](wiki/20-EmmsUI-Mental-Model.md)
- [`wiki/23-EmmsUI-State-Events-and-Identity.md`](wiki/23-EmmsUI-State-Events-and-Identity.md)
- [`wiki/26-Extending-EmmsUI.md`](wiki/26-Extending-EmmsUI.md)
- [`wiki/31-Version-Compatibility.md`](wiki/31-Version-Compatibility.md)

## 当前锁定的研究快照

本包内容基于 `sources.lock.json` 中记录的源码快照：

- UE‑AS 官方文档源码：`3864c72fa3c1ef67413dfaad24417bad01879b4d`
- 用户当前 UE‑AS 引擎基线：`546c4d6af141f1e820be1b2976211a756ca2639d`
  - 分支：`angelscript-master`
  - `Engine/Build/Build.version`：Unreal Engine `5.8.1`
  - 观察日期：2026‑08‑14
- EmmsUI：`c5d4e303f1fc8a1545de4d336be19e69dc8518c0`
  - 观察日期：2026‑08‑12

### 当前兼容性判断

旧包 0.1.0 基于尚未同步的 UE 5.5.4 镜像，因此把当前 EmmsUI 标记为存在明显日期/API 间隔。该判断现已失效。

当前 UE‑AS 基线包含 `1a06a2bf...` 引入的新 `Iterate()` 迭代协议；当前 EmmsUI 又包含 `c9985c1...` 对 ListView 的匹配实现。因此，**当前锁定组合的迭代协议在源码信号层面对齐**。

这不等于已经证明二进制或运行时兼容。仍应运行：

```powershell
python .agent/ueas-agent-kit/tools/probe_compatibility.py `
  --engine-root "D:\UE-Angelscript" `
  --emmsui-root "<Project>\Plugins\EmmsUI" `
  --project-root "<Project>" `
  --json-out "<Project>\Saved\ueas-compatibility.json"
```

然后完成目标 C++ build、最小 `UMMWidget`、ListView range-for、双向输入、Editor Tab 结构性热重载、simulate-cooked 与 Cook/Package smoke。

## 验证本包

```bash
python tools/validate_kit.py .
python -m unittest discover -s tests -v
```

验证内容包括：

- Skill frontmatter；
- Skill 名称唯一性；
- Markdown 相对链接；
- 代码围栏完整性；
- JSON 可解析；
- 来源锁和清单；
- 兼容性探针协议判断；
- UE‑AS 静态检查关键规则；
- SHA‑256 校验。

## 使用原则

- 项目源码和项目约定始终高于本包的通用建议。
- 不把普通 AngelScript 与 UE‑AS 定制语法混为一谈。
- 不把 UE‑AS 当作“复制到项目 Plugins 目录即可”的普通插件；它包含引擎源码修改。
- 不为“可能有用”而添加 `UPROPERTY` / `UFUNCTION`；只在反射边界需要时添加。
- Blueprint 可调用/事件函数的参数不要命名为 `Self`；当前编译器会将其视为 Unreal 反射保留名。
- 不把脚本热重载与 C++ Live Coding 混为一谈。
- 即使锁定组合源码信号对齐，也不跳过目标项目编译和运行时验证。
- 不把 `GetUnderlyingWidget()` 当成默认路径。
- 不把 UI 状态藏在每帧临时局部变量中，除非 helper 明确通过引用回写。
- 不以“编辑器能运行”代替 simulate-cooked、打包和多人模式验证。

## 研究边界

本环境完成了官方文档、官方公开仓库和用户可访问引擎镜像的源码级静态审阅，但没有在本机编译完整 Unreal 引擎，也没有运行目标项目的 PIE、Dedicated Server、Cook 或平台包。`RESEARCH_REPORT.md` 对已验证事实、源码对齐信号和待项目验证事项做了区分。
