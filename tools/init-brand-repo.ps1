param(
    [Parameter(Mandatory = $true)]
    [string]$BrandSlug,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [string]$BrandName = "",

    [ValidateSet("8", "16", "24", "32", "40")]
    [int]$InitialSetCount = 8,

    [ValidateSet("generic", "fixed_ip", "collaboration")]
    [string]$BrandType = "generic",

    [ValidateSet("static-emoji", "animation-emoji", "static-sticker")]
    [string]$ProductItemType = "static-sticker",

    [ValidateSet("startup", "production")]
    [string]$RepoProfile = "startup"
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

function Write-Template {
    param(
        [Parameter(Mandatory = $true)][string]$TemplatePath,
        [Parameter(Mandatory = $true)][string]$TargetPath,
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$DestRoot,
        [Parameter(Mandatory = $true)][hashtable]$Replacements
    )

    $content = Read-Utf8File (Join-Path $RepoRoot $TemplatePath)
    $content = Apply-Replacements -Content $content -Replacements $Replacements
    Write-Utf8File -Path (Join-Path $DestRoot $TargetPath) -Content $content
}

function Copy-Snapshot {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target,
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$DestRoot
    )

    Copy-Item -LiteralPath (Join-Path $RepoRoot $Source) -Destination (Join-Path $DestRoot $Target) -Force
}

if ($BrandSlug -notmatch '^[a-z0-9-]+$') {
    throw "BrandSlug must be lowercase hyphen-case."
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$destRoot = [System.IO.Path]::GetFullPath($Destination)

if (Test-Path -LiteralPath $destRoot) {
    throw "Destination already exists: $destRoot"
}

if ($RepoProfile -eq "production" -and $ProductItemType -eq "animation-emoji") {
    throw "RepoProfile production does not support animation-emoji packaging yet. Use RepoProfile startup for animation hypotheses."
}

if (-not $BrandName) {
    $parts = ($BrandSlug -split "-") | ForEach-Object {
        if ($_.Length -gt 0) { $_.Substring(0, 1).ToUpper() + $_.Substring(1) } else { $_ }
    }
    $BrandName = ($parts -join " ")
}

$releaseId = "release-001"
$initDate = Get-Date -Format "yyyy-MM-dd"
$copyright = ($BrandSlug -replace "-", "")
$packageType = if ($ProductItemType -eq "static-sticker") { "sticker" } else { "emoji" }
$animation = if ($ProductItemType -eq "animation-emoji") { "true" } else { "false" }
$animationSupportedItem = if ($ProductItemType -eq "animation-emoji") { '    - "animation-emoji"' } else { "" }

$dirs = @(
    "brand",
    "startup",
    "data",
    "prompts",
    "market",
    "references/shared",
    "schemas",
    "tools"
)

if ($BrandType -eq "fixed_ip") {
    $dirs += "brand/ip"
}

if ($RepoProfile -eq "production") {
    $dirs += @(
        "releases/$releaseId/prompts",
        "releases/$releaseId/production/rough-boards",
        "releases/$releaseId/production/finals",
        "releases/$releaseId/production/main",
        "releases/$releaseId/production/tab",
        "releases/$releaseId/qa",
        "releases/$releaseId/submission",
        "releases/$releaseId/submission/line-upload/images",
        "releases/$releaseId/submission/internal-archive"
    )
}

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path (Join-Path $destRoot $dir) -Force | Out-Null
}

$startupSnapshots = @(
    @{ Source = "rules/line-platform-baseline.md"; Target = "references/shared/line-platform-baseline.md" },
    @{ Source = "rules/structure-constraints.md"; Target = "references/shared/structure-constraints.md" },
    @{ Source = "rules/evaluation-model.md"; Target = "references/shared/evaluation-model.md" },
    @{ Source = "rules/brand-taxonomy.md"; Target = "references/shared/brand-taxonomy.md" },
    @{ Source = "rules/brand-creation-rules.md"; Target = "references/shared/brand-creation-rules.md" },
    @{ Source = "rules/emoji-product-rules.md"; Target = "references/shared/emoji-product-rules.md" },
    @{ Source = "rules/sticker-product-rules.md"; Target = "references/shared/sticker-product-rules.md" },
    @{ Source = "rules/review-risk-rules.md"; Target = "references/shared/review-risk-rules.md" },
    @{ Source = "rules/review-risk-keywords.yaml"; Target = "references/shared/review-risk-keywords.yaml" },
    @{ Source = "workflows/brand-distillation-workflow.md"; Target = "references/shared/brand-distillation-workflow.md" },
    @{ Source = "workflows/set-architecture-workflow.md"; Target = "references/shared/set-architecture-workflow.md" }
)

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

foreach ($item in $startupSnapshots) {
    Copy-Snapshot -Source $item.Source -Target $item.Target -RepoRoot $repoRoot -DestRoot $destRoot
}
if ($RepoProfile -eq "production") {
    foreach ($item in $productionSnapshots) {
        Copy-Snapshot -Source $item.Source -Target $item.Target -RepoRoot $repoRoot -DestRoot $destRoot
    }
}

$schemaFiles = @(
    "schemas/brand-manifest.schema.json",
    "schemas/market-observation.schema.json"
)

if ($RepoProfile -eq "production") {
    $schemaFiles += @(
        "schemas/submission-metadata.schema.json",
        "schemas/release-spec.schema.json",
        "schemas/production-handoff.schema.json",
        "schemas/asset-validation-report.schema.json",
        "schemas/quality-ledger.schema.json",
        "schemas/usage-validation.schema.json",
        "schemas/post-release-metrics.schema.json"
    )
}

if ($BrandType -eq "fixed_ip") {
    $schemaFiles += @(
        "schemas/ip-style-bible.schema.json",
        "schemas/reference-asset-register.schema.json"
    )
}

foreach ($schemaPath in $schemaFiles | Select-Object -Unique) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $schemaPath) -Destination (Join-Path $destRoot $schemaPath) -Force
}

$toolFiles = @(
    "tools/validate-brand-repo.py",
    "tools/validate-brand-repo.ps1",
    "tools/validate-schemas.py",
    "tools/check-source-integrity.py",
    "tools/check-data-files.py",
    "tools/check-placeholders.py",
    "tools/validate-manifest-paths.py",
    "tools/sync-shared-snapshots.ps1",
    "tools/promote-brand-repo.ps1"
)

if ($RepoProfile -eq "production") {
    $toolFiles += @(
        "tools/validate-metadata.py",
        "tools/validate-assets.py",
        "tools/package-release.py"
    )
}

foreach ($toolPath in $toolFiles | Select-Object -Unique) {
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
$replacements["[DESCRIPTION]"] = "LINE item for $BrandName."
$replacements["[COPYRIGHT]"] = $copyright
$replacements["[INITIAL_SET_COUNT]"] = [string]$InitialSetCount
$replacements["[BRAND_TYPE]"] = $BrandType
$replacements["[ITEM_TYPE]"] = $ProductItemType
$replacements["[PACKAGE_TYPE]"] = $packageType
$replacements["[ANIMATION]"] = $animation
$replacements["[REPO_PROFILE]"] = $RepoProfile
$replacements["  # [ANIMATION_SUPPORTED_ITEM]"] = $animationSupportedItem

Write-Template "templates/repo/brand-repo-readme-template.md" "README.md" $repoRoot $destRoot $replacements
Write-Template "templates/repo/brand-startup-agents-template.md" "AGENTS.md" $repoRoot $destRoot $replacements
Write-Template "templates/repo/brand-startup-project-map-template.md" "PROJECT_MAP.md" $repoRoot $destRoot $replacements
Write-Template "templates/repo/brand-repo-manifest-template.yaml" "brand-manifest.yaml" $repoRoot $destRoot $replacements
Write-Template "templates/startup/brand-startup-template.md" "startup/brand-startup.md" $repoRoot $destRoot $replacements
Write-Template "templates/startup/startup-checklist-template.md" "startup/startup-checklist.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-canon-template.md" "brand/brand-canon.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-setting-template.md" "brand/brand-setting.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-positioning-template.md" "brand/brand-positioning.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-production-brief-template.md" "brand/brand-production-brief.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-system-prompt-template.md" "brand/brand-system-prompt.md" $repoRoot $destRoot $replacements
Write-Template "templates/brand/brand-product-catalog-template.md" "brand/product-catalog.md" $repoRoot $destRoot $replacements
Write-Template "templates/data/characters-template.json" "data/characters.json" $repoRoot $destRoot $replacements
Write-Template "templates/data/item-seeds-template.json" "data/item-seeds.json" $repoRoot $destRoot $replacements
Write-Template "templates/data/asset-log-template.csv" "data/asset-log.csv" $repoRoot $destRoot $replacements
Write-Template "templates/prompts/brand-prompt-library-template.md" "prompts/prompt-library.md" $repoRoot $destRoot $replacements
Write-Template "templates/market/market-observation-log-template.md" "market/market-observation-log.md" $repoRoot $destRoot $replacements
Write-Template "templates/market/category-gap-map-template.md" "market/category-gap-map.md" $repoRoot $destRoot $replacements

if ($BrandType -eq "fixed_ip") {
    Write-Template "templates/ip/ip-style-bible-template.md" "brand/ip/ip-style-bible.md" $repoRoot $destRoot $replacements
    Write-Template "templates/ip/reference-asset-register-template.md" "brand/ip/reference-asset-register.md" $repoRoot $destRoot $replacements
    Write-Template "templates/ip/ip-approval-log-template.md" "brand/ip/ip-approval-log.md" $repoRoot $destRoot $replacements
    Write-Template "templates/ip/character-expression-matrix-template.md" "brand/ip/character-expression-matrix.md" $repoRoot $destRoot $replacements
}

if ($RepoProfile -eq "production") {
    Write-Template "templates/release/release-spec-template.md" "releases/$releaseId/release-spec.md" $repoRoot $destRoot $replacements
    Write-Template "templates/release/series-plan-template.md" "releases/$releaseId/series-plan.md" $repoRoot $destRoot $replacements
    Write-Template "templates/release/production-handoff-template.md" "releases/$releaseId/production-handoff.md" $repoRoot $destRoot $replacements
    Write-Template "templates/release/release-log-template.md" "releases/$releaseId/release-log.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/rough-generation-template.md" "releases/$releaseId/prompts/rough-generation.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/finalization-template.md" "releases/$releaseId/prompts/finalization.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/revision-template.md" "releases/$releaseId/prompts/revision.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/qa-review-template.md" "releases/$releaseId/prompts/qa-review.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/metadata-review-template.md" "releases/$releaseId/prompts/metadata-review.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/item-image-prompt-template.md" "releases/$releaseId/prompts/item-image-prompt.md" $repoRoot $destRoot $replacements
    Write-Template "templates/prompts/regeneration-feedback-template.md" "releases/$releaseId/prompts/regeneration-feedback.md" $repoRoot $destRoot $replacements
    Write-Template "templates/repo/rough-boards-readme-template.md" "releases/$releaseId/production/rough-boards/README.md" $repoRoot $destRoot $replacements
    Write-Template "templates/repo/finals-readme-template.md" "releases/$releaseId/production/finals/README.md" $repoRoot $destRoot $replacements
    Write-Template "templates/qa/release-checklist-template.md" "releases/$releaseId/qa/release-checklist.md" $repoRoot $destRoot $replacements
    Write-Template "templates/qa/quality-ledger-template.md" "releases/$releaseId/qa/quality-ledger.md" $repoRoot $destRoot $replacements
    Write-Template "templates/qa/usage-validation-template.md" "releases/$releaseId/qa/usage-validation.md" $repoRoot $destRoot $replacements
    Write-Template "templates/qa/release-retrospective-template.md" "releases/$releaseId/qa/release-retrospective.md" $repoRoot $destRoot $replacements
    Write-Template "templates/submission/submission-metadata-template.yaml" "releases/$releaseId/submission/metadata.yaml" $repoRoot $destRoot $replacements
    Write-Template "templates/submission/submission-checklist-template.md" "releases/$releaseId/submission/submission-checklist.md" $repoRoot $destRoot $replacements
    Write-Template "templates/submission/submission-audit-report-template.md" "releases/$releaseId/submission/submission-audit-report.md" $repoRoot $destRoot $replacements
    Write-Template "templates/submission/package-report-template.md" "releases/$releaseId/submission/package-report.md" $repoRoot $destRoot $replacements
    Write-Utf8File -Path (Join-Path $destRoot "releases/$releaseId/submission/line-upload/images/.gitkeep") -Content ""
    Write-Utf8File -Path (Join-Path $destRoot "releases/$releaseId/submission/internal-archive/.gitkeep") -Content ""
    Write-Utf8File -Path (Join-Path $destRoot "releases/$releaseId/production/main/.gitkeep") -Content ""
    Write-Utf8File -Path (Join-Path $destRoot "releases/$releaseId/production/tab/.gitkeep") -Content ""

    $manifestPath = Join-Path $destRoot "brand-manifest.yaml"
    $manifestText = Read-Utf8File $manifestPath
    $productionBlock = @"

production:
  profile: "gpt-series-production"
  release_root: "releases"
  active_release: "release-001"
  final_asset_dir: "releases/release-001/production/finals"
  prompt_bundle_dir: "releases/release-001/prompts"

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
  release_checklist_path: "releases/release-001/qa/release-checklist.md"
  quality_ledger_path: "releases/release-001/qa/quality-ledger.md"
  usage_validation_path: "releases/release-001/qa/usage-validation.md"
  retrospective_path: "releases/release-001/qa/release-retrospective.md"
  release_log_path: "releases/release-001/release-log.md"

submission:
  metadata_path: "releases/release-001/submission/metadata.yaml"
  checklist_path: "releases/release-001/submission/submission-checklist.md"
  audit_report_path: "releases/release-001/submission/submission-audit-report.md"
  line_upload_dir: "releases/release-001/submission/line-upload"
  internal_archive_dir: "releases/release-001/submission/internal-archive"
"@
    $manifestText = $manifestText.Replace("  set_architecture_workflow: `"references/shared/set-architecture-workflow.md`"", @"
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
"@)
    $manifestText = $manifestText.Replace("  startup_brief_path: `"startup/brand-startup.md`"", @"
  startup_brief_path: "startup/brand-startup.md"
  active_release_spec_path: "releases/release-001/release-spec.md"
  active_series_plan_path: "releases/release-001/series-plan.md"
"@)
    $manifestText = $manifestText.Replace("releases: []", @"
$productionBlock

releases:
  - id: "release-001"
    status: "draft"
    item_type: "$ProductItemType"
    package_type: "$packageType"
    set_count: $InitialSetCount
    animation: $animation
    series_plan: "releases/release-001/series-plan.md"
    spec: "releases/release-001/release-spec.md"
    handoff: "releases/release-001/production-handoff.md"
    checklist: "releases/release-001/qa/release-checklist.md"
    submission: "releases/release-001/submission"
"@)
    Write-Utf8File -Path $manifestPath -Content $manifestText
}

if ($BrandType -eq "fixed_ip") {
    $manifestPath = Join-Path $destRoot "brand-manifest.yaml"
    $manifestText = Read-Utf8File $manifestPath
    $ipBlock = @"

ip:
  style_bible: "brand/ip/ip-style-bible.md"
  reference_asset_register: "brand/ip/reference-asset-register.md"
  approval_log: "brand/ip/ip-approval-log.md"
  character_expression_matrix: "brand/ip/character-expression-matrix.md"
"@
    $manifestText = $manifestText.Replace("releases:", "$ipBlock`n`nreleases:")
    Write-Utf8File -Path $manifestPath -Content $manifestText
}

$requirements = @(
    "jsonschema",
    "PyYAML"
)
if ($RepoProfile -eq "production") {
    $requirements += "pillow"
}
Write-Utf8File -Path (Join-Path $destRoot "requirements-dev.txt") -Content (($requirements -join "`n") + "`n")

Write-Utf8File -Path (Join-Path $destRoot ".gitignore") -Content @"
.venv/
__pycache__/
*.pyc
releases/*/submission/line-upload/*.zip
releases/*/submission/internal-archive/*.zip
"@

Write-Host "Brand $RepoProfile repo initialized at $destRoot"
