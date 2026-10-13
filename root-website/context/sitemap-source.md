# ROOT by Aikyam: sitemap as found in the sources

Compiled 12-Oct-2026 from earlier chats and artifacts. Every fact carries a source tag. Nothing here is client-approved unless a source says so.

## Sources, newest first

| Tag | What it is | Date | Page count it states |
|---|---|---|---|
| [Fact base 12-Oct] | Internal fact base written in the session "Root business objectives and sitemap" | 12-Oct-2026 | Restates Sitemap v2 and proposes an "IA v3 (Motilal pattern)" marked "a proposal for discussion, not an agreed sitemap" |
| [Data Points 09-Oct] | Claude Doc "ROOT Data Points to Fetch" | 09-Oct-2026 | Phase 2 data pages only |
| [MO API Map 09-Oct] | Artifact "Motilal Oswal API Map", section "What ROOT needs for Phase 2" | 09-Oct-2026 | Phase 2 data pages, "live 8 Dec 2026" |
| [Theme v1 08-Oct] | Artifact "ROOT Website Theme" (theme v1, "prepared by Giraffe Partners for the Phase 1 design workshop") | 08-Oct-2026 | **73 pages, 3 phases, 8 templates (A to H), "the approved plan"** |
| [Sitemap v2 sheet] | Google Sheet "ROOT by Aikyam Sitemap-v2 (2)" (created 10-Sep, modified 21-Sep) | 21-Sep-2026 | About 50 rows, entity-tagged, 3 tabs: Sitemap, Entity & Compliance Map, Footer & Notes |
| [session 09-Sep] | Session "ROOT by Aikyam sitemap proposal" (09 to 16-Sep) | 09-Sep-2026 | "Twelve nav sections, roughly 73 URLs", "~73 pages on 14 templates" |
| [session 06-Sep] | Session "ROOT by Aikyam website sitemap" | 06-Sep-2026 | "roughly 55 to 58 pages / ~35 unique templates" |

**Newest statement of the approved page list: [Theme v1 08-Oct].** The 12-Oct fact base is newer, but it says it could not find the phase split, and its v3 IA is labelled a proposal for discussion. So it does not replace the theme's list. [Data Points 09-Oct] and [MO API Map 09-Oct] agree with the theme's Phase 2 list and its 8-Dec date.

**The 75-page working list** is `root-website/sitemap.json` (created in the current session). It is the theme's 73 pages plus two pages the build added: `login` and `lp-open-account`. The slugs below come from that file. No source has approved any slug. [Placeholder Register] Q14 is still open: does the site use trailing-slash directory URLs or `.html` files? Pick one before indexing.

## The 73-page plan as the theme states it [Theme v1 08-Oct]

| Phase | Pages | Templates named for the phase |
|---|---|---|
| Phase 1, 25 pages, live **2 Nov 2026** | Home, Invest, Trade, Plan & Tools, Learn, Pricing, About, Help Centre; Start Trading, Start Investing, Get the App; Aikyam Capital, Aikyam Wealth, Leadership, Contact; 10 legal and compliance pages | Home, A, D, E, F, G |
| Phase 2, 25 pages, live **8 Dec 2026** | Mutual Funds, Fund Explorer, SIP, Scheme detail, Distribution Fee Disclosure; IPO, Upcoming IPOs, IPO Calendar, IPO detail; Equity, Intraday & Delivery, F&O, Currency & Commodity, Stock detail, Markets & Indices; Calculators hub + 6 calculators, Risk Profiler, Retirement, Child Education | A, B, C, G |
| Phase 3, 23 pages, **13 Jan 2027** | Insurance (4), Bonds, NPS, PMS (4) "as CMS drafts"; Partner with ROOT, Distributor Partner, Authorised Person; Tax Saving, 5 Guides, Glossary; Careers, Press & Media, Raise a Ticket | A, B, E, F |

### Templates [Theme v1 08-Oct]

| Code | Name | Block stack | Pages the theme names |
|---|---|---|---|
| A | Hub page | Header + mega-menu; breadcrumb + d1 + creds hero; sticky lead form (right column); product cards 3-up; pillars or steps; calculator teaser; FAQ; dark band (app or closing CTA); risk + light footer | Invest, Trade, Plan & Tools, Mutual Funds, IPO, Equity, F&O, Currency & Commodity, Insurance (draft) |
| B | Detail page | Header; breadcrumb + name + price; chart + range tabs, quote card with lead capture; stat blocks; data tables; riskometer / IPO dates; disclaimers + source; footer | Stock detail, Scheme detail, IPO detail, Markets & Indices, Fund Explorer results. "Programmatic SEO lives here." |
| C | Calculator page | Header; breadcrumb + d1; calculator above the fold; Start investing CTA; how it works (article); formula + example; FAQ; footer | SIP, Lumpsum, Retirement, Brokerage, Margin, SPAN, Risk Profiler, Retirement and Child Education planning |
| D | Account opening | Logo only, no menu; d1 + creds, sticky form right; ₹0 numeral + charges; four steps + documents; FAQ; short footer + risk | Start Trading, Start Investing, Get the App, every paid-ads landing page |
| E | Article | Header; thumbnail + d1 + read time; 66ch body, tables, callouts; inline calculator or CTA; related guides; footer | Learn, the five Guides, Glossary, Tax Saving, Press & Media, monthly SEO articles |
| F | Company page | Header; d1 + lead; group root diagram; people grid (photos); credential wall; closing CTA band; footer | About ROOT & the Group, Aikyam Capital, Aikyam Wealth, Leadership, Careers, Partner pages, Contact |
| G | Legal page | Header; d2 + last updated date; numbered clauses, sticky contents list; Download PDF; footer | Privacy, T&C, Disclosures & Investor Charter, Grievance & SCORES/ODR, Policies, Bank Accounts, Escalation & KMP, Risk Disclosure, Notices |
| H | Coming-soon product | Header; d1 + "Coming soon" badge; what it is, who it's for (CMS draft); "Tell me when it's live" dialog; related live products; footer | Insurance (4 pages), Bonds & Fixed Income, NPS, PMS (4 pages). "Kept as drafts until each product is cleared to launch." |

## Page-by-page table (75 rows: 73 plan pages + 2 build additions)

"Tpl named in Theme v1" shows the template the theme names for that page. "not stated" means the theme names no template for it, so the template in `sitemap.json` is an inference. "Entity in Sitemap v2" comes from the client-facing v2 sheet.

| # | Page (sitemap.json title) | Slug in sitemap.json | Tpl in sitemap.json | Tpl named in Theme v1 | Phase | Entity in sitemap.json | Entity in Sitemap v2 |
|---|---|---|---|---|---|---|---|
| 1 | Home | `/` | HOME | Home | 1 | Both | n/a |
| 2 | Invest | `/invest` | A | A | 1 | Both | Wealth |
| 3 | Trade | `/trade` | A | A | 1 | Capital | Capital |
| 4 | Plan & Tools | `/plan` | A | A | 1 | Both | not in v2 |
| 5 | Learn | `/learn` | A | E | 1 | Both | Both |
| 6 | Pricing | `/pricing` | A | not stated | 1 | Both | Capital (Brokerage & Charges) |
| 7 | About ROOT and the Aikyam Group | `/about` | F | F | 1 | Both | Both |
| 8 | Help Centre | `/help` | A | not stated | 1 | Both | Both |
| 9 | Start Trading | `/open-account/trading` | D | D | 1 | Capital | Capital |
| 10 | Start Investing | `/open-account/investing` | D | D | 1 | Wealth | Wealth |
| 11 | Get the App | `/app` | D | D | 1 | Both | not in v2 |
| 12 | Aikyam Capital | `/about/aikyam-capital` | F | F | 1 | Capital | Capital |
| 13 | Aikyam Wealth | `/about/aikyam-wealth` | F | F | 1 | Wealth | Wealth |
| 14 | Leadership | `/about/leadership` | F | F | 1 | Both | Both |
| 15 | Contact | `/contact` | F | F | 1 | Both | Both |
| 16 | Disclosures and Investor Charter | `/legal/disclosures` | G | G | 1 | Both | Capital + Wealth (two pages in v2) |
| 17 | Grievance Redressal, SCORES and ODR | `/legal/grievance-redressal` | G | G | 1 | Both | Both |
| 18 | Escalation Matrix and Key Managerial Persons | `/legal/escalation-matrix` | G | G | 1 | Both | not in v2 |
| 19 | Policies | `/legal/policies` | G | G | 1 | Both | not in v2 |
| 20 | Client Bank Accounts | `/legal/client-bank-accounts` | G | G | 1 | Capital | not in v2 |
| 21 | KYC and Account Opening Documents | `/legal/kyc-documents` | G | not stated | 1 | Both | Both |
| 22 | Risk Disclosure | `/legal/risk-disclosure` | G | G | 1 | Capital | not in v2 |
| 23 | Notices and Caution to the Public | `/legal/notices` | G | G | 1 | Both | not in v2 |
| 24 | Terms and Conditions | `/legal/terms` | G | G | 1 | Both | Both |
| 25 | Privacy Policy | `/legal/privacy` | G | G | 1 | Both | Both |
| 26 | Mutual Funds | `/invest/mutual-funds` | A | A | 2 | Wealth | Wealth |
| 27 | Fund Explorer | `/invest/mutual-funds/explore` | B | B | 2 | Wealth | Wealth |
| 28 | SIP | `/invest/sip` | A | not stated | 2 | Wealth | Wealth |
| 29 | Scheme Detail (example) | `/invest/mutual-funds/example-flexi-cap-fund` | B | B | 2 | Wealth | not in v2 |
| 30 | Distribution Fee and Commission Disclosure | `/legal/distribution-commission` | G | not stated | 2 | Wealth | Wealth |
| 31 | IPO | `/ipo` | A | A | 2 | Capital | Capital |
| 32 | Upcoming IPOs | `/ipo/upcoming` | B | not stated | 2 | Capital | Capital |
| 33 | IPO Calendar and Allotment Status | `/ipo/calendar` | B | not stated | 2 | Capital | Capital |
| 34 | IPO Detail (example) | `/ipo/example-ipo` | B | B | 2 | Capital | not in v2 |
| 35 | Equity | `/trade/equity` | A | A | 2 | Capital | Capital |
| 36 | Intraday and Delivery | `/trade/intraday-delivery` | A | not stated | 2 | Capital | Capital |
| 37 | Futures and Options | `/trade/futures-options` | A | A | 2 | Capital | Capital |
| 38 | Currency and Commodity | `/trade/currency-commodity` | A | A | 2 | Capital | Capital |
| 39 | Stock Detail (example) | `/stocks/example` | B | B | 2 | Capital | not in v2 |
| 40 | Markets and Indices | `/markets` | B | B | 2 | Capital | not in v2 |
| 41 | Calculators | `/tools` | A | not stated | 2 | Both | not in v2 |
| 42 | SIP Calculator | `/tools/sip-calculator` | C | C | 2 | Wealth | Wealth |
| 43 | Lumpsum Calculator | `/tools/lumpsum-calculator` | C | C | 2 | Wealth | Wealth |
| 44 | Retirement Calculator | `/tools/retirement-calculator` | C | C | 2 | Wealth | Wealth |
| 45 | Brokerage Calculator | `/tools/brokerage-calculator` | C | C | 2 | Capital | Capital |
| 46 | Margin Calculator | `/tools/margin-calculator` | C | C | 2 | Capital | Capital |
| 47 | SPAN Calculator | `/tools/span-calculator` | C | C | 2 | Capital | Capital |
| 48 | Risk Profiler | `/tools/risk-profiler` | C | C | 2 | Both | Both |
| 49 | Retirement Planning | `/plan/retirement` | C | C | 2 | Wealth | Wealth |
| 50 | Child Education Planning | `/plan/child-education` | C | C | 2 | Wealth | Wealth |
| 51 | Insurance | `/insurance` | H | A and H | 3 | TBC | TO CONFIRM |
| 52 | Life Insurance | `/insurance/life` | H | H | 3 | TBC | TO CONFIRM |
| 53 | Health Insurance | `/insurance/health` | H | H | 3 | TBC | TO CONFIRM |
| 54 | Motor, Travel and Home Insurance | `/insurance/general` | H | H | 3 | TBC | TO CONFIRM |
| 55 | Bonds and Fixed Income | `/invest/bonds` | H | H | 3 | Wealth | Wealth |
| 56 | NPS | `/invest/nps` | H | H | 3 | Wealth | Wealth |
| 57 | PMS | `/invest/pms` | H | H | 3 | Wealth | Wealth |
| 58 | Empanelled PMS Strategies | `/invest/pms/strategies` | H | H | 3 | Wealth | Wealth |
| 59 | PMS Manager Profiles | `/invest/pms/managers` | H | H | 3 | Wealth | Wealth |
| 60 | PMS Eligibility and Minimum Investment | `/invest/pms/eligibility` | H | H | 3 | Wealth | Wealth |
| 61 | Partner with ROOT | `/partner` | F | F | 3 | Both | not in v2 |
| 62 | Distributor Partner Programme | `/partner/distributor-programme` | F | F | 3 | Wealth | Wealth |
| 63 | Authorised Person Programme | `/partner/authorised-person` | F | F | 3 | Capital | Capital |
| 64 | Tax Saving | `/plan/tax-saving` | E | E | 3 | Wealth | Wealth |
| 65 | Guide: Getting Started | `/learn/guides/getting-started` | E | E | 3 | Both | Both |
| 66 | Guide: Mutual Funds | `/learn/guides/mutual-funds` | E | E | 3 | Wealth | Both |
| 67 | Guide: PMS | `/learn/guides/pms` | E | E | 3 | Wealth | Both |
| 68 | Guide: Insurance | `/learn/guides/insurance` | E | E | 3 | TBC | Both |
| 69 | Guide: Trading Basics | `/learn/guides/trading-basics` | E | E | 3 | Capital | Both |
| 70 | Glossary | `/learn/glossary` | E | E | 3 | Both | not in v2 |
| 71 | Careers | `/careers` | F | F | 3 | Both | Both |
| 72 | Press and Media | `/press` | E | E | 3 | Both | Both |
| 73 | Raise a Ticket | `/help/raise-ticket` | F | not stated | 3 | Both | Both |
| 74 | Login | `/login` | D | not stated | 3 | Both | not in v2 |
| 75 | Paid Campaign Landing Page | `/lp/open-account` | D | not stated | 3 | Capital | not in v2 |

Entity codes: Capital = Aikyam Capital Private Limited (broking, own service). Wealth = Aikyam Wealth Private Limited (distribution under an AMFI ARN, plus third-party PMS). Both = group-level page. TBC = insurance licensing entity not confirmed. [Sitemap v2 sheet, Entity & Compliance Map]

## Discrepancies between sources

1. **Page count.** 55 to 58 pages [session 06-Sep], about 50 [session 09-Sep], "1 page to 70 pages" [session 09-Sep], about 73 [session 09-Sep], 73 [Theme v1 08-Oct], 75 [sitemap.json, which adds Login and one paid landing page]. 73 is the approved plan; the 2 extra pages are build additions.
2. **The 10th Phase 1 legal page is not named.** The theme says "10 legal and compliance pages" but the Template G list names 9 (Distribution Fee Disclosure is Phase 2). `sitemap.json` fills the gap with "KYC and Account Opening Documents". That matches v2's "KYC / Account Opening Policy" and the footer link "Standard KYC Documents". TO CONFIRM.
3. **Phase 3 templates.** The phase table lists Phase 3 as "A, B, E, F". But Template H explicitly covers Insurance (4), Bonds, NPS and PMS (4), and Template A lists "Insurance (draft)". `sitemap.json` uses H for all ten. Treat H as correct; the phase table omits it.
4. **Learn hub template.** Template E (Article) lists "Learn", and Phase 1 includes E. `sitemap.json` uses A for Learn. TO DECIDE.
5. **IPO placement.** v2 puts IPO under Trade (Aikyam Capital). The theme's header puts "IPOs" and "ETFs" under the Invest mega-menu. Entity stays Aikyam Capital either way.
6. **ETFs.** They appear in the theme's Invest menu, product cards and footer, but there is no ETF page in the 73. TO DECIDE: add a page or link elsewhere.
7. **Direct Plans** (v2: Invest > Mutual Funds > Direct Plans) were dropped from the 73-page plan. This is deliberate: an ARN-registered distributor cannot deal in Direct Plans [Fact base 12-Oct, citing CX context doc]. The Drive copy of v2 still shows the line, and "Become an IFA" and "Sub-broker". The corrected wording lives in the theme and `sitemap.json`.
8. **Pricing entity.** v2 tags "Brokerage & Charges" as Aikyam Capital and the distribution-fee page as Aikyam Wealth. `sitemap.json` tags Pricing "Both", because the theme's charges table includes a Mutual Funds row.
9. **Stock detail and data pages.** [Fact base 12-Oct] recommends DEFERRING stock quote pages until a market-data licence exists. [Theme v1 08-Oct], [MO API Map 09-Oct] and [Data Points 09-Oct] keep Stock detail, Markets & Indices, F&O and Currency & Commodity in Phase 2. The data licence is TO CONFIRM (see placeholders.md).
10. **IA v3 proposal** [Fact base 12-Oct] uses a different header: Trade, Invest, IPO, Pricing, Learn, Partner, Support, Login (Trading / Client Desk / Partner Desk), Open Account. It also uses different slugs (`/trade/stocks`, `/trade/commodity` and `/trade/currency` as separate pages, `/support/...`, `/disclosures/aikyam-capital`, `/glossary/{term}`, `/market-holidays/{year}`, `/important-links`). It is a proposal, not approved.
11. **Launch date.** The theme says Phase 1 goes live 2 Nov 2026. [Fact base 12-Oct], citing the 18-Sep CX doc, records an earlier target go-live of 20-Oct-2026 and a content freeze around 9-Oct. That earlier date is superseded by the theme's phasing; whether the client has agreed to 2 Nov is TO CONFIRM.

## In other sources but not in the 73-page plan

| Item | Where it appears | Status |
|---|---|---|
| e-KYC page redesign (`ekyc.rootbyaikyam.com`) | Client email in [session 06-Sep]: redesign of the Login page **and** the e-KYC page | Not in `sitemap.json`. The Login page is (#74). These are vendor-built React apps (likely Finovo 1KYC). Design-only vs implementation is TO CONFIRM |
| Track Ticket Status | Sitemap v2, Support | Not in plan (only Raise a Ticket) |
| Partner / Client Desk Login | Sitemap v2, Partner with Us ("separate from trading login", NJ Wealth "Client Desk" naming) | Not in plan |
| Blog / Market & Fund Insights posts | Sitemap v2, Learn | Learn hub is in Phase 1; the theme counts recurring SEO articles outside the 73 |
| Guides hub, Goal-Based Planning hub | Sitemap v2 | Not separate pages in the 73 |
| The Aikyam Group page | Sitemap v2, About | Merged into "About ROOT & the Group" |
| AIF | Client launch brief names "PMS, AIFs" [session 09-Sep]; the group runs AIFs | Not in v2 or the 73. AIFs are private placement only, minimum ₹1 crore, no scheme-level public content [CX context doc]. TO CONFIRM whether any AIF page is wanted |
| Paid landing pages | Template D, "every paid-ads landing page" | `sitemap.json` #75 is one example. Each one counts as an advertisement and needs exchange filing |
| Stock directory, market holidays, news, research, NRI, US stocks | MO pattern / IA v3 proposal | Deferred or blocked; see motilal-patterns.md |
