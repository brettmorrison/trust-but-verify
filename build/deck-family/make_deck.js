const pptxgen = require("pptxgenjs");

const NAVY = "16324F";
const NAVY_DEEP = "0E2138";
const WHITE = "FFFFFF";
const INK = "1B2430";
const MUTED = "5B6672";
const AMBER = "E0973D";
const PAPER = "F7F6F3";
const LINE = "D9DDE1";

function deck() {
  const p = new pptxgen();
  p.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
  return p;
}

function darkSlide(p) {
  const s = p.addSlide();
  s.background = { color: NAVY_DEEP };
  return s;
}
function lightSlide(p) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  return s;
}

function kicker(s, text, color) {
  s.addText(text.toUpperCase(), {
    x: 0.6, y: 0.5, w: 9, h: 0.4,
    fontFace: "Calibri", fontSize: 12, bold: true,
    color: color || AMBER, charSpacing: 2,
  });
}

function pageNum(s, n, dark) {
  s.addText(String(n), {
    x: 12.5, y: 7.05, w: 0.6, h: 0.35,
    fontFace: "Calibri", fontSize: 10, color: dark ? "5B7186" : "A9B0B8",
    align: "right",
  });
}

const p = deck();

// ---------------------------------------------------------------- Slide 1
{
  const s = darkSlide(p);
  s.addText("PROTECTING THE PERSON YOU LOVE", {
    x: 0.9, y: 2.5, w: 11.5, h: 0.5,
    fontFace: "Calibri", fontSize: 14, bold: true, color: AMBER, charSpacing: 2,
  });
  s.addText("A guide for family members", {
    x: 0.85, y: 2.95, w: 11.5, h: 1.3,
    fontFace: "Cambria", fontSize: 44, bold: true, color: WHITE,
  });
  s.addText("How to help someone you love without making them feel diminished", {
    x: 0.9, y: 4.15, w: 10, h: 0.6,
    fontFace: "Calibri", fontSize: 17, color: "AEB9C4",
  });
  s.addText("trustbutverifyproject.org  ·  Free, public domain, no sponsors", {
    x: 0.9, y: 6.7, w: 10, h: 0.4,
    fontFace: "Calibri", fontSize: 11, color: "6F7E8C",
  });
  s.addNotes(
    "Welcome. This isn't the same talk given to seniors themselves - this one is for the person who worries about a parent or grandparent. " +
    "The core message up front: this isn't about vigilance, and it isn't about your parent's competence. It's about one habit and one phone call. " +
    "Say your own name and why you're here - not as an expert, just someone who's watched this happen to people they know."
  );
}

// ---------------------------------------------------------------- Slide 2 - origin
{
  const s = lightSlide(p);
  kicker(s, "Why this exists", NAVY);
  s.addText(
    "“Grandma? I’m in trouble. Please don’t tell Mom.”",
    { x: 0.9, y: 1.3, w: 11.2, h: 1.1, fontFace: "Cambria", fontSize: 32, bold: true, italic: true, color: INK }
  );
  s.addText("She had $1,100 in a courier's hands within the hour. Her grandson was at work the whole time. He never knew until she told him that night.",
    { x: 0.9, y: 2.5, w: 8.6, h: 1.1, fontFace: "Calibri", fontSize: 16, color: MUTED });

  const rows = [
    ["A great-uncle", "took out a reverse mortgage — $300,000 of his house, gone."],
    ["A coworker's father", "was on the phone with “Microsoft,” being walked into his bank account."],
    ["A coworker's daughter", "sent money for months to a boyfriend she'd never met, “working in Oman.”"],
  ];
  let y = 4.0;
  rows.forEach(([who, what]) => {
    s.addShape("ellipse", { x: 0.9, y: y + 0.05, w: 0.12, h: 0.12, fill: { color: AMBER }, line: { type: "none" } });
    s.addText([{ text: who + " — ", options: { bold: true, color: INK } }, { text: what, options: { color: MUTED } }],
      { x: 1.2, y: y - 0.15, w: 10.8, h: 0.5, fontFace: "Calibri", fontSize: 14.5, valign: "top" });
    y += 0.62;
  });
  s.addText("None of them are foolish. That's the whole point.", {
    x: 0.9, y: 6.15, w: 10.5, h: 0.5, fontFace: "Cambria", fontSize: 17, italic: true, color: NAVY,
  });
  pageNum(s, 2, false);
  s.addNotes(
    "Use a real story if you have one - local and specific beats generic every time, and never name anyone without permission. " +
    "The three short examples are all real, recent, and close to home. Pause after reading them. Let the room sit with 'none of them are foolish' before moving on - " +
    "that's the sentence that gives people permission to stop being embarrassed and start paying attention."
  );
}

// ---------------------------------------------------------------- Slide 3 - reframe
{
  const s = darkSlide(p);
  s.addText("The goal isn't that she never gets a scam call.", {
    x: 0.9, y: 2.3, w: 11.4, h: 1.0, fontFace: "Cambria", fontSize: 34, bold: true, color: WHITE,
  });
  s.addText("She will get several this week.", {
    x: 0.9, y: 3.25, w: 11.4, h: 0.6, fontFace: "Calibri", fontSize: 19, color: "9FB2C4",
  });
  s.addShape("line", { x: 0.9, y: 4.15, w: 4.2, h: 0, line: { color: "35485C", width: 1 } });
  s.addText("The goal is that she calls you during — instead of telling nobody after.", {
    x: 0.9, y: 4.4, w: 10.5, h: 0.8, fontFace: "Cambria", fontSize: 24, bold: true, color: AMBER,
  });
  pageNum(s, 3, true);
  s.addNotes(
    "This is the single most important reframe in the whole talk. Say it slowly, and if you only remember one line from these notes, remember this one. " +
    "The families who catch it in time aren't the ones who scared their parent into being careful. They're the ones whose parent felt safe enough to call mid-call and say 'something feels off.'"
  );
}

// ---------------------------------------------------------------- Slide 4 - the mistake
{
  const s = lightSlide(p);
  kicker(s, "The mistake almost everyone makes", NAVY);
  const steps = [
    ["You warn.", "“Be careful, you're vulnerable.”"],
    ["They feel managed.", "The conversation felt like an assessment of their competence."],
    ["They stop mentioning it.", "Why invite another lecture?"],
    ["Six months later,", "you find out from a bank statement."],
  ];
  const colW = 2.85, gap = 0.25, x0 = 0.9;
  steps.forEach((pair, i) => {
    const x = x0 + i * (colW + gap);
    s.addShape("roundRect", { x, y: 1.5, w: colW, h: 2.5, rectRadius: 0.08,
      fill: { color: i === 3 ? "FBEEDD" : PAPER }, line: { color: LINE, width: 1 } });
    s.addText(String(i + 1), { x: x + 0.2, y: 1.65, w: 1, h: 0.6, fontFace: "Cambria", fontSize: 26, bold: true, color: i === 3 ? AMBER : NAVY });
    s.addText(pair[0], { x: x + 0.2, y: 2.35, w: colW - 0.4, h: 0.6, fontFace: "Calibri", fontSize: 14.5, bold: true, color: INK });
    s.addText(pair[1], { x: x + 0.2, y: 2.95, w: colW - 0.4, h: 1.0, fontFace: "Calibri", fontSize: 12, color: MUTED });
    if (i < 3) {
      s.addText("→", { x: x + colW + 0.02, y: 2.5, w: gap - 0.02, h: 0.5, fontFace: "Calibri", fontSize: 16, color: "9AA5AF", align: "center" });
    }
  });
  s.addText("Every part of that chain starts with the first conversation feeling like an assessment of their competence. So don't make it about them.", {
    x: 0.9, y: 4.5, w: 10.8, h: 0.8, fontFace: "Cambria", fontSize: 18, italic: true, color: NAVY,
  });
  pageNum(s, 4, false);
  s.addNotes(
    "Walk through the four boxes left to right - this is the failure mode almost every well-meaning family falls into. " +
    "The insight: the failure isn't a single bad conversation, it's a chain reaction that starts the moment the conversation feels evaluative. " +
    "Everything on the next few slides exists to avoid starting that chain."
  );
}

// ---------------------------------------------------------------- Slide 5 - openings that work
{
  const s = lightSlide(p);
  kicker(s, "Openings that work", NAVY);
  s.addText("Ask for help instead of offering it", { x: 0.9, y: 1.25, w: 11, h: 0.5, fontFace: "Cambria", fontSize: 22, bold: true, color: INK });

  const quotes = [
    "“Mom, I almost got taken by a text about a package delivery last week. Have you been getting those?”",
    "“I want us to have a family rule — nobody moves money on a call they didn't start. Me included.”",
    "“The neighbor down the hall lost money to one of these. Would you look at this sheet and tell me if it's clear?”",
  ];
  const labels = ["Two adults comparing notes", "A household rule, not a personal one", "Turns them into an ally, not a patient"];
  let y = 2.1;
  quotes.forEach((q, i) => {
    s.addShape("roundRect", { x: 0.9, y, w: 11.3, h: 1.35, rectRadius: 0.06, fill: { color: PAPER }, line: { type: "none" } });
    s.addText(q, { x: 1.2, y: y + 0.12, w: 10.7, h: 0.75, fontFace: "Cambria", fontSize: 15.5, italic: true, color: INK, valign: "top" });
    s.addText(labels[i], { x: 1.2, y: y + 0.92, w: 10.7, h: 0.35, fontFace: "Calibri", fontSize: 11.5, bold: true, color: AMBER, charSpacing: 0.5 });
    y += 1.55;
  });
  pageNum(s, 5, false);
  s.addNotes(
    "Read each quote out loud, in a normal conversational voice, not a performance voice - these are meant to sound like something you'd actually say at dinner. " +
    "The common thread across all three: none of them position the parent as the person being protected. They're all peer-to-peer."
  );
}

// ---------------------------------------------------------------- Slide 6 - four things to set up (part 1)
{
  const s = lightSlide(p);
  kicker(s, "Four things worth actually setting up", NAVY);
  s.addText("Skip the lectures. Do these.", { x: 0.9, y: 1.2, w: 10, h: 0.5, fontFace: "Cambria", fontSize: 22, bold: true, color: INK });

  const items = [
    ["1", "The code word", "One word the family uses to confirm identity. Not a birthday or a pet's name that's on Facebook — something from shared life that was never posted anywhere. Set it at a meal, out loud, with the grandchildren present. Four minutes. It defeats every voice-cloning scam that exists."],
    ["2", "“Call me first” — with a real reason", "“If anybody ever asks you for money, call me first, even at 3 a.m. Not because you can't handle it — because if it's real I want to be there for it, and if it's not I want to be the one who's annoyed instead of you.”"],
  ];
  let x = 0.9;
  items.forEach((it) => {
    s.addShape("ellipse", { x, y: 2.15, w: 0.55, h: 0.55, fill: { color: NAVY }, line: { type: "none" } });
    s.addText(it[0], { x, y: 2.15, w: 0.55, h: 0.55, fontFace: "Cambria", fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle" });
    s.addText(it[1], { x: x + 0.75, y: 2.12, w: 5.15, h: 0.5, fontFace: "Calibri", fontSize: 15.5, bold: true, color: INK });
    s.addText(it[2], { x: x + 0.75, y: 2.62, w: 5.15, h: 3.3, fontFace: "Calibri", fontSize: 12.5, color: MUTED, valign: "top" });
    x += 6.0;
  });
  pageNum(s, 6, false);
  s.addNotes(
    "These four things (this slide has the first two, the next slide has the other two) are the actual to-do list. Everything before this was about the conversation; " +
    "this is what the conversation should lead to. The code word is the single highest-value four minutes available to any family - say that explicitly."
  );
}

// ---------------------------------------------------------------- Slide 7 - four things part 2
{
  const s = lightSlide(p);
  kicker(s, "Four things worth actually setting up", NAVY);
  s.addText("Two more, and they're fast.", { x: 0.9, y: 1.2, w: 10, h: 0.5, fontFace: "Cambria", fontSize: 22, bold: true, color: INK });

  const items = [
    ["3", "A trusted contact at the bank", "Most banks let an account holder name a trusted contact — someone the bank can call if they see something alarming. No control over the account, no ability to move money. Just a phone call. Ten minutes at a branch."],
    ["4", "Credit freezes for everyone", "Free at all three bureaus, reversible, no downside if nobody's currently applying for a loan. Do yours at the same time — a shared errand, not an intervention."],
  ];
  let x = 0.9;
  items.forEach((it) => {
    s.addShape("ellipse", { x, y: 2.15, w: 0.55, h: 0.55, fill: { color: NAVY }, line: { type: "none" } });
    s.addText(it[0], { x, y: 2.15, w: 0.55, h: 0.55, fontFace: "Cambria", fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle" });
    s.addText(it[1], { x: x + 0.75, y: 2.12, w: 5.15, h: 0.5, fontFace: "Calibri", fontSize: 15.5, bold: true, color: INK });
    s.addText(it[2], { x: x + 0.75, y: 2.62, w: 5.15, h: 3.3, fontFace: "Calibri", fontSize: 12.5, color: MUTED, valign: "top" });
    x += 6.0;
  });
  pageNum(s, 7, false);
  s.addNotes(
    "Trusted contact and credit freeze are both boring, bureaucratic, and extremely effective - exactly the kind of unglamorous defense that actually works. " +
    "If the room only does one of these four things this week, it should be the code word; if they do two, add the trusted contact."
  );
}

// ---------------------------------------------------------------- Slide 8 - if it's already happened
{
  const s = darkSlide(p);
  kicker(s, "If it's already happened", AMBER);
  s.addText("The first thing out of your mouth decides the next ten years.", {
    x: 0.9, y: 1.3, w: 11.2, h: 1.0, fontFace: "Cambria", fontSize: 27, bold: true, color: WHITE,
  });

  s.addShape("roundRect", { x: 0.9, y: 2.7, w: 6.9, h: 1.5, rectRadius: 0.08, fill: { color: "1E3A2C" }, line: { color: "2E5540", width: 1 } });
  s.addText("SAY THIS", { x: 1.15, y: 2.85, w: 3, h: 0.35, fontFace: "Calibri", fontSize: 11, bold: true, color: "7FD9A8", charSpacing: 1.5 });
  s.addText("“I'm really glad you told me. Let's fix what we can.”", {
    x: 1.15, y: 3.2, w: 6.4, h: 0.9, fontFace: "Cambria", fontSize: 18, italic: true, color: WHITE, valign: "top" });

  s.addShape("roundRect", { x: 0.9, y: 4.4, w: 6.9, h: 1.9, rectRadius: 0.08, fill: { color: "3A1F22" }, line: { color: "5C2E32", width: 1 } });
  s.addText("NOT THIS", { x: 1.15, y: 4.55, w: 3, h: 0.35, fontFace: "Calibri", fontSize: 11, bold: true, color: "E29B95", charSpacing: 1.5 });
  s.addText("“Why didn't you call me?”  •  “How could you not see it?”  •  “I told you about this.”", {
    x: 1.15, y: 4.9, w: 6.4, h: 1.3, fontFace: "Cambria", fontSize: 15, italic: true, color: "E8CFCC", valign: "top" });

  s.addText("All three teach the person to never tell you again — and there's very likely to be a next time. People scammed once are deliberately targeted again.", {
    x: 8.2, y: 2.7, w: 4.2, h: 3.6, fontFace: "Calibri", fontSize: 13.5, color: "AEB9C4", valign: "top" });

  pageNum(s, 8, true);
  s.addNotes(
    "This slide is worth slowing down for. All three 'not this' lines come from a place of love and fear, not cruelty - say that explicitly so nobody in the room feels attacked for having said one of them before. " +
    "Then: handle the logistics yourself if they'll let you, but let them keep decisions about their own money. Losing money AND losing authority over your own accounts in the same week is two losses, not one."
  );
}

// ---------------------------------------------------------------- Slide 9 - capacity concern
{
  const s = lightSlide(p);
  kicker(s, "When it's more than one scam call", NAVY);
  s.addText("Sometimes it's a pattern, not an incident.", { x: 0.9, y: 1.25, w: 10.5, h: 0.6, fontFace: "Cambria", fontSize: 24, bold: true, color: INK });
  s.addText("Repeated payments. New secrecy. A new “friend” on the phone. Confusion about transactions that were once routine. That's a different problem, and it needs more than a website.", {
    x: 0.9, y: 1.95, w: 10.8, h: 0.9, fontFace: "Calibri", fontSize: 14.5, color: MUTED });

  const res = [
    ["Their doctor", "A cognitive check — financial mistakes are sometimes the earliest visible symptom, showing up before memory complaints do."],
    ["Eldercare Locator", "800-677-1116 — connects you to local aging services."],
    ["Adult Protective Services", "If you believe someone is being financially exploited, particularly by a caregiver or new acquaintance."],
    ["An elder law attorney", "If powers of attorney need looking at."],
  ];
  let y = 3.15;
  res.forEach(([who, what]) => {
    s.addShape("rect", { x: 0.9, y, w: 0.06, h: 0.75, fill: { color: AMBER }, line: { type: "none" } });
    s.addText(who, { x: 1.15, y: y - 0.05, w: 3.2, h: 0.85, fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY, valign: "top" });
    s.addText(what, { x: 4.5, y: y - 0.05, w: 7.2, h: 0.85, fontFace: "Calibri", fontSize: 12.5, color: MUTED, valign: "top" });
    y += 0.92;
  });
  pageNum(s, 9, false);
  s.addNotes(
    "This is the slide for the harder conversation - not every family in the room needs it today, but some do, and they're often too embarrassed to ask afterward. " +
    "Say plainly: doing this early, while everyone can participate in the decision, is far kinder than doing it during a crisis."
  );
}

// ---------------------------------------------------------------- Slide 10 - check yourself
{
  const s = darkSlide(p);
  s.addText("Whatever rule you set for your mother — follow it yourself.", {
    x: 0.9, y: 2.5, w: 11.2, h: 1.1, fontFace: "Cambria", fontSize: 32, bold: true, color: WHITE,
  });
  s.addText("Out loud, where she can see. The fastest-growing victim group by percentage isn't older adults — it's younger people. They just lose smaller amounts, because they have less.", {
    x: 0.9, y: 3.7, w: 9.8, h: 1.0, fontFace: "Calibri", fontSize: 15.5, color: "AEB9C4" });
  s.addText("That's what makes it a family standard — not a supervision plan.", {
    x: 0.9, y: 4.85, w: 9.8, h: 0.6, fontFace: "Cambria", fontSize: 18, italic: true, color: AMBER });
  pageNum(s, 10, true);
  s.addNotes(
    "Short slide, but don't skip it - it's often the moment people relax, because it reframes the whole talk from 'protect a vulnerable person' to 'this is just how our family handles money now.' " +
    "That reframe is what makes the habit stick instead of feeling like surveillance."
  );
}

// ---------------------------------------------------------------- Slide 11 - success
{
  const s = lightSlide(p);
  kicker(s, "What success actually looks like", NAVY);
  s.addText(
    "“Someone called me about my account and I told them I'd call the bank myself.”",
    { x: 0.9, y: 1.6, w: 11.2, h: 1.3, fontFace: "Cambria", fontSize: 30, bold: true, italic: true, color: INK }
  );
  s.addText("Said the way you'd mention taking out the trash.", {
    x: 0.9, y: 2.95, w: 9, h: 0.5, fontFace: "Calibri", fontSize: 16, color: MUTED });
  s.addShape("line", { x: 0.9, y: 4.0, w: 4.2, h: 0, line: { color: LINE, width: 1 } });
  s.addText("Not vigilance. Not worry. Just a habit she has, that she's a little proud of, that she'll pass along to a friend down the hall.", {
    x: 0.9, y: 4.25, w: 9.8, h: 0.9, fontFace: "Cambria", fontSize: 17, color: NAVY });
  pageNum(s, 11, false);
  s.addNotes(
    "Close on this image deliberately. The whole talk has been building toward this one picture of what success feels like day to day - ordinary, not dramatic. " +
    "Let it sit for a second before moving to the resources slide."
  );
}

// ---------------------------------------------------------------- Slide 12 - resources / close
{
  const s = darkSlide(p);
  s.addText("Free help, no judgment", { x: 0.9, y: 0.85, w: 8, h: 0.6, fontFace: "Cambria", fontSize: 24, bold: true, color: WHITE });

  const phones = [
    ["833-372-8311", "National Elder Fraud Hotline · Mon–Fri"],
    ["877-908-3360", "AARP Fraud Watch · Mon–Fri"],
    ["800-677-1116", "Eldercare Locator"],
  ];
  let y = 1.85;
  phones.forEach(([num, label]) => {
    s.addText(num, { x: 0.9, y, w: 3.6, h: 0.55, fontFace: "Cambria", fontSize: 24, bold: true, color: AMBER });
    s.addText(label, { x: 4.6, y: y + 0.08, w: 6, h: 0.5, fontFace: "Calibri", fontSize: 14, color: "AEB9C4", valign: "middle" });
    y += 0.75;
  });

  s.addShape("line", { x: 0.9, y: 4.5, w: 11.4, h: 0, line: { color: "2E4258", width: 1 } });
  s.addText("Everything in this deck, plus the full site — fridge sheets, scam-by-scam guides, and the family conversation guide this deck is drawn from:", {
    x: 0.9, y: 4.75, w: 8, h: 0.9, fontFace: "Calibri", fontSize: 13.5, color: "AEB9C4" });
  s.addText("trustbutverifyproject.org/for-family", {
    x: 0.9, y: 5.55, w: 8, h: 0.5, fontFace: "Cambria", fontSize: 19, bold: true, color: WHITE });

  s.addText("Free. Public domain. No sponsors, no data collected. Take it, change it, put your name on it.", {
    x: 0.9, y: 6.7, w: 10.5, h: 0.4, fontFace: "Calibri", fontSize: 11, italic: true, color: "6F7E8C" });
  pageNum(s, 12, true);
  s.addNotes(
    "Close with the phone numbers and the URL up on screen long enough for people to photograph it. " +
    "Remind the room: this whole deck is free to take, copy, retitle, and give again - encourage them to send it to a sibling who couldn't be here, not just keep it to themselves."
  );
}

p.writeFile({ fileName: "trust-but-verify-for-family.pptx" }).then(() => {
  console.log("wrote trust-but-verify-for-family.pptx");
});
