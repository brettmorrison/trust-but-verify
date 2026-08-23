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
  in build_site.py — the actual source of truth for site nav).
- **Fixed a critical bug, already caught and corrected:** reportlab's
  default font can't render non-Latin scripts, so every fridge sheet/
  wallet card generated for Greek, Gujarati, Hebrew, Georgian, Khmer,
  Punjabi, or Serbian came out as solid black boxes — briefly live on the
  deployed site. Deleted the broken files, removed their dead links, kept
  the 15 Latin-script wallet cards that render correctly. Fridge sheets
  now exist for 38 languages, wallet cards for 28 — accurate counts,
  verified against what's actually on disk, not hand-maintained.
- Editable DOCX handout no longer published (tampering/impersonation risk)
  — routed through translations@ email instead. Note: the source .docx is
  still in the public GitHub repo itself; ask if you want it stripped from
  there too.
- Fixed: 404 page's relative stylesheet path broke on any missing URL that
  looked like a subdirectory; talk deck .pptx was never actually copied to
  the deployed site; printables.md's download tables were undercounting
  both fridge sheets and wallet cards even before this session's additions.
- Zero broken internal links across all 89 pages, verified by script.
- Family-member presentation built (12 slides + speaker notes,
  formats/talk/trust-but-verify-for-family.pptx), drawn from for-family.md,
  linked from there and cross-linked from give-this-talk.md. Validated and
  visually QA'd — no defects. The existing volunteer deck was reviewed and
  judged already complete (22 slides, full speaker script) — no rebuild
  needed there, just needed to be discoverable, which give-this-talk.md
  already fixed.
- About page: cut the manifesto-style sections, fixed off-center logo
  checkmark (header, favicon, infographic).
- hreflang alternate tags added for all 45 language landing pages (plus
  x-default), so search engines treat them as translations of each other
  instead of unrelated content. Deep English-only content is untagged.
- Social share cards (og:image) built and shipped for all pages —
  typographic, drawn from the site's own design system, no sourced-photo
  problem. See `build/make_share_cards.py`.
- Four new scam-type pages: charity-scams.md, medicare-scams.md,
  sim-swap.md, lottery-sweepstakes.md — wired into the home grid and
  cross-linked, each with a real FBI IC3/FTC/HHS-OIG citation.
- Feedback form built: /feedback page (plain HTML form, no JS, honeypot
  spam defense) + functions/api/feedback.js (Cloudflare Pages Function,
  forwards to translations@ via Resend, nothing stored). Code is
  deployed; needs a one-time Resend account + RESEND_API_KEY secret to
  actually send — see "Set up the feedback form" below.

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
4. Set up the feedback form: create a Resend account, verify
   trustbutverifyproject.org (add its DNS records in Cloudflare —
   merge into the existing SPF TXT record if Email Routing already
   made one, don't add a second), generate an API key, and add it as
   the `RESEND_API_KEY` secret on the Cloudflare Pages project. Full
   steps in DEPLOY.md. The code (functions/api/feedback.js,
   content/en/feedback.md) is already built and deployed — this is
   just the account/key setup, a user action.
5. Circulate the translation validator recruitment page — nothing
   non-English is validated yet, across all 45 languages.
6. Wallet cards exist for 28 of 45 languages; fridge sheets for 38 of 45.
   The missing 7 (Greek, Gujarati, Hebrew, Georgian, Khmer, Punjabi,
   Serbian) need real Unicode font embedding (Noto Sans per script) plus
   bidi reshaping for Hebrew — WeasyPrint (not installed this session) or
   a properly font-equipped reportlab pipeline, not the plain-Helvetica
   approach that broke this session.
7. Deeper content only exists in 4 languages (es/vi/zh/ru) plus English —
   the other 40 are single landing pages. Decide whether to expand any.
8. SEO metadata pass (meta titles/descriptions) per page/language — done
   for English; per-language pass not started.
9. Verify whether any *stable, national* (not local/volatile) same-
   language-community fraud-support orgs are worth adding alongside the
   two hotlines in resources-by-language.md — needs real verification,
   the file already deliberately avoids hardcoding volatile local orgs.
10. resources-by-language.md's language table (federal-materials
    availability) only covers the original ~16 languages, not all 45.
11. The 4 new scam pages (charity/Medicare/SIM-swap/lottery) exist in
    English only — no translations yet, unlike the original 13.

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session —
investigate directly (not via email links), not tied to the Cloudflare
domains.
