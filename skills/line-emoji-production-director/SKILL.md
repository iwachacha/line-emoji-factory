---
name: line-emoji-production-director
description: rough、finalization、revision、handoff を工程profileとして管理し、制作物とrelease specを接続する入口。
---

# LINE絵文字 production director

## Workflow

1. `../../rules/production-profile-rules.md` を開き、工程profileを確認する。
2. `../../workflows/production-pipeline-workflow.md` を開き、制作工程を固定する。
3. `../../templates/release/production-handoff-template.md` を使う。
4. prompt は `../../templates/prompts/rough-generation-template.md`, `../../templates/prompts/finalization-template.md`, `../../templates/prompts/revision-template.md` を使う。
5. QA review には `../../templates/prompts/qa-review-template.md` を使う。

## Output Rules

- `roughで固定するもの / finalで変えてよいもの / slot別修正 / handoff / Watch` を出す。
- finalization stage に構造判断を押し込まない。
