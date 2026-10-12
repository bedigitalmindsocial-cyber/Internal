# Pattern library

Every reusable section layout, so 75 pages stay one family. Page agents reuse these first ("Option A" in the layout step).
Source markup: `theme/sections-reference.html` (theme v1 homepage, each section preceded by its PATTERN comment).
New patterns are added only by golden pages and promoted by the orchestrator after review (CSS moves into `theme/patterns.css`).
Golden-page markup: `theme/components.html` (index in `theme/components.md`). Rows marked "01" or "09" were promoted from the pilot goldens on 12-Oct-2026; their CSS is in `theme/patterns.css`, not in the pages.

| Pattern | Root class | Specs | Reuse on | Source |
|---|---|---|---|---|
| Hero · proof before form | `section.hero` [h-hero] | d1 serif 64/66, creds strip, lead bar | Invest, Trade, Open Account | theme v1 |
| Pillars · editorial 2×2 | `section.band` [h-trust] | hairline grid, no cards | About, Help Centre | theme v1 |
| Product card | `section.band.band--mist` #products | r16 · shadow-1 → shadow-2 on hover, 48px icon tile | Invest, Trade hubs | theme v1 |
| Charges block | `section.band` #pricing | serif ₹0 numeral, data table, "to confirm" placeholder | Pricing page | theme v1 |
| Process steps | `section.band.band--mist` [h-steps] | numbered: order matters, gold connector = root line; `--cols` applies from 900 px, theme gives 2 columns at 899 and 1 at 640 | Start Trading, Start Investing | theme v1 (breakpoint fix from 01/09) |
| Goal tiles | `section.band` #goals | serif d3 title, link to a calculator | Plan &amp; Tools, goal pages | theme v1 |
| Calculator | `section.band.band--mist` #calc | range + output pairs, split bar + yearly bars | 6 calculator pages | theme v1 |
| Feature switcher | `section.band` [h-feat] | vertical tablist, panel enters 450ms | product pages | theme v1 |
| Market modules | `section.band.band--mist` #markets | index card · IPO row · fund card, riskometer | Phase 2 data pages | theme v1 |
| Group + credential wall | `section.band` #about | root diagram (SVG geometry), mono for registration codes | About, Aikyam Capital | theme v1 |
| Article card + thumbnail system | `section.band.band--mist` #learn | 16:10 · brand gradient · serif title · rings | Learn, Guides, Glossary | theme v1 |
| FAQ accordion | `section.band` #faq | native details/summary, answers in HTML for search | every product page | theme v1 |
| Dark band · one per page | `section.band.band--dark` [h-app] | app-icon gradient #1C0F2F → #0C2229 | Get the App, final CTA | theme v1 |
| Closing CTA | `section.band` #final | d2 + two buttons, every page ends here |  | theme v1 |
| Mandatory disclosure | `section.band.band--mist.band--tight` #risk | never collapsed, verbatim SEBI text | every F&amp;O page | theme v1 |
| Header (full) | `header.site-head` | announcement bar, logo, mega menus Invest/Trade/Plan & Tools, Learn, Pricing, About, Help, search, Login, Open free account | every page except template D | theme v1 / shell |
| Header (minimal) | `header.site-head.site-head--min` | logo, "Need help? Talk to us", Login | template D | shell |
| Footer (full) | `footer.site-foot` | 5 columns, two-entity registration strip (mono), Attention Investors, disclaimer, caution | every page except template D | theme v1 / shell |
| Footer (short) | `footer.site-foot.site-foot--min` | legal links row, registration strip, market-risk line, base | template D | shell |
| Breadcrumb | `nav.crumbs-bar > ol.crumbs` | rendered by build from front matter | all pages except Home and D | theme v1 / shell |
| Placeholder | `mark.ph`, `div.ph.ph--block` | gold-wash chip; dashed block for images and client-supplied text; blocks and chips in form cards, risk boxes and docs strips wrap, and every chip in main wraps below 900 px (cloned padding per line) | anywhere a value is unconfirmed | shell (wrap fix from 01/09) |
| Hero · form card (template D) | `section.hero` > `.hero-grid` + `.hero-side` > `section.form-card#s-open` | hero copy and creds left (7), form card right (5), top-aligned; card: label, h2 styled h3, +91 field with help, unticked consent, receiver line, full-width submit, handoff; 3+ states on the board | 10 Start Investing, 11 Get the App (notify card), 75 Paid landing | 09 |
| Form card · cost line + side door | `.form-card .cost-line`, `.side-door` | hairline under the form, charge token + "See all charges"; the other company's wrapping link with its risk line under the card | 75, any form that must answer cost where you act | 01 |
| Cost cred | `.creds li.cred-cost` + `.cost-line` | a cred whose value is a charge chip plus a link spans both cred columns | 10, 75, any hero with a cost cred | 09 |
| Docs strips, stacked | `.docs` + `.docs` | 16 px apart, shared 17rem label column from 900 px; right side a list or a `.stack` of one line + `ph--block`; `.steps-note` under the steps | 10, 75 | 09 |
| Charges block · placeholder numeral | `.price-grid` > `.zero.zero--top` | unconfirmed value renders at body size in the serif numeral slot (a confirmed value fills it, no markup change); card content grouped at the top; `.fees` stack; visible `.data caption`; row title bold in the stacked 2-column table at 640 | 06 Pricing, 75 | 09 |
| Info card split | `.split` > `.info-card` | lead + link left, white cards right (h3, copy or `ph--block`, `.links`); changing figures are linked to the exchange, never printed | 37 F&O, 38 Currency and Commodity, 75 | 09 |
| FAQ on a Mist band | `.band--mist .faq` | plus button on paper so it stays visible on Mist | any FAQ on a Mist band | 09 |
| Closing CTA · phones | `.final .row` | both buttons stack full width at 640 | every page with two closing buttons | 09 |
| Wrapping link | `a.link.link--wrap` + `span.link-tail` | inline link, arrow follows the last word when the label wraps | side doors, external links, any long label | 09 |
| Entity doors | `.doors` > `article.door` | one panel per company: label + company h3 + `.door-reg .mono` code; `.door-rows` (tile + name link + one line); warn `.risk` strip; `.door-foot` pinned bottom (action, risk line, hub link); 2 columns, 1 at 899 | Invest and Trade hubs, 06 Pricing, 07 About | 01 |
| Two ledgers | `.ledgers` > `.ledger` | 7/5; `.ledger-head` names the company; 2-column `table.data--stack` rows become one line (charge left, value right) at 640; `dl.kv-list` card for non-tabular terms | 06 Pricing, 13 Aikyam Wealth, 30 commission disclosure | 01 |
| Group map | `figure.gmap` | HTML root node, `svg.gmap-lines` (4 paths, non-scaling stroke), `ul.gmap-branches` (`.is-on` = on ROOT) with HTML labels; 2 x 2, no lines at 640. Replaces the theme diagram's SVG text | 07 About, 12 Aikyam Capital, 13 Aikyam Wealth | 01 |
| Check it yourself ledger | `.verify` > `dl.verify-list` > `.verify-row` | company link + role, `.mono` registration token, regulator link (opens their site); 3 columns, stacked at 640 | 07 About, 12, 13, 15 Contact, 16 Disclosures | 01 |
| Facts list | `ul.facts` | icon + one checkable line; claim-free replacement for the theme pillars | 07 About, Help Centre | 01 |
| Disclosure band · MF and distribution | `.band--mist.band--tight` > `.risk-box` (info icon) | risk-box with the info icon in ink; verbatim MF risk line + distributor disclaimer; never collapsed | Aikyam Wealth and mixed pages | 01 |
| Dark band copy | `.band--dark .lead/.handoff/.illus/.link` | on-dark colours for copy and links on the gradient | any dark band | 01 (fix) |
| Mono codes | `.mono` | Red Hat Mono 500 for registration codes outside creds-wall and foot-reg | doors, verify ledger, creds | 01 |
