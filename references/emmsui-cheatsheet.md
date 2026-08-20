# EmmsUI Cheat Sheet

## Root

```angelscript
class UPanel : UMMWidget
{
    UFUNCTION(BlueprintOverride)
    void DrawWidget(float DeltaTime)
    {
    }
}
```

```angelscript
mm::BeginDraw(Target);
...
mm::EndDraw();
```

```angelscript
mm::BeginDrawViewportOverlay(n"StableId");
...
mm::EndDraw();
```

## Layout

```angelscript
mm::BeginVerticalBox();
mm::EndVerticalBox();

mm::BeginHorizontalBox();
mm::EndHorizontalBox();

mm::WithinBorder(Color);
mm::WithinSizeBox(MinWidth=200);
mm::BeginScrollBox(EOrientation::Orient_Vertical);
```

## Slot before child

```angelscript
mm::Slot_Fill();
mm::Padding(8);
mm::Text("Fills parent");
```

## Basic widgets

```angelscript
mm::Text("Label", FontSize=14, bBold=true);
mm::Spacer(8);
if (mm::Button("Run")) {}
mm::Image(n"Icons.Search");
```

## Input

```angelscript
mm::EditableTextBox(Query);
mm::Slider(Value, 0, 100);
mm::SpinBox(Value);
mm::CheckBox(bEnabled, "Enabled");
```

State must persist across Draws.

## Typed handle

```angelscript
mm<UTextBlock> Label = mm::Text("Ready");
Label.SetAutoWrapText(true);
```

## Event

```angelscript
if (Button.WasClicked()) {}

Button.OnClicked(this, n"HandleClicked");
```

## List

```angelscript
mm<UListView> List = mm::ListView(Count);
for (UMMListViewEntryWidget Entry : List)
{
    mm::BeginDraw(Entry);
    ...
    mm::EndDraw();
}
```

## Rules

- Begin/End pair；
- Slot property before child；
- persistent model state；
- stable sibling ordering；
- ListView for large lists；
- avoid heavy work in Draw；
- avoid long-lived `mm<T>` handles；
- `GetUnderlyingWidget()` only as escape hatch；
- verify target version.
