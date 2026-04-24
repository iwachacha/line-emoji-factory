# [BRAND_NAME]

このリポジトリは、LINE絵文字ブランド `[BRAND_NAME]` の制作、QA、審査、公開運用に集中するためのブランド別 repo です。

## 入口
- ブランド正本: `brand/brand-setting.md`
- スターターキット構成: `brand/brand-starter-kit.md`
- 固定IPバイブル: `brand/fixed-ip-bible.md`（固定IPを使うブランドのみ）
- 制作基盤正本: `brand/brand-production-brief.md`
- ブランド専用AI制作指示: `brand/brand-system-prompt.md`
- 機械可読 manifest: `brand/brand-manifest.yaml`
- 共通基盤 snapshot: `references/shared/`
- release 仕様: `emoji-sets/releases/`
- rough board: `production/rough-boards/`
- handoff: `production/handoffs/`
- final asset: `production/finals/`
- export-ready asset: `production/export-ready/`
- prompt 束: `prompts/`
- QA checklist: `qa/release-checklist.md`
- quality ledger: `qa/quality-ledger.md`
- usage validation: `qa/usage-validations/`
- retrospective: `qa/retrospectives/`
- 提出 / 審査 / 公開履歴: `submissions/release-log.md`
- 販売直前 manifest: `submissions/sales-package-manifest.md`

## 運用原則
- `構造 → ブランド → 商品` の順で判断する。
- 固定IPは optional module として扱い、必要なブランドだけ有効にする。
- 共通固定条件、ブランド可変域、release 可変域を混ぜない。
- rough / handoff / final の責務を混ぜない。
- fixed IP、final candidate、export-ready asset の責務を混ぜない。
- `Watch` は `qa/quality-ledger.md` と handoff に残す。
- ユーザー手作業提出前は `submissions/sales-package-manifest.md` を `Ready` にする。
- 審査、差し戻し、修正、公開の履歴は `submissions/release-log.md` に残す。
- factory 更新は自動同期しない。
- 公式仕様変更、審査基準変更、再発品質問題があるときだけ snapshot 再同期を判断する。
- 日常運用の正本は `brand/`, `emoji-sets/`, `production/`, `qa/`, `submissions/` 側の実体文書とする。
