# 基盤文書メンテナンスフロー

このファイルは、基盤文書の監査・改訂・再編を行うときの標準手順を定義する。
最小修正で効く改善を優先し、概念ドリフトを防ぐ。

## 正本の持ち場
- `AGENTS.md`
  - 入口とルーティングだけを持つ。
- `PROJECT_MAP.md`
  - ディレクトリ地図と責務境界を持つ。
- `rules/`
  - 用語、制約、評価基準の正本。
- `workflows/`
  - 手順の正本。
- `templates/`
  - 出力項目の正本。
- `skills/`
  - 実務入口の正本。

## 変更種別と更新先
### 新しい評価語彙を追加する
- 先に `rules/evaluation-model.md` を更新する。
- その語を使う `rules/`, `workflows/`, `templates/`, `skills/` を追随更新する。

### 公式仕様や販売運用の事実を更新する
- 先に `rules/line-platform-baseline.md` を更新する。
- `最終確認日` を更新する。
- 影響がある `rules/structure-constraints.md`, `rules/emoji-product-rules.md`, `rules/review-risk-rules.md`, `templates/brand/brand-production-brief-template.md` を追随更新する。

### 既存概念を改名する
- 正本ファイルを先に更新する。
- `PROJECT_MAP.md` と `AGENTS.md` を更新する。
- 依存する `workflows/`, `templates/`, `skills/` の参照を全置換する。

### ワークフローを変える
- `workflows/` を更新する。
- 入口が変わるなら `AGENTS.md` と `skills/` を更新する。

### 継続改善ループを変える
- 先に `rules/continuous-improvement-rules.md` を更新する。
- 次に `workflows/continuous-improvement-workflow.md` を更新する。
- 次に `templates/improvement/factory-improvement-ledger-template.md` を整合させる。
- 入口が変わるなら `skills/line-emoji-factory-auditor/SKILL.md` を更新する。
- 学習機構が重くなる変更なら、削減策も同時に入れる。

### 市場調査つき探索を変える
- 先に `rules/idea-research-rules.md` を更新する。
- 次に `workflows/idea-research-workflow.md` を更新する。
- 次に `templates/market/idea-batch-template.md` を整合させる。
- 通常探索の入口が変わるなら `workflows/consultation-workflow.md` と `skills/line-emoji-router/SKILL.md` を更新する。

### 具体会話検証を変える
- 先に `workflows/usage-validation-workflow.md` を更新する。
- 次に `templates/qa/usage-validation-template.md` を整合させる。
- 品質管理との接続が変わるなら `workflows/quality-control-workflow.md`, `templates/qa/release-checklist-template.md`, `skills/line-emoji-router/SKILL.md` を更新する。

### release 振り返りを変える
- 先に `workflows/release-retrospective-workflow.md` を更新する。
- 次に `templates/qa/release-retrospective-template.md` を整合させる。
- 継続改善との接続が変わるなら `workflows/continuous-improvement-workflow.md`, `templates/release/release-log-template.md`, `skills/line-emoji-factory-auditor/SKILL.md` を更新する。

### 共通制作パイプラインを変える
- 先に `workflows/production-pipeline-workflow.md` を更新する。
- 次に `templates/brand/brand-production-brief-template.md` と `templates/release/production-handoff-template.md` を更新する。
- 次に `templates/release/release-spec-template.md` を整合させる。
- 次に `templates/brand/brand-system-prompt-template.md` を整合させる。
- brand repo へ影響するなら `templates/repo/brand-repo-blueprint.md`, `templates/repo/brand-repo-manifest-template.yaml`, `tools/init-brand-repo.ps1` を更新する。

### 品質管理フローを変える
- 先に `workflows/quality-control-workflow.md` を更新する。
- 次に `templates/qa/release-checklist-template.md`, `templates/qa/quality-ledger-template.md`, `templates/release/release-log-template.md` を更新する。
- brand repo へ影響するなら `templates/repo/brand-repo-blueprint.md`, `templates/repo/brand-repo-manifest-template.yaml`, `tools/init-brand-repo.ps1` を更新する。

### テンプレート項目を変える
- 先に `templates/brand/brand-setting-template.md` を更新する。
- `templates/brand/brand-system-prompt-template.md` を整合させる。
- その項目を参照する `skills/` を更新する。

### skill を追加・改修・整理する
- 先に対象 skill の `SKILL.md` を更新する。
- agent 入口があるなら `agents/openai.yaml` を更新する。
- `AGENTS.md` と `PROJECT_MAP.md` の入口を整合させる。
- 依存する `workflows/` と `templates/` を更新する。
- 重複 skill があるなら、新設ではなく統合や廃止も検討する。

### brand repo の scaffold 出力を変える
- 先に対応する `templates/*-template.*` を更新する。
- script 内の直書きを正本にしない。
- 次に `tools/init-brand-repo.ps1` を更新する。

### ブランド別 repo の雛形を変える
- 先に `templates/repo/brand-repo-blueprint.md` を更新する。
- 次に `templates/repo/brand-repo-manifest-template.yaml` を更新する。
- 自動化している場合は `tools/init-brand-repo.ps1` を更新する。

## 重複検出手順
1. 変更した用語で全文検索する。
2. 同義語や旧称が残っていないか確認する。
3. 似た役割の節が複数ファイルに分散していないか確認する。
4. `rules` と `workflows` で新しい定義を二重管理していないか確認する。

## ドリフト防止チェック
- 構造、ブランド、商品の順序が崩れていないか。
- `構造分類` と `ブランド主型` が混同されていないか。
- `Fail / Revise / Keep / Design Ready` の意味が揃っているか。
- `Hard NG / Revise / Watch` の意味が揃っているか。
- `templates/brand/brand-setting-template.md`, `templates/brand/brand-production-brief-template.md`, `templates/release/production-handoff-template.md` で `templates/brand/brand-system-prompt-template.md` を埋められるか。
- `templates/release/release-spec-template.md`, `templates/qa/release-checklist-template.md`, `templates/qa/quality-ledger-template.md`, `templates/release/release-log-template.md` が `workflows/quality-control-workflow.md` と揃っているか。
- `rules/line-platform-baseline.md` の事実が古くなっていないか。
- ブランド設定だけで止まらず、必要なら `templates/brand/brand-production-brief-template.md` まで落とせるか。
- 共通制作パイプラインが `workflows/production-pipeline-workflow.md`, `templates/repo/brand-repo-blueprint.md`, `tools/init-brand-repo.ps1` で揃っているか。
- 継続品質管理が `workflows/quality-control-workflow.md`, `templates/repo/brand-repo-blueprint.md`, `tools/init-brand-repo.ps1` で揃っているか。
- 継続改善ループが `rules/continuous-improvement-rules.md`, `workflows/continuous-improvement-workflow.md`, `templates/improvement/factory-improvement-ledger-template.md`, `skills/line-emoji-factory-auditor/SKILL.md` で揃っているか。
- 市場調査つき探索が `rules/idea-research-rules.md`, `workflows/idea-research-workflow.md`, `templates/market/idea-batch-template.md`, `skills/line-emoji-router/SKILL.md` で揃っているか。
- 具体会話検証が `workflows/usage-validation-workflow.md`, `templates/qa/usage-validation-template.md`, `workflows/quality-control-workflow.md` で揃っているか。
- release 振り返りが `workflows/release-retrospective-workflow.md`, `templates/qa/release-retrospective-template.md`, `workflows/continuous-improvement-workflow.md` で揃っているか。
- `tools/init-brand-repo.ps1` が release / QA / log 骨格を script 内で二重定義していないか。
- ブランド分離基準が `workflows/brand-lifecycle-workflow.md` と `tools/init-brand-repo.ps1` で揃っているか。
- `skills/` がルール本文を再掲していないか。
- 学習台帳や skill が重くなりすぎていないか。
- `AGENTS.md` が厚い仕様書に戻っていないか。

## 監査時の出力原則
- 問題は重大度順に出す。
- 何が正本で、どこが従属かを明示する。
- 改善案は、最小修正案を先に出す。
- 仕組みが重い場合は、追加案の前に削減案を出す。
