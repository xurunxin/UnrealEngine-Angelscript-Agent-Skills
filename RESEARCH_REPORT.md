# 研究报告与结论

## 1. 最重要的系统判断

### UE‑AS 不是一个普通项目插件

UnrealEngine‑Angelscript 同时包含 Unreal 引擎源码修改与 `Angelscript` 插件。正确起点是拥有 Epic GitHub 源码权限、固定一个 UE‑AS 引擎 commit、从源码构建 Editor，再在项目根目录使用自动创建的 `Script/` 文件夹。仅把某个插件目录复制到 `Project/Plugins` 不是完整安装方式。

### UE‑AS 的价值是“文本化 Gameplay + UE 反射互操作 + 快速迭代”

它并不是让所有 C++ 消失。合理边界通常是：

- C++：底层引擎扩展、性能关键算法、第三方库、平台能力、复杂绑定；
- UE‑AS：Gameplay 编排、Actor/Component/Subsystem、工具逻辑、易变业务规则；
- Blueprint：关卡/资产装配、设计师可视化配置、动画和局部表现；
- EmmsUI：代码驱动、频繁迭代的工具 UI、调试 UI、简单运行时 UI；
- UMG/Slate：复杂视觉设计、动画、无障碍、成熟资产工作流或需要完整保留式控制的界面。

### EmmsUI 不是“每帧重建全部 UMG”

EmmsUI 每次 Draw 重新声明 UI，但内部通过 Widget 类型、父元素和标识哈希寻找并复用 `UWidget`。它保存 Active/Pending 子树、属性状态和事件监听器，只更新变化，并在属性本帧不再声明时恢复默认值。它是一个 **即时式 API + 保留式 UMG 后端**。

这意味着即时式 UI 的优点成立——控制流直观、状态与界面靠近、热重载快速——但仍要尊重 UMG 的对象生命周期、布局、焦点、事件和属性重建成本。

## 2. 版本状态（0.1.1 修订）

| 组件 | 本次观察快照 | 状态 |
|---|---|---|
| UE‑AS 文档 | 2026‑03‑23 / `3864c72…` | 文档基线 |
| UE‑AS 引擎 | 2026‑08‑14 / `546c4d6…` / UE 5.8.1 | 用户当前同步基线 |
| EmmsUI | 2026‑08‑12 / `c5d4e303…` | 当前观察主分支 |

0.1.0 曾根据旧的 UE 5.5.4 镜像推断“当前 EmmsUI 与引擎存在显著日期/API 间隔”。用户同步上游后，该推断已不再成立。

当前 UE‑AS head 已包含 `1a06a2bf...` 的新 `Iterate()` 迭代协议、range-for 解析与 StaticJIT 支持；当前 EmmsUI head 已包含 `c9985c1...` 的 ListView 匹配绑定。因此：

- **可确认：**双方在新 ListView 迭代协议的源码信号上对齐；
- **不可据此确认：**完整 C++ ABI、全部手工绑定、目标项目插件组合、运行时输入状态、热重载和 Cook 一定通过。

正确结论从“已知版本间隔警告”改为：**源码协议对齐，运行时仍需目标项目证据。**

## 3. 同步后值得 Agent 注意的变化

### 新迭代协议成为当前基线

UE‑AS 新协议由 iterator 的 `Iterate()` 返回当前元素或空值结束，取代旧的 range-for 预处理改写路径，并加入 TArray/TMap/TSet 等原生容器及 StaticJIT 支持。EmmsUI ListView iterator 使用 `if_handle_then_const Iterate() const` 对接同一协议。

Agent 处理当前锁定组合时，不应再建议“先降级 EmmsUI 以避开新 iterator”作为默认动作；应先运行兼容性探针和最小 ListView 编译。只有单侧协议信号缺失或真实编译失败时，才讨论固定旧 commit 或回移补丁。

### 热重载基线更新

当前 UE‑AS head 修复了 soft hot reload 可能重复生成默认析构函数的问题；当前 EmmsUI head处理了打开中的 `UMMEditorUtilityTab` 对象重实例化。二者降低了已知风险，但不能替代结构性热重载矩阵：字段、继承、UFUNCTION/UPROPERTY、Tab、Delegate 与焦点状态仍需分别验证。

### Editor-only 类型更完整

当前 UE‑AS 已让 Editor 目录中的脚本 class/struct 在生成的 UASClass/UASStruct 上体现 Editor-only 状态。这改善了带 Editor-only 函数的 Blueprint 编译边界。项目仍必须运行 `-as-simulate-cooked`，因为运行时脚本签名泄漏 Editor 类型、资产引用或插件模块依赖仍可能失败。

### 反射保留名更早失败

当前编译器会拒绝 BlueprintCallable/BlueprintEvent 参数名 `Self`。这是正确的早期错误，不应通过规避编译器或修改生成代码绕过；应重命名参数，例如 `Target`、`Object` 或领域名称。

## 4. 源码确认的最佳实践

### 反射最小化

普通脚本成员和普通脚本函数不需要 `UPROPERTY` / `UFUNCTION`。只有需要编辑器、Blueprint、序列化、复制、动态委托、计时器或 UE 反射查找时才增加。这样可以降低结构性热重载和 API 面积。

### 默认值放在类体与 `default` 语句

UE‑AS 为热重载做了专门语义：字段初始化和 `default` 语句优于模拟 C++ 构造函数。Actor/Component 要通过 `DefaultComponent`、`RootComponent`、`Attach` 等声明式方式搭建默认组件。

### Blueprint Hook 分层

不要让核心行为完全依赖 Blueprint 子类记得调用父实现。推荐：

```angelscript
void ExecuteAction()
{
    // 必须执行的脚本逻辑
    ...

    BP_OnActionExecuted();
}

UFUNCTION(BlueprintEvent, NotBlueprintCallable)
void BP_OnActionExecuted()
{
}
```

Blueprint 只覆盖表现 Hook，不能跳过核心不变量。

### Editor-only 必须在编译边界隔离

使用 `#if EDITOR`，或把完整脚本放进名为 `Editor` 的目录。`Examples` 与 `Dev` 目录同样会在 cooked 编译中被忽略。即使当前 UASClass/UASStruct 已正确标记 Editor-only，CI 仍必须运行 `-as-simulate-cooked -run=AngelscriptTest`。

### 网络默认可靠不是免费的

UE‑AS RPC 默认 Reliable。高频、可丢失的状态更新应明确 `Unreliable`，持久状态由复制属性负责。所有 RPC/OnRep 都应在专用服务器 + 客户端集成测试中验证，而不是只在 Standalone PIE 验证。

### EmmsUI 绘制顺序也是身份的一部分

公开 API 的普通子节点默认哈希为 0，内部身份主要由 Widget 类型、父元素和同类节点出现顺序决定。条件分支中插入、删除或重排同类型兄弟节点，可能使输入焦点、选择或内部状态“移动”到另一个逻辑节点。这是源码推断，应通过项目版本验证。

对策：

- 保持同类兄弟的结构和顺序稳定；
- 把动态分支放入不同的父 Panel；
- 列表使用 ListView/TreeView 虚拟化，不手工生成大量同类输入控件；
- 持久业务状态放在脚本对象/模型，不依赖 Widget 内部状态；
- 新增显式 ID 能力前先审查当前 EmmsUI 是否已在目标 commit 支持。

### `Was...` 与 `On...` 有不同语义

- `WasClicked()` / `WasTextChanged(...)`：面向 Draw 周期的边沿消费；适合“本次 Draw 执行一次动作”。
- `OnClicked(this, n"Handler")`：即时委托；适合每次事件都必须到达、需要参数或回复的场景。

事件监听源码只保存最近一组参数供 `Was...` 读取；同一 Draw 前发生多次时不应把它当完整事件队列。

### 双向输入状态必须由模型持有

`EditableTextBox(FString& Value)`、`Slider(double& Value)` 等通过引用在 UI 变化时回写模型。传入每帧重新创建的空局部变量会丢状态；应使用类成员、ViewModel 或持久集合。当前锁定 EmmsUI 已包含 mutable state 修复，但项目仍需覆盖“用户输入与程序值同帧变化”的测试。

## 5. 社区与生态补充

- 官方 VS Code 扩展仍是能力最完整、与 Editor 连接最紧密的路径：保存时编译/热重载、错误诊断、LSP、断点和异常暂停。
- 社区 Rider 插件把官方语言服务器接入 Rider，可作为非官方替代，但应以目标项目测试为准。
- UE 自身提供实验性的 SlateIM，定位偏调试工具。它与 EmmsUI 不同：SlateIM 是 Slate 的即时式包装；EmmsUI 面向 UE‑AS，并以 UMG 为后端，更适合 UMG 属性、Widget Blueprint 混合和脚本热重载。
- 社区还存在 AngelscriptImGui 等方案。Dear ImGui 路线适合独立调试面板和跨引擎工具；EmmsUI 更适合需要 Unreal 原生 Widget、编辑器详情面板或 UMG 混合的场景。

社区结论只作为选型信号，不覆盖官方源码行为。

## 6. 尚未在本环境执行的验证

- 当前 UE‑AS 5.8.1 引擎全量构建；
- EmmsUI `c5d4e303...` 与 UE‑AS `546c4d6...` 的真实 C++ 编译；
- 目标项目 AngelScript 编译与 VS Code 调试连接；
- PIE 中结构性/非结构性热重载矩阵；
- ListView/TreeView 新协议运行时行为；
- mutable input state 冲突场景；
- Dedicated Server 集成测试；
- Cook/Package 与 `PrecompiledScript.Cache`；
- 各平台性能和内存分析。

本包提供脚本、探针和检查清单，要求在目标项目中补齐这些证据。
