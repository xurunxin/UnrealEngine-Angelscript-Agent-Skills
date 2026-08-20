struct FAgentKitNotification
{
    FName Id;
    FString Message;
    double ExpiresAt = 0.0;
}

class UAgentKitNotificationSubsystem : UScriptWorldSubsystem
{
    TArray<FAgentKitNotification> Notifications;

    void Push(FName Id, FString Message, double LifetimeSeconds)
    {
        FAgentKitNotification Item;
        Item.Id = Id;
        Item.Message = Message;
        Item.ExpiresAt = System::GameTimeSeconds + LifetimeSeconds;
        Notifications.Add(Item);
    }

    void RemoveExpired()
    {
        const double Now = System::GameTimeSeconds;
        for (int Index = Notifications.Num() - 1; Index >= 0; --Index)
        {
            if (Notifications[Index].ExpiresAt <= Now)
                Notifications.RemoveAt(Index);
        }
    }
}
