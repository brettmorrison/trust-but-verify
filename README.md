# The Trust But Verify Project

Free, plain-language material to help older adults avoid scams — in 45 languages.

**Live site:** https://trustbutverifyproject.org

Everything here is free to print, copy, translate, adapt, rebrand, and hand out.
You do not need permission. Licensed CC BY — the one condition is a credit
line somewhere reasonable ("Adapted from the Trust But Verify Project,
trustbutverifyproject.org"). A sentence from this repository ending up on
somebody's refrigerator, with that one line of credit, is the project
working as intended.

---

## The whole idea

You don't have to become a suspicious person. You add **one step** before money
or access moves:

1. **Look up the number yourself.**
2. **Call the person yourself.**
3. **Wait a day.**

Every page, sheet, card, and script here is that same method applied to a
specific situation.

---

## What's in here

```
content/          Markdown source — the site is generated from this
  en/             English: 51 pages (scam types, question pages, action pages)
  es/ vi/ zh/ ru/ The 4 languages with full-length translated content
  and 40 more     A landing page in each remaining language
assets/
  photos/web/     Licensed, attributed photos used on some pages (see manifest.json)
build/            Generators (Python + one Node script)
functions/        Cloudflare Pages Function backing the /feedback form
formats/
  print/          91 print-ready PDFs — fridge sheets and wallet cards, all 45 languages
  og/             Social share-card PNGs, one per page
  talk/           25-minute slide deck, family-talk deck, and speaker script
  spoken/         60-second, 5-minute, and volunteer Q&A scripts
  outreach/       Ready-to-send texts and emails
  docx/           Source for the front-desk handout — emailed on request, not
                  published as a download (an editable file with this project's
                  name on it is easy to alter and pass off as official)
site/             Generated output (not committed — Cloudflare builds it)
```

Start with **00-CONTENT-PLAN.md** for the editorial rules and page inventory,
and **TRANSLATIONS.md** for what has and hasn't been validated.

---

## Building it

```bash
pip install -r requirements.txt
python3 build/build_site.py          # markdown -> site/
```

That's the whole toolchain. No framework, no bundler, no JavaScript.

Regenerating the printed material and photos needs more (WeasyPrint or
reportlab with real Unicode fonts, macOS system fonts, Node), so those
outputs are committed rather than built in CI:

```bash
python3 build/make_fridge.py             # fridge sheets, original language batch
python3 build/make_fridge_new_langs.py   # fridge sheets, later languages
python3 build/make_cards.py              # wallet cards, original language batch
python3 build/make_cards_new_langs.py    # wallet cards, later languages
python3 build/add_qr_codes.py            # stamps QR codes onto the fridge sheets
python3 build/make_infographic.py        # the one-page stats infographic
python3 build/make_share_cards.py        # og:image social cards, one per page
node    build/make_deck.js               # the volunteer talk deck
node    build/deck-family/make_deck.js   # the family-member talk deck
```

---

## Deployment

Cloudflare Pages, connected to this repository.

- **Build command:** `pip install -r requirements.txt && python3 build/build_site.py`
- **Output directory:** `site`

Push to `main` and it publishes. See **DEPLOY.md**.

---

## Design constraints

These aren't preferences. They're what the material is for.

- **No JavaScript anywhere.** The Content-Security-Policy blocks all scripts,
  which is only possible because the site genuinely has none.
- **No cookies, no accounts, no personal data collected or stored.**
  Cloudflare's cookie-free Web Analytics counts anonymous pageviews only, and
  the feedback form at `/feedback` forwards submissions by email without
  storing them anywhere — nothing sold, nothing shared, nothing kept beyond
  what's needed to answer you. A site about not letting people take your
  information should still say plainly what little it keeps.
- **20px minimum type on screen, 18pt in print.** Non-negotiable.
- **Sixth-grade reading level** — not because readers are simple, but because
  frightened people read at a lower level than calm people.
- **No shame, anywhere.** Shame is why this crime goes unreported, which makes
  shame a co-conspirator.
- **Every page ends on the reader's capability**, never on the threat. A page
  that ends on fear produces a frightened reader, and frightened people are
  exactly what these operations are built to sell.
- **Federal sources only** for statistics — FBI IC3 and FTC — with the year
  named.

---

## Translations

**Nothing non-English is treated as validated until a native speaker has read it
and that's been confirmed.** Until then it carries a warning band, in its own
language, saying so.

We need readers. One or two hours per language, no professional qualification —
the best qualification is being the person in your family who translated at the
doctor's office growing up.

**translations@trustbutverifyproject.org** · see `TRANSLATIONS.md`

---

## Maintenance

**Every April**, when the FBI's Internet Crime Complaint Center publishes its
annual report, update the statistics. Search `content/` for the year to find
every instance.

When an English page changes, its translations become stale — put the warning
band back until someone re-reads them.

---

## Contributing

Corrections are welcome, especially:

- Anything factually wrong or out of date
- Translation fixes (see above — this is the biggest need)
- Accessibility problems, particularly with screen readers
- Scams that reach your community and aren't covered here

Statistics must cite FBI IC3 or FTC, with the year.

---

## License

Creative Commons Attribution 4.0 (CC BY). Take it, change it, put your own
name on it — just keep a credit line back to the Trust But Verify Project.
