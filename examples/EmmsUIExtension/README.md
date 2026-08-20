# EmmsUI Extension Skeleton

这里不提供可直接编译的完整 helper，因为 Attr specification 的初始化、
binding 注册阶段和目标 UE‑AS API 都具有版本敏感性。正确流程：

1. 在目标 EmmsUI commit 搜索最相近 helper；
2. 在 `EmmsWidgetHelpers.h/.cpp` 添加 helper；
3. 复用 `GetWidgetAttrSpec` / Event lookup；
4. 通过 `UEmmsStatics::AddWidget` 获取节点；
5. 用 `FEmmsAttributeState::SetPendingValue`；
6. 输入控件实现 mirrored/current/pending 四方协调；
7. 在脚本绑定阶段添加函数与文档；
8. Runtime 与 Editor module 分离；
9. 增加脚本测试和 Cook 测试。

`HelperChecklist.md` 是实现 PR 的检查表。
