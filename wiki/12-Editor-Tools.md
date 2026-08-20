# 12. 编辑器工具

## Editor-only 保护

```angelscript
#if EDITOR
class UMyAssetMenu : UScriptAssetMenuExtension
{
}
#endif
```

或完整文件放 `Editor/`。

当前 UE‑AS 基线会把 Editor-only 模块中的脚本 class/struct 反映为 Editor-only UASClass/UASStruct，这改善了带 Editor-only 函数的 Blueprint 编译。但它不替代边界设计：运行时类型的字段、参数、返回值、资产或模块依赖仍不能泄漏 Editor-only 类型。

## Actor Menu

支持类列表，`CallInEditor` 函数成为菜单项。带 Actor 参数时可对选中 Actor 逐个调用；其他参数可触发输入对话框。

## Asset Menu

使用 `FAssetData`，避免无必要加载。确需修改：

1. TryLoad；
2. `Modify()`；
3. 修改；
4. 标记 Dirty；
5. 由用户/显式流程保存。

## Editor Menu / Toolbar

`ExtensionPoint` 对应 `UToolMenus::ExtendMenu` 的标识。Category 可形成子菜单，Meta 指定 Icon/ButtonStyle。扩展点会随 UE 版本改变，目标引擎验证。

## Transaction

批量编辑必须支持 Undo：

- Begin transaction（项目 API）；
- 每个对象 Modify；
- 修改；
- End transaction；
- 异常时安全结束。

## Progress 与取消

长任务：

- 先收集计划；
- 显示数量/影响；
- 用户确认；
- 分批执行；
- 检查取消；
- 输出成功/跳过/失败；
- 不在 Draw 中每帧重复调用。

## Editor Subsystem

用于全局工具状态、监听 Editor Delegate、跨 Tab 协调。必须在 Deinitialize 解绑。

## UMG 与 EmmsUI

- UMG：复杂设计、动画、Designer；
- EmmsUI：代码工具、快速重载；
- 可混合：EmmsUI 内嵌 UDetailsView/自定义 UWidget，或 UMG 外壳调用脚本逻辑。

当前 EmmsUI 已包含 Editor Tab object reinstancing 修复。仍要测试：打开 Tab、结构性脚本修改、对象替换、关闭/重开、重复菜单和退出 Editor。

## Cook Gate

任何 Editor 工具提交都必须运行 simulate-cooked，确保运行时脚本不依赖其类型：

```powershell
UnrealEditor-Cmd.exe Project.uproject `
  -unattended -as-simulate-cooked -run=AngelscriptTest
```

Editor-only 标记正确不代表运行时签名、资产引用和插件 module dependency 一定安全。
