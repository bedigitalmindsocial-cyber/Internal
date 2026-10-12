# HTML rules: clean code that imports into Figma (v2)

Every page is one self-contained file in `figma/`, imported into Figma with html.to.design (plugin by URL, or the Chrome extension on the open file) at 1440 and 390 wide, then refined by a UI/UX designer. Write for that designer: every layer they get should be meaningful, editable and named. The designer imports `figma/00-kit.html` first and turns it into components.

## What you write
Only `pages/src/NN-id.html`. The build adds the doctype, head, fonts, theme CSS, header, footer, breadcrumb and mobile bar.
```html
<!--page {"title": "Open a trading and demat account | ROOT by Aikyam",
          "description": "70 to 160 characters, plain, no claims ROOT cannot prove.",
          "query": "open demat account online",
          "lint_allow": [], "mbar": {"label": "Get OTP", "href": "#s-open"}} -->
<style data-page>/* only if no theme class or pattern fits; tokens only; short */</style>
<section class="hero" id="s-hero" aria-labelledby="h-hero"> ... </section>
<template data-state="otp-sent" data-label="OTP sent, 30 s resend timer"> ...markup of the changed component... </template>
```
Front matter keys: `title`, `description`, `query` (main search query), optional `breadcrumb` (default: built from the sitemap), `header`/`footer` ("full" or "min"; template D defaults to min), `spine` (default true), `mbar` (default follows the page's primary action; `false` to hide), `lint_allow` (words the lint should only flag for review, e.g. "sub-broker" on a page explaining the change).

## Structure
- One `h1` (class `d1`). Each section has an `h2` (class `d2 node`, which sits on the gold spine) unless it is the hero. No skipped levels.
- Every `<section>` has `id="s-<name>"` named for what it is (`s-charges`, `s-documents`, `s-eligibility`); ids become anchors and, if the importer uses them, layer names.
- Mark the page's primary action (the button or form submit) with `data-primary`. Exactly one per page in the main flow.
- Use theme layout classes: `wrap`, `band`, `band--mist`, `band--dark` (at most one per page), `band--tight`, `head`, `split`, `stack`, `cards`, `hero-grid`, `price-grid`, `steps` (set `style="--cols:3"` when not 4), `goals`, `pillars`, `feature`, `faq`, `app`, `final`, `risk-box`, `creds-wall`, `posts`, `fund-grid`, `idx-grid`, `ipo-list`, `tablewrap` + `table.data`.
- Reuse markup from `theme/components.html` when it exists (golden pages add to it), then `theme/sections-reference.html`.

## Values and placeholders
- Site-wide values are tokens: `{{cta.primary}}`, `{{reg.capital.sebi}}`, `{{reg.wealth.arn}}`, `{{contact.grievance_email}}`, `{{pms.minimum}}`... (list in the brief). Never type a registration number, CTA label or company contact literally: one edit in `memory/values.json` must update all 75 pages. A token whose value is not known yet renders as a placeholder chip automatically.
- Anything else not confirmed (a price, a payout, a date, a count, a claim in `rules/claims.json` "unconfirmed"): `<mark class="ph" data-ph="short-key">what is missing</mark>`; blocks and images: `<div class="ph ph--block" style="--ar:4/3">Photo: what it shows, ratio</div>`.
- Market or fund data is illustrative, uses fictional names (Example Industries Ltd, Sample Flexi Cap Fund), shows an as-on date and a source line, and is labelled `<p class="illus">Illustrative data. Not real prices or returns.</p>`. Missing values are a dash, never 0%.
- Legal pages: structure (contents list, numbered clause headings, what each covers) with the client's text in `ph ph--block` placeholders. Never draft legal or regulatory text. SEBI-prescribed texts in `rules/compliance-blocks.md` are used verbatim.

## Interaction states (the static page shows the default state)
Put every other state in `<template data-state="key" data-label="what it shows">` blocks: the build renders them on `figma/NN-id.states.html`, one labelled frame each, for the designer. Template D needs at least: OTP sent (with resend timer), wrong OTP or invalid number (error), verified / next step. Any form needs an error and a success state. Tabs: the first panel on the page, each other panel as a state. Use theme classes for states: `.fgroup.is-error`, `.alert--err`, `.alert--ok`, `.btn.is-loading`, `.otp`, `.skel`.

## Figma-safe rules
- **No JavaScript**, no `onsubmit`, no `<script>`, no `hidden` content the design needs (use a state block instead).
- Layout with theme flex/grid classes; no absolute positioning for content, no transforms for layout, no negative-margin tricks. The build's static mode turns one-direction stacks into flex and draws outlines as borders.
- **Icons**: `<svg class="i"><use href="#i-NAME"/></svg>` only (the build expands them with explicit strokes). Names: stocks, fo, commodity, etf, ipo, mf, shield, bond, nps, pms, bolt, research, support, lock, sun, cap, home, sprout, search, user, chev, arrow, ne, check, info, alert, phone, qr, menu, close, plus, cal, bell, doc, calc, book, chart, swap, handshake, store, rupee.
- **No images.** Theme illustrations (phone mockup on Home and Get the App only; rings; gradient article thumbs; group root diagram) or labelled placeholders.
- Rings and gauges (riskometer, goal progress): inline SVG with paths and an HTML label, not `conic-gradient` or `attr()`.
- Tables with more than 3 columns: `<table class="data data--stack">` with `<span class="td-label">Column name</span>` at the start of each cell, so they stack on phones instead of being cut off.
- Inline `style` only for CSS custom properties. New CSS in `<style data-page>`, tokens only (never hex), short; reusable pieces are named in memory section 7 for promotion.
- Charts: SVG with paths only, axis labels and values as HTML text next to it.

## Check before you finish
`python3 scripts/gate.py NN` (Bash timeout 300000) must print `"ok": true`. Then look at the slices.

## Importer results (fill in after importing figma/00-import-test.html)
| Test | Result | What we changed |
|---|---|---|
| 1 Layer names (id / class / data-name / aria-label) | pending | |
| 2 Grid column vs flex column | pending | |
| 3 Card grid vs flex-wrap | pending | |
| 4 ::before dot vs real element | pending | |
| 5 Inset shadow vs border | pending | |
| 6 Conic ring vs SVG ring, gradient band | pending | |
| 7 Icon strokes | pending | |
| 8 Fonts and clamp() sizes | pending | |
| 9 details/summary, hidden | pending | |
| 10 Fixed bar | pending | |
