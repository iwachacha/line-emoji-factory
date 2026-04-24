---
name: line-emoji-improvement-auditor
description: 既存のLINE絵文字ブランド、release、prompt束、品質台帳、または基盤文書に対する改善案を監査し、採用・保留・却下と反映先を決めるスキル。改善案が本当に LINE絵文字として妥当か、brand 固有修正で足りるか、factory の owner file まで上げるべきかを `構造 → ブランド → 商品` の順で判定するときに使う。
---

# LINE絵文字改善監査

## Overview

既存案を広げるためではなく、改善候補を切り分けるための入口である。
brand 価値向上と factory 再利用価値を分けて判断する。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と責務境界を確認する。
2. `../../workflows/quality-control-workflow.md` を開き、改善論点が brand 固有か factory 問題かの切り分け軸を固定する。
3. `../../rules/continuous-improvement-rules.md` を開き、昇格条件と軽量運用原則を固定する。
4. factory 側へ昇格の可能性がある場合だけ `../../workflows/framework-maintenance.md` を開き、owner file と追随更新先を確定する。
5. factory や skill の学習閉路まで閉じる必要がある場合は `../../workflows/continuous-improvement-workflow.md` を開く。
6. 相談対象の brand repo または設計文書から、最低でも `brand-setting`, `brand-production-brief`, `release-spec`, `production-handoff`, `quality-ledger` を読む。
7. 具体会話の勝ち負けが論点なら `usage-validation` を読む。
8. 改善候補ごとに、必ず `構造 → ブランド → 商品` の順で再評価する。
9. `構造不成立` または `実装前提の誤認` に触れる改善は採らず、必要なら `../../workflows/transformation-workflow.md` へ戻す。
10. 採用する改善は、まず brand 固有修正で足りるかを判定する。次のいずれかを満たすときだけ factory へ上げる。
   - 同種の論点が 2 release 以上または 2 ブランド以上で再発しうる。
   - fixed IP / startup set / sales package / template / workflow / scaffold の項目欠落が原因である。
   - quality ledger だけでは抑えきれず、共通 owner file を変えないと再発する。
11. 採用する改善は最小修正で入れ、brand 側なら `quality-ledger` と `release-log` に反映し、factory 側なら依存する `templates/`, `skills/`, `AGENTS.md`, `PROJECT_MAP.md` を追随更新する。
12. milestone 学習の圧縮が必要なら `../../workflows/release-retrospective-workflow.md` を使う。
13. 改善の仕組み自体が重いと見えたら、追加案ではなく削減案も監査対象に含める。

## Decision Rules

- `かわいくなる`, `世界観が増える` だけの改善は採らない。必ず `商品転換力`, `セット整合性`, `再使用性` に返す。
- `公式最小数だから 8 個でよい` は採らない。`初期セット個数の根拠` が言えないなら `Revise` に落とす。
- 組み合わせ補助枠は自動で却下しない。ただし少数か、単体意味が残るか、上段高頻度枠を圧迫しないかを必ず見る。
- release 固有コンセプトがブランド説明の言い換えだけなら、商品改善としては弱いと見る。
- 改善案が broad でも、既存の評価語彙と判定状態は増やさない。
- 完成 asset を販売直前へ渡す改善では、final candidate と export-ready asset を混ぜない。
- 台帳、workflow、skill が重くなりすぎたこと自体も改善論点として扱う。

## Output Rules

- すべての回答に `監査対象 / 採用 / 保留 / 却下 / factory昇格 / 軽量化判断 / 次観測点` を含める。
- `採用` は brand 固有修正か factory 修正かを明記する。
- `factory昇格` では、更新する owner file と追随更新先を明記する。
- `保留` は、何が観測できたら採るかを1文で書く。
- `却下` は、構造・評価語彙・再利用性のどれで切ったかを明示する。
