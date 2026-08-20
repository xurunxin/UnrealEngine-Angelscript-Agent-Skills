---
name: ueas-core-scripting
description: Write idiomatic UnrealEngine-Angelscript classes, structs, functions, values, references, namespaces, defaults, literals, and hot-reload-friendly code.
---


# UE‑AS Core Scripting

## 使用前

先检查项目同类 `.as` 文件、`UAngelscriptSettings` 配置和目标 commit。UE‑AS 是定制语言，普通 AngelScript 手册不能覆盖 Unreal 绑定语义。

## 语言模型

- `class` 通常是 UObject 派生的引用类型；
- `struct` 是值类型；
- UObject 变量不写 `*`，成员访问不写 `->`；
- `float` 在默认配置中解析为 64 位；需要明确精度时用 `float32` / `float64`；
- `n"Name"` 是编译期 `FName` 字面量；
- `f"{Value}"` 用于格式字符串；
- `TArray`、`TMap`、`TSet` 使用 Unreal 容器绑定；
- 全局可复用 API 放在命名空间中，避免依赖跨文件无命名空间全局函数。

详见 [`../../wiki/04-Language-Cheatsheet.md`](../../wiki/04-Language-Cheatsheet.md)。

## 热重载友好写法

- 字段默认值写在声明处；
- 父类默认属性用 `default` 语句；
- 默认组件用 `UPROPERTY(DefaultComponent, ...)`；
- 不模拟复杂 C++ 构造函数；
- 函数体逻辑与反射签名改动分开提交；
- 不在 `Print()`、`check()` 等 Development-only 表达式中放副作用；
- 使用稳定类型名和字段名，重命名前评估资产/Blueprint/序列化引用。

## 引用与输出

结构体需要原地修改时使用引用：

```angelscript
void ClampHealth(FHealthState& State)
{
    State.Current = Math::Clamp(State.Current, 0.0, State.Maximum);
}
```

需要 UE/Blueprint 风格输出时使用 `&out`。不要为了避免复制随意给所有参数加引用；UE‑AS 对结构体参数有自己的优化和调用约定。

## 代码组织

推荐：

```text
Script/
  Game/
    Characters/
    Interaction/
    UI/
    Systems/
  Shared/
  Editor/
  Tests/
```

每个文件聚焦一个主要类型或紧密相关的一组类型。命名空间表达模块边界，不依赖文件包含顺序。

## Agent 生成规则

- 使用目标项目已存在的 API 名称，不凭 C++ 名称猜脚本名称；
- 优先在 Editor/LSP API Reference 中检索绑定名；
- 使用 `Math::`、`Gameplay::`、`System::` 等脚本命名空间；
- 对可疑数值类型显式标注；
- 使用 `n""` 传递反复使用的函数名、GameplayTag 路径或 Overlay ID；
- 不生成 C++ 指针语法；
- 不默认使用 `StaticClass()`；目标配置可能已弃用或禁止，优先类字面量。

## 验证

保存后必须查看：

- Editor 输出与 VS Code Problems；
- 热重载是否保留当前实例；
- 是否出现结构性重实例化；
- 单元测试；
- simulate-cooked。

仅有语法高亮不代表 Editor 编译成功。
