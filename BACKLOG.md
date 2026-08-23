# Trust But Verify — Backlog

Roughly priority order. Update as items close.

## Resolved (verified 2026-08-23)
- Translations: 17 languages of full site content exist in `content/` (am, ar, bn, en, es, fa, hi, hy, ja, ko, ps, ru, sq, tl, ur, vi, zh).
- Print materials: 24 fridge sheets and 12 wallet cards exist in `formats/print/`, editable DOCX handout in `formats/docx/`, talk deck + speaker script in `formats/talk/`.
- Build verified locally in a clean venv: `pip install -r requirements.txt && python3 build/build_site.py` → 53 pages, 0 errors.
- The "7 quarantined languages" (Ukrainian, French, German, Portuguese, Polish, Romanian, Indonesian) are **not** a non-issue as previously reported — fridge sheets exist for all 7 (`fridge-sheet-{uk,fr,de,pt,pl,ro,id}.pdf`). They just don't have full site content pages in `content/`. Worth deciding whether to build those out later or leave print-only.
- Repo pushed public: https://github.com/brettmorrison/trust-but-verify — personal identifying details (Brett's name, tied to translation-validation approval) scrubbed from `00-CONTENT-PLAN.md` and `TRANSLATIONS.md` before making it public.

## Open
1. Deploy to Cloudflare Pages — connect the GitHub repo, build command `pip install -r requirements.txt && python3 build/build_site.py`, output dir `site`. Steps and exact copy-paste values are in `DEPLOY.md` and were also sent as a separate copy-paste sheet.
2. Set up `translations@trustbutverifyproject.org` via Cloudflare Email Routing.
3. Confirm auto-renew is off on `trustbutverifiyproject.com` (the typo domain) and set up the 301 redirect rules for the typo domains once Pages is live.
4. Add Cloudflare Web Analytics (cookie-free) before announcing publicly.
5. Circulate the translation validator recruitment page (`content/en/help-translate.md`) to line up native speakers — nothing non-English is validated yet per `TRANSLATIONS.md`.
6. Add a QR code on print materials linking to the matching web page.
7. SEO-optimize every page, in every language (meta titles/descriptions, clean URLs) — stay consistent with the "no shame / no fear / capability-first" editorial rules already baked into the content itself.
8. Add a share card (Open Graph / Twitter Card image) per page, in every language, so links look inviting when texted or shared — not scary or alarmist.
9. Decide whether to build full `content/` pages for the 7 print-only languages, or leave them as fridge-sheet-only.

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session — investigate directly (not via email links), not tied to the Cloudflare domains.
