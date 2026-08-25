#!/usr/bin/env python3
"""
Social share cards (og:image), one per page — typographic, not photo-based.
Deliberately sidesteps sourcing/licensing real photos: every card is built
from the site's own design system (trust-blue, magnifying-glass-and-
checkmark mark, the page's own title + description), so there's nothing to
attribute and nothing that can go stale or be the wrong photo for the page.

Font coverage was verified visually per script before shipping (see
BACKLOG.md — this project already shipped one tofu-box font bug this
session and this script exists partly to not repeat it). Arial Unicode
covers every script used on this site except Amharic and Khmer, which get
their own fonts.

    python3 build/make_share_cards.py

Writes to formats/og/ — NOT site/og/. Like the fridge-sheet PDFs, these are
committed to the repo and copied into site/ by build_site.py at build time,
rather than regenerated on every Cloudflare Pages build: this script uses
macOS system fonts (Arial Unicode, Kefa, Khmer Sangam MN) for correct
per-script rendering, which (a) don't exist in Cloudflare's Linux build
image and (b) aren't Apple-licensed for redistribution anyway. Regenerate
locally whenever a page's title/description changes, then commit the PNGs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "formats", "og")

W, H = 1200, 630
INK = (17, 17, 17)
MUTED = (74, 74, 74)
PAPER = (255, 253, 249)
ACCENT = (18, 63, 122)

FONT_DIR = "/System/Library/Fonts/Supplemental"
F_LATIN_BOLD = os.path.join(FONT_DIR, "Arial Bold.ttf")
F_LATIN_REG = os.path.join(FONT_DIR, "Arial.ttf")
F_UNICODE = os.path.join(FONT_DIR, "Arial Unicode.ttf")
F_AMHARIC = os.path.join(FONT_DIR, "KefaIII.ttf")
F_KHMER = os.path.join(FONT_DIR, "Khmer Sangam MN.ttf")

LATIN_LANGS = {
    "en", "es", "vi", "de", "fr", "pt", "pl", "ro", "uk", "id", "ht", "so",
    "hmn", "lt", "lv", "et", "it", "hu", "hr", "sr", "ms", "sv", "no", "da",
    "sw", "tl", "sq", "ru", "el",
}
# sr is Cyrillic in our content but Arial Bold covers Cyrillic; ru/el too.

RTL_LANGS = {"ar", "ur", "fa", "ps", "he"}

_font_cache = {}


def get_font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def title_font_for(lang, size):
    if lang == "am":
        return get_font(F_AMHARIC, size), 0
    if lang == "km":
        return get_font(F_KHMER, size), 0
    if lang in LATIN_LANGS:
        return get_font(F_LATIN_BOLD, size), 0
    # Arial Unicode has no bold weight file; fake it with a stroke.
    return get_font(F_UNICODE, size), max(1, size // 22)


def body_font_for(lang, size):
    if lang == "am":
        return get_font(F_AMHARIC, size)
    if lang == "km":
        return get_font(F_KHMER, size)
    if lang in LATIN_LANGS:
        return get_font(F_LATIN_REG, size)
    return get_font(F_UNICODE, size)


def wrap(draw, text, fnt, max_w, stroke_width=0):
    # Word-wrap for space-delimited scripts; character-wrap for CJK/Khmer,
    # which don't reliably use spaces between words.
    space_ratio = text.count(" ") / max(1, len(text))
    units = text.split(" ") if space_ratio > 0.03 else list(text)
    sep = " " if space_ratio > 0.03 else ""
    lines, line = [], ""
    for u in units:
        test = (line + sep + u) if line else u
        extra = stroke_width * 2
        if draw.textlength(test, font=fnt) + extra > max_w and line:
            lines.append(line)
            line = u
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def draw_mark(draw, x, y, r, color, width=7):
    draw.ellipse([x - r, y - r, x + r, y + r], outline=color, width=width)
    draw.line([(x - r * 0.36, y), (x - r * 0.11, y + r * 0.28), (x + r * 0.42, y - r * 0.35)],
              fill=color, width=width, joint="curve")
    hx1, hy1 = x + r * 0.72, y + r * 0.72
    hx2, hy2 = x + r * 1.55, y + r * 1.55
    draw.line([(hx1, hy1), (hx2, hy2)], fill=color, width=width + 2)


def draw_watermark(img, rtl):
    # A big, quiet version of the site mark, bottom corner — fills the dead
    # space the card used to leave empty, without adding a sourced photo.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    r = 210
    cx = m_watermark_x(rtl)
    cy = H - 60
    tint = ACCENT + (26,)
    od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=tint, width=26)
    od.line([(cx - r * 0.36, cy), (cx - r * 0.11, cy + r * 0.28), (cx + r * 0.42, cy - r * 0.35)],
            fill=tint, width=26, joint="curve")
    hx1, hy1 = cx + r * 0.72, cy + r * 0.72
    hx2, hy2 = cx + r * 1.55, cy + r * 1.55
    od.line([(hx1, hy1), (hx2, hy2)], fill=tint, width=30)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))


def m_watermark_x(rtl):
    return 260 if rtl else W - 260


def make_card(title, desc, lang, rtl, out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw_watermark(img, rtl)
    d = ImageDraw.Draw(img)

    m = 70
    mark_x = W - m - 26 if rtl else m + 26
    draw_mark(d, mark_x, m + 26, 24, ACCENT)
    wm = "TRUST BUT VERIFY"
    wm_font = get_font(F_LATIN_BOLD, 26)
    if rtl:
        d.text((mark_x - 36, m + 8), wm, font=wm_font, fill=INK, anchor="ra")
    else:
        d.text((mark_x + 36, m + 8), wm, font=wm_font, fill=INK)

    d.line([(m, 150), (W - m, 150)], fill=(200, 200, 200), width=2)

    size = 56 if len(title) < 40 else 46
    tfont, stroke = title_font_for(lang, size)
    lines = wrap(d, title, tfont, W - 2 * m, stroke)[:3]
    y = 210
    for line in lines:
        x = W - m if rtl else m
        anchor = "ra" if rtl else "la"
        d.text((x, y), line, font=tfont, fill=INK, stroke_width=stroke, stroke_fill=INK, anchor=anchor)
        y += int(size * 1.22)

    if desc:
        y += 18
        dsize = 24
        dfont = body_font_for(lang, dsize)
        dlines = wrap(d, desc, dfont, W - 2 * m)[:2]
        for line in dlines:
            x = W - m if rtl else m
            anchor = "ra" if rtl else "la"
            d.text((x, y), line, font=dfont, fill=MUTED, anchor=anchor)
            y += int(dsize * 1.45)

    d.line([(m, H - 90), (W - m, H - 90)], fill=(200, 200, 200), width=2)
    url_font = get_font(F_LATIN_BOLD, 20)
    tag_font = get_font(F_LATIN_REG, 18)
    if rtl:
        d.text((W - m, H - 68), "trustbutverifyproject.org", font=url_font, fill=ACCENT, anchor="ra")
        d.text((m, H - 66), "Free · CC BY · no ads", font=tag_font, fill=MUTED)
    else:
        d.text((m, H - 68), "trustbutverifyproject.org", font=url_font, fill=ACCENT)
        d.text((W - m, H - 66), "Free · CC BY · no ads", font=tag_font, fill=MUTED, anchor="ra")

    img.save(out_path, "PNG", optimize=True)


def split_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
    return meta


def main():
    os.makedirs(OUT, exist_ok=True)
    count = 0
    for dirpath, _dirs, files in os.walk(CONTENT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            meta = split_front_matter(open(path, encoding="utf-8").read())
            title = meta.get("title", "Trust But Verify")
            desc = meta.get("description", "")
            lang = meta.get("lang", "en")
            slug = meta.get("slug") or "/" + os.path.relpath(path, CONTENT)[:-3]
            rel = slug.strip("/") or "index"
            out_path = os.path.join(OUT, rel.replace("/", "_") + ".png")
            make_card(title, desc, lang, lang in RTL_LANGS, out_path)
            count += 1
    print("wrote %d share cards to %s" % (count, OUT))


if __name__ == "__main__":
    main()
