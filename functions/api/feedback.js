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

const TO_ADDRESS = "translations@trustbutverifyproject.org";
const FROM_ADDRESS = "Trust But Verify <feedback@trustbutverifyproject.org>";
const SITE = "https://trustbutverifyproject.org";

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = await request.formData();
  } catch {
    return new Response("Bad request", { status: 400 });
  }

  // Honeypot: a hidden field real visitors never see or fill in.
  if (String(form.get("website") || "").trim() !== "") {
    return Response.redirect(SITE + "/feedback/thanks/", 303);
  }

  const message = String(form.get("message") || "").trim();
  const email = String(form.get("email") || "").trim();

  if (!message || message.length > 5000 || email.length > 200) {
    return Response.redirect(SITE + "/feedback/?error=1", 303);
  }

  if (!env.RESEND_API_KEY) {
    return new Response("Feedback form is not configured yet.", { status: 503 });
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
    return Response.redirect(SITE + "/feedback/?error=1", 303);
  }

  return Response.redirect(SITE + "/feedback/thanks/", 303);
}

export async function onRequestGet() {
  return Response.redirect(SITE + "/feedback/", 303);
}
