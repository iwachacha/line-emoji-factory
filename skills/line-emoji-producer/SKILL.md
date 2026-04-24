---
name: line-emoji-producer
description: LINE絵文字ブランドの通常運用スキル。候補出し、構造判定、比較評価、ブランド設計、絵文字商品設計、初期release設計、制作ハンドオフ設計、品質管理、ブランド専用AI制作指示作成など、通常のブランド相談をこのリポジトリ内で処理するときに使う。
---

# LINE絵文字ブランド運用

## Overview

通常のブランド相談を、探索・評価・設計の3モードで処理する。
ルール本文を再掲せず、正本ファイルへ順に辿る。

## Workflow

1. `../../PROJECT_MAP.md` を開き、正本範囲と相談の標準処理順を確認する。
2. `../../workflows/consultation-workflow.md` を開き、`探索 / 評価 / 設計` のどのモードで処理するか決める。
3. 探索モードで新規案出しや市場調査が必要なら `../../workflows/idea-research-workflow.md` を起動する。
4. 最初に `../../rules/line-platform-baseline.md` を読み、公式仕様と表示事実を確認する。
5. その上で `../../rules/structure-constraints.md` で構造を判定する。
6. 構造で `Fail` したら、`../../workflows/transformation-workflow.md` へ進み、変換案を返す。
7. 構造通過後に、`../../rules/brand-taxonomy.md` と `../../rules/brand-creation-rules.md` でブランドを判断する。
8. その後 `../../rules/emoji-product-rules.md` と `../../rules/review-risk-rules.md` で商品とリスクを判断する。
9. `../../rules/evaluation-model.md` の語と判定状態だけで結論を出す。
10. `Design Ready` なら `../../templates/brand-setting-template.md` を埋める。
11. ブランドスタートアップセットを一式化するなら `../../workflows/brand-startup-set-workflow.md` を使う。
12. 制作へ進める場合は `../../workflows/production-pipeline-workflow.md` で共通制作フローを固定する。
13. ブランド固有制作基盤が必要なら `../../templates/brand-production-brief-template.md` を埋める。
14. 初期 release / set が必要なら `../../templates/release-spec-template.md` を埋める。
15. 品質管理が必要なら `../../workflows/quality-control-workflow.md` と `../../templates/release-checklist-template.md`, `../../templates/quality-ledger-template.md`, `../../templates/release-log-template.md` を初期化する。
16. 実会話での勝ち筋確認が必要なら `../../workflows/usage-validation-workflow.md` と `../../templates/usage-validation-template.md` を使う。
17. release / set ごとの handoff が必要なら `../../templates/production-handoff-template.md` を埋める。
18. ブランドの継続運用や独立制作が見えたら `../../workflows/brand-lifecycle-workflow.md` を確認する。
19. 分離する場合は `../../templates/brand-repo-blueprint.md` と `../../templates/brand-repo-manifest-template.yaml` を使う。
20. 専用AI制作指示が必要なら `../../templates/brand-system-prompt-template.md` と工程別 prompt template へ転記する。
21. 節目学習を圧縮するなら `../../workflows/release-retrospective-workflow.md` と `../../templates/release-retrospective-template.md` を使う。
22. 作業結果や探索上の癖が見えたら `../../workflows/continuous-improvement-workflow.md` へ接続する。

## Output Rules

- すべての回答に `モード / 構造判定 / ブランド判定 / 商品判定 / 最終判断 / 次アクション` を含める。
- `最終判断` は `Fail / Revise / Keep / Design Ready` の4値だけを使う。
- 構造Failの案を、そのままブランド議論や商品議論へ進めない。
- 設定を濃くする前に、ブランド核と商品転換力を確認する。
- 市場調査を使った場合は、観測日と見た範囲を明示する。
- 作業後に再利用可能な学習が出たら、`../../workflows/continuous-improvement-workflow.md` に戻す。

## Use This Skill For

- 候補出しや探索相談
- 市場調査つきの案出し
- 複数案の比較・選別
- ブランド核と視覚記号の設計
- 絵文字セット構成と差分設計
- 初期 release 設計
- ブランドスタートアップセット化
- 具体会話での使用検証
- 共通制作パイプラインと handoff 設計
- 継続品質管理
- release の節目振り返り
- ブランド別 repo 分離判断
- ブランド専用AI制作指示作成
