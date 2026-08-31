# Council of Experts — Trust But Verify
**Convened 2026-08-30.** Six personas debating the highest-value next moves
across extend/improve, secure, reach, and content quality.

Nothing in this document has been shipped. Recommendations touching safety
content are flagged for Brett and were deliberately not executed.

---

## Ground truth put in front of the council

Measured from the repo, not assumed. Several of these disprove worries the
council would otherwise have spent its time on.

| | |
|---|---|
| Pages built | 196, across 45 languages |
| English content | 58 files, 18,134 words |
| Deep languages (es, vi, zh, ru, ko) | 12 files each |
| Thin languages | 39, at 2 files each (landing page + phishing) |
| Non-English pages validated by a native speaker | **0 of 138** |
| Non-English files missing the UNVALIDATED banner | **0** (all 138 carry it) |
| Phone numbers in translations absent from the English set | **0** |
| Broken internal links sitewide | **0** |
| `/right-now` (the mid-scam-call page) | present in **6** of 45 languages |
| English median reading grade | **6.3** |
| `home.md` reading grade | **10.5** |
| `/right-now` reading grade | **4.3** |
| Feedback form | broken for every visitor since launch (no `RESEND_API_KEY`) |
| Analytics | never confirmed enabled |
| Audit harness | 0 errors, 11 warnings |

**Two worries were tested and dismissed before the debate.** Unvalidated AI
translation has *not* corrupted any helpline number: every phone number across
all 44 non-English languages appears in the English set. And every one of the
138 non-English files carries its in-language warning banner. The translation
risk is real, but it is a *prose* risk rather than a *data* risk, which changes
what to do about it.

---

## The council

- **Dr. Amara Osei** — geriatric fraud-prevention researcher. Studies how
  victimisation actually unfolds, not how it is described afterwards.
- **Ruth Delgado** — plain-language and editorial lead, ex-newspaper standards
  desk. Cares about comprehension under stress.
- **Kwame Boateng** — accessibility engineer and daily screen-reader user.
- **Mei-Lin Chow** — localisation director, has shipped safety content in 30+
  languages.
- **Judith Farrow** — trust-and-safety skeptic. Her brief is to find the way
  this site hurts somebody.
- **Tomas Reid** — reach and distribution strategist, nonprofit sector.

---

## The debate

### Opening: what is this site for?

**Amara.** Before anything gets ranked, the audience needs stating precisely,
because the whole list changes depending on the answer. This site is not for
people researching fraud. It is for a 78-year-old on the phone *right now* with
someone claiming to be their grandson, and for the adult daughter who finds out
on Sunday. Those are two different products sharing a domain.

**Tomas.** And neither of them arrives by searching "grandparent scam." That is
the fiction I want to kill early. Nobody in crisis Googles a taxonomy. They are
handed a piece of paper by a librarian, or their daughter texts them a link.

**Ruth.** Then let me put the most uncomfortable number on the table. The median
page reads at grade 6.3, which is genuinely good work. `/right-now`, the crisis
page, reads at 4.3, which is excellent and exactly right. But `home.md` reads at
**10.5**. The front door is the second-hardest page on the entire site, harder
than either blog post, and more than four grades harder than the page that
actually saves someone.

**Amara.** That is worse than it sounds, because comprehension collapses under
adrenaline. A grade-10 sentence read by a frightened person is not a grade-10
sentence any more.

**Judith.** I will accept that as the strongest finding so far, and I have not
even started.

### The translations

**Judith.** Here is my brief. This site publishes safety advice in 44 languages
that **no human has ever read**. 138 pages. Zero validated. To an audience
selected for vulnerability. If one of those pages inverts an instruction — if
"never say the code aloud" becomes "always say the code" in Amharic — a person
loses their savings and the site caused it.

**Mei-Lin.** I want to be careful, because that is a real risk stated in an
unreal way. The council checked. Every phone number is correct. Every page
carries a warning banner in its own language. Machine translation in 2026 does
not typically invert imperatives; it degrades in register and idiom. The
plausible failure is a page that reads oddly and loses trust, not a page that
tells someone to hand over the code.

**Judith.** "Does not typically" is doing enormous work in that sentence, and
nobody has looked at even one page to check.

**Mei-Lin.** Agreed, and that is the actual gap. But your implied remedy —
withhold until validated — has a body count too. Somebody who reads only
Tagalog gets nothing at all while we wait for a volunteer who may never arrive.
Imperfect guidance in your own language beats perfect guidance you cannot read.

**Judith.** Then at minimum the banner should say what it means. Right now it
says, in effect, "not reviewed, do not print." It does not say "this might be
wrong." Those are different warnings and only one of them is honest.

**Mei-Lin.** That I will concede. The banner is written for a distributor, not
for a reader.

**Ruth.** Which is a copy problem, and it is copy on safety pages, so it is not
ours to fix. Flag it.

> **FLAGGED FOR BRETT — not executed.** Rewording the UNVALIDATED banner is a
> change to safety content in 44 languages. The council believes the current
> wording addresses the wrong reader, but this is Brett's call and would need
> native-speaker review to ship.

### The inverted priority

**Amara.** Something in the language rollout is backwards, and I think it is the
single most actionable thing here. `/right-now` — the page for the person
mid-call — exists in 6 languages. The *landing page* exists in 45.

**Mei-Lin.** So a Tagalog speaker gets a homepage and one phishing article, but
not the page for the moment it is actually happening.

**Amara.** The value per visit is not remotely comparable. A landing page in
your language is hospitality. The crisis page is the intervention. We have
translated the hospitality 45 times and the intervention 6 times.

**Tomas.** That is the ranking argument I would make from distribution too. If a
librarian hands out one URL, it should be that one.

**Judith.** No objection. This is the rare case where the highest-value move and
the lowest-risk move are the same page, because `/right-now` is short and mostly
imperative — the register machine translation handles best.

### Reach

**Tomas.** My turn. Everything above assumes people arrive. Nothing establishes
that anyone does. Analytics were never confirmed on, and the feedback form has
been broken for every visitor since launch. This project has no idea whether it
has ever helped one person.

**Ruth.** That reframes the whole list. Every ranking we produce below that line
is informed guesswork.

**Tomas.** It is worse than guesswork, it is unfalsifiable. And the fix is not
mine to make; it is two dashboard actions only Brett can do. But note the second
one: the feedback form is the only channel by which a native speaker could tell
us a translation is wrong. Judith's 138-page risk and my measurement gap are the
same missing pipe.

**Judith.** That is a good point and I will steal it. The validation programme
cannot start until the form works.

**Kwame.** Then the cheap intermediate is a fallback that does not depend on an
API key at all. A plain mail link works with no service, no secret, no server.

### Accessibility

**Kwame.** Mine is short, but I do not want it minimised. The automated checks
pass, the landmarks are real, the heading order is fixed. None of that tells you
whether the site is *usable* with a screen reader, because no human has ever
tried. Automated tooling catches maybe a third of real barriers.

**Amara.** And this audience skews to low vision at exactly the same rate it
skews to fraud targeting. They are the same cohort.

**Kwame.** Right. Audio narration exists, which is genuinely ahead of most
sites, but in 6 languages — mirroring the same inversion Amara found. I would
not rank a VoiceOver pass above the crisis-page translations, but it is the
highest-value thing needing a human hour rather than a budget.

### The adversarial angle

**Judith.** Last one, and nobody has raised it. This site teaches people to
verify everything they are told. It does not teach them to verify *it*. A
scammer who clones this site with one helpline number changed has built a
near-perfect trap for precisely this audience: the victim believes they are
doing the safe thing at the moment they are being robbed.

**Amara.** That is not hypothetical. Recovery scams already work by
impersonating the help.

**Tomas.** The printed materials help here, oddly. A fridge sheet with the real
domain is a physical anchor that cannot be cloned by SEO.

**Judith.** Partly. But there is still no DMARC record, so nothing stops mail
being spoofed from the domain today.

> **FLAGGED FOR BRETT — not executed.** A "how to know you're on the real site"
> note is new safety-adjacent content and should not be drafted without Brett.
> The missing DMARC record is already open item #5 in BACKLOG.md and is a
> dashboard action only Brett can take.

### Closing disagreement

**Ruth.** I want the record to show the council did not reach consensus on one
thing. Judith holds that 138 unvalidated safety pages is the site's largest
liability. Mei-Lin holds that withdrawing them would harm more people than it
protects. Both positions are coherent. It is a values call, not a technical one,
and it belongs to Brett.

**Judith.** Accurate. I would add only that the site's own validation-status page
already publishes this honestly, which is more than most projects would do.

---

## Ranked recommendations

Ranked by expected harm prevented per unit of effort.

**1. Restore measurement. The project cannot tell whether it works.** — *Brett*
No confirmed analytics; feedback form broken for 100% of visitors since launch.
Also the only channel through which a native speaker could report a bad
translation, so it blocks recommendation 4 as well.
Brett-only: set `RESEND_API_KEY`, confirm Cloudflare Web Analytics.
*Partly executable:* a mail-link fallback that works with no API key at all.

**2. Simplify the homepage. The front door is the hardest page on the site.** — *executable*
Grade 10.5 against a site median of 6.3 and a crisis page at 4.3. Also the
second-stiffest page by contraction rate. The page deciding whether a frightened
person stays is written four grades above the page that helps them. English,
non-safety, review-gated.

**3. Translate the crisis page before anything else.** — *Brett, cost*
`/right-now` is in 6 languages; the landing page is in 45. Highest value per
visit, shortest page, mostly imperative and therefore also the lowest
translation risk. Should precede any new scam article in any language.

**4. Start validation with one language, not a programme.** — *Brett*
Zero of 138 pages validated. A single validated language proves the pipeline and
gives `learn_from_edits.py` its first real signal. Blocked behind 1.

**5. Lock in the invariants that are currently clean.** — *executable*
Phone numbers correct in all 44 languages, banners present on all 138 files,
zero broken links. All true today, none enforced. Cheap insurance, no content
change.

**6. Fix the 8 over-long page titles.** — *executable*
Truncated in search results and link previews, which is where the adult-child
audience actually encounters the site. Metadata only.

**7. A human screen-reader pass.** — *Brett, one hour*
Automated checks catch roughly a third of real barriers. Same cohort as the
fraud target.

**8. Reword the UNVALIDATED banner to address readers, not distributors.** — *FLAGGED, not executed*
Safety content in 44 languages. Council split on urgency, unanimous that the
current wording addresses the wrong person.

**9. Teach people to verify this site.** — *FLAGGED, not executed*
A cloned site with one changed number is a near-perfect trap for this audience.
New safety-adjacent content, plus the open DMARC item.
