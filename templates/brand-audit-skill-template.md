# ブランド別監査SKILLテンプレート

このテンプレートは、ブランド別 repo または sandbox 内に置く auditor SKILL の骨格である。
`skills/line-emoji-brand-audit-skill-builder/SKILL.md` でブランド固有 anchor を抽出してから使う。

```markdown
---
name: [BRAND_SLUG]-emoji-auditor
description: [BRAND_NAME] のLINE絵文字監査SKILL。[BRAND_NAME] の構想案、rough board、production handoff、完成絵文字、release 運用を、ブランド固有条件と共通評価順 `構造 → ブランド → 商品` で監査・評価するときに使う。
---

# [BRAND_NAME] 絵文字監査

## Overview

`[BRAND_NAME]` の絵文字案と制作物を監査する入口である。
ブランドを広げるためではなく、構造不成立、ブランド drift、商品品質不良、審査・運用リスクを切り分ける。

## Read Order

1. `../../brand/brand-setting.md` を開き、ブランド核と固定条件を確認する。
2. `../../brand/brand-production-brief.md` を開き、制作・商品運用の固定条件を確認する。
3. `../../brand/brand-system-prompt.md` を開き、工程別 AI 指示との整合を見る。
4. release 単位の監査なら `../../emoji-sets/releases/` の該当 release を読む。
5. rough / handoff / final の監査なら、該当する `../../production/rough-boards/`, `../../production/handoffs/`, `../../production/finals/` を読む。
6. 継続論点を確認するため、`../../qa/quality-ledger.md`, `../../qa/release-checklist.md`, `../../qa/usage-validations/`, `../../qa/retrospectives/` を読む。
7. 判定語彙と共通制約は `../../references/shared/evaluation-model.md`, `../../references/shared/line-platform-baseline.md`, `../../references/shared/structure-constraints.md`, `../../references/shared/emoji-product-rules.md`, `../../references/shared/review-risk-rules.md` を使う。
8. 構造 `Fail` なら `../../references/shared/transformation-workflow.md` へ戻す。

## Brand Anchors

- ブランド名: `[BRAND_NAME]`
- 一言定義: `[BRAND_ONE_LINE]`
- 構造分類: `[STRUCTURE_TYPE]`
- ブランド主型: `[BRAND_MAIN_TYPE]`
- ブランド副型: `[BRAND_SUB_TYPE]`
- 補助タグ: `[SUPPORT_TAGS]`
- 採用枠: `[ADOPTION_FRAME]`
- 小表示で守る視覚記号: `[SMALL_SIZE_ANCHORS]`
- 高頻度用途: `[HIGH_FREQUENCY_USES]`
- 不得意領域: `[WEAK_OR_OUT_OF_SCOPE_AREAS]`
- 変えてはいけないもの: `[NON_NEGOTIABLES]`
- 変えてよいもの: `[VARIABLES]`
- 差分軸: `[DIFFERENTIATION_AXES]`
- 重複禁止ルール: `[DUPLICATION_RULES]`
- 代替されやすい既存表現: `[LIKELY_SUBSTITUTES]`
- 商品として残す理由: `[PRODUCT_REASON_TO_EXIST]`

## Stage Audit

### 構想案

- 1画像単位で意味が成立するかを見る。
- `[BRAND_NAME]` の核へ自然に接続しているかを見る。
- 既存表現で足りる案は、商品として残す理由を再確認する。

### Rough Board

- 小表示で `[SMALL_SIZE_ANCHORS]` が残るかを見る。
- set 全体で `[DIFFERENTIATION_AXES]` が読めるかを見る。
- rough 由来の drift: `[ROUGH_DRIFT_POINTS]`

### Production Handoff

- 各絵文字に `用途 / 単体送信時の意味 / 文中使用時の役割` があるかを見る。
- keep / strengthen / trim / risk が `[BRAND_NAME]` 固有条件に沿っているかを見る。
- handoff 由来の drift: `[HANDOFF_DRIFT_POINTS]`

### Final Asset

- 公式仕様、視認性、即読性、差分明確性、セット整合性を確認する。
- 画像を監査する場合は、実物または添付画像を見てから判断する。
- final 由来の drift: `[FINAL_DRIFT_POINTS]`

### Release 運用

- release 固有コンセプトがブランド説明の言い換えだけになっていないかを見る。
- `quality-ledger`, `release-log`, `usage-validation`, `retrospective` に残すべき論点を分ける。
- 再発問題は brand local で閉じるか factory へ戻すか判定する。

## Decision Rules

- 判断順序は常に `構造 → ブランド → 商品`。
- 構造 `Fail` の案は、そのままブランド評価や商品評価へ進めない。
- `[NON_NEGOTIABLES]` を崩す修正は採らない。
- `[VARIABLES]` の範囲なら、商品性を上げる調整として扱う。
- `Hard NG` は即 `Fail` とし、提出や制作継続に進めない。
- `Watch` は潰し切ろうとせず、必要な owner file へ残す。
- 現行市場や人気傾向を根拠にする場合は、観測日と範囲を明示する。

## Output Rules

- すべての回答に `監査対象 / 入力 / 構造判定 / ブランド判定 / 商品判定 / リスク / 最終判断 / 修正先 / 記録先 / 次アクション` を含める。
- `最終判断` は `Fail / Revise / Keep / Design Ready` の4値だけを使う。
- 完成物監査でも独自ステータスを増やさず、提出可否は判断理由として文章で書く。
- 修正先は `brand-setting / brand-production-brief / release-spec / rough board / handoff / final asset / quality-ledger / release-log` から選ぶ。
- factory 側へ戻す場合だけ、`../../references/shared/continuous-improvement-workflow.md` と factory の改善台帳へ接続する。
```
