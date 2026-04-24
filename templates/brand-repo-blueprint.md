# ブランド別リポジトリ設計テンプレート

このテンプレートは、ブランド別リポジトリをどう構成するかの正本である。
ブランド repo は、工場本体の探索機能を持たず、
そのブランドの制作・QA・審査・リリースに集中する。

## 推奨ディレクトリ構成
```text
brand-repo/
├── README.md
├── brand/
│   ├── brand-manifest.yaml
│   ├── brand-setting.md
│   ├── brand-production-brief.md
│   └── brand-system-prompt.md
├── references/
│   ├── market/
│   │   └── idea-batch-001.md
│   └── shared/
│       ├── evaluation-model.md
│       ├── line-platform-baseline.md
│       ├── structure-constraints.md
│       ├── emoji-product-rules.md
│       ├── review-risk-rules.md
│       ├── continuous-improvement-rules.md
│       ├── transformation-workflow.md
│       ├── production-pipeline-workflow.md
│       ├── quality-control-workflow.md
│       ├── continuous-improvement-workflow.md
│       ├── usage-validation-workflow.md
│       └── release-retrospective-workflow.md
├── prompts/
│   ├── gpt-image2-rough-prompts.md
│   ├── claude-design-prompts.md
│   └── revision-prompts.md
├── production/
│   ├── rough-boards/
│   │   └── README.md
│   ├── handoffs/
│   │   └── release-001-handoff.md
│   └── finals/
│       └── README.md
├── emoji-sets/
│   └── releases/
│       └── release-001.md
├── qa/
│   ├── release-checklist.md
│   └── quality-ledger.md
│   ├── usage-validations/
│   │   └── release-001.md
│   └── retrospectives/
│       └── release-001.md
└── submissions/
    └── release-log.md
```

## 各ファイルの役割
- `brand/brand-manifest.yaml`
  - 機械可読な最小メタ情報。
  - factory 由来の version、商品種別、package type、運用方針を置く。
- `brand/brand-setting.md`
  - ブランドの核、視覚記号、派生方針の正本。
- `brand/brand-production-brief.md`
  - 実制作と登録運用の正本。
- `brand/brand-system-prompt.md`
  - 工程別 AI 指示束の正本。
- `references/shared/*`
  - 工場本体から持ち出した rules / workflow snapshot。
  - snapshot 内のファイル参照名は factory 側の owner file 名を保持してよい。
  - brand repo で日常運用するときの正本は、`brand/`, `emoji-sets/`, `production/`, `qa/`, `submissions/` 側の実体文書とする。
- `references/market/idea-batch-001.md`
  - 採用時の市場観測と候補比較の snapshot。
  - brand repo 側で広い探索を続けるためではなく、採用理由と真似しない線引きを後から確認するために残す。
- `references/shared/evaluation-model.md`
  - brand repo 側で使う判定語彙の snapshot。
- `references/shared/structure-constraints.md`
  - rough review や構造後退確認で参照する構造成立性の snapshot。
- `references/shared/transformation-workflow.md`
  - brand repo 側で構造後退が見えたときの戻し先になる変換フローの snapshot。
- `references/shared/continuous-improvement-rules.md`
  - brand repo 側で再発問題や運用過重を factory へ返すときの判断基準 snapshot。
- `references/shared/continuous-improvement-workflow.md`
  - brand repo 側の QA や運用学習を factory 改善へ返すための workflow snapshot。
- `references/shared/usage-validation-workflow.md`
  - brand repo 側で具体会話検証を行うための workflow snapshot。
- `references/shared/release-retrospective-workflow.md`
  - brand repo 側で節目学習を短く圧縮するための workflow snapshot。
- `prompts/*`
  - `GPT-image2.0` 用 rough prompt、`ClaudeDesign` 用仕上げ prompt、修正 prompt を蓄積する。
- `production/rough-boards/*`
  - rough stage の全体図、anchor、過程メモを残す。
- `production/handoffs/*`
  - release / set ごとの handoff 正本を残す。
- `production/finals/*`
  - 完成データの置き場を分ける。
- `emoji-sets/releases/*`
  - リリース単位のセット仕様と差分計画を書く。
- `qa/release-checklist.md`
  - リリース前確認の正本。
- `qa/quality-ledger.md`
  - 継続品質管理の正本。
- `qa/usage-validations/*`
  - release ごとの具体会話検証を残す。
- `qa/retrospectives/*`
  - milestone ごとの短い振り返りを残す。
- `submissions/release-log.md`
  - 提出、審査差し戻し、修正、再提出の履歴を残す。

## repo に残すべきもの
- そのブランドだけに必要な決定
- そのブランドの制作ログ
- そのブランド専用の prompt、rough board、handoff、QA、品質台帳
- そのブランドの具体会話検証と節目振り返り
- そのブランドの将来リリース計画
- 採用時の市場観測 snapshot

## repo に残さないもの
- 他ブランド比較
- 工場本体の ideation メモ
- 汎用 taxonomy や exploration log の全部
- 中途候補の墓場
- 採用されなかった市場探索 batch の全量

## 運用原則
- brand repo は **制作と運用に特化** させる。
- brand repo 側で共通ルールを再解釈しない。
- 公式仕様更新があったら、snapshot を更新するかどうかを明示的に判断する。
- rough / handoff / final の責務を混ぜない。
- 再発問題や運用過重が見えたら、factory 側の継続改善へ戻す。
