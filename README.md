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

The generated submission outputs are intentionally split:

- `submission/line-upload/images.zip`: LINE upload ZIP. Images only.
- `submission/internal-archive/package.zip`: internal archive with metadata, reports, asset map, checksums, and snapshots.

## Main Tools

- `tools/init-brand-repo.ps1`: scaffold a brand repo.
- `tools/validate-brand-repo.py`: manifest-driven brand repo validation.
- `tools/validate-brand-repo.ps1`: PowerShell wrapper for the Python validator.
- `tools/validate-assets.py`: static emoji image validation, including submission filename checks.
- `tools/validate-metadata.py`: LINE metadata length, emoji, copyright, and review-risk warning checks.
- `tools/package-release.py`: creates line-upload and internal archive packages.
- `tools/check-project-map-paths.py`: validates path references in `PROJECT_MAP.md`.

## Validation

```powershell
python -m compileall tools
python tools/validate-schemas.py --check-schemas schemas
python tools/check-project-map-paths.py
pytest
```

## Example

`examples/soeshirushi` is a design-stage reference. It is not production-ready and does not contain final submission images.

## Operating Rule

判断順序は常に `構造 → ブランド → 商品` です。構造が成立しない案は、魅力や雰囲気だけでは通しません。
