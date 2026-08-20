class AAgentKitDoor : AActor
{
    bool bOpen = false;

    UFUNCTION(BlueprintCallable)
    void SetDoorOpen(bool bRequestedOpen)
    {
        if (bOpen == bRequestedOpen)
            return;

        // Required invariant stays in script and cannot be skipped by Blueprint.
        bOpen = bRequestedOpen;
        UpdateCollision();

        // Blueprint only customizes presentation.
        BP_OnDoorStateChanged(bOpen);
    }

    private void UpdateCollision()
    {
        // Project-specific collision update.
    }

    UFUNCTION(BlueprintEvent, NotBlueprintCallable)
    void BP_OnDoorStateChanged(bool bNowOpen)
    {
    }
}
