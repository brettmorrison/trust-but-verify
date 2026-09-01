#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate assets/photos/web/ from assets/photos/source/.

The web copies are committed (source/ is 150 MB and gitignored), so this
script is how they get made rather than something anyone should do by hand.

Sizing. The content column is --measure, 34rem, so 544 px. A hero renders at
100% of that on desktop and at roughly 343 px on a 375 px phone. 1200 px
therefore covers 2x on desktop and better than 3x on a phone, with headroom.
The previous files were 1600 px, which mostly bought nothing: a 304 KB
photograph was the entire weight of the charity-scams page, and this audience
is disproportionately on metered mobile connections.

Quality 82 with 4:2:0 chroma subsampling is the usual sweet spot for
photographic content at this size. progressive=True so the image paints in
passes rather than top to bottom on a slow link.
"""
import os, sys, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "photos", "source")
WEB = os.path.join(ROOT, "assets", "photos", "web")
MAX_W = 1200
QUALITY = 82

def main():
    if not os.path.isdir(SRC):
        print("no assets/photos/source/ here (it is gitignored); nothing to do")
        return 0
    os.makedirs(WEB, exist_ok=True)
    before = after = 0
    rows = []
    for src in sorted(glob.glob(os.path.join(SRC, "*.jpg")) + glob.glob(os.path.join(SRC, "*.jpeg"))):
        name = os.path.splitext(os.path.basename(src))[0] + ".jpg"
        dst = os.path.join(WEB, name)
        old_kb = os.path.getsize(dst) / 1024.0 if os.path.exists(dst) else 0.0
        im = Image.open(src)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=QUALITY, optimize=True,
                progressive=True, subsampling="4:2:0")
        new_kb = os.path.getsize(dst) / 1024.0
        before += old_kb; after += new_kb
        rows.append((old_kb, new_kb, im.width, im.height, name))
    rows.sort(key=lambda r: -r[0])
    print("%-38s %9s %9s %10s" % ("photo", "before", "after", "size"))
    for o, n, w, h, name in rows:
        print("%-38s %7.0f KB %7.0f KB  %sx%s" % (name[:38], o, n, w, h))
    saved = before - after
    print("-" * 70)
    print("%-38s %7.0f KB %7.0f KB   saved %.0f KB (%.0f%%)"
          % ("TOTAL (%d photos)" % len(rows), before, after, saved,
             100.0 * saved / before if before else 0))
    return 0

if __name__ == "__main__":
    sys.exit(main())
