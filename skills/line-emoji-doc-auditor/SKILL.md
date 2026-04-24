---
name: line-emoji-doc-auditor
description: LINE絵文字ブランド基盤の文書監査スキル。ドキュメント群の破綻、矛盾、用語衝突、責務重複、欠落、運用上の曖昧さを洗い出し、最小修正で効く改善案や再編案を出すときに使う。
---

# LINE絵文字文書監査

## Overview

基盤文書の監査、再編、保守を行う。
正本の持ち場を崩さず、概念ドリフトを防ぎながら改善する。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と責務境界を確認する。
2. `../../workflows/framework-maintenance.md` を開き、変更種別と更新先を確定する。
3. `../../rules/line-platform-baseline.md` を開き、公式仕様と運用事実の更新要否を確認する。
4. `../../rules/evaluation-model.md` を開き、評価語彙と判定状態を固定する。
5. 継続改善や skill の再編が絡むなら `../../rules/continuous-improvement-rules.md` と `../../workflows/continuous-improvement-workflow.md` を開く。
6. 変更対象の owner file を特定し、そこを先に直す。
7. 依存する `AGENTS.md`, `PROJECT_MAP.md`, `workflows/`, `templates/`, `skills/` を追随更新する。
8. 同義語、旧称、重複節が残っていないか検索で確認する。

## Audit Rules

- 問題は重大度順に出す。
- `構造分類` と `ブランド主型` を混同しない。
- `Fail / Revise / Keep / Design Ready` を勝手に増やさない。
- 改善案は、まず最小修正案を出す。
- ルール本文を `AGENTS.md` や `skills/` に再掲しない。
- 重い仕組みをさらに重くする改修を避ける。
- 自己改善の仕組み自体が重い場合は、削減案を先に出す。

## Use This Skill For

- 文書群の監査
- 用語辞書や判定状態の整理
- ファイル責務の再分配
- ワークフローとテンプレートの接続確認
- ブランドスタートアップセットの正本監査
- 共通制作パイプラインの監査と再編
- 継続品質管理フローと scaffold 正本の監査
- 具体会話検証と release 振り返りの正本監査
- 継続改善ループと学習台帳の軽量化監査
- local skill の肥大化や重複の監査
- 将来のメンテ性を上げる再編案作成
