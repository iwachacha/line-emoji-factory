---
name: line-emoji-production-director
description: brand canon、series planning、rough / anchor、item finalization、revision、handoff を工程profileとして管理し、制作物とrelease specを接続する入口。
---

# LINE絵文字 / スタンプ production director

## Workflow

1. `../../rules/production-profile-rules.md` を開き、工程profileを確認する。
2. `../../workflows/production-pipeline-workflow.md` を開き、制作工程を固定する。
3. 新シリーズなら `../../workflows/series-development-workflow.md` と `../../templates/release/series-plan-template.md` を使う。
4. item finalization なら `../../workflows/item-generation-workflow.md` を開く。
5. `../../templates/release/production-handoff-template.md` を使う。
6. prompt は `../../templates/prompts/rough-generation-template.md`, `../../templates/prompts/item-image-prompt-template.md`, `../../templates/prompts/finalization-template.md`, `../../templates/prompts/revision-template.md` を使う。
7. QA review には `../../templates/prompts/qa-review-template.md` を使う。

## Output Rules

- `brand canon / series 差分 / roughで固定するもの / finalで変えてよいもの / slot別修正 / handoff / Watch` を出す。
- item finalization stage に構造判断やシリーズ企画を押し込まない。
- 1アイテム4案比較と小表示 QA を明示する。
