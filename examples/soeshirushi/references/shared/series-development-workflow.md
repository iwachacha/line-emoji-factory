# シリーズ開発ワークフロー

このファイルは、既存ブランドから新シリーズを作るときの標準手順を定義する。
単発商品ではなく、ブランド資産として継続展開するために使う。

## 起動条件
- 既存ブランドで次 release / 新シリーズを企画する。
- 過去商品との差分、継承要素、カニバリゼーションを確認したい。
- ブランド/IP の核を守りながら新鮮さを出したい。

## 使う正本
- brand canon: `templates/brand/brand-canon-template.md`
- brand product catalog: `templates/brand/brand-product-catalog-template.md`
- series plan: `templates/release/series-plan-template.md`
- release spec: `templates/release/release-spec-template.md`
- 制作パイプライン: `workflows/production-pipeline-workflow.md`
- 品質管理: `workflows/quality-control-workflow.md`

## 標準手順
1. `brand-setting` と `brand-canon` を読み、守る核と禁止 drift を確認する。
2. `brand/product-catalog.md` を読み、過去シリーズのテーマ、感情レンジ、主要モチーフ、差分軸、避けるべき重複を確認する。
3. 新シリーズの目的を、使用場面、主感情レンジ、商品テーマ、コアモチーフで定義する。
4. 過去商品から継承する要素と、今回だけの新規性要素を分ける。
5. 既存シリーズとの重複リスクとカニバリゼーション回避を記録する。
6. ブランドらしさを壊す逸脱がないか、`構造 → ブランド → 商品` の順で確認する。
7. `series-plan.md` を作り、release spec の初版へ接続する。
8. rough / anchor 生成へ進める前に、必ず series plan の差分軸を handoff へ渡せる粒度にする。
9. release 完了後、catalog に結果、成功した差分軸、避けるべき重複、次シリーズへの拡張余地を戻す。

## 必須チェック
- このシリーズはブランドらしいか。
- 過去シリーズと似すぎていないか。
- ブランド/IPを壊すほど逸脱していないか。
- どの要素を継承し、どの要素で新鮮さを出すのかが明確か。
- 商品として使い分けできるか。
- 既存商品を食い合わないか。
- LINE上で実用性があるか。
- 見た目だけでなく会話で使いたくなるか。

## 差し戻し
- ブランド/IP の核が崩れる場合: brand canon を更新するか企画を戻す。
- 過去商品との差分が弱い場合: series plan を戻す。
- 商品用途が弱い場合: release spec と usage validation を戻す。
- 見た目だけで使い道が薄い場合: item spec 作成前に止める。

## 完了条件
- series plan が埋まっている。
- release spec に series plan の継承要素、新規性、重複回避が反映されている。
- final QA 後に brand product catalog が更新されている。
- 次シリーズで参照できる `継承すべき要素 / 避けるべき重複 / 拡張余地` が残っている。
