[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern("^[A-Za-z0-9][A-Za-z0-9.-]*$")]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [ValidatePattern("^[A-Za-z0-9._-]+$")]
    [string]$SshUser,

    [ValidateRange(1, 65535)]
    [int]$SshPort = 22,

    [ValidateRange(1, 65535)]
    [int]$PostgresLocalPort = 15432,

    [ValidateRange(1, 65535)]
    [int]$RedisLocalPort = 16379,

    [ValidateRange(1, 65535)]
    [int]$MinioApiLocalPort = 19000,

    [ValidateRange(1, 65535)]
    [int]$MinioConsoleLocalPort = 19001,

    [string]$IdentityFile,

    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$localPorts = @(
    $PostgresLocalPort,
    $RedisLocalPort,
    $MinioApiLocalPort,
    $MinioConsoleLocalPort
)

if (($localPorts | Select-Object -Unique).Count -ne $localPorts.Count) {
    throw "Local tunnel ports must be unique."
}

$sshCommand = Get-Command "ssh.exe" -ErrorAction SilentlyContinue
if ($null -eq $sshCommand) {
    $sshCommand = Get-Command "ssh" -ErrorAction SilentlyContinue
}
if ($null -eq $sshCommand) {
    throw "Windows OpenSSH client was not found. Install the OpenSSH Client optional feature."
}

$sshArguments = @(
    "-N",
    "-o", "ExitOnForwardFailure=yes",
    "-o", "ConnectTimeout=10",
    "-o", "ServerAliveInterval=30",
    "-o", "ServerAliveCountMax=3",
    "-p", $SshPort.ToString()
)

if (-not [string]::IsNullOrWhiteSpace($IdentityFile)) {
    if (-not (Test-Path -LiteralPath $IdentityFile -PathType Leaf)) {
        throw "SSH identity file was not found: $IdentityFile"
    }
    $resolvedIdentityFile = (Resolve-Path -LiteralPath $IdentityFile).Path
    $sshArguments += @("-i", $resolvedIdentityFile)
}

$sshArguments += @(
    "-L", "127.0.0.1:${PostgresLocalPort}:127.0.0.1:5432",
    "-L", "127.0.0.1:${RedisLocalPort}:127.0.0.1:6379",
    "-L", "127.0.0.1:${MinioApiLocalPort}:127.0.0.1:9000",
    "-L", "127.0.0.1:${MinioConsoleLocalPort}:127.0.0.1:9001"
)

Write-Output "FlowVerse local-only middleware SSH tunnel"
Write-Output "  PostgreSQL:   127.0.0.1:${PostgresLocalPort} -> server 127.0.0.1:5432"
Write-Output "  Redis:        127.0.0.1:${RedisLocalPort} -> server 127.0.0.1:6379"
Write-Output "  MinIO API:    127.0.0.1:${MinioApiLocalPort} -> server 127.0.0.1:9000"
Write-Output "  MinIO Console:127.0.0.1:${MinioConsoleLocalPort} -> server 127.0.0.1:9001"

if ($ValidateOnly) {
    Write-Output "Tunnel configuration validation passed; no SSH connection was opened."
    exit 0
}

Write-Output "Keep this window open while developing. Press Ctrl+C to close all forwards."
& $sshCommand.Source @sshArguments "${SshUser}@${Server}"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
