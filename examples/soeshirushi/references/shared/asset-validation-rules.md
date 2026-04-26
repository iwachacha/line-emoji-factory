# Asset Validation Rules

This file defines the mechanical gate for LINE emoji image assets.

## Judgment Order

1. Structure: file type, dimensions, count, transparency, and submission names.
2. Brand: visual consistency and readable expression.
3. Product: usable small-format reactions for LINE conversations.

## Static Emoji Requirements

- Content image: `180 x 180` PNG.
- Tab image: `96 x 74` PNG.
- Content image count: `8`, `16`, `24`, `32`, or `40`.
- Transparent background is required.
- Fully transparent images fail.
- Visible content below `15%` of the canvas fails as near-empty.
- Visible content below `35%` of the canvas warns.
- Any transparent margin above `35%` warns.
- Duplicate and near-duplicate content images warn because the set may not provide enough conversation coverage.
- Low contrast visible content warns because it may collapse at small LINE emoji sizes.
- Low color variety warns as a production-review prompt, not as a structural failure.
- Each image must be `1MB` or less.
- A ZIP package must be `20MB` or less.

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
- Submission-stage content filenames must be `001.png`, `002.png`, ...
- Submission-stage tab image must be `tab.png`.

## Preview Output

The validator can generate a contact sheet for small-format readability review. The preview includes `180px`, `48px`, `32px`, and `24px` views for each content image.

## Tool Contract

Use `tools/validate-assets.py`.

```powershell
python tools/validate-assets.py path/to/images --expected-count 8 --stage production
python tools/validate-assets.py path/to/submission/line-upload/images --expected-count 8 --stage submission
python tools/validate-assets.py path/to/apng --expected-count 8 --asset-type animation
python tools/validate-assets.py path/to/submission/line-upload/images --preview-contact-sheet report/contact-sheet.png
```
