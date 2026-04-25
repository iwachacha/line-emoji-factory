---
name: line-emoji-ip-governor
description: 固定IP、企業キャラクター、コラボIPをLINE絵文字として扱うときに、許諾範囲、参照素材、禁止表現、承認ログを統制する入口。
---

# LINE絵文字 IP governor

## Workflow

1. `../../PROJECT_MAP.md` を開き、固定IP制作の正本範囲を確認する。
2. `../../rules/ip-governance-rules.md` を開き、許諾範囲と禁止事項を確認する。
3. `../../rules/review-risk-rules.md` で審査・権利リスクを確認する。
4. `../../workflows/ip-production-workflow.md` を開き、制作手順を固定する。
5. `../../templates/ip/ip-style-bible-template.md` を使い、固定仕様を作る。
6. `../../templates/ip/reference-asset-register-template.md` を使い、参照素材を登録する。
7. 権利者確認が必要なら `../../templates/ip/ip-approval-log-template.md` を使う。
8. LINE絵文字としての使用場面は、必ず `構造 → ブランド → 商品` で判定する。

## Output Rules

- `許諾範囲 / 使用可能素材 / 禁止事項 / IPらしさ / LINE絵文字使用場面 / 承認状態 / 次アクション` を出す。
- 許諾範囲が不明な素材は使わない前提で止める。
- IP説明だけ濃く、日常会話で使えない案は `Revise` に落とす。
