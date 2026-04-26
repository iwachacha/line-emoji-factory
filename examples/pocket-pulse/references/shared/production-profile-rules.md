# production profile ルール

このファイルは、制作工程を特定ツール名ではなく profile として扱うための正本である。

## 原則
- rule / workflow / template は、特定ツール名を正本にしない。
- 正本は工程要件であり、ツール名は profile の値として扱う。
- `rough / anchor` と `item finalization` と `product QA` の責務を混ぜない。
- `GPT / image_gen` は標準実行手段だが、工程責務そのものではない。
- optional external review を使う場合も、正本はこの profile と handoff に残す。

## 標準 profile
```yaml
production_profile:
  name: gpt-series-production
  brand_canon_stage:
    purpose: brand canon and IP guardrail confirmation
    required_outputs:
      - brand_canon
      - ip_guardrails
      - allowed_variations
      - prohibited_drift

  series_planning_stage:
    purpose: release differentiation from previous products
    required_outputs:
      - product_catalog_review
      - series_plan
      - inheritance_points
      - novelty_points
      - cannibalization_notes

  rough_stage:
    purpose: style, character, motif, and set-direction exploration
    required_outputs:
      - style_anchor
      - character_anchor
      - rough_board
      - per_item_intent
      - failure_notes

  item_finalization_stage:
    purpose: one-item-at-a-time final asset candidate production
    required_outputs:
      - item_specs
      - four_candidate_minimum
      - candidate_comparison
      - final_assets
      - correction_notes
      - export_check

  product_qa_stage:
    purpose: small-size and product usability QA
    required_outputs:
      - contact_sheet
      - chat_preview
      - asset_validation_report
      - duplicate_and_usage_overlap_notes
      - unresolved_watch_items

  release_ledger_stage:
    purpose: update release ledger and brand product catalog
    required_outputs:
      - release_log_update
      - quality_ledger_update
      - product_catalog_update
      - next_series_watch

  revision_stage:
    purpose: slot-level corrections
    required_outputs:
      - revision_notes
      - fixed_assets
      - unresolved_watch_items
```

## 禁止
- rough stage に最終品質判断まで押し込む。
- item finalization stage に構造判断やシリーズ企画を押し戻す。
- tool 名に合わせて brand rule を変える。
- prompt template 名を特定ツール名に固定する。
- 1セット全体を一括生成して final asset として扱う。
- 1アイテム1案だけで採用する。
