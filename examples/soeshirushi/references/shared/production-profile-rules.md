# production profile ルール

このファイルは、制作工程を特定ツール名ではなく profile として扱うための正本である。

## 原則
- rule / workflow / template は、特定ツール名を正本にしない。
- 正本は工程要件であり、ツール名は profile の値として扱う。
- rough stage、finalization stage、revision stage の責務を混ぜない。

## 標準 profile
```yaml
production_profile:
  name: rough-to-final
  rough_stage:
    purpose: structure and set-direction exploration
    required_outputs:
      - rough_board
      - per_emoji_intent
      - failure_notes

  finalization_stage:
    purpose: final asset production
    required_outputs:
      - final_assets
      - correction_notes
      - export_check

  revision_stage:
    purpose: slot-level corrections
    required_outputs:
      - revision_notes
      - fixed_assets
      - unresolved_watch_items
```

## 禁止
- rough stage に最終品質判断まで押し込む。
- finalization stage に構造判断を押し戻す。
- tool 名に合わせて brand rule を変える。
- prompt template 名を特定ツール名に固定する。
