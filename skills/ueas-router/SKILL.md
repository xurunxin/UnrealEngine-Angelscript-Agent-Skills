---
name: ueas-router
description: Route UnrealEngine-Angelscript and EmmsUI tasks to the smallest relevant specialist skill after verifying exact engine and plugin versions.
---


# UE‑AS / EmmsUI Router

## 何时加载

任务涉及 `.as`、`Script/`、UnrealEngine‑Angelscript、`AngelscriptCode`、`BlueprintOverride`、`UMMWidget`、EmmsUI 或 `mm::` 时首先加载本 Skill。

## 第一关：版本与项目事实

在提出或修改代码前，读取：

1. `<Engine>/Engine/Build/Build.version`；
2. UE‑AS commit/branch，优先使用项目锁文件、子模块或构建记录；
3. `Plugins/EmmsUI/EmmsUI.uplugin` 及 EmmsUI commit；
4. `.uproject`、相关 `.uplugin`、`*.Build.cs`；
5. `Config/DefaultEngine.ini` 中 `AngelscriptSettings` 与 `AngelscriptTestSettings`；
6. 项目 `Script/` 的目录、命名、同类实现和测试。

没有精确版本时，不使用“当前 master 应该支持”作为结论。运行：

```bash
python tools/probe_compatibility.py --engine-root <engine> --project-root <project> --emmsui-root <emmsui>
```

## 任务路由

| 任务信号 | 加载 |
|---|---|
| 安装、源码构建、插件编译、版本升级、IDE | `../ueas-bootstrap/SKILL.md` |
| 语法、类/结构体、值/引用、命名空间、默认值 | `../ueas-core-scripting/SKILL.md` |
| Actor、Component、Subsystem、输入、Gameplay 结构 | `../ueas-gameplay/SKILL.md` |
| UPROPERTY/UFUNCTION、Blueprint、事件、委托、计时器、UMG | `../ueas-reflection-blueprint/SKILL.md` |
| Replicated、RPC、OnRep、多人模式 | `../ueas-networking/SKILL.md` |
| 测试、覆盖率、调试、异常、CI | `../ueas-testing-debugging/SKILL.md` |
| C++ API 在脚本不可见、自动绑定、Mixin、手工绑定 | `../ueas-cpp-bindings/SKILL.md` |
| Cook、Shipping、预编译缓存、转译、性能 | `../ueas-packaging-performance/SKILL.md` |
| Editor 菜单、资产工具、详情定制、Editor subsystem | `../ueas-editor-tools/SKILL.md` |
| UMMWidget、Overlay、WidgetComponent、运行时 mm:: UI | `../emmsui-runtime/SKILL.md` |
| EmmsUI Editor Tab、详情面板、弹窗、Context Menu | `../emmsui-editor-tools/SKILL.md` |
| 新增 EmmsUI helper、属性、事件或修改插件 C++ | `../emmsui-extension/SKILL.md` |
| 审查已有改动、风险或迁移 | `../ueas-review/SKILL.md` |

只加载完成任务所需的 Skill；不要把整个 Wiki 注入上下文。

## 全局不变量

- UE‑AS 是修改过的引擎 + 插件，不是普通项目插件。
- 项目代码与目标 commit 是事实源；网站示例只是起点。
- 普通脚本成员/函数优先，只有跨 UE 反射边界时才加宏。
- 结构性脚本修改与函数体修改的热重载风险不同。
- Editor-only 代码必须在编译边界隔离。
- 网络逻辑必须在真实 client/server 模式验证。
- EmmsUI Draw 必须成对、身份必须稳定、状态必须在模型中持有。
- 任何发布路径都必须经过 simulate-cooked 与目标配置验证。

## 输出契约

交付内容必须包含：

1. 读取到的版本与相关配置；
2. 采用的 Skill；
3. 设计边界与不采用的替代方案；
4. 修改文件；
5. 执行过的验证与实际结果；
6. 未验证风险，特别是热重载、Cook、网络和版本兼容性。
