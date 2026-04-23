# 品質台帳

`そえしるし` の継続品質論点をここに集約する。
初期段階なので、現時点では `Watch` 中心で管理する。

## 1. Open Issues
- ID: `SOE-Q-001`
  - 初出 release: `release-001`
  - 症状: `みて左 / みて右` が単体送信で片割れに見える可能性がある
  - 影響レイヤー: `商品`
  - 根本原因: ペア使用の印象が強いと、単体意味が弱くなる
  - 直す owner file: `brand/brand-production-brief.md`, `production/handoffs/release-001-handoff.md`
  - 次アクション: rough board で単体表示とペア表示を必ず並置検証する
- ID: `SOE-Q-002`
  - 初出 release: `release-001`
  - 症状: `補足` と `結論` の差が弱くなる可能性がある
  - 影響レイヤー: `商品`
  - 根本原因: どちらも文章整理系で、外形が近づきやすい
  - 直す owner file: `emoji-sets/releases/release-001.md`, `production/handoffs/release-001-handoff.md`
  - 次アクション: 中央サインと外形の閉じ方向を逆に固定する
- ID: `SOE-Q-003`
  - 初出 release: `release-001`
  - 症状: 実用寄りに振れすぎると日常接続性が弱く見える可能性がある
  - 影響レイヤー: `ブランド`
  - 根本原因: 仕事連絡文脈を基準に置きすぎると温度感が硬くなる
  - 直す owner file: `brand/brand-setting.md`, `emoji-sets/releases/release-001.md`
  - 次アクション: サンプル使用場面に友人同士の軽い会話も含める
- ID: `SOE-Q-004`
  - 初出 release: `release-001`
  - 症状: `確認 / 要返信 / 了解` が近づくと、依頼と応答の向きが曖昧になる
  - 影響レイヤー: `商品`
  - 根本原因: 近い実用品機能を増やしたため、中央サイン設計が弱いと混同しやすい
  - 直す owner file: `emoji-sets/releases/release-001.md`, `production/handoffs/release-001-handoff.md`
  - 次アクション: 戻す / 返す / 収める の向き差を rough board で並置比較する

## 2. Monitoring
- ID: `SOE-M-001`
  - 監視理由: 色に頼った差分になると小表示で機能差が落ちる
  - 再発条件: モノクロで見分けがつかない絵文字が2個以上出る
  - 次に確認する release: `release-001`
- ID: `SOE-M-002`
  - 監視理由: 上段4個の頻度想定が実使用とずれる可能性がある
  - 再発条件: rough review 時点で `補足` や `締切` の方が汎用に見える
  - 次に確認する release: `release-001`
- ID: `SOE-M-003`
  - 監視理由: 組み合わせ補助枠の存在感が強すぎると、主力枠より演出感が前に出る
  - 再発条件: rough board で `みて左 / みて右` が上段主力より強く見える
  - 次に確認する release: `release-001`

## 3. Closed Issues
- ID: `SOE-C-001`
  - 何を直したか: brand repo の shared snapshot 不足を factory 側で補った
  - 更新した owner file: `workflows/brand-lifecycle-workflow.md`, `templates/brand-repo-blueprint.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1`
  - いつ閉じたか: `2026-04-23`
- ID: `SOE-C-002`
  - 何を直したか: 初期 release を `8` から `16` へ拡張し、release 固有コンセプトと主力 / 補助枠を定義した
  - 更新した owner file: `brand/brand-production-brief.md`, `emoji-sets/releases/release-001.md`, `production/handoffs/release-001-handoff.md`
  - いつ閉じたか: `2026-04-23`

## 4. Recurring Drift
- 繰り返し起きる drift: まだなし
- rough stage 由来か: 未判定
- handoff 由来か: 未判定
- final QA 由来か: 未判定
- metadata / review 由来か: 未判定

## 5. Factory Feedback
- 工場本体へ戻すべき問題: 現時点では追加なし
- `workflows/production-pipeline-workflow.md` 更新候補: なし
- `templates/brand-production-brief-template.md` 更新候補: なし
- `templates/production-handoff-template.md` 更新候補: なし
- `scripts/init-brand-repo.ps1` 更新候補: shared snapshot 追加は反映済み
