# Quickstart

## Create a Brand Repo
```powershell
./tools/init-brand-repo.ps1 -BrandSlug "my-brand" -BrandName "マイブランド" -Destination ".\brands\my-brand"
./tools/validate-brand-repo.ps1 ".\brands\my-brand"
```

## Fill First
- `brand/brand-setting.md`
- `brand/brand-positioning.md`
- `brand/brand-production-brief.md`
- `releases/release-001/release-spec.md`
- `releases/release-001/production-handoff.md`
- `releases/release-001/submission/metadata.yaml`

## Validate Before Submission
```powershell
python ./tools/validate-metadata.py ".\brands\my-brand\releases\release-001\submission\metadata.yaml"
python ./tools/validate-assets.py ".\brands\my-brand\releases\release-001\submission\images" --expected-count 8
```

## Package
```powershell
python ./tools/package-release.py ".\brands\my-brand" --expected-count 8
```
