struct FAgentKitHealthState
{
    float Current = 100.0;
    float Maximum = 100.0;

    float GetPercent() const property
    {
        return Maximum > 0.0 ? Current / Maximum : 0.0;
    }
}

namespace AgentKitHealth
{
    void Clamp(FAgentKitHealthState& State)
    {
        State.Maximum = Math::Max(State.Maximum, 0.0);
        State.Current = Math::Clamp(State.Current, 0.0, State.Maximum);
    }
}

class UAgentKitHealthComponent : UActorComponent
{
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Health")
    float32 DefaultMaximum = 100.0f;

    FAgentKitHealthState State;

    event void FOnHealthChanged(float Current, float Maximum);
    FOnHealthChanged OnHealthChanged;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        State.Maximum = DefaultMaximum;
        State.Current = DefaultMaximum;
        BroadcastState();
    }

    UFUNCTION(BlueprintCallable)
    void ApplyDamage(float Amount)
    {
        if (Amount <= 0.0)
            return;

        State.Current -= Amount;
        AgentKitHealth::Clamp(State);
        BroadcastState();
    }

    private void BroadcastState()
    {
        OnHealthChanged.Broadcast(State.Current, State.Maximum);
    }
}
