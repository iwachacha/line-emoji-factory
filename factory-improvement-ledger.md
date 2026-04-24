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
- Trigger: ブランド創出とブランドスタートアップセット支援の共通基盤を全体監査した
- Scope candidate: `factory common`
- Observation: `Design Ready` 後に、共通品質を保ったままブランドごとの可変域を明示して、制作・QA・prompt・scaffold へ一式化する正本が薄かった
- Affected layer: `商品 / 品質 / 制作パイプライン / 文書`
- Evidence: `workflows/production-pipeline-workflow.md`, `templates/brand-production-brief-template.md`, `templates/gpt-image2-rough-prompts-template.md`, `templates/brand-repo-manifest-template.yaml`
- Candidate owner file: `workflows/brand-startup-set-workflow.md`, `templates/brand-production-brief-template.md`, `templates/brand-system-prompt-template.md`, 工程別 prompt templates, `templates/brand-repo-manifest-template.yaml`, `scripts/init-brand-repo.ps1`
- Next audit point: 次回の brand repo scaffold と初期 release 設計
- ID: `FAC-2026-04-25-002`
- Date: `2026-04-25`
- Trigger: ブランド創出後に固定IP設計、実絵文字制作、LINE販売直前状態まで整える共通基盤が必要になった
- Scope candidate: `factory common`
- Observation: startup set は設計一式に強いが、固定IPの権利 / 造形 / 禁止 drift と、手作業提出直前の asset / metadata / manifest を切り分ける正本が不足していた
- Affected layer: `固定IP / 商品 / 品質 / 販売直前パッケージ / scaffold`
- Evidence: `templates/brand-setting-template.md`, `workflows/production-pipeline-workflow.md`, `workflows/quality-control-workflow.md`, `templates/release-checklist-template.md`, `templates/brand-repo-blueprint.md`
- Candidate owner file: `workflows/fixed-ip-design-workflow.md`, `templates/fixed-ip-bible-template.md`, `workflows/sales-ready-package-workflow.md`, `templates/sales-package-manifest-template.md`, `scripts/init-brand-repo.ps1`
- Next audit point: 次回の固定IPブランド制作と販売直前パッケージ生成

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
- Hypothesis: brand startup set の正本と工程別 prompt 骨格を明示すれば、共通固定条件を保ちながらブランドごとの可変域を制作・QA・scaffold に落としやすくなる
- Intervention: startup set workflow を追加し、相談 / 制作 / QA / lifecycle / scaffold / prompt template を追随更新する
- Updated owner file: workflow / template / scaffold へ反映済み。一時 scaffold で snapshot、manifest 参照、実用 prompt 束の生成を確認済み
- Verification method: 次回の実ブランド scaffold と初期 release 設計で、共通固定条件とブランド可変域が混線しないかを見る
- Verify on: 次回 brand startup set 作成時
- ID: `FAC-2026-04-25-002`
- Hypothesis: fixed IP bible と sales package manifest を追加すれば、ブランド固有のIPらしさを保ちながら、手作業提出直前の asset / metadata まで再利用可能な品質で揃えられる
- Intervention: fixed IP design workflow、sales-ready package workflow、対応 template、brand repo scaffold を追加・更新する
- Updated owner file: fixed IP を任意 module として扱う startup set、fixed IP bible、sales-ready package、manifest、export-ready README、brand repo scaffold へ反映済み
- Verification method: `scripts/init-brand-repo.ps1` を固定IPなし / `-IncludeFixedIp` ありの両方で実行し、starter kit、manifest、任意 fixed IP bible、export-ready README、sales package manifest、workflow snapshot の生成差分を確認済み
- Verify on: 次回の実ブランド startup set 作成と販売直前パッケージ生成時

## 3. Verified Upgrades

## 4. Skill Evolution

## 5. Market / Diversity Memory

## 6. Lightweight Maintenance
- Heavy artifact:
- Why it became heavy:
- Compress / archive / merge / retire:
- Owner file:
- Next review date:

## 7. Deferred / Rejected
