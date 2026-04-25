---
name: line-emoji-factory-auditor
description: LINE絵文字 factory 全体の改善採否、文書監査、workflow 監査、skill 監査、schema/tool/CI 改善を扱う統合監査入口。
---

# LINE絵文字 factory auditor

## Modes

- `doc_audit`
- `brand_audit`
- `release_audit`
- `workflow_audit`
- `skill_audit`
- `factory_upgrade`

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と責務境界を確認する。
2. `../../workflows/framework-maintenance.md` を開き、変更種別と更新先を確定する。
3. `../../rules/continuous-improvement-rules.md` を開き、昇格条件と軽量運用原則を固定する。
4. 改善候補ごとに、必ず `構造 → ブランド → 商品` の順で再評価する。
5. `構造不成立` または `実装前提の誤認` に触れる改善は採らず、必要なら `../../workflows/transformation-workflow.md` へ戻す。
6. 採用する改善は、brand 固有修正で足りるか factory 修正が必要かを分ける。
7. factory 側へ上げる場合は owner file、追随更新先、検証方法を明記する。
8. schema、tool、CI の変更は `../../workflows/schema-validation-workflow.md` と接続する。
9. 作業結果は `../../factory-improvement-ledger.md` に記録する。
10. 閉じる前に、改善の仕組み自体が重くなっていないか確認する。

## Decision Rules

- `かわいくなる`, `世界観が増える` だけの改善は採らない。
- ルール本文を skill に再掲しない。
- 同じ概念を別名で増やさない。
- 既存 2 skill 以上にまたがる入口の詰まりは、統合か router 化を先に考える。
- schema や validator を追加した場合、CI または scaffold 検証へ接続する。

## Output Rules

- `監査対象 / mode / 採用 / 保留 / 却下 / factory昇格 / owner file / 検証 / push 状態` を出す。
- `保留` は、何が観測できたら採るかを書く。
- `却下` は、構造・評価語彙・再利用性のどれで切ったかを明示する。
