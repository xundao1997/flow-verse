[CmdletBinding()]
param(
    [ValidateRange(1, 65535)]
    [int]$PostgresLocalPort = 15432,

    [ValidateRange(1, 65535)]
    [int]$RedisLocalPort = 16379,

    [ValidateRange(1, 65535)]
    [int]$MinioApiLocalPort = 19000,

    [ValidatePattern("^[A-Za-z_][A-Za-z0-9_-]*$")]
    [string]$PostgresUser = "flowverse",

    [ValidatePattern("^[A-Za-z_][A-Za-z0-9_-]*$")]
    [string]$PostgresDatabase = "flowverse"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$examplePath = Join-Path $repositoryRoot ".env.example"
$environmentPath = Join-Path $repositoryRoot ".env"
$startScript = Join-Path $PSScriptRoot "start.ps1"

function Read-ConfirmedSecret {
    param([Parameter(Mandatory)][string]$Label)

    $firstSecure = Read-Host "Enter $Label" -AsSecureString
    $secondSecure = Read-Host "Confirm $Label" -AsSecureString
    $first = ([PSCredential]::new("value", $firstSecure)).GetNetworkCredential().Password
    $second = ([PSCredential]::new("value", $secondSecure)).GetNetworkCredential().Password
    if ([string]::IsNullOrWhiteSpace($first)) {
        throw "$Label cannot be empty."
    }
    if ($first -ne $second) {
        throw "$Label values do not match."
    }
    if ($first -ne $first.Trim()) {
        throw "$Label cannot start or end with whitespace."
    }
    return $first
}

function Write-EnvironmentValues {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][System.Collections.IDictionary]$Values
    )

    $sourcePath = if (Test-Path -LiteralPath $Path -PathType Leaf) {
        $Path
    }
    else {
        $examplePath
    }
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Environment source is missing: $sourcePath"
    }

    $lines = [System.Collections.Generic.List[string]]::new()
    foreach ($line in [IO.File]::ReadAllLines($sourcePath)) {
        $lines.Add($line)
    }
    $remaining = [System.Collections.Generic.HashSet[string]]::new(
        [string[]]$Values.Keys,
        [StringComparer]::Ordinal
    )
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^([A-Za-z_][A-Za-z0-9_]*)=") {
            $name = $Matches[1]
            if ($Values.Contains($name)) {
                $lines[$index] = "${name}=$($Values[$name])"
                $null = $remaining.Remove($name)
            }
        }
    }
    if ($remaining.Count -gt 0) {
        $lines.Add("")
        foreach ($name in $Values.Keys) {
            if ($remaining.Contains([string]$name)) {
                $lines.Add("${name}=$($Values[$name])")
            }
        }
    }

    [IO.File]::WriteAllLines($Path, $lines, [Text.UTF8Encoding]::new($false))
}

$postgresPassword = Read-ConfirmedSecret "PostgreSQL password"
$redisPassword = Read-ConfirmedSecret "Redis password"
$minioAccessKey = Read-Host "Enter MinIO root user"
if ([string]::IsNullOrWhiteSpace($minioAccessKey)) {
    throw "MinIO root user cannot be empty."
}
$minioSecretKey = Read-ConfirmedSecret "MinIO root password"

$escapedPostgresUser = [Uri]::EscapeDataString($PostgresUser)
$escapedPostgresPassword = [Uri]::EscapeDataString($postgresPassword)
$escapedPostgresDatabase = [Uri]::EscapeDataString($PostgresDatabase)
$values = [ordered]@{
    FLOWVERSE_DATABASE_URL = "postgresql+psycopg://${escapedPostgresUser}:${escapedPostgresPassword}@127.0.0.1:${PostgresLocalPort}/${escapedPostgresDatabase}"
    FLOWVERSE_REDIS_HOST = "127.0.0.1"
    FLOWVERSE_REDIS_PORT = $RedisLocalPort.ToString()
    FLOWVERSE_REDIS_PASSWORD = $redisPassword
    FLOWVERSE_MINIO_ENDPOINT = "http://127.0.0.1:${MinioApiLocalPort}"
    FLOWVERSE_MINIO_ACCESS_KEY = $minioAccessKey
    FLOWVERSE_MINIO_SECRET_KEY = $minioSecretKey
    FLOWVERSE_MINIO_REGION = "us-east-1"
    FLOWVERSE_MIDDLEWARE_PROBE_TIMEOUT_SECONDS = "3"
}

Write-EnvironmentValues -Path $environmentPath -Values $values
$postgresPassword = $null
$redisPassword = $null
$minioSecretKey = $null
$values = $null

Write-Output "Local middleware settings were written to the ignored root .env file."
Write-Output "Running authenticated PostgreSQL, Redis and MinIO checks..."
& powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File $startScript middleware-check
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
