---
name: ueas-reflection-blueprint
description: >-
  Design the smallest safe Unreal reflection surface from Angelscript for
  UPROPERTY, UFUNCTION, Blueprint hooks, delegates, timers, accessors, UMG,
  serialization, and GC boundaries. Use when Unreal or Blueprint must discover a
  script member. Do not use for exposing non-reflected native C++ APIs or
  implementing replication policy.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---

# UE-AS Reflection and Blueprint

## 核心决定

先为每个成员写出真实消费者：

```text
script-only
editor-details
blueprint-read
blueprint-write
blueprint-override
serialization/defaults
replication
runtime-reflection
delegate-or-timer
umg-bind-widget
```

只有消费者跨越 Unreal 反射边界时，才添加 `UPROPERTY` 或 `UFUNCTION`。内部缓存、临时状态、
实现 helper 和纯脚本调用保持普通成员/函数。

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

### 默认值来源

区分：

- 脚本字段初始化与 `default` 语句；
- 生成类的 CDO；
- Blueprint Class Defaults；
- 关卡/资产实例覆盖；
- 运行时修改。

热重载后出现“值没有更新”时，先确认哪一层拥有覆盖值，不要重复写构造式修复。

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

## Accessor

脚本 property accessor 可隐藏实现并保持自然语法：

```angelscript
float GetHealthPercent() const property
{
    return MaximumHealth > 0.0 ? CurrentHealth / MaximumHealth : 0.0;
}
```

使用前核对目标项目的隐式 Getter/Setter 设置。需要 Blueprint 访问时，再为具体消费者设计
反射函数；不要假设脚本 accessor 自动形成所需 Blueprint API。

## Delegate 与 Timer

- `delegate` 为单播，`event` 为多播；
- `BindUFunction` / `AddUFunction` 的按名目标必须进入反射；
- Handler 使用稳定函数名，例如 `n"HandleChanged"`；
- 生命周期结束、目标变化或重新初始化时解除绑定；
- 重复热重载/初始化后检查是否多次注册；
- Timer 回调只暴露实际需要的函数，多个并发 Timer 不要错误共享同一身份。

## UMG 与 EmmsUI 边界

- Widget Blueprint 视觉树需要脚本字段连接时使用 `UPROPERTY(BindWidget)`；
- `BindWidget` 名称、类型或父类变化属于结构性 ABI 变化；
- 代码驱动的 Runtime/Editor UI 分别交给 `emmsui-runtime` 或 `emmsui-editor-tools`；
- 只有现有 EmmsUI helper 无法表达需求时才交给 `emmsui-extension`。

## Super 限制

`Super::Function()` 适用于脚本父类。不要假设它能调用所有 C++ `BlueprintNativeEvent` 的原生
父实现。必须执行的原生逻辑应放在非事件函数，由事件包装或 Hook 调用。

## 热重载分类

### 通常较轻

- 普通函数体修改；
- 不改变反射签名的局部逻辑；
- 普通脚本 helper。

### 结构性修改

- 新增/删除/改类型的反射字段；
- UFUNCTION 参数、返回值或 specifier 变化；
- 父类、接口、默认子对象变化；
- `BindWidget` 名称/类型变化；
- Blueprint 可见 API 重命名。

结构性修改后检查 Blueprint 编译、CDO/实例值、Delegate、Timer、Widget 绑定和已打开 Editor
工具。出现不一致时优先完整编译、关闭 PIE、重新打开资产或重启 Editor，不用继续叠加热重载。

## 验收

- 每个反射成员都有具体消费者；
- Blueprint 权限没有超过需求；
- 核心不变量不能被 Blueprint 绕过；
- Blueprint 子类和相关资产重新编译；
- 默认值与实例覆盖按预期保留；
- Delegate/Timer 不重复注册；
- Editor-only 类型没有进入 cooked Runtime 签名；
- 结构性修改的恢复和验证范围已记录；
- 网络和 C++ Binding 需求已正确交接。

## 输出

```yaml
Result:
  mode: design | implement | review | repair
  reflected_members:
    - member: ""
      consumer: ""
      specifiers: []
  script_only_members: []
  blueprint_hooks: []
  structural_changes: []
  evidence: []
  risks_or_unverified: []
  next_handoff:
    skill: null
    completion_gate: "Blueprint/assets compile and relevant runtime gate passes"
```
