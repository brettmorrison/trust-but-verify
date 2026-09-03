// Cloudflare Pages Function — backend for /feedback.
//
// No database, no storage, no cookies: the message is read from the
// submitted form and forwarded by email via Resend, then discarded.
// Requires a RESEND_API_KEY secret set in the Pages project (dashboard ->
// Settings -> Environment variables -> add as "Secret", Production).
// See DEPLOY.md for the one-time setup this needs.
//
// Spam defense is a honeypot field, not Turnstile: Turnstile needs
// client-side JavaScript, which this site's CSP does not allow anywhere.

// The addresses stay hardcoded on purpose -- mail always goes to the real
// project inbox from the real verified sending domain, whichever deploy is
// running. Redirect targets are the opposite: they are derived from the
// request, so a submission on a *.pages.dev preview lands on that preview's
// own thanks/error page instead of bouncing the tester to production, which
// made a preview look like it worked when it had not.
const TO_ADDRESS = "translations@trustbutverifyproject.org";
const FROM_ADDRESS = "Trust But Verify <feedback@trustbutverifyproject.org>";

const originOf = (request) => new URL(request.url).origin;

export async function onRequestPost({ request, env }) {
  const site = originOf(request);
  let form;
  try {
    form = await request.formData();
  } catch {
    return new Response("Bad request", { status: 400 });
  }

  // Honeypot: a hidden field real visitors never see or fill in.
  if (String(form.get("website") || "").trim() !== "") {
    return Response.redirect(site + "/feedback/thanks/", 303);
  }

  const message = String(form.get("message") || "").trim();
  const email = String(form.get("email") || "").trim();

  const emailLooksValid = !email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!message || message.length > 5000 || email.length > 200 || !emailLooksValid) {
    return Response.redirect(site + "/feedback/error/", 303);
  }

  if (!env.RESEND_API_KEY) {
    return Response.redirect(site + "/feedback/error/", 303);
  }

  const body = {
    from: FROM_ADDRESS,
    to: [TO_ADDRESS],
    subject: "Feedback from trustbutverifyproject.org",
    text: message + "\n\n---\nReply-to: " + (email || "(not given)"),
  };
  if (email) body.reply_to = email;

  const resp = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + env.RESEND_API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    return Response.redirect(site + "/feedback/error/", 303);
  }

  return Response.redirect(site + "/feedback/thanks/", 303);
}

export async function onRequestGet({ request }) {
  return Response.redirect(originOf(request) + "/feedback/", 303);
}
