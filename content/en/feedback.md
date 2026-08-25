---
title: Feedback
slug: /feedback
description: Something wrong, out of date, or unclear? Tell us. No account, no login, just a message.
lang: en
---

# Feedback

Found something wrong, out of date, confusing, or missing? Tell us. This goes
straight to the maintainer's inbox — nothing is stored, and nothing is added
to any list.

Prefer email? **translations [at] trustbutverifyproject [dot] org** reaches the same
place.

<form class="feedback-form" method="POST" action="/api/feedback">
<p class="hp" aria-hidden="true">
<label for="website">Leave this field blank</label>
<input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
</p>

<p>
<label for="message"><strong>What's wrong or what would help?</strong></label><br>
<textarea id="message" name="message" rows="6" required maxlength="5000"></textarea>
</p>

<p>
<label for="email">Your email, if you'd like a reply <em>(optional)</em></label><br>
<input type="email" id="email" name="email" maxlength="200">
</p>

<p><button type="submit">Send</button></p>
</form>

## What happens to what you write

It's emailed to the person who maintains this site, read by a person, and
not stored anywhere else — no database, no analytics, no mailing list. See
the full [privacy policy](/privacy).

---

**Related:** [Help translate a page](/help-translate) ·
[Privacy policy](/privacy)
