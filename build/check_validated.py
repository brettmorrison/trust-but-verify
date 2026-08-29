#!/usr/bin/env python3
"""
Guard against silently overwriting a human validator's work.

THE FAILURE THIS PREVENTS: a native speaker validates a translated page --
the single most valuable, hardest-to-replace input this project gets. Later,
the English source changes and someone re-runs a translation pass over that
language. The regenerated file overwrites the validated one, the validator's
corrections are gone, and nothing anywhere says so. The page still LOOKS
fine. That's the worst kind of failure: expensive, invisible, and it burns
the goodwill of the exact volunteer this project most needs.

HOW IT WORKS: any content file whose frontmatter has a real `validated_by`
value (i.e. not "(none yet)") is registered here with a hash of its body.
Run this before and after any bulk translation/regeneration work:

    python3 build/check_validated.py --snapshot   # record current state
    ... do the translation work ...
    python3 build/check_validated.py             # verify nothing was clobbered

If a validated file's content changed, this exits non-zero and names the
file. It does NOT block the change -- sometimes a validated page genuinely
should be updated -- it just refuses to let it happen silently. Re-snapshot
deliberately after a change you actually intended.

Also usable as a plain audit: with no snapshot present, `--list` reports
which pages are validated and by whom.
"""
import os, re, sys, json, hashlib, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SNAPSHOT = os.path.join(ROOT, "build", ".validated_snapshot.json")
UNVALIDATED = "(none yet)"


def split_front_matter(text):
    meta = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = text[end + 4:]
    return meta, body


def validated_pages():
    out = {}
    for dirpath, _dirs, files in os.walk(CONTENT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            meta, body = split_front_matter(open(path, encoding="utf-8").read())
            who = meta.get("validated_by", "").strip()
            if who and who != UNVALIDATED:
                out[rel] = {
                    "validated_by": who,
                    "lang": meta.get("lang", "?"),
                    "hash": hashlib.sha256(body.strip().encode("utf-8")).hexdigest(),
                }
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", action="store_true",
                     help="Record the current validated pages + content hashes")
    ap.add_argument("--list", action="store_true",
                     help="List validated pages and who validated them")
    args = ap.parse_args()

    current = validated_pages()

    if args.list or (not args.snapshot and not os.path.exists(SNAPSHOT)):
        if not current:
            print("No validated pages yet -- every translated page still carries "
                  "the unvalidated-AI-translation banner.")
            print("(This guard activates automatically once the first native-speaker "
                  "validation lands.)")
        else:
            print("Validated pages (%d):" % len(current))
            for rel, info in sorted(current.items()):
                print("  %-55s %s  [%s]" % (rel, info["validated_by"], info["lang"]))
        sys.exit(0)

    if args.snapshot:
        json.dump(current, open(SNAPSHOT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("Snapshotted %d validated page(s)." % len(current))
        sys.exit(0)

    prior = json.load(open(SNAPSHOT, encoding="utf-8"))
    problems = []
    for rel, info in prior.items():
        if rel not in current:
            problems.append("%s: was validated by %s, now missing or its "
                            "validated_by was cleared" % (rel, info["validated_by"]))
        elif current[rel]["hash"] != info["hash"]:
            problems.append("%s: content CHANGED since validation by %s"
                            % (rel, info["validated_by"]))
    if problems:
        print("VALIDATED-CONTENT CHECK FAILED:")
        for p in problems:
            print("  " + p)
        print("\nIf these changes were intended, re-run with --snapshot to accept "
              "them. If not, restore from git before committing -- a validator's "
              "corrections are the hardest input in this project to replace.")
        sys.exit(1)
    print("OK -- %d validated page(s) unchanged." % len(prior))
