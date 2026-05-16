param(
    [switch]$InstallDependencies,
    [switch]$KeepTemp
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("chamanp_wheel_smoke_" + [System.Guid]::NewGuid().ToString("N"))
$venvPath = Join-Path $tempRoot "venv"
$outsideCwd = Join-Path $tempRoot "outside_checkout"

function Invoke-Step {
    param(
        [string]$Label,
        [scriptblock]$Command
    )

    Write-Host "==> $Label"
    & $Command
}

try {
    New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $outsideCwd | Out-Null

    Push-Location $repoRoot
    try {
        Invoke-Step "Build local sdist and wheel" {
            python -m build --no-isolation
        }

        $wheel = Get-ChildItem -Path (Join-Path $repoRoot "dist") -Filter "chamanp-*.whl" |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1

        if (-not $wheel) {
            throw "No CHAMANP wheel found in dist/."
        }

        Write-Host "Wheel: $($wheel.FullName)"
    }
    finally {
        Pop-Location
    }

    Invoke-Step "Create temporary virtual environment outside checkout" {
        python -m venv $venvPath
    }

    $pythonExe = Join-Path $venvPath "Scripts/python.exe"
    $chamanpExe = Join-Path $venvPath "Scripts/chamanp.exe"

    $installArgs = @("-m", "pip", "install")
    if (-not $InstallDependencies) {
        $installArgs += "--no-deps"
    }
    $installArgs += $wheel.FullName

    Invoke-Step "Install wheel" {
        & $pythonExe @installArgs
    }

    Push-Location $outsideCwd
    try {
        Invoke-Step "Check CLI version" {
            & $chamanpExe --version
        }

        Invoke-Step "Check CLI help" {
            & $chamanpExe --help
        }

        Invoke-Step "Check public imports and Pipeline privacy" {
            & $pythonExe -c "from chamanp import ChamanpConfig, ChamanpResult, validate_config, run; import chamanp; print(chamanp.__version__, hasattr(chamanp, 'Pipeline'), chamanp.__all__)"
        }
    }
    finally {
        Pop-Location
    }

    Write-Host "CHAMANP wheel smoke install passed."
}
finally {
    if ($KeepTemp) {
        Write-Host "Temporary smoke directory kept at: $tempRoot"
    }
    elseif (Test-Path $tempRoot) {
        Remove-Item -Recurse -Force $tempRoot
    }
}
