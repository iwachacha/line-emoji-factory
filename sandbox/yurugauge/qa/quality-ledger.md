# ゆるゲージ 品質台帳

## 1. Open Issues
- ID: `YG-QA-001`
  - 初出 release: `release-001`
  - 症状: `了 / 済 / 決` が近い意味に見える可能性がある
  - 影響レイヤー: `商品`
  - 根本原因: 了承、完了、決定が日本語会話で近接する
  - 直す owner file: `emoji-sets/releases/release-001.md`, `production/handoffs/release-001-handoff.md`, final PNG
  - factory昇格候補: `monitor only`
  - 次アクション: final preview で補助サインとバー量差を確認
- ID: `YG-QA-002`
  - 初出 release: `release-001`
  - 症状: 1文字ラベルが64px相当で読めない可能性
  - 影響レイヤー: `商品`
  - 根本原因: 絵文字内文字の可読性が品質を左右する設計
  - 直す owner file: final PNG, `production/handoffs/release-001-handoff.md`
  - factory昇格候補: `factory common`
  - 次アクション: PNG仕様検査と縮小previewを asset manifest に残す
- ID: `YG-QA-003`
  - 初出 release: `release-001`
  - 症状: `休` が進捗と返事の核から少し外れる
  - 影響レイヤー: `ブランド / 商品`
  - 根本原因: 日常温度を足す補助枠だが、状態共有の直線からは外れる
  - 直す owner file: `emoji-sets/releases/release-001.md`
  - factory昇格候補: `monitor only`
  - 次アクション: 初回では残し、公開後または次QAで使用価値を再判定

## 2. Monitoring
- ID: `YG-MON-001`
  - 監視理由: 仕事寄りに寄りすぎると日常接続性が落ちる
  - 再発条件: 具体会話検証で日常シーンが `Revise` 以下になる
  - 次に確認する release: `release-002`
- ID: `YG-MON-002`
  - 監視理由: ゲージ量が使用者に意味として伝わるかは公開後学習が必要
  - 再発条件: `中 / 調 / 待 / 後` の使い分けが曖昧になる
  - 次に確認する release: `release-001 final QA`

## 3. Closed Issues
- ID: `YG-CLOSED-001`
  - 何を直したか: 初期案の長い敬語テキストをやめ、1文字ラベル + ゲージ量に圧縮した
  - 更新した owner file: `brand/brand-setting.md`, `emoji-sets/releases/release-001.md`
  - いつ閉じたか: `2026-04-25`

## 4. Recurring Drift
- 繰り返し起きる drift: 便利語を増やしすぎて、普通の敬語テキスト絵文字へ戻る
- rough stage 由来か: あり。ラベル候補を増やすと起きる
- handoff 由来か: あり。用途説明が長いと長文ラベル化する
- final QA 由来か: 小表示対策で文字を増やすと逆効果
- metadata / review 由来か: 検索語を詰めすぎると内容とズレる

## 5. Factory Feedback
- 工場本体へ戻すべき問題:
  - brand repo scaffold に市場調査 artifact の置き場がない
  - final asset manifest / PNG仕様検査の共通出力枠がない
- `workflows/production-pipeline-workflow.md` 更新候補: final asset QA の成果物として `asset-manifest` を明示する
- `templates/brand-production-brief-template.md` 更新候補: 画像生成後の縮小preview / 容量検査項目を追加する
- `templates/production-handoff-template.md` 更新候補: final asset manifest へのリンク欄を追加する
- `skills/` 更新候補: まだ不要。1件の試走では skill 改修まで上げない
- `scripts/init-brand-repo.ps1` 更新候補: `references/market/idea-batch-001.md` を初期化する

## 6. Lightweight Maintenance
- 重くなった artifact: usage validation
- 要約 / 統合 / 昇格の候補: decisive 9ケースのみ維持し、類似会話は増やさない
- 次回まで残す最小論点: 混同3組、小表示可読性、`休` の適合

## 7. Linked Evidence
- usage validation: `qa/usage-validations/release-001.md`
- retrospective: `qa/retrospectives/release-001.md`

