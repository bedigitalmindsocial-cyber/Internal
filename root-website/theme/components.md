# Component markup library

Canonical markup in `theme/components.html` (find a block by its `<!-- COMPONENT: name -->` comment); CSS in `theme/patterns.css`. Copy the block, keep class names, replace the copy. Verbatim compliance blocks stay in `rules/compliance-blocks.md`. Curated 12-Oct-2026 from 01 Home and 09 Start Trading.

- **Hero · form card (template D)**: `section.hero` > `.hero-grid` (`.hero-copy` with `.root-seed`, h1, lead, `ul.creds` with `li.cred-cost`) + `.hero-side` (`section.form-card#s-open`, `.hero-alt` wrapping link). Use for 09, 10, 11 (notify card), 75. Source 09 s-hero.
- **Form card · states**: OTP sent, invalid number, consent missing, wrong OTP, verified, each a `<template data-state>` block of `.form-card`. Use for every template D form (3+ states). Source 09.
- **Form card · cost line + side door**: `.hero-side` > `.form-card` with `p.small.cost-line` at its foot + `.side-door` (wrapping link + one `xs` line). Use for 01, 75, any form that must answer cost where you act. Source 01 s-hero.
- **Process steps + docs strips**: `ol.steps` (`--cols` when not 4) + stacked `.docs` strips (shared label column from 900 px, `.stack` with a `ph--block`) + `p.steps-note` + `.band-cta`. Use for 09, 10, 75. Source 09 s-steps.
- **Charges block · placeholder numeral**: `.price-grid` > `.zero.zero--top` (`.big` numeral, `.fees`) + captioned two-column `table.data.data--stack` with `td-label`. Use for 06, 09, 75. Source 09 s-charges.
- **Info card split**: `.split` with lead and link left, `.info-card` blocks (h3, copy or `ph--block`, `.links`) right. Use for 37, 38, 75. Source 09 s-fo.
- **FAQ split on a Mist band**: `.band--mist` > `.split` (intro, grievance email, Help Centre link) + `.faq` native `details`, first open. Use for every product and onboarding page. Source 09 s-faq.
- **Closing CTA · two buttons**: `.final` > h2 naming the company + `.row` (primary, other company ghost; full width at 640) + `p.handoff`. Use for every page end. Source 09 s-final.
- **Entity doors**: `.doors` > `article.door` (`.door-head` label + h3 company + `.door-reg .mono`; `ul.door-rows` of `.tile` + `.row-text`; `.risk` strip; `.door-foot`). Use for 01, Invest and Trade hubs, 06, 07. Source 01 s-products.
- **Two ledgers**: `.ledgers` (7/5) > `.ledger` (`.ledger-head`, two-column `table.data--stack` that becomes one line per row at 640; `dl.kv-list` card). Use for 01, 06, 13, 30. Source 01 s-pricing.
- **Group section · who is behind ROOT**: `.split` of copy + facts list and the group map, then the check-it-yourself ledger. Use for 01, 07, 12, 13. Source 01 s-group.
- **Facts list**: `ul.facts` (icon + one checkable line), the claim-free replacement for the theme pillars. Use for 01, 07, Help Centre. Source 01 s-group.
- **Group map**: `figure.gmap` (`.gmap-root`, `svg.gmap-lines` with non-scaling strokes, `ul.gmap-branches` > `li.is-on` > `.gmap-dot` + `.gmap-card`); HTML labels, 2 x 2 at 640. Use for 01, 07, 12, 13. Source 01 s-group.
- **Check it yourself ledger**: `.verify` > `dl.verify-list` > `.verify-row` (dt company link + role, dd `.mono` code, dd regulator link). Use for 01, 07, 12, 13, 15, 16. Source 01 s-group.
- **Disclosure band · mutual funds and distribution**: `.band--mist.band--tight` > `.risk-box` with the info icon (ink colour), verbatim MF risk line and distributor disclaimer. Use for Aikyam Wealth and mixed pages. Source 01 s-disclosures.
- **Wrapping link**: `a.link.link--wrap` with the last word and icon in `span.link-tail`. Use for any long link label. Source 09.
- **Utility `.mono`**: Red Hat Mono 500 for registration codes outside `creds-wall` and `foot-reg` (no block; see the doors and the verify ledger). Source 01.
