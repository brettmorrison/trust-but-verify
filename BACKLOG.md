# Trust But Verify — Backlog

Roughly priority order. Update as items close.

## Resolved
- The 4 RTL pages (Arabic, Urdu, Farsi, Pashto) — long-flagged as "never
  visually verified, check on a real phone" — checked live at desktop
  and mobile widths. 3 of 4 clean; fixed one real cosmetic wrap bug in
  the "[Language], please" quote box (Urdu, plus fa/ps preemptively).
- Hero-photo loading bug fixed: `loading="lazy"` on an always-above-
  the-fold image caused a visible blank-then-paint flash — swapped to
  `fetchpriority="high"`.
- Mobile table rendering fixed: every table on the site (printables.md,
  resources-by-language.md) was forced to 100% width with no wrap
  protection, so words broke mid-character at 375px ("PDF" stacked
  into "P/D/F"). Tables now scroll horizontally in their own container
  instead of being force-squeezed.
- Feedback form honeypot fixed: the site's strict CSP (style-src 'self',
  no unsafe-inline) was silently blocking the inline style= that hid
  the honeypot field, so "Leave this field blank" was fully visible on
  the live page — a confused visitor filling it in would have their
  real feedback silently dropped as spam. Moved to a proper CSS class.
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
- Real photos (Wikimedia Commons, properly licensed + attributed) added
  to the home page, about page, and 14 scam-type pages. Full record in
  assets/photos/manifest.json. 6 topics still have no photo — see Open.
- resources-by-language.md's federal-materials table expanded from 16
  to all 45 languages, checked against ftc.gov/languages and
  ssa.gov/multilanguage directly — also fixed two languages (Arabic,
  Farsi) that were wrongly marked "Limited" when they actually have
  real federal materials. Also fixed: the page had zero internal links
  pointing to it anywhere on the site; linked from home.md.
- Added NAPCA's multilingual helpline (Mandarin/Cantonese/Korean/
  Vietnamese) to resources-by-language.md — the one national org that
  survived verification against several other candidates checked.
- Fixed two real bugs and completed print materials for all 45
  languages: (1) reportlab's Latin-1-only base font produced solid
  black tofu boxes for Greek/Gujarati/Hebrew/Georgian/Khmer/Punjabi/
  Serbian fridge sheets — fixed with real Unicode TTFs + bidi (Hebrew)
  + arabic_reshaper (Farsi/Pashto/Urdu wallet cards); (2) a greedy
  regex bug silently gave 15 already-live wallet cards the wrong
  tagline (the closing line, not the actual tagline) — fixed. Fridge
  sheets and wallet cards are both 45/45 now (was 38/45 and 28/45).
  printables.md's tables rebuilt from disk.

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
6. Deeper content only exists in 4 languages (es/vi/zh/ru) plus English —
   the other 40 are single landing pages. Decide whether to expand any.
7. SEO metadata pass (meta titles/descriptions) per page/language — done
   for English; per-language pass not started.
8. The 4 new scam pages (charity/Medicare/SIM-swap/lottery) exist in
   English only — no translations yet, unlike the original 13.
9. 6 pages still have no hero photo: charity-scams and government-
    impersonation (candidates were sourced but rejected on review —
    museum artifact / no visible connection to the topic, see
    assets/photos/manifest.json), plus recovery-scam, lottery-
    sweepstakes, for-family, and printables (nothing suitable found on
    Wikimedia Commons at all, tried twice independently). Try again,
    or leave them photo-less — the site reads fine either way.
    phantom-hacker got a replacement photo and is done.

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session —
investigate directly (not via email links), not tied to the Cloudflare
domains.
