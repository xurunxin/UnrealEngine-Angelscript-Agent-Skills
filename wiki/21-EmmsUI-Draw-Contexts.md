# 21. EmmsUI 绘制上下文

## 1. UMMWidget

```angelscript
class UStatusPanel : UMMWidget
{
    UFUNCTION(BlueprintOverride)
    void DrawWidget(float DeltaTime)
    {
        mm::Text("Status");
    }
}
```

`UMMWidget` 默认在 Construct 和 Tick 驱动 Draw。可通过默认属性控制 `bDrawOnConstruct`、`bAllowDraw` 和根 Panel。

## 2. 外部 BeginDraw

```angelscript
mm::BeginDraw(TargetWidget);
DrawPanel();
mm::EndDraw();
```

适合：

- Detail customization 返回的 UMMWidget；
- ListView entry；
- WidgetComponent 实例；
- 外部系统拥有的 UMMWidget。

禁止同一个 UMMWidget 重入 BeginDraw。源码会检测并抛错。

## 3. Viewport Overlay

```angelscript
mm::BeginDrawViewportOverlay(n"Debug.Network", 100);
DrawNetworkOverlay();
mm::EndDraw();
```

Overlay ID 是复用键。使用稳定 `FName`，不要每帧动态生成。停止调用后由 Subsystem 生命周期管理移除；具体过期行为检查目标版本。

## 4. Popup Window

继承 `UMMPopupWindow`：

```angelscript
class UConfirmWindow : UMMPopupWindow
{
    UFUNCTION(BlueprintOverride)
    void DrawWindow(float DeltaTime)
    {
        mm::Text("Continue?");
        if (mm::Button("Close"))
            CloseWindow();
    }
}
```

## 5. Widget Component

组件 WidgetClass 设置为 `UMMWidget`，取得实例后 BeginDraw。注意：

- World-space 输入；
- Widget 初始化时机；
- Dedicated Server 不创建视觉；
- Actor 销毁后引用失效。

## 6. Editor Tab / Detail Row

由 EmmsUIEditor 类型创建 UMMWidget 容器，再在 Tick/Draw 中 BeginDraw。参阅 [EmmsUI Editor Tools](25-EmmsUI-Editor-Tools.md)。

## Begin/End 纪律

错误：

```angelscript
mm::BeginHorizontalBox();
if (!bReady)
    return; // End 未执行
```

推荐：

```angelscript
if (!bReady)
{
    mm::Text("Loading...");
    return;
}

DrawReadyContent();
```

或把作用域拆小，不在 Begin/End 中间早退。

源码对缺失 EndDraw、Panel 未结束、类型不匹配会抛错并尝试恢复，但不应依赖恢复机制。

## 嵌套根

ListView Entry 需要自己的 BeginDraw/EndDraw，这是独立根绘制，不是简单把 Entry 当当前 Panel 子节点。不要跨根混用 Handle。
