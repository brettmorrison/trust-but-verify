# Publishing the site

The site is plain static HTML generated from markdown. No framework, no
JavaScript, no build server, no database. That's deliberate: fewer moving parts
means less to maintain and nothing that can quietly start collecting data.

**Host:** Cloudflare Pages, connected to a GitHub repository. Push a change,
the site rebuilds and publishes itself.

---

## Cloudflare build settings

| Setting | Value |
|---|---|
| **Framework preset** | None |
| **Build command** | `pip install -r requirements.txt && python3 build/build_site.py` |
| **Build output directory** | `site` |
| **Root directory** | `/` (leave blank) |

Add one environment variable so the build image uses the right interpreter:

| Variable | Value |
|---|---|
| `PYTHON_VERSION` | `3.12` |

---

## What is and isn't committed

**Committed:** all markdown in `content/`, the generators in `build/`, and every
finished PDF, DOCX, and PPTX in `formats/`.

**Not committed:** `site/` — Cloudflare generates it on every push. It's in
`.gitignore`.

The PDFs are committed rather than built in CI on purpose. Regenerating them
needs WeasyPrint, wkhtmltopdf, and Noto fonts for sixteen scripts, none of which
are in Cloudflare's build image. Regenerate locally when a translation changes,
then commit the result.

The social share-card PNGs (`formats/og/*.png`, one per page, used for
`og:image`) are committed the same way and for the same reason — they're
built with macOS system fonts (`build/make_share_cards.py`) that neither
exist in Cloudflare's Linux build image nor are licensed for redistribution
in the first place. `build_site.py` just copies them into `site/og/` on
every build. Regenerate locally whenever a page's title or description
changes, then commit the PNGs.

The hero photos on the home page and some scam-type pages
(`assets/photos/web/*.jpg`) follow the same committed-asset pattern —
`build_site.py` copies them into `site/photos/`. Every one is a real
photo from Wikimedia Commons under a license that requires attribution
(CC BY / CC BY-SA), sourced and recorded in `assets/photos/manifest.json`
(topic, license, author, source URL) — the on-page caption under each
photo *is* that attribution, so don't strip it. `assets/photos/source/`
holds the full-resolution originals (100+ MB, gitignored, not needed for
the site to build) in case a photo ever needs re-cropping.

---

## The feedback form (`/feedback`)

The form at `/feedback` posts to a Cloudflare Pages Function
(`functions/api/feedback.js`) that emails the message to
`translations@trustbutverifyproject.org` via [Resend](https://resend.com)
and stores nothing. It needs one-time setup:

1. Create a free Resend account at resend.com (100 emails/day, 3,000/month —
   plenty for a feedback form).
2. In Resend, **Domains** → **Add Domain** → `trustbutverifyproject.org`.
   Resend shows you a handful of DNS records (SPF/DKIM) to add.
3. Add those records in Cloudflare → **DNS** → **Records** for
   trustbutverifyproject.org. If Cloudflare Email Routing already added an
   SPF `TXT` record at the root, don't create a second one — edit the
   existing `TXT` record and merge in Resend's `include:` value instead
   (a domain can only have one SPF record; two will break both).
4. Back in Resend, click **Verify** on the domain — usually confirms within
   a few minutes.
5. Resend → **API Keys** → **Create API Key** → name it `tbv-feedback-form`,
   permission **Sending access only**, restricted to
   trustbutverifyproject.org if that scoping option is offered. Copy the
   key — it's shown once.
6. Cloudflare Pages → the `trust-but-verify` project → **Settings** →
   **Environment variables** → **Add variable**: name `RESEND_API_KEY`,
   paste the key, click the **Encrypt** / **Secret** toggle so it's not
   visible again after saving, apply to **Production** (and Preview if you
   want the form to work on preview deploys too). Save, then redeploy
   (Cloudflare → Deployments → **Retry deployment** on the latest one, or
   just push any commit) so the Function picks up the new variable.

Until step 6 is done, the form returns "Feedback form is not configured
yet." instead of erroring silently.

---
## Fallback — drag and drop (if you ever need it)

Only useful for a one-off emergency deploy. The git method above is the normal path; a drag-and-drop project cannot later be connected to git, so don't start here.

1. Go to **dash.cloudflare.com** → **Workers & Pages** → **Create** →
   **Pages** → **Upload assets**
2. Project name: `trust-but-verify`
3. Drag the whole **site** folder in
4. **Deploy**

You'll get a URL like trust-but-verify.pages.dev. Check it works.

5. In the project: **Custom domains** → **Set up a custom domain** →
   `trustbutverifyproject.org` → **Activate**
6. Add `www.trustbutverifyproject.org` the same way

Because the domain is already in your Cloudflare account, DNS is automatic.
HTTPS certificates issue on their own, usually within a few minutes.

To update later, upload a new version of the folder. Cloudflare keeps every
previous deployment and you can roll back with one click.

---

## The git setup, step by step



1. Put the whole project in a GitHub repo (public is fine — everything here is
   meant to be copied)
2. Cloudflare → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**
3. Build settings:
   - **Build command:** `pip install markdown && python3 build/build_site.py`
   - **Build output directory:** `site`
4. Add the custom domain as in Option A

Now editing a markdown file and pushing rebuilds and publishes the site.

Add `site/` to `.gitignore` if you use this option — no reason to commit
generated files.

---

## Domains

The canonical domain is `trustbutverifyproject.org`. `trustbutverifyproject.com`
(the same, correct spelling, just the `.com`) was registered separately and
redirects to it:

**Rules** → **Redirect Rules** → **Create rule**

- **If:** Hostname equals `trustbutverifyproject.com`
- **Then:** Dynamic redirect, **301 permanent**, to
  `concat("https://trustbutverifyproject.org", http.request.uri.path)`

The `concat` expression preserves the path, so a mistyped deep link still lands
in the right place.

The misspelled domains that had been floated (`trustbutverifiyproject.org`,
`trustbutverifiyproject.com`, `trustbutverificationproject.org`) are not being
kept — auto-renew has been turned off on the one confirmed registered. No
redirect setup needed for those.

---

## Settings to check once

**SSL/TLS** → set encryption mode to **Full (strict)**.

**SSL/TLS → Edge Certificates** → turn on **Always Use HTTPS** and
**Automatic HTTPS Rewrites**.

**Speed → Optimization** → leave Rocket Loader **off**. It injects JavaScript,
which this site doesn't need and shouldn't have.

**Analytics** — decided: on, in Cloudflare's automatic mode (no JS beacon, no
cookies, aggregate pageviews only). Enable at **Analytics & Logs → Web
Analytics** for the domain. The copy in `README.md`, `content/en/about.md`,
and `content/en/home.md` has already been updated to describe exactly this —
an anonymous pageview count, nothing more — so the site's privacy claims stay
accurate. If the analytics setup ever changes, update those three files to
match. Never let the copy and the reality drift apart on this site of all
sites.

**Do not add** Google Analytics, Meta pixels, chat widgets, or embedded fonts.
Any of those would make the privacy statement false.

---

## What's already handled

The generator writes these into `site/` for you:

- **`_headers`** — security headers Cloudflare Pages applies automatically:
  a strict Content-Security-Policy that blocks all scripts, `X-Frame-Options`,
  `nosniff`, `no-referrer`, HSTS, and a Permissions-Policy that switches off
  geolocation, camera, microphone, and cohort tracking
- **`robots.txt`** and **`sitemap.xml`** — regenerated on every build
- **`404.html`** — written in the same voice as the rest of the site, and it
  leads with "nothing is wrong and you haven't broken anything" rather than an
  error code
- **`/print/`** — every PDF, so the printables page can link to real files

---

## Before you announce it

- [ ] Create **translations@trustbutverifyproject.org** — it's printed on the
      fridge sheets and on the site. Cloudflare Email Routing does this free:
      **Email** → **Email Routing**, forward it to your Gmail.
- [ ] Click every link on the homepage
- [ ] Open it on an actual phone, not a desktop browser window made narrow
- [ ] Read one page at arm's length. If you squint, the type is too small.
- [ ] Test with a screen reader if you can — VoiceOver on iPhone is two taps to
      enable and is the fastest reality check available
- [ ] Have one person over 70 use it in front of you without help, and watch
      where they hesitate. This will tell you more than everything else on this
      list combined.

---

## Known gaps

**Check the four right-to-left pages on a real phone before announcing them.**
Arabic, Urdu, Farsi, and Pashto. The printed PDFs are fixed and verified — they
now render through WeasyPrint, which does proper HarfBuzz shaping.

The *web* pages use standards-correct CSS (direction set on the content
container, max-width, overflow-wrap), which every modern browser handles
correctly. But the only renderer available in the build environment is a
2012-era WebKit that doesn't wrap right-to-left text, so I could not verify them
visually. They are almost certainly fine. "Almost certainly" is not a standard
this project should accept on a page someone reads while frightened, so please
open all four on an actual phone and confirm the text wraps rather than running
off the edge.

**No translated page is validated.** Every non-English page carries a warning
band saying so. That band stays until a native speaker signs off.

---

## Maintenance

**Every April**, when the FBI's Internet Crime Complaint Center publishes its
annual report, update the statistics. They appear in:

- `content/en/i-think-i-was-scammed.md`
- `content/en/scams/investment-and-crypto.md`
- `content/en/scams/voice-cloning.md`
- `content/en/about.md`
- `content/en/glossary.md`
- and the equivalent line in each translation

Search the content folder for the year to find them all.

**Whenever a page changes**, the corresponding translations become stale. Put
the warning band back if it was ever removed.
