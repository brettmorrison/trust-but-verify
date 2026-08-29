#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static audit of the built site. Run after build/build_site.py.

Exists because two sitewide passes have now silently damaged this site in ways
that the build itself was happy with: an em-dash removal fused table rows and
took five languages' helpline guidance off the interpreter page, and new
content shipped with og:image tags pointing at share cards nobody generated.
build_site.py now guards those two specifically. This covers the wider surface
that nothing else looks at: accessibility attributes, metadata, internal links,
and page weight.

Exits non-zero if any ERROR check fails. WARN findings are reported and do not
fail the build, because they are judgement calls rather than defects.

    python3 build/audit_site.py [--strict]     # --strict makes WARN fail too
"""
import os, re, sys, glob, io, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
errors, warns = [], []

def err(cat, detail):  errors.append((cat, detail))
def warn(cat, detail): warns.append((cat, detail))

def pages():
    for f in sorted(glob.glob(os.path.join(OUT, "**", "index.html"), recursive=True)):
        yield f, io.open(f, encoding="utf-8").read()

def rel(f):
    return f.replace(OUT + os.sep, "").replace(os.sep + "index.html", "") or "/"

# ---------------------------------------------------------------- accessibility
def check_accessibility():
    for f, h in pages():
        p = rel(f)
        for img in re.findall(r"<img[^>]*>", h):
            if "alt=" not in img:
                err("img missing alt", "%s :: %s" % (p, img[:70]))
        if not re.search(r'<html lang="[a-zA-Z-]+"', h):
            err("missing lang on <html>", p)
        if h.count("<h1") == 0:
            err("no h1", p)
        elif h.count("<h1") > 1:
            err("multiple h1", p)
        levels = [int(m.group(1)) for m in re.finditer(r"<h([1-6])\b", h)]
        for a, b in zip(levels, levels[1:]):
            if b > a + 1:
                err("heading level skipped", "%s :: h%d -> h%d" % (p, a, b)); break
        for tag in re.findall(r"<(?:input|textarea|select)\b[^>]*>", h):
            if 'type="hidden"' in tag:
                continue
            m = re.search(r'id="([^"]+)"', tag)
            labelled = m and ('for="%s"' % m.group(1)) in h
            if not labelled and "aria-label" not in tag:
                err("form control without a label", "%s :: %s" % (p, tag[:60]))
        for a in re.findall(r"<a\b[^>]*>(.*?)</a>", h, re.S):
            if not re.sub(r"<[^>]+>", "", a).strip():
                err("link with no accessible text", p)
        # every page needs a skip link, whatever language it is written in
        if 'class="skip"' not in h:
            err("no skip link", p)

# ------------------------------------------------------------------- metadata
def check_metadata():
    for f, h in pages():
        p = rel(f)
        for pat, name in ((r"<title>(.*?)</title>", "title"),
                          (r'<meta name="description" content="(.*?)"', "meta description"),
                          (r'<link rel="canonical" href="(.*?)"', "canonical"),
                          (r'og:title" content="(.*?)"', "og:title"),
                          (r'og:image" content="(.*?)"', "og:image")):
            if not re.search(pat, h, re.S):
                err("missing " + name, p)
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        # length limits are search-result cosmetics, not defects
        if t and len(t.group(1)) > 70:
            warn("title over 70 chars", "%s (%d)" % (p, len(t.group(1))))
        if d and len(d.group(1)) > 200:
            warn("description over 200 chars", "%s (%d)" % (p, len(d.group(1))))

# ---------------------------------------------------------------------- links
def check_links():
    for f, h in pages():
        p, d = rel(f), os.path.dirname(f)
        for href in sorted(set(re.findall(r'href="([^"#?]+)"', h))):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            t = os.path.normpath(os.path.join(d, href))
            if os.path.isdir(t):
                t = os.path.join(t, "index.html")
            elif not os.path.splitext(t)[1]:
                t = os.path.join(t, "index.html")
            if not os.path.exists(t):
                err("broken internal link", "%s -> %s" % (p, href))
        for src in sorted(set(re.findall(r'src="([^"?]+)"', h))):
            if src.startswith(("http://", "https://", "data:")):
                continue
            t = os.path.normpath(os.path.join(d, src))
            if not os.path.exists(t):
                err("broken asset reference", "%s -> %s" % (p, src))

# --------------------------------------------------------------------- weight
def check_weight():
    # a page whose images dwarf its text costs the reader real money on a
    # metered mobile connection, which is a large slice of this audience
    for img in glob.glob(os.path.join(OUT, "photos", "*")):
        kb = os.path.getsize(img) / 1024.0
        if kb > 250:
            warn("image over 250 KB", "%s (%.0f KB)" % (os.path.basename(img), kb))
    for f, h in pages():
        kb = os.path.getsize(f) / 1024.0
        if kb > 100:
            warn("html page over 100 KB", "%s (%.0f KB)" % (rel(f), kb))

# ------------------------------------------------------- focus indicator regression
def check_focus_styles():
    css_path = os.path.join(OUT, "style.css")
    if not os.path.exists(css_path):
        err("stylesheet missing", "site/style.css"); return
    css = io.open(css_path, encoding="utf-8").read()
    # regression guard: a focusable control must never be left with its outline
    # removed and nothing put back. This shipped once on the feedback form.
    for m in re.finditer(r"([^{}]*):focus(?:-visible)?\s*\{([^}]*)\}", css):
        sel, body = m.group(1).strip(), m.group(2)
        if not re.search(r"outline\s*:\s*(none|0)\b", body):
            continue
        # A box-shadow ring is a legitimate substitute for an outline.
        # A border-colour swap is NOT accepted here on purpose: that is exactly
        # what shipped on the feedback form, where the swap measured 1.81:1
        # against the resting border and was effectively invisible. If a border
        # really is the intended indicator, prove the contrast and note it.
        if "box-shadow" in body:
            continue
        err("focus rule removes the outline without a box-shadow replacement", sel[:70])

def main():
    strict = "--strict" in sys.argv
    for fn in (check_accessibility, check_metadata, check_links, check_weight, check_focus_styles):
        fn()
    n = len(list(pages()))
    print("audited %d pages in %s" % (n, OUT))
    for label, items in (("ERROR", errors), ("WARN", warns)):
        if not items:
            print("  %s: none" % label); continue
        grouped = collections.OrderedDict()
        for cat, detail in items:
            grouped.setdefault(cat, []).append(detail)
        print("  %s: %d" % (label, len(items)))
        for cat, ds in grouped.items():
            print("    %-46s %d" % (cat, len(ds)))
            for d in ds[:4]:
                print("        " + d[:110])
            if len(ds) > 4:
                print("        ... and %d more" % (len(ds) - 4))
    if errors or (strict and warns):
        raise SystemExit(1)
    print("PASS")

if __name__ == "__main__":
    main()
