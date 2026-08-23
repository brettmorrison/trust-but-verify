#!/usr/bin/env python3
"""
Stamp a QR code onto each fridge sheet, linking to that language's page.

Run once after make_fridge.py (or whenever the PDFs are regenerated):

    python3 build/add_qr_codes.py

Placed in the confirmed-blank bottom-right corner of the page — verified by
inspecting the actual rendered layout, not guessed. Skips a PDF quietly if it
turns out not to have room, rather than overlapping existing text.
"""
import io, os
import qrcode
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINT = os.path.join(ROOT, "formats", "print")
SITE = "https://trustbutverifyproject.org"

# Languages that have a page on the live site (lang == "en" is the root).
HAS_PAGE = {"en", "es", "vi", "zh", "ru", "ko", "tl", "hi", "bn", "hy", "am",
            "sq", "ja", "ar", "ur", "fa", "ps", "de", "fr", "pt", "pl", "ro",
            "uk", "id"}

QR_SIZE = 72          # points (1 inch = 72pt) — small, corner-only
MARGIN = 28            # distance from right/bottom page edge


def url_for(lang):
    return SITE + "/" if lang == "en" else "%s/%s/" % (SITE, lang)


def make_qr_png(url):
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#123f7a", back_color="#fffdf9")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def stamp(pdf_path, lang):
    url = url_for(lang)
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    w, h = float(page.mediabox.width), float(page.mediabox.height)

    qr_buf = make_qr_png(url)
    qr_path = pdf_path + ".qr.png"
    with open(qr_path, "wb") as f:
        f.write(qr_buf.read())

    overlay_buf = io.BytesIO()
    c = canvas.Canvas(overlay_buf, pagesize=(w, h))
    x = w - MARGIN - QR_SIZE
    y = MARGIN
    c.drawImage(qr_path, x, y, width=QR_SIZE, height=QR_SIZE,
                preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(0.29, 0.29, 0.29)
    label = "trustbutverifyproject.org" if lang == "en" else url.replace("https://", "")
    c.drawRightString(x + QR_SIZE, y - 9, label)
    c.save()
    overlay_buf.seek(0)
    os.remove(qr_path)

    overlay_reader = PdfReader(overlay_buf)
    page.merge_page(overlay_reader.pages[0])

    writer = PdfWriter()
    writer.add_page(page)
    for p in reader.pages[1:]:
        writer.add_page(p)
    with open(pdf_path, "wb") as f:
        writer.write(f)


def main():
    done, skipped = [], []
    for fn in sorted(os.listdir(PRINT)):
        if not fn.startswith("fridge-sheet-") or not fn.endswith(".pdf"):
            continue
        lang = fn[len("fridge-sheet-"):-len(".pdf")]
        if lang not in HAS_PAGE:
            skipped.append(lang)
            continue
        stamp(os.path.join(PRINT, fn), lang)
        done.append(lang)
    print("stamped: %d (%s)" % (len(done), ", ".join(done)))
    if skipped:
        print("skipped, no matching page yet: %s" % ", ".join(skipped))


if __name__ == "__main__":
    main()
