# line-emoji-factory

LINE emoji and sticker brand ideas are evaluated and carried through structure, brand, product, production, validation, and submission packaging. The packaging pipeline targets static emoji and static sticker releases, while each release chooses one item type.

The standard production path is GPT / image_gen centered: brand canon, series planning, rough / anchor generation, one-item-at-a-time finalization, product QA, and catalog update. Rough boards are never treated as final products.

## Requirements

- Python 3.12
- PowerShell 7 recommended for CI parity. Windows PowerShell can parse the local scripts.
- Development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

## Quickstart

```powershell
./tools/init-brand-repo.ps1 `
  -BrandSlug "my-brand" `
  -BrandName "My Brand" `
  -Destination ".\brands\my-brand" `
  -InitialSetCount 8 `
  -BrandType generic `
  -ProductItemType static-emoji

./tools/validate-brand-repo.ps1 ".\brands\my-brand"
```

Add production assets before packaging:

```text
brands/my-brand/releases/release-001/production/tab/source-tab.png
brands/my-brand/releases/release-001/production/finals/*.png
```

For static sticker releases, also add:

```text
brands/my-brand/releases/release-001/production/main/source-main.png
```

Production final filenames can be arbitrary. The package tool normalizes static emoji submission filenames to `001.png`, `002.png`, ... and `tab.png`; static sticker releases use `01.png`, `02.png`, ..., `main.png`, and `tab.png`.

```powershell
python ./tools/package-release.py ".\brands\my-brand" `
  --release-id release-001 `
  --target both `
  --clean

./tools/validate-brand-repo.ps1 ".\brands\my-brand"
```

Generate a readability contact sheet after packaging:

```powershell
python ./tools/validate-assets.py ".\brands\my-brand\releases\release-001\submission\line-upload\images" `
  --expected-count 8 `
  --stage submission `
  --preview-contact-sheet ".\brands\my-brand\releases\release-001\qa\contact-sheet.png" `
  --preview-chat-sheet ".\brands\my-brand\releases\release-001\qa\chat-preview.png" `
  --report-json ".\brands\my-brand\releases\release-001\qa\asset-validation.json"
```

The generated submission outputs are intentionally split:

- `submission/line-upload/images.zip`: LINE upload ZIP. Images only.
- `submission/internal-archive/package.zip`: internal archive with metadata, reports, asset map, checksums, and snapshots.

## Main Tools

- `tools/init-brand-repo.ps1`: scaffold a brand repo.
- `tools/check-source-integrity.py`: fails collapsed or non-parseable source before weaker compile checks.
- `tools/check-canonical-drift.py`: fails old skills, old root templates, or old scaffold entrypoints in canonical scope.
- `tools/check-data-files.py`: parses YAML, workflow YAML, JSON schema files, and dependency lines.
- `tools/validate-brand-repo.py`: manifest-driven brand repo validation.
- `tools/validate-brand-repo.ps1`: PowerShell wrapper for the Python validator.
- `tools/validate-assets.py`: static emoji, static sticker, and APNG emoji validation, submission filename checks, contact sheet previews, chat previews, and report JSON.
- `workflows/series-development-workflow.md`: new-series inheritance, differentiation, and catalog-update flow.
- `workflows/item-generation-workflow.md`: item-by-item GPT / image_gen finalization flow with four-candidate comparison.
- `tools/validate-metadata.py`: LINE metadata length, emoji-character, copyright, and review-risk warning checks.
- `tools/package-release.py`: creates static emoji/sticker line-upload and internal archive packages.
- `tools/check-project-map-paths.py`: validates path references in `PROJECT_MAP.md`.
- `tools/check-example-drift.py`: verifies standalone examples have current embedded schemas, tools, and shared snapshots.

Static emoji and static sticker packaging are the supported release paths. Animation APNG validation is available through `tools/validate-assets.py --asset-type animation-emoji`, but animation release packaging is not implemented in `tools/package-release.py` yet.
Generated brand manifests include `production_profile` so brand canon, series planning, rough / anchor, item finalization, product QA, ledger update, and revision outputs stay explicit and tool-neutral.

## Production Guardrails

- Fill `brand/brand-canon.md` before production.
- For a new series, read `brand/product-catalog.md` and create `releases/<release-id>/series-plan.md`.
- Use rough boards only for direction; do not bulk-generate final products.
- Finalize one item at a time with at least four candidates, then compare and QA.
- Update `brand/product-catalog.md`, `qa/quality-ledger.md`, and `release-log.md` after QA.

## Validation

```powershell
python tools/check-source-integrity.py
python tools/check-canonical-drift.py
python tools/check-data-files.py
python -m compileall tools tests
python tools/validate-schemas.py --check-schemas schemas
python tools/check-project-map-paths.py
python tools/check-example-drift.py examples/soeshirushi
pytest
```

## Example

`examples/soeshirushi` is a standalone generated repo sample at design stage. It is drift-checked against current embedded schemas, tools, and shared snapshots, but it is not production-ready and does not contain final submission images.

## Operating Rule

Judge in this order: `structure -> brand -> product`. If structure fails, do not pass the idea on mood or appeal alone.
