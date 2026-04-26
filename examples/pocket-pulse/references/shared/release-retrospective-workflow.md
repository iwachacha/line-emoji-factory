# リリース振り返りワークフロー

このファイルは、release の節目ごとに
`何が効いたか / 何が外れたか / 何を削るか / 何を factory へ返すか`
を短く圧縮する標準手順を定義する。

## 起動条件
- `Design Ready` で設計を固めた。
- series plan を確定した。
- rough review が一区切りついた。
- item finalization review が一区切りついた。
- final QA が終わった。
- 審査結果が返った。
- 公開後の drift や使用学習が溜まった。

## 使う正本
- 品質論点: `templates/qa/quality-ledger-template.md`
- 具体会話検証: `templates/qa/usage-validation-template.md`
- 履歴: `templates/release/release-log-template.md`
- catalog: `templates/brand/brand-product-catalog-template.md`
- 継続改善: `workflows/continuous-improvement-workflow.md`
- 出力枠: `templates/qa/release-retrospective-template.md`

## 標準手順
1. milestone を `design / series planning / rough / item finalization / final QA / review / public` から決める。
2. その節目で効いた判断と外した判断を 3 件以内でまとめる。
3. `何が自分たちを誤誘導したか` を 1〜3 件に絞る。
4. brand 固有で直すことと factory へ返すことを分ける。
5. `削る / 要約する / もう追わない` を明示する。
6. `release-log`, `quality-ledger`, `product-catalog`, 必要なら `factory-improvement-ledger` を更新する。
7. 旧 retrospective が増えすぎたら、最新判断に必要な差分だけ残して畳む。

## 出力原則
- 褒め感想ではなく、次回の判断を変える事実だけ残す。
- milestone ごとに 1 ファイルを原則にし、枝番を増やしすぎない。
- factory へ返す改善は、具体証拠と一緒に書く。
