# 04. 语言速查

## 类型

| UE‑AS | 说明 |
|---|---|
| `int`, `int64` | 整数 |
| `float` | 默认设置通常为 64 位 |
| `float32`, `float64` | 显式精度 |
| `bool` | 布尔 |
| `FString` | 可变字符串 |
| `FName` / `n"Id"` | 名称，字面量编译期建立 |
| `FText` | 本地化展示文本 |
| `TArray<T>` | 数组 |
| `TMap<K,V>` | 映射 |
| `TSet<T>` | 集合 |
| `TSubclassOf<T>` | 类引用 |
| `TSoftObjectPtr<T>` | 软资产引用 |
| `TWeakObjectPtr<T>` | 弱对象引用 |

## 对象与结构体

```angelscript
class UInventoryModel : UObject
{
    TArray<FItemStack> Items;
}

struct FItemStack
{
    UPROPERTY()
    FName ItemId;

    UPROPERTY()
    int Amount = 1;

    bool IsEmpty() const
    {
        return Amount <= 0;
    }
}
```

Class 是引用语义；Struct 是值语义。UObject 不使用 C++ 指针/箭头。

## 默认值

```angelscript
class AExample : AActor
{
    float32 Cooldown = 0.5f;
    default bReplicates = true;
}
```

## 格式字符串

```angelscript
Log(f"Actor={GetName()} Value={Value :.2}");
Log(f"{DeltaSeconds =}");
```

## FName

```angelscript
Delegate.BindUFunction(this, n"HandleChanged");
mm::BeginDrawViewportOverlay(n"Debug.Inventory");
```

反复从普通字符串构造 FName 会有查表；稳定标识使用 `n""`.

## Cast

```angelscript
APlayerController PC = Cast<APlayerController>(GetOwner());
if (PC == nullptr)
    return;
```

## 属性访问器

```angelscript
float GetNormalized() const property
{
    return Maximum > 0.0 ? Current / Maximum : 0.0;
}
```

## 引用

```angelscript
void AddAmount(FItemStack& Stack, int Delta)
{
    Stack.Amount += Delta;
}

void TryFind(FName Id, bool&out bFound, FItemStack&out Stack)
{
    ...
}
```

## Mixin

```angelscript
mixin bool IsAlive(AActor Actor)
{
    return Actor != nullptr && !Actor.IsActorBeingDestroyed();
}

// Actor.IsAlive()
```

## Gameplay Tags

Tag `UI.Action.Escape` 自动变成：

```angelscript
GameplayTags::UI_Action_Escape
```

## 条件编译

```angelscript
#if EDITOR
...
#endif

#if TEST
...
#endif

#if RELEASE
...
#endif
```

## 常见 C++ 迁移错误

- `Object->Function()` → `Object.Function()`
- `UObject*` → `UObject`
- 构造函数 → 字段 initializer + `default`
- `FMath::` → 通常 `Math::`
- `UGameplayStatics::` → 通常 `Gameplay::`
- `GetWorld()->` → World Context/Subsystem API
- 所有字段 UPROPERTY → 只保留反射需要字段
