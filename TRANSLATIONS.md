# Translation registry

**The rule: no non-English material is treated as trustworthy until a native
speaker has validated it and the project maintainer has confirmed that.**

Until then, every page, sheet, and card in that language carries a warning band
in its own language saying it is machine-translated and should not be printed or
distributed.

This file is the single source of truth for what has been checked.

---

## Status

| Language | Code | Web | Fridge sheet | Wallet card | Status | Validated by |
|---|---|---|---|---|---|---|
| English | `en` | full site | yes | yes | **VALIDATED** | |
| Spanish | `es` | full site | yes | yes | not yet | |
| Vietnamese | `vi` | full site | yes | yes | not yet | |
| Chinese (Simplified) | `zh` | full site | yes | yes | not yet | |
| Russian | `ru` | full site | yes | yes | not yet | |
| Korean | `ko` | landing page | yes | yes | not yet | |
| Tagalog | `tl` | landing page | yes | yes | not yet | |
| Hindi | `hi` | landing page | yes | yes | not yet | |
| Bengali | `bn` | landing page | yes | yes | not yet | |
| Armenian | `hy` | landing page | yes | yes | not yet | |
| Amharic | `am` | landing page | yes | yes | not yet | |
| Albanian | `sq` | landing page | yes | yes | not yet | |
| Japanese | `ja` | landing page | yes | yes | not yet | |
| Arabic | `ar` | landing page | yes | yes | not yet | |
| Urdu | `ur` | landing page | yes | yes | not yet | |
| Farsi | `fa` | landing page | yes | yes | not yet | |
| Pashto | `ps` | landing page | yes | yes | not yet | |
| German | `de` | landing page | yes | yes | not yet | |
| French | `fr` | landing page | yes | yes | not yet | |
| Portuguese | `pt` | landing page | yes | yes | not yet | |
| Polish | `pl` | landing page | yes | yes | not yet | |
| Romanian | `ro` | landing page | yes | yes | not yet | |
| Ukrainian | `uk` | landing page | yes | yes | not yet | |
| Indonesian | `id` | landing page | yes | yes | not yet | |
| Haitian Creole | `ht` | landing page | yes | yes | not yet | |
| Punjabi | `pa` | landing page | yes | yes | not yet | |
| Gujarati | `gu` | landing page | yes | yes | not yet | |
| Somali | `so` | landing page | yes | yes | not yet | |
| Khmer | `km` | landing page | yes | yes | not yet | |
| Hmong | `hmn` | landing page | yes | yes | not yet | |
| Georgian | `ka` | landing page | yes | yes | not yet | |
| Lithuanian | `lt` | landing page | yes | yes | not yet | |
| Latvian | `lv` | landing page | yes | yes | not yet | |
| Estonian | `et` | landing page | yes | yes | not yet | |
| Italian | `it` | landing page | yes | yes | not yet | |
| Greek | `el` | landing page | yes | yes | not yet | |
| Hebrew | `he` | landing page | yes | yes | not yet | |
| Hungarian | `hu` | landing page | yes | yes | not yet | |
| Croatian | `hr` | landing page | yes | yes | not yet | |
| Serbian | `sr` | landing page | yes | yes | not yet | |
| Malay | `ms` | landing page | yes | yes | not yet | |
| Swedish | `sv` | landing page | yes | yes | not yet | |
| Norwegian | `no` | landing page | yes | yes | not yet | |
| Danish | `da` | landing page | yes | yes | not yet | |
| Swahili | `sw` | landing page | yes | yes | not yet | |

**Web** — "full site" means the deeper, multi-topic translated content (three
steps, three signs, payment red flags, "I think I was scammed," for-family, all
in one long page). "landing page" means the shorter version with the same core
method plus a link to the printed sheet. Every language now has both a fridge
sheet and a wallet card — that gap closed in August 2026 (see BACKLOG.md).

---

## How to mark a language validated

When a native speaker has read the material and you're satisfied:

1. In `content/<code>/`, change the frontmatter:
   - `status:` → `validated by a native speaker, <month year>`
   - `validated_by:` → their name, or `anonymous` if they preferred
2. Remove the warning blockquote at the top of the page.
3. In `build/make_fridge.py`, delete that language's entry from the `NOTICE`
   dictionary. That removes the band from the printed sheet automatically.
4. Rebuild: `python3 build/make_fridge.py && python3 build/build_site.py`
5. Update the row above.

**If the English source later changes, the translation becomes stale.** Put the
banner back until someone re-reads it.

---

## What a validator is asked to do

Not a professional translation. One person who speaks the language daily, one or
two hours, reporting:

- what sounds translated rather than written
- **what sounds condescending** — the most important item on the list
- what words their community wouldn't use
- what's missing, because the scams reaching their community may differ

Recruitment page: `/help-translate`.
Contact: **translations@trustbutverifyproject.org**

---

## Known limitation

The four right-to-left languages (Arabic, Urdu, Farsi, Pashto) have verified
print PDFs, generated through WeasyPrint for correct HarfBuzz shaping. Their
**web** pages use standards-correct CSS but were never visually confirmed in a
modern browser — the build environment only had a 2012-era renderer that cannot
wrap right-to-left text. Check those four on a real device.
