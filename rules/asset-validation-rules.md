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
- Each image must be `1MB` or less.
- A ZIP package must be `20MB` or less.

## Filename Rules

- Production-stage filenames are not judged.
- Submission-stage content filenames must be `001.png`, `002.png`, ...
- Submission-stage tab image must be `tab.png`.

## Unsupported Scope

Animation emoji validation is explicitly unsupported for now. Animation packages must fail until APNG frame, loop, duration, and size validation are implemented.

## Tool Contract

Use `tools/validate-assets.py`.

```powershell
python tools/validate-assets.py path/to/images --expected-count 8 --stage production
python tools/validate-assets.py path/to/submission/images --expected-count 8 --stage submission
```
