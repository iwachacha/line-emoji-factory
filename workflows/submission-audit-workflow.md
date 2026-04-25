# 申請前監査ワークフロー

このファイルは、LINE申請前に画像、metadata、審査リスク、package 完全性を総合監査する標準手順を定義する。

## 起動条件
- release の final asset が揃った。
- metadata 案が出た。
- LINE申請 package 作成前。
- 審査差し戻し後の再提出前。

## 使う正本
- 公式仕様: `rules/line-platform-baseline.md`
- 審査リスク: `rules/review-risk-rules.md`
- 画像検査: `rules/asset-validation-rules.md`
- metadata: `rules/submission-metadata-rules.md`
- 品質管理: `workflows/quality-control-workflow.md`

## 標準手順
1. `release-spec` と `production-handoff` で、提出対象の範囲を確認する。
2. `tools/validate-assets.py` で画像仕様を検査する。
3. `tools/validate-metadata.py` で metadata を検査する。
4. title / description / copyright が絵文字内容と一致しているか確認する。
5. `rules/review-risk-rules.md` で Hard NG / Revise / Watch を確認する。
6. `submission-checklist.md` と `submission-audit-report.md` を更新する。
7. 差し戻しや再提出が発生したら `release-log.md` と `quality-ledger.md` に戻す。

## 完了条件
- 画像と metadata の機械検査が通る。
- Hard NG が残っていない。
- Revise を提出前に処理したか、提出しない判断になっている。
- Watch が quality ledger に移されている。
