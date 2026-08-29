#!/usr/bin/env python3
"""
Generate content/en/validation-status.md -- a public, honest table of which
languages have been checked by a native speaker and which haven't.

WHY THIS IS A PAGE AND NOT JUST AN INTERNAL REPORT: the site's single
biggest gap is that nothing in 45 languages has been validated by a native
speaker, and every translated page says so in its own banner. A generic
"please help us translate" appeal converts poorly. A visible scoreboard --
"Korean: checked by a volunteer. Vietnamese: still waiting." -- converts
better, because it shows a specific unmet need rather than an abstract one,
and it publicly credits the people who did help.

It is also the honest thing to do. This site asks readers to verify claims
before trusting them; publishing exactly how far its own translations have
been checked is the same standard applied to itself.

Reads the `validated_by` frontmatter field that already exists on every
translated page (written by make_lang_pages.py as "(none yet)"), so there's
no separate state to maintain -- validating a page is just editing that one
field, and this page updates itself on the next build.

    python3 build/validation_report.py

Run it before build_site.py whenever validation status changes.
"""
import os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT_MD = os.path.join(CONTENT, "en", "validation-status.md")
UNVALIDATED = "(none yet)"

# Mirrors LANGS in build_site.py -- code -> display label. Kept as a small
# local copy rather than importing build_site, which would run its whole
# module-level setup just to read one list.
LANG_LABELS = {}


def load_lang_labels():
    text = open(os.path.join(ROOT, "build", "build_site.py"), encoding="utf-8").read()
    m = re.search(r"^LANGS = \[(.*?)^\]", text, re.S | re.M)
    if not m:
        raise SystemExit("Could not find LANGS in build_site.py")
    for code, _short, label in re.findall(r'\("(\w+)",\s*"([^"]*)",\s*"([^"]*)"\)', m.group(1)):
        LANG_LABELS[code] = label


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


def scan():
    per_lang = collections.defaultdict(lambda: {"total": 0, "validated": 0, "validators": set()})
    for dirpath, _dirs, files in os.walk(CONTENT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            meta = split_front_matter(open(path, encoding="utf-8").read())
            lang = meta.get("lang", "en")
            if lang == "en":
                continue
            rec = per_lang[lang]
            rec["total"] += 1
            who = meta.get("validated_by", "").strip()
            if who and who != UNVALIDATED:
                rec["validated"] += 1
                rec["validators"].add(who)
    return per_lang


def render(per_lang):
    total_pages = sum(r["total"] for r in per_lang.values())
    total_validated = sum(r["validated"] for r in per_lang.values())

    lines = [
        "---",
        "title: Which translations have been checked",
        "slug: /validation-status",
        "description: Every non-English page on this site was translated by AI. This is exactly how much of it a native speaker has checked so far, language by language.",
        "lang: en",
        "---",
        "",
        "# Which translations have been checked",
        "",
        "This site asks you to verify things before trusting them. It would be",
        "strange not to hold itself to that, so here is exactly where its own",
        "translations stand.",
        "",
        "**Every non-English page here was translated by AI.** A page counts as",
        "checked only when a person who speaks the language every day has read it",
        "and told us it's right. Until then it carries a warning at the top, in",
        "that language, and it shouldn't be printed or handed out.",
        "",
    ]

    if total_validated == 0:
        lines += [
            "**Right now, none of it has been checked yet** — %d pages across %d "
            "languages, all still waiting for a first reader." % (total_pages, len(per_lang)),
            "",
            "That's not a comfortable thing to publish, and it's the honest",
            "number. If you speak one of these languages, an hour of your time",
            "changes it.",
            "",
        ]
    else:
        lines += [
            "So far **%d of %d pages** have been checked, across %d languages."
            % (total_validated, total_pages, len(per_lang)),
            "",
        ]

    lines += [
        "[How to help check a language](/help-translate)",
        "",
        "---",
        "",
        "## Language by language",
        "",
        "| Language | Pages | Checked | Checked by |",
        "|---|---|---|---|",
    ]

    def sort_key(item):
        code, rec = item
        # Most-complete first, then most pages, then alphabetical -- puts
        # real progress at the top where it reads as momentum.
        return (-rec["validated"], -rec["total"], LANG_LABELS.get(code, code))

    for code, rec in sorted(per_lang.items(), key=sort_key):
        label = LANG_LABELS.get(code, code)
        if rec["validated"] == 0:
            checked = "Not yet"
            who = "*Nobody yet — [this could be you](/help-translate)*"
        elif rec["validated"] == rec["total"]:
            checked = "All %d" % rec["total"]
            who = ", ".join(sorted(rec["validators"]))
        else:
            checked = "%d of %d" % (rec["validated"], rec["total"])
            who = ", ".join(sorted(rec["validators"]))
        lines.append("| [%s](/%s/) | %d | %s | %s |" % (label, code, rec["total"], checked, who))

    lines += [
        "",
        "---",
        "",
        "## What checking actually involves",
        "",
        "Not a professional translation, and not a certification. One person who",
        "speaks the language every day, reading the pages and telling us what's",
        "wrong — what sounds machine-made, what sounds condescending, what words",
        "their community wouldn't use.",
        "",
        "Most languages here have a single core page, about 2,000 words, which is",
        "an hour or two. A few have more.",
        "",
        "[The full explanation, and how to reach us](/help-translate)",
        "",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    load_lang_labels()
    per_lang = scan()
    open(OUT_MD, "w", encoding="utf-8").write(render(per_lang))
    total = sum(r["total"] for r in per_lang.values())
    validated = sum(r["validated"] for r in per_lang.values())
    print("wrote %s (%d/%d pages validated across %d languages)"
          % (os.path.relpath(OUT_MD, ROOT), validated, total, len(per_lang)))
