# 00. 项目上下文与证据发现

## 为什么需要项目上下文

UE-AS 项目的答案高度依赖实际源码引擎、插件 ref、模块、Script roots 和发布方式。只知道
“项目使用 Unreal 5.8”并不足以判断：

- 实际 Engine checkout 是否包含当前 UE-AS 修改；
- 项目使用的是 Engine 插件还是 Project 插件；
- EmmsUI 是否被固定到与引擎对应的 commit；
- 哪些 `.as` 目录进入 Cook；
- C++ Binding 位于 Runtime 还是 Editor 模块；
- Dedicated Server、Static JIT 或 Precompiled Script 是否属于交付范围。

因此首次接手项目、同步上游或改变插件后，应创建或刷新：

```text
.agents/ueas-project-context.md
```

由 [`ueas-project-context`](../skills/ueas-project-context/SKILL.md) 负责生成。

## 零假设发现

1. 先确认唯一 `.uproject`；多个候选时停止自动选择。
2. 从 `Engine/Build/Build.version` 读取版本，不只看目录名。
3. 从实际 Engine checkout 获取 UE-AS ref，不用文档或上游 latest 代替。
4. 在 Project 与 Engine 两处检查 EmmsUI，报告重复副本。
5. 从 `.uproject`、`.uplugin`、`Build.cs`、`Target.cs` 和 Config 识别模块与 Gate。
6. 只把执行过的 Build、Script Compile、PIE、Cook、Package 标为通过。

## 兼容性状态梯度

```text
not-checked
→ source-signals-aligned
→ build-passed
→ script-compile-passed
→ runtime-smoke-passed
→ cook-passed
→ package-launch-passed
```

不能从任意前一级跳到后一级。两个仓库存在相同的 `Iterate()` 或
`if_handle_then_const` 只说明选择对应 smoke test 的依据，不证明二进制和运行兼容。

## 上下文应保持小

记录会改变实现与验收的事实，不复制完整文件树。每个可变事实包含来源、观察日期和状态；
未知内容写 `unknown`，不要补全成看似合理的项目约定。

## 刷新时机

- Engine、UE-AS、EmmsUI ref 或 dirty state 改变；
- `.uproject`、插件、模块、Target 或 Script roots 改变；
- 新增 C++ Binding；
- 网络拓扑、目标平台或发布方式改变；
- 现有证据路径失效；
- 用户指出仓库已同步或版本已更新。
