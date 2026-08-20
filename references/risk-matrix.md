# Risk Matrix

| 变化 | Hot Reload | Cook | Runtime | 建议 |
|---|---:|---:|---:|---|
| 函数体 | 低 | 低 | 低 | 保存 + Unit |
| 普通字段新增 | 中 | 低 | 中 | 退出 PIE，检查实例 |
| UPROPERTY 改名/类型 | 高 | 中 | 高 | 迁移资产，重启 |
| UFUNCTION 签名 | 高 | 中 | 高 | BP/RPC/Delegate 全查 |
| 默认组件 | 高 | 中 | 高 | 实例/BP 迁移 |
| Editor-only API | 低 Editor | 高 | 高 | simulate-cooked |
| RPC Reliability | 低 compile | 低 | 高 | 网络压测 |
| EmmsUI Draw 结构 | 中 | 低 | 中 | 焦点/身份测试 |
| EmmsUI helper C++ | 高 | 高 | 高 | 全矩阵 |
| UE‑AS/EmmsUI upgrade | 高 | 高 | 高 | 分阶段升级 |
| Precompiled cache reuse | n/a | 高 | 高 | executable 匹配 |
