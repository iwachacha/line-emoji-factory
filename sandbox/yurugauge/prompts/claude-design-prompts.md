# ゆるゲージ ClaudeDesign prompts

## Core Finish Prompt
`brand/brand-setting.md`, `brand/brand-production-brief.md`, `emoji-sets/releases/release-001.md`, and `production/handoffs/release-001-handoff.md` を優先して、各PNGをLINE絵文字として完成させる。最優先は `1文字ラベルの可読性`, `太い輪郭`, `ゲージ文法の統一`, `各状態の差分明確性`。ラフの雰囲気ではなく、1画像単位で意味が成立するかを基準に直す。

## Handoff-Specific Prompts
- `002 了`: 了承の返答。完了印に寄せない。
- `004 済`: 処理済み。了承ではなく完了。
- `015 決`: 決定事項。完了チェックではなく確定の丸印。
- `003 中`: 対応中。作業が進んでいる。
- `013 調`: 調整中。スライダーまたは調整サインで `中` と分ける。
- `005 確`: 確認依頼。`見` の確認済みと混ぜない。
- `006 返`: 返信依頼。圧を強めすぎない。

## Fix Prompts
- If a label is not legible at 64px preview, enlarge the label and remove the auxiliary sign before changing the brand grammar.
- If two emojis are confused, change the auxiliary sign and progress amount before changing color.
- If an emoji feels too business-only, soften corners and color saturation while keeping outline contrast.

