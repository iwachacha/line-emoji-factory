---
name: line-emoji-factory-evolver
description: 作業結果、監査結果、市場観測、skill の詰まりを factory の継続改善へ変換するスキル。brand 固有で止めるか、factory や skill に昇格させるか、軽量化まで含めて閉じるときに使う。
---

# LINE絵文字 factory 継続改善

## Overview

改善を 1 回の修正で終わらせず、
`監査 → owner file 更新 → 記録 → 軽量化 → push`
まで閉じるための入口である。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と責務境界を確認する。
2. `../../rules/continuous-improvement-rules.md` を開き、昇格条件と軽量運用原則を固定する。
3. `../../workflows/continuous-improvement-workflow.md` を開き、改善ループの標準手順を固定する。
4. 品質起点なら `../../workflows/quality-control-workflow.md` を開き、brand 側と factory 側の切り分け軸を揃える。
5. 文書や skill の変更が絡むなら `../../workflows/framework-maintenance.md` を開く。
6. brand 側記録が必要なら `quality-ledger` と `release-log` を更新する。
7. factory 側記録が必要なら repo root の `factory-improvement-ledger.md` を更新する。
8. skill の不足が原因なら `../line-emoji-skill-builder/SKILL.md` に接続する。
9. 閉じる前に、改善の仕組み自体が重くなっていないか確認する。

## Decision Rules

- `構造不成立` が見えたら、改善ではなく `../../workflows/transformation-workflow.md` へ戻す。
- brand 固有で閉じる問題を factory へ過剰昇格させない。
- 再発問題、偏り、skill friction は brand 側だけで抱え込まない。
- 重い台帳、重い workflow、重い skill も改善対象に含める。
- work 完了は、記録更新と remote push 完了まで含む。

## Output Rules

- すべての回答に `起点 / スコープ / 直す owner file / 軽量化判断 / 次観測点 / push 状態` を含める。
- 改善案は、まず最小修正案を出す。
- 学習量を増やすより、再利用できる密度を優先する。
