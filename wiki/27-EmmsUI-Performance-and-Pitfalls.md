# 27. EmmsUI 性能与陷阱

## 性能事实

EmmsUI 复用 UWidget 并差分层级/属性，但 Draw 函数本身仍每帧执行。性能由以下部分组成：

- Script Draw；
- 数据查询；
- Widget lookup；
- 属性比较/复制；
- Widget rebuild；
- Panel child reorder；
- Slate invalidation/layout；
- Paint；
- UObject/GC。

## 常见热点

### Draw 中全量扫描

错误：

```angelscript
void DrawWidget(float DeltaTime)
{
    Gameplay::GetAllActorsOfClass(AActor, Actors);
}
```

改为在 World 变化/查询变化/定时刷新时更新模型。

### 每帧同步加载

使用 `mm::AsyncLoadAsset` 或项目异步资源系统，把完成结果缓存。注意该 helper 在加载完成前会返回 nullptr，调用方不能把 nullptr 当永久缺失。

### 属性触发 rebuild

只读/构造属性变化可能重建 UWidget。高频动画不要依赖此路径。

### 子树重排

Panel 从第一个不匹配 child 起移除后续节点再添加。前部插入会放大成本。稳定顺序、局部 Panel 和 ListView 可以降低。

### 巨大字符串与 FText

仅在值变化时格式化昂贵文本；本地化展示使用 FText，日志使用 FString/f-string。避免每帧创建大量富文本。

## Profiling

- Unreal Insights；
- Stat Slate；
- Stat UObjects/GC；
- Script profiler（目标版本能力）；
- Widget Reflector；
- 自定义 Draw 时间；
- UWidget 创建计数；
- 属性 rebuild 计数。

## 预算

为内部 Editor 工具也设预算：

- Draw ms；
- 最大 UWidget 数；
- 搜索响应；
- 大列表滚动；
- 热重载恢复；
- GC 峰值。

## 陷阱

- Handle 跨帧保存；
- Draw 中早退漏 End；
- Pending Slot 用错目标；
- local input state；
- `Was...` 当队列；
- `GetUnderlyingWidget` 不复位；
- 条件重排同类型 input；
- Weak 引用未验证；
- Runtime module 引入 Editor dependency；
- master API 套在旧 UE‑AS。
