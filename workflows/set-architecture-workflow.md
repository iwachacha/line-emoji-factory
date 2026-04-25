# set architecture ワークフロー

このファイルは、8 / 16 / 24 / 32 / 40個のLINE絵文字 set を設計する標準手順を定義する。

## 起動条件
- 初回 release を切る。
- 既存 release の構成が弱い。
- 高頻度用途、補助枠、遊び枠の配分を決める。

## 使う正本
- 商品設計判断: `rules/emoji-product-rules.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 出力: `templates/release/release-spec-template.md`

## 標準手順
1. 初回 set count と根拠を決める。
2. 最上段の高頻度絵文字を決める。
3. 応答、感情、補助、遊びの配分を決める。
4. 単体送信と文中挿入の両方で用途を確認する。
5. 似すぎ、色違い水増し、任意テキスト依存を取り除く。
6. 次 release に残す余白を明文化する。

## 完了条件
- release spec に count、役割、差分軸、slot が落ちている。
- Gate 0 の品質確認へ進める。
