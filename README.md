# line-emoji-factory

LINE絵文字ブランドを、`構造 → ブランド → 商品` の順で設計・評価・改善するための factory repo です。

## 入口
- 全体地図: `PROJECT_MAP.md`
- オーケストレーター指示: `AGENTS.md`
- 通常のブランド相談: `skills/line-emoji-producer/SKILL.md`
- 改善監査: `skills/line-emoji-improvement-auditor/SKILL.md`
- 文書監査: `skills/line-emoji-doc-auditor/SKILL.md`
- 継続改善: `skills/line-emoji-factory-evolver/SKILL.md`

## よく使う正本
- 公式仕様と表示事実: `rules/line-platform-baseline.md`
- 構造成立性: `rules/structure-constraints.md`
- 評価語彙: `rules/evaluation-model.md`
- ブランドスタートアップセット: `workflows/brand-startup-set-workflow.md`
- 固定IP設計: `workflows/fixed-ip-design-workflow.md`
- 共通制作パイプライン: `workflows/production-pipeline-workflow.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 販売直前パッケージ: `workflows/sales-ready-package-workflow.md`

## brand repo scaffold
```powershell
.\scripts\init-brand-repo.ps1 -BrandSlug your-brand-slug -BrandName "Your Brand Name" -Destination ..\your-brand-repo
```

固定IPバイブルを初期生成する場合は `-IncludeFixedIp` を付けます。
