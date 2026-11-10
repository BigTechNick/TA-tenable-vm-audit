"""Draws the add-on's icons (an audit log page with a magnifying glass): static/appIcon*.png."""
import os
import sys
from PIL import Image, ImageDraw

NAVY = (31, 78, 121, 255)


def draw(size, background):
    s = size * 8
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fg, bg = (255, 255, 255, 255), NAVY
    if background:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=s // 6, fill=NAVY)
    else:
        fg, bg = NAVY, (0, 0, 0, 0)
    w = max(2, s // 22)
    # log page with lines
    d.rounded_rectangle([s * 0.18, s * 0.14, s * 0.66, s * 0.82], radius=s // 30, outline=fg, width=w)
    for y in (0.30, 0.42, 0.54):
        d.line([s * 0.27, s * y, s * 0.57, s * y], fill=fg, width=w)
    d.line([s * 0.27, s * 0.66, s * 0.44, s * 0.66], fill=fg, width=w)
    # magnifying glass over the lower right corner
    cx, cy, r = s * 0.64, s * 0.62, s * 0.15
    d.ellipse([cx - r - w, cy - r - w, cx + r + w, cy + r + w], fill=bg)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg, width=w)
    hw = w * 1.4
    d.line([cx + r * 0.72, cy + r * 0.72, s * 0.86, s * 0.86], fill=fg, width=int(hw))
    return img.resize((size, size), Image.LANCZOS)


def main(folder):
    os.makedirs(folder, exist_ok=True)
    for name, size, bg in (("appIcon.png", 36, True), ("appIcon_2x.png", 72, True),
                           ("appIconAlt.png", 36, False), ("appIconAlt_2x.png", 72, False)):
        draw(size, bg).save(os.path.join(folder, name), optimize=True)


if __name__ == "__main__":
    main(sys.argv[1])
