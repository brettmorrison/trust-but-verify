// Trust But Verify — 25-minute talk deck
// node build/make_deck.js
const pptxgen = require("pptxgenjs");

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
p.title = "Trust But Verify — protecting yourself from scams";

// ---------- helpers ----------

function dark(notes) {
  const s = p.addSlide();
  s.background = { color: INK };
  if (notes) s.addNotes(notes);
  return s;
}
function light(notes) {
  const s = p.addSlide();
  s.background = { color: PAPER };
  if (notes) s.addNotes(notes);
  return s;
}
function title(s, text, opts) {
  s.addText(text, Object.assign({
    x: M, y: 0.55, w: W - M * 2, h: 1.2,
    fontFace: F, fontSize: 40, bold: true, color: INK, margin: 0,
    valign: "top",
  }, opts || {}));
}
// the deck's motif: an enormous numeral, echoing the printed fridge sheet
function numeral(s, n, color) {
  s.addText(String(n), {
    x: M, y: 1.35, w: 2.6, h: 4.3,
    fontFace: F, fontSize: 260, bold: true, color: color || INK,
    align: "left", valign: "middle", margin: 0,
  });
}

// ---------- 1. title ----------
let s = dark(
  "Wait for the room to settle. Don't start until people are looking at you.\n\n" +
  "Say your name, and say you're a volunteer, not a salesperson. Say plainly: " +
  "I am not selling anything and I will not ask for anything.\n\nThen pause."
);
s.addText("TRUST", { x: M, y: 1.5, w: W - M * 2, h: 1.3, fontFace: F, fontSize: 88, bold: true, color: PAPER, margin: 0 });
s.addText("BUT VERIFY", { x: M, y: 2.7, w: W - M * 2, h: 1.3, fontFace: F, fontSize: 88, bold: true, color: PAPER, margin: 0 });
s.addText("You don't have to get suspicious of everybody.\nYou add one step.", {
  x: M, y: 4.4, w: 9.5, h: 1.4, fontFace: F, fontSize: 24, color: "D8D4CC", margin: 0, lineSpacing: 34,
});

// ---------- 2. the story ----------
s = dark(
  "Tell this slowly. Do not rush it. If you have a local story, use that instead — " +
  "local always beats dramatic. Never name anyone.\n\n" +
  "Pause after 'he never knew'. Let it land before you go on."
);
s.addText("\u201CGrandma? I'm in trouble.\nPlease don't tell Mom.\u201D", {
  x: M, y: 1.7, w: W - M * 2, h: 2.4, fontFace: F, fontSize: 46, bold: true, color: PAPER, margin: 0, lineSpacing: 62,
});
s.addText("She had $1,100 in a courier's hands within the hour.\nHer grandson was at work the whole time.", {
  x: M, y: 4.6, w: 10.5, h: 1.4, fontFace: F, fontSize: 22, color: "D8D4CC", margin: 0, lineSpacing: 32,
});

// ---------- 3. not foolish ----------
s = light(
  "This is the most important slide in the talk for how the room feels.\n\n" +
  "Say it directly: that woman is not foolish. Then say the part about professionals — " +
  "call centres, scripts, supervisors, quotas.\n\n" +
  "Include yourself. Mention a text that nearly got you. That's the permission slip " +
  "that lets people ask questions later."
);
title(s, "She is not foolish.");
s.addText("She raised four children and ran a business for thirty years.", {
  x: M, y: 1.9, w: 11.5, h: 0.6, fontFace: F, fontSize: 24, color: GREY, margin: 0,
});
[["They do this full time.", "Call centres. Managers. Quotas."],
 ["They work from scripts.", "Tested on thousands of people."],
 ["They practise.", "You are meeting a professional."]].forEach((row, i) => {
  const y = 2.95 + i * 1.35;
  s.addShape(p.ShapeType.ellipse, { x: M, y: y, w: 0.62, h: 0.62, fill: { color: INK } });
  s.addText(String(i + 1), { x: M, y: y, w: 0.62, h: 0.62, fontFace: F, fontSize: 22, bold: true, color: PAPER, align: "center", valign: "middle", margin: 0 });
  s.addText(row[0], { x: M + 1.0, y: y - 0.05, w: 10.5, h: 0.5, fontFace: F, fontSize: 30, bold: true, color: INK, margin: 0 });
  s.addText(row[1], { x: M + 1.0, y: y + 0.46, w: 10.5, h: 0.45, fontFace: F, fontSize: 21, color: GREY, margin: 0 });
});

// ---------- 4. the scale ----------
s = light(
  "Give the number, then immediately reframe it: this is an industry, not a series of " +
  "unlucky individuals.\n\nThat reframing removes the implication that being targeted " +
  "says something about you."
);
title(s, "This is an industry.");
s.addText("$7.7", { x: M, y: 2.0, w: 5.2, h: 2.4, fontFace: F, fontSize: 150, bold: true, color: INK, margin: 0, valign: "middle" });
s.addText("BILLION", { x: M + 0.15, y: 4.3, w: 5.0, h: 0.6, fontFace: F, fontSize: 30, bold: true, color: INK, charSpacing: 4, margin: 0 });
s.addText("reported lost by Americans over 60, in one year", {
  x: M, y: 4.95, w: 5.6, h: 0.9, fontFace: F, fontSize: 17, color: GREY, margin: 0,
});
s.addShape(p.ShapeType.rect, { x: 6.9, y: 2.0, w: 5.65, h: 3.5, fill: { color: BAND } });
s.addText([
  { text: "201,266", options: { fontSize: 40, bold: true, color: INK, breakLine: true } },
  { text: "complaints from people 60 and over\n\n", options: { fontSize: 17, color: GREY, breakLine: true } },
  { text: "$38,501", options: { fontSize: 40, bold: true, color: INK, breakLine: true } },
  { text: "average loss for that age group", options: { fontSize: 17, color: GREY } },
], { x: 7.25, y: 2.3, w: 5.0, h: 2.9, fontFace: F, margin: 0, valign: "top" });
s.addText("FBI Internet Crime Complaint Center, 2025", {
  x: M, y: 6.5, w: 8, h: 0.35, fontFace: F, fontSize: 12, color: GREY, italic: true, margin: 0,
});

// ---------- 5. section: the three steps ----------
s = dark(
  "Transition line: 'So nobody here is going to out-think a professional, and I'm not " +
  "going to ask you to. I'm going to ask you to be slower than one.'\n\n" +
  "Then: 'Here is the whole thing. Three steps.'"
);
s.addText("The three steps", { x: M, y: 2.4, w: 11, h: 1.4, fontFace: F, fontSize: 66, bold: true, color: PAPER, margin: 0 });
s.addText("Before any money moves.", { x: M, y: 3.9, w: 11, h: 0.8, fontFace: F, fontSize: 28, color: "D8D4CC", margin: 0 });

// ---------- 6-8. the steps ----------
const STEPS = [
  ["Look up the number\nyourself.",
   "Not the number they gave you.\nThe one on your card or your statement.",
   "Say it twice. This is the single highest-value sentence in the talk.\n\n" +
   "Give them the line to use: 'I'm going to hang up and call the number on my card.'\n\n" +
   "Then say: a scammer will argue with you about that sentence. The argument IS the answer. " +
   "You don't have to win it. You just have to hang up."],
  ["Call the person\nyourself.",
   "Hang up first. Then call.\nIf it was real, they'll still be there.",
   "Emphasise: call the person on the number you have always used — not the number that " +
   "called you.\n\nIf they don't answer, call someone else in the family. Say clearly that " +
   "this is not going behind anyone's back.\n\nKey line: a real emergency survives one more " +
   "phone call. A fake one can't."],
  ["Wait a day.",
   "Real problems survive a night's sleep.\nScams do not.",
   "List them out loud: not the IRS, not Medicare, not your bank's fraud department, not a " +
   "warrant, not a utility.\n\nThen the key sentence: urgency is not evidence that something " +
   "is real. Urgency is evidence that someone needs you to stop thinking.\n\n" +
   "If a day is too long, twenty minutes. Tell one person out loud."],
];
STEPS.forEach((st, i) => {
  const sl = light(st[2]);
  numeral(sl, i + 1);
  sl.addText(st[0], { x: 3.7, y: 1.5, w: 8.9, h: 2.6, fontFace: F, fontSize: 66, bold: true, color: INK, margin: 0, lineSpacing: 80 });
  sl.addText(st[1], { x: 3.7, y: 4.45, w: 8.9, h: 1.8, fontFace: F, fontSize: 32, color: GREY, margin: 0, lineSpacing: 46 });
});

// ---------- 9. the number they gave you ----------
s = light(
  "This is the sentence you most want people to leave with. Say it, pause, say it again.\n\n" +
  "Then: almost every scheme collapses the moment you dial a number they didn't choose for you."
);
s.addText("The number they gave you\nis the scam.", {
  x: M, y: 2.2, w: 11.8, h: 3, fontFace: F, fontSize: 62, bold: true, color: INK, margin: 0, lineSpacing: 78, align: "center",
});

// ---------- 10. code word ----------
s = light(
  "Explain voice cloning in one sentence: software copies a voice from a few seconds of " +
  "video, it's free, it takes a minute.\n\nSo 'it sounded just like him' is no longer proof.\n\n" +
  "Then give the fix. Emphasise it takes four minutes at a Sunday dinner. " +
  "Ask the room to actually do it this week."
);
title(s, "The family code word");
s.addText("Software can copy your grandson's voice from three seconds of video.\nIt cannot know something that was never said out loud on the internet.", {
  x: M, y: 1.85, w: 11.8, h: 1.2, fontFace: F, fontSize: 22, color: GREY, margin: 0, lineSpacing: 32,
});
s.addShape(p.ShapeType.rect, { x: M, y: 3.3, w: 11.8, h: 2.5, fill: { color: BAND } });
s.addText("Pick one word your family knows\nand nobody else could guess.", {
  x: M + 0.4, y: 3.6, w: 11, h: 1.1, fontFace: F, fontSize: 30, bold: true, color: INK, margin: 0, lineSpacing: 40,
});
s.addText("Never post it. Never text it. Say it out loud, at a meal, with the grandchildren there.\nFour minutes — and it defeats every voice-cloning scam that exists.", {
  x: M + 0.4, y: 4.8, w: 11, h: 0.9, fontFace: F, fontSize: 18, color: GREY, margin: 0, lineSpacing: 26,
});

// ---------- 11. section: three signs ----------
s = dark("Transition: 'How do you know when to use those three steps? Three signs.'");
s.addText("Three signs\nto stop", { x: M, y: 2.1, w: 11, h: 2.4, fontFace: F, fontSize: 66, bold: true, color: PAPER, margin: 0, lineSpacing: 78 });

// ---------- 12. the three signs ----------
s = light(
  "Go through all three, then say them again as a set.\n\n" +
  "On sign two, mention the physical part — chest tightens, hands go cold, the careful part " +
  "of your brain gets quieter. Say: you are not imagining that you can't think straight.\n\n" +
  "Then: make the rule now, while you're calm."
);
title(s, "Three signs to stop");
[["It came to you.", "You didn't start this. They called you."],
 ["It moved you fast.", "Fear, worry, love, or a deadline."],
 ["It wants a transfer.", "Money, a code, or your computer."]].forEach((row, i) => {
  const y = 2.1 + i * 1.62;
  s.addText(String(i + 1), { x: M, y: y, w: 1.15, h: 1.25, fontFace: F, fontSize: 72, bold: true, color: INK, margin: 0, valign: "middle" });
  s.addText(row[0], { x: M + 1.35, y: y + 0.02, w: 10.4, h: 0.6, fontFace: F, fontSize: 36, bold: true, color: INK, margin: 0 });
  s.addText(row[1], { x: M + 1.35, y: y + 0.7, w: 10.4, h: 0.55, fontFace: F, fontSize: 24, color: GREY, margin: 0 });
});
s.addText("Three yeses is a scam until proven otherwise — and it can only be proven on a number you looked up.", {
  x: M, y: 6.55, w: 11.8, h: 0.5, fontFace: F, fontSize: 17, color: GREY, italic: true, margin: 0,
});

// ---------- 13. section: two absolutes ----------
s = dark("Transition: 'Two things I want you to remember for the rest of your life.'");
s.addText("Two things that\nare always true", { x: M, y: 2.1, w: 11.5, h: 2.4, fontFace: F, fontSize: 60, bold: true, color: PAPER, margin: 0, lineSpacing: 74 });

// ---------- 14. gift cards ----------
s = light(
  "This is the most absolute statement in the whole talk. Deliver it as such.\n\n" +
  "List them: not the IRS, not Microsoft, not the electric company, not a court, not a bail " +
  "bondsman, not a hospital.\n\n" +
  "Then: if gift cards come up, that is the end of the conversation. Every time. No exceptions."
);
s.addShape(p.ShapeType.rect, { x: M, y: 1.5, w: 11.8, h: 4.4, fill: { color: PAPER }, line: { color: RED, width: 5 } });
s.addText("Nobody legitimate\nis ever paid in gift cards.", {
  x: M + 0.5, y: 2.0, w: 10.8, h: 2.1, fontFace: F, fontSize: 48, bold: true, color: RED, margin: 0, lineSpacing: 62,
});
s.addText("Not the IRS. Not Microsoft. Not the electric company.\nNot a court. Not a bail bondsman. Not a hospital.\n\nIf gift cards come up, that is the end of the conversation.", {
  x: M + 0.5, y: 4.15, w: 10.8, h: 1.5, fontFace: F, fontSize: 20, color: INK, margin: 0, lineSpacing: 28,
});

// ---------- 15. safe account ----------
s = light(
  "This is the sentence that stops the Phantom Hacker — the scheme that empties whole " +
  "retirement accounts.\n\nAdd: there is no such thing as a government safe account. The " +
  "Federal Reserve does not hold accounts for individuals.\n\n" +
  "And: nobody comes to your house to collect cash, gold, or valuables. Nobody. If someone " +
  "is coming to your door for money, call the police."
);
s.addShape(p.ShapeType.rect, { x: M, y: 1.5, w: 11.8, h: 4.4, fill: { color: PAPER }, line: { color: RED, width: 5 } });
s.addText("Your bank will never ask you\nto move money out of your bank.", {
  x: M + 0.5, y: 2.0, w: 10.8, h: 2.1, fontFace: F, fontSize: 44, bold: true, color: RED, margin: 0, lineSpacing: 58,
});
s.addText("Not to a safe account. Not to protect it. Not while they investigate.\n\nThere is no such thing as a government safe account.\nAnd nobody comes to your home to collect cash, gold, or valuables.", {
  x: M + 0.5, y: 4.15, w: 10.8, h: 1.5, fontFace: F, fontSize: 20, color: INK, margin: 0, lineSpacing: 28,
});

// ---------- 16. how they ask to be paid ----------
s = light(
  "Frame it: you may not be able to tell whether a caller really works for your bank. But " +
  "you can always tell how they want the money.\n\n" +
  "Scammers only accept payments that can't be reversed. That's the whole logic.\n\n" +
  "Give them the question to ask: 'How do you want to be paid?' Ask it early. It's a normal " +
  "question and the answer often ends the conversation for you."
);
title(s, "How they ask to be paid");
s.addText("Scammers only accept payments that can't be reversed. That's the whole logic.", {
  x: M, y: 1.85, w: 11.8, h: 0.5, fontFace: F, fontSize: 21, color: GREY, margin: 0,
});
const PAY = ["Gift cards", "Wire transfer", "Bitcoin machine", "Cash by courier", "Payment app to a stranger", "A \u201Csafe account\u201D"];
PAY.forEach((t, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = M + col * 4.0, y = 2.65 + row * 1.75;
  s.addShape(p.ShapeType.rect, { x: x, y: y, w: 3.7, h: 1.45, fill: { color: BAND } });
  s.addText("\u2715", { x: x + 0.25, y: y + 0.22, w: 0.5, h: 0.5, fontFace: F, fontSize: 22, bold: true, color: RED, margin: 0 });
  s.addText(t, { x: x + 0.25, y: y + 0.72, w: 3.2, h: 0.6, fontFace: F, fontSize: 19, bold: true, color: INK, margin: 0 });
});
s.addText("Ask early: \u201CHow do you want to be paid?\u201D", {
  x: M, y: 6.35, w: 11.8, h: 0.5, fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0,
});

// ---------- 17. section: if it already happened ----------
s = dark(
  "Change your tone here. Slower, warmer.\n\n" +
  "Do NOT ask who in the room has been scammed. Not even for a show of hands. " +
  "Not even anonymously."
);
s.addText("If it already\nhappened", { x: M, y: 2.1, w: 11, h: 2.4, fontFace: F, fontSize: 60, bold: true, color: PAPER, margin: 0, lineSpacing: 74 });

// ---------- 18. not your fault ----------
s = light(
  "Say this plainly and without hurrying.\n\n" +
  "The shame is the last part of the scam — it keeps people quiet long enough for the money " +
  "to disappear.\n\nThen the practical part: call your bank on the number on your card and say " +
  "'I am reporting fraud and I need to recall a payment.' Speed matters more than anything."
);
title(s, "It is not your fault. It is not too late.");
s.addText("The shame is the last part of the scam.\nIt keeps people quiet long enough for the money to disappear.", {
  x: M, y: 1.95, w: 11.8, h: 1.1, fontFace: F, fontSize: 24, color: GREY, margin: 0, lineSpacing: 34,
});
[["Call your bank now", "On the number on your card. Say: \u201CI am reporting fraud and I need to recall a payment.\u201D"],
 ["Keep everything", "Don't delete the texts or emails. They're evidence."],
 ["Tell one person", "Not so they can fix it. So you're not carrying it alone."]].forEach((row, i) => {
  const y = 3.35 + i * 1.25;
  s.addShape(p.ShapeType.ellipse, { x: M, y: y, w: 0.55, h: 0.55, fill: { color: INK } });
  s.addText(String(i + 1), { x: M, y: y, w: 0.55, h: 0.55, fontFace: F, fontSize: 20, bold: true, color: PAPER, align: "center", valign: "middle", margin: 0 });
  s.addText(row[0], { x: M + 0.9, y: y - 0.06, w: 10.8, h: 0.48, fontFace: F, fontSize: 27, bold: true, color: INK, margin: 0 });
  s.addText(row[1], { x: M + 0.9, y: y + 0.42, w: 10.8, h: 0.45, fontFace: F, fontSize: 19, color: GREY, margin: 0 });
});

// ---------- 19. the helplines ----------
s = light(
  "Say both numbers out loud, slowly, twice. Point at the sheet in their hands.\n\n" +
  "Stress: free, and nobody there will judge you. The second one you can call even if " +
  "nothing has happened — just to ask whether something sounds wrong."
);
title(s, "Free help. No judgment.");
[["833-372-8311", "National Elder Fraud Hotline", "Mon\u2013Fri, 10\u20136 Eastern \u00B7 U.S. Dept. of Justice"],
 ["877-908-3360", "AARP Fraud Watch Helpline", "Mon\u2013Fri, 8\u20138 Eastern \u00B7 Free for anyone, member or not"]].forEach((row, i) => {
  const y = 2.15 + i * 2.35;
  s.addText(row[0], { x: M, y: y, w: 8.2, h: 1.2, fontFace: F, fontSize: 72, bold: true, color: INK, margin: 0 });
  s.addText(row[1], { x: M, y: y + 1.18, w: 8.5, h: 0.5, fontFace: F, fontSize: 26, bold: true, color: INK, margin: 0 });
  s.addText(row[2], { x: M, y: y + 1.68, w: 8.5, h: 0.45, fontFace: F, fontSize: 18, color: GREY, margin: 0 });
});
s.addText("Interpreters available.\nAsk in English: your language, then \u201Cplease.\u201D", {
  x: 8.9, y: 2.3, w: 3.9, h: 1.6, fontFace: F, fontSize: 17, color: INK, margin: 0, lineSpacing: 26,
});

// ---------- 20. the second scam ----------
s = light(
  "This is the slide people thank you for afterward.\n\n" +
  "Say it as a prediction: if it has happened to you, someone WILL call in the coming weeks " +
  "offering to get the money back.\n\nA call that was described to you last month is a call " +
  "you recognise. That recognition is the whole defence."
);
title(s, "Expect the second call.");
s.addText("People who have been scammed once are targeted again \u2014 on purpose.\nYour name goes on a list that is bought and sold.", {
  x: M, y: 1.95, w: 11.8, h: 1.1, fontFace: F, fontSize: 24, color: GREY, margin: 0, lineSpacing: 34,
});
s.addShape(p.ShapeType.rect, { x: M, y: 3.5, w: 11.8, h: 2.75, fill: { color: PAPER }, line: { color: RED, width: 5 } });
s.addText("No legitimate agency ever charges a fee\nto return your money.", {
  x: M + 0.5, y: 3.7, w: 10.8, h: 1.3, fontFace: F, fontSize: 36, bold: true, color: RED, margin: 0, lineSpacing: 48,
});
s.addText("A \u201Claw firm,\u201D a \u201Crecovery service,\u201D a \u201Cgovernment investigator.\u201D Same crew, or their customers.", {
  x: M + 0.5, y: 5.45, w: 10.8, h: 0.6, fontFace: F, fontSize: 20, color: INK, margin: 0,
});

// ---------- 21. recap ----------
s = light(
  "Say all three again, slowly. Ask the room to say them with you if it feels right.\n\n" +
  "This is the fourth time they've heard them. That repetition is the whole delivery method."
);
title(s, "So: three steps.");
[["Look up the number yourself.", "Not the one they gave you."],
 ["Call the person yourself.", "Hang up first."],
 ["Wait a day.", "Real problems survive a night's sleep."]].forEach((row, i) => {
  const y = 2.15 + i * 1.65;
  s.addText(String(i + 1), { x: M, y: y, w: 1.2, h: 1.3, fontFace: F, fontSize: 80, bold: true, color: INK, margin: 0, valign: "middle" });
  s.addText(row[0], { x: M + 1.5, y: y + 0.05, w: 10.3, h: 0.62, fontFace: F, fontSize: 38, bold: true, color: INK, margin: 0 });
  s.addText(row[1], { x: M + 1.5, y: y + 0.75, w: 10.3, h: 0.5, fontFace: F, fontSize: 23, color: GREY, margin: 0 });
});

// ---------- 22. closing ----------
s = dark(
  "Close on capability, never on fear.\n\n" +
  "Then: 'Take two sheets — one for you, one for a neighbour.' Hand them over personally " +
  "as people leave. Don't leave a stack on a table.\n\n" +
  "Then take questions. Leave at least twelve minutes. The questions are where the real " +
  "education happens.\n\nIf someone tells you they've lost money — your first words are " +
  "'I'm glad you told me.'"
);
s.addText("You don't have to get\nsuspicious of everybody.", {
  x: M, y: 2.0, w: 11.8, h: 2.2, fontFace: F, fontSize: 52, bold: true, color: PAPER, margin: 0, lineSpacing: 68,
});
s.addText("You just add one step.", {
  x: M, y: 4.35, w: 11.8, h: 0.9, fontFace: F, fontSize: 40, bold: true, color: "D8D4CC", margin: 0,
});
s.addText("trustbutverifyproject.org", {
  x: M, y: 6.3, w: 11.8, h: 0.5, fontFace: F, fontSize: 18, color: "9A958C", margin: 0,
});

p.writeFile({ fileName: "/home/claude/tbv/formats/talk/trust-but-verify-talk.pptx" })
  .then(f => console.log("wrote", f));
