# 33. 社区与生态

## 官方生态

- UE‑AS 文档与 API Reference；
- VS Code Language Server / Debug Adapter；
- Formatter；
- EmmsUI；
- Discord；
- 多个已发布游戏作为生产采用信号。

官方明确说明项目虽在 Hazelight 大规模生产使用，但不承诺支持，商业项目应具备能维护自定义引擎的程序员。

## IDE

### VS Code

官方首选。与运行中 Editor 连接，提供：

- Completion；
- Diagnostics；
- Rename/References；
- Semantic Highlight；
- Debug；
- Exception break；
- Unreal source navigation。

### Rider

社区插件把官方 LSP 接入 Rider。可用性和调试体验随版本变化，不应替代官方路径作为唯一故障排查基线。

## 社区插件

- EmmsUI forks；
- AngelscriptImGui；
- Gameplay/Capability systems；
- Script skill packs；
- 自定义 bindings。

评估时检查：

- 最近 commit；
- 目标 UE‑AS SHA；
- License；
- Cook；
- Runtime/Editor modules；
- 测试；
- 是否错误宣称“普通插件安装”。

## 社区经验的正确使用

社区内容适合发现：

- 实际项目模式；
- 缺失教程；
- IDE 选择；
- 升级坑；
- 可复用架构。

不适合决定：

- 当前 API 名；
- ABI；
- binding flags；
- Shipping 支持；
- 平台许可。

这些以目标源码和官方文档为准。

## 持续跟踪建议

每次升级前查看：

- UE‑AS engine commits；
- Docs commits；
- EmmsUI recent commits；
- VS Code extension commits；
- 项目 fork divergence；
- Epic 对 Slate/UMG/SlateIM 的变化。

把重要上游修复记录成项目 Issue，而不是靠成员记忆。


## Agent Skills 与 skills.sh（0.2.0 调研）

本次检索未发现另一套同时深入覆盖 UE-AS 与 EmmsUI 的公开 Skill 套件，但通用 Unreal Skill 已较丰富：

- Epic 的 Unreal Agent Skills 强调 Skill 新颖性、耐久性、工具无关性和上下文经济；
- quodsoler 以 `.agents/ue-project-context.md` 作为跨 Skill 项目事实；
- kevinpbuckley 用精确 UE 版本、源码路径和 golden tasks 控制漂移；
- DSTN2000 强调零假设项目发现；
- gamedev-skills 使用 Router 和 `agents/openai.yaml`；
- skills.sh 提供标准安装与发现入口。

本仓库吸收这些工作流，但不复制通用 Niagara、Animation、Audio、Mass、GAS 或普通 C++ 内容。UE-AS/EmmsUI 特有语义由本仓库负责，普通 Unreal 领域交给更专业的通用 Skill。

详见 [生态比对报告](../docs/ECOSYSTEM-COMPARISON-2026-08-20.md)。
