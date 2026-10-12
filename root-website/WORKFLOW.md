# ROOT 75-page build: the workflow (v2)

v1 was red-teamed on 12-Oct-2026 by three independent reviewers (Figma handoff, PM and compliance, ops and speed) who simulated real pages through it. The changelog at the end lists what changed and why.

## Principles
1. **Decide once, reuse 74 times.** One shell and one values file, built by script; one golden page per template (10) sets the layouts; 65 derivative pages inherit them. Exploration effort goes where it multiplies.
2. **Questions before layouts, layouts before code.** Mandatory questions by page type plus page-specific ones with a source; layout options only for the sections that decide the page (`rules/page-method.md`).
3. **Machines check everything; agents judge what machines cannot; people judge golden pages.** `gate.py` (build, lint, screenshots) on every page; an independent reviewer on every page; the user at the gates.
4. **Never block on a human.** Agents use a stated default plus a visible placeholder and log the question in the page memory; `questions.py` collects them; the orchestrator asks the user at gates.
5. **State lives on disk.** Page memory status, `review/NN/gate.json` and `verdict.json` (with the sha of the file they judged), `STATUS.md` from `status.py`. Any session resumes from files. Only the orchestrator runs git, after every run.

## Roles
| Role | Who | Writes |
|---|---|---|
| Orchestrator | main session | sitemap, values, site memory, patterns, questions; runs waves; asks the user; commits |
| Strategist | agent, every page | page memory sections 1 to 6 and 10 (golden: options for every key section; derivative: decides) |
| Judge | agent, golden pages only | final decisions in memory section 6 |
| Builder | agent, every page | `pages/src/NN-id.html`, memory sections 7 to 11; returns the gate JSON |
| Reviewer | agent, every page | `review/NN/verdict.json` via `scripts/verdict.py`; blind trace first, then the checklist |
| Fixer | builder again, once | applies blocking fixes; returns the gate JSON and an attestation per fix |
| Curator | one agent after the golden wave | promotes reusable CSS to `theme/patterns.css` and markup to `theme/components.html` |

## Per-page pipeline
- **Golden**: pack → Strategist → Judge → Builder (gate, max 3 loops) → Reviewer → if blocking fixes: Fixer → Reviewer (second round) → user gate.
- **Derivative**: pack → Strategist (decides) → Builder (gate, max 3 loops) → Reviewer → if blocking fixes: Fixer (gate + attestation, no second review).
- A page whose gate still fails after the builder's loops and one retry, or whose second review still has blocking fixes, is marked `needs-human`; the wave continues.
- Blocking (must-fix) is only: a claim or disclosure problem, an unanswered MUST question, the primary action not visible (first screen at 1440, 1.5 screens at 390), or a broken layout. Everything else is should-fix.

## Waves and gates
| Run | Pages | Gate |
|---|---|---|
| 0 Pilot | 01 Home (golden), 09 Start Trading (golden D), 10 Start Investing (derivative of 09) | User reviews the 3 pages, imports `00-kit.html` and `00-import-test.html` into Figma, answers the top questions |
| 1 Goldens | 03 Trade (A), 07 About (F), 17 Grievance (G), 29 Scheme detail (B), 42 SIP calculator (C), 57 PMS (H), 62 Distributor Partner (P), 65 Getting Started guide (E), then Curate | User approves the 10 golden pages: nothing inherits from an unapproved golden |
| 2 Phase 1 derivatives | the other 15 Phase 1 pages | Summary + questions |
| 3 Phase 2 and 3 derivatives | the other 47 pages (2 runs if needed) | Final summary, full rebuild, spot checks |
If a golden page changes after its derivatives exist, only the Builder re-runs for pages whose memory says "inherit NN".

## Human input
- Every page memory has an open-questions table (section 10) with the default used. `python3 scripts/questions.py` merges them into `memory/questions.md` after every run.
- At each gate the orchestrator asks the top 4 by impact (multiple choice, recommended default first), records answers in the Answered section, updates `memory/values.json` or `memory/site.md`, and runs a full rebuild (`build.py --all`, then lint and shoot). Value answers need no agent at all.
- Judges can raise `ask_user` items for close calls that are brand or business decisions; these join the gate questions.

## Speed and cost
- Briefs (`packs/NN-id.md`, about 13 KB) replace about 10 file reads per agent.
- Chromium runs at most 4 at a time (lock files); agents use a 300 s Bash timeout for the gate.
- Estimated agents: pilot about 13; goldens about 45; derivatives about 3 each (about 195). Re-review only on golden pages.

## Failure handling and resume
- `python3 scripts/status.py` shows each page's next stage (brief, judge, build, gate, fix, review, done) and flags stale results (the file changed after it was checked).
- A workflow run can be resumed in the same session with its run id; in a new session, re-run the wave with only the pages whose next stage is not done.
- Files are written atomically; parallel builds never touch shared files (the index is rebuilt only by `build.py --all`).

## Figma import
1. Install the fonts in Figma: Tiro Devanagari Hindi, Mukta, Red Hat Mono.
2. Import `figma/00-import-test.html` once and fill in the results table in `rules/figma-html.md`.
3. Import `figma/00-kit.html` and turn it into components and styles.
4. Import golden pages and every `.states.html` board at 1440 and 390; derivative pages at 1440, and at 390 where the mobile layout differs from their golden page.

## Changelog: red-team round 1 (12-Oct-2026)
| Finding | Change |
|---|---|
| Disclosure lint passed pages by accident (the header mega menu carries the F&O line) | Lint checks required disclosures inside `<main>` only; all four F&O bullets must sit in `#s-risk`; placement rules |
| Theme v1's unproven claims would be copied into 74 pages | `rules/claims.json` registry (blocked / unconfirmed / review); lint fails unconfirmed claims outside placeholders |
| No central journey or CTA map; one-flow-or-two leaked everywhere | sitemap "cta" per page (href, event, data receiver), parent hubs; header and mobile bar follow the page's company |
| Advice and comparison wording slipped through | wider patterns incl. ratings, awards, handpicked, comparisons, urgency; attributes and meta scanned |
| Generic, self-certified PM questions | mandatory question sets by page type + 3 sourced page-specific questions; trace table with answering sentence, checked by lint; reviewer traces blind first |
| Partner pages derived from About | new template P, golden 62 |
| F&O facts from model memory | placeholders + exchange links; box after the hero on F&O pages; version line |
| Rubric rewarded looks; no SEO checks | conversion hypothesis per option; primary action position measured; title, description, query, internal links linted |
| Interaction states lost in static pages | `<template data-state>` blocks rendered to a states board per page; D pages need 3+ states |
| No component kit; header and footer imported 150 times | `figma/00-kit.html` with all shell states; designer imports it first |
| Importer behaviour untested | `figma/00-import-test.html` + results table; static-mode CSS (flex stacks, real borders, whole-pixel type, real node dots, static tabs) |
| Template B markup would drift | curator promotes golden markup into `theme/components.html`; tables stack on phones; SVG gauges |
| No durable state | verdict and gate files with sha; status.py next stage; questions.py; commit after every run |
| Golden rejected after derivatives built | all goldens in one run with a user gate before any derivatives |
| Site-wide changes needed agent re-runs | values.json tokens; a value change is a 1-second rebuild |
| Lint loops and unfixable errors | `lint_allow`, max 3 gate loops, then needs-human |
| Workflow trusted agents' own reports | builder returns gate.py JSON; review skipped when the gate fails; fixed failed-page mapping |
| Subjective reviews flood needs-human | blocking fixes limited to four categories |
| Chromium contention vs Bash timeout | 4-slot lock, 300 s timeout, atomic folder swap, slices end at the footer |
