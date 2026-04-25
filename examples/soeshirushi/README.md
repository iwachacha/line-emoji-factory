# そえしるし

このディレクトリは design-stage example です。
実画像と最終申請 package は未完了のため、production ready 例としては扱いません。
factory の schema / tool / shared snapshot を埋め込んだ standalone generated repo sample として drift check します。

## Entry Points
- Machine-readable manifest: `brand-manifest.yaml`
- Brand source of truth: `brand/brand-setting.md`
- Brand positioning: `brand/brand-positioning.md`
- Production source of truth: `brand/brand-production-brief.md`
- Brand prompt source of truth: `brand/brand-system-prompt.md`
- Market evidence: `market/`
- Shared snapshots: `references/shared/`
- Active release spec: `releases/release-001/release-spec.md`
- Active handoff: `releases/release-001/production-handoff.md`
- Active QA: `releases/release-001/qa/`
- Active submission: `releases/release-001/submission/`

## Status
- Stage: `design-ready`
- Final assets: not ready
- Package: not ready
- Use: ブランド核、初回 release、handoff、QA、申請前不足の読み方を見る参照例

## Validation
```powershell
./tools/validate-brand-repo.ps1 ".\examples\soeshirushi"
python ./tools/validate-metadata.py ".\examples\soeshirushi\releases\release-001\submission\metadata.yaml"
python ./tools/check-example-drift.py ".\examples\soeshirushi"
```

## Operating Rules
- Keep this example focused on brand-specific production and operations.
- Do not treat this as market proof; market evidence is still low confidence.
- Re-sync shared baselines only when official platform changes, review-policy changes, or repeated quality issues require it.
