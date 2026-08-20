---
name: ueas-bootstrap
description: Set up, pin, upgrade, and diagnose a source-built UnrealEngine-Angelscript environment, project Script workspace, IDE integration, and EmmsUI plugin compatibility.
---


# UE‑AS Bootstrap

## 适用范围

安装、构建、升级、分支固定、项目首次接入、VS Code/Rider 语言服务、EmmsUI 插件编译问题。

## 必须先确认

- Epic Games GitHub 源码访问权限；
- 目标平台与 Unreal 版本；
- UE‑AS 精确 commit，不使用浮动 `master` 作为生产依赖；
- 项目是否含二进制-only 插件；源码引擎通常要求插件与目标引擎重新编译；
- EmmsUI 精确 commit 与它所需的 UE‑AS 语言/绑定能力。

参阅 [`../../wiki/02-Install-and-Version-Pinning.md`](../../wiki/02-Install-and-Version-Pinning.md) 与 [`../../wiki/31-Version-Compatibility.md`](../../wiki/31-Version-Compatibility.md)。

## 推荐工作流

1. 从受授权的 UE‑AS 引擎仓库创建团队 fork。
2. 以不可变 commit/tag 建立引擎基线。
3. 运行 Unreal 的依赖安装与项目文件生成流程。
4. 构建目标 Editor。
5. 用该 Editor 打开项目，确认项目根目录生成 `Script/`。
6. VS Code 直接把 `Script/` 作为工作区根目录；确认 Editor 正在运行并建立语言服务器连接。
7. 以子模块、固定 SHA 或 vendored 源码接入 EmmsUI。
8. 运行兼容性探针和最小编译。当前锁定的 UE‑AS 5.8.1 与 EmmsUI 在新 `Iterate()` 协议源码信号上对齐，但仍必须验证：
   - 一个 Actor；
   - 一个 `UMMWidget`；
   - 一个 ListView 可见项迭代；
   - 一个 Editor Tab 热重载；
   - simulate-cooked。

## 升级策略

升级必须拆成两步：

1. 先升级 UE/UE‑AS，保持项目与 EmmsUI 不变；
2. 再升级 EmmsUI，并单独验证脚本 API 与编辑器热重载。

不要同时升级引擎、UE‑AS、EmmsUI、项目 Gameplay 和第三方插件。

建议维护：

```text
Config/Toolchain.lock.json
EngineAssociation.md
Build/ueas-version.txt
Plugins/EmmsUI/.upstream-commit
```

## IDE

官方 VS Code 扩展依赖运行中的 Editor 提供完整诊断、补全和调试。离线时部分能力不可用。Rider 社区插件可以复用官方语言服务器，但属于非官方集成，必须在目标版本验证。

## 常见误区

- **错误：**把 `Engine/Plugins/Angelscript` 复制到普通 Epic Launcher 引擎。
  **原因：**UE‑AS 还修改引擎源码。
- **错误：**使用预编译 Marketplace 插件并假设 ABI 一致。
  **处理：**获取源码并针对目标引擎构建。
- **错误：**只记录 UE 版本，不记录 UE‑AS commit。
  **处理：**两者都固定。
- **错误：**EmmsUI 编译通过就认为运行时兼容。
  **处理：**再验证输入、ListView 迭代、Editor Tab 重实例化和 Cook。

## 完成标准

- Editor 能启动；
- `Script/` 自动加载；
- 保存 `.as` 能收到 Editor 诊断；
- 断点可连接；
- 最小脚本 Actor 与 EmmsUI UI 可运行；
- simulate-cooked 通过；
- 锁文件记录全部 commit；
- 团队机器可重复构建。
