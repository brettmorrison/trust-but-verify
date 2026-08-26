#!/usr/bin/env python3
"""
Audio narration, for blind/low-vision visitors who want to listen rather
than (or in addition to) using a screen reader. Zero-JS, zero-tracking,
same static-file pattern as the PDFs and talk decks: generate locally,
commit the .mp3, link it with a plain <audio controls> element.

Two voice engines:

- macOS's built-in `say` (free, no API key, no network call) for most
  pages -- converted AIFF -> MP3 via ffmpeg, both local tools. Every
  language this project translates into has a native macOS voice
  (checked: es, vi, zh, ru, ko all have one -- see MAC_VOICES below).
- ElevenLabs, for the ~20 highest-value ENGLISH pages (TOP20 below), plus
  -- as of 2026-08-25, Brett's call after hearing the quality gap -- the
  top scam-type articles in the 5 priority non-English languages, one
  language and tier at a time as translations land and quota allows (see
  LANG_EL_PAGES below). Requires the ELEVENLABS_API_KEY environment
  variable -- NEVER hardcode a key here, this repo is public. Check
  remaining quota (elevenlabs.io/app/subscription) before adding a new
  language or tier to LANG_EL_PAGES -- a full scam-type article runs
  ~5,000 characters, so 5 languages x 5 articles is ~125k characters, more
  than one Creator-plan billing cycle by itself. Pace it.

    ELEVENLABS_API_KEY=... python3 build/make_audio.py          # everything
    python3 build/make_audio.py                                  # macOS-only pages, skips English TOP20 if no key set

Regenerate a page's audio whenever its content changes meaningfully enough
that the stale narration would be actively wrong (not for every typo fix).
"""
import os, re, subprocess, html, urllib.request, urllib.error, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_ROOT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "assets", "audio")
EL_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # "Rachel", a stock ElevenLabs voice
EL_MODEL = "eleven_multilingual_v2"
# eleven_multilingual_v2 doesn't support Vietnamese at all (confirmed
# against ElevenLabs' own docs) -- Turbo v2.5 does. Default model above
# covers es/zh/ru/ko; override per-language here only where needed.
EL_MODEL_OVERRIDE = {"vi": "eleven_turbo_v2_5"}

# One native macOS voice per language this project translates into.
# Confirmed available via `say -v '?'` on the machine that runs this script.
MAC_VOICES = {
    "en": "Samantha",
    "es": "Paulina",   # es_MX -- Latin American Spanish, matches this
                        # project's likely US-based Spanish-speaking audience
    "vi": "Linh",       # vi_VN
    "zh": "Tingting",   # zh_CN, Simplified -- matches this project's
                        # existing Simplified-Chinese translation convention
    "ru": "Milena",     # ru_RU
    "ko": "Yuna",       # ko_KR
}

# The ~20 highest-value pages -- the core method, the crisis-moment page,
# and the scam types this project's own citations show are most common or
# highest-loss. Everyone else still gets narration, just via the free
# macOS voice (see ALL_PAGES below). Brett's call: keep ElevenLabs spend
# scoped to this set, not the whole site.
TOP20 = [
    "home", "the-three-steps", "warning-signs", "about", "i-think-i-was-scammed",
    "scams/phantom-hacker", "scams/tech-support-popup", "scams/grandparent-scam",
    "scams/government-impersonation", "scams/romance-scam", "scams/job-scams",
    "scams/investment-and-crypto", "scams/medicare-scams", "scams/voice-cloning",
    "scams/delivery-toll-recall-texts", "scams/virtual-kidnapping", "scams/recovery-scam",
    "how-they-ask-to-be-paid", "for-family", "scams/sim-swap",
]

# Everything else that's worth narrating -- free macOS voice.
# (give-this-talk.md is excluded: it's a navigational hub page whose real
# content is a card grid, not prose -- narrating just its two-sentence
# intro produced a useless 4-second clip.)
REST = [
    "scams/charity-scams", "scams/lottery-sweepstakes", "scams/home-repair",
    "scams/phishing", "how-they-got-your-information", "for-facilities",
]

ALL_PAGES = TOP20 + REST

# Non-English pages worth narrating, one list per language, macOS voice
# only (see MAC_VOICES). Filled in as translations land -- "slowly," per
# Brett -- so a language only appears once it has real translated content
# worth reading aloud. Slugs are filenames relative to content/<lang>/,
# same convention as TOP20/REST above.
SCAM5 = [
    "scams/phantom-hacker", "scams/tech-support-popup", "scams/grandparent-scam",
    "scams/government-impersonation", "scams/romance-scam",
]

LANG_PAGES = {
    "es": [
        "nucleo",  # the combined home/three-steps/warning-signs landing page
        # the 5 scam articles moved to LANG_EL_PAGES (ElevenLabs) below
    ],
    # vi/zh/ru/ko: free voice for now -- interim narration while their
    # ElevenLabs upgrades queue up per the paced rollout (see
    # LANG_EL_PAGES). Move a language's SCAM5 list here -> there as its
    # ElevenLabs batch actually runs, same pattern as Spanish.
    "vi": list(SCAM5),
    "zh": list(SCAM5),
    "ru": list(SCAM5),
    "ko": list(SCAM5),
}

# Non-English pages worth the ElevenLabs upgrade, one list per language.
# Brett's call (2026-08-25): front-load the top 5 scam articles across all
# 5 priority languages, tier by tier, paced against real remaining quota
# (check elevenlabs.io/app/subscription before adding to this list -- a
# full article is ~5,000 characters, so a 5-article tier for one language
# is ~25,000). Filled in as both translation AND budget allow.
LANG_EL_PAGES = {
    "es": list(SCAM5),
}


def split_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            return meta, text[end + 4:].strip()
    return meta, text


def markdown_to_speech_text(body):
    s = body
    # Pages like home.md carry a raw-HTML card grid (internal-link menu)
    # after the prose -- reading tag soup aloud is useless, and a flat list
    # of card links doesn't work as linear narration anyway. Stop the
    # narration at the first raw HTML block; the prose above it is always
    # a complete, self-contained thought at that point in every page this
    # script currently covers.
    html_start = re.search(r"\n<(div|figure)\b", s)
    if html_start:
        s = s[:html_start.start()]
    # Strip the warning-band blockquote lines some pages carry (not present
    # on English content, but harmless to guard against).
    s = re.sub(r"^>.*$", "", s, flags=re.M)
    # markdown attr_list heading IDs, e.g. "## Header {#anchor}"
    s = re.sub(r"\s*\{#[^}]+\}", "", s)
    # Links: [text](url) -> text
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    # Bold/italic markers
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)
    # Headings -> plain sentence, with a pause after
    s = re.sub(r"^#{1,6}\s*(.+)$", r"\1.", s, flags=re.M)
    # List markers
    s = re.sub(r"^\s*[-*]\s+", "", s, flags=re.M)
    s = re.sub(r"^\s*\d+\.\s+", "", s, flags=re.M)
    # Horizontal rules and stray markdown table pipes
    s = re.sub(r"^-{3,}$", "", s, flags=re.M)
    s = re.sub(r"\|", " ", s)
    # Phone numbers already read fine digit-by-digit via either engine.
    # Safety net for any remaining raw HTML this script didn't anticipate.
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n\n", s).strip()
    return s


def find_source(lang, slug):
    # home.md has slug "/", not a filename match -- handle directly.
    if lang == "en" and slug == "home":
        return os.path.join(CONTENT_ROOT, "en", "home.md")
    return os.path.join(CONTENT_ROOT, lang, slug + ".md")


def out_path(lang, slug, ext):
    # Flatten "scams/foo" -> "scams_foo.mp3", matching the og-image naming
    # convention elsewhere in this build, so assets/audio/ stays one flat
    # directory (no subdirs to create/copy). English keeps its original,
    # already-committed filenames (no lang prefix); every other language
    # gets one so e.g. Spanish and English "phishing" narration don't collide.
    flat = slug.replace("/", "_")
    if lang != "en":
        flat = lang + "_" + flat
    return os.path.join(OUT, flat + "." + ext)


def make_mac(lang, slug):
    text = markdown_to_speech_text(
        split_front_matter(open(find_source(lang, slug), encoding="utf-8").read())[1]
    )
    aiff, mp3 = out_path(lang, slug, "aiff"), out_path(lang, slug, "mp3")
    subprocess.run(["say", "-v", MAC_VOICES[lang], "-o", aiff, text], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
         "-codec:a", "libmp3lame", "-qscale:a", "4", mp3],
        check=True,
    )
    os.remove(aiff)
    print("wrote %s (%.1f MB, macOS, %s)" % (mp3, os.path.getsize(mp3) / 1e6, lang))


def make_elevenlabs(lang, slug, api_key):
    text = markdown_to_speech_text(
        split_front_matter(open(find_source(lang, slug), encoding="utf-8").read())[1]
    )
    mp3 = out_path(lang, slug, "mp3")
    model = EL_MODEL_OVERRIDE.get(lang, EL_MODEL)
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/text-to-speech/" + EL_VOICE_ID,
        data=json.dumps({"text": text, "model_id": model}).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as e:
            print("ElevenLabs FAILED for %s/%s: %s %s" % (lang, slug, e.code, e.read().decode()[:200]))
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print("ElevenLabs timeout/network error for %s/%s (attempt %d/3): %s" % (lang, slug, attempt + 1, e))
            if attempt == 2:
                return False
    with open(mp3, "wb") as f:
        f.write(data)
    print("wrote %s (%.1f MB, ElevenLabs/%s, %d chars)" % (mp3, len(data) / 1e6, model, len(text)))
    return True


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    api_key = os.environ.get("ELEVENLABS_API_KEY")

    if api_key:
        todo = [s for s in TOP20 if not os.path.exists(out_path("en", s, "mp3"))]
        total_chars = 0
        for slug in todo:
            text = markdown_to_speech_text(
                split_front_matter(open(find_source("en", slug), encoding="utf-8").read())[1]
            )
            total_chars += len(text)
        skipped = len(TOP20) - len(todo)
        print("TOP20: %d already done, %d to do, %d characters" % (skipped, len(todo), total_chars))
        for slug in todo:
            make_elevenlabs("en", slug, api_key)

        for lang, slugs in LANG_EL_PAGES.items():
            todo = [s for s in slugs if not os.path.exists(out_path(lang, s, "mp3"))]
            total_chars = 0
            for slug in todo:
                text = markdown_to_speech_text(
                    split_front_matter(open(find_source(lang, slug), encoding="utf-8").read())[1]
                )
                total_chars += len(text)
            print("%s (ElevenLabs): %d already done, %d to do, %d characters" %
                  (lang, len(slugs) - len(todo), len(todo), total_chars))
            for slug in todo:
                make_elevenlabs(lang, slug, api_key)
    else:
        print("No ELEVENLABS_API_KEY set -- skipping English TOP20 and LANG_EL_PAGES (run with the env var set to do those).")

    for slug in REST:
        if os.path.exists(out_path("en", slug, "mp3")):
            continue
        make_mac("en", slug)

    for lang, slugs in LANG_PAGES.items():
        for slug in slugs:
            if os.path.exists(out_path(lang, slug, "mp3")):
                continue
            make_mac(lang, slug)
