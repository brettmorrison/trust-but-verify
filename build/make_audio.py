#!/usr/bin/env python3
"""
Audio narration for a pilot set of English pages, for blind/low-vision
visitors who want to listen rather than (or in addition to) using a screen
reader. Zero-JS, zero-tracking, same static-file pattern as the PDFs and
talk decks: generate locally, commit the .mp3, link it with a plain
<audio controls> element.

Uses macOS's built-in `say` (free, no API key, no network call) with the
Samantha voice, then converts AIFF -> MP3 via ffmpeg. Both are local tools,
nothing is uploaded anywhere.

    python3 build/make_audio.py

Regenerate a page's audio whenever its content changes meaningfully enough
that the stale narration would be actively wrong (not for every typo fix).
"""
import os, re, subprocess, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content", "en")
OUT = os.path.join(ROOT, "assets", "audio")
VOICE = "Samantha"

# Pilot batch -- the core method plus the two pages it's built from.
# Expand this list once the pattern is proven; see BACKLOG.md.
PAGES = ["home", "the-three-steps", "warning-signs", "about"]


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
    # Phone numbers already read fine digit-by-digit via `say`; leave as-is.
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


def make(slug):
    src = find_source(slug)
    raw = open(src, encoding="utf-8").read()
    meta, body = split_front_matter(raw)
    text = markdown_to_speech_text(body)

    aiff = os.path.join(OUT, slug + ".aiff")
    mp3 = os.path.join(OUT, slug + ".mp3")
    subprocess.run(["say", "-v", VOICE, "-o", aiff, text], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
         "-codec:a", "libmp3lame", "-qscale:a", "4", mp3],
        check=True,
    )
    os.remove(aiff)
    size = os.path.getsize(mp3)
    print("wrote %s (%.1f MB)" % (mp3, size / 1e6))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug in PAGES:
        make(slug)
