# Source Map

本表记录本包结论的主要上游依据。外部源码未被复制进本包；用户私有 Unreal Engine fork 只记录路径、版本和 commit。

## UE‑AS 官方文档

Repository: `Hazelight/Docs-UnrealEngine-Angelscript`  
Commit: `3864c72fa3c1ef67413dfaad24417bad01879b4d`

| Path | 主题 |
|---|---|
| `content/getting-started/installation.md` | 源码引擎安装 |
| `content/getting-started/introduction.md` | Script 根、首个 Actor |
| `content/scripting/actors-components.md` | Actor/默认组件 |
| `content/scripting/cpp-differences.md` | UObject、float、默认值 |
| `content/scripting/functions-and-events.md` | UFUNCTION/BP events |
| `content/scripting/properties-and-accessors.md` | UPROPERTY/accessor |
| `content/scripting/delegates.md` | delegate/event |
| `content/scripting/networking-features.md` | RPC/复制 |
| `content/scripting/editor-script.md` | Editor-only/simulate-cooked |
| `content/scripting/script-tests.md` | Unit/Integration/Coverage |
| `content/scripting/subsystems.md` | Subsystem |
| `content/cpp-bindings/automatic-bindings.md` | 反射自动绑定 |
| `content/cpp-bindings/mixin-libraries.md` | C++ ScriptMixin |
| `content/cpp-bindings/precompiled-data.md` | 缓存/JIT |
| `content/project/development-status.md` | 生产状态/限制 |
| `content/project/license.md` | 许可 |

## UE‑AS 引擎观察快照

Repository: `xurunxin/UnrealEngine-Angelscript`（私有访问快照）  
Branch: `angelscript-master`  
Commit: `546c4d6af141f1e820be1b2976211a756ca2639d`  
Engine: 5.8.1  
Observed commit date: 2026‑08‑14

| Path / Commit | 主题 |
|---|---|
| `Engine/Build/Build.version` | UE 5.8.1 版本事实 |
| `Engine/Plugins/Angelscript/Angelscript.uplugin` | Runtime/Editor/Loader 模块入口 |
| `Engine/Plugins/Angelscript/Source/**` | UE 反射、预处理、绑定、StaticJIT |
| `Engine/Plugins/Angelscript/ThirdParty/include/angelscript.h` | UE‑AS 定制 AngelScript 类型/模板标志 |
| `1a06a2bf...` | 新 `Iterate()` 迭代协议与 range-for/JIT 支持 |
| `f459e632...` | Editor 目录脚本生成的 UASClass/UASStruct 标记 Editor-only |
| `94f7023b...` | Blueprint 可调用/事件参数名 `Self` 的编译错误 |
| `546c4d6a...` | soft hot reload 重复默认析构函数修复 |

旧观察快照 `7a77e74...` / UE 5.5.4 仅保留在兼容性历史记录中，不再作为当前项目基线。

## EmmsUI

Repository: `Hazelight/EmmsUI`  
Commit: `c5d4e303f1fc8a1545de4d336be19e69dc8518c0`  
Observed commit date: 2026‑08‑12

| Path / Commit | 主题 |
|---|---|
| `README.md` | 使用方式 |
| `EmmsUI.uplugin` | Runtime/Editor modules |
| `Source/EmmsUI/Public/EmmsWidgetElement.h` | 身份/Element |
| `.../EmmsWidgetHandle.h` | `mm<T>` handle |
| `.../EmmsAttribute.h/.cpp` | 属性状态/差分 |
| `.../MMWidget.h/.cpp` | Draw、复用、层级 |
| `.../EmmsStatics.h/.cpp` | 隐式栈、Begin/End、events |
| `.../EmmsEventListener.h/.cpp` | Was/On 事件语义 |
| `.../EmmsScriptBinds.cpp` | 自动属性/事件绑定 |
| `.../EmmsWidgetHelpers.*` | helper 与输入状态 |
| `Script-Examples/*.as` | Tab/List/Tree/Details/Overlay |
| `32ae41d...` | mutable input state |
| `c9985c1...` | 与 UE‑AS 新 `Iterate()` 协议匹配的 ListView iterator |
| `c5d4e30...` | Editor Tab object reinstancing/hot reload |

## 当前组合的证据边界

UE‑AS `1a06a2bf...` 与 EmmsUI `c9985c1...` 在源码层面对同一新迭代协议作了对应修改，且都包含在上述锁定 head 中。因此 0.1.0 的“旧引擎缺少新协议”警告不再适用于当前快照。

这仍不是二进制和运行时兼容性证明。目标项目必须补齐 C++ build、脚本编译、ListView、输入状态、Editor Tab 热重载、simulate-cooked 与 Cook 证据。

## 社区/生态

- `Hazelight/vscode-unreal-angelscript`：官方 LSP/Debug。
- `scriptacus/rider-unreal-angelscript`：社区 Rider 集成。
- Epic SlateIM API：官方实验性即时式 Slate。
- `EnvarStudio/AngelscriptImGui`：社区 ImGui 绑定信号。

社区来源只支持生态/选型判断，不用于覆盖源码 API。
