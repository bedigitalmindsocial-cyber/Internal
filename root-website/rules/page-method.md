# The page method (every one of the 75 pages goes through this)

Think like a product manager first, a UX designer second, a front-end builder third. Order matters: no layout before the page's questions are known; no HTML before a layout has beaten its alternatives.

## Step 0. Read (budget: skim, do not paste whole files into your reply)
1. `sitemap.json` entry for the page: template, entity, flags, primary CTA, audiences.
2. `context/facts.md` (business, users, tasks, conversions, compliance traps, registration data).
3. `rules/voice-and-claims.md`, `rules/compliance-blocks.md`, `rules/figma-html.md`.
4. `memory/site.md` (site-wide decisions) and `memory/patterns.md` (the pattern library).
5. If the page is a derivative: the golden page's memory for its template (`memory/pages/<golden>.md`) and its built source in `pages/src/`.
6. Memory of journey neighbours if it exists (the parent hub, the page users go to next).
7. Only the relevant sections of `theme/sections-reference.html`.
8. `context/*.md` from earlier sessions (decisions, placeholders, Motilal patterns) where relevant.

## Step 1. Understand the page and its place in the journey
Write, in this order:
- **Job** (one sentence): "This page exists so that [user] can [task], and leaves ready to [next step]."
- **Arrival**: where people come from (nav, Google query, ad, internal link, app) and their awareness level (unaware, problem-aware, solution-aware, product-aware, ready to act).
- **Journey stage**: Discover, Evaluate, Act, Onboard, Use, Get help, or Verify. Name the previous page and the next page(s) by URL.
- **Users** (sitemap codes) and their top three anxieties or objections, in their words.
- **Success**: the primary action (one), the secondary action (at most one), and the measurement event (account_start, otp_verified, app_install_click, partner_lead, wealth_lead, notify_signup, ticket_raised, calculator_used, document_download).

## Step 2. The questions the page must answer (the product manager's list)
List 6 to 10 questions in the order the visitor would ask them. Tag each MUST or SHOULD. For every question say which section answers it.
Always consider: What is this and is it for me? What does it cost? Who exactly am I dealing with (which Aikyam company, which licence)? Is it safe and regulated? How long does it take and what do I need? What happens next? What if something goes wrong? On product pages add: how is it different here, what are the risks?
Also list **what the page must not say** (licence boundaries, claims ROOT cannot prove yet).
Traceability rule: every MUST question is answered by a section; every section answers at least one question. Sections that answer nothing are cut.

## Step 3. Section plan
An ordered list of sections. For each: purpose (question ids), content outline (real headings and key copy points, not lorem), and the component it needs. Respect the template skeleton in `sitemap.json` "templates", deviating only with a stated reason.

## Step 4. Layout exploration (2 to 3 options per section, then choose one)
- **Option A is always the baseline**: the theme or pattern-library layout for that kind of section.
- **Options B and C must differ in structure** (information hierarchy, layout, density or interaction), not in colour or decoration.
- Describe each option in at most three lines as a wireframe spec: columns, order, what is biggest, component used.
- Score each option 1 to 5 on the rubric below; pick the winner; record one line on why the winner won and why each loser lost.
- Derivative pages: inherit the golden page's section layouts by default ("inherit 09 §3"). Explore options only for sections that are new to this page or where the inherited layout fails this page's questions.

### Rubric (weight)
| Criterion | Weight |
|---|---|
| Answers its questions, in the order asked | 3 |
| Moves the visitor to the next step (one clear primary action) | 3 |
| Trust and compliance (claims rule, entity named, disclosures) | 3, and any failure is a veto |
| Scannable hierarchy (a 5-second test: what is this, why here, what do I do) | 2 |
| Theme fidelity and consistency with the pattern library | 2 |
| Mobile at 390 px (stacks cleanly, CTA reachable) | 1 |
| Figma editability (plain flex or grid, no tricks) | 1 |
| Build cost (reuse beats novelty unless novelty wins on the top three) | 1 |
Vetoes: an invented number or claim; a missing mandatory disclosure; content only visible through JavaScript; a layout that hides the primary action on mobile.

## Step 5. Build the page
Follow `rules/figma-html.md`. Write `pages/src/NN-id.html`, then run from `root-website/`:
`python3 scripts/build.py NN && python3 scripts/lint.py NN && python3 scripts/shoot.py NN`
Fix every lint error and every overflow. Look at the desktop and mobile slices in `review/NN-id/` (at least the first two of each) and fix what looks wrong.

## Step 6. Save the page memory
Write `memory/pages/NN-id.md` from `memory/pages/_TEMPLATE.md`. It is the page's permanent context: the next designer, the next agent and the client review all start from it. Keep it factual and short; no copy of the HTML.
