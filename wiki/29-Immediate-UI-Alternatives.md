# 29. SlateIM、ImGui 与其他即时式 UI

## EmmsUI

- 语言：UE‑AS（核心体验）；
- 后端：UMG/UWidget；
- 优势：反射属性自动暴露、Widget Blueprint 混合、Editor Details、脚本热重载；
- 风险：版本绑定、身份顺序、UMG rebuild/layout。

## SlateIM

Epic 官方实验性插件，是 Slate 的即时式 wrapper，官方定位为 Debugging tools。新版 UE 提供 Runtime/Engine/InGame/Blueprint 等模块，但仍标记 Experimental。适合 C++/Slate 生态，不替代 EmmsUI 的 UE‑AS + UMG 目标。

## Dear ImGui / AngelscriptImGui

- 独立即时式生态；
- Debugger/Profiler 控件丰富；
- 后端和输入接入清晰；
- 与 Unreal UMG、Details、Widget Blueprint 的自然融合较弱。

适合不要求原生 UWidget 资产/布局的内部面板。

## UMG

保留式；最适合 Designer、美术资产、动画和玩家 UI。脚本 Presenter 可以与 UMG View 配合。

## 选择建议

| 场景 | 推荐 |
|---|---|
| UE‑AS Editor Tool | EmmsUI |
| UE‑AS Runtime debug overlay | EmmsUI |
| C++ 新版 UE debug tool | SlateIM 候选 |
| 跨项目 profiler/debug | ImGui |
| 玩家 HUD/菜单，视觉复杂 | UMG |
| 核心 Editor 定制控件 | Slate C++ |

## 不要把“即时式”当性能结论

即时/保留描述的是 API 和状态组织，不直接决定快慢。EmmsUI 本身保留 UWidget；性能要看实际 Draw、更新、布局、Paint 和数据工作。
