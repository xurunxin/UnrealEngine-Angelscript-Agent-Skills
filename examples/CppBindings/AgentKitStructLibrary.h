#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "AgentKitStructLibrary.generated.h"

USTRUCT(BlueprintType)
struct FAgentKitRange
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    double Minimum = 0.0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    double Maximum = 1.0;
};

UCLASS(Meta=(ScriptMixin="FAgentKitRange"))
class UAgentKitStructLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintPure, ScriptCallable, Category="Agent Kit|Range")
    static bool Contains(const FAgentKitRange& Range, double Value);

    UFUNCTION(BlueprintPure, ScriptCallable, Category="Agent Kit|Range")
    static double Size(const FAgentKitRange& Range);
};
