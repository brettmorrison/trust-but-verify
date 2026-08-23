# Trust But Verify — Backlog

Roughly priority order. Update as items close.

## Resolved
- Site live end-to-end: `trustbutverifyproject.org` (canonical), plus
  `trustbutverifyproject.com`, `tbvproject.com`, `tbvproject.org` all 301 →
  canonical. Misspelled typo domains dropped, auto-renew cancelled.
- Repo public: https://github.com/brettmorrison/trust-but-verify
- Real deliverable deployed via Cloudflare Pages (17 → 24 languages of print
  material, 24 fridge sheets, 13 wallet cards, talk deck, speaker script).
- Site navigation added (2026-08-23) — header nav, JS-free language switcher,
  wide-screen sidebar rail, footer links. Previously the site had none, so
  8 of 12 scam-type pages were unreachable from anywhere.
- Home page rebuilt as a "What kind of call did you get?" card grid linking
  every scam-type page — large tap targets, single column on mobile.
- New content: `virtual-kidnapping.md` (real, distinct FBI-tracked scam, not
  the same as the grandparent/bail scam); cold-call tech-support variant
  added to `tech-support-popup.md`; password-manager section added to
  `phishing.md` (built-in OS options only, no product endorsement).
- Trust-blue accent color (10.24:1 contrast, WCAG AAA) + shield-checkmark
  logo mark + SVG favicon, all inline/self-hosted, no new requests.
- 7 new language landing pages shipped: German, French, Portuguese, Polish,
  Romanian, Ukrainian, Indonesian — fridge sheets already existed for these,
  web pages now match.
- `printables.md` download tables fixed — previously undercounted both
  fridge sheets (said 13, 24 actually exist) and wallet cards (listed 3 of
  13) even before this session's additions.
- QR codes added to all 24 fridge sheets, linking to each language's own
  page (`build/add_qr_codes.py`, re-run after regenerating any sheet).
- Analytics copy (README/about/home + all 17 original language footer
  strings) updated to match Cloudflare Web Analytics running in cookie-free
  automatic mode.

## Open
1. Confirm Cloudflare Web Analytics is actually toggled on in the dashboard
   (Analytics & Logs → Web Analytics, automatic mode) — copy already
   assumes it is.
2. Set up `translations@trustbutverifyproject.org` via Cloudflare Email
   Routing.
3. Circulate the translation validator recruitment page
   (`content/en/help-translate.md`) — nothing non-English is validated yet.
4. Build full `content/` pages for the 7 print-only-until-now languages
   (they only had a single landing page written this session, not the
   fuller multi-page treatment `es`/`vi`/`zh`/`ru` have) — same question
   applies to whether the original 12 single-landing-page languages
   (am, ar, bn, fa, hi, hy, ja, ko, ps, sq, tl, ur) get expanded too.
5. Wallet cards only exist in 13 of 24 languages — regenerate the missing
   11 (needs WeasyPrint + system deps, not installed in this session).
6. SEO metadata pass (meta titles/descriptions, clean URLs) per page/language.
7. Share cards (Open Graph / Twitter Card images) per page/language, with
   real photos — see next item.
8. **Not started, distinct type of work:** source Creative-Commons-licensed
   photos for share cards, with correct attribution. Needs real web research
   and license verification per image, not just generation — flagged
   separately since a misattributed photo is a real risk for a public
   nonprofit site.
9. **Not started:** research reportfraud.ftc.gov and ic3.gov for additional
   content ideas.
10. **Not started:** one-page infographic (separate from the fridge sheet).
11. **Not started:** a new presentation + speaker notes for volunteers who
    give the talk to help others resist scams (distinct from the existing
    `formats/talk/trust-but-verify-talk.pptx` — clarify how it differs
    before building).
12. **Not started:** a second, new presentation targeted at family members
    of seniors, on how to help "inoculate" a senior they love.
13. Candidate new scam-type pages, not yet written: charity scams, Medicare/
    health insurance scams, SIM-swap, lottery/sweepstakes (each mentioned in
    passing elsewhere, no dedicated page).

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session —
investigate directly (not via email links), not tied to the Cloudflare
domains.
