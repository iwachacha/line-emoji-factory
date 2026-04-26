# Architecture

## Judgment Order
`構造 → ブランド → 商品`

## Layers
- `rules/`: 判断基準
- `workflows/`: 手順
- `templates/`: 成果物の型
- `schemas/`: 機械検証契約
- `tools/`: 実行と検査
- `skills/`: 入口と読む順序
- `sandbox/`: 壊してよい実験場

## Factory Flow
```text
market observation
  -> brand distillation
  -> set architecture
  -> brand canon / series planning
  -> production direction
  -> item finalization
  -> asset validation
  -> submission audit
  -> release packaging
  -> post-release learning
```

## Brand Repo Boundary
brand repo は制作と運用に集中する。
factory の共通ルールは snapshot として `references/shared/` に渡し、brand repo 側で再解釈しない。
