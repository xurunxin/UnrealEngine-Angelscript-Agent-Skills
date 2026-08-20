#if EDITOR

class UAgentKitActorBrowserTab : UMMEditorUtilityTab
{
    default TabTitle = "Agent Kit Actor Browser";
    default Category = "Agent Kit";
    default Icon = n"ClassIcon.Actor";

    FString Query;
    TArray<TWeakObjectPtr<AActor>> VisibleActors;
    TWeakObjectPtr<AActor> SelectedActor;

    UFUNCTION(BlueprintOverride)
    void OnTabOpened()
    {
        RebuildResults();
    }

    UFUNCTION(BlueprintOverride)
    void DrawTab(float DeltaTime)
    {
        mm::BeginVerticalBox();

            mm<UEditableTextBox> Search = mm::EditableTextBox(Query);
            Search.SetHintText(FText::FromString("Search actors..."));

            if (Search.WasTextChanged())
                RebuildResults();

            mm::Slot_Fill();
            DrawActorList();

        mm::EndVerticalBox();
    }

    private void DrawActorList()
    {
        mm<UListView> List = mm::ListView(VisibleActors.Num());

        for (UMMListViewEntryWidget Entry : List)
        {
            if (!VisibleActors.IsValidIndex(Entry.ItemIndex))
                continue;

            AActor Actor = VisibleActors[Entry.ItemIndex].Get();
            if (Actor == nullptr)
                continue;

            mm::BeginDraw(Entry);

                FLinearColor Background = Entry.IsListItemSelected()
                    ? FLinearColor(0.05, 0.20, 0.08, 1.0)
                    : FLinearColor::Transparent;

                mm<UBorder> Row = mm::WithinBorder(Background);
                mm::Padding(5);
                mm::Text(Actor.ActorNameOrLabel);

                if (Row.WasClicked())
                    SelectedActor = Actor;

            mm::EndDraw();
        }
    }

    private void RebuildResults()
    {
        VisibleActors.Reset();

        TArray<AActor> Actors;
        Gameplay::GetAllActorsOfClass(AActor, Actors);

        for (AActor Actor : Actors)
        {
            if (Actor == nullptr)
                continue;

            if (Query.IsEmpty() || Actor.ActorNameOrLabel.Contains(Query))
                VisibleActors.Add(Actor);
        }
    }
}

#endif
