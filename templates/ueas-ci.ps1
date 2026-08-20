[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$EditorCmd,

    [Parameter(Mandatory)]
    [string]$Project,

    [ValidateSet("Unit", "Integration", "SimulateCooked", "All")]
    [string]$Mode = "All",

    [string]$ReportRoot = "$PSScriptRoot/../Saved/TestReports"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Unreal {
    param(
        [Parameter(Mandatory)]
        [string[]]$Arguments,
        [Parameter(Mandatory)]
        [string]$Name
    )

    Write-Host "==> $Name"
    Write-Host "$EditorCmd $($Arguments -join ' ')"

    & $EditorCmd @Arguments
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        throw "$Name failed with exit code $exitCode"
    }
}

if (-not (Test-Path -LiteralPath $EditorCmd)) {
    throw "UnrealEditor-Cmd not found: $EditorCmd"
}
if (-not (Test-Path -LiteralPath $Project)) {
    throw "Project not found: $Project"
}

New-Item -ItemType Directory -Force -Path $ReportRoot | Out-Null

$common = @(
    $Project,
    "-unattended",
    "-nop4",
    "-nosplash",
    "-NoSound",
    "-NullRHI"
)

if ($Mode -in @("Unit", "All")) {
    Invoke-Unreal -Name "UE-AS Unit Tests" -Arguments ($common + @(
        "-ExecCmds=Automation RunTests Angelscript.UnitTests;Quit",
        "-TestExit=Automation Test Queue Empty",
        "-ReportExportPath=$ReportRoot/Unit"
    ))
}

if ($Mode -in @("SimulateCooked", "All")) {
    Invoke-Unreal -Name "UE-AS Simulate Cooked" -Arguments ($common + @(
        "-as-simulate-cooked",
        "-run=AngelscriptTest"
    ))
}

if ($Mode -in @("Integration", "All")) {
    Invoke-Unreal -Name "UE-AS Integration Tests" -Arguments ($common + @(
        "-ExecCmds=Automation RunTests Angelscript.IntegrationTests;Quit",
        "-TestExit=Automation Test Queue Empty",
        "-ReportExportPath=$ReportRoot/Integration"
    ))
}

Write-Host "All requested UE-AS checks passed."
