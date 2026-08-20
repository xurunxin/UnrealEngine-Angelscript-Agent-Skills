# 01. 系统模型

## 组件关系

```text
Epic Unreal Engine source
        │
        ├── UE-AS engine modifications
        │
        └── Engine/Plugins/Angelscript
              ├── AngelscriptCode   Runtime
              ├── AngelscriptEditor Editor
              └── AngelscriptLoader Runtime
                         │
<Project>/Script/*.as ───┘
                         │
                  C++ Reflection / Bind Database
                         │
              Blueprint / UMG / Gameplay API
                         │
                     EmmsUI plugin
              ├── EmmsUI       Runtime
              └── EmmsUIEditor Editor
```

UE‑AS 不是“另一个独立脚本虚拟机套在 Unreal 外面”。它直接扫描 Unreal 反射数据，把可用的 UCLASS/USTRUCT/UPROPERTY/UFUNCTION 映射到脚本，并修改引擎以支持脚本类型、重实例化、调试、预编译和可选转译。

## 编程模型

### C++

负责：

- 引擎和插件；
- 平台与第三方库；
- 性能关键数据结构；
- 反射无法表达的绑定；
- Shipping 级底层能力。

### UE‑AS

负责：

- Gameplay 规则；
- Actor/Component/Subsystem；
- 状态机与任务编排；
- Editor 工具；
- 快速变化的 UI/工具逻辑；
- 需要文本合并和快速热重载的行为。

### Blueprint

负责：

- 资产与关卡装配；
- 设计师参数；
- 动画/表现；
- 小型可视化 Hook；
- 脚本基类的内容派生。

### EmmsUI

负责：

- 代码驱动的工具 UI；
- Debug Overlay；
- Editor Tab/Details；
- 低到中等视觉复杂度的运行时界面；
- 需要脚本热重载的 UI。

## 反射边界

普通脚本代码只存在于脚本 VM/类型系统。加上 UPROPERTY/UFUNCTION 后，成员进入 Unreal 反射系统，可被 Editor、Blueprint、Replication、Delegate、Timer、Serialization 等系统观察。

边界越大，能力越强，同时：

- 类型布局更稳定地被资产引用；
- 结构性修改更重；
- 命名和兼容性成本更高；
- API 更容易被其他系统依赖。

默认策略是最小反射面。

## Hot Reload 与 Reinstancing

函数体变化通常可以在 PIE 中热重载。字段、类型继承、反射签名、默认组件等结构性变化可能需要类型重实例化。已有对象、Blueprint 子类、Editor Tab、Delegate 和 UI 状态都可能受影响。

因此“保存即可看到变化”不等于“任何改动都无状态迁移风险”。

## EmmsUI 的双层模型

Draw 代码是即时式：

```angelscript
if (mm::Button("Save"))
    Save();
```

底层是被保留的 UMG：

- 已存在 UWidget 尽量复用；
- 属性有 Default/Current/Pending/Mirrored 状态；
- 子树有 Active/Pending；
- 事件通过 Listener 拦截；
- 层级只在变化处更新。

正确理解这两层，是避免焦点错位、状态丢失和性能误判的前提。
