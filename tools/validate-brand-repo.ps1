param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$factoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$brandRoot = [System.IO.Path]::GetFullPath($Path)
$errors = New-Object System.Collections.Generic.List[string]

function Add-ValidationError {
    param([Parameter(Mandatory = $true)][string]$Message)
    $errors.Add($Message)
}

function Test-RequiredFile {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    $fullPath = Join-Path $brandRoot $RelativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        Add-ValidationError "Missing required file: $RelativePath"
    }
}

function Test-RequiredDirectory {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    $fullPath = Join-Path $brandRoot $RelativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
        Add-ValidationError "Missing required directory: $RelativePath"
    }
}

if (-not (Test-Path -LiteralPath $brandRoot -PathType Container)) {
    throw "Brand repo path does not exist: $brandRoot"
}

$requiredFiles = @(
    "README.md",
    "brand-manifest.yaml",
    "brand/brand-setting.md",
    "brand/brand-positioning.md",
    "brand/brand-production-brief.md",
    "brand/brand-system-prompt.md",
    "market/market-observation-log.md",
    "market/category-gap-map.md",
    "releases/release-001/release-spec.md",
    "releases/release-001/production-handoff.md",
    "releases/release-001/release-log.md",
    "releases/release-001/qa/release-checklist.md",
    "releases/release-001/qa/quality-ledger.md",
    "releases/release-001/qa/usage-validation.md",
    "releases/release-001/qa/release-retrospective.md",
    "releases/release-001/submission/metadata.yaml",
    "releases/release-001/submission/submission-checklist.md",
    "releases/release-001/submission/submission-audit-report.md",
    "releases/release-001/submission/package-report.md",
    "references/shared/line-platform-baseline.md",
    "references/shared/structure-constraints.md",
    "references/shared/emoji-product-rules.md",
    "references/shared/review-risk-rules.md",
    "references/shared/evaluation-model.md",
    "references/shared/quality-control-workflow.md",
    "references/shared/usage-validation-workflow.md",
    "tools/validate-assets.py",
    "tools/validate-metadata.py",
    "tools/package-release.py",
    "tools/check-placeholders.py",
    "tools/validate-manifest-paths.py"
)

foreach ($file in $requiredFiles) {
    Test-RequiredFile $file
}

$requiredDirs = @(
    "releases/release-001/prompts",
    "releases/release-001/production/rough-boards",
    "releases/release-001/production/finals",
    "releases/release-001/submission/images"
)

foreach ($dir in $requiredDirs) {
    Test-RequiredDirectory $dir
}

$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) {
    Add-ValidationError "python was not found in PATH"
} else {
    $schemaTool = Join-Path $factoryRoot "tools/validate-schemas.py"
    $manifestSchema = Join-Path $factoryRoot "schemas/brand-manifest.schema.json"
    $manifest = Join-Path $brandRoot "brand-manifest.yaml"
    if (Test-Path -LiteralPath $manifest) {
        & python $schemaTool --schema $manifestSchema --data $manifest
        if ($LASTEXITCODE -ne 0) {
            Add-ValidationError "brand-manifest.yaml failed schema validation"
        }
    }

    $manifestPathTool = Join-Path $factoryRoot "tools/validate-manifest-paths.py"
    & python $manifestPathTool $brandRoot
    if ($LASTEXITCODE -ne 0) {
        Add-ValidationError "brand-manifest.yaml contains missing path references"
    }

    $metadataTool = Join-Path $factoryRoot "tools/validate-metadata.py"
    $metadata = Join-Path $brandRoot "releases/release-001/submission/metadata.yaml"
    if (Test-Path -LiteralPath $metadata) {
        & python $metadataTool $metadata
        if ($LASTEXITCODE -ne 0) {
            Add-ValidationError "submission metadata failed validation"
        }
    }

    $placeholderTool = Join-Path $factoryRoot "tools/check-placeholders.py"
    & python $placeholderTool $brandRoot
    if ($LASTEXITCODE -ne 0) {
        Add-ValidationError "unresolved placeholder check failed"
    }
}

if ($errors.Count -gt 0) {
    foreach ($errorItem in $errors) {
        [Console]::Error.WriteLine($errorItem)
    }
    exit 1
}

Write-Host "brand repo validation passed: $brandRoot"
