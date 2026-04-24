# 相談運用フロー

このファイルは、通常のブランド相談を処理する標準手順の正本である。
`モード` は内部状態、`出力レシピ` は回答形式であり、同一ではない。

## 標準処理順
1. 相談の目的を把握する。
2. `探索 / 評価 / 設計` のいずれかのモードを選ぶ。
3. 探索モードで新規案出しや市場調査が必要なら `workflows/idea-research-workflow.md` を起動する。
4. `rules/line-platform-baseline.md` で公式仕様と表示事実を確認する。
5. `rules/structure-constraints.md` で構造を判定する。
6. 構造で `Fail` したら `workflows/transformation-workflow.md` へ送る。
7. 構造通過後に `rules/brand-taxonomy.md` と `rules/brand-creation-rules.md` でブランド判断を行う。
8. その後 `rules/emoji-product-rules.md` と `rules/review-risk-rules.md` で商品判断を行う。
9. 最後に `rules/evaluation-model.md` の判定状態へ落とす。
10. `Design Ready` なら `templates/brand-setting-template.md` を埋める。
11. ブランドスタートアップセットを一式化するなら `workflows/brand-startup-set-workflow.md` を起動する。
12. 制作へ進める場合は `workflows/production-pipeline-workflow.md` で共通制作フローを固定する。
13. ブランド固有の制作基盤が必要なら `templates/brand-production-brief-template.md` を埋める。
14. 初期 release / set が必要なら `templates/release-spec-template.md` を埋める。
15. 品質管理が必要なら `workflows/quality-control-workflow.md` を起動し、`templates/release-checklist-template.md`, `templates/quality-ledger-template.md`, `templates/release-log-template.md` を初期化する。
16. release / set ごとの handoff が必要なら `templates/production-handoff-template.md` を埋める。
17. 実会話での勝ち筋確認が必要なら `workflows/usage-validation-workflow.md` と `templates/usage-validation-template.md` を使う。
18. 専用AI制作指示が必要なら `templates/brand-system-prompt-template.md` と工程別 prompt template を埋める。
19. milestone 学習を圧縮するなら `workflows/release-retrospective-workflow.md` と `templates/release-retrospective-template.md` を使う。
20. 継続改善や作業後の学習が必要なら `workflows/continuous-improvement-workflow.md` へ接続する。

## モード判定
### 探索モード
- 方向性が固まっていない。
- 核の有無や変換可能性を見たい。
- 構造不成立の案を、成立形へ変換したい。
- 市場調査を踏まえて多様な候補を出したい。

### 評価モード
- 複数案を比較したい。
- 残す案と切る案を分けたい。
- `Keep` 候補を絞り込みたい。

### 設計モード
- 採用候補を制作可能な仕様へ落としたい。
- ブランド設定、差分設計、初期 release 設計、共通制作フロー、ブランド固有制作基盤、handoff、品質管理、専用AI制作指示まで固めたい。

## モード遷移条件
- `探索 → 評価`
  - 候補が2案以上あり、比較可能な状態になったとき。
- `評価 → 設計`
  - 少なくとも1案が `Design Ready` 相当まで見えたとき。
- `評価 → 探索`
  - 有望案がないか、構造Failから変換し直す必要が出たとき。
- `設計 → 評価`
  - 設計中に `Revise` が大きく、採用見直しが必要になったとき。

## 共通ヘッダ
すべての回答は、最低限以下を含める。
- `モード`
- `構造判定`
- `ブランド判定`
- `商品判定`
- `最終判断`
- `次アクション`

## 出力レシピ
### 短い相談
- 共通ヘッダ
- 要約
- 主要論点
- 改善方針 1〜3件

### 市場調査つき探索相談
- 共通ヘッダ
- 要約
- 観測日と見た範囲
- 混みやすい表現
- 狙うホワイトスペース
- 残す案
- 切る案
- 次に試す軸

### 比較相談
- 共通ヘッダ
- 要約
- 比較軸
- 残す案
- 切る案
- 次に試すこと

### ブランド設計相談
- 共通ヘッダ
- 要約
- ブランド核
- 視覚記号
- 主型 / 副型 / 補助タグ / 採用枠
- 派生方向

### 商品化相談
- 共通ヘッダ
- 要約
- セット構成
- 差分設計
- 優先検証シーン
- 商品品質上の弱点
- リスク

### ブランド固有基盤化相談
- 共通ヘッダ
- 要約
- 推奨パッケージタイプ
- 初期セット個数
- rough stage / handoff / 余白 / アウトライン / アニメーション方針
- サジェスト表示タグ候補
- 審査注意
- 次の制作単位

### ブランドスタートアップセット相談
- 共通ヘッダ
- 要約
- 揃える必須文書
- 共通固定条件
- ブランド可変域
- release 可変域
- 初期 release の買う理由
- prompt 束へ転記する項目
- QA 初期化項目
- 分離判断

### 初期release設計相談
- 共通ヘッダ
- 要約
- release の目的
- 商品コンセプト
- ブランド内での役割
- 初期セット個数の根拠
- 最上段に置く高頻度絵文字
- 主力枠と補助枠の配分
- 差分の軸
- metadata 下書き
- 先に止めるべきリスク

### 制作パイプライン基盤化相談
- 共通ヘッダ
- 要約
- rough stage で固定するもの
- ClaudeDesign へ渡す単位
- handoff で明示するべき差分軸
- 差し戻し先
- 先に埋める正本

### 専用AI制作指示化相談
- 共通ヘッダ
- 要約
- ブランド設定から転記する項目
- rough stage の固定条件
- ClaudeDesign 仕上げ条件
- NG表現

### 品質管理相談
- 共通ヘッダ
- 要約
- blocking 問題
- 具体会話で負ける場面
- `Watch` 項目
- 直す owner file
- 次 release までに固定すること

## 回答原則
- 構造でFailしたら、ブランドや商品を先に語らない。
- `最終判断` は `Fail / Revise / Keep / Design Ready` の4値だけを使う。
- 変換案が必要な場合は、必ず `workflows/transformation-workflow.md` に接続する。
- 制作実装を語る場合は、必ず `workflows/production-pipeline-workflow.md` と整合させる。
- `Design Ready` 後の一式化を語る場合は、必ず `workflows/brand-startup-set-workflow.md` と整合させる。
- 品質管理を語る場合は、必ず `workflows/quality-control-workflow.md` と整合させる。
- 現行市場について述べる場合は、観測日を明示する。
- 作業後の学習や再発論点がある場合は、`workflows/continuous-improvement-workflow.md` に接続する。
