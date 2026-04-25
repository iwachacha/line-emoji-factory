# release-001 振り返り

この振り返りは、`release-001` の design milestone を
次回判断に効く最小単位へ圧縮したもの。

## 1. Meta
- ブランド名: `そえしるし`
- release: `release-001`
- milestone: `design`
- 日付: `2026-04-24`
- 参照した evidence: `releases/release-001/release-spec.md`, `releases/release-001/production-handoff.md`, `releases/release-001/qa/quality-ledger.md`, `releases/release-001/qa/usage-validation.md`, `releases/release-001/release-log.md`

## 2. What Held
- 効いた判断: `文字補助絵文字` という広い親テーマから、`記号型・実用品寄り` の1ブランドへ絞ったこと
- 維持する条件: `1機能=1外形`, 主力14枠 + 補助2枠, 左右ペアの少数運用

## 3. What Broke
- 外した判断: 設計だけで `共有 / メモ / おすすめ` の勝ち筋が十分見えると考えたこと
- 壊れたレイヤー: `商品`
- 次の修正先: `releases/release-001/qa/usage-validation.md`, `releases/release-001/release-spec.md`, `releases/release-001/production-handoff.md`

## 4. What Fooled Us
- 誤誘導した前提: `実用そうに見える` だけで、具体会話での買う理由まで立つと思っていた
- 見落としていた証拠: `句読点 / 既存記号` で十分なシーンと、`左右ペア` の片割れ感を早い段階で比較していなかった

## 5. Brand / Release Changes
- brand 側で直すこと: 市場観測サマリーとホワイトスペースを明文化し、仕事寄りへの偏りを監視する
- release 側で直すこと: `S05 / S06`, `S08 / S16`, `S09 / S10`, `S14 / S15` を優先監査対象として固定する

## 6. Factory Feedback
- 共通基盤へ返すこと: 具体会話検証と release retrospective を factory workflow / template / scaffold に組み込むこと
- 返す根拠: soeshirushi では quality ledger だけでは `どの会話で負けるか` と `どの学習を残すか` が薄く、実会話検証と振り返り圧縮が必要だった

## 7. Delete / Compress
- もう追わない論点: 現時点ではなし
- 要約してよい記録: usage validation の派生文例は増やさず、decisive な 6 シーンだけ残す
- 重くなった artifact: まだなし

## 8. Next Experiment
- 次に試すこと: rough board で `S05/S06`, `S08/S16`, `S09/S10`, `S14/S15` を白黒比較と単体送信比較で再検証する
- 次に確認する release / milestone: `release-001 / rough`
