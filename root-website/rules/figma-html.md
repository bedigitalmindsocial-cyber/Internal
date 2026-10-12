# HTML rules: clean code that imports into Figma

The output of every page is one self-contained HTML file in `figma/`, imported into Figma (html.to.design plugin or its Chrome extension, at 1440 and 390 wide) and then refined by a UI/UX designer. Write for that designer: every layer they get should be meaningful, editable and named.

## What you write
Only `pages/src/NN-id.html`. The build adds the doctype, head, fonts, theme CSS, header, footer and mobile bar.
```html
<!--page {"title": "Start Trading | Open a demat and trading account | ROOT by Aikyam",
          "description": "155 characters max, plain, no claims ROOT cannot prove.",
          "breadcrumb": [["Home", "/"], ["Open account", "/open-account/trading"]],
          "header": "full|min", "footer": "full|min", "spine": true} -->
<style data-page>
/* only if no theme class or pattern fits; tokens only; keep it short */
</style>
<section class="hero" id="s-hero" aria-labelledby="h-hero"> ... </section>
<section class="band band--mist" id="s-steps" aria-labelledby="h-steps"> ... </section>
```
- Header defaults to "min" for pages flagged `minimal_header` (template D), otherwise "full". Footer follows the header.
- Breadcrumb: give it for every page except Home and template D.

## Structure
- One `h1` per page (class `d1`). Each section has an `h2` (class `d2 node`, which sits on the gold spine) unless the section is the hero. No skipped levels.
- Each `<section>` gets an `id="s-<name>"` and `aria-labelledby`. Section ids become layer names in Figma, so name them for what they are (`s-charges`, `s-documents`), not `s-section3`.
- Use the theme's layout classes: `wrap`, `band`, `band--mist`, `band--dark` (at most one per page), `band--tight`, `head`, `split`, `stack`, `cards`, `hero-grid`, `price-grid`, `steps`, `goals`, `pillars`, `feature`, `faq`, `app`, `final`, `risk-box`, `creds-wall`, `posts`, `fund-grid`, `idx-grid`, `ipo-list`, `tablewrap` + `table.data`.
- Class names are semantic and lowercase-hyphenated. No utility soup.

## Figma-safe rules
- **No JavaScript**, no `onsubmit`, no `<script>`. Everything the design needs is in the DOM in its final state. Tabs: render the first panel; show the other tab labels only.
- Layout with plain flex or grid from the theme. No absolute positioning for content (decoration only), no transforms for layout, no negative-margin tricks.
- **Icons**: `<svg class="i"><use href="#i-NAME"/></svg>`; the build expands them to inline vectors. Available: stocks, fo, commodity, etf, ipo, mf, shield, bond, nps, pms, bolt, research, support, lock, sun, cap, home, sprout, search, user, chev, arrow, ne, check, info, alert, phone, qr, menu, close, plus, cal, bell, doc, calc, book, chart, swap, handshake, store, rupee. Do not invent icon names; if none fits, use the closest and note it in memory.
- **No images**. Use the theme's built illustrations (phone mockup, rings, gradient article thumbs, group root diagram) or a labelled placeholder: `<div class="ph ph--block" style="--ar:4/3">Photo: plant team at the Mumbai office, 4:3</div>`.
- Inline `style` only for CSS custom properties (`style="--w:62%"`, `style="--n:2"`).
- New CSS goes in `<style data-page>`, uses tokens only (`var(--aub)`, never hex), and stays short. If you create something reusable, name it as a pattern and flag it in the page memory under "new patterns".

## Content rules
- Real copy, written for this page, in the ROOT voice (`rules/voice-and-claims.md`). No lorem ipsum.
- Any regulated number, price, fee, date, count or claim not confirmed in `context/` is a placeholder: `<mark class="ph" data-ph="key">what is missing</mark>`. Never invent one.
- Market or fund data is illustrative and labelled: `<p class="illus">Illustrative data. Not real prices.</p>`. Use obviously fictional names (Example Industries Ltd, Sample Flexi Cap Fund).
- Legal pages: write the structure (contents list, numbered clause headings, what each clause covers) and put the client's text in `ph ph--block` placeholders. Never draft legal or regulatory text that the client must supply. SEBI-prescribed texts in `rules/compliance-blocks.md` are used verbatim.
- Links: internal links use sitemap URLs (`/pricing`, `/open-account/trading`); in-page anchors `#s-name`; external links only to regulators and exchanges (scores.sebi.gov.in, smartodr.in, nseindia.com, bseindia.com, mcxindia.com, amfiindia.com).
- Forms: visible labels, correct input types, helper text naming the company that receives the data, and the consent line. No dark patterns, no pre-ticked consent.

## Check before you finish
`python3 scripts/build.py NN && python3 scripts/lint.py NN && python3 scripts/shoot.py NN` from `root-website/`. Lint errors and overflow must be zero. Open the screenshot slices and look.
