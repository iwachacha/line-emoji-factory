# 共通制作パイプライン ワークフロー

このファイルは、全ブランド共通で使う制作実装フローの正本である。
このプロジェクトでは、制作方法を
`GPT-image2.0 で高品質なたたき台 / 全体図を大まかに作る → ClaudeDesign へ必要情報を渡し、1つ1つの絵文字として完成させる`
で固定する。

これは `rules/line-platform-baseline.md` の公式事実ではなく、
この工場が採用する内部制作方式の正本である。

## 境界
- このフローは、`構造 → ブランド → 商品` の判断順序を置き換えない。
- 構造で `Fail` した案を、このフローで救済しない。
- 構造 `Fail` は、必ず先に `workflows/transformation-workflow.md` で変換する。
- `GPT-image2.0` はラフと全体図の工程を担う。
- `ClaudeDesign` は受け渡された条件を元に、個別絵文字の完成工程を担う。

## 開始条件
- 少なくとも、構造 `Fail` ではない。
- ブランド核、視覚記号、主要使用場面が揺れすぎていない。
- `Design Ready` 相当まで見えた案だけを本格制作へ送る。

## 制作で固定する正本
- ブランド核: `templates/brand/brand-setting-template.md`
- ブランド共通の制作実装条件: `templates/brand/brand-production-brief-template.md`
- release / set の範囲と差分計画: `templates/release/release-spec-template.md`
- release / set ごとの受け渡し条件: `templates/release/production-handoff-template.md`
- AIへの工程別指示束: `templates/brand/brand-system-prompt-template.md`

## Stage 1: GPT-image2.0 ラフ生成
### 目的
- ブランド核と視覚記号を壊さずに、セット全体の見え方を早く外化する。
- 主要絵文字の方向、差分軸、全体トーン、並びの骨格を先に固定する。

### ここで必ず作るもの
- セット全体図または rough board
- 高頻度絵文字のラフ
- 視覚記号の anchor
- 差分軸の見取り図
- ClaudeDesign へ渡すための不足点メモ

### ここでやってはいけないこと
- ラフの雰囲気だけで、1絵文字ごとの意味不足を隠す。
- 全体図でしか成立しない案を、そのまま通す。
- 1画像単位の弱さを「後で整える」で先送りする。
- ブランド核が曖昧なまま、色味や装飾だけ先に固定する。

### Stage 1 の通過条件
- 主要絵文字が小表示でも読める見込みがある。
- 差分軸が set 全体で重複していない。
- 1絵文字ごとの用途と反応が説明できる。
- ClaudeDesign に渡す共通条件と個別条件を言語化できる。

## Stage 2: ClaudeDesign 仕上げ
### 入力
- `release-spec`
- `brand-setting`
- `brand-production-brief`
- rough board / ラフ画像
- `production-handoff`
- usage validation があればその結果
- 必要なら stage 別 prompt

### ClaudeDesign の責務
- ラフをそのまま清書することではなく、
  LINE絵文字として成立する個別絵文字へ完成させること。
- ただし、ブランド核や set の差分軸を勝手に作り替えない。
- 1絵文字ごとの意味、視認性、差分明確性、セット整合性を仕上げる。

### ClaudeDesign に渡すべき情報
- set 全体で守る核
- 絵文字ごとの用途
- 単体送信時 / 文中使用時 / 連続使用時の役割
- 残す要素と削ってよい要素
- 禁止 drift
- 出力ファイル方針と命名方針

### Stage 2 の通過条件
- 1絵文字単位で意味が成立している。
- 単体送信でも文中使用でも死んでいない。
- rough stage で固定した核と差分軸が保たれている。
- `rules/emoji-product-rules.md` と `rules/review-risk-rules.md` を通る。

## 差し戻しルール
- 問題が `構造不成立` なら、制作工程で直さず `workflows/transformation-workflow.md` へ戻す。
- 問題が brand 核の曖昧さや差分軸崩れなら、Stage 1 へ戻す。
- 問題が個別絵文字の仕上げ品質なら、Stage 2 で修正する。
- 問題の原因が不明瞭なまま、両工程を往復させない。

## Quality Gate
- 提出前と継続改善は `workflows/quality-control-workflow.md` を使う。
- 生成結果の強弱は `workflows/usage-validation-workflow.md` で具体会話に通す。
- 監査結果や運用上の学習は `workflows/continuous-improvement-workflow.md` へ戻す。
- blocking 問題が `release-checklist` に残る間は提出しない。
- `Watch` 項目は `quality-ledger` と release handoff に引き継ぐ。

## release / set ごとの最小出力
- セット仕様: `releases/*/release-spec.md`
- handoff 文書: `releases/*/production-handoff.md`
- release checklist: `qa/release-checklist.md`
- quality ledger: `qa/quality-ledger.md`
- rough board 置き場: `production/rough-boards/`
- 完成データ置き場: `production/finals/`
- release log: `releases/*/release-log.md`
- prompt 蓄積: `prompts/`

## 回答や設計で必ず明示すること
- rough stage で固定するもの
- ClaudeDesign へ渡す単位
- 絵文字ごとの差分軸
- 差し戻し先
- 正本ファイルの更新順
