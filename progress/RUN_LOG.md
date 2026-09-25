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

### 25-Sep-2026 (same session, later): Ludhiana search-only pass
- **Why:** the user asked for the leads sheet while page fetches were still blocked, so this pass used web search only.
- **Covered:** Punjab, Ludhiana. Four parallel sweeps: Acuité rationales; CARE, ICRA, CRISIL, Infomerics, India Ratings and
  Brickwork rationales; 2025 and 2026 trade fair exhibitor pages; expansion news and SME IPO filings.
- **Output:** `output/Candidates_Ludhiana_UNVERIFIED.xlsx` (git-ignored): 30 candidates (Strong 3, Good 5, Check 22),
  27 follow-up names, 58 screened out with reject codes. No Active leads: none has had the website audit,
  owner-contact capture or MCA checks. Raw sweep data in `data/work/ludhiana_*.json` (git-ignored).
- **Counts in DB:** candidates 30 (status NEW), sources logged 69, leads 0, rejected 0.
- **Blockers:** (1) page fetches still blocked by the network policy; (2) the session's web search allowance
  (200 searches) is spent, so every sweep stopped early; (3) the repo is still public.
- **Sources that worked best:** CARE and CRISIL press releases (revenue in search summaries); Messe Frankfurt
  exhibitor pages (Automechanika, Heimtextil, Eurobike) show Ludhiana addresses; SME IPO coverage (DRHP figures).
  Acuité pages are poorly indexed by city and mostly return 2014 to 2019 rationales.
- **Next step:** in a session with Full network access, verify the 8 Strong and Good candidates first (website audit,
  turnover from the source document, owner mobile, MCA status), then work through the Check rows and the follow-ups.
  Ludhiana's source checkboxes stay unticked because the sweeps were incomplete.

### 25-Sep-2026 (same session, later): Ludhiana contact enrichment
- **Why:** the user asked for website links and the owners' own phone numbers, not the website numbers.
- **Done:** three parallel search sweeps for all 30 candidates: official websites (21 of 24 remaining candidates
  found), current directors from MCA aggregators (23 of 24), probable next-gen directors, and the company's own
  listing pages (IndiaMART, TradeIndia, Justdial, ExportersIndia, exhibitor and association entries) where owners
  publish their mobiles. 6 listings name the owner or a director as the contact (Shingora, Rex Sewing, Shiva Texfabs,
  Surindera Cycles, Vidhata, Yerik).
- **Owner mobiles:** not written into the sheet. Page fetches are still blocked, and numbers read from search summaries
  cannot be checked against the source page. The sheet links each listing so the team can read the number directly.
  Data brokers, Truecaller-style lookups and bought lists stay excluded (Section 8).
- **Changed by the new evidence:** screened out Sobhagia Sales (Sportking group, R4), Eastman Cast and Forge (Eastman
  Group, R4), Aarti Steels (above Rs 500 Cr, R1), Falcon Garden Tools, Lotus Cycles and Upper India Steel (below
  Rs 50 Cr, R2). Vallabh Textiles moved from Strong to Check: after insolvency it is controlled by listed Sabrimala
  Industries (possible R4, user to decide). Shah Foils flagged for Wave 2 (Gujarat head office). Bansal Spinning
  (Rs 391 Cr) and Jawandsons (Rs 417 Cr) upgraded to Good.
- **Result:** 24 candidates (Strong 2, Good 9, Check 13), 64 screened out. Metro Tyres not researched (search
  allowance ran out again).
- **Next step:** unchanged: Full network access, then verify and capture owner mobiles from the linked listings.
