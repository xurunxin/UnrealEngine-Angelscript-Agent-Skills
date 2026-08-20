# 11. C++ 绑定

## 自动绑定

UE‑AS 启动时遍历 Unreal 反射。常见可见条件：

- UCLASS BlueprintType 或含 BlueprintCallable；
- USTRUCT BlueprintType 或有可编辑/Blueprint 属性；
- UPROPERTY BlueprintVisible/Edit；
- UFUNCTION BlueprintCallable；
- UENUM。

静态 Function Library 会转换成脚本命名空间。

## 脚本专用 metadata

目标版本支持的常见项：

- `NotInAngelscript`
- `NoAutoAngelscriptBind`
- `ScriptReadWrite`
- `ScriptReadOnly`
- `ScriptCallable`

在目标源码中确认，不跨版本硬编码。

## 名称映射

例如：

- `UKismetMathLibrary` → `Math::`
- `UGameplayStatics` → `Gameplay::`
- `UWidgetBlueprintLibrary` → `Widget::`

项目设置有 Prefix/Suffix strip 数组。LSP/API Reference 是最终脚本名来源。

## ScriptMixin

静态 C++ 方法的第一个参数为目标类型，可绑定成实例方法：

```cpp
UCLASS(Meta=(ScriptMixin="FMyStruct"))
class UMyStructMixinLibrary : public UObject
{
    GENERATED_BODY()

public:
    UFUNCTION(ScriptCallable)
    static FString Describe(const FMyStruct& Value);
};
```

## 手工绑定

适用于模板、运算符、迭代协议、非 UHT 类型。要求理解：

- 注册顺序；
- `FAngelscriptBinds`；
- TypeUsage；
- 泛型调用；
- Handle/Object ownership；
- GC；
- exception；
- docs metadata；
- Bind Database。

## 迭代协议

EmmsUI ListView 最近切换到新的 UE‑AS iterator protocol。手工绑定迭代器是版本敏感面。升级时通过最小脚本：

```angelscript
for (UMMListViewEntryWidget Entry : List)
{
}
```

验证，不只检查 C++ 编译。

## 绑定测试

- C++ 编译；
- 脚本可解析类型；
- overload resolution；
- null；
- const/ref/out；
- UObject GC；
- Blueprint 同时可用；
- Cook；
- 热重载；
- 文档生成。
