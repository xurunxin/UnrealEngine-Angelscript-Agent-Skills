# 25. EmmsUI 编辑器工具

## UMMEditorUtilityTab

```angelscript
#if EDITOR
class UAssetAuditTab : UMMEditorUtilityTab
{
    default TabTitle = "Asset Audit";
    default Category = "Project Tools";
    default Icon = n"Icons.Search";

    FString Query;
    TArray<FAssetData> Results;

    UFUNCTION(BlueprintOverride)
    void OnTabOpened()
    {
        Refresh();
    }

    UFUNCTION(BlueprintOverride)
    void DrawTab(float DeltaTime)
    {
        DrawToolbar();
        DrawResults();
    }
}
#endif
```

## Hot Reload

最新 EmmsUI 会监听 `OnObjectsReinstanced`，当脚本 Tab 对象被替换时：

- 调用旧对象 OnTabClosed；
- 把 SlateTab 迁移给新对象；
- 重新 Spawn；
- 清理旧 StrongSelf/MMWidget/Delegate。

旧版本不一定有此修复。升级或回移后测试。

## 弱引用

Tab 中保存关卡 Actor：

```angelscript
TWeakObjectPtr<AActor> SelectedActor;
```

切图后 `IsValid()` 再访问。强引用旧 Actor 会阻止非法 World 对象释放。

## Detail Customization

Class：

1. `CustomizeDetails()` 添加 Immediate Row；
2. 保存返回的 UMMWidget；
3. Tick 中 BeginDraw；
4. 操作 `GetCustomizedObject()`；
5. Transaction。

Struct：

1. `CustomizeHeader/Children`；
2. `GetStructValue(Type)`；
3. 修改拷贝；
4. `SetStructValue`。

## Context Menu

`FMMContextMenu` 支持：

- Option；
- Checkbox；
- Section；
- Separator；
- SubMenu；
- UFUNCTION Delegate。

菜单构建和业务执行分离。回调重新验证对象，不依赖菜单打开时的裸指针。

## Prompt

复杂参数用 UPROPERTY struct + `EditorPrompt::ShowPromptForStruct`。比手工维护临时 Form 更符合 Unreal 反射与类型校验。

## 工具状态机

长任务状态：

```text
Idle → Planning → Confirming → Running → Completed/Failed/Cancelled
```

Draw 仅显示状态和接受指令；实际执行分批或通过任务系统。
