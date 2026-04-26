# Release Packaging Workflow

This workflow defines how the factory creates submission packages for static emoji and static sticker releases.

## Start Conditions
- The release has a manifest entry with one concrete item type.
- Final production PNGs exist under `releases/<release-id>/production/finals`.
- Companion images exist for the selected item type:
  - Static emoji: `production/tab/source-tab.png`.
  - Static sticker: `production/main/source-main.png` and `production/tab/source-tab.png`.
- Metadata exists at `releases/<release-id>/submission/metadata.yaml`.

## Canonical Inputs
- Packaging rules: `rules/release-packaging-rules.md`
- Submission audit workflow: `workflows/submission-audit-workflow.md`
- Tool: `tools/package-release.py`

## Steps
1. Confirm the release item type and package type from `brand-manifest.yaml`.
2. Confirm the expected set count from the release entry.
3. Run metadata validation.
4. Run production asset validation for the selected item type.
5. Copy final assets into `submission/line-upload/images/` with normalized LINE filenames.
6. Validate normalized submission images and ZIP contents.
7. Create `submission/line-upload/images.zip` with images only.
8. Create `submission/internal-archive/asset-map.json`, `package-report.md`, and `package-checksums.txt`.
9. Create `submission/internal-archive/package.zip` with metadata, report, asset map, checksums, manifest snapshot, and release spec snapshot.
10. Record package creation and validation status in `release-log.md` and the QA ledger.

## Item-Type Filename Rules
- Static emoji content files become `001.png`, `002.png`, ... plus `tab.png`.
- Static sticker content files become `01.png`, `02.png`, ... plus `main.png` and `tab.png`.

## Completion Conditions
- `submission/line-upload/images.zip` exists and contains images only.
- `submission/internal-archive/package.zip` exists.
- Metadata validation passed.
- Asset validation passed for production and submission images.
- ZIP size is under the current item-type limit.
- Release log and QA records describe the package result.
