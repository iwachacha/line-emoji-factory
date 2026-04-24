from __future__ import annotations

import math
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FINALS = ROOT / "production" / "finals"
OUT_DIR = FINALS / "release-001"
UPLOAD_ZIP = FINALS / "release-001-upload.zip"
PREVIEW = FINALS / "release-001-preview.png"
SMALL_PREVIEW = FINALS / "release-001-small-preview.png"

CANVAS = 180
TAB_SIZE = (96, 74)
SCALE = 4
OUTLINE = "#27383f"
SHADOW = (39, 56, 63, 52)
WHITE = "#fffaf0"
BAR_BG = "#d8e0df"

FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/NotoSansJP-VF.ttf"),
    Path("C:/Windows/Fonts/YuGothB.ttc"),
    Path("C:/Windows/Fonts/meiryob.ttc"),
]


@dataclass(frozen=True)
class EmojiSpec:
    filename: str
    label: str
    title: str
    meaning: str
    fill: str
    accent: str
    progress: float
    sign: str


SPECS = [
    EmojiSpec("001.png", "見", "見た", "見ました", "#e8f6ff", "#43a4d8", 0.35, "eye"),
    EmojiSpec("002.png", "了", "了解", "了解", "#eef9ec", "#52ae62", 0.70, "check"),
    EmojiSpec("003.png", "中", "対応中", "対応中", "#fff5dc", "#e0a42b", 0.55, "play"),
    EmojiSpec("004.png", "済", "完了", "完了", "#ebf8f0", "#24a760", 1.00, "doublecheck"),
    EmojiSpec("005.png", "確", "確認", "確認して", "#edf0ff", "#727bdc", 0.45, "search"),
    EmojiSpec("006.png", "返", "要返信", "返信ください", "#fff0f2", "#d76b83", 0.40, "reply"),
    EmojiSpec("007.png", "共", "共有", "共有です", "#eaf8f7", "#28a69d", 0.60, "share"),
    EmojiSpec("008.png", "礼", "ありがとう", "ありがとう", "#fff4e9", "#df8840", 0.80, "spark"),
    EmojiSpec("009.png", "待", "保留", "保留", "#f4f1ff", "#8b75cf", 0.25, "pause"),
    EmojiSpec("010.png", "後", "あとで", "あとで", "#eef7ea", "#75a843", 0.30, "clock"),
    EmojiSpec("011.png", "急", "急ぎ", "急ぎ", "#fff0e8", "#dd5b45", 0.90, "bang"),
    EmojiSpec("012.png", "締", "締切", "締切", "#fff8df", "#d69b18", 0.85, "calendar"),
    EmojiSpec("013.png", "調", "調整中", "調整中", "#eef2f5", "#5f7f95", 0.50, "sliders"),
    EmojiSpec("014.png", "未", "未定", "未定", "#f2f6fb", "#7292bd", 0.15, "question"),
    EmojiSpec("015.png", "決", "決定", "決定", "#f0f9ee", "#4aa857", 1.00, "circle"),
    EmojiSpec("016.png", "休", "休憩", "休憩", "#f6f2ea", "#a78254", 0.10, "rest"),
]


def font_path() -> Path:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    raise RuntimeError("No Japanese font found")


FONT_PATH = font_path()


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size)


def scaled_image(size: tuple[int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def sc(value: float) -> int:
    return round(value * SCALE)


def rounded(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        tuple(sc(v) for v in xy),
        radius=sc(radius),
        fill=fill,
        outline=outline,
        width=sc(width),
    )


def line(draw: ImageDraw.ImageDraw, xy, fill, width=1, joint="curve"):
    draw.line(tuple((sc(x), sc(y)) for x, y in xy), fill=fill, width=sc(width), joint=joint)


def ellipse(draw: ImageDraw.ImageDraw, xy, fill=None, outline=None, width=1):
    draw.ellipse(tuple(sc(v) for v in xy), fill=fill, outline=outline, width=sc(width))


def rectangle(draw: ImageDraw.ImageDraw, xy, fill=None, outline=None, width=1):
    draw.rectangle(tuple(sc(v) for v in xy), fill=fill, outline=outline, width=sc(width))


def polygon(draw: ImageDraw.ImageDraw, points, fill):
    draw.polygon([(sc(x), sc(y)) for x, y in points], fill=fill)


def centered_text(draw: ImageDraw.ImageDraw, text: str, y: int, size: int, fill: str, canvas: int = CANVAS):
    fnt = font(size * SCALE)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = (canvas * SCALE - (bbox[2] - bbox[0])) // 2
    draw.text((x, sc(y)), text, font=fnt, fill=fill)


def draw_sign(draw: ImageDraw.ImageDraw, spec: EmojiSpec):
    c = spec.accent
    if spec.sign == "eye":
        ellipse(draw, (122, 45, 148, 61), fill="#ffffff", outline=OUTLINE, width=4)
        ellipse(draw, (132, 50, 139, 57), fill=c)
    elif spec.sign == "check":
        line(draw, [(124, 55), (132, 63), (149, 43)], fill=c, width=7)
    elif spec.sign == "doublecheck":
        line(draw, [(118, 58), (126, 66), (142, 45)], fill=c, width=6)
        line(draw, [(133, 58), (141, 66), (158, 43)], fill=c, width=6)
    elif spec.sign == "play":
        polygon(draw, [(126, 45), (126, 66), (148, 55)], fill=c)
    elif spec.sign == "search":
        ellipse(draw, (124, 43, 146, 65), fill="#ffffff", outline=c, width=5)
        line(draw, [(141, 61), (153, 72)], fill=c, width=5)
    elif spec.sign == "reply":
        line(draw, [(150, 51), (126, 51), (136, 41)], fill=c, width=6)
        line(draw, [(126, 51), (136, 62)], fill=c, width=6)
    elif spec.sign == "share":
        for xy in [(121, 45, 133, 57), (145, 40, 157, 52), (145, 62, 157, 74)]:
            ellipse(draw, xy, fill="#ffffff", outline=c, width=4)
        line(draw, [(133, 51), (145, 46)], fill=c, width=4)
        line(draw, [(133, 55), (145, 68)], fill=c, width=4)
    elif spec.sign == "spark":
        line(draw, [(139, 38), (139, 70)], fill=c, width=4)
        line(draw, [(123, 54), (155, 54)], fill=c, width=4)
        line(draw, [(129, 44), (150, 65)], fill=c, width=3)
        line(draw, [(150, 44), (129, 65)], fill=c, width=3)
    elif spec.sign == "pause":
        rounded(draw, (126, 43, 134, 68), 3, c)
        rounded(draw, (143, 43, 151, 68), 3, c)
    elif spec.sign == "clock":
        ellipse(draw, (124, 42, 154, 72), fill="#ffffff", outline=c, width=5)
        line(draw, [(139, 57), (139, 47)], fill=OUTLINE, width=4)
        line(draw, [(139, 57), (149, 62)], fill=OUTLINE, width=4)
    elif spec.sign == "bang":
        rounded(draw, (135, 39, 145, 61), 5, c)
        ellipse(draw, (134, 65, 146, 77), fill=c)
    elif spec.sign == "calendar":
        rounded(draw, (123, 42, 155, 72), 6, "#ffffff", outline=c, width=5)
        rectangle(draw, (123, 51, 155, 58), fill=c)
    elif spec.sign == "sliders":
        for y, x in [(45, 139), (56, 129), (67, 148)]:
            line(draw, [(122, y), (156, y)], fill=c, width=4)
            ellipse(draw, (x - 5, y - 5, x + 5, y + 5), fill="#ffffff", outline=c, width=3)
    elif spec.sign == "question":
        centered_text(draw, "?", 33, 34, c)
    elif spec.sign == "circle":
        ellipse(draw, (124, 42, 154, 72), fill=None, outline=c, width=7)
    elif spec.sign == "rest":
        rounded(draw, (125, 51, 154, 69), 7, "#ffffff", outline=c, width=4)
        line(draw, [(154, 56), (162, 58), (154, 64)], fill=c, width=4)
        line(draw, [(129, 45), (134, 38)], fill=c, width=3)
        line(draw, [(142, 45), (147, 38)], fill=c, width=3)


def draw_emoji(spec: EmojiSpec) -> Image.Image:
    img, draw = scaled_image((CANVAS, CANVAS))

    rounded(draw, (18, 43, 162, 139), 31, SHADOW)
    rounded(draw, (14, 36, 166, 132), 31, spec.fill, outline=OUTLINE, width=10)

    # Inner highlight and bottom gauge.
    rounded(draw, (31, 49, 149, 68), 9, (255, 255, 255, 95))
    rounded(draw, (35, 112, 145, 125), 7, BAR_BG)
    bar_right = 35 + 110 * spec.progress
    rounded(draw, (35, 112, bar_right, 125), 7, spec.accent)

    # Small left anchor prevents pure label-only look.
    ellipse(draw, (28, 51, 44, 67), fill=spec.accent, outline=OUTLINE, width=3)

    centered_text(draw, spec.label, 49, 62, OUTLINE)
    draw_sign(draw, spec)

    # A tiny lower notch gives the gauge a product-ownable silhouette.
    polygon(draw, [(82, 132), (98, 132), (90, 143)], fill=OUTLINE)
    polygon(draw, [(84, 132), (96, 132), (90, 140)], fill=spec.fill)

    return img.resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)


def draw_tab() -> Image.Image:
    img, draw = scaled_image(TAB_SIZE)
    rounded(draw, (6, 14, 90, 60), 18, "#eaf8f7", outline=OUTLINE, width=6)
    rounded(draw, (19, 48, 77, 55), 4, BAR_BG)
    rounded(draw, (19, 48, 61, 55), 4, "#28a69d")
    fnt = font(30 * SCALE)
    text = "進"
    bbox = draw.textbbox((0, 0), text, font=fnt)
    draw.text(((TAB_SIZE[0] * SCALE - (bbox[2] - bbox[0])) // 2, sc(17)), text, font=fnt, fill=OUTLINE)
    ellipse(draw, (70, 20, 82, 32), fill="#28a69d", outline=OUTLINE, width=2)
    return img.resize(TAB_SIZE, Image.Resampling.LANCZOS)


def save_png(path: Path, image: Image.Image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", dpi=(72, 72), optimize=True)


def create_preview(paths: list[Path], tab_path: Path):
    cell = 180
    label_h = 34
    margin = 18
    preview = Image.new("RGBA", (cell * 4 + margin * 2, (cell + label_h) * 5 + margin * 2), "#f6f6f1")
    draw = ImageDraw.Draw(preview)
    small_font = font(18)

    draw.text((margin, 8), "ゆるゲージ release-001 final candidate", font=small_font, fill=OUTLINE)
    for i, path in enumerate(paths):
        row = i // 4
        col = i % 4
        x = margin + col * cell
        y = margin + 18 + row * (cell + label_h)
        tile = Image.open(path).convert("RGBA")
        preview.alpha_composite(tile, (x, y))
        spec = SPECS[i]
        draw.text((x + 12, y + cell - 2), f"{path.name} {spec.title}", font=small_font, fill=OUTLINE)

    tab = Image.open(tab_path).convert("RGBA").resize((144, 111), Image.Resampling.NEAREST)
    y = margin + 18 + 4 * (cell + label_h)
    draw.text((margin, y + 16), "tab.png", font=small_font, fill=OUTLINE)
    preview.alpha_composite(tab, (margin + 90, y))
    save_png(PREVIEW, preview)


def create_small_preview(paths: list[Path]):
    cell = 82
    margin = 12
    preview = Image.new("RGBA", (cell * 4 + margin * 2, cell * 4 + margin * 2), "#f6f6f1")
    for i, path in enumerate(paths):
        row = i // 4
        col = i % 4
        x = margin + col * cell + 9
        y = margin + row * cell + 9
        tile = Image.open(path).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
        preview.alpha_composite(tile, (x, y))
    save_png(SMALL_PREVIEW, preview)


def write_manifest(paths: list[Path], tab_path: Path):
    lines = [
        "# release-001 asset manifest",
        "",
        "- Generated: `2026-04-25 JST`",
        "- Generator: `production/finals/generate_assets.py`",
        "- Package type: `絵文字`",
        "- Contents: `001.png` to `016.png`, `tab.png`",
        "- ZIP: `production/finals/release-001-upload.zip`",
        "- Preview: `production/finals/release-001-preview.png`",
        "- Small preview: `production/finals/release-001-small-preview.png`",
        "",
        "## Metadata",
        "- Title: `ゆるゲージ 進捗と返事16`",
        "- Description: `確認中・対応中・完了など、仕事や日常の短文に進み具合と返事を軽く添える実用絵文字です。`",
        "- Copyright: `YURUGAUGE`",
        "- Suggest tags: `了解`, `完了`, `確認`, `対応`, `返信`, `共有`, `締切`, `あとで`",
        "",
        "## File Checks",
    ]

    all_paths = [tab_path] + paths
    for path in all_paths:
        with Image.open(path) as img:
            has_alpha = img.mode == "RGBA" and img.getchannel("A").getextrema()[0] < 255
            lines.append(
                f"- `{path.name}`: `{img.size[0]}x{img.size[1]}`, mode `{img.mode}`, "
                f"transparent `{has_alpha}`, size `{path.stat().st_size}` bytes"
            )

    lines.extend(
        [
            "",
            "## Individual Meanings",
        ]
    )
    for spec in SPECS:
        lines.append(f"- `{spec.filename}`: `{spec.title}` / `{spec.meaning}` / label `{spec.label}`")

    lines.extend(
        [
            "",
            "## QA Notes",
            "- All content images are `180 x 180 px` PNG with transparency.",
            "- `tab.png` is `96 x 74 px` PNG with transparency.",
            "- Each file is below `1MB`; ZIP is below `20MB`.",
            "- Watch pairs: `了 / 済 / 決`, `中 / 調`, `見 / 確 / 返`.",
        ]
    )

    (OUT_DIR / "asset-manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_zip(paths: list[Path], tab_path: Path):
    if UPLOAD_ZIP.exists():
        UPLOAD_ZIP.unlink()
    with zipfile.ZipFile(UPLOAD_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(tab_path, "tab.png")
        for path in paths:
            zf.write(path, path.name)


def validate(paths: list[Path], tab_path: Path):
    errors: list[str] = []
    if len(paths) != 16:
        errors.append(f"Expected 16 emoji files, got {len(paths)}")
    for path in paths:
        with Image.open(path) as img:
            if img.size != (180, 180):
                errors.append(f"{path.name}: expected 180x180, got {img.size}")
            if img.format != "PNG":
                errors.append(f"{path.name}: expected PNG")
            if img.mode != "RGBA" or img.getchannel("A").getextrema()[0] >= 255:
                errors.append(f"{path.name}: expected transparent alpha")
        if path.stat().st_size > 1_000_000:
            errors.append(f"{path.name}: exceeds 1MB")
    with Image.open(tab_path) as img:
        if img.size != TAB_SIZE:
            errors.append(f"tab.png: expected {TAB_SIZE}, got {img.size}")
        if img.mode != "RGBA" or img.getchannel("A").getextrema()[0] >= 255:
            errors.append("tab.png: expected transparent alpha")
    if UPLOAD_ZIP.exists() and UPLOAD_ZIP.stat().st_size > 20_000_000:
        errors.append("release-001-upload.zip exceeds 20MB")
    if errors:
        raise SystemExit("\n".join(errors))


def main():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    paths = []
    for spec in SPECS:
        path = OUT_DIR / spec.filename
        save_png(path, draw_emoji(spec))
        paths.append(path)

    tab_path = OUT_DIR / "tab.png"
    save_png(tab_path, draw_tab())
    make_zip(paths, tab_path)
    create_preview(paths, tab_path)
    create_small_preview(paths)
    validate(paths, tab_path)
    write_manifest(paths, tab_path)

    print(f"Generated {len(paths)} emoji PNGs")
    print(f"Upload ZIP: {UPLOAD_ZIP} ({UPLOAD_ZIP.stat().st_size} bytes)")
    print(f"Preview: {PREVIEW}")
    print(f"Small preview: {SMALL_PREVIEW}")
    print(f"Manifest: {OUT_DIR / 'asset-manifest.md'}")


if __name__ == "__main__":
    main()
