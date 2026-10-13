# Component markup library

Canonical markup in `theme/components.html` (find a block by its `<!-- COMPONENT: name -->` comment; nested comments mark parts that also work alone); CSS in `theme/patterns.css`. Copy the block, keep class names, replace the copy. Verbatim compliance blocks stay in `rules/compliance-blocks.md`: blocks that need one hold a comment naming it. v3 blocks curated 12-Oct-2026 from 01 Home v3 and 09 Start Trading v3; Wave 1 blocks curated 12-Oct-2026 from the golden pages 03, 07, 17, 29, 42, 57, 62 and 65 (one kit per template). Start new pages from the v3 and Wave 1 blocks; no page uses the legacy blocks since 10 Start Investing was rebuilt on v3.

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

## Wave 1 goldens (canonical per template; CSS in the "Wave 1 golden promotions" part of patterns.css)
Template rules in patterns.css apply by body class (`.tpl-a` and so on, set by the build): hero top under the breadcrumb (A, H, P 40 px; E, F 40/80), full-width wrapping buttons in main at 640 (HOME, A, E, F, H), risk box icon above the text at 640 (all but D and P). Derivatives get them without page CSS.

**A · hubs (03 Trade)**
- **Hero · ticket stage (template A hub hero)**: the v3 hub hero with `.hero-stage` > `.ui-card.ui-list.ticket` (300 px, `.ticket-toggle` with `span.on`, rows, 38 px `.ui-pill`) + `.stage-cards`. Use for 31, 35 to 38; 06 with the receipt as the ticket. Source 03 s-hero.
- **Rows plus explainer split**: `.split.split--rows` (7/5, centred) > `article.door` rows + `.ui-stage.explain-stage` (two staggered `.ui-card.ui-list.explain-card`, caption). Use for the product block of every A page. Source 03 s-products.
- **Card head in a hairline row card**: `.ui-list .ui-head` (tile + label, no label padding) with a status `.chip` pushed right. Use for any `.ui-list` card with an icon and a status. Source 03.
- **Info card with a foot button + receipt**: `.cards--2` > `.info-card` (tile, h3, `.price-notes`, ghost `.btn` pinned to the foot) + `.ui-receipt`. Use for hub cost cards beside a taller card. Source 03 s-charges.

**F · company pages (07 About)**
- **Hero · group stage (template F)**: `.hero-copy` (`.hero-act` > `.hero-actions` + `p.fine`; `ul.creds.creds--row` with `span.cred-sub` + inline `.mono`) + `.hero-visual` > `.ui-stage--panel.group-stage` (rings, `figure.gmap`, `figcaption.gmap-caption`). Use for 12, 13; 14, 15, 71, 73 keep the copy column. Source 07 s-hero.
- **Hero actions + hero act**: `.hero-act` > `.hero-actions` (button + on-page link; full-width button, link under it at 640) + `p.fine` 12 px under. Use for any hero whose action is not a form (07, 17, 65). Source 07, 17.
- **Proof row with company sub-lines**: `ul.creds.creds--row` > `li` with `span.cred-sub` ("Company · " + `span.mono` token, inline). Use for 01, 03, 09, 12 proof rows. Source 07.
- **Entity doors · about variant**: `.doors` > `article.door` with `ul.door-rows.door-rows--about` (label over a 1rem answer, 40 px Mist tiles, `p.fine.row-soon`), foot with button and hand-off, `p.fine` under the doors. Use for 12, 13, 06 intro. Source 07 s-companies.
- **Company registers**: `ol.check-strip` + `.ledgers` > `.ledger.register` (2/3 row grid, `dd.mono`, "Check on" link) + `.ledger-side` (`.doc-block` > `ul.doc-list`) + `.info-card.safe-card`. Use for 12, 13, 15, 16. Source 07 s-verify.
- **People cards · compact**: `ul.people` > `li.person` (`figure.img-slot.img-slot--face` with `span.initials`; a portrait replaces them, no markup change) + `p.small.people-note` + `.people-links`. Use for 12, 13; 14 until the shoot. Source 07 s-people.
- **Contact strip**: `.contact-strip` > `.contact-col` (tile, h3, `a.value`, lines, `.links`), hairline above, no frame. Use for 15, 73. Source 07 s-contact.

**G · legal and help (17 Grievance)**
- **Hero · route card (template G)**: d2 h1, `.hero-actions`, applies-to `p.fine`; `.hero-side` > `.ui-stage--panel.route-stage` > `nav.ui-card.route-card` (`p.route-group`, `ol.route-steps` rows with `.route-rail` > `.route-dot` + `i.route-line`, `.route-alts`, `.route-foot`). Columns centred. Use for 16, 18 to 25. Source 17 s-hero.
- **Clause split · desk card**: `section.clause` > `.split.clause-split` (7/5): "Step N" eyebrow, `h3.d3.node`, copy, `.desk-action`; `.info-card.desk-card` (`ul.desk-rows`, `.desk-next` with a `.kv-list--cols` row list). Use for 21, 23, 15, 18, 08. Source 17 s-write.
- **Escalation ladder v2**: `.ui-stage--panel.ladder-stage` > `ol.ladder` > `li.ladder-start` (Mist bracket, quiet rungs) + `li.ladder-group` (gold rail, ink chips), each a `span.label` and an `ol` of `.rung`. Use for 18 Escalation Matrix. Source 17 s-escalate.
- **Portal cards · a step whose answer is a choice**: `.stack.clause-head` + `.cards--2` of `article.info-card.portal-card` (`.portal-top`, `.portal-name`, row lists, `.links` at the foot) + `p.fine.clause-fine`. Use for 16, 22. Source 17 s-scores-odr.
- **Row list, two columns**: `dl.kv-list.kv-list--row.kv-list--cols` with `--dt` (dt fixed column, dd left beside it; stacked at 640). Use for 13, 16, 20, 30. Source 17 (inside the desk card).
- **Checklist**: `ul.checklist` (gain-green check icons, ink text). Use for 21, 23. Source 17.
- **Document frame**: `.doc-grid` (4/8 from 1100 px) > `aside.doc-rail[data-sticky]` (`ol.toc`, `.doc-file`) + `ol.clauses` (numbered articles, compact client `ph--block`). Use for 16, 19, 21 to 25, 30. Source 17 s-policy.
- **FAQ answer links**: `p.faq-links` inside an answer: external links with `i-ne` in a wrapping row. Source 17 s-faq.
- **Product cards four across**: `.cards.cards--4` of theme `article.pcard`. Use for 16's index, any related row of four. Source 17 s-related.
- **Closing CTA · light, two buttons + fine-print pair**: `.final` > h2 + `.row` + `div.final-fine` (two `p.fine`, 6 px apart; no CSS). Use for any light closing CTA with a draft line plus a contact line. Source 17 s-final.
- **Mail card (state)**: `.ui-card.mail-card` (To, Subject, `.mail-body`) + caption on the states board. Use for 18, 23. Source 17 states.

**B · data pages (29 Scheme detail)**
- **Hero · data hero (template B)**: `.hero-grid.hero-grid--data` (copy, `.hero-side` invest card, `.hero-chart`): `h1.d1.d1--name`, `.chip-row` with `.chip-risk`, `.nav-row`; `section.form-card.invest-card`; `figure.data-card.chart-card` (`.chart-top`, `.chart-plot` with `.chart-y`, `.chart-x`). Use for 34, 39, 27, 32, 33, 40. Source 29 s-hero.
- **Paired bars + reading card**: `.tabs.band-tabs`, `.split--data.split--returns` > `figure.data-card.pairbars` (`.pb-legend` with `.sw` keys, `.pb-rows`, `.data-foot`) + `.info-card.read-card`. Use for 34, 27. Source 29 s-returns.
- **Riskometer dials**: `.split--half` > `.ui-stage--panel.dial-stage` > `.dials` (two `figure.dial`) + `.data-foot`, beside an info card (bare `ul`, `h4.h4`). Source 29 s-riskometer.
- **Costs · stat tiles + timing receipt (template B)**: `.stat-tiles--3`, `.data-foot.price-notes`, `.cards--2` (row list card + `.ui-card.ui-receipt.ui-receipt--stack` "When each cost applies", no amounts). Use for 34, 27. Source 29 s-costs.
- **Composition card + facts card**: `.split--data.split--stretch` > `.data-card` (`figure.mix`, `.barcols` of `ol.barrows`, factsheet `a.link.link--wrap`, `.data-foot`) + `.info-card.facts-card`. Use for 34 financials, 39 shareholding. Source 29 s-portfolio.
- **Data foot** (and the data card): `.data-card` (white, shadow-1, no border) and `.data-foot` (`p.src`, `p.fine`, `p.illus`, 4 px apart). Every block with numbers. Source 29 s-returns.

**C · calculators (42 SIP calculator)**
- **Hero · calculator (template C)**: `section.hero.hero--calc` > `.hero-grid--calc`: `fieldset.calc-in` (`.calc-row` with `.calc-field`, `input.range`, `.calc-note`) + `section.ui-stage--panel.calc-stage#s-result` (`.calc-card` with `dl.calc-split` and the primary; `figure.calc-chart`; `details.calc-years`; `.calc-links`). Use for 43 to 50. Source 42 s-hero.
- **Smooth versus real**: `.split.split--75` > `ul.facts.facts--chips` (`.fact-head`) + `a.facts-link`; `.ui-stage--panel.assume-stage` > `figure.assume-art` (SVG, `figcaption.assume-key`) + caption. Use for 43, 44, 49, 50. Source 42 s-assume.
- **Formula card + worked-example receipt**: `.cards--2` > `.info-card` (`p.formula`, `dl.kv-list--row.formula-keys`) + `.ui-card.ui-receipt.calc-receipt` (`.is-total`). Use for 43 to 50; 45 the receipt. Source 42 s-formula.
- **FAQ side links**: `.stack.faq-side` with `h3.label` + `.faq-links` (10 px stack). Use for 42 to 50, 64 to 70. Source 42 s-faq.
- **Legend keys** (inside Paired bars, the Composition card and the Result card): `.sw` (12 px square, ink tints `--bm`, `--2` to `--4`) and `--line`, `--dash`, `--soft`, `--bar` on an `i` or `span` (never a control look; the kit's colour swatches are `div.sw`). Source 29, 42.

**H · products (57 PMS)**
- **Hero · set-up stage (template H)**: `.label-row` (eyebrow + `span.soon`), lead with `.nb`, `div.notify#s-notify` > `form.hero-form` (notify bar), `.hero-alt`, proof row; `.hero-stage` > `.ui-card.ui-list.setup-card` (stacked rows) + `.stage-cards` of `.outcome-card`. Use for 51 to 60. Source 57 s-hero.
- **Stacked rows**: `.ui-list--stack` (new cards), `.setup-card`, `.agree-card`: each row a small grey label over a bold value. Source 57, 62.
- **Who does what card**: `.split.split--roles` > `.stack` (h2, lead, `a.link.link--wrap`) + `.info-card.roles-card` (row list, fine). Use for 58, 59. Source 57 s-roles.
- **Product card with a label**: `.cards--2` of `.info-card.today-card` (tile, label naming the company, h3, copy, `.card-foot`). Use for "related live products" on every H page. Source 57 s-today.

**P · partner programmes (62 Distributor partner)**
- **Path cards**: `.cards.cards--2.path-cards` > `.info-card.path-card` (tile, h3, `ul.facts` or `ol.facts` with 36 px tiles, short line, link or `.links` at the foot). Use for 61, 63. Source 62 s-eligibility.
- **Payout split + money path**: `.split.split--pay` (row lists) + `.ui-stage--panel.money-stage` > `ol.money-path` (`.ui-mini` nodes, `i.path-line`, ink last tile) + balanced caption. Use for 63. Source 62 s-payouts.
- **Agreement split · agreement card + Always and Never lists**: `.split.split--agree` > `.ui-card.ui-list.agree-card` on a stage panel + `.stack.agree-side` (`.cards--2` of `ul.rule-list` cards, client `ph--block`, regulator link). Use for 63. Source 62 s-agreement.

**E · guides (65 Guide: getting started)**
- **Hero · guide route card (template E)**: `.hero-act` (one button + `p.fine`), `.hero-alt`; `.ui-stage--panel.route-stage` > `nav.ui-card.route-card` (`.route-head`, `ol.route` > `li` > `a` > `.route-mark` (`span.dot` + `i.route-line`) + `.route-text`, `.route-foot`). Use for 64, 66 to 70, 72. Source 65 s-hero.
- **Route card · reading state**: `li.is-done` (gold dot with a check), `li.is-on` (`aria-current="location"`). Source 65 states.
- **Chapter band · chapter head + guide product cards + row callout**: `div.head.chapter-head` ("Part N of M", question h2, 66ch lead), `.cards--2.guide-cards` of `article.pcard` (`dl.start-with` at the foot), `aside.callout.callout--row`. Use for 66, 69. Source 65 s-basics.
- **Chapter band · prose + doors with a term callout**: `.chapter-head` with `.prose`; Entity doors v3 with `aside.callout.callout--term` in a door; `p.small` under the doors. Source 65 s-account.
- **Costs card + receipt (template E)**: `.split--wide.split--top` > `.info-card.cost-card` (two company labels, two row lists, stacked rows at 640) + 09's receipt. Use for 64, 66, 67, 69. Source 65 s-costs.
- **Open chapter · steps + wide documents strip + band CTA**: steps with mini screens on white, `.docs.docs--tiles.docs--wide`, `.band-cta.open-cta`, `p.small.open-alt`. Source 65 s-open.
- **Light product stage + callout with an ask list**: `.split--wide.first-split` > facts + `.ui-stage.first-stage` (two staggered cards); `aside.callout.choose-callout` > `.ask` > `ul.ask-list`. Use for 66, 69. Source 65 s-first.

## Legacy (v1 and v2 pilot; no page uses them since 10 was rebuilt on v3; kept for 06 and 75 until they decide)
- **LEGACY v2 · Hero · form card (template D)**: form card with a step label, cost cred `li.cred-cost`. On 10 today; new pages use the onboarding stage hero. Source 09 v2.
- **LEGACY v2 · Form card · cost line + side door**: `.form-card .cost-line` + `.side-door`. Only for a form card that must answer cost where you act (75). Source 01 v2.
- **LEGACY v2 · Process steps + docs strips**: stacked `.docs` strips with a shared label column. On 10 today. Source 09 v2.
- **LEGACY v2 · Charges block · placeholder numeral**: `.price-grid` > `.zero.zero--top` + two-column `table.data--stack`. For a 06 Pricing rate card if needed. Source 09 v2.
- **LEGACY v2 · Info card split**: lead left, `.info-card` blocks right; replaced on 09 by the F&O section (`.info-card` itself stays current). Source 09 v2.
- **LEGACY v1 · Two ledgers**: `.ledgers` > `.ledger` (two-column `table.data--stack`, `dl.kv-list` card). 10 uses `.ledger` + `kv-list`. Source 01 v1.
- **Check it yourself · rows (compact variant)**: `.verify` > `dl.verify-list` > `.verify-row` (3 columns, stacked at 640) where cards are too heavy (15, 16). Source 01 v1.
- Removed on 12-Oct-2026: the v1 Entity doors (its shortened F&O strip is not the verbatim box) and the v2 form card states (replaced by the v3 states).
