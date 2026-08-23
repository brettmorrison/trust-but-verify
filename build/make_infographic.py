#!/usr/bin/env python3
"""
One-page "by the numbers" infographic — English only for now.

More visual than the fridge sheet on purpose: a big headline stat, a bar
comparison of where the money actually goes, then the same three-step method
everything else on this site teaches. Sources: FBI IC3 2025 Internet Crime
Report (ic3.gov) and FTC Protecting Older Consumers 2024-2025 (ftc.gov).

    python3 build/make_infographic.py
"""
import os, io
import qrcode
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "formats", "print", "infographic-en.pdf")

INK = HexColor("#111111")
MUTED = HexColor("#4a4a4a")
PAPER = HexColor("#fffdf9")
ACCENT = HexColor("#123f7a")
BAND = HexColor("#f0ece4")

W, H = 612, 792
M = 42  # page margin


def wrap(c, text, x, y, font, size, max_w, leading, color=INK, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, font, size) > max_w and line:
            _draw_line(c, line, x, y, font, size, max_w, align)
            y -= leading
            line = word
        else:
            line = test
    if line:
        _draw_line(c, line, x, y, font, size, max_w, align)
        y -= leading
    return y


def _draw_line(c, line, x, y, font, size, max_w, align):
    if align == "center":
        c.drawCentredString(x + max_w / 2, y, line)
    else:
        c.drawString(x, y, line)


def qr_image(url):
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#123f7a", back_color="#fffdf9")
    path = OUT + ".qr.png"
    img.save(path)
    return path


def bar(c, x, y, w, h, frac, label, amount, color=ACCENT):
    c.setFillColor(BAND)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(color)
    c.rect(x, y, w * frac, h, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    c.drawString(x, y + h + 5, label)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(x + w, y + h + 5, amount)


def draw():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # header
    y = H - M
    c.setFillColor(ACCENT)
    c.setLineWidth(2)
    # magnifying glass + checkmark, matching the site logo:
    # "look it up yourself" (glass), "it checks out" (check)
    sx, sy, sr = M + 8, y - 20, 7
    c.setLineWidth(2.3)
    c.circle(sx, sy, sr, fill=0, stroke=1)
    p = c.beginPath()
    p.moveTo(sx - 2.5, sy + 0)
    p.lineTo(sx - 0.8, sy - 1.7)
    p.lineTo(sx + 2.3, sy + 2.2)
    c.drawPath(p, fill=0, stroke=1)
    c.line(sx + sr * 0.72, sy - sr * 0.72, sx + sr * 1.55, sy - sr * 1.55)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(INK)
    c.drawString(M + 28, y - 26, "TRUST BUT VERIFY")
    y -= 44
    c.setStrokeColor(INK)
    c.setLineWidth(3)
    c.line(M, y, W - M, y)
    y -= 8
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(M, y - 10, "Elder fraud, by the numbers — and the one habit that stops most of it")
    y -= 34

    # headline stat
    c.setFont("Helvetica-Bold", 58)
    c.setFillColor(ACCENT)
    c.drawString(M, y - 50, "$7.7 BILLION")
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(M, y - 70, "lost by Americans 60+ to fraud in 2025 — a 59% jump in one year")
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    c.drawString(M, y - 84, "201,266 complaints filed. Average loss per victim: $38,500. FBI IC3, 2025.")
    y -= 112

    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(M, y, W - M, y)
    y -= 26

    # bar chart
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(M, y, "WHERE THE MONEY ACTUALLY GOES")
    y -= 26
    bw = W - 2 * M
    bh = 20
    bar(c, M, y - bh, bw, bh, 1.00, "Investment fraud (crypto, fake trading platforms)", "$3.52B")
    y -= bh + 34
    bar(c, M, y - bh, bw, bh, 0.153, "Recovery scams — stealing from people already scammed once", "$540M")
    y -= bh + 34
    bar(c, M, y - bh, bw, bh, 0.100, "Tech support scams (FTC, 2024)", "$159M")
    y -= bh + 34
    bar(c, M, y - bh, bw, bh, 0.0014, "Grandparent / distress scams, voice cloning", "$5M+")
    y -= bh + 26
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(MUTED)
    c.drawString(M, y, "Bar length shows relative size, not to scale below ~1%. FBI IC3 2025 Elder Fraud data; FTC 2024-2025 for tech support.")
    y -= 22

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 26

    # what's rising
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(M, y, "WHAT'S GROWING FASTEST")
    y -= 20
    rising = [
        ("Phishing / spoofing texts and emails, age 60+", "up over 100%"),
        ("Government impersonation calls", "nearly doubled"),
        ("Romance scams targeting older adults", "up 30%"),
        ("Scams referencing or using AI voice cloning", "3,100+ complaints, $352M+ lost"),
    ]
    c.setFont("Helvetica", 10.5)
    for label, stat in rising:
        c.setFillColor(INK)
        c.drawString(M + 12, y, "•  " + label)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(ACCENT)
        c.drawRightString(W - M, y, stat)
        c.setFont("Helvetica", 10.5)
        y -= 17
    y -= 12

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 26

    # the method
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(M, y, "THE ONE HABIT THAT STOPS MOST OF THIS")
    y -= 24
    steps = [
        ("1", "Look up the number yourself.", "Not the one they gave you."),
        ("2", "Call the person yourself.", "Hang up first. If it was real, they'll still be there."),
        ("3", "Wait a day.", "Real problems survive a night's sleep. Scams don't."),
    ]
    step_w = (W - 2 * M - 24) / 3
    for i, (num, head, sub) in enumerate(steps):
        x = M + i * (step_w + 12)
        c.setFont("Helvetica-Bold", 26)
        c.setFillColor(ACCENT)
        c.drawString(x, y, num)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(INK)
        yy = wrap(c, head, x, y - 20, "Helvetica-Bold", 10.5, step_w, 13)
        wrap(c, sub, x, yy - 2, "Helvetica", 8.5, step_w, 11, color=MUTED)
    y -= 78

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 22

    # footer: hotlines + QR
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    c.drawString(M, y, "FREE HELP — NO JUDGMENT")
    y -= 15
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "833-372-8311")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(M + 92, y + 1, "National Elder Fraud Hotline")
    y -= 16
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(M, y, "877-908-3360")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(M + 92, y + 1, "AARP Fraud Watch")
    y -= 16
    c.setFont("Helvetica", 8.5)
    c.drawString(M, y, "Report at ic3.gov and reportfraud.ftc.gov  ·  Sources: FBI IC3 2025 Internet Crime Report, FTC Protecting Older Consumers 2024-2025")

    qr_path = qr_image("https://trustbutverifyproject.org")
    qr_size = 62
    c.drawImage(qr_path, W - M - qr_size, M - 4, width=qr_size, height=qr_size,
                preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, M - 12, "trustbutverifyproject.org")

    c.showPage()
    c.save()
    os.remove(qr_path)
    print("wrote", OUT)


if __name__ == "__main__":
    draw()
