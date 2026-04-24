---
name: line-emoji-brand-audit-skill-builder
description: LINE絵文字ブランドごとの監査SKILLを作成・改修するスキル。ブランド別 repo や sandbox 内で、絵文字の構想案、rough board、production handoff、完成絵文字、release をそのブランド固有の特徴で監査・評価する auditor SKILL を、共通テンプレートから生成するときに使う。
---

# LINE絵文字ブランド監査SKILL作成

## Overview

ブランド別の絵文字監査SKILLを、共通品質で作るための入口である。
共通ルール本文を再掲せず、ブランド固有の監査 anchor だけを抽出して skill 化する。

## Workflow

1. `../../PROJECT_MAP.md` を開き、skills と templates の責務境界を確認する。
2. `../../workflows/framework-maintenance.md` を開き、skill 追加・改修時の追随更新先を確認する。
3. `../../rules/continuous-improvement-rules.md` を開き、skill 昇格条件と軽量運用原則を確認する。
4. `../../templates/brand-audit-skill-template.md` を開き、ブランド別 auditor SKILL の共通骨格を使う。
5. 対象ブランドの root を決める。標準配置は `<brand-root>/skills/<brand-slug>-emoji-auditor/` とする。
6. 対象ブランドから、最低限 `brand/brand-setting.md`, `brand/brand-production-brief.md`, `brand/brand-system-prompt.md`, `qa/quality-ledger.md` を読む。
7. release や制作物の監査が主用途なら、該当する `emoji-sets/releases/`, `production/handoffs/`, `qa/usage-validations/`, `qa/retrospectives/`, `submissions/release-log.md` も読む。
8. 既存のブランド別 auditor SKILL があるなら、その `SKILL.md` と `agents/openai.yaml` を読んで、新設ではなく改修で足りるか判定する。
9. brand 側の正本が未確定で、監査 anchor を固定できない場合は、先に brand-setting または brand-production-brief の更新へ戻す。
10. template の `[BRAND_*]` と `[AUDIT_*]` を埋め、ブランド固有の `固定条件 / 可変条件 / drift / Watch / NG / 高頻度用途 / 差分軸` を短く入れる。
11. `agents/openai.yaml` を併設し、display name、short description、default prompt をブランド名に合わせる。
12. 作成後、重複するルール本文や長すぎるブランド説明を削り、参照パスと判断順だけで運用できる軽さにする。
13. skill の不足や blind spot が factory 側の再発問題なら、`../../workflows/continuous-improvement-workflow.md` に接続して記録する。

## Common Elements

ブランド別 auditor SKILL に必ず残す共通要素は次の範囲だけにする。

- 判断順序: `構造 → ブランド → 商品`
- 構造 `Fail` 時の戻し先: `transformation-workflow`
- 参照する正本または snapshot の読み順
- 監査対象 stage: 構想案、rough board、handoff、final asset、release 運用
- 出力枠: `監査対象 / 入力 / 構造判定 / ブランド判定 / 商品判定 / リスク / 最終判断 / 修正先 / 記録先 / 次アクション`
- 記録先: brand 側の `quality-ledger`, `release-log`, 必要時のみ factory 側の改善台帳

## Brand-Specific Elements

ブランド別 auditor SKILL へ入れる固有要素は、監査時に毎回読み直すとぶれやすい要点だけに絞る。

- ブランド核と一言定義
- 構造分類、ブランド主型、副型、補助タグ、採用枠
- 小表示で守る視覚記号
- 変えてはいけないもの、変えてよいもの
- 高頻度用途と不得意領域
- 差分軸、重複禁止ルール、上段高頻度枠
- rough / handoff / final で起きやすい drift
- `Hard NG / Revise / Watch` として残す監査論点
- 代替されやすい既存表現と、商品として残す理由

## Decision Rules

- ブランド別 auditor SKILL は、ブランド設定の代替にしない。
- 未確定のブランド核を skill 側で勝手に補完しない。
- 共通ルール本文を貼り直さず、必ず brand repo の snapshot か factory 正本へ参照で戻す。
- 構想案監査と完成物QAを同じ出力枠で扱ってよいが、stage ごとの入力と修正先は分ける。
- 監査観点を増やしすぎて 1 絵文字単位の判断が遅くなる場合は、観点を `blocking / drift / watch` 相当へ圧縮する。
- 既存の汎用監査 skill で足りるなら、新しいブランド別 skill は作らない。

## Output Rules

- すべての回答に `対象 skill / 新設か改修か統合か廃止か / 直す owner file / 軽量化判断 / 次観測点` を含める。
- 作成する場合は、生成先パス、参照した brand 正本、埋めた固有 anchor、残した Watch を明記する。
- factory 側へ戻す改善がある場合は、更新候補の owner file と記録先を明記する。
