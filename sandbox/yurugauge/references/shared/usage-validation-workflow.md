# 具体会話検証ワークフロー

このファイルは、ブランド案や生成絵文字が
実際の会話文脈で本当に機能するかを検証する標準手順を定義する。

## 起動条件
- `release-spec` ができた。
- rough board や handoff ができた。
- 生成絵文字や final asset を監査したい。
- `買う理由` や `日常接続性` が設計上は見えるが、実例でまだ弱い。

## 使う正本
- ブランド核: `templates/brand-setting-template.md`
- release 設計: `templates/release-spec-template.md`
- handoff 条件: `templates/production-handoff-template.md`
- 品質管理: `workflows/quality-control-workflow.md`
- 出力枠: `templates/usage-validation-template.md`
- 継続改善: `workflows/continuous-improvement-workflow.md`

## 標準手順
1. 対象 release と対象絵文字を決める。
2. 6〜12 個の decisive な会話シーンを選ぶ。
   - 単体送信
   - 文中使用
   - 2個連続または左右ペア
   - 仕事寄り
   - 日常寄り
   - 少し尖った文脈
   を最低限混ぜる。
3. 各シーンで、
   - 何を伝えたいか
   - どの絵文字を置くか
   - 代替される既存表現は何か
   - 絵文字を使う意味が本当にあるか
   を書く。
4. 実際の読まれ方を `Pass / Revise / Cut / Monitor` で判定する。
5. `Revise` と `Cut` は、どこで壊れたかを `構造 / ブランド / 商品` の順に切り分ける。
6. 反復する失敗パターンをまとめる。
7. `release-spec`, `production-handoff`, `quality-ledger` のどれを直すか決める。
8. 同種の負け筋が再発するなら `workflows/continuous-improvement-workflow.md` に戻す。
9. シートが重くなったら、決定を変えたケースだけ残して圧縮する。

## 判定の目安
- `Pass`
  - 絵文字を置く意味が明確で、代替表現より読ませ方に利点がある。
- `Revise`
  - 意味はあるが、近い絵文字や既存表現に負ける。
- `Cut`
  - 実例で使い所が乏しく、商品枠を使う理由が弱い。
- `Monitor`
  - 現時点では保留。rough や final で再判定する。

## 軽量原則
- 具体会話は、生ログではなく decisive な短文だけ残す。
- 同じ失敗を説明する似たシーンは 1 件へまとめる。
- brand 固有で閉じるケースを factory 台帳へ大量転記しない。
