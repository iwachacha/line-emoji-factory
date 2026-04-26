# 市場調査つきアイデア探索ワークフロー

このファイルは、LINE絵文字 / スタンプの新しいブランド案や item 案を、
市場観測つきで多様に出しつつ偏りを抑える標準手順を定義する。

## 起動条件
- 新しいブランド案や item 案が必要。
- 直近の探索が似たテーマや温度感に寄っている。
- 市場の混雑と空白を見ながら探索したい。
- 安定枠だけでなく、尖った候補も混ぜて比較したい。

## 使う正本
- 相談入口: `workflows/consultation-workflow.md`
- 探索の判断基準: `rules/idea-research-rules.md`
- 構造の判定: `rules/structure-constraints.md`
- ブランド / 商品の確認: `rules/brand-creation-rules.md`, `rules/emoji-product-rules.md`, `rules/sticker-product-rules.md`
- 記録枠: `templates/market/idea-batch-template.md`
- 継続改善: `workflows/continuous-improvement-workflow.md`

## 標準手順
1. 相談の制約を確認する。
   - 対象ユーザー
   - テーマ制約
   - 季節性
   - 既存ブランドとの衝突有無
2. 直近の探索履歴や `factory-improvement-ledger.md` を見て、寄りやすい軸を洗い出す。
3. 現行市場を観測する。
   - 観測日を残す。
   - 何を見たかを残す。
   - `混みやすい表現 / 空白 / 真似しない線引き` を分けて書く。
4. 今回の回転軸を決める。
   - テーマ
   - 構造分類
   - ブランド主型
   - 温度感
   - 実用品寄り / 感情寄り
   - 安定枠 / 尖り枠
5. 原則 6〜12 件の候補を出す。
   - 高頻度・安定寄り
   - 実用品・機能寄り
   - 季節 / 文化寄り
   - ニッチ / 尖り寄り
   を混ぜる。ただし依頼が狭い場合はその範囲内で散らす。
6. 各候補に `一言定義 / 想定使用場面 / 視覚記号 / 候補構造分類 / 主なリスク` を付ける。
7. `rules/structure-constraints.md` で予備判定を行い、明確な `Fail` は切る。
8. 核が残る `Fail` は `workflows/transformation-workflow.md` へ送る。
9. 残った候補だけを、軽く `ブランド / 商品` の順で見る。
10. `templates/market/idea-batch-template.md` に、
    `市場観測 / 回転軸 / 候補群 / 昇格候補 / 次回の偏り対策`
    を残す。
11. 探索の癖や運用上の詰まりが見えたら `workflows/continuous-improvement-workflow.md` を起動する。

## 偏り対策
- 直近 2 batch が同系統なら、今回は意図的に外した候補を入れる。
- 毎回かわいい寄りに流れるなら、低装飾・低温度の候補を混ぜる。
- 毎回実用寄りに流れるなら、記号性や尖りを持つ候補を混ぜる。
- 尖り枠は残してよいが、構造や商品転換の筋がない案は温存しない。

## 出力原則
- 市場調査は雰囲気共有ではなく、判断材料として要約する。
- アイデア出しは量で終わらせず、比較可能な候補群へ整える。
- 「今売れていそう」だけでは通さず、ブランドとして育つ筋を確認する。
