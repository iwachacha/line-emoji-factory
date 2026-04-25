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
- Evidence: `workflows/quality-control-workflow.md`, 旧 `skills/line-emoji-improvement-auditor/SKILL.md`, `PROJECT_MAP.md` だけでは、作業後の学習閉路と軽量化判断が分散していた
- Candidate owner file: `rules/continuous-improvement-rules.md`, `workflows/continuous-improvement-workflow.md`, `skills/line-emoji-factory-auditor/SKILL.md`
- Next audit point: 次回の探索相談、次回の改善監査、次回の doc audit
- ID: `FAC-2026-04-24-002`
- Date: `2026-04-24`
- Trigger: `そえしるし` を見ると、設計は通っていても `具体会話で本当に勝つか` と `milestone ごとの圧縮学習` を残す部品が弱かった
- Scope candidate: `factory common`
- Observation: quality ledger だけでは `どの会話で句読点に負けるか` と `何を削って軽く保つか` が薄く、brand 実例から基盤不足が見えた
- Affected layer: `商品 / 品質 / 運用`
- Evidence: `examples/soeshirushi/releases/release-001/qa/quality-ledger.md`, `examples/soeshirushi/releases/release-001/release-spec.md`, `examples/soeshirushi/releases/release-001/production-handoff.md`
- Candidate owner file: `workflows/usage-validation-workflow.md`, `templates/qa/usage-validation-template.md`, `workflows/release-retrospective-workflow.md`, `templates/qa/release-retrospective-template.md`
- Next audit point: `release-001` rough 後
- ID: `FAC-2026-04-25-001`
- Date: `2026-04-25`
- Trigger: 他AIによる factory 改善提案を監査し、実装に落とす必要があった
- Scope candidate: `factory common`
- Observation: factory が思想と文書に寄っており、schema / validator / scaffold / CI / submission 前検査の機械的な抑止力が不足していた
- Affected layer: `構造 / 商品 / 品質 / skill / tool`
- Evidence: `line-emoji-factory-improvement-proposal.md`, `README.md`, 旧 `scripts/init-brand-repo.ps1`, 旧 `skills/line-emoji-producer/SKILL.md`
- Candidate owner file: `docs/factory-improvement-adoption-2026-04-25.md`, `PROJECT_MAP.md`, `tools/`, `schemas/`, `skills/line-emoji-factory-auditor/SKILL.md`
- Next audit point: scaffold smoke test と次回 brand repo 生成
- ID: `FAC-2026-04-25-002`
- Date: `2026-04-25`
- Trigger: 改善案の全実装完了と push まで求められた
- Scope candidate: `factory common`
- Observation: P0で段階化した template 階層化、P1/P2 skill、release packager、post-release 学習、soeshirushi 新 scaffold 移行まで閉じる必要があった
- Affected layer: `構造 / 商品 / skill / tool / CI`
- Evidence: `docs/factory-improvement-adoption-2026-04-25.md`
- Candidate owner file: `templates/`, `skills/`, `tools/package-release.py`, `workflows/release-packaging-workflow.md`, `workflows/post-release-learning-workflow.md`
- Next audit point: 実画像あり brand repo で package-release を実行する時

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

## 3. Verified Upgrades
- ID: `FAC-2026-04-25-001`
- Verified: P0 の基盤改善として、採用判断文書、README、schema、validator、CI、router / auditor skill、固定IP入口、market / submission template、example 移動を実装した
- Verification method: `tools/init-brand-repo.ps1` で生成し、`tools/validate-brand-repo.ps1` と schema / metadata validation を通す
- Remaining risk: 実画像ありの申請 package と公開後 metrics は、実運用データが入るまで monitor only
- ID: `FAC-2026-04-25-002`
- Verified: template canonical path の完全階層化、P1/P2 skill 追加、release package tool、post-release 学習、CI保守 workflow、soeshirushi の新 scaffold 構造移行を実装した
- Verification method: schema validation、PowerShell syntax、YAML parse、scaffold smoke、brand repo validation、metadata validation、asset validation、package smoke、example validation、diff check
- Remaining risk: 実販売データを使う post-release 分析は、公開後データが入るまで monitor only
- ID: `FAC-2026-04-26-002`
- Verified: P1 asset validation として APNG 検査、contact sheet preview、metadata risk keyword 外部化テストを追加した
- Verification method: `pytest`, `python tools/validate-assets.py ... --asset-type animation`, `python tools/validate-assets.py ... --preview-contact-sheet ...`
- Remaining risk: animation release packaging は未実装のため、`tools/package-release.py` は static package 専用として維持する
- ID: `FAC-2026-04-26-003`
- Verified: P2 として APNG 検査の duration/static-negative coverage、post-release metrics schema、manifest / tool / scaffold への `production_profile` 接続、`examples/soeshirushi` の standalone drift check を実装した
- Verification method: `python -m compileall tools`, `python tools/validate-schemas.py --check-schemas schemas`, `python tools/check-project-map-paths.py`, `python tools/check-example-drift.py examples/soeshirushi`, `pytest`, scaffold smoke, package smoke
- Owner files updated: `schemas/brand-manifest.schema.json`, `schemas/post-release-metrics.schema.json`, `tools/validate-brand-repo.py`, `tools/check-example-drift.py`, `tools/init-brand-repo.ps1`, `templates/repo/brand-repo-manifest-template.yaml`, `examples/soeshirushi/`, `.github/workflows/validate.yml`
- Remaining risk: animation release packaging は引き続き未実装で、実販売データを使う post-release metrics は公開後データが入るまで monitor only
- Push status: this work is intended to be committed and pushed after final validation

## 4. Skill Evolution
- ID: `FAC-2026-04-25-001`
- Change: 旧 `line-emoji-producer` を `line-emoji-router` へ置換し、旧 doc / improvement / evolver / skill-builder 系入口を `line-emoji-factory-auditor` へ統合した
- Reason: 実務1 + メタ4の構造では、画像検査、申請監査、固定IP統制の入口が弱く、同じ概念を別名で増やしていた
- Next review: 次回の通常相談、画像検査、申請前監査で router と auditor の責務が過不足ないかを見る
- ID: `FAC-2026-04-25-002`
- Change: P1/P2 実務 skill を追加し、router から市場観測、ブランド抽出、set設計、制作管理、package、公開後分析へ接続できるようにした
- Reason: factory を `考える` だけでなく、`作る / 検査する / 提出する / 学ぶ` へ閉じるため
- Next review: 次回の release package 作成と公開後分析で skill の粒度を確認する

## 5. Market / Diversity Memory

## 6. Lightweight Maintenance
- Heavy artifact:
- Why it became heavy:
- Compress / archive / merge / retire:
- Owner file:
- Next review date:

## 7. Deferred / Rejected
# 2026-04-26 P0 Implementation Note

- ID: `FAC-2026-04-26-001`
- Scope: `package / validation / schema / CI / docs`
- Change: split LINE upload image ZIP from internal archive, made brand validation manifest-driven, hardened asset and metadata validators, added pytest negative gates, and synchronized quickstart docs.
- Owner files updated: `tools/`, `schemas/brand-manifest.schema.json`, `rules/line-platform-baseline.md`, `rules/asset-validation-rules.md`, `rules/release-packaging-rules.md`, `README.md`, `docs/quickstart.md`, `PROJECT_MAP.md`, `AGENTS.md`.
- Verification target: `python -m compileall tools`, `python tools/validate-schemas.py --check-schemas schemas`, `python tools/check-project-map-paths.py`, `pytest`, package smoke, brand repo validation smoke.
- Push status: not attempted in this working turn unless explicitly requested.
