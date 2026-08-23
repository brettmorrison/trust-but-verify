#!/usr/bin/env python3
"""
Wallet cards for the 32 languages that don't have one yet — reusing the
text already written in each content/<lang>/index.md landing page rather
than retranslating. 8 cards per Letter page, cut on the hairlines.

    python3 build/make_cards_new_langs.py
"""
import os, re
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

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
    "am", "bn", "da", "el", "et", "fa", "gu", "he", "hi", "hmn", "hr", "hu",
    "hy", "it", "ja", "ka", "km", "ko", "lt", "lv", "ms", "no", "pa", "ps",
    "so", "sq", "sr", "sv", "sw", "tl", "ur",
]


def parse(lang):
    path = os.path.join(CONTENT, lang, "index.md")
    text = open(path, encoding="utf-8").read()

    m = re.search(r'^# (.+)$', text, re.M)
    brand = m.group(1).strip()

    m = re.search(r'^# .+\n\n\*\*(.+?)\*\*', text, re.M | re.S)
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
    words, lines, line = text.split(), [], ""
    for w in words:
        t = (line + " " + w).strip()
        if stringWidth(t, font, size) > max_w and line:
            lines.append(line)
            line = w
        else:
            line = t
    if line:
        lines.append(line)
    return lines


def draw_card(c, x0, y0, d):
    m = 14
    x, y = x0 + m, y0 + CARD_H - m
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(0.5)
    c.rect(x0, y0, CARD_W, CARD_H, fill=0, stroke=1)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ACCENT)
    for line in wrap_lines(d["brand"], "Helvetica-Bold", 11, CARD_W - 2 * m):
        c.drawString(x, y - 10, line)
        y -= 13
    y -= 2

    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    for line in wrap_lines(d["tagline"], "Helvetica", 7.5, CARD_W - 2 * m)[:2]:
        c.drawString(x, y - 8, line)
        y -= 10
    y -= 4

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(INK)
    for i, (head, _desc) in enumerate(d["steps"], 1):
        line = "%d. %s" % (i, head)
        for wline in wrap_lines(line, "Helvetica-Bold", 7.5, CARD_W - 2 * m)[:2]:
            c.drawString(x, y - 8, wline)
            y -= 10
    y -= 4

    c.setStrokeColor(HexColor("#dddddd"))
    c.line(x, y, x0 + CARD_W - m, y)
    y -= 12

    for phone, label in d["helps"]:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(INK)
        c.drawString(x, y - 8, phone)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(MUTED)
        c.drawString(x, y - 17, label)
        y -= 22

    c.setFont("Helvetica-Oblique", 6.5)
    c.setFillColor(MUTED)
    for line in wrap_lines(d["closing"], "Helvetica-Oblique", 6.5, CARD_W - 2 * m)[:2]:
        c.drawString(x, y - 7, line)
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
            draw_card(c, x0, y0, d)
    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    for lang in LANGS:
        draw(lang)
