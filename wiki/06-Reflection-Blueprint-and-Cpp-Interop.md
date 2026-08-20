# 06. 反射、Blueprint 与 C++ 互操作

## 何时进入反射

| 需求 | 机制 |
|---|---|
| Editor 可配置 | UPROPERTY |
| Blueprint 读取/写入 | UPROPERTY specifier |
| Blueprint 调用 | UFUNCTION |
| 覆盖 C++ BP event | BlueprintOverride |
| BP 子类覆盖脚本 | BlueprintEvent |
| RPC | UFUNCTION Server/Client/NetMulticast |
| OnRep | UFUNCTION |
| Dynamic Delegate | UFUNCTION |
| Timer 按名 | UFUNCTION |
| UMG Designer 绑定 | BindWidget |

## 最小暴露

```angelscript
class UWeaponConfig : UObject
{
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
    float32 Damage = 20.0f;

    // 纯脚本缓存，不进入 Unreal 反射。
    float32 CachedDamageMultiplier = 1.0f;
}
```

## BlueprintOverride

UE‑AS 会按绑定规则简化某些 C++ 事件名，例如移除 `Receive`、`BP_`、`K2_` 等前缀/后缀。不要手工猜；通过 LSP 查找。

## BlueprintEvent 安全模式

```angelscript
void ActivateAbility()
{
    ConsumeCost();
    StartCooldown();
    BP_PlayActivation();
}

UFUNCTION(BlueprintEvent, NotBlueprintCallable)
void BP_PlayActivation()
{
}
```

核心不变量先执行，Blueprint 只负责可选表现。

## C++ Super 限制

脚本父类可以：

```angelscript
Super::BeginPlay();
```

但 C++ BlueprintNativeEvent 的原生父实现不能按相同方式调用。C++ API 设计应提供一个普通 callable 函数承载父逻辑。

## 自动绑定

启动时扫描反射：

- BlueprintType UCLASS/USTRUCT；
- BlueprintCallable UFUNCTION；
- Blueprint-visible/editable UPROPERTY；
- UENUM；
- 静态函数库。

“Blueprint 可用 ⇒ 脚本通常可用”是原则，不保证所有特殊签名都能自动绑定。

## 命名与禁用

C++ 可通过 metadata 禁止或定制绑定。项目 Bind Database 还可能重命名。Agent 必须检查目标源码。

## GC

脚本对象引用由 UE‑AS 管理。反射属性中含 UObject 的自定义 C++ 类型仍需正确 AddReferencedObjects。不要把两个层次混淆。

## UMG

保留式 UMG 模式：

```angelscript
class UHUDWidget : UUserWidget
{
    UPROPERTY(BindWidget)
    UTextBlock StatusText;
}
```

EmmsUI 模式参阅 [UI 选型](13-UI-Technology-Decision.md)。
