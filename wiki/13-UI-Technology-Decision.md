# 13. UMG / EmmsUI / Slate / SlateIM / ImGui 选型

| 方案 | 优势 | 代价 | 首选场景 |
|---|---|---|---|
| UMG + Widget Blueprint | Designer、动画、资产化、成熟 | 保留式引用/绑定更繁琐 | 玩家 UI、设计师主导 |
| UMG + Script UUserWidget | 视觉与逻辑分离 | 仍需 Designer 资产 | 复杂视觉 + 文本逻辑 |
| EmmsUI | 代码直观、热重载、UMG 混合 | Draw/身份/状态规则需理解 | Editor 工具、Debug、代码型 UI |
| Slate C++ | 最强控制与性能 | C++ 迭代慢、代码多 | 核心 Editor/复杂控件 |
| SlateIM | Unreal 官方实验性 Slate 即时包装 | 官方定位偏 Debug，实验性 | 新版 UE 调试工具、C++ |
| Dear ImGui binding | 生态成熟、调试工具快 | 与 UMG/Editor Details 融合弱 | 独立 Debug/Profiler |

## EmmsUI 适合

- 一边改脚本一边看 UI；
- 表单、列表、筛选、按钮、状态面板；
- Editor Tab、详情定制；
- Viewport Overlay；
- 内部工具；
- UMG Widget 复用和混合。

## 不应默认使用 EmmsUI

- 大量时间轴动画；
- 复杂响应式视觉由美术维护；
- 完整无障碍/输入导航要求但未验证 helper；
- 需要成熟 Designer Preview；
- UI 不应每帧执行声明逻辑；
- 目标 UE‑AS 与 EmmsUI 版本未兼容。

## 混合架构

```text
Gameplay Model
    ↓
Presenter / ViewModel (UE-AS)
    ├── UMG production HUD
    └── EmmsUI debug/editor view
```

同一个 Model 支持两种 View，避免业务逻辑绑死 UI 技术。

## 决策问题

1. 谁维护视觉？
2. 是否需要动画？
3. 是否需要 Editor Details/Asset Widget？
4. UI 是否内部工具？
5. 状态复杂度？
6. 数据量与虚拟化？
7. 输入/焦点/手柄/无障碍？
8. Shipping 平台？
9. 目标版本支持度？
10. 是否能写自动化测试？
