# Pattern library

Every reusable section layout, so 75 pages stay one family. Page agents reuse these first ("Option A" in the layout step).
Source markup: `theme/sections-reference.html` (theme v1 homepage, each section preceded by its PATTERN comment).
New patterns are added only by golden pages and promoted by the orchestrator after review (CSS moves into `theme/patterns.css`).

| Pattern | Root class | Specs | Reuse on | Source |
|---|---|---|---|---|
| Hero · proof before form | `section.hero` [h-hero] | d1 serif 64/66, creds strip, lead bar | Invest, Trade, Open Account | theme v1 |
| Pillars · editorial 2×2 | `section.band` [h-trust] | hairline grid, no cards | About, Help Centre | theme v1 |
| Product card | `section.band.band--mist` #products | r16 · shadow-1 → shadow-2 on hover, 48px icon tile | Invest, Trade hubs | theme v1 |
| Charges block | `section.band` #pricing | serif ₹0 numeral, data table, "to confirm" placeholder | Pricing page | theme v1 |
| Process steps | `section.band.band--mist` [h-steps] | numbered: order matters, gold connector = root line | Start Trading, Start Investing | theme v1 |
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
| Placeholder | `mark.ph`, `div.ph.ph--block` | gold-wash chip; dashed block for images and client-supplied text | anywhere a value is unconfirmed | shell |
