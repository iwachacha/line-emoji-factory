# Contribution Guide

## Before Editing
- `PROJECT_MAP.md` で owner file を確認する。
- rules、workflows、templates、schemas、tools、skills の責務を混ぜない。
- 変更後に scaffold smoke test を通す。

## Required Local Checks
```powershell
python ./tools/validate-schemas.py --check-schemas ./schemas
./tools/init-brand-repo.ps1 -BrandSlug "smoke-brand" -BrandName "Smoke Brand" -Destination "$env:TEMP\smoke-brand"
./tools/validate-brand-repo.ps1 "$env:TEMP\smoke-brand"
git diff --check
```

## Push Policy
権限がある場合は commit / push まで行う。
権限がない場合は push 状態と必要な次アクションを明記する。
