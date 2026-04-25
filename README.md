# line-emoji-factory

LINE 絵文字ブランドを、構造、ブランド、商品の順で評価し、制作、検証、申請準備まで運用するための factory リポジトリです。

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
  -BrandName "マイブランド" `
  -Destination ".\brands\my-brand" `
  -InitialSetCount 8

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
- `tools/validate-brand-repo.py`: manifest-driven brand repo validation.
- `tools/validate-brand-repo.ps1`: PowerShell wrapper for the Python validator.
- `tools/validate-assets.py`: static PNG and APNG validation, submission filename checks, and contact sheet previews.
- `tools/validate-metadata.py`: LINE metadata length, emoji, copyright, and review-risk warning checks.
- `tools/package-release.py`: creates static line-upload and internal archive packages.
- `tools/check-project-map-paths.py`: validates path references in `PROJECT_MAP.md`.
- `tools/check-example-drift.py`: verifies standalone examples have current embedded schemas, tools, and shared snapshots.

Animation APNG validation is available through `tools/validate-assets.py --asset-type animation`. Animation release packaging is not implemented in `tools/package-release.py` yet.
Generated brand manifests include `production_profile` so rough, finalization, and revision outputs stay explicit and tool-neutral.

## Validation

```powershell
python -m compileall tools
python tools/validate-schemas.py --check-schemas schemas
python tools/check-project-map-paths.py
python tools/check-example-drift.py examples/soeshirushi
pytest
```

## Example

`examples/soeshirushi` is a standalone generated repo sample at design stage. It is drift-checked against current embedded schemas, tools, and shared snapshots, but it is not production-ready and does not contain final submission images.

## Operating Rule

判断順序は常に `構造 → ブランド → 商品` です。構造が成立しない案は、魅力や雰囲気だけでは通しません。
