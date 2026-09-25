# Run log

One entry per session: date, states and clusters covered, counts by tier, blockers,
sources that worked best, next step.

## 25-Sep-2026: Session 1 (setup)
- **Covered:** no states or clusters yet. Setup only (CLAUDE.md Section 14, steps 1 to 3).
- **Counts:** Tier A 0, Tier B 0, Tier C 0, Longterm 0, Rejected 0.
- **Built:** CLAUDE.md saved to the repo; `config/states.json` (37 state entries, 159 clusters, regional keywords);
  `config/exclusions.txt` (Neev Seeds, Kasturi India, MW Wiretec, PJS Commodities); scripts `common`, `db`,
  `score`, `dedupe`, `audit_website`, `wayback_check`, `progress`, `export_xlsx`; 35 offline tests on fictional
  fixtures (decayed site scores 9 of 9 checkable points, modern HTTPS site scores 0); empty master workbook.
- **Input lists:** `input/` is empty, nothing to process.
- **Blockers:**
  1. Network policy (Section 0 stop condition): outbound fetches to company websites, acuite.in, tofler.in,
     web.archive.org, indiamart.com return 403 from the environment's egress proxy, for scripts and WebFetch.
     WebSearch works (it surfaces Acuite rationale PDFs for Ludhiana) but the PDFs cannot be opened here.
  2. The GitHub repo is public, so lead data (`data/*.db`, `data/work/`, `input/`, `output/`) is git-ignored.
     Until the repo is private or another store is agreed, the DB does not persist between cloud sessions.
  3. PageSpeed API without a key returns 429: decay point 7 is skipped and noted until `PSI_API_KEY` is set.
- **Sources that worked best:** not applicable yet.
- **Next step:** once network access allows it, run `audit_website.py` on 5 real manufacturer websites and show
  the scores (Section 14 step 2), then start Wave 1, Punjab, Ludhiana with rating rationales.
