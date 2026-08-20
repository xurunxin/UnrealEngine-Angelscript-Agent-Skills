# Changelog

## 0.1.1 — 2026‑08‑20

- 将用户可访问的 UE‑AS 快照更新到 `546c4d6a…` / Unreal Engine 5.8.1。
- 移除已失效的“UE 5.5.4 与 EmmsUI 相差约 15 个月”兼容性警告。
- 将当前组合状态改为“新 `Iterate()` 协议信号对齐、运行时未验证”。
- 记录 UE‑AS `1a06a2bf...` 与 EmmsUI `c9985c1...` 的对应 iterator 实现。
- 修复兼容性探针只扫描 `Source/`、从而漏掉 `ThirdParty` 协变模板标志的问题。
- 当双方协议均存在时报告 `compat.iterator_protocol_aligned`；单侧缺失时才警告。
- 新增当前对齐组合、历史已淘汰组合、旧引擎和反射参数 `Self` 的回归检查。
- 更新热重载、Editor-only、ListView、反射、发布与代码审查指导。
- 更新 Wiki、来源锁、研究报告、验证报告、Manifest 与 SHA‑256。

## 0.1.0 — 2026‑08‑20

- 初始发布。
- 14 个按需加载 Skills。
- 30+ Wiki/参考页面。
- UE‑AS 与 EmmsUI 原创示例。
- 兼容性探针、文档验证器、CI 模板。
- 锁定 UE‑AS 文档、EmmsUI 与当时可访问的引擎镜像 commit。
