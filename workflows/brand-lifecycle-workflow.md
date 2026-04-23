# ブランド運用・分離ワークフロー

このファイルは、ブランド創出後に
「工場本体に残すか」「ブランド別リポジトリへ分離するか」
を決めるための正本である。

## 結論
- デフォルトは **ハイブリッド運用** にする。
- つまり、
  - ブランド探索と初期設計はこの工場リポジトリで行う。
  - `Design Ready` を超えて、継続制作・独立運用が必要になったブランドだけ別リポジトリへ分離する。

## なぜ常時一元管理ではないか
- 早期探索では速い。
- ただしブランド数が増えると、資産、prompt、QA、リリース履歴が混ざる。
- LLM運用時に別ブランドの文脈混入が起きやすい。
- 将来的に外注、共同制作、商品化連携へ渡しにくい。

## なぜ常時分離でもないか
- 早期候補の段階で repo を切ると、失敗案にも運用コストが乗る。
- 比較評価や変換を跨いだ判断が遅くなる。
- 工場本体の学習や query 改善が蓄積しにくい。

## 推奨モデル
### Stage 0: 探索前
- まだブランド核がない。
- 工場本体のみで扱う。

### Stage 1: 探索中
- 候補出し、変換、比較を繰り返す。
- 工場本体のみで扱う。

### Stage 2: 設計確定直前
- `Design Ready` 候補が見えた。
- `templates/brand-setting-template.md` と `templates/brand-production-brief-template.md` を埋める。
- `templates/release-spec-template.md` を埋める。
- 必要なら `templates/release-checklist-template.md`, `templates/quality-ledger-template.md`, `templates/release-log-template.md` を初期化する。
- 必要なら `templates/production-handoff-template.md` の初版を埋める。
- まだ工場本体に置く。

### Stage 3: 独立運用開始
- 初期セットの制作を始める。
- 同一ブランドで prompt、QA、品質台帳、リリース履歴、差分資産が増える。
- この時点で別リポジトリへ分離する。

### Stage 4: 拡張・量産
- 派生シリーズ、季節版、アニメ版、商品化連携が走る。
- ブランド別リポジトリで継続運用する。

## 分離の判定条件
次の条件を **4つ以上** 満たしたら分離を推奨する。
- `Design Ready` に到達している。
- `brand-setting` が埋まっている。
- `brand-production-brief` が埋まっている。
- 初期 release spec がある。
- 初期 release の handoff 文書がある。
- 初期セット構成が固まっている。
- ブランド固有の工程別 AI 指示を継続使用する見込みがある。
- QA、品質台帳、審査ログをブランド別に蓄積したい。
- 今後 2回以上のリリースや改訂を見込む。
- 別の担当者や外部協力者に渡す可能性がある。
- 商品化・ライセンス拡張の話が出ている。

## 工場本体に残すべき条件
次のどれかに当たる間は、分離しない。
- まだ `Revise` が大きい。
- ブランド核が揺れている。
- セット構成より先に比較や変換が必要。
- 量産より前に、ブランド自体を切る可能性が高い。

## 分離時の設計原則
- **live dependency にしない。**
- 工場本体のルールを submodule やシンボリックリンクで参照させない。
- 分離時点の共通基盤を **snapshot として持ち出す。**
- snapshot には `factory_base_version` と `template_schema_version` を残す。
- 以後の共通基盤更新は、ブランド repo 側で **任意に取り込む。**

## 持ち出すべき共通基盤
### 必須
- `rules/evaluation-model.md` の snapshot
- `rules/line-platform-baseline.md` の snapshot
- `rules/structure-constraints.md` の snapshot
- `rules/emoji-product-rules.md` の snapshot
- `rules/review-risk-rules.md` の snapshot
- `rules/continuous-improvement-rules.md` の snapshot
- `workflows/transformation-workflow.md` の snapshot
- `workflows/production-pipeline-workflow.md` の snapshot
- `workflows/quality-control-workflow.md` の snapshot
- `workflows/continuous-improvement-workflow.md` の snapshot
- `templates/brand-setting-template.md` から埋めたブランド設定
- `templates/brand-production-brief-template.md` から埋めた制作基盤
- `templates/release-spec-template.md` から埋めた release spec
- `templates/production-handoff-template.md` から埋めた release handoff
- `templates/brand-system-prompt-template.md` から埋めた専用AI制作指示
- `templates/brand-repo-manifest-template.yaml` から埋めた manifest

### 推奨
- prompt 集
- QA checklist
- quality ledger
- 審査対応ログ
- 提出履歴

### 持ち出さないもの
- 工場本体の ideation 用比較資料
- 他ブランドの設定
- ブランド分類や探索候補の履歴全部
- 工場全体の skill 定義

## 実現方法
### 第一推奨
- この工場 repo を正本に保つ。
- `scripts/init-brand-repo.ps1` でブランド repo を scaffold する。
- scaffold 時に必要な snapshot とテンプレートだけをコピーする。

### 第二推奨
- 手動で brand repo を作る。
- ただし `templates/brand-repo-blueprint.md` と manifest に従う。

### 非推奨
- 工場 repo をそのまま fork してブランド repo にする。
- 共通基盤を毎回手でつまみ食いしてコピーする。
- 工場 repo と brand repo を live sync させる。

## 同期ポリシー
- 工場本体が更新されても、既存ブランド repo を自動更新しない。
- 公式仕様変更や審査基準変更が入ったときだけ、ブランド repo 側で再同期判断を行う。
- 再同期時は `factory_base_version` を上げ、変更差分を release log に残す。
- 再発問題や運用過重が見えたら、brand repo 側で抱え込まず factory 側の継続改善へ戻す。
