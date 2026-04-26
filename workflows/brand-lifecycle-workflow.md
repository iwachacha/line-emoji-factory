# ブランドスタートアップ / 分離ワークフロー

このファイルは、初期ブランド構想を factory から切り離して、個別ブランドの startup repo として成立させるための正本である。

## 結論

デフォルトは **startup 分離** にする。

- factory repo は、比較、変換、評価、共通基盤改善を担当する。
- 個別ブランド repo は、採用候補の文脈、canon、初回商品仮説、prompt seed を保持する。
- QA、submission、release ledger は、実画像制作へ進むまで配布しない。

## なぜ production repo を標準にしないか

- 初期ブランドにはまだ実画像、審査、公開履歴がない。
- 最初から submission や QA を配ると、ブランド創出より運用管理が重くなる。
- 世界観未固定の段階でrelease運用まで作ると、後から削る判断が遅れる。
- ブランドごとに、キャラ型、モチーフ型、記号型、デコ文字型、固定IP型など必要な資産が違う。

## Stage 0: Factory Exploration

- ブランド核がまだ揺れている。
- 複数候補の比較、構造Fail時の変換、市場観測はfactory repoで行う。
- この段階ではrepoを切らない。

## Stage 1: Startup Ready

次の条件を満たしたら、startup repoへ分離する。

- 構造分類を仮置きできる。
- LINE item type の最初の仮説がある。
- ブランドを1文で言える。
- Hard NG が見えていない。
- 初回商品仮説、または初回set seedがある。
- 今後このブランドだけのprompt、canon、item seedを持つ見込みがある。

## Stage 2: Startup Repo

`tools/init-brand-repo.ps1` の標準 `startup` mode でrepoを作る。

startup repoに配るもの:

- brand setting
- brand canon / IP guardrails
- brand positioning
- brand production brief seed
- brand system prompt seed
- product catalog seed
- startup brief
- startup checklist
- character / motif data
- item seed data
- prompt library
- market observation seed
- fixed shared snapshots
- lightweight validation tools

startup repoに配らないもの:

- final asset置き場
- submission package置き場
- release QA一式
- release retrospective
- package tool
- asset validation tool

## Stage 3: Production Promotion

次の条件を満たしたら production skeleton を追加する。

- 初回set countとslot構成が固まっている。
- style anchor または character / motif anchor を作る段階に入った。
- 1 itemずつfinalizationする意思決定がある。
- asset QA、metadata、submission package が近い将来必要になる。

production repoに追加するもの:

- release spec
- series plan
- production handoff
- release log
- prompts bundle
- production pipeline snapshot
- production rough / final / main / tab dirs
- QA checklist / quality ledger / usage validation
- submission metadata / checklist / audit report
- asset validation and packaging tools

## Stage 4: Release / Learning

- 実画像ができたら、production-pipeline、quality-control、submission-auditを通す。
- 公開後の学習はbrand repoに残し、再発問題だけfactoryへ戻す。

## Fixed Startup Distribution

startup repoが必ず持つsnapshot:

- `rules/line-platform-baseline.md`
- `rules/structure-constraints.md`
- `rules/evaluation-model.md`
- `rules/brand-taxonomy.md`
- `rules/brand-creation-rules.md`
- `rules/emoji-product-rules.md`
- `rules/sticker-product-rules.md`
- `rules/review-risk-rules.md`
- `rules/review-risk-keywords.yaml`
- `workflows/brand-distillation-workflow.md`
- `workflows/set-architecture-workflow.md`

startup repoが必ず持つtool:

- `tools/validate-brand-repo.py`
- `tools/validate-brand-repo.ps1`
- `tools/validate-schemas.py`
- `tools/check-source-integrity.py`
- `tools/check-data-files.py`
- `tools/check-placeholders.py`
- `tools/validate-manifest-paths.py`
- `tools/sync-shared-snapshots.ps1`
- `tools/promote-brand-repo.ps1`

## Supported Patterns

startup repoは次のブランド型に対応する。

- キャラクター型
- モチーフ型
- 記号型
- 図形・抽象型
- デコ文字型
- 固定IP型
- collaboration型

型によって不要な欄は空でよい。空欄を埋めるためだけに世界観やキャラを増やさない。

## Non-Negotiable

- 判断順序は `構造 → ブランド → 商品`。
- startup repoは、production repoではない。
- hard canonを太らせない。
- live dependencyにしない。
- factory repoを丸ごとforkしない。
- 他ブランドの資料を持ち込まない。
- 画像制作前にsubmission運用を重くしない。

## 実現方法

- 標準startup分離:
  - `tools/init-brand-repo.ps1 -BrandSlug <slug> -Destination <path> -BrandName <name>`
- 既存startup repoのproduction昇格:
  - `tools/promote-brand-repo.ps1 -BrandRepo <path> -ProductItemType <static-emoji|static-sticker>`
- production skeletonつき新規分離:
  - `tools/init-brand-repo.ps1 -BrandSlug <slug> -Destination <path> -BrandName <name> -RepoProfile production`
