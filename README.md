# line-emoji-factory

LINE emoji brand ideas are evaluated and carried through structure, brand, product, production, validation, and submission packaging. The current packaging pipeline targets static emoji releases.

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
  -BrandType generic

./tools/validate-brand-repo.ps1 ".\brands\my-brand"
```

Add production assets before packaging:

```text
brands/my-brand/releases/release-001/production/tab/source-tab.png
brands/my-brand/releases/release-001/production/finals/*.png
```

Production final filenames can be arbitrary. The package tool normalizes submission filenames to `001.png`, `002.png`, ... and `tab.png`.

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
  --preview-contact-sheet ".\brands\my-brand\releases\release-001\qa\contact-sheet.png"
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
- `tools/validate-assets.py`: static PNG and APNG validation, submission filename checks, and contact sheet previews.
- `tools/validate-metadata.py`: LINE metadata length, emoji, copyright, and review-risk warning checks.
- `tools/package-release.py`: creates static line-upload and internal archive packages.
- `tools/check-project-map-paths.py`: validates path references in `PROJECT_MAP.md`.
- `tools/check-example-drift.py`: verifies standalone examples have current embedded schemas, tools, and shared snapshots.

Static emoji packaging is the primary supported release path. Animation APNG validation is available through `tools/validate-assets.py --asset-type animation`, but animation release packaging is not implemented in `tools/package-release.py` yet.
Generated brand manifests include `production_profile` so rough, finalization, and revision outputs stay explicit and tool-neutral.

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
