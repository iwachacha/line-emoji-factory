# Brand Repo Blueprint

Brand repos contain brand-specific production and release artifacts. The factory repo keeps shared rules, workflows, schemas, tools, and templates. A release chooses one LINE item type; a brand may be prepared for both emoji and stickers without forcing both to ship.

## Layout

```text
brand-repo/
  README.md
  brand-manifest.yaml
  brand/
    brand-setting.md
    brand-positioning.md
    brand-production-brief.md
    brand-system-prompt.md
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

`brand-manifest.yaml` includes `production_profile` as the machine-readable production stage contract.

## Production Assets

- Put arbitrary-named final content PNGs in `production/finals/`.
- Put the tab source PNG at `production/tab/source-tab.png`.
- For static sticker releases, put the main source PNG at `production/main/source-main.png`.
- Do not manually name submission assets. `tools/package-release.py` creates item-type-specific submission filenames.
- Static emoji submission filenames are `001.png`, `002.png`, ... and `tab.png`.
- Static sticker submission filenames are `01.png`, `02.png`, ..., `main.png`, and `tab.png`.
- Keep rough, finalization, and revision outputs in `production_profile`; do not make a tool name the production source of truth.

## Submission Outputs

- `submission/line-upload/images.zip` is the LINE upload ZIP and contains only images.
- `submission/internal-archive/package.zip` is the internal archive and contains traceability files.
