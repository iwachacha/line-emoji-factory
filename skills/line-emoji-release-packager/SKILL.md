---
name: line-emoji-release-packager
description: final assets と metadata からLINE申請用packageを作り、検証、ZIP、checksum、release log更新へ接続する入口。
---

# LINE絵文字 / スタンプ release packager

## Workflow

1. `../../rules/release-packaging-rules.md` を開き、package 前提を確認する。
2. `../../workflows/release-packaging-workflow.md` を開き、手順を固定する。
3. `../../workflows/submission-audit-workflow.md` を通して Hard NG が残っていないか確認する。
4. `../../tools/package-release.py` を使い、package zip と checksum を作る。
5. `release-log.md` と `submission-checklist.md` を更新する。

## Output Rules

- `対象 release / final assets / metadata / validation / package / checksum / release log / 次アクション` を出す。
- validator が落ちる状態で package 完了にしない。
