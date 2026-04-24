# ブランドスターターキット テンプレート

このテンプレートは、個別ブランドへ配布する初期支援セットの構成を記録する。
全ブランドを同じ型に固定せず、共通コアと optional module を分ける。

## 1. Meta
- ブランド名: [BRAND_NAME]
- brand slug: [BRAND_SLUG]
- 作成日: [INIT_DATE]
- factory_base_version: [FACTORY_BASE_VERSION]
- template_schema_version: 1.1
- 参照する brand-setting:
- 参照する brand-production-brief:
- 参照する release spec:

## 2. Common Core
- [ ] brand-setting
- [ ] brand-production-brief
- [ ] release-spec
- [ ] production-handoff
- [ ] brand-system-prompt
- [ ] gpt-image2 rough prompts
- [ ] ClaudeDesign prompts
- [ ] revision prompts
- [ ] release-checklist
- [ ] quality-ledger
- [ ] usage-validation
- [ ] release-log
- [ ] sales-package-manifest
- [ ] brand-manifest

## 3. Optional Modules
- 固定IP設計:
  - enabled: [FIXED_IP_ENABLED]
  - fixed-ip-bible: [FIXED_IP_BIBLE_PATH]
  - 起動条件:
- キャラクター運用:
  - enabled:
  - キャラクター数:
  - 関係性:
- コンセプト / 記号運用:
  - enabled:
  - 固定する視覚文法:
  - 固定IPなしで守る境界:
- アニメーション絵文字:
  - enabled:
  - 1フレーム目ルール:
  - フレーム / ループ方針:
- デコ文字:
  - enabled:
  - package type:
  - 可読性ルール:
- 季節 / 文化派生:
  - enabled:
  - 使用期間:
  - 通年派生方針:

## 4. Brand-Specific Optimization
- 共通コアからそのまま使うもの:
- ブランド用に最適化するもの:
- 使わない optional module:
- 後で足す可能性がある module:
- 最初の release で検証すること:

## 5. Handoff To Brand Repo
- この repo での working source of truth:
- snapshot 参照先:
- ユーザーが手作業で行うこと:
- factory へ戻す改善候補:
