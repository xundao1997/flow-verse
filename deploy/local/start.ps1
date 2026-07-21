[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("preflight", "api", "worker", "worker-check", "web", "all")]
    [string]$Mode = "all"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$launcher = Join-Path $repositoryRoot "scripts\start-local.ps1"

if (-not (Test-Path -LiteralPath $launcher -PathType Leaf)) {
    throw "FlowVerse local launcher is missing: $launcher"
}

Write-Output "FlowVerse local test deployment: $Mode"
& powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File $launcher $Mode
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
