param(
    [Parameter(Mandatory = $true)]
    [string]$BrandSlug,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [string]$BrandName = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Content
    )

    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Read-Utf8File {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Apply-Replacements {
    param(
        [Parameter(Mandatory = $true)][string]$Content,
        [Parameter(Mandatory = $true)][hashtable]$Replacements
    )

    foreach ($key in $Replacements.Keys) {
        $Content = $Content.Replace($key, $Replacements[$key])
    }

    return $Content
}

if ($BrandSlug -notmatch '^[a-z0-9-]+$') {
    throw "BrandSlug must be lowercase hyphen-case."
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$destRoot = [System.IO.Path]::GetFullPath($Destination)

if (Test-Path -LiteralPath $destRoot) {
    throw "Destination already exists: $destRoot"
}

if (-not $BrandName) {
    $parts = ($BrandSlug -split "-") | ForEach-Object {
        if ($_.Length -gt 0) { $_.Substring(0, 1).ToUpper() + $_.Substring(1) } else { $_ }
    }
    $BrandName = ($parts -join " ")
}

$releaseId = "release-001"
$initDate = Get-Date -Format "yyyy-MM-dd"
$copyright = ($BrandSlug -replace "-", " ")

$dirs = @(
    "brand",
    "brand/ip",
    "market",
    "references/shared",
    "releases/$releaseId/prompts",
    "releases/$releaseId/production/rough-boards",
    "releases/$releaseId/production/finals",
    "releases/$releaseId/qa",
    "releases/$releaseId/submission/images",
    "schemas",
    "tools"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path (Join-Path $destRoot $dir) -Force | Out-Null
}

$sharedFiles = @(
    @{ Source = "rules/evaluation-model.md"; Target = "references/shared/evaluation-model.md" },
    @{ Source = "rules/line-platform-baseline.md"; Target = "references/shared/line-platform-baseline.md" },
    @{ Source = "rules/structure-constraints.md"; Target = "references/shared/structure-constraints.md" },
    @{ Source = "rules/emoji-product-rules.md"; Target = "references/shared/emoji-product-rules.md" },
    @{ Source = "rules/review-risk-rules.md"; Target = "references/shared/review-risk-rules.md" },
    @{ Source = "rules/asset-validation-rules.md"; Target = "references/shared/asset-validation-rules.md" },
    @{ Source = "rules/submission-metadata-rules.md"; Target = "references/shared/submission-metadata-rules.md" },
    @{ Source = "workflows/quality-control-workflow.md"; Target = "references/shared/quality-control-workflow.md" },
    @{ Source = "workflows/usage-validation-workflow.md"; Target = "references/shared/usage-validation-workflow.md" },
    @{ Source = "workflows/submission-audit-workflow.md"; Target = "references/shared/submission-audit-workflow.md" }
)

foreach ($item in $sharedFiles) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $item.Source) -Destination (Join-Path $destRoot $item.Target) -Force
}

$schemaFiles = @(
    "schemas/brand-manifest.schema.json",
    "schemas/submission-metadata.schema.json",
    "schemas/release-spec.schema.json",
    "schemas/asset-validation-report.schema.json",
    "schemas/market-observation.schema.json",
    "schemas/production-handoff.schema.json",
    "schemas/quality-ledger.schema.json",
    "schemas/usage-validation.schema.json",
    "schemas/ip-style-bible.schema.json",
    "schemas/reference-asset-register.schema.json"
)

foreach ($schemaPath in $schemaFiles) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $schemaPath) -Destination (Join-Path $destRoot $schemaPath) -Force
}

$toolFiles = @(
    "tools/validate-schemas.py",
    "tools/validate-assets.py",
    "tools/validate-metadata.py",
    "tools/check-placeholders.py",
    "tools/validate-manifest-paths.py",
    "tools/package-release.py",
    "tools/sync-shared-snapshots.ps1"
)

foreach ($toolPath in $toolFiles) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $toolPath) -Destination (Join-Path $destRoot $toolPath) -Force
}

$replacements = @{}
$replacements["your-brand-slug"] = $BrandSlug
$replacements["YOUR_BRAND_NAME"] = $BrandName
$replacements["[BRAND_NAME]"] = $BrandName
$replacements["[BRAND_SLUG]"] = $BrandSlug
$replacements["[INIT_DATE]"] = $initDate
$replacements["[RELEASE_ID]"] = $releaseId
$replacements["[CREATOR_NAME]"] = $BrandName
$replacements["[TITLE]"] = $BrandName
$replacements["[DESCRIPTION]"] = "LINE emoji for $BrandName."
$replacements["[COPYRIGHT]"] = $copyright

function Write-Template {
    param(
        [Parameter(Mandatory = $true)][string]$TemplatePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    $content = Read-Utf8File (Join-Path $repoRoot $TemplatePath)
    $content = Apply-Replacements -Content $content -Replacements $replacements
    Write-Utf8File -Path (Join-Path $destRoot $TargetPath) -Content $content
}

Write-Template "templates/repo/brand-repo-readme-template.md" "README.md"
Write-Template "templates/repo/brand-repo-manifest-template.yaml" "brand-manifest.yaml"
Write-Template "templates/brand/brand-setting-template.md" "brand/brand-setting.md"
Write-Template "templates/brand/brand-positioning-template.md" "brand/brand-positioning.md"
Write-Template "templates/brand/brand-production-brief-template.md" "brand/brand-production-brief.md"
Write-Template "templates/brand/brand-system-prompt-template.md" "brand/brand-system-prompt.md"
Write-Template "templates/market/market-observation-log-template.md" "market/market-observation-log.md"
Write-Template "templates/market/category-gap-map-template.md" "market/category-gap-map.md"
Write-Template "templates/ip/ip-style-bible-template.md" "brand/ip/ip-style-bible.md"
Write-Template "templates/ip/reference-asset-register-template.md" "brand/ip/reference-asset-register.md"
Write-Template "templates/ip/ip-approval-log-template.md" "brand/ip/ip-approval-log.md"
Write-Template "templates/ip/character-expression-matrix-template.md" "brand/ip/character-expression-matrix.md"
Write-Template "templates/release/release-spec-template.md" "releases/$releaseId/release-spec.md"
Write-Template "templates/release/production-handoff-template.md" "releases/$releaseId/production-handoff.md"
Write-Template "templates/release/release-log-template.md" "releases/$releaseId/release-log.md"
Write-Template "templates/prompts/rough-generation-template.md" "releases/$releaseId/prompts/rough-generation.md"
Write-Template "templates/prompts/finalization-template.md" "releases/$releaseId/prompts/finalization.md"
Write-Template "templates/prompts/revision-template.md" "releases/$releaseId/prompts/revision.md"
Write-Template "templates/prompts/qa-review-template.md" "releases/$releaseId/prompts/qa-review.md"
Write-Template "templates/prompts/metadata-review-template.md" "releases/$releaseId/prompts/metadata-review.md"
Write-Template "templates/repo/rough-boards-readme-template.md" "releases/$releaseId/production/rough-boards/README.md"
Write-Template "templates/repo/finals-readme-template.md" "releases/$releaseId/production/finals/README.md"
Write-Template "templates/qa/release-checklist-template.md" "releases/$releaseId/qa/release-checklist.md"
Write-Template "templates/qa/quality-ledger-template.md" "releases/$releaseId/qa/quality-ledger.md"
Write-Template "templates/qa/usage-validation-template.md" "releases/$releaseId/qa/usage-validation.md"
Write-Template "templates/qa/release-retrospective-template.md" "releases/$releaseId/qa/release-retrospective.md"
Write-Template "templates/submission/submission-metadata-template.yaml" "releases/$releaseId/submission/metadata.yaml"
Write-Template "templates/submission/submission-checklist-template.md" "releases/$releaseId/submission/submission-checklist.md"
Write-Template "templates/submission/submission-audit-report-template.md" "releases/$releaseId/submission/submission-audit-report.md"
Write-Template "templates/submission/package-report-template.md" "releases/$releaseId/submission/package-report.md"

Write-Utf8File -Path (Join-Path $destRoot "releases/$releaseId/submission/images/.gitkeep") -Content ""

Write-Host "Brand repo initialized at $destRoot"
