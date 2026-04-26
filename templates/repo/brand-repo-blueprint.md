# Brand Repo Blueprint

Brand repos contain brand-specific production and release artifacts. The factory repo keeps shared rules, workflows, schemas, tools, and templates. A release chooses one LINE item type; a brand may be prepared for both emoji and stickers without forcing both to ship.

## Layout

```text
brand-repo/
  README.md
  brand-manifest.yaml
  brand/
    brand-canon.md
    brand-setting.md
    brand-positioning.md
    brand-production-brief.md
    brand-system-prompt.md
    product-catalog.md
    ip/
      ip-style-bible.md
      reference-asset-register.md
      ip-approval-log.md
      character-expression-matrix.md
  market/
    market-observation-log.md
    category-gap-map.md
  releases/
    release-001/
      series-plan.md
      release-spec.md
      production-handoff.md
      release-log.md
      prompts/
      production/
        rough-boards/
        finals/
        main/
          source-main.png
        tab/
          source-tab.png
      qa/
      submission/
        metadata.yaml
        submission-checklist.md
        submission-audit-report.md
        line-upload/
        internal-archive/
  references/
    shared/
  schemas/
  tools/
```

`brand-manifest.yaml` includes `production_profile` as the machine-readable production stage contract and points to brand canon, product catalog, and active series plan.

## Production Assets

- Put arbitrary-named final content PNGs in `production/finals/`.
- Put the tab source PNG at `production/tab/source-tab.png`.
- For static sticker releases, put the main source PNG at `production/main/source-main.png`.
- Do not manually name submission assets. `tools/package-release.py` creates item-type-specific submission filenames.
- Static emoji submission filenames are `001.png`, `002.png`, ... and `tab.png`.
- Static sticker submission filenames are `01.png`, `02.png`, ..., `main.png`, and `tab.png`.
- Keep brand canon, series planning, rough / anchor, item finalization, product QA, ledger update, and revision outputs in `production_profile`; do not make a tool name the production source of truth.
- Do not treat rough boards or bulk-generated set images as final assets.
- Finalization is one item at a time, with at least four candidates per item and QA before adoption.

## Series Operations

- `brand/brand-canon.md` defines the brand/IP elements that cannot drift.
- `brand/product-catalog.md` records past releases and series differences.
- Each release has `series-plan.md`; create it before `release-spec.md` when developing a new series.
- After QA, update product catalog with inherited elements, successful differentiation, and overlap to avoid.

## Submission Outputs

- `submission/line-upload/images.zip` is the LINE upload ZIP and contains only images.
- `submission/internal-archive/package.zip` is the internal archive and contains traceability files.
