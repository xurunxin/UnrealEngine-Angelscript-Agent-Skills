# 08. 网络

## 复制属性

```angelscript
class AReplicatedSwitch : AActor
{
    default bReplicates = true;

    UPROPERTY(ReplicatedUsing = OnRep_Enabled)
    bool bEnabled = false;

    UFUNCTION()
    void OnRep_Enabled()
    {
        ApplyVisualState();
    }
}
```

服务器更新时也主动调用统一的 `ApplyVisualState()`，不要只依赖客户端 OnRep。

## RPC

```angelscript
UFUNCTION(Server, Reliable)
void Server_RequestSetEnabled(bool bRequested)
{
    if (!CanChangeState())
        return;

    bEnabled = bRequested;
    ApplyVisualState();
}
```

默认 RPC Reliable；显式思考是否要 `Unreliable`.

## Reliability 决策

| 类型 | 建议 |
|---|---|
| 稀少、必须到达命令 | Reliable |
| 高频输入/瞄准 | Unreliable |
| 持久状态 | Replicated property |
| 视觉瞬时效果 | Unreliable Multicast 或本地由状态推导 |
| 晚加入必须知道 | Replicated state |

## Authority 与 Ownership

Server RPC 只能从拥有该 Actor/Component 的客户端可靠调用。世界物体通常不由客户端拥有，需通过 PlayerController/Pawn/Owned Component 转发请求。

## Replication Condition

根据 OwnerOnly、SkipOwner、InitialOnly 等条件减少流量，但测试所有观察者。条件名称以目标 UE‑AS 绑定为准。

## 安全

服务端验证：

- 调用者；
- 距离；
- 频率；
- 参数范围；
- 当前状态；
- 资源消耗；
- 重放/重复。

客户端 UI 不构成权限。

## Integration Test

默认 UE‑AS 集成测试支持 client/dedicated-server。测试至少断言：

- Server 权威值；
- Client A/B 收到值；
- 非 Owner 请求被拒绝；
- 晚加入同步；
- Unreliable 在丢包下不破坏最终状态。

## 常见问题

- `bReplicates` 未开启；
- Component 未复制；
- OnRep 不是 UFUNCTION；
- RPC 名称/签名热重载后旧 BP 引用；
- Reliable 高频；
- Multicast 当数据库；
- Standalone 通过，Dedicated 失败。
