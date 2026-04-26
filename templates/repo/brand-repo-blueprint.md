# Brand Startup Repo Blueprint

Brand startup repos isolate one brand concept after the factory has enough structure to keep it. They are not full submission projects by default. The default scaffold distributes only the common elements needed to create, judge, and prepare a brand for rough anchors or first-series planning.

## Default Layout

```text
brand-startup-repo/
  AGENTS.md
  PROJECT_MAP.md
  README.md
  brand-manifest.yaml
  requirements-dev.txt
  brand/
    brand-canon.md
    brand-setting.md
    brand-positioning.md
    brand-production-brief.md
    brand-system-prompt.md
    product-catalog.md
  startup/
    brand-startup.md
    startup-checklist.md
  data/
    characters.json
    item-seeds.json
    asset-log.csv
  prompts/
    prompt-library.md
  market/
    market-observation-log.md
    category-gap-map.md
  references/
    shared/
  schemas/
  tools/
```

## Fixed Startup Distribution

The startup scaffold always carries these common snapshots:

- `line-platform-baseline`
- `structure-constraints`
- `evaluation-model`
- `brand-taxonomy`
- `brand-creation-rules`
- `emoji-product-rules`
- `sticker-product-rules`
- `review-risk-rules`
- `review-risk-keywords`
- `brand-distillation-workflow`
- `set-architecture-workflow`

The startup scaffold always carries these tools:

- `validate-brand-repo.py`
- `validate-brand-repo.ps1`
- `validate-schemas.py`
- `check-source-integrity.py`
- `check-data-files.py`
- `check-placeholders.py`
- `validate-manifest-paths.py`
- `sync-shared-snapshots.ps1`
- `promote-brand-repo.ps1`

Asset validation and package creation are not part of the default startup distribution. Add them only when the repo is promoted to production.

## Startup Responsibilities

- Preserve the brand context outside the factory repo.
- Keep hard canon narrow enough to support multiple future series.
- Record what is fixed, what is variable, and what remains undecided.
- Seed first-series item ideas without forcing full release operations.
- Keep prompts reusable across sticker, emoji, and later series patterns.
- Avoid mixing this brand with unrelated ideation history.

## Production Extension

When a startup repo is ready for actual asset production, add a production skeleton:

```text
releases/
  release-001/
    series-plan.md
    release-spec.md
    production-handoff.md
    release-log.md
    prompts/
    production/
      rough-boards/
      finals/
      main/
      tab/
    qa/
    submission/
      metadata.yaml
      submission-checklist.md
      submission-audit-report.md
      line-upload/
      internal-archive/
```

Production repos also carry:

- `production-pipeline-workflow`
- `quality-control-workflow`
- `series-development-workflow`
- `item-generation-workflow`
- `usage-validation-workflow`
- `asset-validation-rules`
- `visual-asset-quality-rules`
- `production-profile-rules`
- `submission-metadata-rules`
- `validate-metadata.py`
- `validate-assets.py`
- `package-release.py`

Use `tools/promote-brand-repo.ps1` when adding this layer to an existing startup repo. Use `tools/init-brand-repo.ps1 -RepoProfile production` only when creating a production repo from scratch.

## Item Types

A brand may support several LINE item types. The manifest records one first hypothesis in `product.item_type`, but this is not a final release obligation. A production release chooses one item type.

Supported startup hypotheses:

- `static-sticker`
- `static-emoji`
- `animation-emoji` as a future hypothesis only; packaging is still unsupported.

## Operating Rules

- Do not live-sync factory files. Shared files are snapshots.
- Do not copy other brands into the repo.
- Do not force QA, submission, or release ledgers before real assets exist.
- Do not treat rough boards or bulk-generated set images as final assets.
- Keep `startup/brand-startup.md`, `brand/brand-canon.md`, and `data/item-seeds.json` aligned.
