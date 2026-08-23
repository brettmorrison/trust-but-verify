const fs = require("fs");
const path = require("path");

const OUT = __dirname;
const SITE = "The Trust But Verify Project";

const NAV = [
  ["/how-scams-work.html", "How scams work"],
  ["/it-just-happened.html", "It just happened"],
  ["/give-this-talk.html", "Give this talk"],
  ["/print.html", "Print & share"],
  ["/blog/", "Real examples"],
  ["/about.html", "About"],
];

function page({ file, title, desc, current, body, depth = 0 }) {
  const root = depth ? "../" : "";
  const nav = NAV.map(([href, label]) => {
    const h = depth ? ".." + href : "." + href;
    const cur = current === href ? ' aria-current="page"' : "";
    return `<li><a href="${h}"${cur}>${label}</a></li>`;
  }).join("\n          ");

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title} · ${SITE}</title>
<meta name="description" content="${desc}">
<link rel="stylesheet" href="${root}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>

<div class="promise">We will never call you, email you, or ask you for money.</div>

<header class="masthead">
  <div class="wrap">
    <a class="wordmark" href="${depth ? "../index.html" : "./index.html"}">Trust&nbsp;But&nbsp;<span>Verify</span></a>
    <nav aria-label="Main">
      <ul>
          ${nav}
      </ul>
    </nav>
  </div>
</header>

<main id="main">
${body}
</main>

<footer>
  <div class="wrap">
    <div class="grid grid-3">
      <div>
        <h2>If it just happened</h2>
        <ul>
          <li>Call your bank's fraud department using the number on your card.</li>
          <li>AARP Fraud Watch Helpline: <strong>877&#8209;908&#8209;3360</strong></li>
          <li>Report it: <a href="https://www.ic3.gov">ic3.gov</a></li>
          <li>In danger, or someone at your door? Call 911.</li>
        </ul>
      </div>
      <div>
        <h2>On this site</h2>
        <ul>
          <li><a href="${depth ? "../how-scams-work.html" : "./how-scams-work.html"}">How scams work</a></li>
          <li><a href="${depth ? "../it-just-happened.html" : "./it-just-happened.html"}">It just happened</a></li>
          <li><a href="${depth ? "../give-this-talk.html" : "./give-this-talk.html"}">Give this talk</a></li>
          <li><a href="${depth ? "../print.html" : "./print.html"}">Print &amp; share</a></li>
          <li><a href="${depth ? "../blog/index.html" : "./blog/index.html"}">Real examples</a></li>
        </ul>
      </div>
      <div>
        <h2>Our promises</h2>
        <ul>
          <li>We will never contact you first.</li>
          <li>Everything here is free. Nothing is for sale.</li>
          <li>No ads and no sponsors.</li>
          <li>No accounts, no sign-ups, no mailing list.</li>
          <li>This site uses no cookies, no trackers, and no scripts of any kind.</li>
        </ul>
      </div>
    </div>
    <p class="fineprint">
      ${SITE} is a volunteer effort. We are not lawyers, financial advisers, or law enforcement,
      and nothing here is individual legal or financial advice.
      Figures cited come from the FBI Internet Crime Complaint Center's 2025 Annual Report unless noted.
      Anyone may copy, print, and reuse our materials, including for their own community.
    </p>
  </div>
</footer>
</body>
</html>
`;
  const full = path.join(OUT, file);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, html);
  return file;
}

/* ============================ HOME ============================ */
page({
  file: "index.html",
  title: "Trust people. Verify the message",
  desc: "A free, plain-language guide to the scams aimed at older adults — and the one habit that stops most of them. No ads, nothing for sale.",
  current: "/",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">A free guide for older adults and the people who love them</p>
    <h1>Trust people. Verify the message.</h1>
    <p class="lede">You don't have to become suspicious of everyone to be safe.
    You only have to add one step: check through your own door, not the one they sent you.</p>
    <div class="btn-row">
      <a class="btn btn--amber" href="./it-just-happened.html">Something just happened →</a>
      <a class="btn btn--ghost" href="./how-scams-work.html">Show me how scams work</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Their door, or your door</h2>
    <p class="narrow">Every scam depends on you walking through the door they opened —
    clicking their link, calling their number, staying on their phone call.
    Verifying just means using a door you already had.</p>

    <div class="doors">
      <div class="door door--theirs">
        <p class="tag">Their door</p>
        <h3>Whatever reached you</h3>
        <ul>
          <li>The link inside the email or text</li>
          <li>The phone number in the pop-up</li>
          <li>The person already on the line</li>
          <li>The website the message opened for you</li>
          <li>Right now, before you have time to think</li>
        </ul>
      </div>
      <div class="door door--yours">
        <p class="tag">Your door</p>
        <h3>Something you already had</h3>
        <ul>
          <li>The number printed on your card or statement</li>
          <li>The website you type in yourself</li>
          <li>Your grandson's phone number in your contacts</li>
          <li>A person you know, asked out loud</li>
          <li>Tomorrow morning, after you've slept</li>
        </ul>
      </div>
    </div>

    <div class="callout callout--amber">
      <p><strong>A logo proves nothing. Knowing your name proves nothing.</strong>
      Anyone can put a bank's logo on an email or a Google logo on an advertisement.
      Your name, address, and even your grandchildren's names are bought and sold for pennies.
      Familiar details are not evidence.</p>
    </div>
  </div>
</section>

<section class="on-ink">
  <div class="wrap">
    <p class="eyebrow">The part worth memorizing</p>
    <h2>Three red flags. Every scam has all three.</h2>
    <p class="narrow">The technology changes every year. This pattern does not, because without
    these three things a scam cannot work.</p>
    <div class="flags" style="margin-top:1.8rem">
      <div class="flag">
        <span class="num">1</span>
        <h3>They contacted you</h3>
        <p>A call, text, email, pop-up, or message you didn't go looking for.</p>
      </div>
      <div class="flag">
        <span class="num">2</span>
        <h3>You feel something</h3>
        <p>Fear, urgency, affection, or excitement. Enough to stop you thinking.</p>
      </div>
      <div class="flag">
        <span class="num">3</span>
        <h3>They want something</h3>
        <p>Money, a gift card, a password, remote access to your computer.</p>
      </div>
    </div>
    <div class="btn-row">
      <a class="btn btn--amber" href="./how-scams-work.html">See the eight most common scams →</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What brings you here?</h2>
    <div class="grid grid-3" style="margin-top:1.4rem">
      <div class="card card--go">
        <h3>Something feels wrong right now</h3>
        <p>A call, a message, or a payment you're unsure about. Start here, and take your time —
        nothing legitimate expires in the next ten minutes.</p>
        <p><a href="./it-just-happened.html">What to do →</a></p>
      </div>
      <div class="card">
        <h3>I want to warn my community</h3>
        <p>A complete 25-minute talk, free to use: slides, a full script, handouts, and a card
        for people to take home. Anyone can give it. No experience needed.</p>
        <p><a href="./give-this-talk.html">Get the talk kit →</a></p>
      </div>
      <div class="card">
        <h3>I'm worried about my parents</h3>
        <p>The single most useful thing you can do takes one phone call tonight: agree on a family
        password, and become the person they call before money moves.</p>
        <p><a href="./how-scams-work.html#defend">How to help →</a></p>
      </div>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <h2>Real examples</h2>
    <p class="narrow">Every one of these is a scam we have seen work on careful, intelligent people.
    Read them the way you'd read a story about a neighbor.</p>
    <ul class="posts">
      <li>
        <a href="./blog/screen-being-recorded.html">A pop-up said my screen was being recorded, and it had the Google logo</a>
        <p>It looked like a warning from Google. It was an advertisement — and the tiny word that gave it away.</p>
      </li>
      <li>
        <a href="./blog/grandson-in-jail.html">My grandson called from jail and asked me not to tell his parents</a>
        <p>It sounded exactly like him. That is now the easy part for a scammer.</p>
      </li>
      <li>
        <a href="./blog/bank-said-move-my-money.html">My bank's fraud department told me to move my money to a safe account</a>
        <p>Three callers, three days, one crew. The scam the FBI calls the Phantom Hacker.</p>
      </li>
      <li>
        <a href="./blog/met-someone-online.html">He never asked me for money. He asked me to invest.</a>
        <p>Four months of daily conversation before the subject ever came up. That was the plan.</p>
      </li>
      <li>
        <a href="./blog/get-your-money-back.html">Someone called offering to recover the money I already lost</a>
        <p>They knew exactly what happened to me. That's because victim lists are bought and sold.</p>
      </li>
    </ul>
  </div>
</section>
`,
});

/* ======================= HOW SCAMS WORK ======================= */
page({
  file: "how-scams-work.html",
  title: "How scams work",
  desc: "The three red flags behind every scam, the eight most common scams aimed at older adults, and the six habits that stop them.",
  current: "/how-scams-work.html",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">The pattern behind all of them</p>
    <h1>You don't need to learn forty scams</h1>
    <p class="lede">You need to learn one pattern. Criminals invent new stories constantly,
    but they can never drop these three steps, because the scam stops working without them.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="flags">
      <div class="flag">
        <span class="num">1</span>
        <h3>Unexpected contact</h3>
        <p>They reached out to you. You did not go looking for them. A call, a text, an email,
        a pop-up, a friend request, an advertisement.</p>
      </div>
      <div class="flag">
        <span class="num">2</span>
        <h3>A spike of emotion</h3>
        <p>Fear, urgency, affection, or excitement. The emotion isn't decoration — it's the
        machinery. Frightened people stop checking.</p>
      </div>
      <div class="flag">
        <span class="num">3</span>
        <h3>An unusual request</h3>
        <p>Money by an odd method, a password, a code they texted you, or permission to
        control your computer.</p>
      </div>
    </div>
    <div class="callout callout--green">
      <p><strong>All three at once? It's a scam. Every time.</strong>
      You never have to work out which scam it is. Two out of three is worth a phone call
      to someone you trust before you do anything.</p>
    </div>
  </div>
</section>

<section class="on-ink">
  <div class="wrap">
    <h2>You are not up against one person</h2>
    <p class="narrow">You're up against an industry with buildings, shifts, and quotas. Scam
    operations run call centers with scripts that have been tested on thousands of people,
    supervisors who coach the caller when you hesitate, and software that clones a voice from a
    few seconds of audio.</p>
    <p class="narrow">In 2025, Americans aged 60 and over reported losing <strong>$7.75 billion</strong>
    to online scams — a 59% jump in a single year. The FBI says the true figure is far higher,
    because most people never report it.</p>
    <p class="narrow">That increase happened because the criminals got better tools. Not because
    anyone got more foolish. Falling for one of these is not a character flaw. It means a
    professional got to you.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The eight you're most likely to meet</h2>
    <div class="grid grid-2" style="margin-top:1.4rem">
      <div class="card">
        <h3>Phishing messages</h3>
        <p>A message pretending to be your bank, Amazon, Medicare, the post office, or your church.
        A link takes you to a convincing copy of the real website and captures your password.
        Usually not the theft itself — the front door to it.</p>
      </div>
      <div class="card">
        <h3>Tech support</h3>
        <p>A pop-up, alarm sound, or frozen screen says your computer is infected and gives a number
        to call. They talk you into installing software, then watch your screen while you log into
        your accounts. <strong>Microsoft, Apple, and Google never call you.</strong></p>
      </div>
      <div class="card">
        <h3>The Phantom Hacker</h3>
        <p>Three callers over several days: fake tech support, then a fake bank fraud department,
        then a fake government official — all the same crew. They convince you to move your savings
        somewhere "safe." Victims often lose everything.</p>
      </div>
      <div class="card">
        <h3>Government impersonation</h3>
        <p>Social Security, Medicare, the IRS, or local police, usually with a threat of arrest.
        Social Security numbers cannot be suspended. Real agencies write letters; they don't open
        with a threatening phone call.</p>
      </div>
      <div class="card">
        <h3>Romance and friendship</h3>
        <p>Weeks or months of daily warmth before money is ever mentioned. Often it isn't romance
        at all — a wrong-number text, a shared hobby, a church group. There is always a reason they
        can't meet or video call.</p>
      </div>
      <div class="card">
        <h3>The grandchild in trouble</h3>
        <p>A panicked young voice, an accident or an arrest, and a plea not to tell their parents.
        A few seconds of audio from social media is now enough to clone a real voice convincingly.</p>
      </div>
      <div class="card">
        <h3>Virtual kidnapping</h3>
        <p>Screaming in the background and a demand for money right now. Nobody has been taken. The
        entire crime is the phone call, and it works only because they won't let you off the line
        to check.</p>
      </div>
      <div class="card">
        <h3>Investment and crypto</h3>
        <p>The most expensive of all. A friendly stranger, an app showing your balance climbing, and
        small withdrawals that work perfectly — until you try to take out the large amount and
        suddenly owe "taxes" or "fees."</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The fastest test: how do they want to be paid?</h2>
    <p class="narrow">Skip working out whether the story is true. Just listen for the payment.
    No real bank, agency, company, or family member ever asks to be paid these ways.</p>
    <div class="callout callout--red">
      <p>Gift cards &nbsp;·&nbsp; Wire transfer &nbsp;·&nbsp; Cryptocurrency or a Bitcoin machine
      &nbsp;·&nbsp; Cash or gold handed to a courier at your door &nbsp;·&nbsp; Payment apps to
      someone you've never met &nbsp;·&nbsp; "Move your money to a safe account"</p>
    </div>
  </div>
</section>

<section id="defend">
  <div class="wrap">
    <h2>Six habits that do most of the work</h2>
    <p class="narrow">All free. None require you to be good with computers.</p>
    <ol class="steps">
      <li>
        <h3>Verify through your own door</h3>
        <p>Hang up, close the message, and reach the company yourself — using the number on your
        card, your statement, or a website you type in. Never the number they gave you.</p>
      </li>
      <li>
        <h3>Agree on a family password</h3>
        <p>One word or phrase your family knows and a stranger never would. Anyone calling with an
        emergency has to say it. No password, no money — however much the voice sounds like them.</p>
      </li>
      <li>
        <h3>Wait a day before money moves</h3>
        <p>Real emergencies survive a day. Scams don't, which is exactly why they're always in a
        hurry.</p>
      </li>
      <li>
        <h3>Name your second opinion</h3>
        <p>One person you always call before sending money or giving out information. Tell them
        tonight that they have the job.</p>
      </li>
      <li>
        <h3>Turn on two-step login</h3>
        <p>A code sent to you when you sign in, so a stolen password alone isn't enough. Start with
        your email — it can reset every other account you own.</p>
      </li>
      <li>
        <h3>Freeze your credit</h3>
        <p>Free at all three credit bureaus, and it stops anyone from opening accounts in your name.</p>
      </li>
    </ol>
  </div>
</section>

<section class="on-ink">
  <div class="wrap narrow">
    <h2>Give them less to work with</h2>
    <p>Scam callers sound convincing because they've bought your details. You can shrink what's
    available:</p>
    <ul>
      <li>Set social media profiles to friends-only, and remove your birth year, phone number, and address.</li>
      <li>Post trip photos after you get home, not while you're away.</li>
      <li>Ask family to keep videos of grandchildren private. Public clips are what voice-cloning tools use.</li>
      <li>Skip the quizzes asking your first pet or the street you grew up on. Those are bank security questions.</li>
      <li>Give your email its own unique password — it can reset everything else.</li>
      <li>Your voicemail greeting doesn't need to say your name in your own voice.</li>
    </ul>
    <p>You can't undo every leak, and you don't have to. You only have to be a slower, more
    expensive target than the next person on their list.</p>
  </div>
</section>
`,
});

/* ====================== IT JUST HAPPENED ====================== */
page({
  file: "it-just-happened.html",
  title: "It just happened",
  desc: "What to do in the first 24 hours after a scam — who to call, in what order, and why reporting matters even if you lost nothing.",
  current: "/it-just-happened.html",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">No shame. Just speed.</p>
    <h1>It just happened. Here's what to do.</h1>
    <p class="lede">Move quickly, and don't spend a single minute being embarrassed.
    These crews do this professionally, all day, to thousands of people. You are not the first
    and you are not foolish.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="callout callout--red">
      <p><strong>If someone is at your door demanding money, or you feel unsafe, call 911 now.</strong>
      Scammers do send couriers to collect cash and gold in person.</p>
    </div>

    <h2>The first 24 hours</h2>
    <ol class="steps">
      <li>
        <h3>Call your bank's fraud department</h3>
        <p>Use the number printed on your card or your statement. Wire transfers and bank payments
        can sometimes be frozen or recalled, but only if someone acts fast. Hours matter.</p>
      </li>
      <li>
        <h3>Disconnect any computer they touched</h3>
        <p>If anyone had remote access, unplug it from the internet and don't use it until someone
        you trust has checked it. Don't try to fix it yourself.</p>
      </li>
      <li>
        <h3>Change your passwords, starting with email</h3>
        <p>Your email can reset every other account, so it goes first, then banking. Turn on
        two-step login while you're there.</p>
      </li>
      <li>
        <h3>Tell someone out loud</h3>
        <p>A family member, a friend, the front desk where you live. This is the hardest step and
        the most valuable one. It's also the step that stops the second scam.</p>
      </li>
      <li>
        <h3>Report it, even if you lost nothing</h3>
        <p>Reports are how these crews get identified, and how warnings reach the next person.
        Especially report it if you feel foolish — that feeling is the thing they rely on.</p>
      </li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who to call</h2>
    <table class="res">
      <thead>
        <tr><th>Who</th><th>What they're for</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>AARP Fraud Watch Helpline</strong><br>877&#8209;908&#8209;3360</td>
          <td>Free for anyone, member or not. A real person answers. This is the right number when
          you are <em>not sure yet</em> — call before any money moves. Everything else on this list
          is for afterward.</td>
        </tr>
        <tr>
          <td><strong>FBI Internet Crime Complaint Center</strong><br><a href="https://www.ic3.gov">ic3.gov</a></td>
          <td>Report any internet-enabled scam, any amount, whether or not you lost money.
          Include names, phone numbers, websites, and where any funds were sent.</td>
        </tr>
        <tr>
          <td><strong>Federal Trade Commission</strong><br><a href="https://reportfraud.ftc.gov">reportfraud.ftc.gov</a></td>
          <td>Consumer fraud and identity theft. For identity theft specifically,
          <a href="https://www.identitytheft.gov">identitytheft.gov</a> builds you a step-by-step
          recovery plan.</td>
        </tr>
        <tr>
          <td><strong>Your state Attorney General</strong></td>
          <td>Consumer protection complaints and current scam alerts for your state.</td>
        </tr>
        <tr>
          <td><strong>Adult Protective Services</strong></td>
          <td>If the person being taken advantage of is vulnerable, or the person doing it is a
          caregiver or family member.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section class="on-ink">
  <div class="wrap narrow">
    <h2>Expect them to come back</h2>
    <p>Being scammed once puts your name on a list, and that list gets sold. Within weeks or months,
    someone may contact you offering to recover your money — posing as a law firm, a "fund recovery"
    service, or a government agency. They'll know real details about what happened to you.</p>
    <p><strong>Nobody legitimate charges an upfront fee to recover stolen money.</strong>
    Reporting is always free. In 2025, older adults reported more than half a billion dollars taken
    this way, all of it from people who had already been robbed once.</p>
    <p>This is the practical reason to tell someone what happened. A person who talks about it is
    much harder to hit a second time.</p>
  </div>
</section>
`,
});

/* ======================= GIVE THIS TALK ======================= */
page({
  file: "give-this-talk.html",
  title: "Give this talk",
  desc: "A free, ready-to-deliver 25-minute talk on scams targeting older adults: slides, full script, handouts, and take-home cards. Anyone can give it.",
  current: "/give-this-talk.html",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Free to use, copy, and change</p>
    <h1>Give this talk where your parents live</h1>
    <p class="lede">A complete 25-minute presentation, written so that someone with no background in
    fraud or technology can deliver it well. Assisted living communities, senior centers, libraries,
    churches, and Rotary clubs are all good places to give it.</p>
    <div class="btn-row">
      <a class="btn btn--amber" href="./print.html">Get the materials →</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What's in the kit</h2>
    <div class="grid grid-2" style="margin-top:1.4rem">
      <div class="card">
        <h3>The slides</h3>
        <p>23 slides in large, high-contrast type designed to be read from the back of a activity
        room. Current FBI figures throughout. Provided as PowerPoint and as PDF, in case the venue's
        computer fights you.</p>
      </div>
      <div class="card">
        <h3>The speaker script</h3>
        <p>Every word, written to be spoken aloud, with timings for each slide and delivery notes on
        where to slow down, what to repeat, and which topics need a gentler tone.</p>
      </div>
      <div class="card">
        <h3>The handout</h3>
        <p>One page for people to take home and keep: the three red flags, the payment methods that
        are always a scam, the six habits, and blanks to write in their family password.</p>
      </div>
      <div class="card">
        <h3>The desk card</h3>
        <p>A large-print card to keep by the computer or the phone, with the five questions to ask
        yourself when something feels wrong.</p>
      </div>
    </div>
  </div>
</section>

<section class="on-ink">
  <div class="wrap">
    <h2>How to book one</h2>
    <p class="narrow">Nearly every senior community, library, and church has someone whose job is
    finding programming, and most of them would welcome a free hour on this subject. You don't need
    credentials. You need to be willing to stand up.</p>
    <ol class="steps" style="margin-top:1.5rem">
      <li>
        <h3>Ask the activity director</h3>
        <p>At a senior community, ask for the activities or life enrichment director. At a library,
        ask about adult programming. Say you have a free 25-minute talk on scams, with handouts.</p>
      </li>
      <li>
        <h3>Read the script twice, out loud</h3>
        <p>Once to yourself, once to a family member. That's genuinely enough preparation.</p>
      </li>
      <li>
        <h3>Print more handouts than you need</h3>
        <p>One per person plus twenty. Staff and visiting family always want them.</p>
      </li>
      <li>
        <h3>Stay afterward</h3>
        <p>The most important conversations happen one-on-one when the room empties, and that's
        usually when someone quietly tells you it already happened to them.</p>
      </li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <h2>How to talk about this without being condescending</h2>
    <p>This matters more than any statistic in the deck. The room you're speaking to has run
    businesses, raised families, and survived things you haven't. Talk to them that way.</p>
    <ul>
      <li><strong>Never suggest anyone was foolish.</strong> Say plainly that these are professionals
      with scripts and quotas, and that the audience's manners — answering the phone, being polite
      to strangers — are exactly what's being exploited.</li>
      <li><strong>Don't joke about romance scams.</strong> Someone in the room is in one right now,
      and someone else has already lost money. Your tone decides whether anyone talks to you
      afterward.</li>
      <li><strong>Give permission, not instructions.</strong> "You're allowed to hang up" lands
      better than "don't answer the phone."</li>
      <li><strong>End with something to do.</strong> Two phone calls tonight: set a family password,
      and name a second opinion.</li>
    </ul>
  </div>
</section>
`,
});

/* ========================= PRINT PAGE ========================= */
page({
  file: "print.html",
  title: "Print & share",
  desc: "Free printable materials: the one-page handout, the large-print desk card, the full talk, and the speaker script.",
  current: "/print.html",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Free. No sign-up. No email address required.</p>
    <h1>Print it, copy it, hand it out</h1>
    <p class="lede">Everything here is free to use and free to change. Print it on a church copier,
    hand it out at a community meeting, put your own group's name on it. You don't need to ask us.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid grid-2">
      <div class="card card--go">
        <h3>The desk card</h3>
        <p>One page, large type. The three red flags, the five questions to ask yourself, what
        nobody legitimate ever asks for, and who to call. Designed to sit next to a computer or a
        telephone.</p>
        <p><strong>Print on cardstock if you can. Tape it up — don't file it in a drawer.</strong></p>
        <div class="btn-row"><a class="btn" href="./downloads/trust-but-verify-desk-card.pdf">Download PDF</a><a class="btn btn--ghost" href="./downloads/trust-but-verify-desk-card.docx">Word version</a></div>
      </div>
      <div class="card card--go">
        <h3>The take-home handout</h3>
        <p>One page covering the three red flags, the payment methods that are always a scam, the six
        habits, the privacy steps, and blank lines for a family password and a second opinion.</p>
        <p><strong>Tape it inside a kitchen cabinet door.</strong></p>
        <div class="btn-row"><a class="btn" href="./downloads/trust-but-verify-handout.docx">Download handout</a></div>
      </div>
      <div class="card">
        <h3>The slides</h3>
        <p>The full 25-minute presentation, in PowerPoint so you can edit it and PDF so it will
        display anywhere.</p>
        <div class="btn-row"><a class="btn" href="./downloads/trust-but-verify-slides.pptx">PowerPoint</a><a class="btn btn--ghost" href="./downloads/trust-but-verify-slides.pdf">PDF</a></div>
      </div>
      <div class="card">
        <h3>The speaker script</h3>
        <p>The whole talk written out, with timings and delivery notes. Print it and read from it if
        that's more comfortable — nobody minds.</p>
        <div class="btn-row"><a class="btn" href="./downloads/trust-but-verify-speaker-script.docx">Download script</a></div>
      </div>
    </div>

    <div class="callout callout--amber">
      <p><strong>Two things worth doing tonight, before you print anything.</strong>
      Call one family member and agree on a family password — a word a stranger could never know,
      which anyone claiming an emergency has to say. Then tell one person they're your second
      opinion: the person you'll always call before money moves.</p>
    </div>
  </div>
</section>

<section class="on-ink">
  <div class="wrap narrow">
    <h2>Using our materials</h2>
    <p>Copy them. Reprint them. Translate them. Put your community's name and phone number on
    them. Use them in a talk you charge nothing for.</p>
    <p>The only thing we ask is that you don't sell them, don't attach advertising to them, and
    don't use them to promote a product or service. This material exists to be given away, and
    the moment it carries a sponsor it stops being trustworthy.</p>
  </div>
</section>
`,
});

/* ============================ ABOUT ============================ */
page({
  file: "about.html",
  title: "About",
  desc: "Who runs the Trust But Verify Project, why it exists, and the promises it makes about how it will and won't contact you.",
  current: "/about.html",
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Why this exists</p>
    <h1>Trust isn't the problem. Checking is the fix.</h1>
    <p class="lede">Trust but verify is a Russian proverb — <em>doveryai, no proveryai</em>. It rhymes
    in Russian, which is part of why it stuck. Reagan learned it to use with Gorbachev and said it so
    often that Gorbachev complained about it.</p>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <p>It worked as a phrase because both men understood the point: checking isn't the opposite of
    trusting. Checking is what lets you keep trusting.</p>
    <p>That's the whole idea here. Most scam advice quietly asks older people to become suspicious
    of everyone, and that's both miserable and dangerous. Isolation is precisely what romance
    scammers and confidence crews look for. We're not asking anyone to stop trusting people.
    We're asking for one step before money moves: verify through your own door.</p>

    <h2>Where this came from</h2>
    <p>This started as a single talk for one assisted living community, written by a volunteer who
    got tired of reading horror stories and forwarding links to a few friends. The talk went well
    enough that other communities asked for it, so the whole thing was made free for anyone to
    deliver.</p>
    <p>We work in data protection and privacy, which shapes what you'll find here. A great deal of
    scam advice ignores the reason these calls sound so convincing: your name, your address, your
    relatives' names, and the details of your life are bought and sold legally, for pennies. That's
    why familiar details prove nothing, and why privacy is treated here as scam defense rather than
    a separate topic.</p>

    <h2>Our promises</h2>
    <div class="callout callout--green">
      <p><strong>We will never call you, email you, text you, or come to your door.</strong>
      If someone claims to be from the Trust But Verify Project and asks you for anything at all —
      money, account details, remote access, a donation — it is not us. Hang up on them. That is
      rule one, and it applies to us exactly as much as to anyone else.</p>
    </div>
    <ul>
      <li>Everything we make is free, and nothing is for sale.</li>
      <li>We take no sponsorship and run no advertising. Identity-theft services, antivirus
      companies, and financial products all have an interest in how this subject gets taught, so we
      don't take their money.</li>
      <li>We don't collect personal information from the people we're trying to protect. There is no
      mailing list, no account, and no sign-up form on this site. A list of older adults who have
      been scammed is exactly the asset criminals buy and resell — so we don't build one.</li>
      <li>This site uses no cookies, no analytics, and no scripts of any kind. Nothing here is
      watching you read.</li>
    </ul>

    <h2>What we're not</h2>
    <p>We're not lawyers, financial advisers, investigators, or law enforcement. We can't recover
    stolen money and we won't offer to try. Anyone who promises that for an upfront fee is running
    the next scam. If you need help right now, the numbers on
    <a href="./it-just-happened.html">this page</a> are the ones to call.</p>
  </div>
</section>
`,
});

/* ============================ BLOG ============================ */

const POSTS = [
  {
    slug: "screen-being-recorded",
    title: "A pop-up said my screen was being recorded, and it had the Google logo",
    blurb: "It looked like a warning from Google. It was an advertisement — and the tiny word that gave it away.",
    kind: "Tech support scam",
    scenario: `<p>She was searching for something ordinary. At the top of the results was a red banner:
      <strong>"Warning: your screen is being recorded. Your Google account may be compromised."</strong>
      It carried the Google logo and a phone number to call for help.</p>
      <p>She trusts Google. The warning appeared to come from Google. She reached for the phone.</p>`,
    reality: `<p>It was a paid advertisement, sitting above the real search results. Anyone can buy one,
      and anyone can put a logo in the picture. Above it, in grey type roughly half the size of
      everything else, was a single word: <strong>Ad</strong>.</p>
      <p>Had she called, the person answering would have said her computer was infected, asked her to
      install a program so they could "clean it," and then asked her to log into her bank so they
      could "check for unauthorized charges." That last step is the point of the whole exercise. It
      lets them see which of your accounts is worth taking.</p>`,
    tells: [
      "The warning arrived on its own, in the middle of something unrelated. Real security warnings from your own devices don't come with a phone number to call.",
      "It appeared inside a web page, not from your computer itself. A web page cannot see whether your screen is being recorded.",
      "It carried a logo — which costs nothing to copy — and no other proof.",
      "The tiny grey \"Ad\" label. It's deliberately easy to miss, and on a phone it's smaller still.",
      "It wanted an immediate phone call. Real problems don't need to be handled in the next sixty seconds.",
    ],
    doThis: `<p><strong>Close it. That's the entire fix.</strong> A pop-up or an advertisement cannot
      harm your computer just by being on the screen — it's a picture. If it won't close, or the
      screen seems frozen, hold the power button until the machine turns off. You have not broken
      anything and you have not lost anything.</p>
      <p>If you're genuinely worried afterward, go to the company yourself: type the address in, or
      call the number on your own paperwork. Never the number in the warning.</p>`,
    verify: "Microsoft, Apple, and Google will never call you, and never put a phone number in a security warning. There is no exception to this.",
  },
  {
    slug: "grandson-in-jail",
    title: "My grandson called from jail and asked me not to tell his parents",
    blurb: "It sounded exactly like him. That is now the easy part for a scammer.",
    kind: "Grandparent scam · AI voice cloning",
    scenario: `<p>The phone rang just after nine at night. A young man's voice, upset and rushed:
      <em>"Grandma? I'm in trouble. There was an accident and I've been arrested. Please don't tell
      Mom and Dad — I'll never hear the end of it."</em></p>
      <p>Then another man came on the line, calm and official, describing himself as the public
      defender. Bail could be posted tonight. A courier could come to the house to collect the cash.</p>`,
    reality: `<p>The grandson was asleep at home, forty miles away. The voice on the phone was a clone,
      generated from a few seconds of him talking in a video his sister had posted publicly.</p>
      <p>The request not to tell his parents is not embarrassment. It's isolation — the single
      most reliable sign of a scam in progress, because the fastest way to end this call is one text
      message to anyone else in the family.</p>`,
    tells: [
      "Unexpected contact, extreme emotion, and an urgent unusual payment — all three flags in the first thirty seconds.",
      "A request for secrecy from family. Real lawyers, real police, and real hospitals all want you to call your family.",
      "Cash handed to a courier at your door. No legitimate bail process has ever worked this way.",
      "A second, calmer \"official\" who takes over the call. The panicked voice creates the emotion; the calm voice makes it credible.",
      "They keep you on the line. They cannot let you hang up and check.",
    ],
    doThis: `<p><strong>Hang up and call your grandson yourself</strong>, on the number already in your
      phone. A cloned voice cannot answer your call. If you can't reach him, call his parents,
      his roommate, anyone — you are not betraying him by checking.</p>
      <p>You can also just ask for the family password. If your family has agreed on one, this call
      ends in four seconds.</p>`,
    verify: "Agree on a family password tonight. One word a stranger could never know, that anyone claiming an emergency has to say. It costs nothing and it defeats every voice-cloning scam at once.",
  },
  {
    slug: "bank-said-move-my-money",
    title: "My bank's fraud department told me to move my money to a safe account",
    blurb: "Three callers, three days, one crew. The scam the FBI calls the Phantom Hacker.",
    kind: "Phantom Hacker",
    scenario: `<p><strong>Tuesday.</strong> A pop-up warned of a virus. He called the number, and a
      polite technician installed a program to "clean things up," then asked him to log into his
      accounts to check for damage.</p>
      <p><strong>Thursday.</strong> His bank's fraud department called. They already knew about the
      computer problem — which made them credible. A foreign hacker was inside his accounts. His
      money had to be moved to a secure account they had set up.</p>
      <p><strong>Saturday.</strong> A federal official called to confirm the investigation was real,
      and told him not to discuss it with his family or his branch. When he hesitated, an email
      arrived on convincing government letterhead.</p>`,
    reality: `<p>All three callers were the same crew. The FBI calls this the Phantom Hacker, and it has
      taken more than a billion dollars from Americans since 2024. It is the scam most likely to take
      everything — checking, savings, and retirement — because the victim believes they are
      protecting their money, not losing it.</p>
      <p>The three-act structure exists to build trust one layer at a time. Each impostor makes the
      next one believable.</p>`,
    tells: [
      "It began with an unsolicited computer warning — the entry point for the whole scheme.",
      "The second caller knew about the first. That's not proof of legitimacy; it's proof they're working together.",
      "The instruction to keep it secret from family and from your own bank branch. This is the signature move, and it is never legitimate.",
      "Official-looking letterhead produced on demand. Documents are trivially easy to fake.",
      "The core request: move your money somewhere to keep it safe.",
    ],
    doThis: `<p><strong>Hang up and call your bank on the number printed on your debit card.</strong>
      Not the number that called you, not a number from an email — the physical card in your wallet.
      Tell them exactly what you were told. They will know immediately.</p>
      <p>Then talk to your family, precisely because you were told not to.</p>`,
    verify: "No bank and no government agency will ever ask you to move money to keep it safe. There is no version of that request that is real.",
  },
  {
    slug: "met-someone-online",
    title: "He never asked me for money. He asked me to invest.",
    blurb: "Four months of daily conversation before the subject ever came up. That was the plan.",
    kind: "Romance and investment scam",
    scenario: `<p>It started with a wrong-number text — a friendly apology, then a real conversation.
      He was an engineer working on a contract overseas. Over four months they spoke every day. He
      remembered her doctor's appointments and asked how her knee was doing.</p>
      <p>He never asked her for a penny. Instead, he mentioned a trading platform he used. She put in
      $500 to try it. The balance climbed. She withdrew $300 and it landed in her account the next
      day, exactly as promised.</p>
      <p>So she invested $60,000. When she tried to withdraw it, the platform said she owed $9,000 in
      taxes before the funds could be released.</p>`,
    reality: `<p>The platform was a website with numbers on it. There were no investments and no
      trading. The small withdrawal that worked perfectly was not a glimpse of a real system — it was
      a $300 marketing expense, spent to earn a $60,000 return.</p>
      <p>Investment fraud is now the most expensive scam aimed at older adults by a wide margin:
      $3.5 billion reported in 2025, nearly half of all elder fraud losses. It very often begins as
      friendship rather than romance.</p>`,
    tells: [
      "A stranger who contacted her, by an accident that wasn't an accident.",
      "Months of warmth with no request. Patience is the investment; you are the return.",
      "There was always a reason he couldn't meet or video call.",
      "The small withdrawal that worked. This is the mechanism that convinces careful, intelligent people — and it's the strongest sign of a fake platform, not a real one.",
      "Fees or taxes owed before you can withdraw. No real investment works this way. Taxes are paid to a government, afterward, not to a platform in advance.",
    ],
    doThis: `<p><strong>Stop sending money and talk to someone today</strong> — your own bank, a
      financial adviser you found yourself, or the AARP Fraud Watch Helpline at 877-908-3360. Take
      screenshots before anything disappears.</p>
      <p>If someone you know is in this situation, be gentle. Mockery guarantees silence, and silence
      is what makes the loss larger.</p>`,
    verify: "Never send money, gift cards, or cryptocurrency to anyone you have not met in person — no matter how long you've been talking. And run any investment past your own bank first. It's free and takes ten minutes.",
  },
  {
    slug: "get-your-money-back",
    title: "Someone called offering to recover the money I already lost",
    blurb: "They knew exactly what happened to me. That's because victim lists are bought and sold.",
    kind: "Recovery scam",
    scenario: `<p>Three months after losing $40,000, she got a call from a firm specializing in fund
      recovery. They knew the amount. They knew roughly when it happened and how the money had left
      her account. They said a portion had been traced and frozen overseas, and that they could
      begin recovery for a $2,500 retainer.</p>
      <p>After everything, someone was finally going to help.</p>`,
    reality: `<p>They knew the details because being scammed once puts your name on a list, and that
      list is a product that gets resold to other crews. The knowledge that felt like proof was
      simply the thing they had purchased.</p>
      <p>In 2025, older adults reported more than half a billion dollars taken this way — every
      dollar of it from people who had already been robbed once. It's among the largest categories
      of elder fraud, and almost nobody warns people about it.</p>`,
    tells: [
      "Unexpected contact, again — they found her, months after the fact.",
      "Detailed knowledge of a private event. Painful but true: that information is for sale.",
      "An upfront fee, retainer, or tax before any recovery happens.",
      "Renewed hope, deployed deliberately. Hope works as well as fear, and after a loss it works better.",
      "Sometimes they'll claim to be from a government agency. Agencies never charge you to investigate a crime.",
    ],
    doThis: `<p><strong>Hang up, and report the recovery attempt itself</strong> at
      <a href="https://www.ic3.gov">ic3.gov</a> — it's a separate crime and worth reporting on its
      own.</p>
      <p>If money might genuinely be recoverable, the people who can do it are your own bank's fraud
      department and law enforcement. Both are free.</p>`,
    verify: "Nobody legitimate charges you money upfront to recover stolen money. Reporting a crime is always free. This is also the practical reason to tell someone after a scam — a person who talks about it is much harder to hit twice.",
  },
];

// blog index
page({
  file: "blog/index.html",
  title: "Real examples",
  desc: "Real scam scenarios explained step by step: what happened, what was actually going on, the warning signs, and what to do.",
  current: "/blog/",
  depth: 1,
  body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Stories, taken apart</p>
    <h1>Real examples, explained</h1>
    <p class="lede">Every one of these worked on someone careful and intelligent. Each is broken down
    the same way: what happened, what was actually going on, the signs, and what to do instead.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <ul class="posts">
      ${POSTS.map(p => `<li>
        <a href="./${p.slug}.html">${p.title}</a>
        <p>${p.blurb}</p>
      </li>`).join("\n      ")}
    </ul>
    <div class="callout callout--amber" style="margin-top:2.5rem">
      <p><strong>Notice what these have in common.</strong> Different technology, different stories,
      different decades of experience among the people they worked on — and the same three steps
      every time. Unexpected contact, a spike of emotion, an unusual request.
      <a href="../how-scams-work.html">That's the pattern worth learning.</a></p>
    </div>
  </div>
</section>
`,
});

// individual posts
POSTS.forEach((p, i) => {
  const next = POSTS[(i + 1) % POSTS.length];
  page({
    file: `blog/${p.slug}.html`,
    title: p.title,
    desc: p.blurb,
    current: "/blog/",
    depth: 1,
    body: `
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">${p.kind}</p>
    <h1>${p.title}</h1>
    <p class="lede">${p.blurb}</p>
  </div>
</section>

<section>
  <div class="wrap">
    <article>
      <h2>What happened</h2>
      <div class="scenario">${p.scenario}</div>

      <h2>What was actually going on</h2>
      ${p.reality}

      <h2>The warning signs</h2>
      <ul>
        ${p.tells.map(t => `<li>${t}</li>`).join("\n        ")}
      </ul>

      <h2>What to do</h2>
      ${p.doThis}

      <div class="callout callout--green">
        <p><strong>Verify through your own door.</strong> ${p.verify}</p>
      </div>

      <h2>Read next</h2>
      <p><a href="./${next.slug}.html">${next.title}</a></p>
      <p><a href="../it-just-happened.html">If something has already happened, start here →</a></p>
    </article>
  </div>
</section>
`,
  });
});

console.log("built:", fs.readdirSync(OUT).join(", "), "+ blog/", fs.readdirSync(path.join(OUT, "blog")).length, "pages");
