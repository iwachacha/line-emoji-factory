# factory 改善台帳

このファイルは、factory 共通で再利用したい学習だけを残す。
重くなったら、その重さ自体を改善対象に含める。

## 1. Intake
- ID: `FAC-2026-04-24-001`
- Date: `2026-04-24`
- Trigger: 自己改善ループ、軽量運用、市場調査つき探索、skill 育成の正本が不足していた
- Scope candidate: `factory common`
- Observation: brand 改善や QA はあっても、factory 全体を継続改善し、重くなりすぎた仕組みを自分で削る導線が薄かった
- Affected layer: `品質 / 市場探索 / skill / 文書`
- Evidence: `workflows/quality-control-workflow.md`, `skills/line-emoji-improvement-auditor/SKILL.md`, `PROJECT_MAP.md` だけでは、作業後の学習閉路と軽量化判断が分散していた
- Candidate owner file: `rules/continuous-improvement-rules.md`, `workflows/continuous-improvement-workflow.md`, `skills/line-emoji-factory-evolver/SKILL.md`
- Next audit point: 次回の探索相談、次回の改善監査、次回の doc audit
- ID: `FAC-2026-04-24-002`
- Date: `2026-04-24`
- Trigger: `そえしるし` を見ると、設計は通っていても `具体会話で本当に勝つか` と `milestone ごとの圧縮学習` を残す部品が弱かった
- Scope candidate: `factory common`
- Observation: quality ledger だけでは `どの会話で句読点に負けるか` と `何を削って軽く保つか` が薄く、brand 実例から基盤不足が見えた
- Affected layer: `商品 / 品質 / 運用`
- Evidence: `sandbox/soeshirushi/qa/quality-ledger.md`, `sandbox/soeshirushi/emoji-sets/releases/release-001.md`, `sandbox/soeshirushi/production/handoffs/release-001-handoff.md`
- Candidate owner file: `workflows/usage-validation-workflow.md`, `templates/usage-validation-template.md`, `workflows/release-retrospective-workflow.md`, `templates/release-retrospective-template.md`
- Next audit point: `release-001` rough 後
- ID: `FAC-2026-04-25-003`
- Date: `2026-04-25`
- Trigger: `ゆるゲージ` の市場調査から brand repo を立てる過程で、採用時の市場観測 snapshot の置き場が scaffold に無かった
- Scope candidate: `factory common`
- Observation: `idea-batch-template` は存在するが、brand repo 初期化時に `references/market/idea-batch-001.md` が作られないため、市場観測が brand-setting に詰め込まれやすい
- Affected layer: `市場探索 / 運用 / scaffold`
- Evidence: `sandbox/soeshirushi/brand/brand-setting.md` には市場観測サマリーがあるが独立 batch がなく、`sandbox/yurugauge/references/market/idea-batch-001.md` は今回手動追加が必要だった
- Candidate owner file: `templates/brand-repo-blueprint.md`, `templates/brand-repo-readme-template.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1`
- Next audit point: 次回 `scripts/init-brand-repo.ps1` で作る brand repo
- ID: `FAC-2026-04-25-004`
- Date: `2026-04-25`
- Trigger: `ゆるゲージ` で販売用PNGとZIPを実作成したところ、最終assetの仕様検査結果を残す共通枠が薄かった
- Scope candidate: `monitor only`
- Observation: release checklist だけでは、個別PNGのサイズ、透過、容量、ZIP内容、縮小preview、metadata version を後から確認しづらい
- Affected layer: `品質 / 制作パイプライン / 運用`
- Evidence: `sandbox/yurugauge/production/finals/release-001/asset-manifest.md`, `sandbox/yurugauge/production/finals/release-001-small-preview.png`
- Candidate owner file: `templates/finals-readme-template.md`, 将来的には final asset manifest template
- Next audit point: 次に actual PNG / ZIP まで作る release

## 2. Active Interventions
- ID: `FAC-2026-04-24-001`
- Hypothesis: 継続改善と軽量化を owner file と入口 skill に明示すれば、brand 修正で閉じる問題と factory 改善を切り分けながら再利用できる
- Intervention: rule / workflow / template / skill / scaffold に自己改善ループと軽量運用を組み込む
- Updated owner file: 正本 / skill / scaffold へ反映済み。次回運用で実効性を観測する段階
- Verification method: 次回の探索・監査で `起点 / スコープ / 次観測点 / push 状態` まで一貫して出せるかを見る
- Verify on: 次回運用時
- ID: `FAC-2026-04-24-002`
- Hypothesis: 具体会話検証と節目振り返りを共通基盤化すれば、`買う理由` の弱さと学習の散逸を早期に検知できる
- Intervention: usage validation / release retrospective の workflow と template を追加し、brand repo scaffold と `そえしるし` 実例へ反映する
- Updated owner file: workflow / template / scaffold / `そえしるし` 実例へ反映済み。rough 以降で実効性を観測する段階
- Verification method: `そえしるし` rough 以降で、使用検証と retrospective が実際の修正判断を動かすかを見る
- Verify on: `release-001 / rough`
- ID: `FAC-2026-04-25-003`
- Hypothesis: 採用時の市場観測を brand repo の `references/market/` に初期化すれば、ブランド設定に市場調査を詰め込みすぎず、採用理由と真似しない線引きを後から監査できる
- Intervention: brand repo blueprint / README template / manifest template / init script に `references/market/idea-batch-001.md` を追加する
- Updated owner file: `templates/brand-repo-blueprint.md`, `templates/brand-repo-readme-template.md`, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1`
- Verification method: 次回の brand repo 初期化で market snapshot が自動生成され、brand-setting が過重にならないかを見る
- Verify on: 次回 `scripts/init-brand-repo.ps1` 実行時
- ID: `FAC-2026-04-25-004`
- Hypothesis: final asset manifest を標準成果物として扱えば、完成PNGの公式仕様、縮小可読性、ZIP内容を release checklist より軽い粒度で監査できる
- Intervention: まず `templates/finals-readme-template.md` に manifest の必要性だけを追記し、template 新設は次の actual asset release まで保留する
- Updated owner file: `templates/finals-readme-template.md`
- Verification method: 次に actual PNG / ZIP を作る release で、manifest が提出前判断を動かすかを見る
- Verify on: 次回 final asset QA

## 3. Verified Upgrades

## 4. Skill Evolution

## 5. Market / Diversity Memory
- `2026-04-25 / ゆるゲージ`: 公式・クリエイターズの上位はIP、アニメーション、敬語テキスト、ふきだし、下線・ペン風、シンプルキャラが強い。敬語テキストへ直進すると混雑するため、`状態共有 / 進捗ゲージ` のように用途は近く、視覚文法は別にする方向が有効だった。

## 6. Lightweight Maintenance
- Heavy artifact:
- Why it became heavy:
- Compress / archive / merge / retire:
- Owner file:
- Next review date:

## 7. Deferred / Rejected
