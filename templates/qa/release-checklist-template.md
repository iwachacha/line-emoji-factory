# [RELEASE_ID] リリースチェックリスト テンプレート

このテンプレートは、提出前と公開後の最低確認項目の正本である。
blocking 問題を通さないために使う。

## Gate 0: 設計前提
- [ ] `brand-setting` が最新である
- [ ] `brand-canon` が最新である
- [ ] `brand-product-catalog` が存在し、過去商品との差分を参照できる
- [ ] `brand-production-brief` が最新である
- [ ] 新シリーズの場合、`series-plan` が存在する
- [ ] `release-spec` が存在する
- [ ] release の一言コンセプトとブランド内での役割が定義されている
- [ ] 初期セット個数の根拠が定義されている
- [ ] `production-handoff` が存在する
- [ ] `Watch` 項目が quality ledger に残っている

## Gate 1: 構造 / ブランド / 商品
- [ ] 構造後退がない
- [ ] ブランド核と視覚記号が揺れていない
- [ ] brand canon / IP guardrails を壊していない
- [ ] 過去シリーズと似すぎていない
- [ ] 逆にブランド/IPを壊すほど逸脱していない
- [ ] 継承要素と新規性要素が明確である
- [ ] 高頻度アイテムが上段に配置されている
- [ ] 差分軸が明確で、実質重複がない
- [ ] 組み合わせ補助枠を入れる場合、数と役割が過剰でない
- [ ] 単体送信でも文中使用でも死んでいない

## Gate 2: rough / handoff
- [ ] style anchor がある
- [ ] character / motif anchor がある
- [ ] rough board が set 全体の方向を説明できる
- [ ] handoff に keep / trim / drift が書かれている
- [ ] 各アイテムに用途と意味がある
- [ ] 生成後に優先監査するアイテムが決まっている
- [ ] item finalization に暗黙前提を押し込んでいない

## Gate 2.8: item finalization
- [ ] 1アイテムごとに item image prompt がある
- [ ] 1アイテムにつき最低4案を比較した
- [ ] final prompt と negative prompt が残っている
- [ ] 背景透過、太いアウトライン、少ない余白、少ない装飾が指定されている
- [ ] 小表示で残す視覚記号が item ごとに定義されている
- [ ] 候補比較で `かわいいが使えない` を落とした

## Gate 2.5: 具体会話検証
- [ ] usage validation シートがある
- [ ] 単体送信 / 文中使用 / 2個連続または左右ペアを検証した
- [ ] 代替される既存表現より、選択 item type を使う意味が残っている
- [ ] 負け筋を quality ledger へ反映した

## Gate 3: 完成データ
- [ ] 公式サイズ、形式、透過、容量制約を満たす
- [ ] `tools/validate-assets.py` が blocking 違反を出していない
- [ ] `180px / 96px / 48px / 32px` の contact sheet を確認した
- [ ] chat preview を確認した
- [ ] 小表示で主要要素が潰れない
- [ ] アニメーション使用時は 1 フレーム目で意味が読める
- [ ] 似た差分や色違い水増しがない
- [ ] 用途被りがない
- [ ] 余白過多、低コントラスト、背景混入、装飾過多がない
- [ ] タブ画像とセット本体が整合している

## Gate 4: metadata / review
- [ ] `tools/validate-metadata.py` が blocking 違反を出していない
- [ ] タイトル、説明文、コピーライトが仕様に収まる
- [ ] metadata と item 内容が一致している
- [ ] Hard NG リスクがない
- [ ] Revise 項目を放置していない

## Gate 5: 記録
- [ ] quality ledger を更新した
- [ ] product catalog を更新した
- [ ] series plan の結果欄を更新した
- [ ] release log を更新した
- [ ] 次 release へ持ち越す `Watch` 項目を明記した
- [ ] factory へ戻すべき再発問題を判定した
- [ ] 台帳や checklist が重くなりすぎていない
- [ ] milestone が変わるなら retrospective を更新した
