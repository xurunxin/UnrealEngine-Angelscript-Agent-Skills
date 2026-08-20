---
name: ueas-cpp-bindings
description: >-
  Expose C++ APIs to UnrealEngine-Angelscript using automatic reflection bindings, script mixins, metadata controls, and narrowly scoped manual bindings. Use when a required native API is not correctly visible to scripts. Do not use when ordinary script code or reflection annotations already solve the task.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---


# UE‑AS C++ Bindings

## 首选顺序

1. 已存在 Blueprint API 的自动绑定；
2. 调整 UCLASS/USTRUCT/UFUNCTION/UPROPERTY metadata；
3. `ScriptMixin` 静态库；
4. 专用 Blueprint/Script Function Library；
5. 最后才写手工 AngelScript binding。

参阅 [`../../wiki/11-Cpp-Bindings.md`](../../wiki/11-Cpp-Bindings.md)。

## 自动绑定原则

如果 C++ API 可被 Blueprint 使用，通常应自动在脚本可见。实际脚本名称可能经过：

- `UKismet` / `UBlueprint` 前缀剥离；
- `Library` / `BlueprintFunctionLibrary` 等后缀剥离；
- `ScriptName`；
- bool `b` 前缀规范化；
- 特定项目 Bind Database 重命名。

因此先在 UE‑AS API Reference/LSP 搜索，不直接把 C++ 全名翻译成脚本调用。

## 控制绑定

常见元数据/标记：

- `NotInAngelscript`
- `NoAutoAngelscriptBind`
- `ScriptReadWrite`
- `ScriptReadOnly`
- `ScriptCallable`

避免为了脚本暴露而过度扩大 Blueprint API；在项目允许时使用 Script 专用标记。

## Mixin

当 C++ 类型尤其 USTRUCT 缺少自然成员方法时，用 `ScriptMixin`：

```cpp
UCLASS(Meta=(ScriptMixin="FInventoryEntry"))
class UInventoryEntryScriptLibrary : public UObject
{
    GENERATED_BODY()

public:
    UFUNCTION(ScriptCallable)
    static bool IsValidEntry(const FInventoryEntry& Entry);
};
```

脚本侧得到类似：

```angelscript
if (Entry.IsValidEntry())
{
}
```

具体签名和 metadata 以目标 UE‑AS commit 为准。

## 手工绑定门槛

只有以下情况才考虑：

- 非 UHT 类型；
- 模板/迭代器/运算符；
- 需要特殊 ABI 或泛型调用；
- 反射无法表达；
- 性能上必须绕过 ProcessEvent。

手工绑定必须：

- 明确注册阶段顺序；
- 处理对象所有权、GC 引用和异常；
- 提供文档 metadata；
- 有编译与运行测试；
- 在引擎升级时有兼容性测试。

## EmmsUI 相关

EmmsUI 的 `mm<T>` 是手工注册的协变模板；随后枚举所有原生 UWidget/UPanelSlot 反射属性与委托，自动生成 `SetX/GetX/WasX/OnX`。扩展时优先让反射自动覆盖新 Widget，不要为每个属性手写 helper。

## 完成标准

交付说明为什么自动绑定不足，并附目标 C++ 与脚本侧的编译测试。
