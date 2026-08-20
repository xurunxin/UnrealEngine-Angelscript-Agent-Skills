/*
 * Verify HasAuthority(), replication condition names, and component setup
 * against the target project.
 */
class AAgentKitReplicatedSwitch : AActor
{
    default bReplicates = true;

    UPROPERTY(ReplicatedUsing = OnRep_Enabled)
    bool bEnabled = false;

    UFUNCTION(BlueprintCallable)
    void RequestSetEnabled(bool bRequestedEnabled)
    {
        if (HasAuthority())
        {
            CommitEnabled(bRequestedEnabled);
        }
        else
        {
            Server_RequestSetEnabled(bRequestedEnabled);
        }
    }

    UFUNCTION(Server, Reliable)
    private void Server_RequestSetEnabled(bool bRequestedEnabled)
    {
        if (!CanClientChangeState())
            return;

        CommitEnabled(bRequestedEnabled);
    }

    private bool CanClientChangeState() const
    {
        // Replace with ownership, range, cooldown, and permission checks.
        return true;
    }

    private void CommitEnabled(bool bNewEnabled)
    {
        if (bEnabled == bNewEnabled)
            return;

        bEnabled = bNewEnabled;
        RefreshPresentation();
    }

    UFUNCTION()
    private void OnRep_Enabled()
    {
        RefreshPresentation();
    }

    private void RefreshPresentation()
    {
        BP_OnPresentationChanged(bEnabled);
    }

    UFUNCTION(BlueprintEvent, NotBlueprintCallable)
    void BP_OnPresentationChanged(bool bNowEnabled)
    {
    }
}
