# ブランドスタートアップセット ワークフロー

このファイルは、`Design Ready` 相当のブランド案を、
制作・QA・審査・継続運用へ進められる starter kit へ変換する標準手順を定義する。

目的は、共通品質を薄めずに、ブランドごとの色を出せる可変域を明示することである。
`構造 → ブランド → 商品` の判断順序は、この workflow でも置き換えない。
固定IP、キャラクター、アニメーション、デコ文字などは optional module として扱い、
ブランドごとに採否を切り分ける。

## 起動条件
- `Fail` ではないブランド案を、制作開始できる状態へ進める。
- `templates/brand-setting-template.md` を埋める段階に入った。
- 初期 release / set、制作 handoff、prompt 束、QA 初期化を一式で揃えたい。
- キャラクターや記号体系を固定IPとして継続制作したい。
- ブランド別 repo へ分離する前に、持ち出せる snapshot と作業正本を固めたい。

## スターターキットの構成
### 共通コア
- `brand-starter-kit`
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
- `sales-package-manifest` の初期枠
- `usage-validation` の初期シート、または実施前なら coverage plan
- `brand-manifest`

### Optional module
- `fixed-ip-bible`
- キャラクター運用メモ
- アニメーション設計
- デコ文字設計
- 季節 / 文化派生設計

### 推奨置き場
- rough board 置き場
- final asset 置き場
- export-ready asset 置き場
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
- 固定IPを持たないブランドでは、キャラクター同一性ではなく、視覚文法と用途境界を固定する。

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
4. `templates/brand-starter-kit-template.md` に、共通コアと optional module の採否を記録する。
5. 固定IPとして扱う場合だけ `workflows/fixed-ip-design-workflow.md` を起動し、`templates/fixed-ip-bible-template.md` に権利、固定要素、可変域、禁止 drift を残す。
6. 固定IPを持たない場合は、`brand-setting` と `brand-production-brief` に、固定する視覚文法、用途境界、禁止 drift を残す。
7. `templates/brand-production-brief-template.md` に、共通固定条件、ブランド可変域、release 可変域、工程責務を落とす。
8. `templates/release-spec-template.md` に、初期 release の目的、買う理由、個数根拠、差分軸、上段高頻度枠を固定する。
9. `workflows/usage-validation-workflow.md` で、単体送信、文中使用、2個連続または左右ペアの coverage plan を作る。
10. `templates/production-handoff-template.md` に、rough から残す要素、削る要素、禁止 drift、個別絵文字仕様を渡す。
11. `templates/brand-system-prompt-template.md` と工程別 prompt template を、brand-starter-kit / brand-setting / optional fixed-ip-bible / production-brief / release-spec / handoff から転記して埋める。
12. `templates/release-checklist-template.md`, `templates/quality-ledger-template.md`, `templates/release-log-template.md`, `templates/sales-package-manifest-template.md` を初期化する。
13. 完成 asset が揃ったら `workflows/sales-ready-package-workflow.md` で販売直前パッケージを作る。
14. 継続運用や独立制作が見える場合は `workflows/brand-lifecycle-workflow.md` で分離判断を行う。
15. scaffold する場合は `templates/brand-repo-blueprint.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1` の整合を確認する。
16. 再発しうる不足や運用の重さが見えたら `workflows/continuous-improvement-workflow.md` に送る。

## Gate
次のどれかが欠けている場合、スタートアップセット完了とは扱わない。
- ブランド核と商品化の勝ち筋が 1 文で言える。
- 固定IPとして扱う場合、権利の所在と禁止 drift が説明できる。
- 固定IPを持たない場合、視覚文法、用途境界、禁止 drift が説明できる。
- 共通固定条件とブランド可変域が分離されている。
- release 固有コンセプトが、ブランド説明の言い換えだけで終わっていない。
- 初期セット個数の根拠が、公式最小数や作りやすさだけに依存していない。
- 主要絵文字に、単体送信時と文中使用時の意味がある。
- 代替される句読点、既存記号、既存絵文字に対する残す理由がある。
- rough stage と ClaudeDesign stage の責務が分かれている。
- `Watch` と blocking 問題の行き先が決まっている。
- 完成後に asset / metadata / 手作業提出メモを `sales-package-manifest` へ落とせる。

## 出力原則
- 追加の世界観説明より、制作・QA・審査で使える決定を優先する。
- ブランドらしさは、共通品質を緩める理由にしない。
- 共通条件を厚くしすぎて、どのブランドも同じ見え方になる状態を避ける。
- 可変域は「何を変えてよいか」だけでなく「どこから drift か」まで書く。
