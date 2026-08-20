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
