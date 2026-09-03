# Active work claims

Multiple Claude Code sessions build in this repo at once. `git` merges text,
not intent — it will happily report "no conflict" for two different
implementations of the same feature. See `~/Claude/coderiver/.claude/CLAIMS.md`
for the incident that motivated this file.

**Before starting non-trivial work** (a new subcommand, a new module, a schema
or wire-format change — not a typo fix), add a row below. **Remove your row**
when you commit, or the work is abandoned.

This file is advisory, not a lock: nothing enforces it, and a stale row
(clearly past its own "by" estimate with no matching commit) is safe to
ignore. It exists to make a five-second check ("is someone already doing
this?") possible before you spend an hour finding out the hard way.

| Started (UTC) | What | By (rough) |
|---|---|---|
