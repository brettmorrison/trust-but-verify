# Trust But Verify — Backlog

Roughly priority order. Update as items close.

## Resolved
- Non-English translation + audio expansion, at Brett's request. Phase
  1: translated the 5 missing scam-type articles from the English
  top-10 list into Spanish (phantom-hacker, tech-support-popup,
  grandparent-scam, government-impersonation, romance-scam), narrated
  via the free macOS voice — $0. Phase 2, same day, after Brett heard a
  direct side-by-side comparison of the free voice vs. ElevenLabs and
  chose to front-load quality: translated the same 5 articles into
  Vietnamese, Chinese, Russian, and Korean too (20 more pages, all
  unvalidated AI drafts pending native review), and upgraded Spanish's
  5 articles from the free voice to ElevenLabs (~25,208 characters,
  checked against the account's real remaining quota first — Creator
  plan, 131,000 credits/mo, resets Sept 24). make_audio.py now has
  LANG_EL_PAGES (ElevenLabs, non-English) alongside LANG_PAGES (free
  macOS voice) and a per-language model override (Vietnamese needs
  Turbo v2.5 — the standard multilingual model doesn't support it at
  all). Also fixed a real, sitewide, pre-existing bug found while
  wiring this up: every non-English page's Home link and site logo
  pointed at the English homepage instead of that language's own
  landing page, and the sidebar's scam-type links always pointed to
  English even when a translated version existed — both fixed for all
  45 languages, not just the 4 added this session. See Open #1 for the
  paced continuation plan (budget doesn't allow doing every language at
  once).
- Full security audit at Brett's request, given how much surface area
  got added this session. One real code fix: build_site.py wrote a
  page's output path straight from frontmatter `slug:` with no
  validation — a crafted slug with `../` segments could make the build
  write outside `site/` entirely (confirmed with a real repro, then
  confirmed the fix blocks it). Requires a malicious commit landing in
  content/ first, not remotely triggerable by a visitor, but worth
  closing on a public repo. Also added a basic email-shape check to
  the feedback function, and documented DMARC + Cloudflare rate
  limiting in DEPLOY.md (both still need the actual DNS
  record/dashboard rule from Brett — see Open). Everything else came
  back clean: no secrets anywhere in git history, CSP/headers as tight
  as intended, no command-injection surface in build scripts, no
  third-party scripts/trackers anywhere in content.
- `translations@trustbutverifyproject.org` is live via Cloudflare Email
  Routing, forwarding to Brett's inbox — confirmed working 2026-08-25
  (on the correct domain, after the typo-domain false start noted
  above). MX/DKIM records show Locked (Cloudflare-managed), the SPF
  TXT record is deliberately Unlocked for the future Resend merge.
- Second blog post: "Spying on the Scammers" (Jim Browning's YouTube
  investigation into a real Indian scam call center) — verified channel
  legitimacy, the specific video, and the BBC Panorama/police-raid
  connection before publishing; included the honest detail that the
  operator was later acquitted rather than the tidier version.
- A real accessibility-tree pass on the feedback form (not just
  automated/structural checks) found the honeypot field's aria-hidden
  was silently inert — Chrome ignores it on any element with a
  focusable descendant, which this field's tabindex="-1" still counts
  as. Fixed by making the label itself unambiguous instead.
- Heads up: a separate session (Brett + Opus 5) has been working this
  same repo in parallel — expanded and translated the phishing page
  into all 45 languages, updated the translation-feedback copy
  sitewide, and caught a real bug in this session's own audio work
  (CSP had no media-src, silently blocking every `<audio>` player in
  production — undetectable via local testing without real CSP
  headers). Both sessions have stayed conflict-free via git so far.
- Accessibility, phase 1 (English, screen-reader + audio): started on
  Brett's request to support visually impaired and blind visitors.
  Real landmarks (distinct header/footer nav labels, a named sidebar),
  the numbered-step badges are now a real `<ol>`/`<h3>` list instead of
  styled `<div>`s, fixed 3 heading-hierarchy violations, and audio
  narration (build/make_audio.py — macOS `say` + ffmpeg, $0 cost, no
  API key, no network call) for a 4-page pilot (home, the-three-steps,
  warning-signs, about) with a plain `<audio controls>` player, zero
  JS. See "Open" below for the natural next steps — more pages, other
  languages, and an actual screen-reader (not just automated-tool)
  pass.
- Fridge sheet: added a labeled blank line for the family's code word,
  across all 45 languages, plus fixed the same stale tagline issue on
  every one of them (still had the pre-tagline-change wording). Also
  fixed a real local-build bug: wkhtmltopdf isn't installed here and
  never was, so the English fridge sheet could never actually be
  regenerated locally before this — switched the whole generator to
  weasyprint, which required a real layout-tightening pass since
  weasyprint's rendering isn't a drop-in match for wkhtmltopdf's.
- Feedback form: every failure path (not just the happy path) now lands
  on a real page instead of either a bare unstyled 503 text dump or a
  query-string error state the static site can't actually display.
  Root cause of "clicking send does nothing" is still the pending
  RESEND_API_KEY setup below — this fixes the failure experience, not
  the underlying missing config.
- The site's most-repeated content pattern ("**1. Do this.** Because
  why.") now gets a real numbered-badge treatment on the website itself
  — previously only the printed materials (fridge sheet, talk deck) had
  any visual weight for it; the site rendered it as plain bold text.
  Applies automatically everywhere the pattern is already used, not
  just home.md.
- Volunteer talk deck (formats/talk/trust-but-verify-talk.pptx): every
  slide now carries a QR code + trustbutverifyproject.org, not just the
  last one — two QR color variants (dark-on-transparent, paper-on-
  transparent) so it reads against both the dark and light slide
  backgrounds. Also fixed the tagline on the title and closing slides,
  still reading the old "You don't have to get suspicious of everybody"
  line, to match the site's current tagline. Along the way, fixed the
  build script's output path, hardcoded to a nonexistent cloud-sandbox
  location — it silently wasn't writing into the repo.
- Infographic translated into the top 10 languages (es/vi/zh/ru/ko/tl/
  hi/bn/hy/am), 11 total with English. Also fixed a real pre-existing
  bug found along the way: the footer (hotlines, report line) was
  rendering below the page's bottom margin — never visible — for every
  version including the original English one. Tightened spacing,
  verified against both English and Armenian (longest text).
- Cloudflare email obfuscation issue fixed without touching Cloudflare:
  the visible "translations@..." address is now written as
  "translations [at] trustbutverifyproject [dot] org" everywhere, which
  never matches Cloudflare's rewrite pattern in the first place — no
  loss of scraper resistance, no JS needed, no dashboard change required.
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
- /help-translate (the exact page Brett is about to circulate) claimed
  only 12 languages were drafted and listed 13 more, including several
  live for a while (Korean, Urdu, Hindi, Farsi, Amharic...), as "not
  yet drafted." Rebuilt with all 44 actually-drafted languages. Only
  Turkish and Traditional Chinese are genuinely not drafted yet.
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
1. Accessibility, phase 3: 26 English pages have audio (20 via
   ElevenLabs, 6 via free macOS voice). Spanish, Vietnamese, and now
   Chinese have all 5 of their scam articles on ElevenLabs (Spanish
   2026-08-25, Vietnamese + Chinese 2026-08-27 — Vietnamese needed the
   eleven_turbo_v2_5 model override since the standard multilingual
   model doesn't support it; Chinese used the standard model and only
   cost 9,117 characters total, since Chinese text is far denser per
   character than Spanish/Vietnamese). ru/ko still have the same 5
   articles translated but on the free macOS voice, TODO for the
   ElevenLabs upgrade. Language order after Spanish was picked by US
   immigrant-population size (Brett's request, 2026-08-27): Vietnamese,
   then Chinese (verified via web search — China clearly outranks
   Korea and Russia); Korean should come before Russian next for the
   same reason unless Brett says otherwise. Real quota checks:
   2026-08-25 showed 64,298/131,000; still 64,298 on 2026-08-27 (2-day
   gap, nothing drifted); after Vietnamese, confirmed 71,574 used,
   59,426 remaining. Chinese's batch (~9,117 chars) not yet
   independently re-confirmed against the dashboard — should cost very
   little given the character count. Creator plan, 131,000 credits/mo,
   resets Sept 24. Brett's standing pacing rule (2026-08-27, still in
   force): go slow, one language at a time, stop and let him check
   spending between batches — do NOT chain multiple languages' batches
   without a fresh quota confirmation in between, even if the math
   looks safe. A "listen in other languages" row now sits inside the
   audio-player box itself on every article translated into more than
   one language (Brett's request, 2026-08-27) — see
   lang_versions_widget() in build_site.py; this will need zero changes
   as more languages/articles get added, it's driven entirely by which
   content/<lang>/<slug>.md files exist on disk. Still open regardless
   of budget: a real screen-reader pass (VoiceOver, free, built into
   macOS) rather than just automated/structural checks; the original
   English-batch ElevenLabs key expired around 2026-09-24 — TBVP2
   (created 2026-08-25) is the active key now, same 30-day-ish expiry
   pattern likely applies, renew when it lapses.
2. Confirm Cloudflare Web Analytics is toggled on (Analytics & Logs → Web
   Analytics, automatic mode) — copy already assumes it is. Note
   (2026-08-25): while checking this, Brett found Cloudflare's separate
   RUM (Real User Measurements) feature on the same page — that's a
   different, more invasive product (collects device/location/network
   context, not just anonymous pageviews) and privacy.md doesn't
   disclose it. Left off for now; if ever enabled, use "Exclude EU"
   and update privacy.md first.
3. Set up the feedback form: create a Resend account, verify
   trustbutverifyproject.org (add its DNS records in Cloudflare —
   merge into the existing SPF TXT record if Email Routing already
   made one, don't add a second), generate an API key, and add it as
   the `RESEND_API_KEY` secret on the Cloudflare Pages project. Full
   steps in DEPLOY.md. The code (functions/api/feedback.js,
   content/en/feedback.md) is already built and deployed — this is
   just the account/key setup, a user action.
4. Circulate the translation validator recruitment page — nothing
   non-English is validated yet, across all 45 languages.
5. Add a DMARC TXT record once SPF and DKIM are both live — steps in
   DEPLOY.md. Low urgency but genuinely missing (found in the security
   audit); without it there's no enforced policy for spoofed
   `@trustbutverifyproject.org` email.
6. Only if `/api/feedback` ever actually gets abused/spammed: add a
   Cloudflare Rate Limiting Rule for `POST /api/feedback` — steps in
   DEPLOY.md. Not worth doing preemptively for this site's traffic
   level; noted so it's a known, ready fix if it ever comes up.
7. Deeper content only exists in 4 languages (es/vi/zh/ru) plus English —
   the other 40 are single landing pages. Decide whether to expand any.
8. A few translated landing pages carry a narrower "before money is sent"
   -style section header right under the tagline (e.g. German's `##
   Bevor Geld überwiesen wird`) that's now slightly inconsistent with the
   broadened tagline above it — cosmetic, low priority, native-speaker
   validation will catch it anyway.
9. The 4 new scam pages (charity/Medicare/SIM-swap/lottery) exist in
   English only — no translations yet, unlike the original 13.
10. 7 pages still have no hero photo: home (previous photo was disliked;
   a dedicated Commons/Openverse search for a replacement came back with
   nothing that cleanly fit license + landscape + tone + setting all at
   once — see assets/photos/manifest.json for the specific candidates
   considered), charity-scams and government-impersonation (candidates
   were sourced but rejected on review — museum artifact / no visible
   connection to the topic), plus recovery-scam, lottery-sweepstakes,
   for-family, and printables (nothing suitable found at all, tried
   twice independently). Try again, or leave them photo-less — the site
   reads fine either way. phantom-hacker got a replacement and is done.

## Unrelated flag
Password reset email clusters in GoDaddy account from an earlier session —
investigate directly (not via email links), not tied to the Cloudflare
domains.
