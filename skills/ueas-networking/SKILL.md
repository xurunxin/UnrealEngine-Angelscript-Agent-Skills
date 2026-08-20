---
name: ueas-networking
description: >-
  Implement and verify Unreal multiplayer replication and RPCs in Angelscript, including authority, ownership, reliability, OnRep, conditions, and dedicated-server integration tests. Use when state or calls cross network roles. Do not use for single-player state flow or general gameplay architecture without networking.
metadata:
  version: "0.2.0"
  language: zh-CN
  owner: xurunxin
---


# UE‑AS Networking

## 适用范围

`Replicated`、`ReplicatedUsing`、`Server`、`Client`、`NetMulticast`、Authority、Ownership、多人同步。

## 先建立权威模型

在写宏前说明：

- 谁拥有状态；
- 谁可以请求；
- 谁验证；
- 谁接收；
- 丢包是否可接受；
- 状态是否需要晚加入同步；
- 是否能由客户端预测。

## 复制属性

```angelscript
UPROPERTY(ReplicatedUsing = OnRep_DoorState)
bool bDoorOpen = false;

UFUNCTION()
void OnRep_DoorState()
{
    RefreshDoorVisuals();
}
```

Actor/Component 必须本身开启复制。`OnRep` 进入反射，因此需要 UFUNCTION。

## RPC

UE‑AS RPC 默认 Reliable；高频输入、瞄准或瞬时效果不要无意识使用 Reliable：

```angelscript
UFUNCTION(Server, Unreliable)
void Server_UpdateAim(FVector_NetQuantizeNormal AimDirection)
{
    if (!HasAuthority())
        return;

    // 校验并更新服务器状态
}
```

客户端提交只是请求，服务端仍要验证范围、频率、权限和对象状态。

## 状态与事件

- 持久状态：复制属性；
- 一次性且所有当前连接需要看到：RPC；
- 可从状态推导的表现：OnRep / 本地刷新；
- 晚加入者必须看到：不能只靠 Multicast；
- 大量动态条目：考虑 FastArray 或 C++ 能力，不要每帧复制整个 TArray。

## 测试矩阵

最低要求：

1. Dedicated Server + 1 Client；
2. Dedicated Server + 2 Clients；
3. Listen Server；
4. 晚加入；
5. 丢包/延迟模拟；
6. 对无权限客户端的恶意/错误请求；
7. 重连或 Actor relevancy 变化。

UE‑AS Integration Test 默认可以使用 client/dedicated-server 模式，不要为了让测试“更容易通过”默认切到 Standalone。

## 常见失败

- Actor 未设置 `bReplicates`；
- Component 未启用复制；
- RPC 调用对象没有正确 Ownership；
- OnRep 只刷新视觉但服务器本地从不调用同一刷新函数；
- Reliable 高频积压；
- Multicast 被当作持久状态；
- 只在单机 PIE 测试；
- Editor-only 工具路径被网络代码引用。

## 完成标准

提交说明中必须列出 Authority/Ownership/Reliability，并附实际 client/server 测试结果。
