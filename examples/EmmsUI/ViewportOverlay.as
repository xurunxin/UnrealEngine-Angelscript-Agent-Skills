class UAgentKitOverlaySubsystem : UScriptEngineSubsystem
{
    bool bVisible = true;
    int Counter = 0;

    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaTime)
    {
        if (!bVisible)
            return;

        mm::BeginDrawViewportOverlay(n"AgentKit.Overlay", OverlayZOrder=100);

            mm::HAlign_Right();
            mm::Padding(8);
            mm::WithinBorder(FLinearColor(0.0, 0.0, 0.0, 0.75), RoundedCornerRadius=6);

            mm::Padding(8);
            mm::BeginHorizontalBox();

                mm::VAlign_Center();
                mm::Text(f"Counter: {Counter}");

                mm::Padding(6, 0);
                if (mm::Button("+"))
                    Counter += 1;

            mm::EndHorizontalBox();

        mm::EndDraw();
    }
}
