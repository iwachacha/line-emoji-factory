# 画像検査ワークフロー

このファイルは、完成画像をLINE絵文字 / スタンプ仕様と商品品質の両方で検査する標準手順を定義する。

## 起動条件
- final asset が出た。
- 申請 package を作る前。
- 審査差し戻しで画像仕様や視認性が問題になった。

## 使う正本
- 公式仕様: `rules/line-platform-baseline.md`
- 画像検査判断: `rules/asset-validation-rules.md`
- visual QA: `rules/visual-asset-quality-rules.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 画像検査 report: `templates/submission/asset-validation-report-template.md`

## 標準手順
1. release spec と production handoff を読み、画像数と用途を確認する。
2. `tools/validate-assets.py <images-dir> --expected-count <count>` を実行する。
3. tab 画像がある場合は、`--tab-image <path>` を追加する。
4. `--preview-contact-sheet`, `--preview-chat-sheet`, `--report-json` を指定し、`180 / 96 / 48 / 32px` 相当の確認物を残す。
5. 機械検査の `Hard NG` は提出前に必ず止める。
6. 小サイズ視認性、表情差、ポーズ差、用途被り、似すぎ、余白過多、低コントラスト、背景混入を目視で見る。
7. `かわいいが使えない`、`きれいだが会話で使わない` は商品品質の `Revise` として止める。
8. `Revise` は release checklist の blocking 項目へ戻す。
9. `Watch` は quality ledger と product catalog に残す。

## 完了条件
- 公式仕様の blocking 違反がない。
- 検査結果が submission audit へ渡せる。
- 修正が必要な asset が slot 単位で特定されている。
- contact sheet、chat preview、report JSON が保存されている。
