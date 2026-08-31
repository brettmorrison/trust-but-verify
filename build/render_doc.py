#!/usr/bin/env python3
"""Render a docs/*.md deliverable to its .html twin.

Every substantial document in docs/ is expected to exist as both a .md (for
other sessions and tools to parse) and a .html (for reading). Keeping the pair
in sync by hand drifts, so this does it: `python3 build/render_doc.py <file.md>`
writes the sibling .html.

Deliberately not a general Markdown implementation. It handles exactly the
constructs these documents use, and it is theme-aware because the pages get
read on a phone at night as often as on a desktop.
"""
import io, os, re, sys, html

def _inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", s)
    return s

def render_body(src):
    lines, out, i = src.split("\n"), [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            out.append("<table>" + "".join(
                "<tr>" + "".join("<td>" + _inline(c) + "</td>" for c in r) + "</tr>"
                for r in rows) + "</table>")
            continue
        if l.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip()); i += 1
            out.append("<blockquote>" + _inline(" ".join(buf)) + "</blockquote>")
            continue
        if l.startswith("- "):
            buf = []
            while i < len(lines) and (lines[i].startswith("- ") or
                                      (lines[i].startswith("  ") and lines[i].strip() and buf)):
                if lines[i].startswith("- "):
                    buf.append(lines[i][2:].strip())
                else:
                    buf[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join("<li>" + _inline(x) + "</li>" for x in buf) + "</ul>")
            continue
        m = re.match(r"^(#{1,3}) (.*)", l)
        if m:
            n = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (n, _inline(m.group(2)), n)); i += 1; continue
        if l.strip() == "---":
            out.append("<hr>"); i += 1; continue
        if not l.strip():
            i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|- |---)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        p = _inline(" ".join(buf))
        # A ranked recommendation gets its own card so the list is skimmable.
        cls = ' class="rec"' if re.match(r"^<strong>\d", p) else ""
        out.append("<p%s>%s</p>" % (cls, p))
    body = "\n".join(out)
    return body.replace("FLAGGED FOR BRETT",
                        "<span class='flag'>FLAGGED FOR BRETT</span>")

STYLE = """<style>
:root{--bg:#fffdf9;--fg:#141414;--mut:#5c5c5c;--rule:#d9d4c6;--card:#fff;--accent:#123f7a;--warn:#8a5a00;--warnbg:#fdf3dd}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15140f;--fg:#f2efe6;--mut:#a9a396;--rule:#3a382f;--card:#1d1b16;--accent:#9ec1f0;--warn:#f0c96b;--warnbg:#332812}}
:root[data-theme="dark"]{--bg:#15140f;--fg:#f2efe6;--mut:#a9a396;--rule:#3a382f;--card:#1d1b16;--accent:#9ec1f0;--warn:#f0c96b;--warnbg:#332812}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;padding:1.15rem;font:17px/1.6 Georgia,'Iowan Old Style',serif;-webkit-text-size-adjust:100%}
main{max-width:44rem;margin:0 auto}
h1{font-size:1.55rem;line-height:1.22;margin:0 0 1rem}
h2{font-size:1.16rem;font-family:system-ui,sans-serif;margin:2.2rem 0 .8rem;padding-bottom:.32rem;border-bottom:2px solid var(--rule)}
h3{font-size:1rem;font-family:system-ui,sans-serif;margin:1.7rem 0 .6rem;color:var(--accent)}
p{margin:0 0 .85rem}
hr{border:0;border-top:1px solid var(--rule);margin:2rem 0}
table{width:100%;border-collapse:collapse;margin:0 0 1.1rem;font:15px/1.45 system-ui,sans-serif;display:block;overflow-x:auto}
td{border-bottom:1px solid var(--rule);padding:.42rem .5rem;vertical-align:top}
tr td:last-child{text-align:right;color:var(--mut)}
tr td:last-child strong{color:var(--fg)}
blockquote{margin:1.1rem 0;padding:.7rem .9rem;background:var(--warnbg);border-left:4px solid var(--warn);border-radius:0 5px 5px 0;font-size:.95rem}
.flag{font:700 .74rem/1 system-ui,sans-serif;letter-spacing:.05em;color:var(--warn)}
ul{padding-left:1.15rem;margin:0 0 1rem}li{margin:.45rem 0}
a{color:var(--accent)}
code{font:.85em ui-monospace,Menlo,monospace;background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:.06em .32em}
p.rec{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--accent);border-radius:0 6px 6px 0;padding:.7rem .9rem;margin:0 0 .55rem}
em{color:var(--mut)}
</style>"""

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".md"):
        sys.exit("usage: render_doc.py <docs/file.md>")
    src_path = sys.argv[1]
    src = io.open(src_path, encoding="utf-8").read()
    m = re.search(r"^# (.*)", src, re.M)
    title = re.sub(r"[*`]", "", m.group(1)) if m else os.path.basename(src_path)
    out_path = src_path[:-3] + ".html"
    io.open(out_path, "w", encoding="utf-8").write(
        "<title>%s</title>\n%s\n<main>%s</main>\n"
        % (html.escape(title), STYLE, render_body(src)))
    print("wrote %s" % out_path)

if __name__ == "__main__":
    main()
