# UE‑AS Specifier Cheat Sheet

目标版本可能改变默认值，先检查 `UAngelscriptSettings`.

## Property

| Specifier | 用途 |
|---|---|
| `UPROPERTY()` | 进入 Unreal 反射；默认权限由设置决定 |
| `EditAnywhere` | 实例与默认值可编辑 |
| `EditDefaultsOnly` | 仅类默认值 |
| `VisibleAnywhere` | 可见不可编辑 |
| `BlueprintReadOnly` | BP 只读 |
| `BlueprintReadWrite` | BP 读写 |
| `Category = "X"` | Details 分类 |
| `Replicated` | 属性复制 |
| `ReplicatedUsing = OnRep_X` | 复制通知 |
| `DefaultComponent` | 脚本默认组件 |
| `RootComponent` | 根组件 |
| `Attach = Parent` | 默认附着 |
| `AttachSocket = Name` | 默认 Socket |
| `BindWidget` | UMG Designer 控件绑定 |
| `EditCondition = "..."` | 编辑条件 |
| `ClampMin/ClampMax` | 元数据范围 |
| `NotEditable` / `EditConst` | 目标 UE‑AS 特定只读语义，核对版本 |

## Function

| Specifier | 用途 |
|---|---|
| `UFUNCTION()` | 进入反射，通常默认 BlueprintCallable |
| `NotBlueprintCallable` | 反射但不允许手工 BP 调用 |
| `BlueprintPure` | BP 纯函数 |
| `BlueprintOverride` | 覆盖 C++ BP event |
| `BlueprintEvent` | 允许 BP 子类覆盖 |
| `CallInEditor` | Editor 按钮/菜单 |
| `Server` | Server RPC |
| `Client` | Client RPC |
| `NetMulticast` | Multicast RPC |
| `Reliable` | 可靠 RPC |
| `Unreliable` | 不可靠 RPC |
| `BlueprintAuthorityOnly` | 权威限制标记 |
| `Category = "X"` | BP 分类 |

## C++ Binding Metadata

| Metadata/Specifier | 用途 |
|---|---|
| `NotInAngelscript` | UCLASS 不自动绑定 |
| `NoAutoAngelscriptBind` | USTRUCT 等禁用自动绑定 |
| `ScriptCallable` | 脚本 callable |
| `ScriptReadOnly` | 脚本只读 |
| `ScriptReadWrite` | 脚本读写 |
| `ScriptMixin = "Type"` | Mixin library |
| `ScriptName = "Name"` | 脚本名称 |

## 条件编译

| Flag | 含义 |
|---|---|
| `EDITOR` | Editor build |
| `EDITORONLY_DATA` | Editor-only data |
| `TEST` | Debug/Development/Test |
| `RELEASE` | Test/Shipping 等发布配置，核对目标版本 |
