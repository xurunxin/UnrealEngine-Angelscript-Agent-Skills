# Command Cheat Sheet

所有路径与 Automation 名称按目标引擎调整。

## Script compile / simulate cooked

```powershell
$Editor = "D:\UE-AS\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$Project = "D:\Game\Game.uproject"

& $Editor $Project `
  -unattended -nop4 -nosplash `
  -as-simulate-cooked `
  -run=AngelscriptTest
```

## Unit tests

```powershell
& $Editor $Project `
  -unattended -nop4 -nosplash `
  -ExecCmds="Automation RunTests Angelscript.UnitTests;Quit" `
  -TestExit="Automation Test Queue Empty" `
  -ReportExportPath="$PWD\Saved\TestReports\UEAS-Unit"
```

## Integration tests

```powershell
& $Editor $Project `
  -unattended -nop4 -nosplash `
  -ExecCmds="Automation RunTests Angelscript.IntegrationTests;Quit" `
  -TestExit="Automation Test Queue Empty" `
  -ReportExportPath="$PWD\Saved\TestReports\UEAS-Integration"
```

## Coverage

```text
-as-enable-code-coverage
```

报告通常在 `Saved/CodeCoverage`.

## Generate precompiled data

```powershell
& "<PackagedGame>.exe" -as-generate-precompiled-data
```

产物与路径以目标版本日志为准，通常包括：

```text
<Project>/Script/PrecompiledScript.Cache
AS_JITTED_CODE/
```

## Development bypass cache

```text
-as-development-mode
```

## Open workspace

Editor Tools 菜单选择 “Open Angelscript workspace”，或 VS Code 打开 `<Project>/Script`.

## Kit validation

```bash
python tools/validate_kit.py .
```

## Compatibility probe

```bash
python tools/probe_compatibility.py \
  --engine-root D:/UE-AS \
  --emmsui-root D:/Game/Plugins/EmmsUI \
  --project-root D:/Game \
  --json-out Saved/ueas-compat.json
```
