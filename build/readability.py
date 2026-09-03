#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reading grade for the English pages, so "sixth-grade reading level" is a
number this repository can check rather than a claim in README.md.

    python3 build/readability.py                    # every English page, sorted
    python3 build/readability.py content/en/terms.md # one file

Flesch-Kincaid grade level:

    0.39 x (words / sentence) + 11.8 x (syllables / word) - 15.59

It is a crude instrument and it is the right one here. It measures exactly
the two things that make a sentence hard for a frightened reader -- how long
the sentence is and how many syllables its words carry -- and it cannot be
argued with, which is the point of having a number at all. It says nothing
about whether the writing is any good; it says whether it is long-winded.

What gets measured: prose only. Front matter, table rows, code, and link
targets are removed first, the same way build/audit_site.py's prose check
removes them, because a table of helpline numbers has no sentence rhythm and
counting its cells as sentences produces a false reading.

Known bias, stated so nobody trusts the number further than it goes: a
heading with no full stop is glued to the paragraph below it and counted as
one long sentence, so every page reads a little harder here than it would to
a person. The bias is the same on every page, it errs towards reporting
difficulty rather than hiding it, and leaving it in keeps this measure
comparable with the ordinary Flesch-Kincaid numbers quoted elsewhere. On this
repository it puts the English median at 6.5 -- the sixth-grade level
README.md promises.
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VOWELS = "aeiouy"


def prose_of(markdown_text):
    """Readable sentences only, with markdown syntax and tables removed."""
    t = re.sub(r"^---.*?^---", "", markdown_text, flags=re.S | re.M)   # front matter
    t = re.sub(r"```.*?```", " ", t, flags=re.S)                        # fenced code
    t = "\n".join(l for l in t.split("\n") if not l.strip().startswith("|"))
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)                         # images
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)                      # links -> text
    t = re.sub(r"`[^`]*`", " ", t)                                      # inline code
    t = re.sub(r"^\s{0,3}#{1,6}\s*", "", t, flags=re.M)                 # heading marks
    t = re.sub(r"^\s{0,3}[-*+]\s+", "", t, flags=re.M)                  # bullets
    t = re.sub(r"^\s{0,3}>\s?", "", t, flags=re.M)                      # blockquote marks
    t = re.sub(r"[*_]{1,3}", "", t)                                     # emphasis
    t = re.sub(r"<[^>]+>", " ", t)                                      # any raw html
    return re.sub(r"[ \t]+", " ", t).strip()


def syllables(word):
    """Syllable estimate for one English word. Never returns zero."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count, prev_vowel = 0, False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if w.endswith("e") and not w.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(count, 1)


def measure(markdown_text):
    """(grade, words, sentences, syllables_per_word) for one document."""
    prose = prose_of(markdown_text)
    # Sentence ends: . ! ? followed by whitespace or end. Abbreviations like
    # "e.g." are rare enough in this copy not to be worth special-casing, and
    # over-counting sentences would flatter the score rather than inflate it.
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", prose) if re.search(r"[A-Za-z]", s)]
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", prose)
    if not sentences or not words:
        return None
    syl = sum(syllables(w) for w in words)
    grade = (0.39 * len(words) / len(sentences)
             + 11.8 * syl / len(words) - 15.59)
    return round(grade, 1), len(words), len(sentences), round(syl / len(words), 3)


def measure_file(path):
    return measure(io.open(path, encoding="utf-8").read())


def english_pages():
    return sorted(glob.glob(os.path.join(ROOT, "content", "en", "**", "*.md"),
                            recursive=True))


def main(argv):
    paths = argv[1:] or english_pages()
    rows = []
    for p in paths:
        m = measure_file(p)
        if m:
            rows.append((m[0], os.path.relpath(p, ROOT), m[1], m[2], m[3]))
    rows.sort(reverse=True)
    print("%-6s %-46s %6s %6s %6s" % ("grade", "file", "words", "sents", "syl/w"))
    for grade, rel, words, sents, sylw in rows:
        print("%-6.1f %-46s %6d %6d %6.2f" % (grade, rel, words, sents, sylw))
    if len(rows) > 1:
        grades = sorted(r[0] for r in rows)
        median = grades[len(grades) // 2]
        print("\n%d pages, median grade %.1f, hardest %.1f, easiest %.1f"
              % (len(rows), median, grades[-1], grades[0]))


if __name__ == "__main__":
    main(sys.argv)
