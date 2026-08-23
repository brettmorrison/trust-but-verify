# The Trust But Verify Project — website

Static site. No build step, no framework, no JavaScript, no cookies, no trackers.

## Deploying to Cloudflare Pages

1. Push this folder to a GitHub repo.
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.
3. Build command: leave empty. Build output directory: `/`
4. Add your custom domain under the Pages project's Custom domains tab.

Or drag this folder straight into Cloudflare Pages' "Direct Upload" option — no repo needed.

## Editing

`build.js` generates every page from one template so the header, footer, and
navigation stay consistent. Edit the content in `build.js`, then run:

    node build.js

Editing the `.html` files directly also works, but changes are overwritten the
next time you run the build.

`assets/style.css` holds the whole design system. Base font size is set to 125%
deliberately — the primary audience needs it.

## Renaming the project

The name appears in `build.js` as the `SITE` constant plus the wordmark markup.
Change those two places and rebuild.

## Files

- `index.html` — home
- `how-scams-work.html` — the three red flags, eight scam types, six habits, privacy
- `it-just-happened.html` — first 24 hours, who to call
- `give-this-talk.html` — the volunteer speaker pitch
- `print.html` — printable materials
- `about.html` — story, promises, what we're not
- `blog/` — five worked examples
- `downloads/` — the slides, script, handout, and desk card
