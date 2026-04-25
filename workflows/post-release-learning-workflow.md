# 公開後学習ワークフロー

このファイルは、公開後の売れ方、審査結果、運用 drift を次 release と factory 改善へ戻す標準手順を定義する。

## 起動条件
- release が公開された。
- 審査差し戻しが発生した。
- 販売、クリック、購入、レビューなどの実績が得られた。

## 使う正本
- 継続改善: `rules/continuous-improvement-rules.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 出力: `templates/post-release/post-release-metrics-template.md`, `templates/post-release/next-release-recommendation-template.md`
- schema: `schemas/post-release-metrics.schema.json`

## 標準手順
1. 公開日、審査結果、差し戻し理由、販売指標を記録する。
2. 売れた理由 / 売れなかった理由を、構造、ブランド、商品に分ける。
3. 次 release に増やす枠、減らす枠、廃止する枠を決める。
4. factory common へ戻すべき学習だけを `factory-improvement-ledger.md` へ送る。
5. 単発ノイズは monitor only にする。

## 完了条件
- next release recommendation が出ている。
- factory へ戻す学習と brand local で閉じる学習が分かれている。
