[CmdletBinding()]
param(
    [string]$Owner = "xurunxin",
    [string]$RepositoryName = "UnrealEngine-Angelscript-Agent-Skills",
    [ValidateSet("private", "public", "internal")]
    [string]$Visibility = "private",
    [string]$Description = "Agent Skills and Wiki for UnrealEngine-Angelscript and EmmsUI development."
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not on PATH."
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or is not on PATH."
}

gh auth status 1>$null

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    if (-not (Test-Path ".git")) {
        throw "The repository metadata is missing: $Root/.git"
    }

    $Status = git status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect Git status."
    }
    if ($Status) {
        throw "The working tree is not clean. Commit or stash changes before publishing."
    }

    $FullName = "$Owner/$RepositoryName"
    gh repo view $FullName 1>$null 2>$null
    $Exists = $LASTEXITCODE -eq 0

    if (-not $Exists) {
        $VisibilityFlag = "--$Visibility"
        gh repo create $FullName $VisibilityFlag --description $Description --source . --remote origin
        if ($LASTEXITCODE -ne 0) {
            throw "GitHub repository creation failed."
        }
    }
    elseif (-not (git remote get-url origin 2>$null)) {
        git remote add origin "https://github.com/$FullName.git"
    }

    git push -u origin main
    if ($LASTEXITCODE -ne 0) {
        throw "Pushing main failed."
    }

    Write-Host "Published: https://github.com/$FullName"
}
finally {
    Pop-Location
}
