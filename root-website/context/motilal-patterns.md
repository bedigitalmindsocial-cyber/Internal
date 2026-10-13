# Motilal Oswal patterns for ROOT: ADOPT / ADAPT / BLOCKED

Compiled 12-Oct-2026. Sources: [MO UI Teardown 08-Oct] (computed styles from the live motilaloswal.com, 1440 and 375 viewports), [MO API Map 09-Oct] (live data calls, used as a spec only), [Fact base 12-Oct] (17-row learning table and IA v3 proposal; Motilal facts there are search-derived, not verified on the page), [Theme v1 08-Oct] ("Taken from Motilal Oswal" and "Made ROOT's own").

Guiding rule: **take the system, not the skin** [MO UI Teardown 08-Oct]. **Copy the machine, not the claims** [Fact base 12-Oct]. The client asked for Motilal Oswal's look and feel as inspiration; ROOT should feel as calm and credible without looking like a copy.

Legend: **ADOPT** = use as is. **ADAPT** = keep the idea, change the execution. **BLOCKED** = licence, regulatory or brand reasons forbid it. **DEFER** = possible later, once a dependency exists. **AVOID** = a Motilal weakness to fix, not copy.

## Visual system

| Pattern | Call | One-line reason |
|---|---|---|
| One ink colour for all text, headings, buttons, icons (MO indigo #2B2E8C, never black) | ADOPT | Most of the "brand feel". ROOT uses aubergine #1C0F2F [Theme v1 08-Oct] |
| Accent as a spark only (MO gold in icons, logo, awards; never buttons or backgrounds) | ADOPT | Keeps the accent meaning "value". ROOT gold #C19C2F follows the same rule |
| Serif for headings only + clean sans for everything else | ADAPT | Keep the idea, change the fonts: ROOT uses Tiro Devanagari Hindi + Mukta |
| Butler + Poppins fonts | BLOCKED | Using them would read as a clone; Butler's licence is also unconfirmed |
| One soft two-layer shadow on every card, no card borders | ADOPT | Calm, light surfaces. ROOT tints shadows aubergine; a card never has a border and a shadow together |
| Section recipe: title, gap, card grid, centred CTA, alternating white and tinted bands, no divider lines | ADOPT | Coherence across a large site. ROOT left-aligns headings on the gold "root line" |
| Filled duotone icon family with one gold detail | ADAPT | ROOT draws line icons (24px grid, 1.5px stroke) with exactly one gold spark, as one family, not two |
| MO icon artwork, logo, gold arc, "Think Equity, Think Motilal Oswal" lines | BLOCKED | Motilal Oswal brand assets; must not appear even in reference mocks |
| Logo motif framing every blog/social thumbnail | ADOPT | Cheap way to keep hundreds of images on-brand. ROOT uses the two rings from the logo's O-o |
| Almost no motion; stillness as a trust signal | ADOPT | ROOT allows short, calm motion only; no parallax, counting numbers or pulsing CTAs |
| No hover feedback on cards | AVOID | Add a 2px lift, a deeper shadow, a focus ring and a pointer cursor |
| CSS `text-transform: capitalize` on H2s | AVOID | Produces "At 0 Cost". Write sentence case by hand |
| Underlined uppercase text inside filled buttons | AVOID | Reads as a link stuck in a box |
| Three different blues across templates; About page losing the brand fonts | AVOID | Pick one ink and one link colour; every template loads the same families |
| Very long pages (10 to 15 sections) | AVOID | Cut sections, not padding |
| Screenshots of MO pages | BLOCKED (outside internal use) | Internal design reference only |

## Page structures

| Pattern | Call | One-line reason |
|---|---|---|
| Product page: H1 + USP ticks + sticky form card right; proof; offer cards; what/why; why us; steps; FAQ | ADAPT | Becomes ROOT Template A (Hub) with a sticky lead form and a FAQ, without MO's 10-section length |
| Paid landing: logo only, no menu or footer links, sticky form (desktop), fixed bottom CTA (mobile) | ADOPT | Becomes Template D for Start Trading, Start Investing, Get the App and every paid landing page |
| Stock page: chart left, sticky quote card right with a mobile-number form inside the data | ADAPT | Becomes Template B with "quote card with lead capture"; needs a licensed data feed |
| SIP calculator: the tool is the hero, the SEO article sits below | ADOPT | Becomes Template C, calculator above the fold, formula + example + FAQ |
| Learning Centre: featured carousel, filter pills, 3-column cards with date and read time | ADAPT | Becomes Template E plus the Learn hub; dated `/learning-centre/{yyyy}/{m}/{slug}` URLs are not needed |
| About: full-bleed video hero, founders cut out | ADAPT | ROOT uses Template F with the group root diagram, real people photos only after a shoot |
| Every product/tool page ends in a long article + FAQs (education as SEO) | ADOPT | Ranks and builds trust; FAQ answers rendered in HTML |
| CTA after every section | ADOPT | A closing CTA on every block ("every page ends here") |

## Hero and trust

| Pattern | Call | One-line reason |
|---|---|---|
| Proof before the form: H1, then 4 or 5 concrete trust items, then a two-field form | ADOPT | ROOT's creds strip: SEBI-registered broker INZ000321232; Member of NSE, BSE, MCX, MSEI; Backed by Aikyam Capital Group; ₹0 account opening; NSDL DP IN305066 |
| Minimum-field form: mobile with a fixed +91 prefix, consent text below | ADOPT | Two fields feel like nothing; the +91 prefix reassures |
| No stock hero image, no carousel in the hero | ADOPT | Product screens and logo geometry instead |
| Scale trust strip (40L+ customers, 37+ years, 2,500+ branches, awards) | BLOCKED | ROOT cannot back these numbers; invented counts are a SEBI advertising breach. Use checkable facts only |
| "Award Winning Research", free reports, stock ideas, gated research teaser cards | BLOCKED | Needs a SEBI Research Analyst registration (MO holds INH000000412); none is known for Aikyam |
| Gated teaser cards (2 open, rest blurred) for any other real data | ADAPT | Only with real data the client may show; never fake numbers |
| Founder/expert videos | ADAPT | Real Aikyam leadership only, after a shoot; no testimonials |

## Account opening

| Pattern | Call | One-line reason |
|---|---|---|
| "Open Demat Account" button in the header on every page, and fixed in the mobile top bar | ADOPT | ROOT: "Open free account" as the one primary label in header, hero and footer |
| Step 1 = mobile number + OTP, then PAN, Aadhaar, bank, e-sign | ADOPT | Drop-offs become callable leads; ROOT shows the four steps and a documents list |
| Separate onboarding host (ekyc.motilaloswal.com) | ADOPT | ROOT already has `ekyc.rootbyaikyam.com`; replace the UAT login link first |
| Pre-ticked marketing consent | BLOCKED | DPDP Act requires active opt-in |
| NRI accounts (PIS via partner banks, offline activation) | DEFER | Needs a PIS bank tie-up and an NRI route |
| WhatsApp chatbot for demat/IPO | DEFER | Not scoped; status of MO's own bot unknown |

## Pricing presentation

| Pattern | Call | One-line reason |
|---|---|---|
| "₹0" as a giant hero numeral (MO shows ₹0 three times: account, brokerage, AMC) | ADAPT | Use ₹0 only where confirmed (account opening); the rest of the rate card is "to confirm" |
| Three-column fee strip with thin dividers | ADOPT | Clear and scannable; ROOT's charges block reuses it on the Pricing page |
| Pricing hidden or inconsistent across MO pages (no indexed pricing page, conflicting figures) | AVOID | Publish ONE clear pricing page with brokerage, DP charges, AMC and the distribution commission disclosure |
| MO's specific rates (₹20/lot, 0.02%, 0.20%, Value Packs) | BLOCKED | Not ROOT's prices; never use them as placeholders |

## IPO and fund modules (Phase 2)

| Pattern | Call | One-line reason |
|---|---|---|
| IPO hub with open / upcoming / closed / listed lists, mainboard and SME | ADOPT | Same data shape from a vendor IPO module [MO API Map 09-Oct] |
| IPO detail: price band, lot, issue size, timeline, category split, live subscription, objects, financials, peers, lead managers, registrar | ADOPT | Status computed from dates; allotment links out to the registrar |
| Scheme page: NAV + date, NAV chart 1Y to 10Y, returns, AUM, expense ratio, exit load, min SIP, riskometer, managers, portfolio, peers | ADOPT | Regular plans only; peers from the same SEBI sub-category; missing data shows a dash |
| Curated fund collections on the MF hub | ADAPT | Lists curated by Aikyam, regular plans only, never framed as advice |
| Stock pages at scale (5,630), A to Z directory, chart pages | ADAPT | Template B with programmatic SEO, once the market-data licence covers website display. [Fact base 12-Oct] says DEFER |
| Calling MO's APIs, reusing their tokens or data | BLOCKED | Data licensed to MO alone; exchange rules forbid redistribution |
| Browser-side keys in a public JSON file; an extra slug-to-code request on every page | AVOID | Keys on ROOT's server; IDs baked in at build time |
| TradingView charting library | DEFER | Licensed on application; a simple line chart covers Phase 2 |
| Market news feed, search suggestions | DEFER | News needs a licensed feed; search helps once there are many data pages |
| US stocks, Intelligent Advisory Portfolios, own PMS/AMC | BLOCKED | Not offered by ROOT; advisory portfolios need IA/RA registration; Aikyam Wealth only distributes PMS |
| MO data bugs (wrong fund in title, 0% for missing returns, stale "ISSUE OPEN" badge, mojibake, 4-decimal prices, "test" in titles) | AVOID | Each is a ROOT build rule [MO API Map 09-Oct] |

## Partner pages

| Pattern | Call | One-line reason |
|---|---|---|
| `/partner-corner` + "Become a Motilal Oswal Authorised Person" page with eligibility (Indian citizen, 18+, 10+2, market knowledge, infrastructure) and benefits | ADOPT | ROOT: Partner with ROOT, Authorised Person Programme (Capital), Distributor Partner Programme (Wealth), marketing pages + lead form only |
| One local microsite per AP office (stockbroker.motilaloswal.com) | DEFER | Worth it only once 20+ APs exist |
| "Sub-broker" wording | BLOCKED | Category abolished; ROOT says Authorised Person |

## Header, navigation and footer

| Pattern | Call | One-line reason |
|---|---|---|
| Mega-menu with uppercase eyebrows, grouped links, icon tiles | ADAPT | ROOT mega-menus use grouped links, no eyebrow labels, F&O risk line in the Trade menu |
| Footer "Investor Alert" ticker + registration numbers + grievance emails + escalation policy + Important Links | ADOPT | Visible compliance is a trust signal; ROOT adds the two-entity strip and the distributor disclaimer |
| Footer as a wall of pipe-separated links and A to Z directories | AVOID | Group links into labelled columns; move directories to their own page |
| Two apps (investor and trader) | ADAPT | ROOT keeps one app and one Get the App page |
| Manufacturer (AMC) and distributor on separate domains | ADAPT | ROOT is one front for two entities, so entity-tag every page and form |
| Mobile: header logo/search collisions, lazy icons failing | AVOID | Test the 375px header; inline critical icons |

## Platform and performance

| Pattern | Call | One-line reason |
|---|---|---|
| Edge-delivered static pages, mobile PageSpeed reported at 100 (Adobe EDS) | ADOPT | ROOT performance budget proposed at mobile PSI 90+ with five security headers |
| Dev/staging URLs and private IPs left in production bundles | AVOID | Build pipeline strips non-production URLs |

## Tokens measured on MO (for reference only)

Container 1248px; section padding 40px; title gap 24px; grid gap 24px; radius scale 12 / 8 / 4; card shadow `4px 4px 12px rgba(30,51,72,.15), 0 16px 48px rgba(112,144,176,.30)`; breakpoints 600 / 768 / 1024 / 1196; header 120px desktop, 67px mobile. ROOT's own values replace all of these (1200px column, 8px base, radius 16 / 12 / 10 / pill, header 72px, breakpoints 640 / 900 / 1100). [MO UI Teardown 08-Oct], [Theme v1 08-Oct]
