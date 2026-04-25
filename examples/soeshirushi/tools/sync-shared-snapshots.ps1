param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$BrandRepo
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$factoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$brandRoot = [System.IO.Path]::GetFullPath($BrandRepo)
$targetRoot = Join-Path $brandRoot "references/shared"

if (-not (Test-Path -LiteralPath $brandRoot -PathType Container)) {
    throw "Brand repo does not exist: $brandRoot"
}

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

$snapshots = @(
    "rules/line-platform-baseline.md",
    "rules/structure-constraints.md",
    "rules/emoji-product-rules.md",
    "rules/review-risk-rules.md",
    "rules/evaluation-model.md",
    "rules/continuous-improvement-rules.md",
    "rules/asset-validation-rules.md",
    "rules/submission-metadata-rules.md",
    "workflows/production-pipeline-workflow.md",
    "workflows/quality-control-workflow.md",
    "workflows/continuous-improvement-workflow.md",
    "workflows/usage-validation-workflow.md",
    "workflows/release-retrospective-workflow.md",
    "workflows/transformation-workflow.md",
    "workflows/submission-audit-workflow.md"
)

foreach ($snapshot in $snapshots) {
    $source = Join-Path $factoryRoot $snapshot
    $target = Join-Path $targetRoot (Split-Path -Leaf $snapshot)
    Copy-Item -LiteralPath $source -Destination $target -Force
}

Write-Host "shared snapshots synced to $targetRoot"
