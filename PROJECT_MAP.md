# LINE絵文字ブランド基盤 プロジェクトマップ

このリポジトリの正本は、番号付きドキュメントではなく、
`AGENTS.md / PROJECT_MAP.md / rules/ / workflows/ / templates/ / skills/`
の6層で運用する。

## 最上位原則
1. まず構造
2. 次にブランド
3. 最後に商品

## ディレクトリ構造
- `AGENTS.md`
  - 最薄のオーケストレーター。
  - 役割、非交渉原則、入口、正本参照先だけを持つ。
- `PROJECT_MAP.md`
  - リポジトリ全体の地図。
  - 正本範囲、標準処理順、責務境界を定義する。
- `rules/`
  - 定義と判断基準の正本。
  - 公式仕様、構造、評価語彙、ブランド分類、商品判断、リスク判定、継続改善、市場探索判断を持つ。
- `workflows/`
  - 手順の正本。
  - 相談処理、共通制作フロー、品質管理、変換処理、継続改善、探索手順、具体会話検証、振り返り、文書保守手順、ブランド運用手順を持つ。
- `templates/`
  - 出力骨格の正本。
  - ブランド設定、制作基盤、release 設計、handoff、QA、品質台帳、ブランド別監査SKILL、factory 改善台帳、探索 batch、具体会話検証、release 振り返り、repo 雛形、ブランド専用AI制作指示を持つ。
- `skills/`
  - 実務入口の正本。
  - 通常運用用スキル、改善監査用スキル、文書監査用スキル、継続改善用スキル、skill 育成用スキル、ブランド別監査SKILL作成用スキルを持つ。

## 正本範囲
- 用語定義と判定状態の正本: `rules/evaluation-model.md`
- 公式仕様と運用事実の正本: `rules/line-platform-baseline.md`
- 構造分類の正本: `rules/structure-constraints.md`
- ブランド主型 / 副型 / 補助タグ / 採用枠の正本: `rules/brand-taxonomy.md`
- 継続改善の昇格判断: `rules/continuous-improvement-rules.md`
- 市場調査つき探索の判断: `rules/idea-research-rules.md`
- 相談モードと回答共通ヘッダの正本: `workflows/consultation-workflow.md`
- 共通制作パイプラインの正本: `workflows/production-pipeline-workflow.md`
- 品質管理フローの正本: `workflows/quality-control-workflow.md`
- 構造Fail時の救済処理の正本: `workflows/transformation-workflow.md`
- 継続改善の正本: `workflows/continuous-improvement-workflow.md`
- 市場調査つき探索の正本: `workflows/idea-research-workflow.md`
- 具体会話検証の正本: `workflows/usage-validation-workflow.md`
- release 振り返りの正本: `workflows/release-retrospective-workflow.md`
- ブランドの残留 / 分離判断の正本: `workflows/brand-lifecycle-workflow.md`
- ブランド設定項目の正本: `templates/brand-setting-template.md`
- ブランド固有制作基盤の正本: `templates/brand-production-brief-template.md`
- release 設計項目の正本: `templates/release-spec-template.md`
- 制作ハンドオフ項目の正本: `templates/production-handoff-template.md`
- release QA 項目の正本: `templates/release-checklist-template.md`
- 品質台帳項目の正本: `templates/quality-ledger-template.md`
- ブランド別監査SKILL項目の正本: `templates/brand-audit-skill-template.md`
- factory 改善台帳項目の正本: `templates/factory-improvement-ledger-template.md`
- アイデア探索 batch 項目の正本: `templates/idea-batch-template.md`
- 具体会話検証項目の正本: `templates/usage-validation-template.md`
- release 振り返り項目の正本: `templates/release-retrospective-template.md`
- 公開 / 審査履歴項目の正本: `templates/release-log-template.md`
- ブランド別リポジトリ設計の正本: `templates/brand-repo-blueprint.md`
- ブランド別 manifest の正本: `templates/brand-repo-manifest-template.yaml`
- 専用AI制作指示項目の正本: `templates/brand-system-prompt-template.md`

## 標準処理順
1. 相談が通常運用か改善監査か文書監査かを判定する。
2. 通常運用なら `skills/line-emoji-producer/SKILL.md` を入口にする。
3. 改善監査なら `skills/line-emoji-improvement-auditor/SKILL.md` を入口にする。
4. 文書監査なら `skills/line-emoji-doc-auditor/SKILL.md` を入口にする。
5. 継続改善や作業後の学習閉路を回すなら `skills/line-emoji-factory-evolver/SKILL.md` を入口にする。
6. local skill の不足や肥大化を直すなら `skills/line-emoji-skill-builder/SKILL.md` を入口にする。
7. ブランド別の監査SKILLを作るなら `skills/line-emoji-brand-audit-skill-builder/SKILL.md` を入口にする。
8. 通常運用では `workflows/consultation-workflow.md` に従ってモードを決める。
9. 探索モードで新規案出しや市場調査が必要なら `workflows/idea-research-workflow.md` を起動する。
10. 先に `rules/line-platform-baseline.md` と `rules/structure-constraints.md` で、公式仕様と構造成立性を判定する。
11. 構造でFailしたら `workflows/transformation-workflow.md` に沿って変換案を出す。
12. 構造を通過した案だけ、ブランドと商品を順に評価する。
13. `Design Ready` まで達したら、`templates/brand-setting-template.md` を埋める。
14. 制作へ進める場合は `workflows/production-pipeline-workflow.md` で共通制作フローを固定する。
15. ブランド固有の制作基盤が必要なら `templates/brand-production-brief-template.md` を埋める。
16. 初期 release / set を切るなら `templates/release-spec-template.md` を埋める。
17. 品質管理に入るなら `workflows/quality-control-workflow.md` を起動し、`templates/release-checklist-template.md`, `templates/quality-ledger-template.md`, `templates/release-log-template.md` を初期化する。
18. release / set ごとの handoff が必要なら `templates/production-handoff-template.md` を埋める。
19. 専用AI制作指示が必要なら `templates/brand-system-prompt-template.md` を埋める。
20. 実際の会話文脈での勝ち筋を確認するなら `workflows/usage-validation-workflow.md` を起動する。
21. 提出前と継続運用では `workflows/quality-control-workflow.md` を回し続ける。
22. 節目ごとの学習を圧縮するなら `workflows/release-retrospective-workflow.md` を起動する。
23. 作業結果、監査結果、市場観測、skill friction は `workflows/continuous-improvement-workflow.md` に接続して、記録、昇格判断、軽量化判断まで閉じる。
24. ブランドの継続運用や独立制作が見えたら `workflows/brand-lifecycle-workflow.md` で残留 / 分離を決める。
25. 分離する場合は `templates/brand-repo-blueprint.md` と `templates/brand-repo-manifest-template.yaml` を使う。
26. 作業完了は、必要な owner file 更新、記録更新、remote push 完了まで含む。

## 責務境界
- `rules/` は「何を守るか」を定義する。手順は書かない。
- `workflows/` は「どう進めるか」を定義する。新しい評価語彙は作らない。
- `templates/` は「何を出力に残すか」を定義する。独自の判断基準は作らない。
- `skills/` は「どの入口で何を読むか」を指示する。ルール本文は再掲しない。
- `factory-improvement-ledger.md` は運用記録であり、正本ではない。項目正本は `templates/factory-improvement-ledger-template.md` に置く。

## 禁止
- かわいいから通す
- 世界観があるから通す
- 面白いから通す
- 構造Failの案を、そのまま商品議論へ進める
- 同じ概念を別名で増やす
- 学習の仕組みを、運用価値より重くする
