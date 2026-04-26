---
name: line-emoji-asset-validator
description: LINE絵文字 / スタンプの実画像を、公式仕様、視認性、セット整合性の順で検査する入口。tools/validate-assets.py と品質管理 workflow へ接続する。
---

# LINE絵文字 / スタンプ asset validator

## Workflow

1. `../../PROJECT_MAP.md` を開き、画像検査の正本範囲を確認する。
2. `../../rules/line-platform-baseline.md` で公式仕様を確認する。
3. `../../rules/asset-validation-rules.md` で機械検査と目視検査の境界を確認する。
4. `../../rules/visual-asset-quality-rules.md` で小表示と商品QAの失格条件を確認する。
5. `../../workflows/asset-validation-workflow.md` を開き、検査手順を固定する。
6. release spec と handoff がある場合は、画像数、用途、slot、series 差分を確認する。
7. `../../tools/validate-assets.py` を実行できる形で対象 path、expected count、contact sheet、chat preview、report JSON を決める。
8. `Hard NG / Revise / Watch` で結果を分ける。
9. `Watch` は quality ledger と product catalog へ接続する。

## Output Rules

- `対象 / 機械検査 / 目視検査 / Hard NG / Revise / Watch / 次アクション` を出す。
- 公式仕様違反を雰囲気で通さない。
- 小サイズ視認性や似すぎは、画像ごとの slot 単位で指摘する。
- `かわいいが使えない`、`きれいだが会話で使わない` は商品QAで止める。
