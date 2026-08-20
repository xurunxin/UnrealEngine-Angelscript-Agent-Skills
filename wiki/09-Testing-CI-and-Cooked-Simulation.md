# 09. 测试、CI 与 Cook 模拟

## 单元测试

```angelscript
void Test_InventoryRejectsOverflow(FUnitTest& T)
{
    FInventoryState State;
    State.Capacity = 2;

    T.AssertTrue(Inventory::TryAdd(State, n"Potion"));
    T.AssertTrue(Inventory::TryAdd(State, n"Key"));
    T.AssertFalse(Inventory::TryAdd(State, n"Coin"));
}
```

单元测试适合：

- 纯规则；
- Struct 转换；
- 状态机；
- 权限判断；
- UI ViewModel；
- 序列化前校验。

## 集成测试

```angelscript
void IntegrationTest_InteractReplicates(FIntegrationTest& T)
{
    // 目标项目 API 驱动步骤和等待条件
}
```

地图默认命名同测试。可用 GetMapName 函数复用其他地图。测试框架支持 latent steps；目标 API 以项目版本为准。

## 命令行

示意：

```powershell
& "$Editor\UnrealEditor-Cmd.exe" "$Project" `
  -unattended -nop4 -nosplash `
  -ExecCmds="Automation RunTests Angelscript.UnitTests;Quit" `
  -TestExit="Automation Test Queue Empty"
```

实际 Test 名称、ReportExportPath 和退出参数从目标引擎 Automation 帮助确认。

## simulate-cooked

```powershell
& "$Editor\UnrealEditor-Cmd.exe" "$Project" `
  -unattended -nop4 -nosplash `
  -as-simulate-cooked `
  -run=AngelscriptTest
```

它验证脚本在移除 Editor-only API 后可编译，不生成完整包。

## 覆盖率

`-as-enable-code-coverage` 或项目设置。报告写 `Saved/CodeCoverage`，每次测试运行可能覆盖。保留 CI Artifact。

## CI 建议

```text
ueas-compile-unit
ueas-simulate-cooked
ueas-integration
cpp-build
cook-smoke
package-launch
```

失败时上传：

- Saved/Logs；
- Automation Report；
- CodeCoverage；
- 版本锁；
- Command line；
- Crash/ensure 信息。

## 快速反馈

本地保存自动跑 UnitTests。CI 再跑完整集合。不要让每次保存启动昂贵 Integration/Cook。

## 非确定性

禁止依赖固定长 Sleep。使用条件等待、明确超时和诊断状态。多人测试记录每个 World/Client 的日志前缀。
