void Test_AgentKitHealthClamp(FUnitTest& T)
{
    FAgentKitHealthState State;
    State.Current = 125.0;
    State.Maximum = 100.0;

    AgentKitHealth::Clamp(State);

    T.AssertEquals(100.0, State.Current);
    T.AssertEquals(1.0, State.Percent);
}

void Test_AgentKitHealthClampHandlesNegativeMaximum(FUnitTest& T)
{
    FAgentKitHealthState State;
    State.Current = 10.0;
    State.Maximum = -1.0;

    AgentKitHealth::Clamp(State);

    T.AssertEquals(0.0, State.Maximum);
    T.AssertEquals(0.0, State.Current);
}
