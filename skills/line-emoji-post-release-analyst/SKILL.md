---
name: line-emoji-post-release-analyst
description: 公開後の販売、審査結果、使用driftを次releaseとfactory改善へ戻す入口。
---

# LINE絵文字 / スタンプ post release analyst

## Workflow

1. `../../workflows/post-release-learning-workflow.md` を開き、公開後学習の手順を固定する。
2. `../../rules/continuous-improvement-rules.md` で factory 昇格条件を確認する。
3. `../../templates/post-release/post-release-metrics-template.md` と `../../templates/post-release/next-release-recommendation-template.md` を使う。
4. factory common へ戻す場合は `../line-emoji-factory-auditor/SKILL.md` へ接続する。

## Output Rules

- `metrics / review outcome / sold because / did not sell because / next release / factory feedback` を出す。
- 実績データが弱い場合は monitor only にする。
