---
name: line-emoji-asset-validator
description: LINE絵文字の実画像を、公式仕様、視認性、セット整合性の順で検査する入口。tools/validate-assets.py と品質管理 workflow へ接続する。
---

# LINE絵文字 asset validator

## Workflow

1. `../../PROJECT_MAP.md` を開き、画像検査の正本範囲を確認する。
2. `../../rules/line-platform-baseline.md` で公式仕様を確認する。
3. `../../rules/asset-validation-rules.md` で機械検査と目視検査の境界を確認する。
4. `../../workflows/asset-validation-workflow.md` を開き、検査手順を固定する。
5. release spec と handoff がある場合は、画像数、用途、slot を確認する。
6. `../../tools/validate-assets.py` を実行できる形で対象 path と expected count を決める。
7. `Hard NG / Revise / Watch` で結果を分ける。
8. `Watch` は quality ledger へ接続する。

## Output Rules

- `対象 / 機械検査 / 目視検査 / Hard NG / Revise / Watch / 次アクション` を出す。
- 公式仕様違反を雰囲気で通さない。
- 小サイズ視認性や似すぎは、画像ごとの slot 単位で指摘する。
