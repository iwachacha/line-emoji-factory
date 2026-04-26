---
name: line-emoji-router
description: LINE emoji / sticker factory の通常入口。依頼内容を読み、構造、ブランド、商品、画像検査、申請前監査、release package、固定IP、公開後学習、factory監査のどの入口へ進めるかを決める。
---

# line-emoji-router

## Overview

ユーザー依頼を適切な入口へ振り分ける。router は重い制作や監査を抱え込まず、読む順序と接続先だけを決める。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と責務境界を確認する。
2. `../../workflows/consultation-workflow.md` を開き、通常相談、探索、評価、設計のどれに該当するかを決める。
3. 先に `../../rules/line-platform-baseline.md` と `../../rules/structure-constraints.md` で、item type、公式仕様、構造成立性を確認する。
4. 構造で `Fail` した場合は `../../workflows/transformation-workflow.md` へ進む。
5. 市場観測が必要なら `../line-emoji-market-scout/SKILL.md` へ接続する。
6. ブランド核抽出なら `../line-emoji-brand-distiller/SKILL.md` へ接続する。
7. set 構成なら `../line-emoji-set-architect/SKILL.md` へ接続する。
8. rough / final / handoff 管理なら `../line-emoji-production-director/SKILL.md` へ接続する。
9. 実画像検査なら `../line-emoji-asset-validator/SKILL.md` へ接続する。
10. 申請前監査なら `../line-emoji-submission-auditor/SKILL.md` へ接続する。
11. release package 作成なら `../line-emoji-release-packager/SKILL.md` へ接続する。
12. 固定IP案件なら `../line-emoji-ip-governor/SKILL.md` へ接続する。
13. 公開後学習なら `../line-emoji-post-release-analyst/SKILL.md` へ接続する。
14. factory 改善、文書監査、skill 整理なら `../line-emoji-factory-auditor/SKILL.md` へ接続する。
15. ブランド repo 分離なら `../../templates/repo/brand-repo-blueprint.md` と `../../tools/init-brand-repo.ps1` を使う。

## Output Rules

- すべての回答で `mode / structure judgment / brand judgment / product judgment / final decision / next action` を必要な範囲で示す。
- `final decision` は `Fail / Revise / Keep / Design Ready` の4値を使う。
- 画像検査、申請前監査、固定IP統制、factory改善は router 内で抱え込まず、専用 skill へ接続する。
- ルール本文を再発明せず、owner file を示す。
