/*
 * Target: UnrealEngine-Angelscript.
 * Verify exact component APIs against the pinned engine.
 */
class AAgentKitBeacon : AActor
{
    UPROPERTY(DefaultComponent, RootComponent)
    USceneComponent Root;

    UPROPERTY(DefaultComponent, Attach = Root)
    UBillboardComponent Billboard;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Beacon")
    float32 PulseInterval = 1.0f;

    bool bPulseEnabled = false;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        bPulseEnabled = true;
        System::SetTimer(this, n"HandlePulse", PulseInterval, bLooping=true);
    }

    UFUNCTION()
    private void HandlePulse()
    {
        if (!bPulseEnabled)
            return;

        Log(f"Beacon pulse: {GetName()}");
        BP_OnPulse();
    }

    UFUNCTION(BlueprintEvent, NotBlueprintCallable)
    void BP_OnPulse()
    {
    }
}
