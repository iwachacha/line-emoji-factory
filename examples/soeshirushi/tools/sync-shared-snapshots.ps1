param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$BrandRepo,

    [string]$FactoryRoot = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-FactoryRoot {
    param([string]$RequestedRoot)

    if ($RequestedRoot) {
        $resolved = (Resolve-Path $RequestedRoot).Path
    } else {
        $resolved = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    }

    if (
        -not (Test-Path -LiteralPath (Join-Path $resolved "rules") -PathType Container) -or
        -not (Test-Path -LiteralPath (Join-Path $resolved "workflows") -PathType Container)
    ) {
        throw "FactoryRoot must point to line-emoji-factory. Pass -FactoryRoot <path-to-factory> when running from a brand repo copy."
    }

    return $resolved
}

function Read-SnapshotTargets {
    param([Parameter(Mandatory = $true)][string]$ManifestPath)

    $targets = @()
    $inSnapshots = $false
    foreach ($line in [System.IO.File]::ReadLines($ManifestPath, [System.Text.Encoding]::UTF8)) {
        if ($line -match '^snapshots:\s*$') {
            $inSnapshots = $true
            continue
        }

        if (-not $inSnapshots) {
            continue
        }

        if ($line -match '^\S') {
            break
        }

        if ($line -match '^\s{2}[A-Za-z0-9_]+:\s*["'']?([^"'']+)["'']?\s*$') {
            $targets += $Matches[1].Trim()
        }
    }

    if ($targets.Count -eq 0) {
        throw "No snapshots listed in $ManifestPath"
    }

    return $targets
}

function Resolve-SnapshotSource {
    param(
        [Parameter(Mandatory = $true)][string]$FactoryRoot,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    $leaf = Split-Path -Leaf $TargetPath
    foreach ($dir in @("rules", "workflows")) {
        $candidate = Join-Path $FactoryRoot (Join-Path $dir $leaf)
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return $candidate
        }
    }

    throw "Snapshot source not found for $TargetPath"
}

$factoryRootPath = Resolve-FactoryRoot -RequestedRoot $FactoryRoot
$brandRoot = [System.IO.Path]::GetFullPath($BrandRepo)
$manifestPath = Join-Path $brandRoot "brand-manifest.yaml"

if (-not (Test-Path -LiteralPath $brandRoot -PathType Container)) {
    throw "Brand repo does not exist: $brandRoot"
}

if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Brand manifest does not exist: $manifestPath"
}

foreach ($targetRel in Read-SnapshotTargets -ManifestPath $manifestPath) {
    $source = Resolve-SnapshotSource -FactoryRoot $factoryRootPath -TargetPath $targetRel
    $target = Join-Path $brandRoot $targetRel
    $targetDir = Split-Path -Parent $target
    if ($targetDir -and -not (Test-Path -LiteralPath $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    Copy-Item -LiteralPath $source -Destination $target -Force
}

Write-Host "shared snapshots synced from $factoryRootPath to $brandRoot"
