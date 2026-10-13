# ROOT by Aikyam: website fact digest

Non-confidential digest of the 12-Oct-2026 fact base, limited to what a page designer or copywriter needs.
Commercial terms, contract status and internal stakeholder notes are deliberately left out.
The full fact base is in `private/` (gitignored). Tags: [DOC] internal document, [WEB] public page, [INFERRED] reasoning, [TO CONFIRM] open.

## 1. What ROOT is
- ROOT by Aikyam (rootbyaikyam.com) is the retail brand of the Aikyam Capital Group. One retail front over two regulated companies:
  - **Aikyam Capital Private Limited**: stock broking (equity, F&O, currency, commodity, IPO). NSE, BSE, MCX (and MSEI per theme v1) member, NSDL depository participant. [DOC]
  - **Aikyam Wealth Private Limited**: mutual fund distribution (AMFI ARN), distribution of third-party PMS, insurance later (licensing entity TO CONFIRM). [DOC]
- Name meaning: Aikyam (Sanskrit) means oneness and togetherness in the investment life cycle. "Root" suggests growth from a base. Theme tagline in the footer: "Where your wealth begins." [DOC]
- The ROOT app exists for iOS and Android (store names and install counts TO CONFIRM). The parent site aikyamcap.com hands retail traffic to ROOT. [DOC]
- The group is institutional in origin (institutional broking and clearing, investment banking, stressed assets, GIFT City funds). Retail is new. ROOT has no retail scale numbers yet: never invent any. [DOC]

## 2. Business objective [INFERRED, agreed working version]
Turn Aikyam's institutional licences into a retail and wealth franchise: acquire retail investors and traders (app plus web), open accounts under the right entity, cross-sell mutual funds, distributed PMS and later insurance. Partners (Authorised Persons, distributors) are a second acquisition engine. The client's board watches app downloads and funded accounts.

North-star metric: funded accounts (account opened AND first trade or first SIP).
Funnel: session > mobile captured > OTP verified > KYC submitted > account active > funded.

## 3. Users (codes used in sitemap.json)
| Code | Who | Entity |
|---|---|---|
| U1 | New and first-time investors: simple account, SIPs, guidance | Wealth (MF), Capital (demat) |
| U2 | Active traders: intraday, delivery, F&O, currency, commodity; care about brokerage, platform, margin | Capital |
| U3 | IPO applicants: upcoming IPOs, calendar, allotment | Capital |
| U4 | Goal planners: retirement, child education, tax saving | Wealth |
| U5 | HNIs, families, professionals, business owners: distributed PMS, AIF, fixed income, a real person to talk to | Wealth |
| U6 | Partners: mutual fund distributors (Distributor Partner Programme) and Authorised Persons | Wealth / Capital |
| U7 | Existing clients: login, client desk, tickets, grievance routes | Both |
| U8 | Insurance buyers (Coming soon) | TO CONFIRM |
| U9 | Diligence readers: compliance officers, exchanges, partners, media checking licences and disclosures. Few, decisive for trust | Both |
| Talent | Job seekers (Careers) | Group |

Not ROOT audiences: FPIs, institutions, lenders, ARCs, fund LPs. They stay on aikyamcap.com.

## 4. Tasks people come to do
T1 open an account (Start Trading: Capital; Start Investing: Wealth) · T2 log in (trading platform, client desk, partner desk) · T3 download the app · T4 check costs (brokerage and charges; distribution commission disclosure) · T5 explore and start (fund explorer, SIP, IPO list and allotment) · T6 plan and calculate (calculators, risk profiler) · T7 learn (guides, glossary) · T8 become a partner · T9 get help (FAQs, tickets, contact) · T10 verify and complain (disclosures, investor charter, grievance, SCORES, ODR, policies).

## 5. Conversions
- Primary: account opening started with mobile number + OTP (the Motilal pattern: drop-offs become callable leads), completed KYC.
- Co-primary: app install (store badges, QR, SMS link).
- Secondary: partner application; wealth enquiry (PMS/AIF/fixed income, "Talk to the wealth team"); callback request; "Tell me when it is live" sign-ups on Coming-soon pages.
- Service (not acquisition): ticket raised.
- Every form names the company that receives the data (Aikyam Capital or Aikyam Wealth).

## 6. Information architecture (agreed direction: "Motilal skeleton at ROOT scale")
- Account-first front door: "Open free account" is the hero action and the sticky header CTA; step 1 is mobile + OTP.
- Header: logo | Invest | Trade | Plan & Tools | Learn | Pricing | About | Help | Login | [Open free account]. Mega menus as in theme v1.
- Entity-tag every page and every form; say plainly which company provides each service.
- One ROOT app (not two). One clear, published pricing page (transparency is where a new broker can beat Motilal Oswal).
- Footer: product, company, support, important-links and legal columns; registration strip for BOTH entities; Attention Investors; disclaimers; caution notice.
- Deferred until licences or data exist: live stock quote pages at scale (market-data licence), research and stock ideas (needs SEBI RA registration), NRI accounts (needs PIS bank tie-up), US stocks, algo/API. Stock Detail and Markets pages are designed with clearly labelled illustrative data.

## 7. Motilal Oswal: what transfers (copy the machine, not the claims)
ADOPT: account-first hero and sticky CTA with mobile + OTP; separate onboarding host; paid landing pages (noindex, one per campaign, each exchange-filed); learning centre with evergreen yearly pages and "how to apply for {IPO} on ROOT" articles; calculator suite; AP recruitment pages; footer Investor Alert + registration numbers + grievance emails + escalation policy + Important Links; performance budget (mobile PageSpeed 90+).
ADAPT: one app page instead of two apps; trust strip of checkable institutional facts (Member NSE, BSE, MCX; registration numbers; part of Aikyam Capital Group; leadership experience) instead of client counts and awards; ROOT's own brand line.
IMPROVE ON MO: publish one clear pricing page.
BLOCKED: "award winning research", free research reports, stock ideas, model portfolios, Intelligent Advisory Portfolios, own PMS or AMC (Aikyam only distributes PMS: "empanelled for distribution").
DEFER: stock quote pages at scale, NRI.

## 8. Compliance traps already caught (apply on every page)
- "Direct plans, zero commission" on the ARN distributor entity: not allowed. Aikyam Wealth earns commission on regular plans.
- "Become an IFA": IFA is barred as a descriptor for distributors. Use "Distributor Partner Programme".
- "Sub-broker / Referral Program": category abolished. Use "Authorised Person (AP) Programme".
- PMS is distributed, never "in-house": say "empanelled for distribution"; SEBI PMS minimum investment is ₹50 lakh (a 2026 consultation on a lower MF-only PMS minimum is not law).
- "AI-led research advisory", "investment recommendations", "advisor": imply RA/IA registration that no Aikyam entity is known to hold [TO CONFIRM]. Do not use.
- Launch creatives count as advertisements and are filed with each exchange (NSE, BSE, MCX) before use. Every page is a draft until compliance approves.
- Proprietary-trading disclosure applies to Aikyam Capital and belongs on broking pages / footer.
- SEBI requires the F&O risk disclosure ("9 out of 10 individual traders...") wherever F&O is promoted.
- Distributor disclaimer for MF, IPO and bonds: "not exchange traded products"; disputes on distribution have no access to exchange redressal or arbitration.

## 9. Registration data in theme v1 (footer strip; theme marks the footer "awaits Aikyam compliance confirmation")
Aikyam Capital Private Limited · SEBI registration INZ000321232 · CIN U67100MH2022PTC394087 · Depository participant IN-DP-854-2026, NSDL DP IN305066 · Exchange membership BSE 6899, NSE 90419, MCX 8136, MSEI 80750 · Clearing BSECL 6899, NCL M70106, MCXCCL 8135 · GST 27AAXCA9480C1Z5.
Aikyam Wealth: AMFI ARN, CIN, insurance licence: TO CONFIRM (render as `<mark class="ph">` placeholders).
Company contact (public): Registered office 1203, Level 12, Lotus Link Square, D.N. Nagar, Andheri (W), Mumbai 400053; Corporate office 1704, Level 17, same building; +91 22 6975 2600; info@aikyamcap.com; grievances@aikyamcap.com.

## 10. Public leadership (from the corporate profile; use titles as written, bios only from approved text)
Nilesh Choudhary (Founder and Director), Navnit Choudhary (Co-founder), Anand Mody (Group COO; compliance officer per old footer), Vishal Goraddia (Managing Partner, Asset Management), Vishal Trehan (Head India Sales and COO Broking and Clearing), Manoj Shetty (Managing Partner, Capital Markets), Manoj S Pawar (Chief Business Officer / Head Wealth Management), Parth Dalal (VP Wealth Management), Pallavi Desai (Head Client Relations), Kunal Rathi (Head Investment Banking, M&A), Prashant Lad (Head of Technology), Adita Talreja (Group Company Secretary). Photos: placeholders.

## 11. Open questions that affect page design (owners: client)
Q4 registration numbers for both entities and grievance officers · Q5 insurance entity and licence type (Protect stays "Coming soon") · Q6 are bonds / fixed income and NPS actually distributed · Q7 one onboarding flow or two; KYC vendor; production login URLs · Q8 the brokerage plan(s) to publish; whether trail commission must be disclosed · Q9 does any Aikyam entity hold RA or IA registration · Q11 app store names, install count, deep-link vs web onboarding.
