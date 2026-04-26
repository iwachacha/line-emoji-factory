param(
    [Parameter(Mandatory = $true)]
    [string]$BrandRepo,

    [ValidatePattern("^release-\d{3}$")]
    [string]$ReleaseId = "release-001",

    [ValidateSet("static-emoji", "static-sticker")]
    [string]$ProductItemType = "static-sticker",

    [ValidateSet("8", "16", "24", "32", "40")]
    [int]$InitialSetCount = 8,

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
        -not (Test-Path -LiteralPath (Join-Path $resolved "templates") -PathType Container) -or
        -not (Test-Path -LiteralPath (Join-Path $resolved "schemas") -PathType Container)
    ) {
        throw "FactoryRoot must point to line-emoji-factory. Pass -FactoryRoot <path-to-factory> when running from a brand repo copy."
    }

    return $resolved
}

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

function Write-Template {
    param(
        [Parameter(Mandatory = $true)][string]$TemplatePath,
        [Parameter(Mandatory = $true)][string]$TargetPath,
        [Parameter(Mandatory = $true)][string]$FactoryRoot,
        [Parameter(Mandatory = $true)][string]$BrandRoot,
        [Parameter(Mandatory = $true)][hashtable]$Replacements
    )

    $content = Read-Utf8File (Join-Path $FactoryRoot $TemplatePath)
    $content = Apply-Replacements -Content $content -Replacements $Replacements
    Write-Utf8File -Path (Join-Path $BrandRoot $TargetPath) -Content $content
}

function Copy-FactoryFile {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target,
        [Parameter(Mandatory = $true)][string]$FactoryRoot,
        [Parameter(Mandatory = $true)][string]$BrandRoot
    )

    $targetPath = Join-Path $BrandRoot $Target
    $targetDir = Split-Path -Parent $targetPath
    if ($targetDir -and -not (Test-Path -LiteralPath $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    Copy-Item -LiteralPath (Join-Path $FactoryRoot $Source) -Destination $targetPath -Force
}

function Get-SectionValue {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Section,
        [Parameter(Mandatory = $true)][string]$Key,
        [Parameter(Mandatory = $true)][string]$Fallback
    )

    $inSection = $false
    foreach ($line in $Text -split "`r?`n") {
        if ($line -match "^$Section`:\s*$") {
            $inSection = $true
            continue
        }
        if ($inSection -and $line -match '^\S') {
            break
        }
        if ($inSection -and $line -match "^\s{2}$Key`:\s*[""']?([^""']+)[""']?\s*$") {
            return $Matches[1].Trim()
        }
    }

    return $Fallback
}

function Replace-Required {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$OldValue,
        [Parameter(Mandatory = $true)][string]$NewValue
    )

    $candidate = $OldValue
    if (-not $Text.Contains($candidate) -and $OldValue.Contains("`n")) {
        $crlfCandidate = $OldValue.Replace("`n", "`r`n")
        if ($Text.Contains($crlfCandidate)) {
            $candidate = $crlfCandidate
        }
    }

    if (-not $Text.Contains($candidate)) {
        throw "Could not find manifest insertion point: $OldValue"
    }

    return $Text.Replace($candidate, $NewValue)
}

$factoryRootPath = Resolve-FactoryRoot -RequestedRoot $FactoryRoot
$brandRoot = [System.IO.Path]::GetFullPath($BrandRepo)
$manifestPath = Join-Path $brandRoot "brand-manifest.yaml"
$releaseRoot = Join-Path $brandRoot "releases/$ReleaseId"

if (-not (Test-Path -LiteralPath $brandRoot -PathType Container)) {
    throw "Brand repo does not exist: $brandRoot"
}
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Brand manifest does not exist: $manifestPath"
}
if (Test-Path -LiteralPath $releaseRoot) {
    throw "Release already exists: $ReleaseId"
}

$manifestText = Read-Utf8File $manifestPath
if ($manifestText -match 'profile:\s*["'']?production["'']?') {
    throw "Brand repo is already production profile."
}

$brandSlug = Get-SectionValue -Text $manifestText -Section "brand" -Key "slug" -Fallback "brand"
$brandName = Get-SectionValue -Text $manifestText -Section "brand" -Key "name" -Fallback $brandSlug
$brandType = Get-SectionValue -Text $manifestText -Section "brand" -Key "type" -Fallback "generic"
$packageType = if ($ProductItemType -eq "static-sticker") { "sticker" } else { "emoji" }

$dirs = @(
    "releases/$ReleaseId/prompts",
    "releases/$ReleaseId/production/rough-boards",
    "releases/$ReleaseId/production/finals",
    "releases/$ReleaseId/production/main",
    "releases/$ReleaseId/production/tab",
    "releases/$ReleaseId/qa",
    "releases/$ReleaseId/submission",
    "releases/$ReleaseId/submission/line-upload/images",
    "releases/$ReleaseId/submission/internal-archive"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path (Join-Path $brandRoot $dir) -Force | Out-Null
}

$productionSnapshots = @(
    @{ Source = "workflows/production-pipeline-workflow.md"; Target = "references/shared/production-pipeline-workflow.md" },
    @{ Source = "rules/asset-validation-rules.md"; Target = "references/shared/asset-validation-rules.md" },
    @{ Source = "rules/visual-asset-quality-rules.md"; Target = "references/shared/visual-asset-quality-rules.md" },
    @{ Source = "rules/production-profile-rules.md"; Target = "references/shared/production-profile-rules.md" },
    @{ Source = "rules/submission-metadata-rules.md"; Target = "references/shared/submission-metadata-rules.md" },
    @{ Source = "workflows/quality-control-workflow.md"; Target = "references/shared/quality-control-workflow.md" },
    @{ Source = "workflows/series-development-workflow.md"; Target = "references/shared/series-development-workflow.md" },
    @{ Source = "workflows/item-generation-workflow.md"; Target = "references/shared/item-generation-workflow.md" },
    @{ Source = "workflows/usage-validation-workflow.md"; Target = "references/shared/usage-validation-workflow.md" },
    @{ Source = "workflows/submission-audit-workflow.md"; Target = "references/shared/submission-audit-workflow.md" }
)
foreach ($item in $productionSnapshots) {
    Copy-FactoryFile -Source $item.Source -Target $item.Target -FactoryRoot $factoryRootPath -BrandRoot $brandRoot
}

$productionSchemas = @(
    "schemas/submission-metadata.schema.json",
    "schemas/release-spec.schema.json",
    "schemas/production-handoff.schema.json",
    "schemas/asset-validation-report.schema.json",
    "schemas/quality-ledger.schema.json",
    "schemas/usage-validation.schema.json",
    "schemas/post-release-metrics.schema.json"
)
foreach ($schema in $productionSchemas) {
    Copy-FactoryFile -Source $schema -Target $schema -FactoryRoot $factoryRootPath -BrandRoot $brandRoot
}

$productionTools = @(
    "tools/validate-metadata.py",
    "tools/validate-assets.py",
    "tools/package-release.py"
)
foreach ($tool in $productionTools) {
    Copy-FactoryFile -Source $tool -Target $tool -FactoryRoot $factoryRootPath -BrandRoot $brandRoot
}

$replacements = @{}
$replacements["your-brand-slug"] = $brandSlug
$replacements["YOUR_BRAND_NAME"] = $brandName
$replacements["[BRAND_NAME]"] = $brandName
$replacements["[BRAND_SLUG]"] = $brandSlug
$replacements["[INIT_DATE]"] = Get-Date -Format "yyyy-MM-dd"
$replacements["[RELEASE_ID]"] = $ReleaseId
$replacements["[CREATOR_NAME]"] = $brandName
$replacements["[TITLE]"] = $brandName
$replacements["[DESCRIPTION]"] = "LINE item for $brandName."
$replacements["[COPYRIGHT]"] = ($brandSlug -replace "-", "")
$replacements["[INITIAL_SET_COUNT]"] = [string]$InitialSetCount
$replacements["[BRAND_TYPE]"] = $brandType
$replacements["[ITEM_TYPE]"] = $ProductItemType
$replacements["[PACKAGE_TYPE]"] = $packageType
$replacements["[ANIMATION]"] = "false"
$replacements["[REPO_PROFILE]"] = "production"
$replacements["  # [ANIMATION_SUPPORTED_ITEM]"] = ""

Write-Template "templates/release/release-spec-template.md" "releases/$ReleaseId/release-spec.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/release/series-plan-template.md" "releases/$ReleaseId/series-plan.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/release/production-handoff-template.md" "releases/$ReleaseId/production-handoff.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/release/release-log-template.md" "releases/$ReleaseId/release-log.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/rough-generation-template.md" "releases/$ReleaseId/prompts/rough-generation.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/finalization-template.md" "releases/$ReleaseId/prompts/finalization.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/revision-template.md" "releases/$ReleaseId/prompts/revision.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/qa-review-template.md" "releases/$ReleaseId/prompts/qa-review.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/metadata-review-template.md" "releases/$ReleaseId/prompts/metadata-review.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/item-image-prompt-template.md" "releases/$ReleaseId/prompts/item-image-prompt.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/prompts/regeneration-feedback-template.md" "releases/$ReleaseId/prompts/regeneration-feedback.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/repo/rough-boards-readme-template.md" "releases/$ReleaseId/production/rough-boards/README.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/repo/finals-readme-template.md" "releases/$ReleaseId/production/finals/README.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/qa/release-checklist-template.md" "releases/$ReleaseId/qa/release-checklist.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/qa/quality-ledger-template.md" "releases/$ReleaseId/qa/quality-ledger.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/qa/usage-validation-template.md" "releases/$ReleaseId/qa/usage-validation.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/qa/release-retrospective-template.md" "releases/$ReleaseId/qa/release-retrospective.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/submission/submission-metadata-template.yaml" "releases/$ReleaseId/submission/metadata.yaml" $factoryRootPath $brandRoot $replacements
Write-Template "templates/submission/submission-checklist-template.md" "releases/$ReleaseId/submission/submission-checklist.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/submission/submission-audit-report-template.md" "releases/$ReleaseId/submission/submission-audit-report.md" $factoryRootPath $brandRoot $replacements
Write-Template "templates/submission/package-report-template.md" "releases/$ReleaseId/submission/package-report.md" $factoryRootPath $brandRoot $replacements
Write-Utf8File -Path (Join-Path $brandRoot "releases/$ReleaseId/submission/line-upload/images/.gitkeep") -Content ""
Write-Utf8File -Path (Join-Path $brandRoot "releases/$ReleaseId/submission/internal-archive/.gitkeep") -Content ""
Write-Utf8File -Path (Join-Path $brandRoot "releases/$ReleaseId/production/main/.gitkeep") -Content ""
Write-Utf8File -Path (Join-Path $brandRoot "releases/$ReleaseId/production/tab/.gitkeep") -Content ""

$productionBlock = @"
production:
  profile: "gpt-series-production"
  release_root: "releases"
  active_release: "$ReleaseId"
  final_asset_dir: "releases/$ReleaseId/production/finals"
  prompt_bundle_dir: "releases/$ReleaseId/prompts"

production_profile:
  name: "gpt-series-production"
  brand_canon_stage:
    purpose: "brand canon and IP guardrail confirmation"
    required_outputs:
      - "brand_canon"
      - "ip_guardrails"
      - "allowed_variations"
      - "prohibited_drift"
  series_planning_stage:
    purpose: "release differentiation from previous products"
    required_outputs:
      - "product_catalog_review"
      - "series_plan"
      - "inheritance_points"
      - "novelty_points"
      - "cannibalization_notes"
  rough_stage:
    purpose: "style, character, motif, and set-direction exploration"
    required_outputs:
      - "style_anchor"
      - "character_anchor"
      - "rough_board"
      - "per_item_intent"
      - "failure_notes"
  item_finalization_stage:
    purpose: "one-item-at-a-time final asset candidate production"
    required_outputs:
      - "item_specs"
      - "four_candidate_minimum"
      - "candidate_comparison"
      - "final_assets"
      - "correction_notes"
      - "export_check"
  product_qa_stage:
    purpose: "small-size and product usability QA"
    required_outputs:
      - "contact_sheet"
      - "chat_preview"
      - "asset_validation_report"
      - "duplicate_and_usage_overlap_notes"
      - "unresolved_watch_items"
  release_ledger_stage:
    purpose: "update release ledger and brand product catalog"
    required_outputs:
      - "release_log_update"
      - "quality_ledger_update"
      - "product_catalog_update"
      - "next_series_watch"
  revision_stage:
    purpose: "slot-level corrections"
    required_outputs:
      - "revision_notes"
      - "fixed_assets"
      - "unresolved_watch_items"

quality:
  release_checklist_path: "releases/$ReleaseId/qa/release-checklist.md"
  quality_ledger_path: "releases/$ReleaseId/qa/quality-ledger.md"
  usage_validation_path: "releases/$ReleaseId/qa/usage-validation.md"
  retrospective_path: "releases/$ReleaseId/qa/release-retrospective.md"
  release_log_path: "releases/$ReleaseId/release-log.md"

submission:
  metadata_path: "releases/$ReleaseId/submission/metadata.yaml"
  checklist_path: "releases/$ReleaseId/submission/submission-checklist.md"
  audit_report_path: "releases/$ReleaseId/submission/submission-audit-report.md"
  line_upload_dir: "releases/$ReleaseId/submission/line-upload"
  internal_archive_dir: "releases/$ReleaseId/submission/internal-archive"

"@

$releaseBlock = @"
releases:
  - id: "$ReleaseId"
    status: "draft"
    item_type: "$ProductItemType"
    package_type: "$packageType"
    set_count: $InitialSetCount
    animation: false
    series_plan: "releases/$ReleaseId/series-plan.md"
    spec: "releases/$ReleaseId/release-spec.md"
    handoff: "releases/$ReleaseId/production-handoff.md"
    checklist: "releases/$ReleaseId/qa/release-checklist.md"
    submission: "releases/$ReleaseId/submission"
"@

$manifestText = $manifestText -replace 'profile:\s*["'']?startup["'']?', 'profile: "production"'
$manifestText = $manifestText -replace 'stage:\s*["'']?startup["'']?', 'stage: "production"'
$manifestText = $manifestText -replace 'status:\s*["'']?hypothesis["'']?', 'status: "production"'
$manifestText = $manifestText -replace '(?m)^  item_type:\s*["'']?[^"'']+["'']?\s*$', "  item_type: `"$ProductItemType`""
$manifestText = $manifestText -replace '(?m)^  package_type:\s*["'']?[^"'']+["'']?\s*$', "  package_type: `"$packageType`""
$manifestText = $manifestText -replace '(?m)^  initial_set_count:\s*\d+\s*$', "  initial_set_count: $InitialSetCount"
$manifestText = $manifestText -replace '(?m)^  animation:\s*(true|false)\s*$', "  animation: false"
$manifestText = Replace-Required -Text $manifestText -OldValue '  set_architecture_workflow: "references/shared/set-architecture-workflow.md"' -NewValue @"
  set_architecture_workflow: "references/shared/set-architecture-workflow.md"
  production_pipeline_workflow: "references/shared/production-pipeline-workflow.md"
  visual_asset_quality_rules: "references/shared/visual-asset-quality-rules.md"
  quality_control_workflow: "references/shared/quality-control-workflow.md"
  series_development_workflow: "references/shared/series-development-workflow.md"
  item_generation_workflow: "references/shared/item-generation-workflow.md"
  usage_validation_workflow: "references/shared/usage-validation-workflow.md"
  asset_validation_rules: "references/shared/asset-validation-rules.md"
  production_profile_rules: "references/shared/production-profile-rules.md"
  submission_metadata_rules: "references/shared/submission-metadata-rules.md"
"@
$manifestText = Replace-Required -Text $manifestText -OldValue '  startup_brief_path: "startup/brand-startup.md"' -NewValue @"
  startup_brief_path: "startup/brand-startup.md"
  active_release_spec_path: "releases/$ReleaseId/release-spec.md"
  active_series_plan_path: "releases/$ReleaseId/series-plan.md"
"@
$manifestText = Replace-Required -Text $manifestText -OldValue "strategy:`n" -NewValue ($productionBlock + "strategy:`n")
$manifestText = Replace-Required -Text $manifestText -OldValue "releases: []" -NewValue $releaseBlock
Write-Utf8File -Path $manifestPath -Content $manifestText

$requirementsPath = Join-Path $brandRoot "requirements-dev.txt"
if (Test-Path -LiteralPath $requirementsPath) {
    $requirements = [System.Collections.Generic.List[string]]::new()
    foreach ($line in [System.IO.File]::ReadAllLines($requirementsPath, [System.Text.Encoding]::UTF8)) {
        if ($line.Trim()) {
            $requirements.Add($line.Trim())
        }
    }
    if (-not $requirements.Contains("pillow")) {
        $requirements.Add("pillow")
    }
    $requirementsContent = (($requirements | Select-Object -Unique) -join "`n") + "`n"
    Write-Utf8File -Path $requirementsPath -Content $requirementsContent
}

Write-Host "Brand repo promoted to production profile at $brandRoot"
