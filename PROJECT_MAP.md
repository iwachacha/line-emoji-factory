# LINE絵文字ブランド基盤 プロジェクトマップ

このリポジトリの正本は、番号付きドキュメントではなく、
`AGENTS.md / PROJECT_MAP.md / rules/ / workflows/ / templates/ / schemas/ / tools/ / skills/`
の8層で運用する。

## 最上位原則
1. まず構造
2. 次にブランド
3. 最後に商品

## ディレクトリ構造
- `AGENTS.md`
  - 最薄のオーケストレーター。入口と非交渉原則だけを持つ。
- `PROJECT_MAP.md`
  - リポジトリ全体の地図。正本範囲、標準処理順、責務境界を定義する。
- `docs/`
  - 人間向けの quickstart、architecture、運用ガイドを持つ。判断基準の正本にはしない。
- `rules/`
  - 何を守るかを定義する。公式仕様、構造、評価語彙、商品、リスク、schema、IP、市場観測の判断基準を持つ。
- `workflows/`
  - どう進めるかを定義する。相談、制作、品質管理、検査、申請前監査、継続改善、固定IP運用の手順を持つ。
- `templates/`
  - 何を成果物として残すかを定義する。brand、release、QA、market、submission、IP の出力骨格を持つ。
- `schemas/`
  - 成果物の機械検証契約を持つ。
- `tools/`
  - scaffold、schema 検証、画像検査、metadata 検査、placeholder 検査を実行する。
- `skills/`
  - 依頼の入口と、読む正本の順序を指示する。
- `examples/`
  - 参照例を置く。production ready ではなく段階を明示する。
- `sandbox/`
  - 壊してよい実験場を置く。

## 正本範囲
- 用語定義と判定状態: `rules/evaluation-model.md`
- 公式仕様と運用事実: `rules/line-platform-baseline.md`
- 構造分類: `rules/structure-constraints.md`
- ブランド主型 / 副型 / 補助タグ / 採用枠: `rules/brand-taxonomy.md`
- 継続改善の昇格判断: `rules/continuous-improvement-rules.md`
- 市場調査つき探索の判断: `rules/idea-research-rules.md`
- 画像検査判断: `rules/asset-validation-rules.md`
- 申請 metadata 判断: `rules/submission-metadata-rules.md`
- 固定IP統制判断: `rules/ip-governance-rules.md`
- 市場観測証跡判断: `rules/market-observation-rules.md`
- schema 契約判断: `rules/schema-contract-rules.md`
- release package 判断: `rules/release-packaging-rules.md`
- 制作 profile 判断: `rules/production-profile-rules.md`
- 相談モード: `workflows/consultation-workflow.md`
- 共通制作パイプライン: `workflows/production-pipeline-workflow.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 構造Fail時の救済処理: `workflows/transformation-workflow.md`
- 継続改善: `workflows/continuous-improvement-workflow.md`
- 市場調査つき探索: `workflows/idea-research-workflow.md`
- 具体会話検証: `workflows/usage-validation-workflow.md`
- release 振り返り: `workflows/release-retrospective-workflow.md`
- ブランドの残留 / 分離判断: `workflows/brand-lifecycle-workflow.md`
- schema 検証: `workflows/schema-validation-workflow.md`
- 画像検査: `workflows/asset-validation-workflow.md`
- 申請前監査: `workflows/submission-audit-workflow.md`
- 固定IP制作: `workflows/ip-production-workflow.md`
- 市場観測: `workflows/market-observation-workflow.md`
- ブランド抽出: `workflows/brand-distillation-workflow.md`
- set 設計: `workflows/set-architecture-workflow.md`
- release package: `workflows/release-packaging-workflow.md`
- 公開後学習: `workflows/post-release-learning-workflow.md`
- CI保守: `workflows/ci-maintenance-workflow.md`
- ブランド設定項目: `templates/brand/brand-setting-template.md`
- ブランド位置づけ項目: `templates/brand/brand-positioning-template.md`
- ブランド固有制作基盤: `templates/brand/brand-production-brief-template.md`
- release 設計項目: `templates/release/release-spec-template.md`
- 制作ハンドオフ項目: `templates/release/production-handoff-template.md`
- release QA 項目: `templates/qa/release-checklist-template.md`
- 品質台帳項目: `templates/qa/quality-ledger-template.md`
- factory 改善台帳項目: `templates/improvement/factory-improvement-ledger-template.md`
- アイデア探索 batch 項目: `templates/market/idea-batch-template.md`
- 具体会話検証項目: `templates/qa/usage-validation-template.md`
- release 振り返り項目: `templates/qa/release-retrospective-template.md`
- 公開 / 審査履歴項目: `templates/release/release-log-template.md`
- ブランド別リポジトリ設計: `templates/repo/brand-repo-blueprint.md`
- ブランド別 manifest: `templates/repo/brand-repo-manifest-template.yaml`
- 専用AI制作指示項目: `templates/brand/brand-system-prompt-template.md`
- 市場観測項目: `templates/market/market-observation-log-template.md`
- 申請 metadata 項目: `templates/submission/submission-metadata-template.yaml`
- 固定IP制作統制項目: `templates/ip/ip-style-bible-template.md`
- 公開後 metrics 項目: `templates/post-release/post-release-metrics-template.md`

## 標準処理順
1. 相談が通常運用、改善監査、文書監査、画像検査、申請前監査、固定IP運用のどれかを判定する。
2. 入口が不明なら `skills/line-emoji-router/SKILL.md` を使う。
3. 市場観測なら `skills/line-emoji-market-scout/SKILL.md` を使う。
4. ブランド核抽出なら `skills/line-emoji-brand-distiller/SKILL.md` を使う。
5. set 構成なら `skills/line-emoji-set-architect/SKILL.md` を使う。
6. 制作工程なら `skills/line-emoji-production-director/SKILL.md` を使う。
7. 実画像の仕様検査なら `skills/line-emoji-asset-validator/SKILL.md` を使う。
8. LINE申請前の総合監査なら `skills/line-emoji-submission-auditor/SKILL.md` を使う。
9. 申請 package 作成なら `skills/line-emoji-release-packager/SKILL.md` を使う。
10. 固定IP案件なら `skills/line-emoji-ip-governor/SKILL.md` を使う。
11. 公開後学習なら `skills/line-emoji-post-release-analyst/SKILL.md` を使う。
12. 改善採否、文書監査、workflow / skill の整理なら `skills/line-emoji-factory-auditor/SKILL.md` を使う。
7. 通常運用では `workflows/consultation-workflow.md` に従ってモードを決める。
8. 探索モードで新規案出しや市場調査が必要なら `workflows/idea-research-workflow.md` を起動する。
9. 先に `rules/line-platform-baseline.md` と `rules/structure-constraints.md` で、公式仕様と構造成立性を判定する。
10. 構造でFailしたら `workflows/transformation-workflow.md` に沿って変換案を出す。
11. 構造を通過した案だけ、ブランドと商品を順に評価する。
12. `Design Ready` まで達したら、`templates/brand/brand-setting-template.md` を埋める。
13. 制作へ進める場合は `workflows/production-pipeline-workflow.md` で共通制作フローを固定する。
14. 初期 release / set を切るなら `templates/release/release-spec-template.md` を埋める。
15. 品質管理に入るなら `workflows/quality-control-workflow.md` を起動し、QA と release log を初期化する。
16. 申請前は `tools/validate-assets.py`, `tools/validate-metadata.py`, `workflows/submission-audit-workflow.md` を通す。
17. ブランドの継続運用や独立制作が見えたら `workflows/brand-lifecycle-workflow.md` で残留 / 分離を決める。
18. 分離する場合は `templates/repo/brand-repo-blueprint.md`, `templates/repo/brand-repo-manifest-template.yaml`, `tools/init-brand-repo.ps1` を使う。
19. 作業結果、監査結果、市場観測、skill friction は `workflows/continuous-improvement-workflow.md` に接続して、記録、昇格判断、軽量化判断まで閉じる。
20. 作業完了は、必要な owner file 更新、記録更新、検証、push 状態の明記まで含む。

## 責務境界
- `rules/` は「何を守るか」を定義する。手順は書かない。
- `workflows/` は「どう進めるか」を定義する。新しい評価語彙は作らない。
- `templates/` は「何を出力に残すか」を定義する。独自の判断基準は作らない。
- `schemas/` は「どの機械可読成果物をどう検証するか」を定義する。運用手順は書かない。
- `tools/` は「検査と生成を実行する」。判断基準を正本化しない。
- `skills/` は「どの入口で何を読むか」を指示する。ルール本文は再掲しない。
- `factory-improvement-ledger.md` は運用記録であり、正本ではない。項目正本は `templates/improvement/factory-improvement-ledger-template.md` に置く。

## 禁止
- かわいいから通す
- 世界観があるから通す
- 面白いから通す
- 構造Failの案を、そのまま商品議論へ進める
- 同じ概念を別名で増やす
- 学習の仕組みを、運用価値より重くする
- schema や validator を文書だけで置き、CI や scaffold に接続しない
# Current Implementation Addendum

- `requirements-dev.txt`: local and CI validation dependencies.
- `tests/`: pytest coverage for packaging, asset validation, metadata validation, and manifest-driven brand repo validation.
- `tools/validate-brand-repo.py`: canonical manifest-driven validator.
- `tools/validate-brand-repo.ps1`: PowerShell wrapper.
- `tools/package-release.py`: creates separated `submission/line-upload/images.zip` and `submission/internal-archive/package.zip`.
- `tools/validate-assets.py`: validates static PNG and APNG assets and can generate contact sheet previews.
- `tools/check-project-map-paths.py`: verifies path references in this map.
