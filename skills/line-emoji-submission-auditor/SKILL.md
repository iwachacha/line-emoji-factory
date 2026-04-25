---
name: line-emoji-submission-auditor
description: LINE申請前に画像、metadata、review risk、submission folder の完全性を監査する入口。asset validator、metadata validator、submission audit workflow へ接続する。
---

# LINE絵文字 submission auditor

## Workflow

1. `../../PROJECT_MAP.md` を開き、申請前監査の正本範囲を確認する。
2. `../../rules/line-platform-baseline.md` で公式仕様を確認する。
3. `../../rules/submission-metadata-rules.md` で metadata 条件を確認する。
4. `../../rules/review-risk-rules.md` で Hard NG / Revise / Watch を確認する。
5. `../../workflows/submission-audit-workflow.md` を開き、監査手順を固定する。
6. 画像は `../line-emoji-asset-validator/SKILL.md` または `../../tools/validate-assets.py` へ接続する。
7. metadata は `../../tools/validate-metadata.py` で検査する。
8. 結果を `submission-checklist`, `submission-audit-report`, `release-log`, `quality-ledger` に振り分ける。

## Output Rules

- `対象 release / assets / metadata / review risk / package 完全性 / 最終判断 / 次アクション` を出す。
- `Hard NG` が残る場合は提出可能としない。
- `Watch` は提出後に消さず、quality ledger に移す。
