# Working Rules for This Repo

This repo is the **system of record** for deal analysis. Chat is ephemeral; sessions end; uploaded files
disappear. Anything not committed here is lost.

## Knowledge-capture protocol (non-negotiable)

1. **Every analysis lands in the repo the moment it exists.** Any extraction, audit, computed table,
   agent-research finding, or derived conclusion produced during a session MUST be written to a dated file
   under `knowledge/` and committed+pushed in the same turn it is produced — before or immediately after
   reporting it in chat. Chat is for reporting results; the repo is where they live.
2. **The end-of-turn check:** before ending any turn, ask "does the repo now contain everything learned
   this turn?" If no — capture it first. A summary bullet in an existing doc does NOT count as capturing
   the underlying analysis (tables, cell references, methodology, exclusions).
3. **Uploaded source files that drive conclusions:** copy deliverable-grade workbooks/exhibits into
   `knowledge/exhibits/`. For large or raw source documents (models, rent rolls, sellers' reports), commit
   the *extraction* as a knowledge file with provenance (filename, vintage, tab/cell refs) so the analysis
   is reproducible without the source.
4. **Supersession, never silent revision.** When a number changes (bid, hold, rent path), add a dated
   supersession note to the affected doc(s) pointing to the new source. Stale figures must be findable and
   labeled, not overwritten.
5. **Provenance on every figure.** Knowledge files cite source file + tab/cell (models), report + vintage
   (third-party data), or method + n + exclusions (computed analyses).

## Repo map

- `knowledge/` — deal knowledge base (the product). Master doc: `Seasons-Meridian-Replacement-Cost-and-Supply-Economics.md`.
- `knowledge/exhibits/` — workbooks, charts, build scripts for exhibits.
- `SeasonsMeridian/`, `CanyonRidge/`, `comparison/`, `summary/`, `research/` — parcel-level land-use /
  supply-threat analysis (see each dir's methodology.md / decisions_log.md).

## Conventions

- Commit and push (`git push -u origin <branch>`) every time knowledge files change — do not batch at
  session end.
- Dated analyses: include "as of" dates in file headers; deal-status snapshots get a date in the filename
  or header.
- When starting work in a new deal repo, copy this CLAUDE.md into it first.
