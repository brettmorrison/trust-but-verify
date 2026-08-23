# Trust But Verify — Backlog

Roughly priority order. Update as items close.

## Resolved
- Site live end-to-end at `trustbutverifyproject.org`, plus `.com`,
  `tbvproject.com`, `tbvproject.org` all 301 → canonical. Misspelled typo
  domains dropped, auto-renew cancelled. Repo public:
  https://github.com/brettmorrison/trust-but-verify
- Full navigation added (header, JS-free language switcher, wide-screen
  sidebar, footer) — previously the site had none, so most scam-type pages
  were unreachable from anywhere.
- Home page rebuilt as a "What kind of call did you get?" card grid to all
  13 scam-type pages.
- New content: virtual-kidnapping.md, cold-call tech-support variant,
  password-manager section, give-this-talk.md hub page (talk deck, speaker
  script, and 3 other talk formats now have real URLs, linked for the
  first time), privacy.md, terms.md.
- About page: first-person origin story, personal + verified DOJ/FBI case
  examples, linked to LinkedIn.
- Trust-blue color (10.24:1 contrast) + magnifying-glass-and-checkmark logo
  (redesigned from a shield-and-checkmark that read as borrowed from
  antivirus/security-badge branding) + matching favicon.
- **45 languages total**, all wired into the header switcher (LANGS list
  in build_site.py — the actual source of truth for site nav). QR codes
  and fridge sheets exist for all of them.
- Editable DOCX handout no longer published (tampering/impersonation risk)
  — routed through translations@ email instead. Note: the source .docx is
  still in the public GitHub repo itself; ask if you want it stripped from
  there too.
- Fixed: 404 page's relative stylesheet path broke on any missing URL that
  looked like a subdirectory; talk deck .pptx was never actually copied to
  the deployed site; printables.md's download tables were undercounting
  both fridge sheets and wallet cards even before this session's additions.
- Zero broken internal links across all 89 pages, verified by script.

## Open
1. Confirm Cloudflare Web Analytics is toggled on (Analytics & Logs → Web
   Analytics, automatic mode) — copy already assumes it is.
2. Set up `translations@trustbutverifyproject.org` via Cloudflare Email
   Routing, if not already done.
3. Turn off Cloudflare's Email Address Obfuscation (Scrape Shield) for
   trustbutverifyproject.org — it rewrites the email address site-wide into
   a broken placeholder that never decodes back, because the site's own
   strict no-JS CSP blocks the decode script. One dashboard toggle fixes
   every instance at once.
4. Build the feedback-form backend: a Cloudflare Pages Function that
   forwards submissions to email, no storage, honeypot instead of Turnstile
   (Turnstile needs client-side JS, which conflicts with the site's CSP).
   Not started — real new infrastructure, not a copy change.
5. Circulate the translation validator recruitment page — nothing
   non-English is validated yet, across all 45 languages.
6. Wallet cards only exist in 13 of 45 languages — the rest need WeasyPrint
   (not installed in this session) or a reportlab-based generator like the
   fridge-sheet one.
7. Deeper content only exists in 4 languages (es/vi/zh/ru) plus English —
   the other 40 are single landing pages. Decide whether to expand any.
8. SEO metadata pass (meta titles/descriptions) per page/language.
9. Share cards (Open Graph images) per page/language — needs sourced,
   correctly-attributed Creative Commons photos, real research work, not
   generation. Not started.
10. One-page infographic — built (formats/print/infographic-en.pdf,
    English only), not yet linked from anywhere on the site.
11. Two new presentations requested, not started: one for volunteers
    giving the talk (distinct from the existing deck — clarify how), one
    for family members of seniors on how to help protect them.
12. Candidate new scam-type pages: charity scams, Medicare/health insurance
    scams, SIM-swap, lottery/sweepstakes.
13. Verify whether any *stable, national* (not local/volatile) same-
    language-community fraud-support orgs are worth adding alongside the
    two hotlines in resources-by-language.md — needs real verification,
    the file already deliberately avoids hardcoding volatile local orgs.
14. resources-by-language.md's language table (federal-materials
    availability) only covers the original ~16 languages, not all 45.

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session —
investigate directly (not via email links), not tied to the Cloudflare
domains.
