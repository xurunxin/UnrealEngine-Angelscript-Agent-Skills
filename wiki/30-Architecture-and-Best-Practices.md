# 30. 架构与最佳实践

## 推荐分层

```text
C++ Platform / Core
      ↑ automatic bindings / mixins
UE-AS Domain Rules
      ↑
UE-AS Gameplay Adapters
      ↑
Blueprint / UMG / EmmsUI Views
```

## 规则一：变化频率决定语言边界

- 高频变化 Gameplay：UE‑AS；
- 稳定底层/性能热点：C++；
- 设计师资产装配：Blueprint；
- 代码工具界面：EmmsUI。

不要按团队职位机械划分。

## 规则二：核心不变量不可由 View 跳过

UI/Blueprint 只发 Command；Model/Service 校验并提交状态。网络服务端重复校验。

## 规则三：反射是 API，不是装饰

每个 UPROPERTY/UFUNCTION 都可能被资产、BP、网络或工具依赖。显式权限、Category、命名和弃用策略。

## 规则四：纯规则先单测

把逻辑从 Tick/Actor 拆到 namespace/struct。Actor 只适配生命周期。

## 规则五：Editor 与 Runtime 单向依赖

Editor → Runtime；Runtime ✕ Editor。Script 目录与 C++ module 同时执行边界。

## 规则六：版本是架构输入

任何 UE‑AS/EmmsUI 设计先固定版本。手工绑定、迭代协议和热重载逻辑是高变面。

## 规则七：UI 是状态投影

EmmsUI Draw 不承担权威状态。输入通过引用或事件写 Model，再从 Model 重绘。

## 规则八：验证覆盖真实环境

- Hot reload；
- Editor restart；
- Standalone；
- Dedicated client/server；
- simulate-cooked；
- Cook/Package；
- Shipping cache。

## 反模式

- God Subsystem；
- 每帧 GetAllActors；
- 过度 BlueprintCallable；
- Blueprint 负责核心事务；
- Reliable 输入流；
- Editor-only 类型穿透；
- UI widget 作为数据库；
- 每帧同步资产加载；
- 未固定 upstream master；
- “编译成功”等同“兼容”。
