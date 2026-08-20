# 28. EmmsUI 组合模式

## 函数组合

```angelscript
void DrawSectionHeader(FString Title)
{
    mm::Padding(8, 4);
    mm::Text(Title, 14, bBold=true);
}
```

小函数只声明 UI，不持有隐藏状态。

## ViewModel

```angelscript
class UAssetAuditViewModel : UObject
{
    FString Query;
    bool bRunning = false;
    TArray<FAssetAuditRow> Rows;

    void SetQuery(FString NewQuery)
    {
        if (Query == NewQuery)
            return;
        Query = NewQuery;
        RebuildRows();
    }
}
```

UI 只调用 ViewModel。这样可单测，UMG/EmmsUI 可共享。

## Stable Branch Wrapper

```angelscript
void DrawOptionalAdvanced()
{
    mm::BeginVerticalBox();

    if (bAdvanced)
        DrawAdvancedContents();
    else
        mm::Spacer(0);

    mm::EndVerticalBox();
}
```

不同逻辑区域使用独立父 Panel，减少同类 sibling 身份错位。

## Command Queue

按钮不直接执行长任务：

```angelscript
if (mm::Button("Scan"))
    PendingCommand = EAuditCommand::StartScan;
```

Tick/Subsystem 消费并更新状态。

## Table-like List

使用 ListView + Entry Draw，列宽/样式由独立函数。业务行由稳定 ID，而不是 index 唯一标识。

## Error Boundary

Draw 前验证：

```angelscript
if (Model == nullptr)
{
    DrawEmptyState("Model unavailable");
    return;
}
```

不要在 Begin Panel 后深层抛出/早退。

## Style Tokens

集中定义：

```angelscript
namespace UIStyle
{
    const float SectionGap = 8.0;
    const FLinearColor Error = FLinearColor(...);
}
```

更复杂样式优先 Slate Style/UMG assets，不在每个 Draw 重建 Brush。

## Hybrid Widget

通过 `mm::Widget(UMyComplexWidget)` 嵌入已有 UMG Widget，再用自动属性或有限 UnderlyingWidget API 配置。复杂动画留给 UMG，外围布局和工具流程用 EmmsUI。
