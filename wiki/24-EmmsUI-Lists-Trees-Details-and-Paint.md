# 24. List、Tree、Details 与 Paint

## ListView 虚拟化

对大量数据使用：

```angelscript
mm<UListView> List = mm::ListView(FilteredItems.Num());

for (UMMListViewEntryWidget Entry : List)
{
    int Index = Entry.ItemIndex;
    if (!FilteredItems.IsValidIndex(Index))
        continue;

    mm::BeginDraw(Entry);
    DrawItem(FilteredItems[Index], Entry.IsListItemSelected());
    mm::EndDraw();
}
```

只绘制可见 Entry，避免创建整个列表的 UWidget。

## 当前 iterator protocol

当前锁定 UE‑AS 包含新 `Iterate()` range-for 协议；当前 EmmsUI 的 `FMMListViewIterator` 提供匹配的 `if_handle_then_const Iterate() const`。因此 0.1.0 的“当前引擎缺少新协议”警告已删除。

仍要做最小编译与运行测试，因为源码信号不能证明：

- 目标项目实际 checkout 的 SHA 正确；
- EmmsUI C++ module 已针对该引擎构建；
- visible entry 回收、滚动和 selection 正确；
- TreeView 与 ListView 的脚本类型推断没有项目特定冲突。

探针若返回 `compat.iterator_protocol_aligned`，表示可以进入编译 Gate，不表示 Gate 已通过。

## Selection

不要把 UListView 内部选择作为唯一业务状态。检测 `WasItemSelectionChanged()` 后，把稳定业务 ID 写入 ViewModel。数据筛选/重排时重新映射。

## TreeView

Tree item 使用 UObject 数据，提供 `OnGetItemChildren` UFUNCTION。Entry Widget 继承 `UMMListViewEntryWidget`，在 Draw 中读取当前 item，处理展开/选择。

避免循环引用，树数据生命周期应长于视图。

## UDetailsView

EmmsUI 可创建 Unreal Details View，显示 UObject 的反射属性。适合编辑器工具。注意：

- 只在 Editor module；
- 对象失效；
- Transaction；
- Filter/Category；
- 多对象编辑；
- 不要每帧设置不同对象导致重建。

## UMMPaintableWidget

适合自定义几何/绘制；业务状态仍外置。手工 Paint 与普通 UMG invalidation、DPI、Layer 和 hit-test 规则需要目标源码验证。

## 大数据优化

- 模型层筛选结果缓存；
- 查询变化才重新筛；
- 条目使用稳定 ID；
- 异步加载；
- 分页/增量；
- 不在 Entry Draw 内访问 AssetRegistry 全量查询；
- Profile list regeneration 和 object churn。
