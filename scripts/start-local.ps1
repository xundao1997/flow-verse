[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("preflight", "api", "worker", "worker-check", "middleware-check", "web", "all")]
    [string]$Service = "preflight"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ApiRoot = Join-Path $RepositoryRoot "services\api"
$WorkerRoot = Join-Path $RepositoryRoot "services\worker"
$WebRoot = Join-Path $RepositoryRoot "services\web"
$TechStackPath = Join-Path $RepositoryRoot "docs\engineering\TECH_STACK.md"
$UvicornLauncher = Join-Path $PSScriptRoot "run_uvicorn.py"

function Import-FlowVerseEnvironment {
    $environmentPath = Join-Path $RepositoryRoot ".env"
    if (-not (Test-Path -LiteralPath $environmentPath -PathType Leaf)) {
        return
    }

    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $environmentPath) {
        $lineNumber++
        $trimmed = $line.Trim()
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith("#")) {
            continue
        }

        $parts = $trimmed.Split("=", 2)
        if ($parts.Count -ne 2 -or $parts[0] -notmatch "^[A-Za-z_][A-Za-z0-9_]*$") {
            throw "Invalid .env entry at line $lineNumber. Expected NAME=value."
        }

        $name = $parts[0]
        if ($null -eq [Environment]::GetEnvironmentVariable($name, "Process")) {
            [Environment]::SetEnvironmentVariable($name, $parts[1], "Process")
        }
    }
}

function Get-EnvironmentValue {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Default
    )

    $value = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }
    return $value
}

function Require-File {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Recovery
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file is missing: $Path`n$Recovery"
    }
}

function Get-StatusLabel {
    param([Parameter(Mandatory)][string]$Path)
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        return "ready"
    }
    return "missing"
}

function Get-DirectoryStatusLabel {
    param([Parameter(Mandatory)][string]$Path)
    if (Test-Path -LiteralPath $Path -PathType Container) {
        return "ready"
    }
    return "missing"
}

function Require-WebRuntime {
    Require-File (Join-Path $WebRoot "pnpm-lock.yaml") "Run the confirmed Web install command in $TechStackPath."
    if (-not (Test-Path -LiteralPath (Join-Path $WebRoot "src") -PathType Container)) {
        throw "Web source is missing under $WebRoot."
    }

    $corepack = Get-Command "corepack" -ErrorAction SilentlyContinue
    if ($null -eq $corepack) {
        throw "corepack is unavailable. Install the confirmed Node.js runtime from $TechStackPath."
    }
    return $corepack.Source
}

function Show-Preflight {
    $apiExecutable = Join-Path $ApiRoot ".venv\Scripts\python.exe"
    $workerExecutable = Join-Path $WorkerRoot ".venv\Scripts\python.exe"
    $webLock = Join-Path $WebRoot "pnpm-lock.yaml"
    $webSource = Join-Path $WebRoot "src"
    $environmentPath = Join-Path $RepositoryRoot ".env"
    $nodeCommand = Get-Command "node" -ErrorAction SilentlyContinue
    $nodeVersion = if ($null -eq $nodeCommand) { "missing" } else { (& $nodeCommand.Source "--version") }

    Write-Output "FlowVerse native local preflight"
    Write-Output "  .env:           $(Get-StatusLabel $environmentPath)"
    Write-Output "  API runtime:    $(Get-StatusLabel $apiExecutable)"
    Write-Output "  Worker runtime: $(Get-StatusLabel $workerExecutable)"
    Write-Output "  ASGI launcher:  $(Get-StatusLabel $UvicornLauncher)"
    Write-Output "  Web lockfile:   $(Get-StatusLabel $webLock)"
    Write-Output "  Web source:     $(Get-DirectoryStatusLabel $webSource)"
    Write-Output "  Node runtime:   $nodeVersion (required: v24.17.0)"
    Write-Output "  Docker:         not used for local startup"
}

function Start-ApiForeground {
    $apiExecutable = Join-Path $ApiRoot ".venv\Scripts\python.exe"
    Require-File $apiExecutable "Run: uv sync --project services/api --python 3.13.14"
    Require-File $UvicornLauncher "Restore the FlowVerse local Uvicorn launcher."
    $hostName = Get-EnvironmentValue "FLOWVERSE_API_HOST" "127.0.0.1"
    $port = Get-EnvironmentValue "FLOWVERSE_API_PORT" "8000"
    Push-Location $ApiRoot
    try {
        & $apiExecutable $UvicornLauncher "flowverse_api.api.main:app" "--app-dir" "src" "--host" $hostName "--port" $port
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    finally {
        Pop-Location
    }
}

function Start-WorkerForeground {
    $workerExecutable = Join-Path $WorkerRoot ".venv\Scripts\python.exe"
    Require-File $workerExecutable "Run: uv sync --project services/worker --python 3.13.14"
    Require-File $UvicornLauncher "Restore the FlowVerse local Uvicorn launcher."
    $hostName = Get-EnvironmentValue "FLOWVERSE_WORKER_HOST" "127.0.0.1"
    $port = Get-EnvironmentValue "FLOWVERSE_WORKER_PORT" "8001"
    Push-Location $WorkerRoot
    try {
        & $workerExecutable $UvicornLauncher "flowverse_worker.api.main:app" "--app-dir" "src" "--host" $hostName "--port" $port
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    finally {
        Pop-Location
    }
}

function Start-MiddlewareCheck {
    $apiExecutable = Join-Path $ApiRoot ".venv\Scripts\python.exe"
    Require-File $apiExecutable "Run: uv sync --project services/api --python 3.13.14"
    Push-Location (Join-Path $ApiRoot "src")
    try {
        & $apiExecutable "-m" "flowverse_api.health.middleware_check"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    finally {
        Pop-Location
    }
}

function Start-WebForeground {
    $corepack = Require-WebRuntime
    $hostName = Get-EnvironmentValue "FLOWVERSE_WEB_HOST" "127.0.0.1"
    $port = Get-EnvironmentValue "FLOWVERSE_WEB_PORT" "5173"
    & $corepack "pnpm@11.10.0" "--dir" $WebRoot "run" "dev" "--host" $hostName "--port" $port
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Start-HiddenService {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Executable,
        [Parameter(Mandatory)][string]$WorkingDirectory,
        [Parameter(Mandatory)][string[]]$Arguments,
        [Parameter(Mandatory)][string]$LogRoot
    )

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $Executable
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.Arguments = (($Arguments | ForEach-Object {
        '"{0}"' -f $_.Replace('"', '\"')
    }) -join " ")
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    if (-not $process.Start()) {
        throw "Unable to start $Name."
    }
    $process | Add-Member NoteProperty FlowVerseName $Name
    $process | Add-Member NoteProperty FlowVerseLogRoot $LogRoot
    $process | Add-Member NoteProperty FlowVerseStdout ($process.StandardOutput.ReadToEndAsync())
    $process | Add-Member NoteProperty FlowVerseStderr ($process.StandardError.ReadToEndAsync())
    $process | Add-Member NoteProperty FlowVerseLogsWritten $false
    return $process
}

function Write-ServiceLogs {
    param([Parameter(Mandatory)][System.Diagnostics.Process]$Process)
    if ($Process.FlowVerseLogsWritten -or -not $Process.HasExited) {
        return
    }
    [IO.File]::WriteAllText(
        (Join-Path $Process.FlowVerseLogRoot "$($Process.FlowVerseName).out.log"),
        $Process.FlowVerseStdout.GetAwaiter().GetResult()
    )
    [IO.File]::WriteAllText(
        (Join-Path $Process.FlowVerseLogRoot "$($Process.FlowVerseName).err.log"),
        $Process.FlowVerseStderr.GetAwaiter().GetResult()
    )
    $Process.FlowVerseLogsWritten = $true
}

function Wait-ServiceHealth {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Uri,
        [Parameter(Mandatory)][System.Diagnostics.Process]$Process,
        [Parameter(Mandatory)][string]$LogRoot
    )

    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    while ([DateTime]::UtcNow -lt $deadline) {
        if ($Process.HasExited) {
            Write-ServiceLogs $Process
            throw "$Name exited before becoming healthy. Inspect logs in $LogRoot."
        }
        try {
            $response = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) { return }
        }
        catch {
            Start-Sleep -Milliseconds 500
        }
    }
    throw "$Name did not become healthy within 30 seconds. Inspect logs in $LogRoot."
}

function Start-AllServices {
    $apiExecutable = Join-Path $ApiRoot ".venv\Scripts\python.exe"
    $workerExecutable = Join-Path $WorkerRoot ".venv\Scripts\python.exe"
    Require-File $apiExecutable "Run: uv sync --project services/api --python 3.13.14"
    Require-File $workerExecutable "Run: uv sync --project services/worker --python 3.13.14"
    Require-File $UvicornLauncher "Restore the FlowVerse local Uvicorn launcher."
    $null = Require-WebRuntime

    $apiHost = Get-EnvironmentValue "FLOWVERSE_API_HOST" "127.0.0.1"
    $apiPort = Get-EnvironmentValue "FLOWVERSE_API_PORT" "8000"
    $workerHost = Get-EnvironmentValue "FLOWVERSE_WORKER_HOST" "127.0.0.1"
    $workerPort = Get-EnvironmentValue "FLOWVERSE_WORKER_PORT" "8001"
    $logRoot = Join-Path $env:TEMP "flowverse-local-$PID"
    New-Item -ItemType Directory -Force $logRoot | Out-Null
    $processes = [System.Collections.Generic.List[System.Diagnostics.Process]]::new()

    try {
        $worker = Start-HiddenService `
            "worker" $workerExecutable $WorkerRoot `
            @($UvicornLauncher, "flowverse_worker.api.main:app", "--app-dir", "src", "--host", $workerHost, "--port", $workerPort) `
            $logRoot
        $processes.Add($worker)
        Wait-ServiceHealth "Worker" "http://${workerHost}:${workerPort}/health/live" $worker $logRoot

        $api = Start-HiddenService `
            "api" $apiExecutable $ApiRoot `
            @($UvicornLauncher, "flowverse_api.api.main:app", "--app-dir", "src", "--host", $apiHost, "--port", $apiPort) `
            $logRoot
        $processes.Add($api)
        Wait-ServiceHealth "API" "http://${apiHost}:${apiPort}/health/live" $api $logRoot

        Write-Output "API and Worker are healthy. Starting Web in the foreground."
        Write-Output "Open: http://$(Get-EnvironmentValue 'FLOWVERSE_WEB_HOST' '127.0.0.1'):$(Get-EnvironmentValue 'FLOWVERSE_WEB_PORT' '5173')"
        Write-Output "Local service logs: $logRoot"
        Start-WebForeground
    }
    finally {
        foreach ($process in $processes) {
            if (-not $process.HasExited) {
                Stop-Process -Id $process.Id -Force
                $process.WaitForExit()
            }
            Write-ServiceLogs $process
            $process.Dispose()
        }
    }
}

Import-FlowVerseEnvironment

switch ($Service) {
    "preflight" { Show-Preflight }
    "api" { Start-ApiForeground }
    "worker" { Start-WorkerForeground }
    "worker-check" {
        $workerExecutable = Join-Path $WorkerRoot ".venv\Scripts\python.exe"
        Require-File $workerExecutable "Run: uv sync --project services/worker --python 3.13.14"
        Push-Location (Join-Path $WorkerRoot "src")
        try {
            & $workerExecutable "-m" "flowverse_worker" "--check"
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
        finally {
            Pop-Location
        }
    }
    "middleware-check" { Start-MiddlewareCheck }
    "web" { Start-WebForeground }
    "all" { Start-AllServices }
}
