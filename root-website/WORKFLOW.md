# ROOT 75-page build: the workflow (v1, pre red-team)

## Principles
1. **Decide once, reuse 74 times.** One shell (header, footer, theme CSS) built by script; one golden page per template sets the patterns; derivative pages inherit them. Exploration effort goes where it multiplies.
2. **Questions before layouts, layouts before code.** Every page: job and journey, then the PM's question list, then 2 to 3 layout options per section scored on a rubric, then HTML (`rules/page-method.md`).
3. **Machines check everything, people judge what matters.** Lint and screenshots run on every page automatically; agent review runs on every page; the user reviews golden pages and gate summaries.
4. **Never block on a human.** Agents use a stated default plus a visible placeholder, log the question, and carry on. The orchestrator batches questions to the user at gates.
5. **State lives on disk.** sitemap.json, memory/, pages/src/, figma/, review/. Any session can resume from the files; git commits after every wave.

## Roles
| Role | Who | Does | Writes |
|---|---|---|---|
| Orchestrator | main session | runs waves, merges questions and patterns, asks the user at gates, commits | memory/site.md, memory/questions.md, memory/patterns.md, theme/patterns.css |
| Strategist | agent per page | Steps 0 to 4 of the page method: job, journey, PM questions, section plan, 2 to 3 options per section | memory/pages/NN-id.md (sections 1 to 6, options) |
| Judge | agent per golden page | independent scoring of the options; can merge, veto, add missed questions | decisions into memory/pages/NN-id.md section 6 |
| Builder | agent per page | Step 5: HTML, build, lint, shoot, self-fix | pages/src/NN-id.html, memory sections 7 to 11 |
| Reviewer | agent per page | looks at screenshots (desktop and mobile), lint report, memory; checks question traceability, compliance, theme fidelity | verdict + fix list (returned, not written) |
| Fixer | the Builder again, once | applies the fix list | pages/src, memory change log |

## Per-page pipeline
Golden page: Strategist → Judge → Builder → Reviewer → (Fixer → Reviewer, once) → done or needs-human.
Derivative page: Strategist (decides with the rubric, inherits golden layouts) → Builder → Reviewer → (Fixer, once) → done or needs-human.

## Waves and gates
| Wave | Pages | Gate at the end |
|---|---|---|
| 0 Pilot | 01 Home (golden), 09 Start Trading (golden D), 10 Start Investing (derivative of 09) | User reviews the 3 pages and test-imports one into Figma; answers top questions; approves the method |
| 1 Phase 1 goldens | 03 Trade (A), 07 About (F), 17 Grievance (G) | User reviews the 3 golden pages |
| 2 Phase 1 rest | the other 16 Phase 1 pages | Summary + questions |
| 3 Phase 2 | goldens 29 Scheme detail (B), 42 SIP calculator (C), then 23 derivatives | Summary + questions |
| 4 Phase 3 | goldens 57 PMS (H), 65 Getting Started guide (E), then 23 derivatives | Final summary |
Within a wave, golden pages run first (in parallel); then a Curator step promotes their new patterns; then derivatives run in parallel.

## Human input
- Agents return open questions (question, why it matters, default used, owner). The orchestrator dedupes them into memory/questions.md.
- At each gate the orchestrator asks the user the top 4 by impact (multiple choice with a recommended default) and records answers in memory/site.md.
- Answers that change built pages trigger a targeted re-run of only the affected pages.

## Memory
- Page memory (`memory/pages/NN-id.md`): job, journey, questions, decisions with rejected options, components, actions, compliance, open questions, designer notes, change log.
- Site memory, pattern library, question log: orchestrator-owned, read by every agent.

## Failure handling
- Every stage returns structured output (schema). A null or failed stage is retried once; a second failure marks the page needs-human and the wave continues.
- Status per page is in its memory front matter; re-running a wave skips pages already reviewed as pass.
- Commit after every wave.

## Figma import
Open `figma/NN-id.html` in Chrome and capture with the html.to.design extension (or host the folder and import by URL in the html.to.design plugin) at 1440 and 390 widths. Fonts needed in Figma: Tiro Devanagari Hindi, Mukta, Red Hat Mono (all Google Fonts).
