# Component markup library

Canonical markup in `theme/components.html` (find a block by its `<!-- COMPONENT: name -->` comment; nested comments mark parts that also work alone); CSS in `theme/patterns.css`. Copy the block, keep class names, replace the copy. Verbatim compliance blocks stay in `rules/compliance-blocks.md`: blocks that need one hold a comment naming it. v3 blocks curated 12-Oct-2026 from 01 Home v3 and 09 Start Trading v3. Start new pages from the v3 blocks; the legacy blocks stay only until 10 Start Investing is rebuilt on v3.

## v3 (canonical)
- **Hero · product stage + inline bar form (v3 hub hero)**: `.hero-grid.hero-grid--stage` (two equal columns from 900 px) > `.hero-copy` (seed, eyebrow naming both companies, h1, lead, `form.hero-form`, `.hero-alt` door, `ul.creds.creds--row`) + `.hero-visual` (`.hero-stage`: rings, theme `.phone` 280 px, `.stage-cards` of two `.ui-card`; `p.illus`). Use for 01, 02, 03, 04, 11. Source 01 s-hero.
- **Hero inline bar form**: `form.hero-form` > `.leadbar` (`label.field` + `.pre`, submit `data-primary`) + `label.check` (consent, `data-draft`) + `.hero-fine` (receiver and hand-off `p.fine`). Two error states: `.fgroup.is-error` around the bar (invalid number) or around the consent box. Use for hub heroes that start an account, 75. Source 01.
- **Proof row**: `ul.creds.creds--row`, three proof points across from 900 px under a hairline, icon top-aligned. Use for hub heroes. Source 01.
- **Product stage**: `.hero-visual` > `.hero-stage` (phone + `.stage-cards`; card parts `.ui-head` > `.ui-tile` + `.ui-label`, `b.ui-name`, label-value `.ui-row`, `span.chip.ui-cta`); cards go side by side under the phone at 640. Use with the hub hero. Source 01.
- **Hero · onboarding stage (template D v3)**: `.hero-grid` > `.hero-copy` (eyebrow with the company, h1, lead, `ul.creds` with `li.cred-wide`, `a.link` to charges) + `.hero-side` (`.ui-stage.ui-stage--panel.open-stage` > rings + `ol.track` + `section.form-card#s-open`; `.hero-alt` wrapping link). Columns centred. Use for 09, 10, 11, 75. Source 09 s-hero.
- **Onboarding stage + step tracker**: `.ui-stage--panel.open-stage` (Mist panel, rings bottom right behind) + `ol.track` (four `li`; `.is-on` gold with `aria-current="step"`, `.is-done` ink with a check). Use beside any account-start form. Source 09.
- **Form card v3 states**: OTP sent, invalid number, consent missing, wrong OTP, verified (stage with the tracker advanced), existing account; each a `<template data-state>` of `.form-card` with `p.fine` lines. Use for every template D form (3+ states). Source 09.
- **Entity doors v3 · products by company**: `.doors` > `article.door` (Trade: `.door-head` label naming the company, `ul.door-rows`, inset risk box, more rows, `.door-foot`) + `.doors-side` (Invest door + coming-soon card). Use for 01, 02, 03, 06, 07. Source 01 s-products.
- **Inset risk box in a door**: `.door .risk-box.risk-box--inset` (`#s-risk` on fo_risk pages), icon and bullets in ink, `h4.h4`, verbatim fo_risk text, source line. Use in the Trade door. Source 01.
- **Goal chips**: `ul.goal-chips` (2 x 2 Mist tiles, icon above label, not links) inside `.row-text.row-text--wide`. Use for 02, 04 until goal pages go live. Source 01.
- **Coming-soon card**: `.doors-side` > `.soon-card` (`span.label`, `ul.soon-list` > `li.soon-item` with a small icon), outside the doors so no company is implied. Use for 02, 03, 51. Source 01.
- **Stat tiles · three across (cost summary)**: `.stat-tiles.stat-tiles--3` > `.stat-tile` (`.tile`, `.label` naming the company, `.num` slot with a token or `.num--word`, `p`, optional `a.link`) + `.price-notes` + band button. Use for 02, 03, 07, 06 header. Source 01 s-pricing.
- **Group section v3 · who is behind ROOT**: Mist band, `.split` (copy + `ul.facts` + link | `figure.gmap`) then `.verify` with verify cards. Use for 01, 07, 12, 13. Source 01 s-group.
- **Facts list**: `ul.facts` (icon + one checkable line), the claim-free replacement for the theme pillars. Use for 01, 07, Help Centre. Source 01.
- **Group map**: `figure.gmap` (`.gmap-root`, `svg.gmap-lines` non-scaling strokes, `ul.gmap-branches` > `li.is-on` > `.gmap-dot` + `.gmap-card`); white cards on Mist, hairline shells for group lines, 2 x 2 at 640. Use for 01, 07, 12, 13. Source 01.
- **Verify cards**: `.verify` > `.verify-head` + `dl.verify-list.verify-list--cards` > `.verify-row` (dt: `.tile`, `b` role, company link; `dd.mono` code; `dd` regulator link at the foot). Use for 07, 12, 13, 15, 16. Source 01.
- **Steps split · KYC step card**: `.split.split--steps` (7/5) > steps side (`ol.steps --cols:2`, `.docs` with a two-column list, `.band-cta` + `p.fine`) + `.ui-stage.kyc-stage` > `.ui-card.kyc-card` (`.kyc-progress`, `.ui-big`, `.ui-field`, `.ui-row.ui-ok`, `.ui-cta`) + `p.ui-caption`. Use for 01, 10, 75, 21. Source 01 s-steps.
- **Process steps · mini screens + documents strip + two info cards**: Mist band, `ol.steps` with `.ui-card.ui-mini` in each `li`, `p.ui-caption`, `.docs.docs--tiles`, `.cards.cards--2` of `.info-card`, `p.small.steps-note`, `.band-cta` link. Use for 09, 10, 75. Source 09 s-steps.
- **Step mini screen**: `.ui-card.ui-mini` at the foot of a step (`.ui-row`: `.ui-label` + status chip; `b.num` masked value). Use for any illustrated process. Source 09.
- **Documents strip with icon tiles**: `.docs.docs--tiles` (h3 + `ul` of `li` > `.tile` + label; 2 x 2 from 641 px). Use for 10, 75. Source 09.
- **Two-card row**: `.cards.cards--2` (two columns from 641 px, 16 px top margin). Use for any pair of cards. Source 09.
- **F&O section · inset risk box + facts + segments card**: `.risk-box.risk-box--inset#s-risk` (verbatim), `.risk-more` link, `.split.fo-split` (lead + `ul.facts` with `.fact-text` | `.ui-stage--panel.seg-stage` > `.ui-card.ui-list.seg-card`). Use for 09, 37, 38, 75. Source 09 s-fo.
- **Facts with a title**: `ul.facts` > `li` > `.tile` + `.fact-text` (`b`, `p`, optional `.links`). Use for 37, 38, 75. Source 09.
- **Segments card**: `.ui-card.ui-list.seg-card` (rows with `chip--gain` or plain chips) centred on a stage panel, caption centred. Use for 37, 38, 75. Source 09.
- **Charges · stat tiles + brokerage row list + contract-note receipt**: Mist band, `.stat-tiles` (tokens in `.num`), `.cards.cards--2` > `.info-card` (h3, `dl.kv-list.kv-list--row`, `p.fine`, link) + `.ui-card.ui-receipt`. Use for 09, 06 header, 75. Source 09 s-charges.
- **Row list**: `dl.kv-list.kv-list--row` (no frame; hairlines; dt left, dd right). Use for 06, 13, 30. Source 09.
- **Receipt card**: `.ui-card.ui-receipt` (contract-note rows: charge and who sets it, closing note, no amounts). Use for 06, 75. Source 09.
- **FAQ split on a Mist band v3**: `.band--mist` > `.split` (`.stack.faq-side`: h2, lead with contact link, `figure.img-slot`, Help Centre and guide links, grievance `p.fine`) + `.faq` native `details`. Use for every product and onboarding page (09 uses it on a white band). Source 01 s-faq.
- **Dark closing band · buttons row + app coming soon + image slot**: `.band--dark` > `.app` (stack: eyebrow, h2, `.final-actions`, `p.fine`, `.app-soon` with disabled `.stores`, link) + `figure.img-slot.final-visual`. Use for 01, hubs. Source 01 s-final.
- **Dark closing band · button column + product cards**: `.band--dark` > `.app` (stack: eyebrow, h2, lead, `.row` column of equal-width buttons, `p.fine`) + `.ui-stage.final-stage` (rings--dark, two `.ui-card.ui-list`, caption). Use for 09, 10, 75. Source 09 s-final.
- **Hairline row card**: `.ui-card.ui-list` (`.ui-label`, `.ui-big`, rows split by 1 px lines, `.ui-pill` action). Use for any illustrative list card. Source 09.
- **Disclosure band · mutual funds and distribution**: `.band--mist.band--tight` > `.risk-box` with the info icon (ink), verbatim MF risk line and distributor disclaimer. Use for Aikyam Wealth and mixed pages. Source 01 s-disclosures.
- **Wrapping link**: `a.link.link--wrap` with the last word and icon in `span.link-tail`. Use for any long link label. Source 09.
- **Closing CTA · light, two buttons**: `.final` > h2 naming the company + `.row` (primary, other company ghost; full width at 640) + `p.handoff`. Use when the page's one dark band is used elsewhere (10 today). Source 09 v2 s-final.
- **Utility `.mono`**: Red Hat Mono 500 for registration codes outside `creds-wall` and `foot-reg` (no block; see the verify cards and creds). Source 01.

## Legacy (v1 and v2 pilot; only until 10 is rebuilt on v3)
- **LEGACY v2 · Hero · form card (template D)**: form card with a step label, cost cred `li.cred-cost`. On 10 today; new pages use the onboarding stage hero. Source 09 v2.
- **LEGACY v2 · Form card · cost line + side door**: `.form-card .cost-line` + `.side-door`. Only for a form card that must answer cost where you act (75). Source 01 v2.
- **LEGACY v2 · Process steps + docs strips**: stacked `.docs` strips with a shared label column. On 10 today. Source 09 v2.
- **LEGACY v2 · Charges block · placeholder numeral**: `.price-grid` > `.zero.zero--top` + two-column `table.data--stack`. For a 06 Pricing rate card if needed. Source 09 v2.
- **LEGACY v2 · Info card split**: lead left, `.info-card` blocks right; replaced on 09 by the F&O section (`.info-card` itself stays current). Source 09 v2.
- **LEGACY v1 · Two ledgers**: `.ledgers` > `.ledger` (two-column `table.data--stack`, `dl.kv-list` card). 10 uses `.ledger` + `kv-list`. Source 01 v1.
- **Check it yourself · rows (compact variant)**: `.verify` > `dl.verify-list` > `.verify-row` (3 columns, stacked at 640) where cards are too heavy (15, 16). Source 01 v1.
- Removed on 12-Oct-2026: the v1 Entity doors (its shortened F&O strip is not the verbatim box) and the v2 form card states (replaced by the v3 states).
