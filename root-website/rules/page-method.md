# The page method (v3: v2 after red-team round 1, plus the pilot review)

Think like a product manager first, a UX designer second, a front-end builder third. No layout before the page's questions are known; no HTML before a layout has beaten its alternatives.

**Read `rules/design-direction.md` before anything else.** The pilot was compliant but not desirable; v3 fixes that without weakening compliance.

## Step 0. Read
1. **`packs/NN-id.md`** (run `python3 scripts/pack.py NN` if it is missing). It holds the page card, journey neighbours, the mandatory questions for this page type, the compliance blocks for its flags, site values, site memory and the pattern library. Start here.
2. Open other files only when the brief points to them: the golden page's memory and source (derivatives), journey neighbours' memories, `context/*.md`, the relevant sections of `theme/sections-reference.html`, and the craft checklists named at the end of the brief.

## Step 1. Understand the page and its place in the journey
- **Job** (one sentence): "This page exists so that [user] can [task], and leaves ready to [next step]."
- **Arrival**: where people come from (nav, a Google query you name, an ad, an internal link, the app) and their awareness level (unaware, problem-aware, solution-aware, product-aware, ready to act).
- **Journey stage**: Discover, Evaluate, Act, Onboard, Use, Get help, or Verify. Previous page and next page(s) by URL. The primary action and its target are in the brief ("cta"); do not invent a different one.
- **Users** (codes) and their top three anxieties, in their words.
- **Success**: the primary action (one, marked `data-primary` on the page), at most one secondary action, and the measurement event.
- **Search**: the main query this page should rank for, the title (70 characters or fewer) and the description (70 to 160).

## Step 2. The questions the page must answer
- All **mandatory questions** for the page type from the brief.
- **At least three page-specific questions**, each with its source: a search query, a user-group anxiety, a Motilal Oswal pattern, or a client decision. A question that would be identical on every page does not count here.
- Order them as the visitor would ask them. Tag MUST or SHOULD.
- **What the page must not say** (licence boundaries, claims ROOT cannot prove yet; see `rules/claims.json`).
- **Traceability**: in memory section 4, each question names the section id that answers it (`s-charges`) and quotes the answering sentence in a few words. A link to another page does not answer a MUST question. Lint checks the ids exist.

## Step 3. Section plan
Ordered sections; each with its id (`s-<name>`), the question numbers it answers, a content outline (real headings and key copy points), and its component. Follow the template skeleton (brief) unless you state why not. Cut any section that answers nothing.

## Step 4. Layout exploration, where it pays
Explore options only for the sections that decide the page: the hero (always: 3 options, at least one led by a product visual), any form, data displays, and the page's key block (pricing table, calculator, steps, eligibility, credential wall). Standard sections (FAQ, closing CTA, risk box, related links) use the pattern library directly.
- **Option A** is the pattern-library layout. **B and C** differ in structure (hierarchy, layout, density or interaction), not decoration. All options use the ROOT theme.
- Each option: a three-line wireframe spec plus a **conversion hypothesis** ("puts the OTP field in the first screen at 390, so more visitors start").
- Score on the rubric, pick, and record one line on why the winner won and why each loser lost.
- Derivatives inherit the golden page's layouts by default ("inherit 09 s-steps"); explore only sections that are new or where the inherited layout fails this page's questions. With no judge, write the strongest argument against each decision before keeping it.

### Rubric (weight)
| Criterion | Weight |
|---|---|
| Desirability: would a 30-year-old professional want to use this after five seconds? (offer clear, visual, confident, calm) | 3 |
| Answers its questions, in the order asked | 3 |
| Moves the visitor to the next step (the primary action is visible on the first screen at 1440 and within 1.5 screens at 390) | 3 |
| Trust and compliance (claims rule, company named, disclosures) | 3, and any failure is a veto |
| Scannable hierarchy (5-second test: what is this, is it for me, what do I do) | 2 |
| Mobile at 390 (stacks cleanly, nothing cut off, tables stack) | 2 |
| Consistency with the pattern library | 1 |
| Figma editability (flex stacks, no tricks) | 1 |
Vetoes: an invented number or claim; a missing mandatory disclosure; content only visible through JavaScript; a primary action hidden on mobile; a first screen without a visual anchor or with placeholder chips outside fine print.

## Step 5. Build
Follow `rules/figma-html.md`. Write `pages/src/NN-id.html`, then run `python3 scripts/gate.py NN` (Bash timeout 300000). It builds, lints and screenshots, and prints one JSON line. Fix and re-run until `"ok": true`, **at most 3 loops**; if it still fails, stop, set memory status `needs-human`, and explain why in the memory change log. Then look at the screenshot slices in `review/NN-id/` and fix what looks wrong (each fix: run the gate again).

## Step 6. Save the page memory
`memory/pages/NN-id.md` from `_TEMPLATE.md`: the page's permanent context for the designer, the next agent and the client review. Section 11 (designer notes) is a list of interaction states (each one either on the states board or described), sticky elements, imagery to source, and anything the static file cannot show. Keep it factual and short. Derivative pages may keep sections 1 to 3 to a few lines each.
