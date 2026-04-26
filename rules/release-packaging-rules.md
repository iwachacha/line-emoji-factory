# Release Packaging Rules

This file defines the current factory contract for emoji and sticker release packaging.

## Judgment Order

1. Structure: package layout must match the LINE upload and internal archive separation.
2. Brand: packaging must preserve source-to-submission traceability.
3. Product: output must be usable for submission without mixing internal files into the upload ZIP.

## Required Outputs

```text
releases/<release-id>/submission/
  line-upload/
    images.zip
    images/
      tab.png
      001.png
      002.png
      # static stickers additionally include:
      main.png
      01.png
      02.png
  internal-archive/
    package.zip
    metadata.yaml
    package-report.md
    asset-map.json
    package-checksums.txt
```

## Line Upload ZIP

- Contains images only.
- Must not contain `metadata.yaml`, reports, asset maps, checksums, release logs, or internal notes.
- Static emoji content image filenames are normalized to `001.png`, `002.png`, ...
- Static sticker content image filenames are normalized to `01.png`, `02.png`, ...
- The tab image filename is `tab.png`.
- The static sticker main image filename is `main.png`.

## Internal Archive

- May contain the line-upload ZIP, metadata, package report, asset map, checksums, manifest snapshot, release spec snapshot, series plan snapshot, brand canon snapshot, and product catalog snapshot.
- Exists for review, traceability, and future release learning.

## Tool Contract

- `tools/package-release.py BRAND_REPO --release-id release-001 --target both --clean`
- Production final filenames may be arbitrary.
- `asset-map.json` records source filenames and normalized submission filenames.
- `--clean` recreates `submission/line-upload/` and `submission/internal-archive/`.
- Animation emoji packaging is unsupported until a dedicated package contract is added.
- Animated, custom, message, big, pop-up, and effect sticker packaging are unsupported until their package contracts are added.
