// Trust But Verify — family deck (for adult children / caregivers)
// node build/deck-family/make_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const QR_BLUE = path.join(__dirname, "..", "deck-assets", "qr-blue.png");
const QR_PAPER = path.join(__dirname, "..", "deck-assets", "qr-paper.png");

// printer-friendly variant: every slide gets a white/light background so an
// inkjet printer isn't laying full-bleed navy-black on half the pages
const PRINTER_FRIENDLY = process.env.PRINTER_FRIENDLY === "1";

// same palette + type system as the volunteer talk deck (build/make_deck.js)
const INK = "141414";
const PAPER = "FFFFFF";
const RED = "9E1B1B";
const GREY = "5A5A5A";
const BAND = "EFECE6";

const F = "Arial";
const W = 13.3, H = 7.5;
const M = 0.75;

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "The Trust But Verify Project";
p.title = "Trust But Verify — for family members";

// ---------- helpers ----------

// every slide carries the URL + a scannable QR — the color flips so it reads on either background
function footer(s, isDark) {
  s.addText("trustbutverifyproject.org", {
    x: M, y: 7.0, w: 6, h: 0.42, fontFace: F, fontSize: 12, color: isDark ? "9A958C" : GREY, margin: 0, valign: "middle",
  });
  s.addImage({ path: isDark ? QR_PAPER : QR_BLUE, x: W - M - 0.42, y: 6.98, w: 0.42, h: 0.42 });
}
// a "dark" slide's authored content (color: PAPER / "D8D4CC") assumes an ink
// background — in printer-friendly mode the background flips to white, so
// any such color must flip too, or the text becomes invisible
function onDark(color) {
  if (!PRINTER_FRIENDLY) return color;
  if (color === PAPER) return INK;
  if (color === "D8D4CC" || color === "9A958C") return GREY;
  return color;
}
function dark(notes) {
  const s = p.addSlide();
  const isDark = !PRINTER_FRIENDLY;
  s.background = { color: isDark ? INK : PAPER };
  if (notes) s.addNotes(notes);
  footer(s, isDark);
  return s;
}
function light(notes) {
  const s = p.addSlide();
  s.background = { color: PAPER };
  if (notes) s.addNotes(notes);
  footer(s, false);
  return s;
}
function title(s, text, opts) {
  s.addText(text, Object.assign({
    x: M, y: 0.55, w: W - M * 2, h: 1.2,
    fontFace: F, fontSize: 40, bold: true, color: INK, margin: 0,
    valign: "top",
  }, opts || {}));
}
// small caps eyebrow label above a slide's headline
function kicker(s, text, isDark) {
  s.addText(text.toUpperCase(), {
    x: M, y: 0.55, w: 10.5, h: 0.4, fontFace: F, fontSize: 14, bold: true,
    color: isDark ? onDark("D8D4CC") : GREY, charSpacing: 2, margin: 0,
  });
}
// numbered badge motif — a filled circle with a bold numeral, used for any
// ordered list (the same treatment the volunteer deck uses on "she is not
// foolish" and "it is not your fault")
function badge(s, n, x, y, size, color) {
  s.addShape(p.ShapeType.ellipse, { x, y, w: size, h: size, fill: { color: color || INK } });
  s.addText(String(n), { x, y, w: size, h: size, fontFace: F, fontSize: size * 40, bold: true, color: PAPER, align: "center", valign: "middle", margin: 0 });
}

// ---------- 1. title ----------
let s = dark(
  "Welcome. This isn't the same talk given to seniors themselves - this one is for the person who worries about a parent or grandparent. " +
  "The core message up front: this isn't about vigilance, and it isn't about your parent's competence. It's about one habit and one phone call. " +
  "Say your own name and why you're here - not as an expert, just someone who's watched this happen to people they know."
);
s.addText("PROTECTING THE PERSON YOU LOVE", {
  x: M, y: 1.75, w: W - M * 2, h: 0.6, fontFace: F, fontSize: 18, bold: true, color: onDark("D8D4CC"), charSpacing: 2, margin: 0,
});
s.addText("A guide for\nfamily members", {
  x: M, y: 2.4, w: W - M * 2, h: 2.5, fontFace: F, fontSize: 74, bold: true, color: onDark(PAPER), margin: 0, lineSpacing: 84,
});
s.addText("How to help someone you love without making them feel diminished.", {
  x: M, y: 4.95, w: 10, h: 0.8, fontFace: F, fontSize: 22, color: onDark("D8D4CC"), margin: 0, lineSpacing: 30,
});

// ---------- 2. origin / why this exists ----------
s = light(
  "Use a real story if you have one - local and specific beats generic every time, and never name anyone without permission. " +
  "The three short examples are all real, recent, and close to home. Pause after reading them. Let the room sit with 'none of them are foolish' before moving on - " +
  "that's the sentence that gives people permission to stop being embarrassed and start paying attention."
);
kicker(s, "Why this exists", false);
s.addText("“Grandma? I’m in trouble.\nPlease don’t tell Mom.”", {
  x: M, y: 1.1, w: W - M * 2, h: 1.9, fontFace: F, fontSize: 40, bold: true, italic: true, color: INK, margin: 0, lineSpacing: 50,
});
s.addText("She had $1,100 in a courier's hands within the hour. Her grandson was at work the whole time. He never knew until she told him that night.", {
  x: M, y: 2.95, w: 10.8, h: 0.9, fontFace: F, fontSize: 18, color: GREY, margin: 0, lineSpacing: 26,
});
const ORIGIN_ROWS = [
  ["A great-uncle", "took out a reverse mortgage — $300,000 of his house, gone."],
  ["A coworker's father", "was on the phone with “Microsoft,” being walked into his bank account."],
  ["A coworker's daughter", "sent money for months to a boyfriend she'd never met, “working in Oman.”"],
];
ORIGIN_ROWS.forEach((row, i) => {
  const y = 4.05 + i * 0.72;
  s.addShape(p.ShapeType.ellipse, { x: M, y: y + 0.1, w: 0.14, h: 0.14, fill: { color: INK } });
  s.addText([
    { text: row[0] + " — ", options: { bold: true, color: INK } },
    { text: row[1], options: { color: GREY } },
  ], { x: M + 0.35, y: y - 0.1, w: 10.8, h: 0.55, fontFace: F, fontSize: 18, valign: "top", margin: 0 });
});
s.addText("None of them are foolish. That's the whole point.", {
  x: M, y: 6.35, w: 10.8, h: 0.5, fontFace: F, fontSize: 22, bold: true, italic: true, color: INK, margin: 0,
});

// ---------- 3. reframe ----------
s = dark(
  "This is the single most important reframe in the whole talk. Say it slowly, and if you only remember one line from these notes, remember this one. " +
  "The families who catch it in time aren't the ones who scared their parent into being careful. They're the ones whose parent felt safe enough to call mid-call and say 'something feels off.'"
);
s.addText("The goal isn’t that she\nnever gets a scam call.", {
  x: M, y: 1.6, w: W - M * 2, h: 2.1, fontFace: F, fontSize: 50, bold: true, color: onDark(PAPER), margin: 0, lineSpacing: 62,
});
s.addText("She will get several this week.", {
  x: M, y: 3.65, w: W - M * 2, h: 0.7, fontFace: F, fontSize: 26, color: onDark("D8D4CC"), margin: 0,
});
s.addText("The goal is that she calls you during —\ninstead of telling nobody after.", {
  x: M, y: 4.7, w: W - M * 2, h: 1.6, fontFace: F, fontSize: 36, bold: true, color: onDark(PAPER), margin: 0, lineSpacing: 46,
});

// ---------- 4. the mistake almost everyone makes ----------
s = light(
  "Walk through the four boxes left to right - this is the failure mode almost every well-meaning family falls into. " +
  "The insight: the failure isn't a single bad conversation, it's a chain reaction that starts the moment the conversation feels evaluative. " +
  "Everything on the next few slides exists to avoid starting that chain."
);
kicker(s, "The mistake almost everyone makes", false);
const MISTAKE = [
  ["You warn.", "“Be careful, you're vulnerable.”"],
  ["They feel managed.", "The conversation felt like an assessment of their competence."],
  ["They stop mentioning it.", "Why invite another lecture?"],
  ["Six months later,", "you find out from a bank statement."],
];
const mColW = 2.75, mGap = 0.24, mX0 = M;
MISTAKE.forEach((pair, i) => {
  const x = mX0 + i * (mColW + mGap);
  const last = i === 3;
  s.addShape(p.ShapeType.rect, { x, y: 1.5, w: mColW, h: 2.9, fill: { color: BAND } });
  s.addText(String(i + 1), { x: x + 0.22, y: 1.68, w: 1, h: 0.7, fontFace: F, fontSize: 30, bold: true, color: last ? RED : INK, margin: 0 });
  s.addText(pair[0], { x: x + 0.22, y: 2.35, w: mColW - 0.44, h: 0.65, fontFace: F, fontSize: 17, bold: true, color: INK, margin: 0 });
  s.addText(pair[1], { x: x + 0.22, y: 3.0, w: mColW - 0.44, h: 1.2, fontFace: F, fontSize: 13.5, color: GREY, margin: 0, lineSpacing: 18 });
  if (!last) {
    s.addText("→", { x: x + mColW + 0.02, y: 2.65, w: mGap - 0.02, h: 0.5, fontFace: F, fontSize: 18, bold: true, color: GREY, align: "center", margin: 0 });
  }
});
s.addText("Every part of that chain starts with the first conversation feeling like an assessment of their competence. So don’t make it about them.", {
  x: M, y: 4.75, w: 10.8, h: 0.9, fontFace: F, fontSize: 21, bold: true, italic: true, color: INK, margin: 0, lineSpacing: 28,
});

// ---------- 5. openings that work ----------
s = light(
  "Read each quote out loud, in a normal conversational voice, not a performance voice - these are meant to sound like something you'd actually say at dinner. " +
  "The common thread across all three: none of them position the parent as the person being protected. They're all peer-to-peer."
);
kicker(s, "Openings that work", false);
title(s, "Ask for help instead of offering it", { y: 1.05, fontSize: 32 });
const OPENINGS = [
  ["“Mom, I almost got taken by a text about a package delivery last week. Have you been getting those?”", "Two adults comparing notes"],
  ["“I want us to have a family rule — nobody moves money on a call they didn’t start. Me included.”", "A household rule, not a personal one"],
  ["“The neighbor down the hall lost money to one of these. Would you look at this sheet and tell me if it’s clear?”", "Turns them into an ally, not a patient"],
];
OPENINGS.forEach((q, i) => {
  const y = 2.05 + i * 1.55;
  s.addShape(p.ShapeType.rect, { x: M, y, w: 11.8, h: 1.3, fill: { color: BAND } });
  s.addText(q[0], { x: M + 0.35, y: y + 0.16, w: 11.1, h: 0.75, fontFace: F, fontSize: 19, italic: true, color: INK, valign: "top", margin: 0 });
  s.addText(q[1], { x: M + 0.35, y: y + 0.9, w: 11.1, h: 0.36, fontFace: F, fontSize: 14, bold: true, color: RED, charSpacing: 0.5, margin: 0 });
});

// ---------- 6. four things worth setting up (1-2) ----------
s = light(
  "These four things (this slide has the first two, the next slide has the other two) are the actual to-do list. Everything before this was about the conversation; " +
  "this is what the conversation should lead to. The code word is the single highest-value four minutes available to any family - say that explicitly."
);
kicker(s, "Four things worth actually setting up", false);
title(s, "Skip the lectures. Do these.", { y: 1.05, fontSize: 32 });
const SETUP_1 = [
  ["1", "The code word", "One word the family uses to confirm identity. Not a birthday or a pet's name that's on Facebook — something from shared life that was never posted anywhere. Set it at a meal, out loud, with the grandchildren present. Four minutes. It defeats every voice-cloning scam that exists."],
  ["2", "“Call me first” — with a real reason", "“If anybody ever asks you for money, call me first, even at 3 a.m. Not because you can't handle it — because if it's real I want to be there for it, and if it's not I want to be the one who's annoyed instead of you.”"],
];
let sx = M;
SETUP_1.forEach((it) => {
  badge(s, it[0], sx, 2.1, 0.6, INK);
  s.addText(it[1], { x: sx + 0.85, y: 2.08, w: 5.15, h: 0.65, fontFace: F, fontSize: 20, bold: true, color: INK, margin: 0 });
  s.addText(it[2], { x: sx + 0.85, y: 2.72, w: 5.15, h: 3.6, fontFace: F, fontSize: 15.5, color: GREY, valign: "top", margin: 0, lineSpacing: 21 });
  sx += 6.0;
});

// ---------- 7. four things worth setting up (3-4) ----------
s = light(
  "Trusted contact and credit freeze are both boring, bureaucratic, and extremely effective - exactly the kind of unglamorous defense that actually works. " +
  "If the room only does one of these four things this week, it should be the code word; if they do two, add the trusted contact."
);
kicker(s, "Four things worth actually setting up", false);
title(s, "Two more, and they’re fast.", { y: 1.05, fontSize: 32 });
const SETUP_2 = [
  ["3", "A trusted contact at the bank", "Most banks let an account holder name a trusted contact — someone the bank can call if they see something alarming. No control over the account, no ability to move money. Just a phone call. Ten minutes at a branch."],
  ["4", "Credit freezes for everyone", "Free at all three bureaus, reversible, no downside if nobody's currently applying for a loan. Do yours at the same time — a shared errand, not an intervention."],
];
sx = M;
SETUP_2.forEach((it) => {
  badge(s, it[0], sx, 2.1, 0.6, INK);
  s.addText(it[1], { x: sx + 0.85, y: 2.08, w: 5.15, h: 0.65, fontFace: F, fontSize: 20, bold: true, color: INK, margin: 0 });
  s.addText(it[2], { x: sx + 0.85, y: 2.72, w: 5.15, h: 3.6, fontFace: F, fontSize: 15.5, color: GREY, valign: "top", margin: 0, lineSpacing: 21 });
  sx += 6.0;
});

// ---------- 8. if it's already happened ----------
s = dark(
  "This slide is worth slowing down for. All three 'not this' lines come from a place of love and fear, not cruelty - say that explicitly so nobody in the room feels attacked for having said one of them before. " +
  "Then: handle the logistics yourself if they'll let you, but let them keep decisions about their own money. Losing money AND losing authority over your own accounts in the same week is two losses, not one."
);
kicker(s, "If it's already happened", true);
s.addText("The first thing out of your mouth\ndecides the next ten years.", {
  x: M, y: 1.1, w: W - M * 2, h: 1.6, fontFace: F, fontSize: 34, bold: true, color: onDark(PAPER), margin: 0, lineSpacing: 44,
});
s.addShape(p.ShapeType.rect, { x: M, y: 2.95, w: 7.0, h: 1.5, fill: { color: BAND } });
s.addText("✓", { x: M + 0.3, y: 3.14, w: 0.5, h: 0.5, fontFace: F, fontSize: 24, bold: true, color: INK, margin: 0 });
s.addText("“I’m really glad you told me.\nLet’s fix what we can.”", {
  x: M + 0.9, y: 3.1, w: 5.8, h: 1.2, fontFace: F, fontSize: 20, italic: true, bold: true, color: INK, valign: "top", margin: 0, lineSpacing: 26,
});
s.addShape(p.ShapeType.rect, { x: M, y: 4.65, w: 7.0, h: 1.75, fill: { color: BAND } });
s.addText("✕", { x: M + 0.3, y: 4.84, w: 0.5, h: 0.5, fontFace: F, fontSize: 24, bold: true, color: RED, margin: 0 });
s.addText("“Why didn’t you call me?” — “How could you not see it?” — “I told you about this.”", {
  x: M + 0.9, y: 4.82, w: 5.8, h: 1.4, fontFace: F, fontSize: 16, italic: true, color: INK, valign: "top", margin: 0, lineSpacing: 22,
});
s.addText("All three teach the person to never tell you again — and there’s very likely to be a next time. People scammed once are deliberately targeted again.", {
  x: 8.3, y: 2.95, w: 4.0, h: 3.4, fontFace: F, fontSize: 17, color: onDark("D8D4CC"), valign: "top", margin: 0, lineSpacing: 24,
});

// ---------- 9. capacity concern ----------
s = light(
  "This is the slide for the harder conversation - not every family in the room needs it today, but some do, and they're often too embarrassed to ask afterward. " +
  "Say plainly: doing this early, while everyone can participate in the decision, is far kinder than doing it during a crisis."
);
kicker(s, "When it's more than one scam call", false);
title(s, "Sometimes it’s a pattern, not an incident.", { y: 1.05, fontSize: 30 });
s.addText("Repeated payments. New secrecy. A new “friend” on the phone. Confusion about transactions that were once routine. That’s a different problem, and it needs more than a website.", {
  x: M, y: 1.85, w: 11.2, h: 0.85, fontFace: F, fontSize: 18, color: GREY, margin: 0, lineSpacing: 25,
});
const RESOURCES = [
  ["Their doctor", "A cognitive check — financial mistakes are sometimes the earliest visible symptom, showing up before memory complaints do."],
  ["Eldercare Locator", "800-677-1116 — connects you to local aging services."],
  ["Adult Protective Services", "If you believe someone is being financially exploited, particularly by a caregiver or new acquaintance."],
  ["An elder law attorney", "If powers of attorney need looking at."],
];
RESOURCES.forEach((row, i) => {
  const y = 3.05 + i * 0.9;
  s.addShape(p.ShapeType.ellipse, { x: M, y: y + 0.1, w: 0.14, h: 0.14, fill: { color: INK } });
  s.addText([
    { text: row[0] + " — ", options: { bold: true, color: INK } },
    { text: row[1], options: { color: GREY } },
  ], { x: M + 0.35, y: y - 0.14, w: 11.0, h: 0.75, fontFace: F, fontSize: 16.5, valign: "top", margin: 0, lineSpacing: 21 });
});

// ---------- 10. check yourself ----------
s = dark(
  "Short slide, but don't skip it - it's often the moment people relax, because it reframes the whole talk from 'protect a vulnerable person' to 'this is just how our family handles money now.' " +
  "That reframe is what makes the habit stick instead of feeling like surveillance."
);
s.addText("Whatever rule you set for your\nmother — follow it yourself.", {
  x: M, y: 2.0, w: W - M * 2, h: 2.0, fontFace: F, fontSize: 44, bold: true, color: onDark(PAPER), margin: 0, lineSpacing: 56,
});
s.addText("Out loud, where she can see. The fastest-growing victim group by percentage isn’t older adults — it’s younger people. They just lose smaller amounts, because they have less.", {
  x: M, y: 4.15, w: 10.2, h: 1.1, fontFace: F, fontSize: 20, color: onDark("D8D4CC"), margin: 0, lineSpacing: 28,
});
s.addText("That’s what makes it a family standard — not a supervision plan.", {
  x: M, y: 5.45, w: 10.2, h: 0.7, fontFace: F, fontSize: 24, bold: true, italic: true, color: onDark(PAPER), margin: 0,
});

// ---------- 11. what success looks like ----------
s = light(
  "Close on this image deliberately. The whole talk has been building toward this one picture of what success feels like day to day - ordinary, not dramatic. " +
  "Let it sit for a second before moving to the resources slide."
);
kicker(s, "What success actually looks like", false);
s.addText("“Someone called me about my account\nand I told them I’d call the bank myself.”", {
  x: M, y: 1.5, w: W - M * 2, h: 1.9, fontFace: F, fontSize: 36, bold: true, italic: true, color: INK, margin: 0, lineSpacing: 46,
});
s.addText("Said the way you’d mention taking out the trash.", {
  x: M, y: 3.45, w: 9, h: 0.6, fontFace: F, fontSize: 20, color: GREY, margin: 0,
});
s.addText("Not vigilance. Not worry. Just a habit she has, that she’s a little proud of, that she’ll pass along to a friend down the hall.", {
  x: M, y: 4.35, w: 10.3, h: 1.1, fontFace: F, fontSize: 22, color: INK, margin: 0, lineSpacing: 30,
});

// ---------- 12. resources / close ----------
s = dark(
  "Close with the phone numbers and the URL up on screen long enough for people to photograph it. " +
  "Remind the room: this whole deck is free to take, copy, retitle, and give again - encourage them to send it to a sibling who couldn't be here, not just keep it to themselves."
);
s.addText("Free help, no judgment", { x: M, y: 0.75, w: 9, h: 0.7, fontFace: F, fontSize: 34, bold: true, color: onDark(PAPER), margin: 0 });
const PHONES = [
  ["833-372-8311", "National Elder Fraud Hotline · Mon–Fri"],
  ["877-908-3360", "AARP Fraud Watch · Mon–Fri"],
  ["800-677-1116", "Eldercare Locator"],
];
let py = 1.85;
PHONES.forEach(([num, label]) => {
  s.addText(num, { x: M, y: py, w: 4.0, h: 0.6, fontFace: F, fontSize: 30, bold: true, color: onDark(PAPER), margin: 0 });
  s.addText(label, { x: M + 4.35, y: py + 0.1, w: 6, h: 0.5, fontFace: F, fontSize: 18, color: onDark("D8D4CC"), valign: "middle", margin: 0 });
  py += 0.8;
});
s.addText("Everything in this deck, plus the full site — fridge sheets, scam-by-scam guides, and the family conversation guide this deck is drawn from:", {
  x: M, y: 4.85, w: 8.5, h: 0.9, fontFace: F, fontSize: 16, color: onDark("D8D4CC"), margin: 0, lineSpacing: 22,
});
s.addText("trustbutverifyproject.org/for-family", {
  x: M, y: 5.7, w: 8.5, h: 0.55, fontFace: F, fontSize: 24, bold: true, color: onDark(PAPER), margin: 0,
});
s.addText("Free, CC BY-NC — fine for nursing homes and senior centers. Credit us; don't resell it.", {
  x: M, y: 6.4, w: 10.5, h: 0.45, fontFace: F, fontSize: 13, italic: true, color: onDark("9A958C"), margin: 0,
});

const OUT_NAME = PRINTER_FRIENDLY ? "trust-but-verify-for-family-printer-friendly.pptx" : "trust-but-verify-for-family.pptx";
p.writeFile({ fileName: path.join(__dirname, "..", "..", "formats", "talk", OUT_NAME) })
  .then(f => console.log("wrote", f));
