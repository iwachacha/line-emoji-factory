# ブランド別リポジトリ設計テンプレート

このテンプレートは、ブランド別リポジトリをどう構成するかの正本である。
ブランド repo は、工場本体の探索機能を持たず、そのブランドの制作・QA・審査・リリースに集中する。

## 推奨ディレクトリ構成
```text
brand-repo/
├── README.md
├── brand-manifest.yaml
├── brand/
│   ├── brand-setting.md
│   ├── brand-positioning.md
│   ├── brand-production-brief.md
│   ├── brand-system-prompt.md
│   └── ip/
│       ├── ip-style-bible.md
│       ├── reference-asset-register.md
│       ├── ip-approval-log.md
│       └── character-expression-matrix.md
├── market/
│   ├── market-observation-log.md
│   └── category-gap-map.md
├── releases/
│   └── release-001/
│       ├── release-spec.md
│       ├── production-handoff.md
│       ├── release-log.md
│       ├── prompts/
│       │   ├── rough-generation.md
│       │   ├── finalization.md
│       │   ├── revision.md
│       │   ├── qa-review.md
│       │   └── metadata-review.md
│       ├── production/
│       │   ├── rough-boards/
│       │   └── finals/
│       ├── qa/
│       │   ├── release-checklist.md
│       │   ├── quality-ledger.md
│       │   ├── usage-validation.md
│       │   └── release-retrospective.md
│       └── submission/
│           ├── metadata.yaml
│           ├── submission-checklist.md
│           ├── submission-audit-report.md
│           └── images/
├── references/
│   └── shared/
│       ├── line-platform-baseline.md
│       ├── structure-constraints.md
│       ├── emoji-product-rules.md
│       ├── review-risk-rules.md
│       ├── evaluation-model.md
│       ├── quality-control-workflow.md
│       └── usage-validation-workflow.md
└── tools/
    ├── validate-assets.py
    ├── validate-metadata.py
    ├── package-release.py
    └── check-placeholders.py
```

## 各ファイルの役割
- `brand-manifest.yaml`
  - 機械可読な最小メタ情報。schema validation の対象。
- `brand/brand-setting.md`
  - ブランドの核、視覚記号、派生方針の正本。
- `brand/brand-positioning.md`
  - 市場内の位置、差別化軸、模倣禁止境界の正本。
- `brand/brand-production-brief.md`
  - 実制作と登録運用の正本。
- `brand/brand-system-prompt.md`
  - 工程別 AI 指示束の正本。
- `brand/ip/*`
  - 固定IP案件でのみ使う許諾範囲、参照素材、承認ログ、表情展開の正本。
- `market/*`
  - 市場観測、ジャンル空白、模倣禁止境界の証跡。
- `releases/*/release-spec.md`
  - release 単位のセット仕様と差分計画。
- `releases/*/production-handoff.md`
  - release / set ごとの handoff 正本。
- `releases/*/qa/*`
  - release 前チェック、品質台帳、具体会話検証、節目振り返り。
- `releases/*/submission/*`
  - metadata、申請 checklist、申請監査、最終画像置き場。
- `references/shared/*`
  - 工場本体から持ち出した rules / workflow snapshot。
- `tools/*`
  - brand repo 単独でも最低限の検査を再実行するための補助 tool。

## repo に残すべきもの
- そのブランドだけに必要な決定
- そのブランドの制作ログ
- そのブランド専用の prompt、rough board、handoff、QA、品質台帳
- そのブランドの具体会話検証と節目振り返り
- そのブランドの将来リリース計画

## repo に残さないもの
- 他ブランド比較
- 工場本体の ideation メモ
- 汎用 taxonomy や exploration log の全部
- 中途候補の墓場

## 運用原則
- brand repo は制作と運用に特化させる。
- brand repo 側で共通ルールを再解釈しない。
- 公式仕様更新があったら、snapshot を更新するかどうかを明示的に判断する。
- rough / handoff / final / submission の責務を混ぜない。
- 再発問題や運用過重が見えたら、factory 側の継続改善へ戻す。
