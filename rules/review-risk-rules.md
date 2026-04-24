# 審査・権利・公開運用リスクルール

このファイルは、審査・権利・公開運用リスクだけを扱う。
視認性やセット重複のような商品品質項目は扱わない。

## 境界
- `視認性`, `重複`, `セット整合性` は主担当を `rules/emoji-product-rules.md` に置く。
- ただし、公式審査で却下要因になる水準まで悪い場合は、このファイルでも `Fail` または `Revise` の根拠になる。

## Hard NG
- `rules/line-platform-baseline.md` の必須仕様に反する。
- 必須画像、必須個数、画像形式、容量、透過要件、アニメーション制約を満たさない。
- 他者IPへの依存が強い。
- ファンアート前提で成立している。
- 固定IPとして扱うのに、権利の所在や素材の出自が説明できない。
- 著名人、写真、商標、ロゴの利用に権利上の問題がある。
- 政治的扇動、宗教勧誘、差別、憎悪表現を含む。
- 露骨な性的要素、過度なグロ表現を含む。
- 自傷、薬物、賭博などの誘導性が強い。

## Revise
- タイトル、説明文、コピーライトの文字数や文字種が公式仕様に合っていない。
- メタデータに絵文字、URL、告知文言、機種依存文字が入っている。
- 絵文字画像とタイトル、説明文、タブ画像の整合性が弱い。
- タイトルや説明文が内容とずれている。
- 広告的、販促的な文言が不自然に強い。
- URLや外部誘導を含む。
- 他社サービスや他メッセンジャー連想が強すぎる。
- 文化・宗教モチーフに誤読リスクがあり、安全側修正が必要。
- 固定IPバイブル、metadata、画像の見え方がずれている。

## Watch
- 地域差や文化差で解釈がぶれやすい。
- 一部差し替えでセット整合性に影響が出る。
- 固定IPの可変域が広く、次 release で別IP化するおそれがある。
- 将来的な公開範囲拡大時に再チェックが必要。

## 評価モデルへの接続
- `Hard NG` は即 `Fail`。
- `Revise` は修正完了まで少なくとも `Revise` 扱い。
- `Watch` は `templates/brand-setting-template.md`, `templates/brand-production-brief-template.md`, `templates/release-spec-template.md`, `templates/production-handoff-template.md`, `templates/quality-ledger-template.md`, `templates/brand-system-prompt-template.md` に引き継ぐ。
- 固定IPに関わる `Watch` は `templates/fixed-ip-bible-template.md` と `templates/sales-package-manifest-template.md` にも引き継ぐ。
