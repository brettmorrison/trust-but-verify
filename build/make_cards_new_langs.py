#!/usr/bin/env python3
"""
Wallet cards for the languages that don't have one yet — reusing the
text already written in each content/<lang>/index.md landing page rather
than retranslating. 8 cards per Letter page, cut on the hairlines.

Font/shaping note (see make_fridge_new_langs.py for the fuller writeup):
reportlab's base-14 fonts are Latin-1 only, and reportlab's drawString does
no OpenType shaping or bidi reordering at all -- real Unicode fonts fix the
missing-glyph (tofu box) problem, but Arabic-script languages (fa, ps, ur)
also need arabic_reshaper to join letters into their correct contextual
forms, and RTL languages (he, fa, ps, ur) need python-bidi to reorder
logical text into visual order, before a single character is drawn.

    python3 build/make_cards_new_langs.py
"""
import os, re
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from bidi.algorithm import get_display
import arabic_reshaper

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "formats", "print")

INK = HexColor("#111111")
MUTED = HexColor("#4a4a4a")
PAPER = HexColor("#fffdf9")
ACCENT = HexColor("#123f7a")

W, H = 612, 792
COLS, ROWS = 2, 4
CARD_W, CARD_H = W / COLS, H / ROWS

LANGS = [
    "am", "bn", "da", "el", "et", "fa", "gu", "he", "hi", "hmn", "hr", "ht",
    "hu", "hy", "it", "ja", "ka", "km", "ko", "lt", "lv", "ms", "no", "pa",
    "ps", "so", "sq", "sr", "sv", "sw", "tl", "ur",
]

# --- Unicode font registration ----------------------------------------------

SYS = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(SYS, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(SYS, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("ArialUnicode", os.path.join(SYS, "Arial Unicode.ttf")))
pdfmetrics.registerFont(TTFont("KhmerSangam", os.path.join(SYS, "Khmer Sangam MN.ttf")))
pdfmetrics.registerFont(TTFont("KefaIII", os.path.join(SYS, "KefaIII.ttf")))

# Arial/Arial-Bold cover Latin-1 plus Greek and Cyrillic. Everything else
# needs a real Unicode font; Arial Unicode has no separate bold weight, so
# those languages reuse the regular face for "bold" text.
FONTS = {
    "am": ("KefaIII", "KefaIII"),
    "bn": ("ArialUnicode", "ArialUnicode"),
    "fa": ("ArialUnicode", "ArialUnicode"),
    "gu": ("ArialUnicode", "ArialUnicode"),
    "he": ("ArialUnicode", "ArialUnicode"),
    "hi": ("ArialUnicode", "ArialUnicode"),
    "hy": ("ArialUnicode", "ArialUnicode"),
    "ja": ("ArialUnicode", "ArialUnicode"),
    "ka": ("ArialUnicode", "ArialUnicode"),
    "km": ("KhmerSangam", "KhmerSangam"),
    "ko": ("ArialUnicode", "ArialUnicode"),
    "pa": ("ArialUnicode", "ArialUnicode"),
    "ps": ("ArialUnicode", "ArialUnicode"),
    "ur": ("ArialUnicode", "ArialUnicode"),
}


def fonts_for(lang):
    return FONTS.get(lang, ("Arial", "Arial-Bold"))


RTL_LANGS = {"he", "fa", "ps", "ur"}
ARABIC_SCRIPT_LANGS = {"fa", "ps", "ur"}  # need letter-joining, unlike Hebrew


def maybe_rtl(text, lang):
    if lang not in RTL_LANGS:
        return text
    if lang in ARABIC_SCRIPT_LANGS:
        text = arabic_reshaper.reshape(text)
    return get_display(text)


# Space-based wrapping breaks for languages that don't use spaces between
# words (Japanese); fall back to character-by-character wrapping when a
# string's space density is too low for word-splitting to do anything.
def _units_for(text):
    space_ratio = text.count(" ") / max(1, len(text))
    if space_ratio > 0.03:
        return text.split(), " "
    return list(text), ""


def parse(lang):
    path = os.path.join(CONTENT, lang, "index.md")
    text = open(path, encoding="utf-8").read()

    m = re.search(r'^# (.+)$', text, re.M)
    brand = m.group(1).strip()

    # Non-greedy on the heading span (`.+?`) is required: with the greedy
    # form and re.S, ".+" swallows the whole rest of the document and then
    # backtracks from the END, so it matches the LAST "**bold**" in the
    # file (the closing line) instead of the tagline immediately after the
    # H1. This silently mislabeled the tagline as the closing line for
    # every language this script generated -- see BACKLOG.md.
    m = re.search(r'^# .+?\n\n\*\*(.+?)\*\*', text, re.M | re.S)
    tagline = re.sub(r'\s+', ' ', m.group(1)).strip()

    steps = re.findall(r'\*\*\d\.\s*(.+?)\*\*\n\n(.+?)\n\n', text, re.S)
    steps = [(re.sub(r'\s+', ' ', h).strip(), re.sub(r'\s+', ' ', d).strip())
             for h, d in steps[:3]]

    helps = re.findall(r'\*\*(\d{3}-\d{3}-\d{4})\*\*\s*—\s*(.+?)\s*·', text)
    helps = [(p, "National Elder Fraud Hotline" if i == 0 else "AARP Fraud Watch")
             for i, (p, _) in enumerate(helps[:2])]

    bolds = re.findall(r'\*\*([^*]{15,220})\*\*', text, re.S)
    closing = re.sub(r'\s+', ' ', bolds[-1]).strip() if bolds else ""

    return dict(brand=brand, tagline=tagline, steps=steps, helps=helps,
                closing=closing)


def wrap_lines(text, font, size, max_w):
    units, sep = _units_for(text)
    lines, line = [], ""
    for u in units:
        t = (line + sep + u) if line else u
        if stringWidth(t, font, size) > max_w and line:
            lines.append(line)
            line = u
        else:
            line = t
    if line:
        lines.append(line)
    return lines


def draw_card(c, x0, y0, d, lang):
    FR, FB = fonts_for(lang)
    m = 14
    x, y = x0 + m, y0 + CARD_H - m
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(0.5)
    c.rect(x0, y0, CARD_W, CARD_H, fill=0, stroke=1)

    c.setFont(FB, 11)
    c.setFillColor(ACCENT)
    for line in wrap_lines(d["brand"], FB, 11, CARD_W - 2 * m):
        c.drawString(x, y - 10, maybe_rtl(line, lang))
        y -= 13
    y -= 2

    c.setFont(FR, 7.5)
    c.setFillColor(MUTED)
    for line in wrap_lines(d["tagline"], FR, 7.5, CARD_W - 2 * m)[:2]:
        c.drawString(x, y - 8, maybe_rtl(line, lang))
        y -= 10
    y -= 4

    c.setFont(FB, 7.5)
    c.setFillColor(INK)
    for i, (head, _desc) in enumerate(d["steps"], 1):
        line = "%d. %s" % (i, head)
        for wline in wrap_lines(line, FB, 7.5, CARD_W - 2 * m)[:2]:
            c.drawString(x, y - 8, maybe_rtl(wline, lang))
            y -= 10
    y -= 4

    c.setStrokeColor(HexColor("#dddddd"))
    c.line(x, y, x0 + CARD_W - m, y)
    y -= 12

    for phone, label in d["helps"]:
        c.setFont(FB, 9)
        c.setFillColor(INK)
        c.drawString(x, y - 8, phone)
        c.setFont(FR, 6.5)
        c.setFillColor(MUTED)
        c.drawString(x, y - 17, maybe_rtl(label, lang))
        y -= 22

    c.setFont(FR, 6.5)
    c.setFillColor(MUTED)
    for line in wrap_lines(d["closing"], FR, 6.5, CARD_W - 2 * m)[:2]:
        c.drawString(x, y - 7, maybe_rtl(line, lang))
        y -= 9


def draw(lang):
    d = parse(lang)
    path = os.path.join(OUT, "wallet-card-%s.pdf" % lang)
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    for row in range(ROWS):
        for col in range(COLS):
            x0 = col * CARD_W
            y0 = H - (row + 1) * CARD_H
            draw_card(c, x0, y0, d, lang)
    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    for lang in LANGS:
        draw(lang)
