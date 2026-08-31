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
import os, re, sys, glob, io, json, collections

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


# ------------------------------------------------------- English prose regression
# Two sitewide writing standards are easy to state and easy to lose:
# no em dashes in English copy, and prose that sounds like a person rather
# than a form letter. Both have already regressed once. The em-dash pass
# removed 614 of them and three came back in files written afterwards,
# because nothing was watching.
#
# Neither check can simply fail on any occurrence: main already carries 47
# em dashes, 45 of which are one repeated table cell on /validation-status,
# and one page is measurably stiff today. So both work as a ratchet against
# build/prose_baseline.json: the current state is recorded, anything worse
# than the record fails, and anything better is reported so the record can
# be tightened. The baseline can only move in the direction of less slop.

PROSE_BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "prose_baseline.json")
CONTRACTION_FLOOR_RATIO = 0.35   # of the site's own live median

def _prose_only(text):
    """Body text with front matter and table rows removed.

    Table rows are excluded because a page that is mostly tabular data
    (/resources-by-language is a helpline table) has no prose rhythm to
    measure, and counting its cells as sentences produces a false stiffness
    reading."""
    body = re.sub(r"^---.*?^---", "", text, flags=re.S | re.M)
    return "\n".join(l for l in body.split("\n") if not l.strip().startswith("|"))

def _english_sources():
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "en", "**", "*.md"),
                              recursive=True)):
        yield os.path.relpath(f, ROOT), io.open(f, encoding="utf-8").read()

def _load_baseline():
    if not os.path.exists(PROSE_BASELINE):
        return {"em_dashes": {}, "stiff_pages": {}}
    return json.load(io.open(PROSE_BASELINE, encoding="utf-8"))

def check_prose_regressions():
    base = _load_baseline()
    em_base = base.get("em_dashes", {})
    stiff_base = base.get("stiff_pages", {})

    rates, counts = {}, {}
    for rel, text in _english_sources():
        counts[rel] = text.count("\u2014") + text.count("\u2013")
        body = _prose_only(text)
        words = len(body.split())
        if words >= 250:
            con = len(re.findall(r"\b\w+['\u2019](?:s|t|re|ll|ve|d|m)\b", body))
            rates[rel] = round(con * 1000.0 / words, 1)

    # 1. em dashes: never more than the recorded number, never in a new file
    for rel, n in sorted(counts.items()):
        alw = em_base.get(rel)
        if n == 0 and alw is None:
            continue   # clean file, nothing recorded: the normal case
        if alw is None:
            err("em dash in English copy, not in the baseline", "%s has %d" % (rel, n))
        elif n > alw:
            err("em dashes increased", "%s has %d, baseline allows %d" % (rel, n, alw))
        elif n < alw:
            warn("em dashes reduced, tighten the baseline",
                 "%s now %d, baseline still allows %d" % (rel, n, alw))

    # 2. contraction rate, measured against the site's own median so the bar
    #    moves with the writing rather than a number frozen in this file
    if rates:
        median = sorted(rates.values())[len(rates) // 2]
        floor = round(median * CONTRACTION_FLOOR_RATIO, 1)
        for rel, r in sorted(rates.items()):
            if r >= floor:
                if rel in stiff_base:
                    warn("page no longer stiff, drop it from the baseline",
                         "%s is %.1f per 1k, floor %.1f" % (rel, r, floor))
                continue
            allowed = stiff_base.get(rel)
            if allowed is None:
                err("English prose reads stiff (contractions far below site median)",
                    "%s at %.1f per 1k, floor %.1f, median %.1f" % (rel, r, floor, median))
            elif r < allowed - 0.05:
                err("English prose got stiffer",
                    "%s at %.1f per 1k, baseline recorded %.1f" % (rel, r, allowed))



# --------------------------------------------------- translated safety invariants
# Three properties of the 138 non-English pages are true today and nothing
# was enforcing any of them. They are cheap to keep and expensive to lose,
# because this is safety copy for people who cannot read the English original
# and so cannot notice when it is wrong.
#
#   1. Every phone number in a translation also appears in the English copy.
#      A helpline number that drifts during translation sends a frightened
#      person to a number nobody answers, or to somebody else entirely.
#   2. Every unvalidated page carries its in-language warning banner. That
#      banner is the only thing telling a reader no human has checked the page.
#   3. Every non-English page declares validated_by, so "checked" is a
#      recorded fact rather than an assumption.
#
# This is insurance on a currently-clean state, not a repair.

PHONE_RE = re.compile(r"\b(?:\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}-\d{4})\b")

def _content_files():
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "**", "*.md"),
                              recursive=True)):
        rel = os.path.relpath(f, ROOT)
        yield rel, rel.split(os.sep)[1], io.open(f, encoding="utf-8").read()

def _front_matter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm

def check_translation_safety():
    english, files = set(), []
    for rel, lang, text in _content_files():
        nums = set(PHONE_RE.findall(text.replace(".", "-")))
        if lang == "en":
            english |= nums
        else:
            files.append((rel, nums, _front_matter(text)))

    if not english:
        err("no English phone numbers found", "the subset check cannot run")
        return

    for rel, nums, fm in files:
        stray = sorted(nums - english)
        if stray:
            err("phone number in a translation that is not in the English copy",
                "%s has %s" % (rel, ", ".join(stray)))

        validator = fm.get("validated_by", "").strip()
        if not validator:
            err("non-English page does not declare validated_by", rel)
        elif validator.startswith("(none"):
            # Not yet checked by a human, so the reader must be told so.
            if "UNVALIDATED" not in fm.get("status", ""):
                err("unvalidated translation is missing its warning banner", rel)



# ------------------------------------------------------------------ hreflang
# hreflang is only valid if it is reciprocal: every page in a translation set
# must declare the whole set, itself included. A one-directional or incomplete
# set is worse than none, because search engines discard the lot and go back
# to treating 45 translations as duplicate pages competing with each other.
#
# This is easy to break silently. The tags are generated from the pages being
# built, so adding one translated page changes the correct answer for every
# other page in its set, and nothing on screen looks wrong when it goes bad.

def check_hreflang():
    declared, built = {}, set()
    for path, html in pages():
        url = "/" + os.path.relpath(os.path.dirname(path), OUT).strip("/")
        if url == "/.":
            url = "/"
        built.add(url)
        tags = re.findall(r'hreflang="([a-z-]+)" href="([^"]+)"', html)
        if tags:
            declared[url] = {c: u for c, u in tags if c != "x-default"}

    def to_path(href):
        # Absolute URLs; keep only the path so it can be matched against
        # what was actually built.
        return (re.sub(r"^https?://[^/]+", "", href).rstrip("/")) or "/"

    for url, langs in sorted(declared.items()):
        if not any(to_path(h) == url for h in langs.values()):
            err("hreflang set omits the page declaring it", url)
        for code, href in sorted(langs.items()):
            target = to_path(href)
            if target not in built:
                err("hreflang points at a page that does not exist",
                    "%s -> %s" % (url, href))
                continue
            other = declared.get(target)
            if other is None:
                err("hreflang target declares none of its own", "%s -> %s" % (url, target))
            elif set(other) != set(langs):
                err("hreflang sets disagree",
                    "%s and %s differ on %s"
                    % (url, target, ",".join(sorted(set(langs) ^ set(other)))))



# ------------------------------------------------------------ table semantics
# Two things a data table needs that markdown does not supply, both measured
# on the real rendered pages before being fixed:
#
#   scope on every header cell, so a screen reader can tie a value back to
#   its column. /resources-by-language is 45 rows of helpline and interpreter
#   data; without scope it reads as 45 rows of bare values.
#
#   tabindex on the scroll container, because a region that scrolls but
#   cannot be focused cannot be scrolled without a mouse. At 320px that
#   table is 491px wide in a 273px box, so about 45% of it was unreachable.

def check_table_semantics():
    for path, html in pages():
        for th in re.findall(r"<th\b[^>]*>", html):
            if "scope=" not in th:
                err("table header cell without scope", "%s: %s" % (rel(path), th))
        for div in re.findall(r'<div class="table-scroll"[^>]*>', html):
            if 'tabindex="0"' not in div:
                err("scrollable table container is not keyboard reachable", rel(path))


def main():
    strict = "--strict" in sys.argv
    for fn in (check_accessibility, check_metadata, check_links, check_weight,
               check_focus_styles, check_prose_regressions,
               check_translation_safety, check_hreflang,
               check_table_semantics):
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
