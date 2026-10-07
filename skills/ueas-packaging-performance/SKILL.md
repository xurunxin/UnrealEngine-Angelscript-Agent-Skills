---
name: ueas-packaging-performance
description: Use when profiling UE-AS or preparing cooked builds, script caches and JIT. Do not use for ordinary editor iteration or storefront publishing.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# UE‑AS Packaging and Performance

## 三种不同工作流

不要混淆：

1. **开发态脚本加载与热重载**：读取 `.as`；
2. **预编译脚本缓存**：启动时加载 `PrecompiledScript.Cache`，通常不再加载脚本文件；
3. **转译/JIT C++ 代码**：把热点脚本进一步接近原生性能。

每种工作流有不同产物和失效条件。

## simulate-cooked

在任何正式 Cook 前先运行：

```bash
UnrealEditor-Cmd.exe Project.uproject -unattended -as-simulate-cooked -run=AngelscriptTest
```

它会移除 Editor-only 绑定并编译掉 `#if EDITOR`，用于发现脚本依赖泄漏。

## 预编译缓存

官方工作流使用目标可执行文件生成 `Script/PrecompiledScript.Cache` 与可能的 `AS_JITTED_CODE/`。关键约束：

- 缓存必须由与运行时匹配的可执行文件生成；
- C++ 二进制或绑定改变后必须重新生成；
- 使用缓存时通常禁用脚本文件加载与热重载；
- 开发调试可用 `-as-development-mode` 绕过缓存；
- 生成代码需要正确的 `AngelscriptCode` 模块依赖。

不要把某台开发机缓存长期提交后跨版本复用。当前 5.8.1 同步包含多项 StaticJIT/转译优化，但上游 commit 不是项目性能证据；必须在目标配置重新 Profile，并记录解释、缓存或转译模式。

## 性能策略

先 Profile，再决定：

- 减少 Tick；
- 缓存稳定查找；
- 避免每帧容器分配与字符串构造；
- 使用 `n""`；
- 对日志使用 Development-only 条件且不把副作用放进参数；
- 大规模数值循环、复杂算法或平台 API 下沉 C++；
- 高热点脚本评估转译/JIT，而不是提前改写全部 Gameplay。

## EmmsUI 性能

- EmmsUI 会复用 UWidget，但 Draw 代码仍每帧执行；
- 不在 Draw 中扫描全世界、同步加载资产或构造巨大模型；
- ListView/TreeView 只绘制可见项；
- 不每帧设置会触发 Widget 重建的只读/构造属性；
- 保持层级稳定，避免后部子树因顺序变化被重新挂接；
- 异步加载结果进入持久模型；
- Profile Slate/UMG invalidation、Draw 时间、UObject 分配与 GC。

## 发布门

- Unit/Integration Tests；
- simulate-cooked；
- 目标配置 C++ 编译；
- Cook；
- Package 启动；
- 无 `.as` 依赖时验证缓存加载；
- 网络项目做 Dedicated Server smoke；
- 平台证书/插件检查；
- 记录缓存生成 executable hash。

## 完成标准

不只给“优化建议”；要给 Profile 证据、目标指标和发布产物的可重复生成步骤。
