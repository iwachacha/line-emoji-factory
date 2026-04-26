# 固定IP制作ワークフロー

このファイルは、許諾済み固定IPをLINE絵文字 / スタンプとして制作するときの標準手順を定義する。

## 起動条件
- 固定キャラクター、企業キャラクター、コラボIP、既存ブランド資産を使う。
- 権利者レビューや承認ログが必要。
- 参照素材の扱いに制限がある。

## 使う正本
- IP統制: `rules/ip-governance-rules.md`
- 審査リスク: `rules/review-risk-rules.md`
- 公式仕様: `rules/line-platform-baseline.md`
- IP style bible: `templates/ip/ip-style-bible-template.md`
- brand canon: `templates/brand/brand-canon-template.md`
- reference register: `templates/ip/reference-asset-register-template.md`
- approval log: `templates/ip/ip-approval-log-template.md`

## 標準手順
1. 使用許諾範囲を確認する。
2. 使用可能キャラクター、ロゴ、モチーフ、禁止事項を `ip-style-bible.md` に固定する。
3. brand canon に、IP として壊してはいけない要素、許容差分、禁止 drift を転記する。
4. 参照素材の出所、使用範囲、AI生成時の扱いを `reference-asset-register.md` に残す。
5. LINE item としての使用場面を `構造 → ブランド → 商品` の順で確認する。
6. release spec と series plan に、固定IPらしさと日常使用の両方を落とす。
7. rough / anchor / item finalization / revision の各段階で、キャラクター崩れと許諾外表現を確認する。
8. 権利者レビューが必要な場合は `ip-approval-log.md` を更新する。
9. 申請前に `workflows/submission-audit-workflow.md` へ接続する。

## 完了条件
- 許諾範囲と禁止事項が明文化されている。
- 使用した参照素材が登録されている。
- 承認が必要な箇所のログが残っている。
- LINE item としての商品使用場面が成立している。
