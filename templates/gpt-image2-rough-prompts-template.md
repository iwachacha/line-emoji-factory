# GPT-image2 rough prompts

このファイルは、`GPT-image2.0` で rough board や set overview を作るための prompt 束である。
完成品の正本ではなく、ClaudeDesign へ渡す前の視覚方向、差分軸、弱点発見に使う。

## 参照する正本
- ブランド設定: `brand/brand-setting.md`
- ブランド制作基盤: `brand/brand-production-brief.md`
- release spec: `emoji-sets/releases/release-001.md`
- handoff: `production/handoffs/release-001-handoff.md`
- brand system prompt: `brand/brand-system-prompt.md`

## Core Rough Prompt
次の条件で、LINE絵文字セットの rough board を作成してください。

- ブランド名: `[BRAND_NAME]`
- release: `release-001`
- 構造分類:
- ブランド主型:
- この release を買う理由:
- 共通固定条件:
- ブランド可変域:
- release 固有可変域:
- 視覚記号:
- 小サイズで守る要素:
- 差分の軸:
- 最上段に置く高頻度絵文字:
- 主力枠と補助枠の配分:

出力は、個別絵文字の候補を一覧で比較できる rough board にしてください。
各絵文字は独立した四角い枠の中で見せ、単体送信時の意味が分かるようにしてください。
全体図の雰囲気だけで成立させず、1画像単位の用途と差分が読めるようにしてください。

## Per-Emoji Rough Prompt
次の1件だけを rough として作成してください。

- ID:
- 用途:
- 単体送信時の意味:
- 文中使用時の役割:
- 連続使用メモ:
- 残すブランド要素:
- 削ってよい要素:
- drift と判定する境界:
- 小表示で最優先する点:

## Variant Rough Prompts
### 上段高頻度枠
- 高頻度用途を優先し、文末に添えても温度が強すぎない方向で作る。
- 装飾より即読性を優先する。
- 似た反応が並ぶ場合は、表情、形、向き、サインのどれで差分を読むかを明確にする。

### 補助枠
- 組み合わせ使用を想定してよいが、単体でも最低限の意味を残す。
- 上段高頻度枠より目立たせない。
- ペア前提、配置依存、片割れだけでは意味が死ぬ表現を避ける。

### 尖り枠
- ブランドの差別化は残す。
- ただし既存記号や句読点で十分な表現に落とさない。
- 小表示で用途が読めない抽象表現は避ける。

## Negative / Guardrails
- 任意文字列を囲む、下線を引く、背景帯を後付けする前提にしない。
- 全体図でしか意味が成立しない構図にしない。
- 色違い、微差分、装飾違いだけで個数を水増ししない。
- キャラクター化、ロゴ化、UIアイコン化、広告記号化へ寄せない。
- 文字や細部を詰め込みすぎない。
- 小表示で主要要素が潰れる線幅、余白、装飾密度にしない。

## Rough Review Memo
- 残す rough 要素:
- ClaudeDesign で削る要素:
- 構造再評価が必要な候補:
- usage validation で先に試す候補:
