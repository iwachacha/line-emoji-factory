# Regeneration Feedback Template

このテンプレートは、finalization 候補が `Revise` または `Hard NG` になったとき、
再生成に使う短い feedback を残すための正本である。

## Target
- release ID:
- item ID:
- candidate ID:
- asset path:
- decision: `Hard NG / Revise / Watch`

## Failure Category
- 構造:
- ブランド:
- 商品:
- 画像仕様:
- series 差分:
- IP / review:

## What Failed
- 小表示で読めなかった要素:
- 意味が弱かった点:
- 表情 / ポーズ差分の弱さ:
- 線 / 余白 / 装飾の問題:
- 背景 / 透過の問題:
- 過去商品との重複:
- brand canon / IP guardrails とのズレ:

## Keep
- 残す要素:
- 残す色:
- 残すポーズ:
- 残す表情:

## Change
- 大きくする要素:
- 削る要素:
- 太くする線:
- 変える表情 / ポーズ:
- 差分を強める方向:

## Feedback Prompt
```text
Regenerate only item <ITEM_ID>.
Keep: <残す要素>
Change: <変える要素>
Remove: <削る装飾>
Must satisfy: transparent background, bold outline, small-size readability at 96/48/32px, clear single-item meaning.
Avoid: <禁止 drift / 背景 / 細線 / 装飾過多 / 近似 item>
```

## Ledger Update
- quality ledger issue ID:
- release checklist blocking item:
- catalog に戻す学習:
