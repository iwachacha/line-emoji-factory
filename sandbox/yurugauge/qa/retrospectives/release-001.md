# release-001 振り返り

## 1. Meta
- ブランド名: `ゆるゲージ`
- release: `進捗と返事コア16`
- milestone: `final QA`
- 日付: `2026-04-25`
- 参照した evidence: `references/market/idea-batch-001.md`, `qa/usage-validations/release-001.md`, `production/finals/release-001/asset-manifest.md`

## 2. What Held
- 効いた判断: 敬語テキスト市場へ直接突っ込まず、状態ゲージへずらしたことで `差別化` と `日常接続性` が両立した。
- 維持する条件: `1状態=1文字ラベル=1ゲージ量`。便利語の追加で普通のテキスト絵文字に戻さない。

## 3. What Broke
- 外した判断: 初期 scaffold に市場調査 artifact の置き場がなく、brand setting へ市場観測を詰め込みやすかった。
- 壊れたレイヤー: `運用`
- 次の修正先: `templates/brand-repo-readme-template.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1`

## 4. What Fooled Us
- 誤誘導した前提: release checklist だけで final assets の仕様検査まで十分に閉じられるという前提。
- 見落としていた証拠: 実際にPNGとZIPを作ると、サイズ、透過、容量、縮小preview、zip内容の manifest が必要になる。

## 5. Brand / Release Changes
- brand 側で直すこと: `休` の使用価値を monitor。公開後に弱ければ release-002 で差し替え候補を検討。
- release 側で直すこと: final asset manifest を保存し、審査提出前に再検査する。

## 6. Factory Feedback
- 共通基盤へ返すこと:
  - brand repo scaffold に `references/market/idea-batch-001.md` を含める。
  - final asset manifest / PNG仕様検査を共通成果物として扱う。
- 返す根拠:
  - `そえしるし` では市場観測が brand setting 内に圧縮され、独立 artifact がない。
  - `ゆるゲージ` では販売用PNGを実作成した時点で、仕様検査とZIP内容の記録が必要になった。

## 7. Delete / Compress
- もう追わない論点: 敬語テキスト案 `C04`。市場混雑が強く、今回の差別化に寄与しない。
- 要約してよい記録: 具体会話の類似ケース。
- 重くなった artifact: usage validation は9ケースで止める。

## 8. Next Experiment
- 次に試すこと: 予定調整版、または感情温度版を別 batch で比較。
- 次に確認する release / milestone: `release-001 / review result`

