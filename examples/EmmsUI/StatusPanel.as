class UAgentKitStatusPanel : UMMWidget
{
    FString FilterText;
    bool bAutoRefresh = true;
    double RefreshInterval = 1.0;

    UFUNCTION(BlueprintOverride)
    void DrawWidget(float DeltaTime)
    {
        mm::BeginVerticalBox(Padding=6);

            DrawHeader();
            DrawControls();
            DrawStatus();

        mm::EndVerticalBox();
    }

    private void DrawHeader()
    {
        mm::Text("Agent Kit Status", FontSize=16, bBold=true);
    }

    private void DrawControls()
    {
        mm::BeginHorizontalBox(Padding=4);

            mm::Slot_Fill();
            mm<UEditableTextBox> Filter = mm::EditableTextBox(FilterText);
            Filter.SetHintText(FText::FromString("Filter..."));

            mm::VAlign_Center();
            mm::CheckBox(bAutoRefresh, "Auto");

            mm::VAlign_Center();
            mm::SpinBox(RefreshInterval);

        mm::EndHorizontalBox();
    }

    private void DrawStatus()
    {
        mm::WithinBorder(FLinearColor(0.02, 0.02, 0.02, 0.8), RoundedCornerRadius=6);
        mm::Padding(8);

        if (FilterText.IsEmpty())
            mm::Text("No filter active");
        else
            mm::Text(f"Filtering by: {FilterText}");
    }
}
