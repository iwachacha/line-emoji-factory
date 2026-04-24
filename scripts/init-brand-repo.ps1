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
        [Parameter(Mandatory = $true)][string]$Content
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
        if ($_.Length -gt 0) { $_.Substring(0,1).ToUpper() + $_.Substring(1) } else { $_ }
    }
    $BrandName = ($parts -join " ")
}

$dirs = @(
    "brand",
    "references/market",
    "references/shared",
    "prompts",
    "production/rough-boards",
    "production/handoffs",
    "production/finals",
    "emoji-sets/releases",
    "qa",
    "qa/usage-validations",
    "qa/retrospectives",
    "submissions"
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
    @{ Source = "rules/continuous-improvement-rules.md"; Target = "references/shared/continuous-improvement-rules.md" },
    @{ Source = "workflows/transformation-workflow.md"; Target = "references/shared/transformation-workflow.md" },
    @{ Source = "workflows/production-pipeline-workflow.md"; Target = "references/shared/production-pipeline-workflow.md" },
    @{ Source = "workflows/quality-control-workflow.md"; Target = "references/shared/quality-control-workflow.md" },
    @{ Source = "workflows/continuous-improvement-workflow.md"; Target = "references/shared/continuous-improvement-workflow.md" },
    @{ Source = "workflows/usage-validation-workflow.md"; Target = "references/shared/usage-validation-workflow.md" },
    @{ Source = "workflows/release-retrospective-workflow.md"; Target = "references/shared/release-retrospective-workflow.md" }
)

foreach ($item in $sharedFiles) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $item.Source) -Destination (Join-Path $destRoot $item.Target) -Force
}

$brandSetting = Read-Utf8File (Join-Path $repoRoot "templates/brand-setting-template.md")
$brandBrief = Read-Utf8File (Join-Path $repoRoot "templates/brand-production-brief-template.md")
$brandRepoReadme = Read-Utf8File (Join-Path $repoRoot "templates/brand-repo-readme-template.md")
$ideaBatchTemplate = Read-Utf8File (Join-Path $repoRoot "templates/idea-batch-template.md")
$gptImage2Prompts = Read-Utf8File (Join-Path $repoRoot "templates/gpt-image2-rough-prompts-template.md")
$claudeDesignPrompts = Read-Utf8File (Join-Path $repoRoot "templates/claude-design-prompts-template.md")
$revisionPrompts = Read-Utf8File (Join-Path $repoRoot "templates/revision-prompts-template.md")
$releaseSpecTemplate = Read-Utf8File (Join-Path $repoRoot "templates/release-spec-template.md")
$handoffTemplate = Read-Utf8File (Join-Path $repoRoot "templates/production-handoff-template.md")
$releaseChecklistTemplate = Read-Utf8File (Join-Path $repoRoot "templates/release-checklist-template.md")
$qualityLedgerTemplate = Read-Utf8File (Join-Path $repoRoot "templates/quality-ledger-template.md")
$usageValidationTemplate = Read-Utf8File (Join-Path $repoRoot "templates/usage-validation-template.md")
$releaseRetrospectiveTemplate = Read-Utf8File (Join-Path $repoRoot "templates/release-retrospective-template.md")
$releaseLogTemplate = Read-Utf8File (Join-Path $repoRoot "templates/release-log-template.md")
$roughBoardsReadme = Read-Utf8File (Join-Path $repoRoot "templates/rough-boards-readme-template.md")
$finalsReadme = Read-Utf8File (Join-Path $repoRoot "templates/finals-readme-template.md")
$brandPrompt = Read-Utf8File (Join-Path $repoRoot "templates/brand-system-prompt-template.md")
$manifest = Read-Utf8File (Join-Path $repoRoot "templates/brand-repo-manifest-template.yaml")

$initDate = Get-Date -Format "yyyy-MM-dd"
$releaseId = "release-001"

$replacements = @{
    "your-brand-slug" = $BrandSlug
    "YOUR_BRAND_NAME" = $BrandName
    "[BRAND_NAME]" = $BrandName
    "[BRAND_SLUG]" = $BrandSlug
    "[INIT_DATE]" = $initDate
    "[RELEASE_ID]" = $releaseId
}

$manifest = Apply-Replacements -Content $manifest -Replacements $replacements
$brandRepoReadme = Apply-Replacements -Content $brandRepoReadme -Replacements $replacements
$ideaBatchTemplate = Apply-Replacements -Content $ideaBatchTemplate -Replacements $replacements
$gptImage2Prompts = Apply-Replacements -Content $gptImage2Prompts -Replacements $replacements
$claudeDesignPrompts = Apply-Replacements -Content $claudeDesignPrompts -Replacements $replacements
$revisionPrompts = Apply-Replacements -Content $revisionPrompts -Replacements $replacements
$releaseSpecTemplate = Apply-Replacements -Content $releaseSpecTemplate -Replacements $replacements
$releaseChecklistTemplate = Apply-Replacements -Content $releaseChecklistTemplate -Replacements $replacements
$qualityLedgerTemplate = Apply-Replacements -Content $qualityLedgerTemplate -Replacements $replacements
$usageValidationTemplate = Apply-Replacements -Content $usageValidationTemplate -Replacements $replacements
$releaseRetrospectiveTemplate = Apply-Replacements -Content $releaseRetrospectiveTemplate -Replacements $replacements
$releaseLogTemplate = Apply-Replacements -Content $releaseLogTemplate -Replacements $replacements
$roughBoardsReadme = Apply-Replacements -Content $roughBoardsReadme -Replacements $replacements
$finalsReadme = Apply-Replacements -Content $finalsReadme -Replacements $replacements

Write-Utf8File -Path (Join-Path $destRoot "README.md") -Content $brandRepoReadme
Write-Utf8File -Path (Join-Path $destRoot "brand/brand-setting.md") -Content $brandSetting
Write-Utf8File -Path (Join-Path $destRoot "brand/brand-production-brief.md") -Content $brandBrief
Write-Utf8File -Path (Join-Path $destRoot "brand/brand-system-prompt.md") -Content $brandPrompt
Write-Utf8File -Path (Join-Path $destRoot "brand/brand-manifest.yaml") -Content $manifest
Write-Utf8File -Path (Join-Path $destRoot "references/market/idea-batch-001.md") -Content $ideaBatchTemplate
Write-Utf8File -Path (Join-Path $destRoot "prompts/gpt-image2-rough-prompts.md") -Content $gptImage2Prompts
Write-Utf8File -Path (Join-Path $destRoot "prompts/claude-design-prompts.md") -Content $claudeDesignPrompts
Write-Utf8File -Path (Join-Path $destRoot "prompts/revision-prompts.md") -Content $revisionPrompts
Write-Utf8File -Path (Join-Path $destRoot "production/rough-boards/README.md") -Content $roughBoardsReadme
Write-Utf8File -Path (Join-Path $destRoot "production/handoffs/release-001-handoff.md") -Content $handoffTemplate
Write-Utf8File -Path (Join-Path $destRoot "production/finals/README.md") -Content $finalsReadme
Write-Utf8File -Path (Join-Path $destRoot "emoji-sets/releases/release-001.md") -Content $releaseSpecTemplate
Write-Utf8File -Path (Join-Path $destRoot "qa/release-checklist.md") -Content $releaseChecklistTemplate
Write-Utf8File -Path (Join-Path $destRoot "qa/quality-ledger.md") -Content $qualityLedgerTemplate
Write-Utf8File -Path (Join-Path $destRoot "qa/usage-validations/release-001.md") -Content $usageValidationTemplate
Write-Utf8File -Path (Join-Path $destRoot "qa/retrospectives/release-001.md") -Content $releaseRetrospectiveTemplate
Write-Utf8File -Path (Join-Path $destRoot "submissions/release-log.md") -Content $releaseLogTemplate

Write-Host "Brand repo initialized at $destRoot"
