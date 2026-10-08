"""Render reference-style captions (white rounded box, purple Poppins text) as
transparent 720x1280 PNGs, one per line of captions/captions.tsv."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 720, 1280
CENTER_Y = 957          # vertical centre of the box, measured on the reference
MAX_TEXT_W = 600        # wrap width
PAD_X, PAD_Y = 24, 14
RADIUS = 22
LINE_GAP = 0
PURPLE = (122, 0, 248)  # sampled from reference (#7A00F8)
FONT = ImageFont.truetype(os.path.join(ROOT, "fonts", "poppins-latin-500-normal.woff"), 38)


def wrap(text, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=FONT) <= MAX_TEXT_W:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) == 2:  # balance the two lines like the reference captions
        best = min(range(1, len(words)),
                   key=lambda k: max(draw.textlength(" ".join(words[:k]), font=FONT),
                                     draw.textlength(" ".join(words[k:]), font=FONT)))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
    return lines


def render(text, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = wrap(text, d)
    asc, desc = FONT.getmetrics()
    lh = 46
    widths = [d.textlength(l, font=FONT) for l in lines]
    bw = max(widths) + 2 * PAD_X
    bh = len(lines) * lh + (len(lines) - 1) * LINE_GAP + 2 * PAD_Y
    x0, y0 = (W - bw) / 2, CENTER_Y - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], RADIUS, fill=(255, 255, 255, 255))
    y = y0 + PAD_Y
    for l, lw in zip(lines, widths):
        d.text(((W - lw) / 2, y), l, font=FONT, fill=PURPLE)
        y += lh + LINE_GAP
    img.save(path)
    return len(lines)


if __name__ == "__main__":
    out = os.path.join(ROOT, "captions", "png")
    os.makedirs(out, exist_ok=True)
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(ROOT, "captions", "captions.tsv"), encoding="utf-8") if l.strip()]
    for i, (s, e, t) in enumerate(rows):
        n = render(t, os.path.join(out, f"{i:03d}.png"))
        if n > 2:
            print(f"WARNING line {i} wraps to {n} lines: {t}", file=sys.stderr)
    print(f"{len(rows)} captions rendered to {out}")
