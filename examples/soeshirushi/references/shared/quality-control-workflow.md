# 品質管理ワークフロー

このファイルは、ブランド工場における継続品質管理の正本である。
対象は、創出ブランドの監査、シリーズ企画、rough / anchor review、item finalization review、
完成物 QA、審査差し戻し対応、公開後の drift 監視までを含む。

## 境界
- このフローは `構造 → ブランド → 商品` の評価順を置き換えない。
- 構造 `Fail` を QA で握りつぶさない。
- 構造問題は必ず `workflows/transformation-workflow.md` に戻す。
- 公式仕様の事実は `rules/line-platform-baseline.md` を正本にする。
- 商品品質の評価語彙は `rules/evaluation-model.md` と item type に応じた `rules/emoji-product-rules.md` / `rules/sticker-product-rules.md` を使う。
- 実画像の商品品質は `rules/visual-asset-quality-rules.md` を使う。

## 起動条件
- 初期 release を設計する。
- 既存ブランドで新シリーズを作る。
- 創出ブランドや生成されたアイテムを監査したい。
- rough board、style anchor、character anchor が出た。
- production handoff を確定したい。
- 1アイテムの finalization 候補が出た。
- 完成データを提出前に点検したい。
- 審査差し戻しや公開後問題が出た。
- 同種の品質事故が複数ブランド、複数 release で再発した。

## 品質問題の分類
- `構造後退`
  - 単体成立、インライン成立、連続使用成立が崩れている。
- `ブランド drift`
  - 核、視覚記号、差分軸、温度感が揺れている。
- `シリーズ差分不良`
  - 過去商品との差分が弱い、または新鮮さのために brand canon を壊している。
- `商品品質不良`
  - 視認性、即読性、差分明確性、セット整合性、再使用性が弱い。
- `画像品質不良`
  - 透過、太線、余白、装飾、低コントラスト、背景混入、小表示が弱い。
- `制作パイプライン不良`
  - rough / anchor、item finalization、product QA の責務や handoff が曖昧。
- `metadata / review 不良`
  - タイトル、説明文、コピーライト、タグ、審査リスク対応が弱い。
- `運用記録不良`
  - series plan、release spec、checklist、quality ledger、product catalog、release log が未更新。
- `改善機構過重`
  - quality ledger、handoff、workflow、skill が重くなり、監査より管理コストが前に出ている。

## 使う正本
- brand canon: `templates/brand/brand-canon-template.md`
- brand product catalog: `templates/brand/brand-product-catalog-template.md`
- series plan: `templates/release/series-plan-template.md`
- release 単位の設計: `templates/release/release-spec-template.md`
- release 前チェック: `templates/qa/release-checklist-template.md`
- 継続品質の論点管理: `templates/qa/quality-ledger-template.md`
- 提出 / 審査 / 公開履歴: `templates/release/release-log-template.md`
- visual QA: `rules/visual-asset-quality-rules.md`
- 画像検査: `rules/asset-validation-rules.md`, `workflows/asset-validation-workflow.md`, `tools/validate-assets.py`
- metadata 検査: `rules/submission-metadata-rules.md`, `tools/validate-metadata.py`
- 申請前監査: `workflows/submission-audit-workflow.md`
- 制作工程の基盤: `workflows/production-pipeline-workflow.md`
- item 生成手順: `workflows/item-generation-workflow.md`
- 具体会話検証: `workflows/usage-validation-workflow.md`, `templates/qa/usage-validation-template.md`
- 節目の振り返り圧縮: `workflows/release-retrospective-workflow.md`, `templates/qa/release-retrospective-template.md`
- factory への再発学習: `workflows/continuous-improvement-workflow.md`, `templates/improvement/factory-improvement-ledger-template.md`

## Gate 0: Brand Canon / IP Guardrails
### 必須入力
- `brand-setting`
- `brand-canon`
- 固定IPの場合は `ip-style-bible` と reference register

### 確認すること
- ブランドコアコンセプトが item 単位で使える。
- 絶対に守る視覚要素、可変要素、禁止 drift が分かれている。
- 感情レンジ、配色、線、世界観境界が定義されている。
- 類似ブランド / 他IP と混同しないための注意点がある。

### 止める状態
- brand canon がなく、雰囲気だけで制作へ進んでいる。
- 固定IPなのに許諾範囲や禁止表現が不明。
- 新鮮さのためにブランド核を変えている。

## Gate 1: Series Planning / Release Differentiation
### 必須入力
- `brand-product-catalog`
- `series-plan`
- `release-spec`

### 確認すること
- 過去商品との差分、継承要素、新規性要素が定義されている。
- 既存シリーズとの重複リスクとカニバリゼーション回避が書かれている。
- この release の目的、使用場面、感情レンジ、テーマが商品単位で説明できる。
- 高頻度アイテム、主力枠、補助枠が過去商品と使い分けできる。

### 止める状態
- ブランド説明の言い換えだけで release 固有コンセプトがない。
- 過去商品との差分が曖昧。
- 似た用途を増やしているだけ。
- 逆にブランド/IPを壊すほど逸脱している。

## Gate 2: Rough / Anchor Quality Review
### 入力
- `series-plan`
- `release-spec`
- style anchor
- character / motif anchor
- rough board
- `brand-production-brief`

### 確認すること
- rough board で set 全体の核と差分軸が読める。
- style anchor と character / motif anchor が brand canon を壊していない。
- 主要アイテムが小表示またはスタンププレビューでも成立する見込みがある。
- 全体図頼みの案や配置依存の案が紛れ込んでいない。
- 後工程へ渡すべき keep / trim / drift が言語化できる。

### 問題が出たときの戻し先
- `構造後退` は `workflows/transformation-workflow.md`
- `ブランド drift` は `brand-canon` または `brand-production-brief`
- `シリーズ差分不良` は `series-plan`
- `商品品質不良` と `制作パイプライン不良` は `release-spec` または rough 再設計

## Concrete Usage Validation
- `release-spec` ができたら、具体会話検証を行う。
- 検証は item type に応じて `単体送信 / 文中使用 / 2個連続または左右ペア / スタンプ送信時の発話` を使い分ける。
- 代替される `句読点 / 既存記号 / 既存絵文字 / 既存スタンプ` と比べて、商品として残す理由があるかを見る。
- 強い負け筋が見えたら `series-plan`, `release-spec`, `production-handoff`, `quality-ledger` を更新する。
- 同じ負け筋が再発するなら `workflows/continuous-improvement-workflow.md` に送る。

## Gate 3: Item Finalization Review
### 入力
- `production-handoff`
- `item-image-prompt`
- 1アイテム4案以上の candidate
- rough / anchor
- `quality-ledger`

### 確認すること
- 各アイテムに item type に応じた `用途 / 単体送信時の意味 / 文中使用時の意味 / スタンプ送信時の発話` がある。
- 候補4案が実質同じではない。
- 残す視覚記号と削る装飾が明示されている。
- 禁止 drift、ブランド固有要素、シリーズ固有要素、過去商品との差分が prompt に入っている。
- 小表示で残す要素が定義されている。

### 止める状態
- handoff が「いい感じに整える」で終わっている。
- 1案だけで採用しようとしている。
- 背景、小物、装飾、細線で意味を補っている。
- Stage 3 に構造判断やシリーズ企画まで押し込んでいる。

## Gate 4: Product QA / Final Asset QA
### 入力
- 完成データ
- contact sheet
- chat preview
- asset validation report
- `release-checklist`
- `quality-ledger`
- metadata 案

### 確認すること
- 公式仕様、視認性、差分明確性、セット整合性を通る。
- `180px / 96px / 48px / 32px` 相当で主要要素が読める。
- `tools/validate-assets.py` が blocking 違反を出していない。
- `tools/validate-metadata.py` が blocking 違反を出していない。
- near-duplicate、用途被り、表情差分/ポーズ差分の弱さが放置されていない。
- 余白過多、低コントラスト、背景混入、装飾過多がない。
- metadata と item 内容が一致している。
- animation を使う場合は 1 フレーム目で意味が読める。
- `かわいいが売れない`、`きれいだが使えない` に当たらない。

### Gate 4 の原則
- `Hard NG` は提出しない。
- `Revise` 相当の弱点は checklist の blocking 項目として止める。
- `Watch` は quality ledger と product catalog に残し、次 release の改善対象へ送る。

## Gate 5: Release Ledger / Catalog Update
### 必須出力
- `releases/<release-id>/release-log.md` 更新
- `qa/quality-ledger.md` 更新
- `brand/product-catalog.md` 更新
- `releases/<release-id>/series-plan.md` 結果欄更新

### 確認すること
- 今回のシリーズの位置づけが catalog に残っている。
- 過去商品との差分、継承要素、成功した差分軸が記録されている。
- 避けるべき重複、壊してはいけないIP要素が次シリーズから読める。
- 審査差し戻し理由を release log に残したか。
- 再発しうる問題を quality ledger に移したか。
- 再発や skill blind spot が見えたら `workflows/continuous-improvement-workflow.md` に接続したか。
- milestone が切り替わったら `workflows/release-retrospective-workflow.md` で振り返りを圧縮したか。

## Lightweight Check
- quality ledger の履歴が active 論点を埋めていないか。
- 同じ論点が handoff、checklist、quality ledger、product catalog に重複していないか。
- 監査項目が多すぎて、1アイテム単位の判断が遅くなっていないか。
- brand 固有問題まで factory 化していないか。
- 改善機構が重い場合、`削る / 要約する / owner file へ寄せる / factory へ昇格させる` のどれで軽くするか決めたか。

## Factory へ昇格させる条件
次のどれかに当たるときは、ブランド repo の修正だけで終えず、
工場本体の owner file を更新する。
- 同種の問題が 2 release 以上で再発した。
- 同種の問題が 2 ブランド以上で再発した。
- script の scaffold 不備が原因だった。
- brand-canon、brand-production-brief、series-plan、production-handoff の項目欠落が原因だった。
- quality ledger だけでは抑えきれず、共通 workflow を変える必要がある。
- 改善機構そのものが重く、継続監査を妨げている。
- skill の入口不足や責務過多が再発原因になっている。

## 監査で必ず見るもの
- blocking 問題が checklist で止まる設計か。
- `Watch` が quality ledger と product catalog に繋がっているか。
- release log に審査差し戻しと修正履歴が残るか。
- brand repo 側に production と quality の snapshot があるか。
- 生成アイテム1件単位でも監査可能な粒度になっているか。
- 監査の仕組み自体が重くなったときの戻し先があるか。
