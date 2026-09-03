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
import os, re, sys, glob, io, json, bisect, collections
from html.parser import HTMLParser

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



# ----------------------------------------------------------- external links
# This site's usefulness rests on a handful of outside URLs staying alive:
# reportfraud.ftc.gov appears on 210 pages and ic3.gov on 204. If either
# moves, every reporting instruction on the site quietly points at nothing,
# and the people least able to recover from that are the ones following it.
#
# Off by default because it needs the network and takes a few seconds. Run
# it deliberately: python3 build/audit_site.py --links
#
# A redirect is reported rather than passed over. It usually means the
# canonical address has changed and the old one is living on borrowed time.
#
# Known limit, stated so nobody trusts this further than it goes: it cannot
# see a soft 404. reportfraud.ftc.gov answers 200 for a path that does not
# exist, so a broken deep link into that site would pass here. What this
# does catch is a dead domain, a DNS failure, a hard 4xx/5xx, and a moved
# address. That covers the realistic failure for the two URLs that matter.

def check_external_links():
    import urllib.request, urllib.error, ssl, collections

    urls = collections.Counter()
    for path, html in pages():
        for u in re.findall(r'href="(https?://[^"]+)"', html):
            if "trustbutverifyproject.org" not in u:
                urls[u] += 1

    ctx = ssl.create_default_context()
    for url, count in sorted(urls.items(), key=lambda kv: -kv[1]):
        req = urllib.request.Request(url, method="GET", headers={
            "User-Agent": "Mozilla/5.0 (compatible; trustbutverify-linkcheck)"})
        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                final = r.geturl()
                if r.status >= 400:
                    err("external link returns %d" % r.status,
                        "%s (on %d pages)" % (url, count))
                elif final.rstrip("/") != url.rstrip("/"):
                    warn("external link redirects",
                         "%s -> %s (on %d pages)" % (url, final, count))
        except urllib.error.HTTPError as e:
            err("external link returns %d" % e.code, "%s (on %d pages)" % (url, count))
        except Exception as e:
            err("external link unreachable",
                "%s (on %d pages): %s" % (url, count, type(e).__name__))



# --------------------------------------------------------------- CSS plumbing
# A small CSS reader shared by the two checks below. It descends into at-rules
# so a rule inside @media is seen with the media query it lives under, which
# is the whole point -- the two type-floor defects this catches were both
# inside a media query, where nothing reading the top level would find them.

def _strip_css_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)

def _css_rules(css, context=""):
    """Yield (selector, declarations, context) for every style rule."""
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            return
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if sel.startswith("@"):
            if "{" in body:
                for r in _css_rules(body, (context + " " + sel).strip()):
                    yield r
        elif sel:
            yield sel, body, context
        i = k

def _declarations(body):
    for decl in body.split(";"):
        if ":" in decl:
            prop, value = decl.split(":", 1)
            yield prop.strip().lower(), value.strip()

def _site_css():
    path = os.path.join(OUT, "style.css")
    if not os.path.exists(path):
        return None
    return _strip_css_comments(io.open(path, encoding="utf-8").read())


# ------------------------------------------------------------- the 20px floor
# README.md: "20px minimum type on screen. Non-negotiable." It was not being
# kept. Thirteen declarations sat under 1rem, and @media (max-width:26rem)
# dropped the root to 118% -- 18.88px -- so on a phone body copy landed at
# 19.8px and the interpreter table under 19px, below the floor on the exact
# device and page where it matters most.
#
# The floor is expressed as 1rem against a 125% root (= 20px), so this reads
# the generated CSS and fails on anything smaller. Two decorative exceptions
# are named, with a reason each, rather than left to judgement.
#
# Print is excluded: it is sized in pt against a 100% root deliberately, and
# the project's print standard is a separate number (18pt on the typeset
# sheets, ~13pt for a browser printout).

TYPE_FLOOR_ALLOWLIST = {
    "figure.hero-photo figcaption": "photo credit line, not reading matter",
    "aside.rail .label": "the rail's own heading, decorative chrome",
}
ROOT_FONT_FLOOR_PCT = 125.0

def _px_of(value):
    """font-size in px assuming a 20px root, or None if not a plain length."""
    m = re.match(r"^([\d.]+)(rem|em|px|pt|%)$", value.strip())
    if not m:
        return None
    n, unit = float(m.group(1)), m.group(2)
    return {"rem": n * 20.0, "em": n * 20.0, "px": n,
            "pt": n * 96.0 / 72.0, "%": n * 20.0 / 100.0}[unit]

def check_type_floor():
    css = _site_css()
    if css is None:
        err("stylesheet missing", "site/style.css"); return
    for sel, body, context in _css_rules(css):
        if "print" in context:
            continue
        for prop, value in _declarations(body):
            if prop != "font-size":
                continue
            norm = re.sub(r"\s+", " ", sel).strip()
            where = norm + ((" in " + context) if context else "")
            if norm in TYPE_FLOOR_ALLOWLIST:
                continue
            # The root percentage sets what 1rem is worth, so it is the one
            # value that has to be checked against 125% rather than 20px.
            if norm == "html":
                m = re.match(r"^([\d.]+)%$", value)
                if not m or float(m.group(1)) < ROOT_FONT_FLOOR_PCT:
                    err("root font-size below the 125% the 20px floor rests on",
                        "%s sets font-size:%s" % (where, value))
                continue
            px = _px_of(value)
            if px is None:
                continue
            if px < 20.0:
                err("font-size below the 20px floor",
                    "%s sets font-size:%s (%.1fpx at a 125%% root)"
                    % (where, value, px))


# ------------------------------------------------------- the printed page
# Browser printing is how this material reaches most of the people it is for:
# a volunteer prints a page and hands it over. The print stylesheet used to
# hide footer.site outright, which quietly removed the National Elder Fraud
# Hotline, AARP Fraud Watch, reportfraud.ftc.gov and ic3.gov from every
# printed page -- the four things the reader is meant to act on.
#
# So the rule is stated as an invariant rather than as a fix: nothing hidden
# in print may contain a phone number. PHONE_RE is the same expression the
# translation-safety check uses, so "a phone number" means the same thing in
# both places.
#
# It needs to know what a selector actually matches on the real pages, so
# there is a small DOM below. Anything more complicated than tag/class/id and
# descendant combinators is refused rather than guessed at, which keeps the
# print block simple enough to stay checkable.

_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
         "meta", "param", "source", "track", "wbr"}

class _Dom(HTMLParser):
    """Elements with their class/id, content span, and parent."""
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.line_starts, pos = [0], 0
        for line in text.split("\n"):
            pos += len(line) + 1
            self.line_starts.append(pos)
        self.nodes, self.stack = [], []
        self.feed(text)
        for i in self.stack:
            self.nodes[i]["end"] = len(text)

    def _offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def _open(self, tag, attrs, void):
        a = dict(attrs)
        start = self._offset() + len(self.get_starttag_text() or "")
        self.nodes.append({
            "tag": tag,
            "classes": set((a.get("class") or "").split()),
            "id": a.get("id"),
            "start": start,
            "end": start if void else None,
            "parent": self.stack[-1] if self.stack else None,
        })
        if not void:
            self.stack.append(len(self.nodes) - 1)

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, tag in _VOID)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs, True)

    def handle_endtag(self, tag):
        for depth in range(len(self.stack) - 1, -1, -1):
            if self.nodes[self.stack[depth]]["tag"] == tag:
                off = self._offset()
                for i in self.stack[depth:]:
                    if self.nodes[i]["end"] is None:
                        self.nodes[i]["end"] = off
                del self.stack[depth:]
                return

_COMPOUND = re.compile(r"^([a-zA-Z][\w-]*)?((?:[.#][\w-]+)+)?$")

def _parse_selector(sel):
    """[(tag, classes, id), ...] left to right, or None if unsupported."""
    parts = []
    for part in sel.split():
        m = _COMPOUND.match(part)
        if not m or not part:
            return None
        tag = (m.group(1) or "").lower() or None
        classes, ident = set(), None
        for token in re.findall(r"[.#][\w-]+", m.group(2) or ""):
            if token[0] == ".":
                classes.add(token[1:])
            else:
                ident = token[1:]
        parts.append((tag, classes, ident))
    return parts or None

def _matches(dom, node_index, parts):
    node = dom.nodes[node_index]
    def hit(part, n):
        tag, classes, ident = part
        return ((tag is None or n["tag"] == tag)
                and classes <= n["classes"]
                and (ident is None or n["id"] == ident))
    if not hit(parts[-1], node):
        return False
    remaining = list(parts[:-1])
    i = node["parent"]
    while remaining and i is not None:
        if hit(remaining[-1], dom.nodes[i]):
            remaining.pop()
        i = dom.nodes[i]["parent"]
    return not remaining

def check_print_stylesheet():
    css = _site_css()
    if css is None:
        err("stylesheet missing", "site/style.css"); return
    hidden, saw_print = [], False
    for sel, body, context in _css_rules(css):
        if "print" not in context:
            continue
        saw_print = True
        for prop, value in _declarations(body):
            if prop == "display" and value.lower() == "none":
                hidden.extend(s.strip() for s in sel.split(",") if s.strip())
    if not saw_print:
        err("no @media print block in the stylesheet",
            "printing is how most of this material reaches people"); return
    if not hidden:
        return

    parsed = {}
    for sel in hidden:
        parts = _parse_selector(re.sub(r"\s+", " ", sel))
        if parts is None:
            err("print rule hides a selector this check cannot evaluate",
                "%s -- keep print hiding to tag/class/id and descendants "
                "so it stays checkable" % sel)
            continue
        parsed[sel] = parts
    if not parsed:
        return

    reported = set()
    for f, h in pages():
        found = [(m.start(), m.group(0)) for m in PHONE_RE.finditer(h)]
        if not found:
            continue
        at = [pos for pos, _n in found]
        dom = _Dom(h)
        for i, node in enumerate(dom.nodes):
            if node["end"] is None or node["end"] <= node["start"]:
                continue
            j = bisect.bisect_left(at, node["start"])
            if j >= len(at) or at[j] >= node["end"]:
                continue
            for sel, parts in parsed.items():
                if sel in reported or not _matches(dom, i, parts):
                    continue
                reported.add(sel)
                err("print stylesheet hides a phone number",
                    "%s hides <%s> on %s, which contains %s"
                    % (sel, node["tag"], rel(f), found[j][1]))


# --------------------------------------------------------- _headers collisions
# Cloudflare Pages does not treat a more specific _headers rule as an override.
# Every rule whose pattern matches the request contributes its headers, and the
# browser receives all of them. For most headers that is merely confusing; for
# Content-Security-Policy it is a trap, because a browser given two policies
# enforces the intersection (CSP3 sec. 8.1) -- the strictest value of each
# directive wins no matter which rule looks more specific.
#
# That is exactly how the feedback form was dead from launch: /* set
# form-action 'none' and /feedback/* set form-action 'self', the live response
# carried two content-security-policy lines, and the intersection was 'none'.
# Pressing Send did nothing at all, with no JavaScript on the page to say why.
#
# So: expand every rule against every built path and fail if any path is
# matched by two rules that set the same header. Comparing patterns to each
# other would not have caught this on its own -- /* and /feedback/* overlap
# only once you know what was built.

def _parse_headers_file(text):
    """[(pattern, [(header-name, value), ...]), ...] from _headers syntax.

    Unindented non-comment lines are path patterns; indented "Name: value"
    lines belong to the pattern above them."""
    rules, current = [], None
    for raw in text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0].isspace():
            if current is not None and ":" in raw:
                name, value = raw.split(":", 1)
                current[1].append((name.strip(), value.strip()))
        else:
            current = (raw.strip(), [])
            rules.append(current)
    return rules

def _headers_pattern_re(pattern):
    """Cloudflare Pages matching: * is a wildcard, :name is one path segment."""
    path = re.sub(r"^https?://[^/]*", "", pattern) or "/"
    out = []
    for part in re.split(r"(\*|:[A-Za-z_][A-Za-z0-9_]*)", path):
        if part == "*":
            out.append(".*")
        elif part.startswith(":"):
            out.append("[^/]+")
        elif part:
            out.append(re.escape(part))
    return re.compile("^" + "".join(out) + "$")

def _built_paths():
    """Every file in site/ as the URL path a visitor would request."""
    for dirpath, _dirs, files in os.walk(OUT):
        for fn in files:
            if fn == "_headers":
                continue
            full = os.path.join(dirpath, fn)
            r = os.path.relpath(full, OUT).replace(os.sep, "/")
            if fn == "index.html":
                d = os.path.dirname(r)
                yield ("/" + d + "/") if d else "/"
            else:
                yield "/" + r

def check_header_collisions():
    hp = os.path.join(OUT, "_headers")
    if not os.path.exists(hp):
        err("_headers missing", "site/_headers"); return
    rules = _parse_headers_file(io.open(hp, encoding="utf-8").read())
    if not rules:
        err("_headers has no rules", "site/_headers"); return
    compiled = [(pat, _headers_pattern_re(pat), hdrs) for pat, hdrs in rules]

    seen = set()
    for path in _built_paths():
        setters = collections.defaultdict(list)
        for pat, rx, hdrs in compiled:
            if not rx.match(path):
                continue
            for name, _value in hdrs:
                setters[name.lower()].append(pat)
        for name, pats in sorted(setters.items()):
            if len(pats) < 2:
                continue
            key = (name, tuple(pats))
            if key in seen:
                continue
            seen.add(key)
            err("two _headers rules set the same header on one path",
                "%s gets %s from %s -- Pages appends both, it does not override"
                % (path, name, " and ".join(pats)))


# ------------------------------------------------------- canonical report URLs
# The two URLs the site's reporting instructions depend on must be written in
# the form that answers directly, not one that answers via a redirect.
#
# Six pages linked the bare https://ic3.gov, which 301s to www. It worked, but
# it made a reporting instruction depend on IC3 keeping a redirect alive, and
# the rest of the site already used the canonical form. A redirect that
# disappears takes six reporting instructions with it, in six languages, for
# readers with no way to notice the link is wrong.
#
# Checked in content/ rather than in the built HTML so the message can name the
# source file and line a person would actually edit.

CANONICAL_REPORT_URLS = {
    "https://ic3.gov": "https://www.ic3.gov",
    "http://ic3.gov": "https://www.ic3.gov",
    "http://www.ic3.gov": "https://www.ic3.gov",
    "http://reportfraud.ftc.gov": "https://reportfraud.ftc.gov",
}

def check_canonical_report_urls():
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "**", "*.md"),
                              recursive=True)):
        text = io.open(f, encoding="utf-8").read()
        for lineno, line in enumerate(text.split("\n"), 1):
            for bad, good in CANONICAL_REPORT_URLS.items():
                # Match the URL only where it ends, so https://ic3.gov does not
                # fire on https://ic3.gov.example and www. is not flagged by the
                # bare-domain rule.
                if re.search(re.escape(bad) + r"(?![\w.-])", line):
                    err("non-canonical reporting URL",
                        "%s:%d uses %s, should be %s"
                        % (os.path.relpath(f, ROOT), lineno, bad, good))


def main():
    strict = "--strict" in sys.argv
    checks = [check_accessibility, check_metadata, check_links, check_weight,
              check_focus_styles, check_prose_regressions,
              check_translation_safety, check_hreflang,
              check_table_semantics, check_type_floor,
              check_print_stylesheet, check_header_collisions,
              check_canonical_report_urls]
    if "--links" in sys.argv:
        checks.append(check_external_links)
    for fn in checks:
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
