# Asset Validation Rules

This file defines the mechanical gate for LINE emoji and sticker image assets.
Product-level visual judgment is defined in `rules/visual-asset-quality-rules.md`.

## Judgment Order

1. Structure: file type, dimensions, count, transparency, and submission names.
2. Brand: visual consistency and readable expression.
3. Product: usable reactions for LINE conversations at the selected item size.

## Static Emoji Requirements

- Content image: `180 x 180` PNG.
- Tab image: `96 x 74` PNG.
- Content image count: `8`, `16`, `24`, `32`, or `40`.
- Transparent background is required.
- Fully transparent images fail.
- White, colored, photo, or scenery backgrounds fail when they replace transparency.
- Visible content below `15%` of the canvas fails as near-empty.
- Visible content below `35%` of the canvas warns.
- Any transparent margin above `35%` warns.
- Duplicate and near-duplicate content images warn because the set may not provide enough conversation coverage.
- Duplicate or near-duplicate warnings must be checked against the release spec and series plan; if the usage is also overlapping, the item is `Revise`.
- Low contrast visible content warns because it may collapse at small LINE emoji sizes.
- Low color variety warns as a production-review prompt, not as a structural failure.
- Each image must be `1MB` or less.
- A ZIP package must be `20MB` or less.

## Static Sticker Requirements

- Main image: `240 x 240` PNG.
- Content image: PNG up to `370 x 320`.
- Content image width and height must be even numbers.
- Tab image: `96 x 74` PNG.
- Content image count: `8`, `16`, `24`, `32`, or `40`.
- Transparent background is required.
- Fully transparent images fail.
- White, colored, photo, or scenery backgrounds fail when they replace transparency.
- Visible content below `15%` of the canvas fails as near-empty.
- Visible content below `35%` of the canvas warns.
- Any transparent margin above `35%` warns.
- Around `10px` of margin is expected by the official guideline, but the validator treats extreme transparent margins as warnings instead of failing ordinary artwork.
- Duplicate and near-duplicate content images warn because the set may not provide enough conversation coverage.
- Duplicate or near-duplicate warnings must be checked against the release spec and series plan; if the usage is also overlapping, the item is `Revise`.
- Low contrast visible content warns because it may collapse in LINE previews.
- Low color variety warns as a production-review prompt, not as a structural failure.
- Each image must be `1MB` or less.
- A ZIP package must be `60MB` or less.

## Animation Emoji Requirements

- Content image: `180 x 180` APNG with `.png` extension.
- APNG file size must be `300KB` or less.
- Frame count must be `5` to `20`.
- Total animation duration must be `4` seconds or less.
- Loop count must be `1` to `4`.
- Tab image remains a static `96 x 74` PNG.
- `tools/package-release.py` is still a static packaging pipeline. Do not package animation emoji until release packaging support is added.

## Filename Rules

- Production-stage filenames are not judged.
- Emoji submission-stage content filenames must be `001.png`, `002.png`, ...
- Sticker submission-stage content filenames must be `01.png`, `02.png`, ...
- Submission-stage tab image must be `tab.png`.
- Sticker submission-stage main image must be `main.png`.

## Visual Product Warnings

The validator can warn on:

- near-empty visible content
- excessive transparent margins
- duplicate and near-duplicate images
- low contrast visible content
- low color variety

These warnings are not a substitute for item-level QA. Use `rules/visual-asset-quality-rules.md` and `workflows/item-generation-workflow.md` to decide whether a warning is acceptable, `Revise`, or `Hard NG`.

## Preview Output

The validator can generate:

- contact sheet: multiple downscaled views for each content image
- chat preview: small LINE-like rows for conversation readability
- report JSON: machine-readable errors and warnings

The standard preview sizes are `180px / 96px / 48px / 32px`.

## Tool Contract

Use `tools/validate-assets.py`.

```powershell
python tools/validate-assets.py path/to/images --expected-count 8 --stage production --asset-type static-emoji
python tools/validate-assets.py path/to/submission/line-upload/images --expected-count 8 --stage submission --asset-type static-emoji
python tools/validate-assets.py path/to/sticker-images --expected-count 8 --stage production --asset-type static-sticker --main-image path/to/main.png --tab-image path/to/tab.png
python tools/validate-assets.py path/to/apng --expected-count 8 --asset-type animation-emoji
python tools/validate-assets.py path/to/submission/line-upload/images --preview-contact-sheet report/contact-sheet.png --preview-chat-sheet report/chat-preview.png --report-json report/asset-validation.json
```
