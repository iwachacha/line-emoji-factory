---
name: line-emoji-skill-builder
description: LINE絵文字 factory の local skill を追加・改修・整理するスキル。必要な入口が欠けたときや、既存 skill が重い / 曖昧 / 重複しているときに使う。
---

# LINE絵文字 skill 育成

## Overview

repo 内の skill を、自己改善ループで育てるための入口である。
足すだけでなく、まとめる、削る、薄くする判断も行う。

## Workflow

1. `../../PROJECT_MAP.md` を開き、skills の責務を確認する。
2. `../../workflows/framework-maintenance.md` を開き、owner file の更新順を固定する。
3. `../../rules/continuous-improvement-rules.md` を開き、skill 昇格条件と軽量運用原則を固定する。
4. 対象 skill が既存なら、その `SKILL.md` と `agents/openai.yaml` を読む。
5. 新設か改修か統合か廃止かを決める。
6. ブランド別の監査SKILL作成なら、`../line-emoji-brand-audit-skill-builder/SKILL.md` に接続する。
7. skill 本文には、読む順序、接続先、判断原則だけを書く。
8. ルール本文や workflow 本文を skill に再掲しない。
9. skill を足したり変えたりしたら、`AGENTS.md`, `PROJECT_MAP.md`, 依存する workflow を追随更新する。
10. 重い skill になったら、先に節を削るか既存 skill へ統合できないか確認する。

## Decision Rules

- 新しい skill は、繰り返し使う distinct な入口があるときだけ作る。
- 一時的な事情や単発相談のためだけに skill を増やさない。
- 既存 skill の責務追加で足りるなら、新設しない。
- 既存 2 skill 以上と強く重なるなら、統合や役割再分配を先に考える。
- heavy だと判定した skill は、機能追加より先に薄くする。

## Output Rules

- すべての回答に `対象 skill / 新設か改修か統合か廃止か / 直す owner file / 軽量化判断 / 次観測点` を含める。
- agent 定義が必要なら `agents/openai.yaml` まで揃える。
