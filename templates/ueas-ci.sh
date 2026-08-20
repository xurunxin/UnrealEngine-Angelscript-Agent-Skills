#!/usr/bin/env bash
set -euo pipefail

EDITOR_CMD="${EDITOR_CMD:?Set EDITOR_CMD to UnrealEditor-Cmd}"
PROJECT="${PROJECT:?Set PROJECT to .uproject}"
MODE="${MODE:-all}"
REPORT_ROOT="${REPORT_ROOT:-Saved/TestReports}"

mkdir -p "$REPORT_ROOT"

common=(
  "$PROJECT"
  -unattended
  -nop4
  -nosplash
  -NoSound
  -NullRHI
)

run_unit() {
  "$EDITOR_CMD" "${common[@]}" \
    "-ExecCmds=Automation RunTests Angelscript.UnitTests;Quit" \
    "-TestExit=Automation Test Queue Empty" \
    "-ReportExportPath=$REPORT_ROOT/Unit"
}

run_simulate_cooked() {
  "$EDITOR_CMD" "${common[@]}" \
    -as-simulate-cooked \
    -run=AngelscriptTest
}

run_integration() {
  "$EDITOR_CMD" "${common[@]}" \
    "-ExecCmds=Automation RunTests Angelscript.IntegrationTests;Quit" \
    "-TestExit=Automation Test Queue Empty" \
    "-ReportExportPath=$REPORT_ROOT/Integration"
}

case "${MODE,,}" in
  unit) run_unit ;;
  simulate-cooked) run_simulate_cooked ;;
  integration) run_integration ;;
  all)
    run_unit
    run_simulate_cooked
    run_integration
    ;;
  *)
    echo "Unknown MODE: $MODE" >&2
    exit 2
    ;;
esac
