void Test_AgentKitRangeMixin(FUnitTest& T)
{
    FAgentKitRange Range;
    Range.Minimum = 10.0;
    Range.Maximum = 20.0;

    T.AssertTrue(Range.Contains(15.0));
    T.AssertFalse(Range.Contains(25.0));
    T.AssertEquals(10.0, Range.Size());
}
