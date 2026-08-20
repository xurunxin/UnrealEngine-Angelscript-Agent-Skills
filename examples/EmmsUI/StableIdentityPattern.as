class UAgentKitIdentityExample : UMMWidget
{
    bool bShowAdvanced = false;
    FString BasicValue;
    FString AdvancedValue;

    UFUNCTION(BlueprintOverride)
    void DrawWidget(float DeltaTime)
    {
        mm::CheckBox(bShowAdvanced, "Advanced");

        // Each logical branch gets its own parent panel. This reduces the risk
        // that same-type editable widgets are reused for another logical field
        // when the branch appears or disappears.
        mm::BeginVerticalBox();
            mm::Text("Basic");
            mm::EditableTextBox(BasicValue);
        mm::EndVerticalBox();

        if (bShowAdvanced)
        {
            mm::BeginVerticalBox();
                mm::Text("Advanced");
                mm::EditableTextBox(AdvancedValue);
            mm::EndVerticalBox();
        }
    }
}
