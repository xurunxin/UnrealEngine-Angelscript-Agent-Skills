---
name: ueas-reflection-blueprint
description: Use when UE-AS members need Blueprint, reflection, delegate, timer or UMG access. Do not use for native C++ bindings or replication policy.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS Reflection and Blueprint

为成员确定真实消费者；脚本内部缓存、临时状态和 helper 保持普通字段/函数。只有 Unreal 反射、Blueprint、序列化、复制或按名 API 确实需要时才增加宏。

## 不同表面不要混为一谈

| 需求 | 首选表面 |
|---|---|
| 脚本内部读写 | 普通字段/函数 |
| 设计师只配置类默认值 | `EditDefaultsOnly` |
| Blueprint 只读 | `BlueprintReadOnly` 或窄 Getter |
| Blueprint 受控写入 | `BlueprintCallable` 命令函数，不直接开放字段写权限 |
| Blueprint 只扩展表现 | `BlueprintEvent, NotBlueprintCallable` Hook |
| 动态委托/Timer 按名回调 | 最小 `UFUNCTION` |
| 复制/RPC | 路由到 `ueas-networking` |
| 原生 C++ API 不可见 | 路由到 `ueas-cpp-bindings` |

不要用 `BlueprintReadWrite` 代替业务 API 设计。

## UPROPERTY

显式写出所需权限，避免依赖项目默认宏行为：

```angelscript
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Scanner")
float ScanRadius = 500.0;
```

UE-AS 脚本引用由脚本运行时追踪；不要把“所有 UObject 引用都必须 UPROPERTY，否则必然被
GC”当作通用规则。`UPROPERTY` 的理由应是 Unreal 反射、序列化、编辑、复制或相关 API。

## UFUNCTION

常见用途：

- `BlueprintOverride`：覆盖 C++ Blueprint event；
- `BlueprintEvent`：允许 Blueprint 子类覆盖脚本 Hook；
- `NotBlueprintCallable`：进入反射但不允许 Blueprint 任意调用；
- `CallInEditor`：明确的 Editor 动作；
- Delegate/Timer 的按名目标；
- RPC：交给 Networking Skill。

当前基线会拒绝 BlueprintCallable/BlueprintEvent 参数名 `Self`，因为它与 Unreal 反射保留
语义冲突。改为 `Target`、`Object` 或领域名称，不修改生成器绕过。

普通脚本函数通常具有更轻的热重载表面，因此不要批量添加 `UFUNCTION`。

## Blueprint Hook 分层

核心不变量由不可绕过的脚本入口保持，Blueprint 只覆盖窄 Hook：

```angelscript
void ExecuteAction()
{
    ValidateAction();
    ApplyAuthoritativeState();
    BP_OnActionExecuted();
}

UFUNCTION(BlueprintEvent, NotBlueprintCallable)
void BP_OnActionExecuted()
{
}
```

这避免 Blueprint 子类因为忘记调用父逻辑而跳过权限、状态或资源更新。

## 按需深入

- Accessor、Delegate/Timer、BindWidget 或脚本/C++ 父调用：[回调与 Widget 边界](references/callbacks-and-widgets.md)。
- 字段、反射签名、继承、默认组件、Widget 绑定或值覆盖问题：[默认值与结构性热重载](references/defaults-and-reload.md)。

结构变化不能按函数体热重载处理。Editor-only 类型不得出现在 cooked Runtime 签名；网络策略和原生 API 缺失分别交给 Networking、C++ Bindings。

## 验收

实现或修复后验证实际 Blueprint 消费者、相关资产编译以及默认值/实例覆盖。回调变更检查重复绑定和生命周期；结构变化检查重实例化及恢复路径。保持权限最小且 Blueprint 无法绕过核心不变量。继续修复已授权范围内的失败，并区分实际通过、仅静态检查和未执行的运行验证。报告受影响成员、结构变化、证据及剩余限制；仅设计或审查时不声称已经执行修改。
