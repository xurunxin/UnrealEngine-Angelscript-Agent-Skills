#include "AgentKitStructLibrary.h"

bool UAgentKitStructLibrary::Contains(const FAgentKitRange& Range, double Value)
{
    return Value >= Range.Minimum && Value <= Range.Maximum;
}

double UAgentKitStructLibrary::Size(const FAgentKitRange& Range)
{
    return FMath::Max(0.0, Range.Maximum - Range.Minimum);
}
