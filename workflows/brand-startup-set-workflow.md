# ブランドスタートアップセット ワークフロー

このファイルは、`Design Ready` 相当のブランド案を、
制作・QA・審査・継続運用へ進められる最小一式へ変換する標準手順を定義する。

目的は、共通品質を薄めずに、ブランドごとの色を出せる可変域を明示することである。
`構造 → ブランド → 商品` の判断順序は、この workflow でも置き換えない。

## 起動条件
- `Fail` ではないブランド案を、制作開始できる状態へ進める。
- `templates/brand-setting-template.md` を埋める段階に入った。
- 初期 release / set、制作 handoff、prompt 束、QA 初期化を一式で揃えたい。
- ブランド別 repo へ分離する前に、持ち出せる snapshot と作業正本を固めたい。

## スタートアップセットの最小構成
### 必須
- `brand-setting`
- `brand-production-brief`
- 初期 `release-spec`
- 初期 `production-handoff`
- `brand-system-prompt`
- `gpt-image2-rough-prompts`
- `claude-design-prompts`
- `revision-prompts`
- `release-checklist`
- `quality-ledger`
- `release-log`
- `usage-validation` の初期シート、または実施前なら coverage plan
- `brand-manifest`

### 推奨
- rough board 置き場
- final asset 置き場
- milestone ごとの `release-retrospective`
- factory snapshot の参照一覧

## 共通固定条件とブランド可変域
### 共通固定条件
- LINE 公式仕様、画像仕様、パッケージ数、metadata 制約を守る。
- 1画像単位の意味成立、単体送信、文中使用、連続使用の確認を省かない。
- 固定制作パイプラインは `GPT-image2.0 rough → ClaudeDesign finish` とする。
- `Hard NG` と blocking `Revise` は提出前に止める。
- `Watch` は `quality-ledger` と handoff に残す。
- 審査、提出、公開、差し戻しの履歴を `release-log` に残す。

### ブランド可変域
- 視覚記号、線の性格、余白感、装飾密度、温度感、反応語彙。
- 主力枠と補助枠の比率。ただし高頻度用途を圧迫しない。
- キャラクター、モチーフ、記号、図形・抽象、デコ文字ごとの表現文法。
- 市場で混みやすい表現を避けるための尖り方。
- 季節、文化、実用品タグの使い方。

### release 可変域
- release 固有コンセプト。
- 初期セット個数とその根拠。
- 個別絵文字の用途、並び順、差分軸。
- サジェスト表示タグ候補。
- 今回だけ検証する会話シーン。

## 標準手順
1. `rules/line-platform-baseline.md` と `rules/structure-constraints.md` で、公式仕様と構造が崩れていないか確認する。
2. `rules/brand-creation-rules.md` と `rules/emoji-product-rules.md` で、ブランド核と商品転換力を再確認する。
3. `templates/brand-setting-template.md` に、ブランド核、視覚記号、絶対条件、可変条件、NG 表現を固定する。
4. `templates/brand-production-brief-template.md` に、共通固定条件、ブランド可変域、release 可変域、工程責務を落とす。
5. `templates/release-spec-template.md` に、初期 release の目的、買う理由、個数根拠、差分軸、上段高頻度枠を固定する。
6. `workflows/usage-validation-workflow.md` で、単体送信、文中使用、2個連続または左右ペアの coverage plan を作る。
7. `templates/production-handoff-template.md` に、rough から残す要素、削る要素、禁止 drift、個別絵文字仕様を渡す。
8. `templates/brand-system-prompt-template.md` と工程別 prompt template を、brand-setting / production-brief / release-spec / handoff から転記して埋める。
9. `templates/release-checklist-template.md`, `templates/quality-ledger-template.md`, `templates/release-log-template.md` を初期化する。
10. 継続運用や独立制作が見える場合は `workflows/brand-lifecycle-workflow.md` で分離判断を行う。
11. scaffold する場合は `templates/brand-repo-blueprint.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1` の整合を確認する。
12. 再発しうる不足や運用の重さが見えたら `workflows/continuous-improvement-workflow.md` に送る。

## Gate
次のどれかが欠けている場合、スタートアップセット完了とは扱わない。
- ブランド核と商品化の勝ち筋が 1 文で言える。
- 共通固定条件とブランド可変域が分離されている。
- release 固有コンセプトが、ブランド説明の言い換えだけで終わっていない。
- 初期セット個数の根拠が、公式最小数や作りやすさだけに依存していない。
- 主要絵文字に、単体送信時と文中使用時の意味がある。
- 代替される句読点、既存記号、既存絵文字に対する残す理由がある。
- rough stage と ClaudeDesign stage の責務が分かれている。
- `Watch` と blocking 問題の行き先が決まっている。

## 出力原則
- 追加の世界観説明より、制作・QA・審査で使える決定を優先する。
- ブランドらしさは、共通品質を緩める理由にしない。
- 共通条件を厚くしすぎて、どのブランドも同じ見え方になる状態を避ける。
- 可変域は「何を変えてよいか」だけでなく「どこから drift か」まで書く。
