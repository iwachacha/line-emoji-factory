---
name: line-emoji-set-architect
description: 8/16/24/32/40個のLINE絵文字 / スタンプセット構成、slot、優先用途、次release余白を設計する入口。
---

# LINE絵文字 / スタンプ set architect

## Workflow

1. item type に応じて `../../rules/emoji-product-rules.md` または `../../rules/sticker-product-rules.md` を開き、商品設計判断を確認する。
2. `../../workflows/set-architecture-workflow.md` を開き、set 設計手順を固定する。
3. `../../templates/release/release-spec-template.md` を使う。
4. release spec ができたら `../../workflows/quality-control-workflow.md` Gate 0 へ接続する。

## Output Rules

- `release count / count reason / high-frequency slots / slot map / 重複禁止 / 次release余白` を出す。
- 初期セット個数を「作りやすいから」で決めない。
