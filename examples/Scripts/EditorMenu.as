#if EDITOR

class UAgentKitActorMenu : UScriptActorMenuExtension
{
    default SupportedClasses.Add(AActor);

    UFUNCTION(CallInEditor, Category = "Agent Kit")
    void LogSelectedActor(AActor Actor)
    {
        if (Actor == nullptr)
            return;

        Log(f"Selected actor: {Actor.ActorNameOrLabel}");
    }
}

#endif
