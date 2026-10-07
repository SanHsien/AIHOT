[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$pythonExe = (Get-Command python -ErrorAction Stop).Source
$nodeExe = (Get-Command node -ErrorAction Stop).Source
$npmCmd = (Get-Command npm.cmd -ErrorAction Stop).Source

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Invoke-Step {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [string]$Exe,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "==> $Label" -ForegroundColor Cyan
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

Write-Host "Starting AIHOT Dev Check Gate..." -ForegroundColor Green

# 1. Environment Verification
Invoke-Step -Label "Environment verification" -Exe $pythonExe -Arguments @("scripts/verify-env.py")

# 2. TypeScript Typecheck
Invoke-Step -Label "TypeScript typecheck" -Exe $npmCmd -Arguments @("run", "typecheck")

# 3. Web Client & SSR Build
Invoke-Step -Label "Web SSR build" -Exe $npmCmd -Arguments @("run", "build", "-w", "@aihot/web")

# 4. Web Unit Tests
$webTests = Get-ChildItem -Path "apps/web/tests/*.test.ts" | ForEach-Object { $_.FullName }
Invoke-Step -Label "Web tests" -Exe $nodeExe -Arguments (@("--test") + $webTests)

# 5. Upstream Divergence Check
Invoke-Step -Label "Upstream divergence check" -Exe $pythonExe -Arguments @("tools/check_divergence.py")

# 6. Fork Divergence Contract Tests
Invoke-Step -Label "Fork divergence tests" -Exe $pythonExe -Arguments @("tests/test_fork_divergence.py")

Write-Host "`nAll checks passed successfully! Ready to push to main." -ForegroundColor Green
