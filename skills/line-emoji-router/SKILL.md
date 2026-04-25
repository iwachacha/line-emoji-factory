---
name: line-emoji-router
description: LINE絵文字 factory の通常入口。依頼内容を読み、構造、ブランド、商品、画像検査、申請監査、固定IP、factory改善のどの入口へ進めるかを決める。自分では重い設計や監査を抱え込まず、正本 workflow と専門 skill へ接続する。
---

# LINE絵文字 router

## Overview

ユーザー依頼を適切な入口へ振り分ける。
`line-emoji-producer` の巨大責務を持ち込まず、読む順序と接続先だけを決める。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と標準処理順を確認する。
2. `../../workflows/consultation-workflow.md` を開き、通常相談の `探索 / 評価 / 設計` を判定する。
3. 先に `../../rules/line-platform-baseline.md` と `../../rules/structure-constraints.md` で、公式仕様と構造成立性を確認する。
4. 構造で `Fail` したら、`../../workflows/transformation-workflow.md` へ進む。
5. 市場観測が必要なら `../line-emoji-market-scout/SKILL.md` へ接続する。
6. ブランド核を作るなら `../line-emoji-brand-distiller/SKILL.md` へ接続する。
7. set 構成なら `../line-emoji-set-architect/SKILL.md` へ接続する。
8. rough / final / handoff 管理なら `../line-emoji-production-director/SKILL.md` へ接続する。
9. 実画像検査なら `../line-emoji-asset-validator/SKILL.md` へ接続する。
10. LINE申請前監査なら `../line-emoji-submission-auditor/SKILL.md` へ接続する。
11. 申請 package 作成なら `../line-emoji-release-packager/SKILL.md` へ接続する。
12. 固定IP案件なら `../line-emoji-ip-governor/SKILL.md` へ接続する。
13. 公開後学習なら `../line-emoji-post-release-analyst/SKILL.md` へ接続する。
14. factory 改善、文書監査、skill 整理なら `../line-emoji-factory-auditor/SKILL.md` へ接続する。
15. ブランド repo 分離なら `../../templates/repo/brand-repo-blueprint.md` と `../../tools/init-brand-repo.ps1` を使う。

## Output Rules

- すべての回答で `モード / 構造判定 / ブランド判定 / 商品判定 / 最終判断 / 次アクション` を使う。
- `最終判断` は `Fail / Revise / Keep / Design Ready` の4値だけを使う。
- 画像検査、申請監査、固定IP統制、factory改善を router 内で抱え込まない。
- ルール本文を再掲せず、owner file を示す。
