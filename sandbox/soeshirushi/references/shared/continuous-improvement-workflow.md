# 継続改善ワークフロー

このファイルは、作業結果を
`監査 → 改善 → 記録 → 次観測点設定 → push`
まで閉じる標準手順を定義する。

## 起動条件
- ブランド探索、評価、設計の区切りがついた。
- 創出ブランドや生成絵文字を監査した。
- rough review、handoff review、final QA を行った。
- 審査差し戻し、公開後 drift、metadata 事故が出た。
- 市場調査つきアイデア探索を行った。
- skill、workflow、template、台帳の運用が重い、曖昧、再発的に詰まると判明した。

## 使う正本
- 判断基準: `rules/continuous-improvement-rules.md`
- 市場探索を含む場合: `rules/idea-research-rules.md`, `workflows/idea-research-workflow.md`
- 品質起点の場合: `workflows/quality-control-workflow.md`
- 文書 / skill 改修を含む場合: `workflows/framework-maintenance.md`
- brand 側記録: `templates/quality-ledger-template.md`, `templates/release-log-template.md`
- factory 側記録: `templates/factory-improvement-ledger-template.md`

## 標準手順
1. 起点になった `Observation` を 1 文で書く。
2. 監査単位を `brand / release / emoji / factory / skill` から決める。
3. 問題または学習を、必ず `構造 → ブランド → 商品` の順で見直す。
4. 構造で `Fail` が見えたら、そのまま改善に入らず `workflows/transformation-workflow.md` へ戻す。
5. `brand local / factory common / skill maintenance / monitor only` のどれかへ分類する。
6. 記録先を決める。
   - brand / release / emoji 起点: `quality-ledger`。提出や審査が絡むなら `release-log` も更新する。
   - factory / skill 起点: repo root の `factory-improvement-ledger.md` を更新する。未作成なら `templates/factory-improvement-ledger-template.md` から初期化する。
   - 両方に跨る場合: 両方を更新し、片方だけで閉じない。
7. 対応を `直す / 試す / 監視する / 捨てる` のどれで扱うか決める。
8. skill の不足が原因なら、既存 skill 改修で足りるかを先に見る。足りなければ `skills/line-emoji-skill-builder/SKILL.md` に接続する。
9. 次に効き目を見る地点を決める。
   - 次 release
   - 次ブランド探索
   - 次の rough review
   - 次の doc audit
10. 軽量化チェックを行う。
   - 台帳が active 論点より履歴で重くなっていないか。
   - 同じ論点が `quality-ledger`, `factory-improvement-ledger`, skill 本文に重複していないか。
   - skill が責務を持ちすぎていないか。
   - workflow が一時的事情を恒久手順にしていないか。
11. 重いと判定した場合は、その場で `削る / 要約する / owner file へ寄せる / skill を統合する / section を畳む` のどれかを行う。
12. 作業終了前に、変更した owner file、記録、依存ファイルを揃える。
13. `git status` を確認し、意図した差分だけを commit する。
14. remote へ push して閉じる。

## factory へ昇格しやすいパターン
- 同じ QA 事故が複数 brand / release で再発した。
- market research の偏りで毎回似た案が出る。
- 同じ skill 補足説明を毎回口頭で付け足している。
- 台帳や workflow が重すぎて、改善自体が滞る。

## 出力原則
- すべての改善ループで `起点 / スコープ / 直す owner file / 次観測点 / push 状態` を明示する。
- 学習の量より、次回判断に効く密度を優先する。
