# [BRAND_NAME]

This repository is a brand startup project for the LINE emoji / sticker brand `[BRAND_NAME]`.

It contains the minimum shared baseline, brand owner files, startup data, and prompt scaffolding needed to turn an initial concept into a production-ready brand. It is intentionally lighter than a full submission repo.

## Entry Points

- Machine-readable manifest: `brand-manifest.yaml`
- Startup brief: `startup/brand-startup.md`
- Startup checklist: `startup/startup-checklist.md`
- Brand source of truth: `brand/brand-setting.md`
- Brand canon / IP guardrails: `brand/brand-canon.md`
- Brand positioning: `brand/brand-positioning.md`
- Production brief seed: `brand/brand-production-brief.md`
- Brand prompt source of truth: `brand/brand-system-prompt.md`
- Product catalog / series ledger seed: `brand/product-catalog.md`
- Character / motif data: `data/characters.json`
- First item seed data: `data/item-seeds.json`
- Prompt library: `prompts/prompt-library.md`
- Shared snapshots: `references/shared/`

## Validation

From this repo:

```powershell
python .\tools\validate-brand-repo.py .
python .\tools\check-source-integrity.py
python .\tools\check-data-files.py
```

Or from the factory repo:

```powershell
.\tools\validate-brand-repo.ps1 "<this-repo-path>"
```

## Startup Rules

- Judge in this order: structure, brand, product.
- Keep hard canon narrow until anchors or first-series testing prove what must be fixed.
- Record variable boundaries instead of inventing lore to hide weak product structure.
- Keep first item ideas in `data/item-seeds.json`; do not create production assets by default.
- Do not add QA, submission, package, or release history until the brand moves into production.
- Image text should be added after generation. Do not ask image generation to render submission text.

## Production Promotion

When the brand is ready for real asset production, add a production skeleton or re-run the factory scaffold in production mode. Production adds release specs, handoff, QA, submission metadata, asset validation, and packaging tools.
For an existing startup repo, use `tools/promote-brand-repo.ps1` from the factory repo or pass `-FactoryRoot` when running the copied tool.
