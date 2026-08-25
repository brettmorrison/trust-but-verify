#!/usr/bin/env python3
"""
Audio narration for English pages, for blind/low-vision visitors who want
to listen rather than (or in addition to) using a screen reader. Zero-JS,
zero-tracking, same static-file pattern as the PDFs and talk decks:
generate locally, commit the .mp3, link it with a plain <audio controls>
element.

Two voice engines:

- macOS's built-in `say` (free, no API key, no network call) for most
  pages -- converted AIFF -> MP3 via ffmpeg, both local tools.
- ElevenLabs, for the ~20 highest-value pages only (TOP20 below), where
  the more natural voice is worth the cost. Requires the ELEVENLABS_API_KEY
  environment variable -- NEVER hardcode a key here, this repo is public.
  The key used this session is IP-restricted, scoped to text-to-speech
  only, and expires in 30 days by design.

    ELEVENLABS_API_KEY=... python3 build/make_audio.py          # everything
    python3 build/make_audio.py                                  # macOS-only pages, skips TOP20 if no key set

Regenerate a page's audio whenever its content changes meaningfully enough
that the stale narration would be actively wrong (not for every typo fix).
"""
import os, re, subprocess, html, urllib.request, urllib.error, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content", "en")
OUT = os.path.join(ROOT, "assets", "audio")
MAC_VOICE = "Samantha"
EL_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # "Rachel", a stock ElevenLabs voice
EL_MODEL = "eleven_multilingual_v2"

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


def find_source(slug):
    # home.md has slug "/", not a filename match -- handle directly.
    if slug == "home":
        return os.path.join(CONTENT, "home.md")
    return os.path.join(CONTENT, slug + ".md")


def out_path(slug, ext):
    # Flatten "scams/foo" -> "scams_foo.mp3", matching the og-image naming
    # convention elsewhere in this build, so assets/audio/ stays one flat
    # directory (no subdirs to create/copy).
    flat = slug.replace("/", "_")
    return os.path.join(OUT, flat + "." + ext)


def make_mac(slug):
    text = markdown_to_speech_text(
        split_front_matter(open(find_source(slug), encoding="utf-8").read())[1]
    )
    aiff, mp3 = out_path(slug, "aiff"), out_path(slug, "mp3")
    subprocess.run(["say", "-v", MAC_VOICE, "-o", aiff, text], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
         "-codec:a", "libmp3lame", "-qscale:a", "4", mp3],
        check=True,
    )
    os.remove(aiff)
    print("wrote %s (%.1f MB, macOS)" % (mp3, os.path.getsize(mp3) / 1e6))


def make_elevenlabs(slug, api_key):
    text = markdown_to_speech_text(
        split_front_matter(open(find_source(slug), encoding="utf-8").read())[1]
    )
    mp3 = out_path(slug, "mp3")
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/text-to-speech/" + EL_VOICE_ID,
        data=json.dumps({"text": text, "model_id": EL_MODEL}).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as e:
            print("ElevenLabs FAILED for %s: %s %s" % (slug, e.code, e.read().decode()[:200]))
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print("ElevenLabs timeout/network error for %s (attempt %d/3): %s" % (slug, attempt + 1, e))
            if attempt == 2:
                return False
    with open(mp3, "wb") as f:
        f.write(data)
    print("wrote %s (%.1f MB, ElevenLabs, %d chars)" % (mp3, len(data) / 1e6, len(text)))
    return True


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    api_key = os.environ.get("ELEVENLABS_API_KEY")

    if api_key:
        todo = [s for s in TOP20 if not os.path.exists(out_path(s, "mp3"))]
        total_chars = 0
        for slug in todo:
            text = markdown_to_speech_text(
                split_front_matter(open(find_source(slug), encoding="utf-8").read())[1]
            )
            total_chars += len(text)
        skipped = len(TOP20) - len(todo)
        print("TOP20: %d already done, %d to do, %d characters" % (skipped, len(todo), total_chars))
        for slug in todo:
            make_elevenlabs(slug, api_key)
    else:
        print("No ELEVENLABS_API_KEY set -- skipping TOP20 (run with the env var set to do those).")

    for slug in REST:
        if os.path.exists(out_path(slug, "mp3")):
            continue
        make_mac(slug)
