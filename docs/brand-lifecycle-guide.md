# Brand Lifecycle Guide

## Stay in Factory
- 案の比較や市場探索が中心。
- brand核がまだ `Revise`。
- 商品としての初回 release が見えない。

## Split to Brand Repo
- `Design Ready` で、制作とQAをブランド単位で持つ必要がある。
- brand canon、product catalog、series plan、release spec、production handoff、quality ledger を継続更新する。
- 固定IPや承認ログなど、ブランド固有の管理が必要。

## Operate After Split
- factory snapshot は自動追随させない。
- 新シリーズ作成時は product catalog を読み、継承要素と差分を series plan に固定する。
- 公式仕様更新、審査事故、再発品質問題が出た場合だけ snapshot を更新する。
- factory common へ戻す学習は `factory-improvement-ledger.md` に圧縮する。
