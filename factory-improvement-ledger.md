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
- ID: `FAC-2026-04-25-001`
- Date: `2026-04-25`
- Trigger: ブランドごとに絵文字案や制作物を監査する SKILL を持たせたいが、毎回 1 から作ると品質が揺れる
- Scope candidate: `skill maintenance`
- Observation: ブランド別 auditor SKILL の共通骨格と、ブランド固有 anchor の抽出手順がなく、監査観点がブランドごとに分散する恐れがあった
- Affected layer: `品質 / skill / 文書`
- Evidence: `skills/line-emoji-skill-builder/SKILL.md`, `templates/quality-ledger-template.md`, `templates/brand-repo-blueprint.md` では、ブランド別 auditor SKILL を作る共通入口と出力骨格が未定義だった
- Candidate owner file: `skills/line-emoji-brand-audit-skill-builder/SKILL.md`, `templates/brand-audit-skill-template.md`, `AGENTS.md`, `PROJECT_MAP.md`
- Next audit point: 初回のブランド別 auditor SKILL 作成時

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
- ID: `FAC-2026-04-25-001`
- Hypothesis: ブランド別 auditor SKILL の共通テンプレートと作成入口を分離すれば、ブランド固有性を保ちながら `構造 → ブランド → 商品` の監査品質を揃えられる
- Intervention: `line-emoji-brand-audit-skill-builder` と `brand-audit-skill-template` を追加し、入口と brand repo 設計へ接続する
- Updated owner file: skill / template / `AGENTS.md` / `PROJECT_MAP.md` / brand repo blueprint へ反映済み。次回作成時に実効性を観測する段階
- Verification method: 初回のブランド別 auditor SKILL 作成で、共通骨格を再掲しすぎず、ブランド固有 anchor を不足なく固定できるかを見る
- Verify on: 次回のブランド別 auditor SKILL 作成時

## 3. Verified Upgrades

## 4. Skill Evolution
- ID: `FAC-2026-04-25-001`
- Friction: ブランド別監査SKILL作成が `line-emoji-skill-builder` の一般手順だけでは粒度不足になり、各ブランドで監査観点がばらつく
- Existing skill to update: `skills/line-emoji-skill-builder/SKILL.md`
- New skill needed: `skills/line-emoji-brand-audit-skill-builder/SKILL.md`
- Why workflow / template only では足りないか: template だけでは、対象 brand repo の正本を読み、固有 anchor を抽出し、既存 skill と統合する判断入口が残らない
- Next check: 初回のブランド別 auditor SKILL 作成時

## 5. Market / Diversity Memory

## 6. Lightweight Maintenance
- Heavy artifact:
- Why it became heavy:
- Compress / archive / merge / retire:
- Owner file:
- Next review date:

## 7. Deferred / Rejected
