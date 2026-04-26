# 共通制作パイプライン ワークフロー

このファイルは、全ブランド共通で使う制作実装フローの正本である。
標準運用は `GPT / image_gen` を中心に完結する。
外部デザイン支援や second review を使ってもよいが、必須工程にはしない。

制作は「一括で最終商品を自動生成して終わり」にしない。
rough / anchor は方向確認、finalization は 1 アイテム単位の商品化として責務を分ける。

## 境界
- このフローは、`構造 → ブランド → 商品` の判断順序を置き換えない。
- 構造で `Fail` した案を、このフローで救済しない。
- 構造 `Fail` は、必ず先に `workflows/transformation-workflow.md` で変換する。
- `GPT / image_gen` は rough、anchor、候補生成、修正案作成に使える。
- final asset は、item spec、候補比較、小表示 QA、release QA を通過して初めて採用候補にする。
- 任意の外部支援は `optional second review / optional art direction / external design support` として扱う。

## 開始条件
- 少なくとも、構造 `Fail` ではない。
- ブランド核、視覚記号、主要使用場面が揺れすぎていない。
- `Design Ready` 相当まで見えた案だけを本格制作へ送る。
- 新シリーズの場合は、過去商品との差分と継承要素を先に読める状態にする。

## 制作で固定する正本
- ブランド核: `templates/brand/brand-setting-template.md`
- ブランド canon / IP guardrails: `templates/brand/brand-canon-template.md`
- ブランド共通の制作実装条件: `templates/brand/brand-production-brief-template.md`
- ブランド商品履歴: `templates/brand/brand-product-catalog-template.md`
- series planning: `templates/release/series-plan-template.md`
- release / set の範囲と差分計画: `templates/release/release-spec-template.md`
- release / set ごとの受け渡し条件: `templates/release/production-handoff-template.md`
- item finalization prompt: `templates/prompts/item-image-prompt-template.md`
- AIへの工程別指示束: `templates/brand/brand-system-prompt-template.md`

## Stage 0: Brand Canon / IP Guardrails
### 目的
- ブランドの核、壊してはいけない視覚要素、許容差分、禁止 drift を固定する。
- 複数シリーズへ展開しても、ブランド/IP の同一性が壊れない境界を作る。

### 必須出力
- brand canon
- 守る視覚記号、可変要素、禁止 drift
- 感情レンジ、トーン&マナー、配色、線、世界観境界
- 類似ブランドや他IPと混同しないための注意点

### 通過条件
- 何を変えてよく、何を変えてはいけないかが item 単位で使える。
- 固定IPや既存資産がある場合、許諾範囲と参照素材ルールが切り分けられている。

## Stage 1: Series Planning
### 目的
- 過去商品を参照し、新シリーズで継承する要素と差別化する要素を決める。
- 商品としての狙い、想定利用シーン、感情レンジ、テーマ、差分軸を固定する。

### 必須出力
- series plan
- 過去商品との差分、重複リスク、カニバリゼーション回避
- 今後の拡張余地
- release spec の初版

### 通過条件
- ブランドらしさと新鮮さの両方が説明できる。
- 既存シリーズと似すぎず、逆にブランド/IP を壊すほど逸脱していない。
- LINE上の会話で使い分けられる用途がある。

## Stage 2: Rough / Anchor Generation
### 目的
- ブランド核とシリーズ差分軸を壊さず、絵柄、世界観、差分軸を早く確認する。
- 最終商品ではなく、style anchor、character anchor、rough board を作る。

### 必須出力
- style anchor
- character / motif anchor
- rough board
- 高頻度アイテムのラフ
- 差分軸の見取り図
- rough で採るもの / 捨てるもの / 未確定のもの

### 禁止
- rough board を final asset として採用する。
- 全体図でしか成立しない案を通す。
- 雰囲気だけで 1 アイテムごとの意味不足を隠す。
- ブランド核が曖昧なまま、色味や装飾だけ先に固定する。

### 通過条件
- 主要アイテムが小表示またはスタンププレビューでも読める見込みがある。
- 差分軸が set 全体で重複していない。
- 1アイテムごとの用途と反応が説明できる。
- Stage 3 へ渡す共通条件と個別条件を言語化できる。

## Stage 3: Item Finalization
### 目的
- 1アイテムずつ、選択した LINE item type として完成候補へ落とす。
- 1アイテム単位で意味、用途、小表示で残す要素を固定し、最低4案を比較する。

### 必須入力
- brand canon
- brand production brief
- product catalog / series plan
- release spec
- production handoff
- item image prompt
- rough / anchor outputs

### 必須出力
- item spec
- 1アイテム4案以上の candidate
- 候補比較
- 小表示チェック結果
- 採用候補、差し戻し理由、再生成指示
- final asset 候補

### finalization の最低条件
- 背景透過。
- 太いアウトライン。
- 余白が少なく、主情報が大きい。
- 装飾が少なく、シルエットで読める。
- 表情差分またはポーズ差分が明確。
- 単体送信時、文中使用時、スタンプ送信時の意味が説明できる。
- 過去商品との差分ポイントを壊さない。

### 禁止
- セット全体を一括生成して、そのまま final asset にする。
- 1案だけで採用する。
- `かわいいが使い道不明`、`きれいだが小表示で読めない` を通す。
- 背景、小物、効果線、細線、淡色だけで意味を作る。

## Stage 4: Product QA
### 目的
- LINE商品としての読みやすさ、使いやすさ、差分明確性、セット整合性を検査する。

### 必須確認
- `180px / 96px / 48px / 32px` 相当の視認性。
- contact sheet と chat preview。
- near-duplicate、用途被り、表情差分/ポーズ差分の弱さ。
- 余白過多、低コントラスト、背景混入、装飾過多。
- brand canon / series plan / release spec との一致。

### 差し戻し
- `構造不成立` は `workflows/transformation-workflow.md`。
- `ブランド drift` は Stage 0。
- `シリーズ差分不明` は Stage 1。
- `rough / anchor 不足` は Stage 2。
- `個別アイテム品質不良` は Stage 3。

## Stage 5: Release Ledger / Catalog Update
### 目的
- 今回のシリーズの位置づけ、過去商品との差分、継承要素、今後の拡張余地を残す。
- 次シリーズ開発時の参照資産にする。

### 必須出力
- release log 更新
- quality ledger 更新
- brand product catalog 更新
- series plan の結果欄更新
- 次シリーズへ持ち越す `Watch`

### 完了条件
- final asset は QA を通過している。
- 過去商品との差分と継承要素が catalog に残っている。
- 次シリーズで避ける重複と伸ばす差分軸が読める。

## Quality Gate
- 提出前と継続改善は `workflows/quality-control-workflow.md` を使う。
- 生成結果の強弱は `workflows/usage-validation-workflow.md` で具体会話に通す。
- 監査結果や運用上の学習は `workflows/continuous-improvement-workflow.md` へ戻す。
- blocking 問題が `release-checklist` に残る間は提出しない。
- `Watch` 項目は `quality-ledger`、release handoff、brand product catalog に引き継ぐ。

## release / set ごとの最小出力
- brand canon: `brand/brand-canon.md`
- brand product catalog: `brand/product-catalog.md`
- series plan: `releases/*/series-plan.md`
- セット仕様: `releases/*/release-spec.md`
- handoff 文書: `releases/*/production-handoff.md`
- release checklist: `qa/release-checklist.md`
- quality ledger: `qa/quality-ledger.md`
- rough board 置き場: `production/rough-boards/`
- 完成データ置き場: `production/finals/`
- release log: `releases/*/release-log.md`
- prompt 蓄積: `prompts/`

## 回答や設計で必ず明示すること
- Stage 0 で守る brand canon / IP guardrails。
- Stage 1 で継承する要素と新規性要素。
- Stage 2 で固定する anchor と未確定にする点。
- Stage 3 で 1アイテムごとに比較する案数、残す視覚記号、削る装飾。
- Stage 4 で止める QA 条件。
- Stage 5 で更新する ledger / catalog。
- 差し戻し先。
- 正本ファイルの更新順。
