# 品質管理ワークフロー

このファイルは、ブランド工場における継続品質管理の正本である。
対象は、創出ブランドの監査、生成絵文字の監査、初期 release 設計、rough review、
handoff review、完成物 QA、審査差し戻し対応、公開後の drift 監視までを含む。

## 境界
- このフローは `構造 → ブランド → 商品` の評価順を置き換えない。
- 構造 `Fail` を QA で握りつぶさない。
- 構造問題は必ず `workflows/transformation-workflow.md` に戻す。
- 公式仕様の事実は `rules/line-platform-baseline.md` を正本にする。
- 商品品質の評価語彙は `rules/evaluation-model.md` と `rules/emoji-product-rules.md` を使う。

## 起動条件
- 初期 release を設計する。
- 創出ブランドや生成された絵文字を監査したい。
- rough board が出た。
- production handoff を確定したい。
- 完成データを提出前に点検したい。
- 審査差し戻しや公開後問題が出た。
- 同種の品質事故が複数ブランド、複数 release で再発した。

## 品質問題の分類
- `構造後退`
  - 単体成立、インライン成立、連続使用成立が崩れている。
- `ブランド drift`
  - 核、視覚記号、差分軸、温度感が揺れている。
- `商品品質不良`
  - 視認性、即読性、差分明確性、セット整合性、再使用性が弱い。
- `制作パイプライン不良`
  - rough stage と仕上げ stage の責務や handoff が曖昧。
- `metadata / review 不良`
  - タイトル、説明文、コピーライト、タグ、審査リスク対応が弱い。
- `運用記録不良`
  - release spec、checklist、quality ledger、release log が未更新。
- `改善機構過重`
  - quality ledger、handoff、workflow、skill が重くなり、監査より管理コストが前に出ている。

## 使う正本
- release 単位の設計: `templates/release-spec-template.md`
- release 前チェック: `templates/release-checklist-template.md`
- 継続品質の論点管理: `templates/quality-ledger-template.md`
- 提出 / 審査 / 公開履歴: `templates/release-log-template.md`
- 制作工程の基盤: `workflows/production-pipeline-workflow.md`
- 具体会話検証: `workflows/usage-validation-workflow.md`, `templates/usage-validation-template.md`
- 節目の振り返り圧縮: `workflows/release-retrospective-workflow.md`, `templates/release-retrospective-template.md`
- factory への再発学習: `workflows/continuous-improvement-workflow.md`, `templates/factory-improvement-ledger-template.md`

## Gate 0: release 設計の成立確認
### 必須入力
- `brand-setting`
- `brand-production-brief`
- `release-spec`

### 確認すること
- この release の目的と使用場面が定義されている。
- この release の一言コンセプトと、ブランド内での役割が定義されている。
- 最上段に置く高頻度絵文字が決まっている。
- 初期セット個数の根拠が言語化されている。
- 差分軸と重複禁止ルールが release 単位で言語化されている。
- 組み合わせ補助枠を入れる場合、数量と役割が release 単位で言語化されている。
- brand 固定条件と release 固有条件が混線していない。
- `release-checklist`, `quality-ledger`, `release-log` を初期化できる。

### Gate 0 で止めるべき状態
- set の目的がなく、単なる寄せ集めになっている。
- release 固有コンセプトがなく、ブランド説明の言い換えだけになっている。
- 初期セット個数が `作りやすい最小数` に寄りすぎ、商品としての厚みが足りない。
- 高頻度用途より雰囲気優先の絵柄が上に来る。
- 組み合わせ補助枠が多すぎ、高頻度枠や主力用途を圧迫している。
- 差分軸が曖昧で、似た絵文字の水増しが見える。

## Gate 1: rough quality review
### 入力
- `release-spec`
- rough board
- `brand-production-brief`

### 確認すること
- rough board で set 全体の核と差分軸が読める。
- 主要絵文字が小表示でも成立する見込みがある。
- 全体図頼みの案や配置依存の案が紛れ込んでいない。
- 後工程へ渡すべき keep / trim / drift が言語化できる。

### 問題が出たときの戻し先
- `構造後退` は `workflows/transformation-workflow.md`
- `ブランド drift` は `brand-setting` または `brand-production-brief`
- `商品品質不良` と `制作パイプライン不良` は `release-spec` または rough 再設計

## Concrete Usage Validation
- `release-spec` ができたら、具体会話検証を行う。
- 検証は `単体送信 / 文中使用 / 2個連続または左右ペア` を最低限含める。
- 代替される `句読点 / 既存記号 / 既存絵文字` と比べて、商品として残す理由があるかを見る。
- 強い負け筋が見えたら `release-spec`, `production-handoff`, `quality-ledger` を更新する。
- 同じ負け筋が再発するなら `workflows/continuous-improvement-workflow.md` に送る。

## Gate 2: handoff quality review
### 入力
- `production-handoff`
- `release-spec`
- rough board
- `brand-system-prompt`

### 確認すること
- 各絵文字に `用途 / 単体送信時の意味 / 文中使用時の意味` がある。
- ClaudeDesign に渡す keep / trim / drift が明示されている。
- set 全体条件と個別絵文字条件が分離されている。
- 未解決の `Watch` 項目が handoff と quality ledger に残っている。

### Gate 2 で止めるべき状態
- handoff が「いい感じに整える」で終わっている。
- rough から何を残し、何を削るかが書かれていない。
- Stage 2 に構造判断まで押し込んでいる。

## Gate 3: final asset QA
### 入力
- 完成データ
- `release-checklist`
- `quality-ledger`
- metadata 案

### 確認すること
- 公式仕様、視認性、差分明確性、セット整合性を通る。
- metadata と絵文字内容が一致している。
- animation を使う場合は 1 フレーム目で意味が読める。
- 提出を止めるべき blocking 問題がない。

### Gate 3 の原則
- `Hard NG` は提出しない。
- `Revise` 相当の弱点は checklist の blocking 項目として止める。
- `Watch` は quality ledger に残し、次 release の改善対象へ送る。

## Gate 4: 提出 / 審査 / 公開後
### 必須出力
- `submissions/release-log.md` 更新
- `qa/quality-ledger.md` 更新

### 確認すること
- 審査差し戻し理由を release log に残したか。
- 差し戻し理由を stage 固有問題か factory 基盤問題か分類したか。
- 再発しうる問題を quality ledger に移したか。
- 再発や skill blind spot が見えたら `workflows/continuous-improvement-workflow.md` に接続したか。
- milestone が切り替わったら `workflows/release-retrospective-workflow.md` で振り返りを圧縮したか。

## Lightweight Check
- quality ledger の履歴が active 論点を埋めていないか。
- 同じ論点が handoff、checklist、quality ledger に重複していないか。
- 監査項目が多すぎて、1 絵文字単位の判断が遅くなっていないか。
- brand 固有問題まで factory 化していないか。
- 改善機構が重い場合、`削る / 要約する / owner file へ寄せる / factory へ昇格させる` のどれで軽くするか決めたか。

## Factory へ昇格させる条件
次のどれかに当たるときは、ブランド repo の修正だけで終えず、
工場本体の owner file を更新する。
- 同種の問題が 2 release 以上で再発した。
- 同種の問題が 2 ブランド以上で再発した。
- script の scaffold 不備が原因だった。
- brand-production-brief や production-handoff の項目欠落が原因だった。
- quality ledger だけでは抑えきれず、共通 workflow を変える必要がある。
- 改善機構そのものが重く、継続監査を妨げている。
- skill の入口不足や責務過多が再発原因になっている。

## 監査で必ず見るもの
- blocking 問題が checklist で止まる設計か。
- `Watch` が quality ledger に繋がっているか。
- release log に審査差し戻しと修正履歴が残るか。
- brand repo 側に production と quality の snapshot があるか。
- 生成絵文字 1 件単位でも監査可能な粒度になっているか。
- 監査の仕組み自体が重くなったときの戻し先があるか。
