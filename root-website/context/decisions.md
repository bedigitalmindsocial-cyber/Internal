# ROOT by Aikyam: decisions and corrections already made

Compiled 12-Oct-2026. Newest decision wins unless a row says otherwise. Source tags: [Theme v1 08-Oct], [Placeholder Register], [Sitemap v2 sheet], [MO UI Teardown 08-Oct], [MO API Map 09-Oct], [Data Points 09-Oct], [session 06-Sep], [session 09-Sep], [session 16-Sep] (later turn of the 09-Sep session), [Fact base 12-Oct], [CX context doc 18-Sep].

## 1. What ROOT is

- ROOT by Aikyam (rootbyaikyam.com) is one retail brand over two regulated companies. Aikyam Capital Private Limited does broking as its own service (equity, F&O, currency, commodity, IPO). Aikyam Wealth Private Limited distributes mutual funds (AMFI ARN) and third-party PMS. Insurance entity: TO CONFIRM. [Sitemap v2 sheet]
- The design problem is to separate "Trade" (Capital) from "Invest/Protect" (Wealth) without it looking like two websites. [session 06-Sep]
- The theme footer reads "© 2026 Aikyam Capital Private Limited. ROOT is a product of Aikyam Capital Group." [Theme v1 08-Oct]
- Primary conversion is a completed account opening plus an app install. Secondary conversions are partner sign-ups and wealth enquiries. [Fact base 12-Oct, partly inferred]

## 2. Naming rules (locked)

| Use | Never use | Why | Source |
|---|---|---|---|
| Distributor Partner Programme | "Become an IFA", "IFA" | "IFA" is barred as a descriptor for distributors | [CX context doc 18-Sep], [Fact base 12-Oct] |
| Authorised Person (AP) Programme | "Sub-broker", "Sub-broker / Referral Program" | SEBI abolished the sub-broker category in favour of Authorised Person. Using the old word is "disqualifying" | [CX context doc 18-Sep] |
| (no Direct Plans line under Aikyam Wealth) | "Direct Plans", "Direct plans, zero commission" | An ARN-registered distributor cannot deal in Direct Plans. Mutual fund pages show regular plans only | [CX context doc 18-Sep], [MO API Map 09-Oct] "regular plans only" |
| "Empanelled for distribution", "third-party SEBI-registered PMS providers" | Any wording implying in-house PMS | v2 exists to correct a v1 error that presented PMS and Insurance as Aikyam's own | [Sitemap v2 sheet], [session 06-Sep] |
| "Plans across equity, debt and hybrid categories" | "Mutual funds at zero commission" | As a distributor, Aikyam earns commission on regular plans | [Theme v1 08-Oct] |
| "A real person to talk to when you need one" | "A real advisor", "advisor", "adviser" | Implies Investment Adviser registration | [Theme v1 08-Oct] |
| "SEBI-registered broker · INZ000321232", "Backed by Aikyam Capital Group" | Invented investor counts, AUM figures | ROOT is new. Invented counts are a SEBI advertising breach | [Theme v1 08-Oct] |
| "Simple, open, grow" | "Seamless, unlock, elevate" | House style | [Theme v1 08-Oct] |
| "See the full list of charges" | "Click here", "Submit" | Links and buttons say what happens | [Theme v1 08-Oct] |
| "Open free account" (primary, same words in header, hero and footer); "Login" (always secondary) | Two primaries side by side | One primary action per view | [Theme v1 08-Oct] |
| Product actions name the product: "Start a SIP", "Apply for IPO" | Generic labels | | [Theme v1 08-Oct] |
| Trading sub-domain: `trade.rootbyaikyam.com` (client email) | `rootbyaikyam.trading.com` (in v2) | trading.com is an unrelated third-party domain | [session 06-Sep], [Fact base 12-Oct] |
| "Dormant Account Policy" | "Dormat Account Policy" (typo on live site) | Fixed in the delivered build | [Placeholder Register] |

**Product name and tagline: still TO CONFIRM.** The content document says "ROOT by Aikyam" and "Where your wealth begins." The client's launch brief says "ROOT by Aikyam Wealth" and "Where Wealth Begins." [session 09-Sep]. The theme uses "ROOT by Aikyam" and "Where your wealth begins." [Theme v1 08-Oct]. Build with the theme's wording and get it locked in writing.

**Case and punctuation:** sentence case everywhere; Title Case only for product names, written by hand and never via CSS `text-transform`. No em dashes in any copy. [Theme v1 08-Oct], [MO UI Teardown 08-Oct]. The theme hero uses "Trade & invest"; the delivered build had changed this to "Trade and invest" [Placeholder Register]. Minor; pick one.

## 3. Entity tagging

- Every page and form is tagged Aikyam Capital, Aikyam Wealth or Both, and the copy says plainly which company provides each service. [Sitemap v2 sheet], [Fact base 12-Oct]
- Use the Entity & Compliance Map as the reference: Broking = Aikyam Capital ("Stock Broker, NSE/BSE/MCX membership, confirm exact segments"); MF = Aikyam Wealth (AMFI ARN); PMS = Aikyam Wealth (empanelled distributor, NOT in-house); Insurance = TO CONFIRM (IRDAI Corporate Agent or Insurance Broker; may sit under Aikyam Wealth or a separate entity). [Sitemap v2 sheet]
- Known legal-document conflict: the live Terms define "Aikyam / Company / We" as Aikyam Wealth, which attaches broking clauses 10, 11, 13 and 14 to the distributor. The Privacy Policy and homepage footer name Aikyam Capital as the broker. This was deliberately NOT corrected on Giraffe's side; it needs a clause allocating services per entity (Placeholder Q1). [Placeholder Register]

## 4. Header and navigation

**Theme v1 header (the current reference)** [Theme v1 08-Oct]:
- Announcement bar: "Account opening is live. The ROOT app for iOS and Android is coming soon." with "Open a free account".
- Top nav: Invest | Trade | Plan & Tools | Learn | Pricing | About | Help | Login | **Open free account**.
- Invest mega-menu: Mutual funds (Mutual Funds, Fund Explorer, SIP); IPOs (Upcoming IPOs, IPO Calendar & Allotment); ETFs; Coming soon (Insurance, Bonds & Fixed Income, NPS, PMS, each with a "Soon" badge); prompt "Not sure where to start? Try a goal." linking to Plan by goal.
- Trade mega-menu: Equity (Equity, Intraday & Delivery); Derivatives (Futures & Options, Currency & Commodity); Markets (Markets & Indices, Stock pages). It carries the F&O risk one-liner "9 out of 10 individual traders in equity F&O incurred net losses." with "Read the risk disclosure".
- Plan & Tools mega-menu: Calculators (SIP, Lumpsum, Brokerage, Retirement, Margin, SPAN); Planning (Risk Profiler, Retirement Planning, Child Education Planning).
- Header height 72px; mega-menus open on click or hover; Esc and an outside click close them.

Earlier headers, superseded: the content doc's "About us | Products | Support" plus a Login/Register CTA [session 06-Sep]; the v2 nav with 12 sections including Protect and Partner with Us [Sitemap v2 sheet]; and the IA v3 proposal (Trade | Invest | IPO | Pricing | Learn | Partner | Support | Login with three destinations | Open Account) [Fact base 12-Oct]. Partner pages arrive in Phase 3 and have no header slot in the theme.

## 5. Footer

**Theme v1 footer** [Theme v1 08-Oct]:
- Grievance line: "For any grievance or complaint about securities broking: grievances@aikyamcap.com".
- Columns: Products (Mutual Funds, Stocks, F&O, Commodity, ETFs, IPOs) | Support (Grievance Redressal, Investor Complaints, SCORES / ODR Portal, Contact Us) | Important links (Standard KYC Documents, Client Bank Accounts, Key Managerial Persons, Escalation Matrix, RMS Policy, Dormant Account Policy) | Legal (Terms & Conditions, Privacy Policy, Risk Disclosure) | Join our team (Careers, LinkedIn).
- Registration table for Aikyam Capital (see compliance.md), then the Attention investor block, Disclaimer, Caution notice for public, and copyright.
- Carries the note "Footer content awaits Aikyam compliance confirmation." The client's content doc marks the whole regulatory footer "Wait for Confirmation"; it must not go live unapproved (Placeholder Q6). [Placeholder Register]
- The footer stays light; one dark band per page sits above it. [Theme v1 08-Oct]

**Required by Sitemap v2 and not yet met:** a bottom strip with SEBI broker reg. no. + AMFI ARN + exchange membership nos. + registered office + CIN **for both Aikyam Capital and Aikyam Wealth, side by side**. The theme shows only Aikyam Capital, because no Aikyam Wealth number exists in any document. [Sitemap v2 sheet], [session 09-Sep]

**Add to the footer** [Placeholder Register]: Investor Charter for Depository Participant (nsdl.com/investor/investor-charter) and Investor Complaints data for Stock Broking and for NSDL DP. These are on the live site but not in the build. The live site also links an "Investor Charter for Stressed Asset Management"; whether it belongs on ROOT is TO CONFIRM.

Footer columns in v2 (for reference): Company / Invest / Trade / Resources (incl. Glossary) / Legal (Capital Disclosures, Wealth Disclosures, Investor Charter, Grievance Redressal, Privacy/T&C). Adapted from Groww / Zerodha / Upstox for trading plus NJ Wealth / FundsIndia for wealth; these benchmarks apply to the footer only. [Sitemap v2 sheet], [session 09-Sep]

## 6. Onboarding (account opening)

- Account opening is live on the web; the app is "coming soon". [Theme v1 08-Oct]
- Two doors: Start Trading (Aikyam Capital) and Start Investing (Aikyam Wealth, "E-Wealth style account"). Whether this is one flow or two is TO CONFIRM; the v2 note reads "can be same or separate flow, confirm UX". [Sitemap v2 sheet]
- Template D: logo only, no menu, sticky form on the right, fully online. [Theme v1 08-Oct]
- Indicative four steps: (1) mobile number + OTP, (2) verify PAN, (3) Aadhaar via DigiLocker, (4) link bank and e-sign. Keep ready: PAN, Aadhaar linked to mobile, bank details, a photo of your signature. Caption: "Steps shown are indicative and will be confirmed with the KYC partner's live flow." [Theme v1 08-Oct]
- Under every form: "You will continue to our secure KYC partner to verify your PAN and Aadhaar. Activation is subject to KYC verification and exchange approval." [Theme v1 08-Oct]
- Mobile + OTP as step 1, so that drop-offs become callable leads (Motilal pattern, ADOPT). [Fact base 12-Oct]
- KYC vendor: the content doc points the CTA at both `uat.rootbyaikyam.com/login` and `aikyamcapital.1kyc.finovo.tech` (Finovo 1KYC). Nobody has decided which one a new user hits. [session 09-Sep]
- Login moves from `uat.rootbyaikyam.com/login` to `trade.rootbyaikyam.com/login` at go-live. The UAT link on the live site must be replaced. [session 06-Sep], [Fact base 12-Oct]
- Consent is never pre-ticked (DPDP Act). [Theme v1 08-Oct], [MO UI Teardown 08-Oct]
- The client also asked for a redesign of the Login page and the e-KYC page (`ekyc.rootbyaikyam.com`). Both are vendor-built React SPAs, so KYC screen order may allow theming only. Design-only vs implementation is TO CONFIRM. [session 06-Sep]

## 7. Launch phasing and "Coming soon"

| Phase | Pages | Date | Source |
|---|---|---|---|
| 1 | 25 | live 2 Nov 2026 | [Theme v1 08-Oct] |
| 2 | 25 (data pages) | live 8 Dec 2026 | [Theme v1 08-Oct], [MO API Map 09-Oct] |
| 3 | 23 | 13 Jan 2027 | [Theme v1 08-Oct] |

- Superseded: go-live 20-Oct-2026 (itself an NSE holiday), with a content freeze around 9-Oct because the compliance officer classified launch creatives as advertisements needing exchange filing. [Fact base 12-Oct] citing [CX context doc 18-Sep]
- "Coming soon": the ROOT app on iOS and Android (store buttons disabled with a "Coming soon" badge; QR code "will appear here at launch"); Insurance (4 pages), Bonds & Fixed Income, NPS, PMS (4 pages) as Template H CMS drafts "until each product is cleared to launch". [Theme v1 08-Oct]
- Insurance, Bonds and NPS: "build all, gated behind compliance sign-off" (user decision). [session 09-Sep]
- Compliance gates live in code as booleans: `PRICING_APPROVED = false`, `APP_LIVE = false`. Device detection for the app stores is written but dormant. [Placeholder Register], [session 06-Sep]
- The "Tell me when it's live" promise has no form or backend yet. Either build one or soften the promise (Placeholder Q12). [Placeholder Register]

## 8. Pricing

- One clear, public pricing page: brokerage, DP charges, AMC and the distribution commission disclosure. Transparency is where a new broker can beat Motilal Oswal. [Fact base 12-Oct]
- Theme layout: "₹0" account-opening numeral, then a charges table whose cells read "Rate card to confirm" until approved, then "See the full list of charges". Line: "Brokerage will never exceed the limits prescribed by SEBI." [Theme v1 08-Oct]
- Drafted figures exist in the delivered homepage source behind `PRICING_APPROVED = false`. They are NOT approved; do not publish them (Placeholder Q7). [Placeholder Register]

## 9. Content, scope and build decisions

- Giraffe writes all marketing copy; the client supplies legal and regulatory text and clears it for SEBI/AMFI/IRDAI. [session 09-Sep] (user's answer)
- Partner with Us: marketing pages + lead form only, no partner portal build. [session 09-Sep] (user's answer)
- Technical SEO is built in; ongoing content production is not part of the build. [session 09-Sep] (user's answer)
- Stack, per the client's scope deck: Next.js / React front end, a custom Node.js CMS (user decision: build it as specified), CRM integration (tied to Finovo / the KYC vendor), an interactive prototype with micro-interactions, training and a QA tester. [session 16-Sep]
- The theme tokens go "into the Next.js theme. Components reference these names only, never raw hex values." [Theme v1 08-Oct]
- Hosting: Next.js plus a Node CMS cannot run on the static cPanel hosting the current homepage uses. It needs a Node runtime and a database. TO CONFIRM with the client's tech team. [session 16-Sep]
- Technical gate before any traffic: five security headers, robots.txt and sitemap.xml returning 200 (both returned HTTP 500 on 18-Sep), no staging/UAT links in production, regulatory disclosures placed and version-stamped. [CX context doc 18-Sep], [Fact base 12-Oct]
- Proposed, not agreed: mobile PageSpeed 90+; GA4 events account_start, otp_verified, kyc_submitted, app_install_click, partner_lead, wealth_lead; north-star metric = funded accounts. [Fact base 12-Oct]
- The live rootbyaikyam.com is an earlier or partial variant of the delivered homepage (no pricing, no announcement bar, no research/comparison section). Confirm who controls that deployment before uploading (Placeholder Q15). [Placeholder Register]

## 10. Phase 2 data pages

- Data comes from a licensed vendor through ROOT's own server `/api`, never the browser. Vendor keys stay on the server. [MO API Map 09-Oct]
- Never call Motilal Oswal's endpoints or copy their data. Use the map as a spec only. [MO API Map 09-Oct]
- Store ISIN / AMFI code / vendor code / NSE symbol / BSE code with each page at build time. [Data Points 09-Oct], [MO API Map 09-Oct]
- Every number shows its as-on date and the data source/vendor name. Missing values show as a dash, never 0%. IPO status is computed from dates. Peers come from the same SEBI sub-category. Prices to 2 decimals. Lots are whole numbers. Text is stored as UTF-8. Trim option chains to traded strikes. [MO API Map 09-Oct]
- Cache to each item's real refresh rate: NAV and fundamentals daily; shareholding quarterly; IPO subscription several times a day; prices as often as the licence allows. [MO API Map 09-Oct], [Data Points 09-Oct]
- NAV comes from AMFI's free daily NAV file. Portfolio, ratings, managers and expense ratio come from the MF data vendor. Allotment status links out to the registrar. [MO API Map 09-Oct]
- 108 data points across 7 categories, plus 5 optional. Optional and later: search suggestions, market news (needs a licensed feed), buy/sell recommendations (needs SEBI RA registration, so BLOCKED), TradingView advanced charts (needs a licence; a simple line chart covers Phase 2), US stocks (not offered). [Data Points 09-Oct]
- Open: which feed the ROOT app already uses; live vs delayed prices (live needs an exchange data licence); a licence that explicitly covers website display. [MO API Map 09-Oct]
- Curated fund lists are Aikyam's choice ("When Aikyam updates"). [Data Points 09-Oct]

## 11. Brand and visual decisions

- Palette from the ROOT logo files: aubergine `#1C0F2F` does the work; gold `#C19C2F` is a spark only (mark, root line, nodes, one icon detail), never text, buttons or surfaces (gold on white is 2.6:1). Brand gradient `#1C0F2F` to `#0C2229`, from the app icon: one dark band per page, footer stays light. [Theme v1 08-Oct]
- Client feedback, 10-Aug: "In phone the dark color is coming out as black ... It should not be perceived as black. We should avoid usage of black." This is a standing brand constraint. [session 09-Sep]
- Type: Tiro Devanagari Hindi (headings) + Mukta (everything else) + Red Hat Mono (registration codes). Both families are Indian multi-script, so Hindi pages match later. [Theme v1 08-Oct]
- Logo files are used exactly as supplied. No stock photos of traders at monitors. Product screens are always captioned "Illustrative" and use example names (Example Bank Ltd), never real tickers with invented prices. Real Aikyam people only, after shoots; customers only with written consent. [Theme v1 08-Oct]
- Motion: calm and short. Not allowed: pulsing CTAs, counting-up numbers, parallax, scroll-jacking, confetti, bouncing springs. Everything stops for reduced-motion users. [Theme v1 08-Oct]
- Aikyam Group gold rule: the theme notes that gold buttons and gold text "conflict with the Aikyam Group gold rule". [Theme v1 08-Oct]
