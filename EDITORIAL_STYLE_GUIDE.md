# Editorial style guide — hand-written, standing rules

**This file is human-owned.** `build/learn_from_edits.py` never touches it —
it only reads it, the same way a future content-generation pass (a new
blog post, a new translation, a Reprocess-style regeneration) should. The
companion file, `EDITORIAL_LEARNED_PATTERNS.md`, is the opposite: fully
machine-owned, regenerated from git-history diffs every run, and never
hand-edited. See `~/Claude/playbooks/editorial/blog-generation-pipeline.md`
for why the split matters — a script that rewrites its own output file will
silently discard anything hand-edited into it.

Anyone (or any agent) drafting new content, translating a page, or
reviewing an edit for this site should read this file first.

---

## The bar: defend every sentence

Every sentence should be defensible in front of someone who knows the
domain better than you — a fraud investigator, a native speaker of the
language, a reader who's actually 78 and has heard every scam pitch there
is. If a sentence makes a claim you can't back with a specific source, a
specific number, or a specific mechanism, soften it or cut it.

"Scammers are very sophisticated" fails this test — vague, unfalsifiable,
doesn't help anyone. "The FBI's 2025 IC3 report puts elder fraud losses at
$X billion" passes — a specific, checkable claim. This site already does
this well in its scam-type pages (compare any of them to a generic
"stay safe online" listicle); the discipline is to keep doing it as the
site grows, not to relax once the novelty wears off.

*(Principle borrowed and adapted from `~/Claude/playbooks/editorial/
voice-and-defend-every-sentence.md`, itself explicitly designed to be
portable to any project publishing user-facing content.)*

## No fear, no shame — this site's one non-negotiable rule

Stated directly in the site's own copy and repeated throughout this
session's work: readers are frightened enough already. Never use urgency,
alarm, or shock language to make a point — even when the underlying fact
is alarming. State the fact plainly and let it land on its own weight.
Never imply a reader who fell for a scam was foolish, careless, or should
have known better; the entire premise of the site is that these schemes
are built by professionals to defeat careful people.

**Banned register, not banned words specifically:** anything that reads as
talking down to the reader, anything that reads as manufactured urgency
("act now," "don't wait," "before it's too late" — outside of literal
crisis-page content like `/right-now` where urgency is the honest truth,
not a rhetorical trick), anything that would sound like a scammer's own
pressure tactics if read aloud.

## Specific, established conventions

- **Numbered-advice pattern:** `**N. Headline.** Description.` as its own
  paragraph — the build auto-converts runs of 2+ of these into a styled
  step list (`numbered_steps()` in build_site.py). Keep using this exact
  markdown shape for any new numbered advice; breaking the pattern loses
  the visual treatment silently, not with an error.
- **Every translated page carries the unvalidated-AI-translation banner**
  until a native speaker validates it (`validated_by` frontmatter field).
  Never remove the banner as part of a translation pass — only a real
  human validation removes it.
- **Phone numbers, hotline numbers, and URLs are never translated** —
  copied verbatim into every language.
- **Spanish uses *usted* throughout, never *tú*** — formal register,
  matches the site's existing 6 Spanish scam-type articles.
- **Cross-links point to the translated version of a target page when one
  exists, to the English original with a language annotation when it
  doesn't** (e.g. Spanish: "(en inglés)"). Getting this wrong silently
  sends a reader in language X back to an English page with no warning —
  check `scam_href()`-style existence logic in build_site.py rather than
  assuming a target is or isn't translated.
- **Register per language, once established, stays consistent**: Korean
  uses 존댓말 (formal/polite) throughout; each language's specific register
  choice should be confirmed against its own already-translated pages
  before adding new ones, not re-decided per page.

## What this file is not

This is not a banned-word list or a grammar checker — TBV's content is
short, direct, and specific by construction, and the "defend every
sentence" bar above does more work than a word blocklist would. Add a
specific rule here only when it's a real, standing decision (like the
Spanish register choice) — not a one-off preference for a single page.
