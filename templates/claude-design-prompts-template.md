# ClaudeDesign prompts

このファイルは、rough board と handoff をもとに、個別絵文字を完成形へ詰めるための prompt 束である。
ClaudeDesign は新しいブランド判断を作るのではなく、渡された条件を LINE絵文字として成立する形へ仕上げる。

## 参照する正本
- ブランド設定: `brand/brand-setting.md`
- 固定IPバイブル: `brand/fixed-ip-bible.md` がある場合のみ参照する
- ブランド制作基盤: `brand/brand-production-brief.md`
- release spec: `emoji-sets/releases/release-001.md`
- production handoff: `production/handoffs/release-001-handoff.md`
- usage validation: `qa/usage-validations/release-001.md`
- quality ledger: `qa/quality-ledger.md`

## Core Finish Prompt
以下の正本を優先して、`release-001` の LINE絵文字を完成形へ仕上げてください。

優先順は、`構造成立 → ブランド核 → 商品品質 → 審査安全性` です。
rough の雰囲気をそのまま清書するのではなく、1絵文字ごとの意味、視認性、差分明確性、セット整合性を完成させてください。

- 共通固定条件:
- ブランド可変域:
- release 固有条件:
- drift と判定する境界:
- 固定IPとして守る造形:
- 固定IPを持たない場合に守る視覚文法:
- 権利 / 出自で触れてはいけない表現:
- 余白方針:
- アウトライン方針:
- 装飾方針:
- 小表示で最優先する点:
- 未解決 `Watch`:

## Per-Emoji Finish Prompt
- ID:
- 用途:
- 単体送信時の意味:
- 文中使用時の意味:
- 連続使用メモ:
- 残す rough 要素:
- 仕上げ時に強める点:
- 仕上げ時に削る点:
- 変えてはいけない核:
- 固定IPとして守る造形:
- 固定IPを持たない場合に守る視覚文法:
- 注意する審査 / リスク:

仕上げ後、次を短く自己点検してください。
- 単体送信でも意味があるか。
- 文中使用で温度が強すぎないか。
- 近い絵文字と混ざらないか。
- ブランドの視覚記号が残っているか。
- 固定IPの造形と禁止 drift を守っているか。
- `Watch` 項目が悪化していないか。

## Handoff-Specific Prompts
handoff の `set 全体で守ること` と `個別絵文字仕様` を優先してください。
handoff にない要素を勝手に補ってブランド核を変えないでください。
必要な情報が足りない場合は、生成前に不足項目を列挙してください。

## Fix Prompts
### 視認性修正
- 主要要素を大きくし、細部を減らす。
- 線幅とコントラストを強める。
- 小表示で残す要素を1つに絞る。

### 差分明確性修正
- 色だけでなく、形、向き、表情、サインのいずれかで差分を作る。
- 近い用途の絵文字は、使用場面が分かれるように調整する。
- 微差分だけの候補は統合または差し替え候補にする。

### セット整合性修正
- 視覚記号、線、余白、温度感を揃える。
- 補助枠が主力枠より目立つ場合は弱める。
- rough stage 由来の drift は Stage 1 へ戻す候補として記録する。

### export-ready 前修正
- 公式サイズ、透過、容量、ファイル名、metadata 整合に関わる問題を優先して直す。
- fixed IP bible がある場合、それと矛盾する見え方は export-ready へ進めない。
- 修正後は `submissions/sales-package-manifest.md` に反映する。
