# release-001 リリースチェックリスト

このチェックリストは、`ことば整理コア16` の現在地を示す。
2026-04-23 時点では設計完了まで進み、rough / final は未着手。

## Gate 0: 設計前提
- [x] `brand-setting` が最新である
- [x] `brand-production-brief` が最新である
- [x] `release-spec` が存在する
- [x] release の一言コンセプトとブランド内での役割が定義されている
- [x] 初期セット個数の根拠が定義されている
- [x] `production-handoff` が存在する
- [x] `Watch` 項目が quality ledger に残っている

## Gate 1: 構造 / ブランド / 商品
- [x] 構造後退がない
- [x] ブランド核と視覚記号が揺れていない
- [x] 高頻度絵文字が上段に配置されている
- [x] 差分軸が明確で、実質重複がない
- [x] 組み合わせ補助枠を入れる場合、数と役割が過剰でない
- [x] 単体送信でも文中使用でも死んでいない前提で設計されている

## Gate 2: rough / handoff
- [x] rough board が set 全体の方向を説明できるメモがある
- [x] handoff に keep / trim / drift が書かれている
- [x] 各絵文字に用途と意味がある
- [x] 生成後に優先監査する絵文字が決まっている
- [x] item finalization に暗黙前提を押し込んでいない

## Gate 2.5: 具体会話検証
- [x] usage validation シートがある
- [x] 単体送信 / 文中使用 / 2個連続または左右ペアを検証した
- [x] 代替される既存表現より、絵文字を使う意味が残っているコア枠がある
- [x] 負け筋を quality ledger へ反映した

## Gate 3: 完成データ
- [ ] 公式サイズ、形式、透過、容量制約を満たす
- [ ] 小表示で主要要素が潰れない
- [ ] アニメーション使用時は 1 フレーム目で意味が読める
- [ ] 似た差分や色違い水増しがない
- [ ] タブ画像とセット本体が整合している

## Gate 4: metadata / review
- [ ] タイトル、説明文、コピーライトが仕様に収まる
- [ ] metadata と絵文字内容が一致している
- [x] Hard NG リスクがない設計になっている
- [ ] Revise 項目を放置していない

## Gate 5: 記録
- [x] quality ledger を更新した
- [x] release log を更新した
- [x] 次 release へ持ち越す `Watch` 項目を明記した
- [x] factory へ戻すべき再発問題を判定した
- [x] 台帳や checklist が重くなりすぎていない
- [x] milestone が変わるなら retrospective を更新した
