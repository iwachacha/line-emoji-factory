# [BRAND_NAME]

This repository is dedicated to production, QA, review, and release work for the LINE emoji / sticker brand `[BRAND_NAME]`.

## Entry Points
- Machine-readable manifest: `brand-manifest.yaml`
- Brand source of truth: `brand/brand-setting.md`
- Brand canon / IP guardrails: `brand/brand-canon.md`
- Production source of truth: `brand/brand-production-brief.md`
- Brand prompt source of truth: `brand/brand-system-prompt.md`
- Product catalog / series ledger: `brand/product-catalog.md`
- Market evidence: `market/`
- Shared snapshots: `references/shared/`
- Release root: `releases/`
- Active release spec: `releases/release-001/release-spec.md`
- Active series plan: `releases/release-001/series-plan.md`
- Active production handoff: `releases/release-001/production-handoff.md`
- Active QA: `releases/release-001/qa/`
- Active submission: `releases/release-001/submission/`
- Production profile: `brand-manifest.yaml` `production_profile`

## Validation
Run these from the factory repo root:

```powershell
./tools/validate-brand-repo.ps1 "<this-repo-path>"
python ./tools/validate-metadata.py "<this-repo-path>/releases/release-001/submission/metadata.yaml"
```

When final images are ready:

```powershell
python ./tools/package-release.py "<this-repo-path>" --release-id release-001 --target both --clean
python ./tools/validate-assets.py "<this-repo-path>/releases/release-001/submission/line-upload/images" `
  --expected-count [INITIAL_SET_COUNT] `
  --stage submission `
  --preview-contact-sheet "<this-repo-path>/releases/release-001/qa/contact-sheet.png" `
  --preview-chat-sheet "<this-repo-path>/releases/release-001/qa/chat-preview.png" `
  --report-json "<this-repo-path>/releases/release-001/qa/asset-validation.json"
```

## Operating Rules
- Keep this repo focused on brand-specific production and operations.
- Do not auto-sync factory updates.
- Re-sync shared baselines and workflow snapshots only when official platform changes, review-policy changes, or repeated quality issues require it.
- Treat `brand/`, `market/`, `releases/`, and `submission/` as the working source of truth for this repo.
- New series must read `brand/product-catalog.md`, update `series-plan.md`, and return final QA learning to the catalog.
- Rough boards and anchors are not final products. Finalization is one item at a time with candidate comparison.
