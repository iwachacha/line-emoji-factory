# Item Generation Workflow

このファイルは、`GPT / image_gen` を使って LINE絵文字 / スタンプの個別アイテムを生成し、
final asset 候補へ進めるための標準手順を定義する。

## 境界
- この workflow は Stage 2 rough / anchor から Stage 3 item finalization までを扱う。
- 構造判断、ブランド採否、シリーズ企画を代替しない。
- final asset の採用可否は `workflows/quality-control-workflow.md` と `rules/visual-asset-quality-rules.md` で判断する。

## 必須入力
- brand canon
- brand production brief
- brand product catalog
- series plan
- release spec
- production handoff
- item image prompt
- unresolved `Watch`

## 標準手順
1. style anchor を作る。
   - 線幅、色、塊、余白、表情の強さ、装飾上限を確認する。
2. character / motif anchor を作る。
   - キャラクター、モチーフ、記号、デコ文字の核が小表示で残るか確認する。
3. rough board を作る。
   - set 全体の差分軸、上段高頻度枠、補助枠、過去商品との差分を一覧で確認する。
4. item spec を作る。
   - 1アイテムごとに用途、単体送信時の意味、文中使用時の意味、スタンプ送信時の発話を固定する。
5. 1アイテムにつき最低4案を生成する。
   - 4案は色違いだけにしない。表情、ポーズ、シルエット、記号配置の差を含める。
6. 候補比較を行う。
   - 視認性、即読性、差分明確性、ブランド一致、シリーズ差分、会話投入性で比較する。
7. 小サイズ視認性チェックを行う。
   - `180px / 96px / 48px / 32px` の contact sheet と chat preview を見る。
8. 差し戻しを分類する。
   - spec 不足、rough 不足、prompt 不足、候補品質不足、brand drift、series 重複に分ける。
9. final asset 候補を作る。
   - 透過、太線、余白、装飾上限、ファイル命名、tab/main との整合を確認する。
10. contact sheet / chat preview を保存する。
11. quality ledger に、採用理由、落とした理由、次回避ける drift を記録する。

## 候補比較の最低項目
- item ID
- candidate ID
- 用途への合致
- 小表示で残る要素
- 削れていない brand 固有要素
- series 固有要素
- 過去商品との差分ポイント
- 重複リスク
- 採用 / Revise / Hard NG
- 再生成指示

## Hard NG
- 透明背景ではない。
- 小表示で意味が読めない。
- 背景や小物が主情報を食う。
- 線が細い。
- 4案が実質同じ。
- 1アイテムの意味が説明できない。
- brand canon / IP guardrails を壊す。
- 過去商品とほぼ同じで、新シリーズとしての差分がない。

## 完了条件
- 各アイテムに item spec と候補比較がある。
- 採用候補は contact sheet / chat preview を通している。
- 差し戻し理由が分類され、再生成に使える形で残っている。
- final asset 候補が Product QA に渡せる。
