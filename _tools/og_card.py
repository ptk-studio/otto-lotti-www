#!/usr/bin/env python3
"""Build otto-lotti.com's share card (og:image, 1200x630) from the site's own otter art: $0, no AI.

python3 _tools/og_card.py   -> assets/og.jpg (_tools/ is skipped by Jekyll, so never served)   (otto-lotti#14)
The page's water gradient, the two otters, the page's headline and tagline. 88eggs asset OpswSdNoKRB3Nmq5LNa-I (Web:Otto-Lotti; R62).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
TOP, MID, BOT = (0xB9, 0xEC, 0xF5), (0x3F, 0xA9, 0xBD), (0x1D, 0x6F, 0x7E)
INK, SAND = (0x14, 0x34, 0x3D), (0xF7, 0xEF, 0xE2)
ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main() -> Path:
    im = Image.new("RGB", (W, H))
    px = ImageDraw.Draw(im)
    for y in range(H):   # the page's gradient: #b9ecf5 → #3fa9bd at 45% → #1d6f7e
        t = y / (H - 1)
        c = mix(TOP, MID, t / 0.45) if t < 0.45 else mix(MID, BOT, (t - 0.45) / 0.55)
        px.line([(0, y), (W, y)], fill=c)
    otto = Image.open(ROOT / "assets" / "otto.png").convert("RGBA").resize((300, 300), Image.LANCZOS)
    lotti = Image.open(ROOT / "assets" / "lotti.png").convert("RGBA").resize((300, 300), Image.LANCZOS)
    lotti = lotti.transpose(Image.FLIP_LEFT_RIGHT)   # mirrored, as on the page (figure.flip)
    im.paste(otto, (250, 40), otto)
    im.paste(lotti, (650, 40), lotti)
    draw = ImageDraw.Draw(im)
    head = ImageFont.truetype(ROUNDED, 76)
    sub = ImageFont.truetype(ROUNDED, 36)
    for text, font, y, fill in (("Meet Otto & Lotti!", head, 380, SAND), ("Two little otters · One big splash", sub, 478, SAND),
                                ("otto-lotti.com", sub, 560, (0xD8, 0xF3, 0xF7))):
        w = draw.textlength(text, font=font)
        draw.text(((W - w) / 2 + 2, y + 3), text, font=font, fill=INK)   # a soft shadow for contrast on the water
        draw.text(((W - w) / 2, y), text, font=font, fill=fill)
    out = ROOT / "assets" / "og.jpg"
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return out


if __name__ == "__main__":
    print(main())
