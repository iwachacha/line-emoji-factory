# Item Image Prompt Template

このテンプレートは、1アイテムを final asset 候補へ進めるための `GPT / image_gen` 用プロンプト正本である。
1アイテムにつき最低4案を生成し、候補比較と小表示 QA を行う。

## 1. Item Identity
- item ID:
- release ID:
- series name:
- item type:
- candidate count: 4以上

## 2. Usage Meaning
- 用途:
- 単体送信時の意味:
- 文中使用時の意味:
- スタンプ送信時の発話:
- 連続使用時の役割:
- 代替されやすい既存表現:
- この item を残す理由:

## 3. Brand / Series Constraints
- ブランド固有要素:
- シリーズ固有要素:
- 過去商品との差分ポイント:
- 継承する視覚要素:
- 禁止 drift:
- 類似させない過去 item:

## 4. Visual Priority
- 残す視覚記号:
- 削る装飾:
- 主情報:
- 補助情報:
- 小表示で最初に読ませるもの:
- 太いアウトライン方針:
- 余白方針:
- 背景透過:

## 5. Final Prompt
```text
<ここに最終生成プロンプトを書く>

Requirements:
- Transparent background.
- Bold dark outline.
- Large readable silhouette.
- Minimal decoration.
- Clear expression or pose difference.
- Designed for LINE emoji / sticker small-size readability.
- Keep brand-specific and series-specific visual rules.
- Do not generate a whole set; generate this one item only.
```

## 6. Negative Prompt
```text
no background, no photo background, no thin lines, no tiny details, no clutter,
no many props, no excessive sparkles, no pale low-contrast art,
no complex scenery, no text overload, no duplicate pose,
no brand drift, no other IP resemblance
```

## 7. Candidate Comparison
- Candidate A:
  - 採用判断:
  - 強い点:
  - 弱い点:
  - 小表示で残るもの:
  - 修正指示:
- Candidate B:
- Candidate C:
- Candidate D:

## 8. Small-Size Check
- 180px:
- 96px:
- 48px:
- 32px:
- 透明背景:
- アウトライン:
- 余白:
- 装飾過多:
- 用途即読性:
- セット内差分:
- 過去商品との差分:

## 9. Final Decision
- Decision: `Hard NG / Revise / Watch / Keep`
- 採用候補:
- 差し戻し理由:
- 再生成する場合の feedback prompt:
- quality ledger に残すこと:
