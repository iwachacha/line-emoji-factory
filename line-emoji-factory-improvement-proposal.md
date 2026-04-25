# line-emoji-factory 改善提案書

作成日: 2026-04-25
対象リポジトリ: `iwachacha/line-emoji-factory`
前提: 既存構造を壊してよい。現状が最適なら維持するが、工場として弱い箇所は破壊的に再設計する。

---

## 1. 結論

現在の `line-emoji-factory` は、LINE絵文字ブランドを考えるための共通基盤としては良い。

特に、次の思想は残すべきである。

- `構造 → ブランド → 商品` の順で判断する
- LINE絵文字固有の制約を先に見る
- ブランドごとに個別リポジトリへ切り出す
- 共通基盤は snapshot として個別ブランドへ渡す
- QA、使用シーン検証、ふりかえり、改善台帳を持つ
- 個別ブランドの文脈で共通基盤を汚染しない

一方で、現状はまだ **「考える factory」** に寄っている。

今後目指すべき姿は、次の5段階をすべて持つ factory である。

```text
考える factory
  ↓
作る factory
  ↓
検査する factory
  ↓
提出する factory
  ↓
売れ方から学ぶ factory
```

現状で最も弱いのは、以下である。

- 実画像の検査
- メタデータ検査
- LINE申請パッケージ化
- schema による成果物検証
- CI による破損検知
- 固定IP向けの運用統制
- 市場調査の証跡管理
- スキルの責務分離
- README / quickstart の入口整備
- テンプレートと script の整合性保証

したがって、今後は **ルールをさらに増やすより、ルールを壊せない仕組み、成果物を検査する仕組み、提出まで包む仕組みを優先する**。

---

## 2. 現状認識

### 2.1 現在のトップレベル構成

確認時点で、root には概ね以下が存在する。

```text
rules/
sandbox/soeshirushi/
scripts/
skills/
templates/
workflows/
AGENTS.md
PROJECT_MAP.md
README.md
factory-improvement-ledger.md
```

この構成は思想としては良いが、工場としては不足がある。

### 2.2 README が入口になっていない

現状の README は実質タイトル程度であり、以下が不足している。

- このリポジトリで何ができるのか
- 誰が使うのか
- 新規ブランドを作る流れ
- 共通基盤と個別ブランドの関係
- `scripts/init-brand-repo.ps1` の使い方
- 品質チェックの流れ
- LINE申請前の流れ
- `sandbox/soeshirushi` の読み方
- 破壊的変更を含む今後の開発方針

README は P0 で書き直すべきである。

### 2.3 スキル構成がメタ作業に寄りすぎている

現在の `skills/` は以下の5つである。

```text
line-emoji-doc-auditor/
line-emoji-factory-evolver/
line-emoji-improvement-auditor/
line-emoji-producer/
line-emoji-skill-builder/
```

この構成は、入口としては分かるが、工場実務としては弱い。

問題は、**実務1 + メタ4** になっていること。

```text
現状:
  実務系:
    - line-emoji-producer

  メタ系:
    - line-emoji-doc-auditor
    - line-emoji-factory-evolver
    - line-emoji-improvement-auditor
    - line-emoji-skill-builder
```

これでは、実際に必要な以下の作業単位が独立していない。

- 市場を見る
- ブランド核を作る
- セット構成を組む
- 画像を制作管理する
- 画像仕様を検査する
- メタデータを検査する
- 固定IPを守る
- 申請パッケージを作る
- 公開後データから学ぶ

### 2.4 `line-emoji-producer` が大きすぎる

`line-emoji-producer` は、候補出し、市場調査、構造判定、ブランド設計、商品設計、初期release設計、制作ハンドオフ、品質管理、ブランド専用AI指示作成まで抱えている。

これは総合入口としては便利だが、スキルとしては責務過多である。

今後は `producer` を実作業スキルではなく router に降格する。

### 2.5 監査系スキルが重複している

以下の3つは統合するべきである。

```text
line-emoji-doc-auditor
line-emoji-improvement-auditor
line-emoji-factory-evolver
```

これらはすべて、広義には factory の品質・整合性・改善採否を扱う監査スキルである。

統合後は以下にする。

```text
line-emoji-factory-auditor
```

内部 mode として分ければよい。

```text
mode:
  - doc_audit
  - brand_audit
  - release_audit
  - workflow_audit
  - skill_audit
  - factory_upgrade
```

### 2.6 script が `init-brand-repo.ps1` だけに集中している

現状の `scripts/` には `init-brand-repo.ps1` だけがある。

これは重要だが、工場としては足りない。

必要なのは、作るだけでなく、検証し、包み、申請直前まで持っていく tool 群である。

### 2.7 templates が単一階層に並びすぎている

現状の `templates/` には、brand、release、QA、prompt、repo scaffold が同じ階層に並んでいる。

これはファイル数が少ない段階ではよいが、今後固定IP、market、submission、schema 対応を増やすと混乱する。

階層化するべきである。

### 2.8 LINE公式仕様に対する validator がない

LINE Creators Market の絵文字仕様では、たとえば以下が定められている。

- トークルームタブ画像: 96px × 74px
- 絵文字コンテンツ画像: 8〜40個、180px × 180px
- PNG形式
- 背景透過
- 解像度 72dpi以上
- RGB
- 1画像 1MB以下
- ZIP 20MB以下
- クリエイター名 50文字以内
- 絵文字タイトル 40文字以内
- 絵文字説明文 160文字以内
- コピーライト 50文字以内、英数字のみ

また、LINE公式は、余白をつけすぎないこと、アウトラインを太く濃くすること、単体で送信するとスタンプのように使えること、表情差を大きくすること、装飾をシンプルにすることも説明している。

現状のリポジトリには、それをルール文書として持つ方向性はあるが、機械的に検証する validator が不足している。

これは P0 で追加すべきである。

---

## 3. 破壊的変更の方針

以下の前提で壊してよい。

### 3.1 残す思想

```text
構造 → ブランド → 商品
共通基盤と個別ブランドの分離
ブランドrepoへの snapshot 配布
使用シーン検証
QA gate
release retrospective
factory improvement ledger
```

### 3.2 壊すもの

```text
line-emoji-producer の巨大責務
監査系3スキルの重複
templates/ の単一階層
scripts/ の単機能化
sandbox/soeshirushi の曖昧な位置づけ
README の空状態
manifest / release spec の非schema状態
ツール名に強く結合した prompt template 名
remote push を完了条件に含める運用
```

### 3.3 壊し方の原則

- ファイル名は意味単位で分ける
- スキルは「人間の作業役割」ではなく「成果物を作る責務」で分ける
- rules は判断基準
- workflows は手順
- templates は成果物の型
- schemas は成果物の機械検証
- tools は実行と検査
- skills は作業入口と判断支援
- CI は壊れたことを検出する

---

## 4. 最終スキル構成案

### 4.1 最終形

```text
skills/
  line-emoji-router/
  line-emoji-market-scout/
  line-emoji-brand-distiller/
  line-emoji-set-architect/
  line-emoji-production-director/
  line-emoji-asset-validator/
  line-emoji-submission-auditor/
  line-emoji-ip-governor/
  line-emoji-release-packager/
  line-emoji-post-release-analyst/
  line-emoji-factory-auditor/
```

### 4.2 現在のスキルからの移行

| 現在 | 最終判断 | 移行先 |
|---|---|---|
| `line-emoji-producer` | 破壊して router 化 | `line-emoji-router` |
| `line-emoji-doc-auditor` | 統合 | `line-emoji-factory-auditor` |
| `line-emoji-improvement-auditor` | 統合 | `line-emoji-factory-auditor` |
| `line-emoji-factory-evolver` | 統合 | `line-emoji-factory-auditor` |
| `line-emoji-skill-builder` | 廃止または統合 | `line-emoji-factory-auditor` の `skill_audit` mode |

### 4.3 `line-emoji-router`

#### 目的

ユーザーの依頼を、適切な専門スキルへ振り分ける。

#### やらないこと

- ブランド設計そのもの
- 市場調査そのもの
- release spec 作成そのもの
- 画像検査そのもの
- 申請監査そのもの

#### routing 例

```text
ブランド案を出したい
  → line-emoji-market-scout
  → line-emoji-brand-distiller

このブランドの初回セットを作りたい
  → line-emoji-set-architect

画像の出来を見てほしい
  → line-emoji-asset-validator

LINE申請前に確認したい
  → line-emoji-submission-auditor

固定IPで作りたい
  → line-emoji-ip-governor
```

### 4.4 `line-emoji-market-scout`

#### 目的

市場観測、ジャンル空白、競合混雑、模倣禁止ラインを整理する。

#### 主な成果物

```text
market-observation-log.md
idea-batch.md
category-gap-map.md
imitation-risk-notes.md
```

#### チェック観点

- 観測日
- 観測場所
- 検索語
- 代表的な競合
- 混雑カテゴリ
- 空白カテゴリ
- 模倣に見えるライン
- 自ブランドが取れる差別化軸
- LINE絵文字として成立する使用場面

### 4.5 `line-emoji-brand-distiller`

#### 目的

市場観測やアイデアから、ブランド核を作る。

#### 主な成果物

```text
brand-setting.md
brand-positioning.md
brand-production-brief.md
```

#### 判断観点

- ブランドを1文で言えるか
- 主型 / 副型 / 補助タグが明確か
- 視覚記号が3〜5個に絞られているか
- 使う場面が明確か
- 使わない場面が明確か
- 買う理由があるか
- release を増やせる余地があるか
- 汎用的ブランドか、固定IPブランドか

### 4.6 `line-emoji-set-architect`

#### 目的

8 / 16 / 24 / 32 / 40個のセット構成を設計する。

#### 主な成果物

```text
release-spec.md
set-composition.md
emoji-slot-map.md
usage-priority-map.md
```

#### 判断観点

- 初回 release は何個にするべきか
- 上段に高頻度絵文字があるか
- 応答、感情、補助、遊びのバランスはよいか
- 似すぎた絵文字がないか
- 文中挿入でも成立するか
- 単体送信でも成立するか
- 次 release に残すべき余白があるか
- 任意テキスト依存が強すぎないか

### 4.7 `line-emoji-production-director`

#### 目的

rough、final、revision、handoff を管理する。

#### 主な成果物

```text
production-handoff.md
rough-generation-prompts.md
finalization-prompts.md
revision-prompts.md
rough-board-notes.md
final-review-notes.md
```

#### 判断観点

- rough で構造と意味が見えているか
- final で小サイズ視認性が上がったか
- 表情差・記号差が明確か
- ブランドの線・色・余白が一貫しているか
- 修正指示が slot 単位で明確か
- final asset と release spec が対応しているか

### 4.8 `line-emoji-asset-validator`

#### 目的

画像仕様と視認性を検査する。

#### 主な成果物

```text
asset-validation-report.md
asset-issues.json
asset-fix-list.md
```

#### 機械検査

- PNG / APNG
- 180px × 180px
- トークルームタブ画像 96px × 74px
- 透過
- RGB
- 72dpi以上
- 1画像 1MB以下
- ZIP 20MB以下
- ファイル命名
- 個数 8 / 16 / 24 / 32 / 40

#### 半自動・目視検査

- 余白過多
- 小サイズ視認性
- アウトラインの太さ
- 濃さ
- 表情差
- 装飾つぶれ
- セット内の似すぎ
- 単体送信時の成立
- 文中挿入時の成立

### 4.9 `line-emoji-submission-auditor`

#### 目的

LINE申請直前の総合監査を行う。

#### 主な成果物

```text
submission-audit-report.md
submission-checklist.md
metadata-validation-report.md
review-risk-report.md
```

#### チェック観点

- 画像仕様
- メタデータ仕様
- title / description / copyright
- 告知表現
- 単なる企業ロゴ
- 特定個人向け表現
- LINE以外のサービス名
- 他社キャラクター名
- 審査落ちしやすい表現
- release package の完全性

### 4.10 `line-emoji-ip-governor`

#### 目的

固定IPを安全に使うための制作統制を行う。

#### 主な成果物

```text
ip-style-bible.md
reference-asset-register.md
ip-approval-log.md
character-expression-matrix.md
ip-risk-report.md
```

#### チェック観点

- 使用許諾範囲
- 使用可能キャラクター
- 使用可能ロゴ
- 使用可能モチーフ
- 禁止ポーズ
- 禁止表情
- 禁止文脈
- 色、線、顔比率、服装、小物
- 公式素材との距離
- AI生成時の参照画像ルール
- 権利者レビューの承認ログ
- キャラクター崩れ
- ブランドセーフティ

### 4.11 `line-emoji-release-packager`

#### 目的

申請用パッケージを作る。

#### 主な成果物

```text
submission/
  images/
  metadata/
  package.zip
  submission-checklist.md
```

#### 実行内容

- final assets を集める
- LINE指定ファイル名に揃える
- metadata を出力する
- ZIP前チェックを行う
- ZIPを作る
- release-log を更新する
- checksum を出す
- 提出直前 checklist を作る

### 4.12 `line-emoji-post-release-analyst`

#### 目的

公開後データから次の release と factory 改善を作る。

#### 主な成果物

```text
post-release-metrics.md
sales-analysis.md
review-outcome-log.md
next-release-recommendation.md
factory-learning-note.md
```

#### チェック観点

- 売れた理由
- 売れなかった理由
- クリックされるが買われない原因
- 審査で落ちた理由
- 次 release に増やすべき枠
- 廃止すべき枠
- factory へ昇格すべき学習

### 4.13 `line-emoji-factory-auditor`

#### 目的

factory 全体の整合性、改善採否、スキル設計を監査する。

#### mode

```text
doc_audit
brand_audit
release_audit
workflow_audit
skill_audit
factory_upgrade
```

#### 主な成果物

```text
factory-audit-report.md
factory-improvement-proposal.md
skill-audit-report.md
migration-plan.md
```

---

## 5. rules 改善案

### 5.1 現状維持する rules

以下は維持する。

```text
brand-creation-rules.md
brand-taxonomy-rules.md
continuous-improvement-rules.md
emoji-product-rules.md
evaluation-model.md
idea-research-rules.md
line-platform-baseline.md
review-risk-rules.md
structure-constraints.md
```

ただし、文書内の責務重複は監査する。

### 5.2 新設する rules

```text
rules/
  asset-validation-rules.md
  submission-metadata-rules.md
  release-packaging-rules.md
  ip-governance-rules.md
  market-observation-rules.md
  production-profile-rules.md
  schema-contract-rules.md
```

### 5.3 `asset-validation-rules.md`

#### 扱う内容

- 画像寸法
- 画像数
- PNG / APNG
- 透過
- RGB
- dpi
- ファイルサイズ
- ZIPサイズ
- 余白
- 視認性
- 線の太さ
- 表情差
- 装飾つぶれ
- 類似過多

### 5.4 `submission-metadata-rules.md`

#### 扱う内容

- クリエイター名
- タイトル
- 説明文
- コピーライト
- 文字数
- 全角文字カウント
- 絵文字禁止
- 告知表現禁止
- 他サービス名禁止
- 特定個人向け禁止
- 単なる企業ロゴ禁止

### 5.5 `release-packaging-rules.md`

#### 扱う内容

- submission folder 構造
- ファイル名
- ZIP作成
- checksum
- metadata の出力形式
- release-log との整合性
- checklist の必須項目

### 5.6 `ip-governance-rules.md`

#### 扱う内容

- 許諾範囲
- 参照素材
- 禁止変形
- 禁止文脈
- キャラクター崩れ
- 権利者承認
- AI生成時の参照ルール
- 公式素材との距離

### 5.7 `market-observation-rules.md`

#### 扱う内容

- 観測日
- 検索語
- 類似カテゴリ
- 混雑領域
- 空白領域
- 模倣禁止境界
- 差別化仮説
- 証跡の残し方

### 5.8 `production-profile-rules.md`

#### 扱う内容

特定ツール名にルールが依存しないよう、工程を profile 化する。

```yaml
production_profile:
  rough_stage:
    tool: gpt-image2.0
    required_outputs:
      - rough_board
      - per_emoji_intent
      - failure_notes

  finish_stage:
    tool: claude-design
    required_outputs:
      - final_assets
      - correction_notes
      - export_check
```

ルール側では `GPT-image2` や `ClaudeDesign` を正本化しない。
正本は工程要件であり、ツールは profile の値にする。

---

## 6. workflows 改善案

### 6.1 現状維持する workflows

既存 workflow は、責務を整理したうえで概ね維持する。

```text
brand-lifecycle-workflow.md
quality-control-workflow.md
usage-validation-workflow.md
production-pipeline-workflow.md
framework-maintenance.md
```

### 6.2 新設する workflows

```text
workflows/
  market-observation-workflow.md
  brand-distillation-workflow.md
  set-architecture-workflow.md
  asset-validation-workflow.md
  submission-audit-workflow.md
  release-packaging-workflow.md
  ip-production-workflow.md
  post-release-learning-workflow.md
  schema-validation-workflow.md
  ci-maintenance-workflow.md
```

### 6.3 重要な変更

`remote push 完了` を作業完了条件から外す。

#### 理由

- AIやレビュー担当が常に push 権限を持つとは限らない
- 分析、レビュー、設計だけの依頼でも完了できるべき
- push は人間またはCIの責務でよい

#### 新しい完了条件

```text
作業完了:
  - owner file の更新案を出す
  - 必要な記録先を示す
  - 差分確認手順を示す
  - 検証コマンドを示す
  - push は権限を持つ人間またはCIが行う
```

---

## 7. templates 改善案

### 7.1 現状の問題

現状の `templates/` は単一階層であり、以下が混在している。

- brand
- release
- QA
- prompts
- repo scaffold
- improvement ledger

今後、固定IP、market、submission、schema 対応を増やすと破綻する。

### 7.2 最終構成

```text
templates/
  brand/
    brand-setting-template.md
    brand-positioning-template.md
    brand-production-brief-template.md
    brand-system-prompt-template.md

  release/
    release-spec-template.md
    release-log-template.md
    production-handoff-template.md

  qa/
    release-checklist-template.md
    quality-ledger-template.md
    usage-validation-template.md
    release-retrospective-template.md

  prompts/
    rough-generation-template.md
    finalization-template.md
    revision-template.md
    qa-review-template.md
    metadata-review-template.md

  repo/
    brand-repo-blueprint.md
    brand-repo-manifest-template.yaml
    brand-repo-readme-template.md

  ip/
    ip-style-bible-template.md
    reference-asset-register-template.md
    ip-approval-log-template.md
    character-expression-matrix-template.md

  market/
    idea-batch-template.md
    market-observation-log-template.md
    category-gap-map-template.md

  submission/
    submission-checklist-template.md
    submission-metadata-template.yaml
    asset-validation-report-template.md
    submission-audit-report-template.md

  improvement/
    factory-improvement-ledger-template.md
    factory-audit-report-template.md
```

### 7.3 壊してよいリネーム

```text
gpt-image2-rough-prompts-template.md
  → templates/prompts/rough-generation-template.md

claude-design-prompts-template.md
  → templates/prompts/finalization-template.md

revision-prompts-template.md
  → templates/prompts/revision-template.md
```

理由は、テンプレート名を特定ツールに結合させないためである。

---

## 8. schemas 新設案

### 8.1 新設する

```text
schemas/
  brand-manifest.schema.json
  release-spec.schema.json
  production-handoff.schema.json
  quality-ledger.schema.json
  usage-validation.schema.json
  market-observation.schema.json
  submission-metadata.schema.json
  asset-validation-report.schema.json
  ip-style-bible.schema.json
  reference-asset-register.schema.json
```

### 8.2 `brand-manifest.schema.json`

必須項目。

```yaml
schema_version: "1.0"
factory_base_version: "2026-04-25"

brand:
  slug: soeshirushi
  name: そえしるし
  stage: design-ready
  owner: ""

snapshots:
  line_platform_baseline: references/shared/line-platform-baseline.md
  structure_constraints: references/shared/structure-constraints.md
  emoji_product_rules: references/shared/emoji-product-rules.md
  review_risk_rules: references/shared/review-risk-rules.md
  evaluation_model: references/shared/evaluation-model.md
  quality_control_workflow: references/shared/quality-control-workflow.md
  usage_validation_workflow: references/shared/usage-validation-workflow.md

releases:
  - id: release-001
    status: draft
    spec: releases/release-001/release-spec.md
```

### 8.3 schema で検出すること

- 必須キー不足
- 参照パス不在
- stage の不正値
- release id の不正形式
- snapshot の欠落
- metadata の文字数超過
- unknown key
- unresolved placeholder

---

## 9. tools / CLI 新設案

### 9.1 `scripts/` から `tools/` へ

現在は `scripts/init-brand-repo.ps1` が中心だが、工場としては `tools/` に昇格する。

```text
tools/
  init-brand-repo.ps1
  validate-brand-repo.ps1
  validate-assets.py
  validate-metadata.py
  package-release.py
  sync-shared-snapshots.ps1
  check-placeholders.py
  validate-schemas.py
```

### 9.2 CLI の将来形

```text
line-emoji-factory init-brand
line-emoji-factory validate-brand
line-emoji-factory validate-assets
line-emoji-factory validate-metadata
line-emoji-factory new-release
line-emoji-factory audit-release
line-emoji-factory package-release
line-emoji-factory sync-snapshots
line-emoji-factory record-retrospective
```

### 9.3 `validate-brand-repo.ps1`

検査項目。

```text
- manifest が schema に通る
- manifest 内の参照パスが存在する
- shared snapshot が存在する
- release spec が存在する
- QA checklist が存在する
- unresolved placeholder がない
- README が存在する
- required directories が存在する
```

### 9.4 `validate-assets.py`

検査項目。

```text
- PNG / APNG
- 画像寸法
- 画像数
- 透過
- RGB
- dpi
- ファイルサイズ
- ZIPサイズ
- ファイル名
- 余白率
- 小サイズプレビュー生成
```

### 9.5 `validate-metadata.py`

検査項目。

```text
- クリエイター名 50文字以内
- タイトル 40文字以内
- 説明文 160文字以内
- コピーライト 50文字以内
- コピーライト英数字のみ
- 絵文字禁止
- 告知表現
- 他サービス名
- 特定個人向け表現
- 単なる企業ロゴ表現
```

### 9.6 `package-release.py`

実行内容。

```text
- final assets を submission へコピー
- ファイル名を正規化
- metadata を出力
- validate-assets を実行
- validate-metadata を実行
- ZIPを作成
- checksum を出力
- submission checklist を更新
```

---

## 10. CI / GitHub Actions 改善案

### 10.1 新設する workflow

```text
.github/workflows/validate.yml
```

### 10.2 実行する検証

```text
- Markdown lint
- YAML parse
- PowerShell syntax check
- Python lint
- schema validation
- scaffold smoke test
- unresolved placeholder check
- generated brand repo validation
- asset validator unit test
- metadata validator unit test
```

### 10.3 scaffold smoke test

CI で次を行う。

```text
1. temporary directory を作る
2. tools/init-brand-repo.ps1 を実行する
3. 生成された manifest を検証する
4. 必須ファイル存在を確認する
5. unresolved placeholder を検出する
6. validate-brand-repo を通す
```

### 10.4 完了条件

main branch では最低限以下を満たす。

```text
README が存在し、最低限の quickstart がある
Markdown / YAML が parse 可能
manifest schema が存在する
scaffold smoke test が通る
unresolved placeholder がない
```

---

## 11. 固定IP対応の新設

### 11.1 なぜ必要か

この factory は、汎用的なLINE絵文字ブランドだけでなく、固定IPに沿った質の高い絵文字も作ることを目的としている。

現状の `review-risk` 系は、権利侵害を避ける方向には使えるが、許諾済みIPを正しく運用する仕組みとしては不足している。

### 11.2 追加する

```text
rules/ip-governance-rules.md
workflows/ip-production-workflow.md
templates/ip/ip-style-bible-template.md
templates/ip/reference-asset-register-template.md
templates/ip/ip-approval-log-template.md
templates/ip/character-expression-matrix-template.md
skills/line-emoji-ip-governor/SKILL.md
schemas/ip-style-bible.schema.json
schemas/reference-asset-register.schema.json
```

### 11.3 IP案件の必須成果物

```text
brand/ip/
  ip-style-bible.md
  reference-asset-register.md
  ip-approval-log.md
  character-expression-matrix.md
```

### 11.4 IP案件で必ず見ること

```text
- 使用許諾範囲
- 使用可能なキャラクター
- 使用可能なロゴ
- 使用可能なモチーフ
- 禁止ポーズ
- 禁止表情
- 禁止文脈
- 色・線・顔比率・衣装・小物の固定仕様
- 公式素材との距離
- AI生成時の参照画像ルール
- 権利者レビュー
- 承認ログ
- 差し戻し履歴
```

---

## 12. 市場調査・証跡管理の強化

### 12.1 現状の問題

市場調査の考え方はあるが、観測証跡が弱い。

ブランドごとに、以下を残すべきである。

```text
market/
  market-observation-log.md
  category-gap-map.md
  competitor-notes.md
  imitation-risk-notes.md
```

### 12.2 `market-observation-log.md` の項目

```markdown
# Market Observation Log

## Observation
- Date:
- Observer:
- Store / platform:
- Search query:
- Locale:
- Category:

## Findings
- Crowded area:
- Sparse area:
- Common visual motifs:
- Common titles / keywords:
- Typical price / package style:

## Imitation boundary
- Do not copy:
- Avoid similar naming:
- Avoid similar composition:
- Avoid similar character traits:

## Opportunity
- Open concept:
- Differentiation axis:
- First release hypothesis:
```

---

## 13. brand repo blueprint 改善案

### 13.1 個別ブランドリポジトリの標準構成

```text
brand-repo/
  README.md
  brand-manifest.yaml

  brand/
    brand-setting.md
    brand-positioning.md
    brand-production-brief.md
    brand-system-prompt.md

  market/
    market-observation-log.md
    category-gap-map.md

  releases/
    release-001/
      release-spec.md
      production-handoff.md
      release-log.md

      prompts/
        rough-generation.md
        finalization.md
        revision.md
        qa-review.md

      production/
        rough-boards/
        finals/

      qa/
        release-checklist.md
        quality-ledger.md
        usage-validation.md
        release-retrospective.md

      submission/
        metadata.yaml
        images/
        package.zip
        submission-checklist.md
        submission-audit-report.md

  references/
    shared/
      line-platform-baseline.md
      structure-constraints.md
      emoji-product-rules.md
      review-risk-rules.md
      evaluation-model.md
      quality-control-workflow.md
      usage-validation-workflow.md

  tools/
    validate-brand-repo.ps1
    validate-assets.py
    validate-metadata.py
    package-release.py
```

### 13.2 固定IPブランドの場合

```text
brand/
  ip/
    ip-style-bible.md
    reference-asset-register.md
    ip-approval-log.md
    character-expression-matrix.md
```

### 13.3 manifest に入れるべきもの

```yaml
schema_version: "1.0"
factory_base_version: "2026-04-25"

brand:
  slug: ""
  name: ""
  type: generic # generic | fixed_ip | collaboration
  stage: ""

market:
  observation_log: market/market-observation-log.md

snapshots:
  line_platform_baseline: references/shared/line-platform-baseline.md
  structure_constraints: references/shared/structure-constraints.md
  emoji_product_rules: references/shared/emoji-product-rules.md
  review_risk_rules: references/shared/review-risk-rules.md
  evaluation_model: references/shared/evaluation-model.md
  quality_control_workflow: references/shared/quality-control-workflow.md
  usage_validation_workflow: references/shared/usage-validation-workflow.md

releases:
  - id: release-001
    status: draft
    spec: releases/release-001/release-spec.md
    checklist: releases/release-001/qa/release-checklist.md
    submission: releases/release-001/submission/
```

---

## 14. `sandbox/soeshirushi` の扱い

### 14.1 現状評価

`soeshirushi` は、単なる sandbox ではなく、参照実装に近い。

「文字補助絵文字」という広い案から、「意味を軽く添える記号ブランド」へ絞り込んでおり、初回16個構成にも理由がある。

ただし、実画像や最終申請パッケージが揃っているわけではないため、production ready ではなく design-stage の例として扱う。

### 14.2 移動案

```text
examples/
  soeshirushi/

sandbox/
  experiments/
```

### 14.3 `examples/soeshirushi` で追加するもの

```text
market/
  market-observation-log.md
  category-gap-map.md

releases/release-001/submission/
  metadata.yaml
  submission-checklist.md
  submission-audit-report.md

asset-validation-report.md
```

---

## 15. README 改善案

### 15.1 README に入れる内容

```markdown
# line-emoji-factory

LINE絵文字ブランドを継続的に作り、検査し、改善するための共通基盤。

## できること

- 新規LINE絵文字ブランドの発想
- 市場観測
- ブランド核の設計
- 初回release構成
- 制作ハンドオフ
- 画像仕様検査
- メタデータ検査
- LINE申請パッケージ化
- 固定IP向け制作統制
- 公開後の改善学習

## 基本思想

構造 → ブランド → 商品

## Quickstart

```powershell
./tools/init-brand-repo.ps1 -BrandSlug "my-brand" -BrandName "マイブランド"
./tools/validate-brand-repo.ps1 ./brands/my-brand
```

## Directory map

...

## Skills

...

## Tools

...

## Examples

...
```

### 15.2 README の完了条件

- 初見ユーザーが目的を理解できる
- 最初のブランドrepoを作れる
- 生成後の検証コマンドが分かる
- `examples/soeshirushi` の読み方が分かる
- 固定IP案件の入口が分かる

---

## 16. 最終ディレクトリ構成案

```text
line-emoji-factory/
  README.md
  PROJECT_MAP.md
  AGENTS.md
  factory-improvement-ledger.md

  docs/
    quickstart.md
    architecture.md
    brand-lifecycle-guide.md
    official-baseline-update.md
    fixed-ip-production-guide.md
    contribution-guide.md

  rules/
    brand-creation-rules.md
    brand-taxonomy-rules.md
    continuous-improvement-rules.md
    emoji-product-rules.md
    evaluation-model.md
    idea-research-rules.md
    line-platform-baseline.md
    review-risk-rules.md
    structure-constraints.md
    asset-validation-rules.md
    submission-metadata-rules.md
    release-packaging-rules.md
    ip-governance-rules.md
    market-observation-rules.md
    production-profile-rules.md
    schema-contract-rules.md

  workflows/
    brand-lifecycle-workflow.md
    quality-control-workflow.md
    usage-validation-workflow.md
    production-pipeline-workflow.md
    framework-maintenance.md
    market-observation-workflow.md
    brand-distillation-workflow.md
    set-architecture-workflow.md
    asset-validation-workflow.md
    submission-audit-workflow.md
    release-packaging-workflow.md
    ip-production-workflow.md
    post-release-learning-workflow.md
    schema-validation-workflow.md
    ci-maintenance-workflow.md

  skills/
    line-emoji-router/
      SKILL.md
    line-emoji-market-scout/
      SKILL.md
    line-emoji-brand-distiller/
      SKILL.md
    line-emoji-set-architect/
      SKILL.md
    line-emoji-production-director/
      SKILL.md
    line-emoji-asset-validator/
      SKILL.md
    line-emoji-submission-auditor/
      SKILL.md
    line-emoji-ip-governor/
      SKILL.md
    line-emoji-release-packager/
      SKILL.md
    line-emoji-post-release-analyst/
      SKILL.md
    line-emoji-factory-auditor/
      SKILL.md

  templates/
    brand/
    release/
    qa/
    prompts/
    repo/
    ip/
    market/
    submission/
    improvement/

  schemas/
    brand-manifest.schema.json
    release-spec.schema.json
    production-handoff.schema.json
    quality-ledger.schema.json
    usage-validation.schema.json
    market-observation.schema.json
    submission-metadata.schema.json
    asset-validation-report.schema.json
    ip-style-bible.schema.json
    reference-asset-register.schema.json

  tools/
    init-brand-repo.ps1
    validate-brand-repo.ps1
    validate-assets.py
    validate-metadata.py
    package-release.py
    sync-shared-snapshots.ps1
    check-placeholders.py
    validate-schemas.py

  tests/
    scaffold/
    schemas/
    validators/

  examples/
    soeshirushi/

  sandbox/
    experiments/

  .github/
    workflows/
      validate.yml
```

---

## 17. P0 改善ロードマップ

P0 は、これをやらないと今後の改善が積み上がらないもの。

### P0-1. 全ファイル整形

#### 内容

- Markdown を通常の複数行へ
- YAML を1キー1行へ
- PowerShell を複数行へ
- diff しやすくする

#### 完了条件

```text
markdownlint が通る
yamllint が通る
PowerShell syntax check が通る
```

### P0-2. README 再構築

#### 内容

- 目的
- quickstart
- スキル説明
- tools 説明
- example 導線
- brand repo 作成手順

#### 完了条件

```text
README だけで新規ブランドrepo作成の入口が分かる
```

### P0-3. スキル再編

#### 内容

- `line-emoji-producer` を `line-emoji-router` へ変更
- 監査系3スキルを `line-emoji-factory-auditor` へ統合
- P0新規スキルを追加

#### P0新規スキル

```text
line-emoji-asset-validator
line-emoji-submission-auditor
line-emoji-ip-governor
```

### P0-4. schema 新設

#### 内容

```text
schemas/brand-manifest.schema.json
schemas/release-spec.schema.json
schemas/submission-metadata.schema.json
```

#### 完了条件

```text
brand-manifest.yaml が schema validation できる
release-spec.md または yaml が validation できる
submission metadata が validation できる
```

### P0-5. validator 新設

#### 内容

```text
tools/validate-brand-repo.ps1
tools/validate-assets.py
tools/validate-metadata.py
```

#### 完了条件

```text
生成された brand repo を validate できる
画像仕様の最低限を validate できる
metadata の文字数と禁止条件を validate できる
```

### P0-6. CI 新設

#### 内容

```text
.github/workflows/validate.yml
```

#### 完了条件

```text
scaffold smoke test が main で通る
schema validation が main で通る
placeholder check が main で通る
```

### P0-7. `sandbox/soeshirushi` を `examples/soeshirushi` へ移動

#### 完了条件

```text
examples/soeshirushi が標準例として README から参照される
sandbox は壊してよい実験場として残る
```

---

## 18. P1 改善ロードマップ

P1 は、工場の生産性と品質を上げるもの。

```text
line-emoji-market-scout
line-emoji-brand-distiller
line-emoji-set-architect
line-emoji-production-director
line-emoji-release-packager
```

追加する templates。

```text
templates/market/
templates/brand/
templates/release/
templates/submission/
templates/prompts/
```

追加する workflows。

```text
market-observation-workflow.md
brand-distillation-workflow.md
set-architecture-workflow.md
release-packaging-workflow.md
```

---

## 19. P2 改善ロードマップ

P2 は、継続改善と実運用データ活用。

```text
line-emoji-post-release-analyst
post-release-metrics-template.md
sales-analysis-template.md
review-outcome-log-template.md
next-release-recommendation-template.md
```

将来的には、LINE Creators Market の実績データを手動入力またはCSVで取り込み、次 release と factory improvement ledger に反映する。

---

## 20. 具体的な GitHub Issue 案

### Issue 1: Rewrite README as user-facing quickstart

```text
Type: docs
Priority: P0
```

内容:

- purpose
- quickstart
- directory map
- skill map
- tool map
- example link
- brand repo lifecycle

### Issue 2: Normalize Markdown / YAML / PowerShell formatting

```text
Type: maintenance
Priority: P0
```

内容:

- one-line files を複数行化
- markdownlint 導入
- yamllint 導入
- PSScriptAnalyzer 導入

### Issue 3: Replace producer with router and split responsibilities

```text
Type: skill-refactor
Priority: P0
```

内容:

- `line-emoji-producer` を `line-emoji-router` に変更
- 実務責務を新スキルへ移す

### Issue 4: Merge audit skills into factory-auditor

```text
Type: skill-refactor
Priority: P0
```

内容:

- doc-auditor
- improvement-auditor
- factory-evolver
- skill-builder

を統合または廃止。

### Issue 5: Add asset validator

```text
Type: tool
Priority: P0
```

内容:

- `tools/validate-assets.py`
- 画像寸法
- PNG
- 透過
- RGB
- ファイルサイズ
- 個数
- ZIPサイズ

### Issue 6: Add metadata validator

```text
Type: tool
Priority: P0
```

内容:

- `tools/validate-metadata.py`
- title
- description
- creator
- copyright
- forbidden expressions

### Issue 7: Add brand manifest schema

```text
Type: schema
Priority: P0
```

内容:

- `schemas/brand-manifest.schema.json`
- manifest template 更新
- generated repo validation

### Issue 8: Add CI validation workflow

```text
Type: ci
Priority: P0
```

内容:

- Markdown lint
- YAML parse
- schema validation
- scaffold smoke test
- placeholder check

### Issue 9: Add fixed-IP governance package

```text
Type: feature
Priority: P0
```

内容:

- `line-emoji-ip-governor`
- `ip-governance-rules.md`
- `ip-production-workflow.md`
- IP templates

### Issue 10: Move soeshirushi from sandbox to examples

```text
Type: repo-structure
Priority: P0
```

内容:

- `sandbox/soeshirushi` → `examples/soeshirushi`
- README から参照
- sandbox は experiments 用に再定義

---

## 21. 最終判断

現状の `line-emoji-factory` は、思想としては良い。

しかし、現状がベストではない。

特に壊すべきなのは、以下である。

```text
- producer の巨大化
- 監査系スキルの重複
- 実務スキル不足
- validator 不在
- schema 不在
- CI 不在
- README 不足
- templates の非階層化
- 固定IP統制不足
- 市場証跡不足
- submission package 不足
```

残すべきなのは、以下である。

```text
- 構造 → ブランド → 商品
- LINE絵文字固有制約を先に見る
- 共通基盤と個別ブランドの分離
- snapshot 配布
- QA gate
- 使用シーン検証
- ふりかえり
- 改善台帳
```

最終的な改善方向は、**考える工場から、作る・検査する・提出する・学ぶ工場へ拡張すること**である。

最優先は、スキルを増やすことそのものではなく、次の3つである。

```text
1. 壊れないようにする
   - schema
   - CI
   - scaffold test
   - placeholder check

2. 申請できるようにする
   - asset validator
   - metadata validator
   - release packager
   - submission auditor

3. 個別ブランドを安全に増やせるようにする
   - market evidence
   - fixed-IP governance
   - brand repo manifest
   - examples
```

この3つを満たすと、`line-emoji-factory` は単なるドキュメント集ではなく、継続的にLINE絵文字ブランドを作り、検査し、改善するための実用的な制作基盤になる。
