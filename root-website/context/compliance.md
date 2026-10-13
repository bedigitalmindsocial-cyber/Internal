# ROOT by Aikyam: compliance rules for copy and layout

Compiled 12-Oct-2026. This is not legal advice. Every line still needs sign-off from Aikyam's compliance officer before publication. Source tags: [Theme v1 08-Oct], [Placeholder Register], [Sitemap v2 sheet], [CX context doc 18-Sep] (Giraffe's internal regime table, which says to "confirm every line with the client's counsel"), [Fact base 12-Oct], [MO UI Teardown 08-Oct], [MO API Map 09-Oct], [Data Points 09-Oct], [session 09-Sep].

## 1. Forbidden words, devices and claims

### Claims and proof
- No invented numbers: investor counts, AUM, "trusted by lakhs", client counts, years, awards. "ROOT is new. Invented counts are a SEBI advertising breach." Prove the parent instead ("Backed by Aikyam Capital Group"). [Theme v1 08-Oct]
- Honesty constraints for a SEBI intermediary's site: no fabricated proof, no borrowed regulator logos, no scale stats, no testimonials, no uptime or latency claims, no urgency mechanics. [CX context doc 18-Sep]
- Broking hard prohibitions: incentives for account opening, contests, return claims. [CX context doc 18-Sep]
- No figure computed by Giraffe. Any performance figure must be the client's, signed by the client. [CX context doc 18-Sep]
- Still to back up or drop: "Bank-grade security", "Fast, reliable execution", "Institutional-grade research" / "Open-architecture research" (all appear in client copy and in the theme homepage pillars). [Theme v1 08-Oct]
- Avoid "superlative or unverified" claims anywhere near PMS (SEBI directed portfolio managers to strip them, June 2025). [CX context doc 18-Sep]

### Advice and research language (no RA or IA registration is known for any Aikyam entity)
- House rule where a group holds no adviser or analyst registration: no advice or research language. This includes the words **advisor, adviser, investment advice, research report, target price, buy / sell / hold**, and it applies in alt text, aria-labels and HTML comments too. [CX context doc 18-Sep]
- No stock ideas, model portfolios, "AI-led research advisory" or "investment recommendations" until Compliance officer confirms whether any entity holds a SEBI Research Analyst (INH) or Investment Adviser (INA) registration. [Fact base 12-Oct]
- Note the conflict: the theme homepage pillar reads "Open-architecture research: Institutional-grade research from Aikyam Capital Group". That breaks the house rule above unless an RA registration is confirmed. TO CONFIRM.

### Mutual fund distribution (Aikyam Wealth, AMFI ARN)
- Never offer **Direct Plans** on the ARN-registered distributing entity. [CX context doc 18-Sep]
- Never use the label **"IFA"**. Use "Distributor Partner Programme". [CX context doc 18-Sep]
- Never omit the ARN. It must be displayed. [CX context doc 18-Sep]
- Never say "zero commission" for mutual funds. [Theme v1 08-Oct]
- Regular plans only in fund lists and data. [MO API Map 09-Oct], [Data Points 09-Oct]
- AMFI is an industry association, not a regulator. Distribution content is built to the AMFI code and says so. [CX context doc 18-Sep]

### PMS (distributed, third-party)
- Never describe third-party empanelled PMS as an in-house product. Copy must say "empanelled for distribution" and "third-party SEBI-registered PMS providers". [Sitemap v2 sheet], [CX context doc 18-Sep]
- SEBI PMS minimum is ₹50 lakh. A 23-Jul-2026 SEBI consultation proposes an MF-only PMS at ₹25 lakh; this is "Not law" and must not be published as if it were. [Fact base 12-Oct]
- Whether strategy performance may appear, in what format and against which APMI benchmark, is TO BE VERIFIED with the compliance officer before any performance page is scoped. [CX context doc 18-Sep]

### Broking terms
- Never write "sub-broker". Use "Authorised Person". [CX context doc 18-Sep]

### Insurance
- Build nothing that makes claims before the IRDAI licence class is confirmed. Corporate Agent and Insurance Broker are different permissions with different claims. Pages stay as Template H drafts. [CX context doc 18-Sep], [Theme v1 08-Oct]

### AIF
- If AIFs ever appear: firm, philosophy, people and process only. Nothing at scheme level. Private placement, ₹1 crore minimum. No assured or indicative returns, and no fund size, tenure, hurdle or carry terms on a public page. [CX context doc 18-Sep]

### Devices and UX
- No pre-ticked consent (DPDP Act); consent is an active opt-in. [Theme v1 08-Oct], [MO UI Teardown 08-Oct]
- No pulsing CTAs and no counting-up numbers. [Theme v1 08-Oct]
- Illustrative screens are always captioned "Illustrative" and use example names, never real tickers with invented prices. Market data blocks on design pages state "All market data in this block is illustrative." [Theme v1 08-Oct]
- Status is never shown by colour alone. [Theme v1 08-Oct]
- No em dashes in copy (house style). [Theme v1 08-Oct]

### Advertisements and exchange filing
- Every creative and every paid landing page that counts as an advertisement is filed with **each exchange Aikyam Capital is a member of** (NSE, BSE, MCX and, if relevant, MSEI) under SEBI's advertisement code for stock brokers. The compliance officer confirms the window each time; Giraffe does not publish a day count. [CX context doc 18-Sep]
- Purely factual communication (name, logo, address, contact) sits outside the approval requirement. Authorised Persons' material and social media sit inside it. [CX context doc 18-Sep]
- Paid landing pages: `/lp/{campaign}`, noindex, one per ad set, each exchange-filed before launch. [Fact base 12-Oct] (proposal)
- The SEBI Common Advertisement Code consultation (comments closed 14-Jul-2026) is "Not law". Do not design around it until it is notified. [CX context doc 18-Sep]

## 2. Mandatory disclosures and where they sit

| Disclosure | Placement | Wording source | Status |
|---|---|---|---|
| **F&O risk disclosure** ("Risk disclosures on derivatives": 9 out of 10 individual traders in equity F&O incurred net losses; average loss close to Rs. 50,000; loss makers spent an additional 28% of net trading losses as transaction costs; profit makers spent 15% to 50% of profit as transaction cost) | On every F&O page, never collapsed. Also a one-liner with a "Read the risk disclosure" link in the Trade mega-menu and on the F&O product card | [Theme v1 08-Oct] | Text, figures, font size and placement must be pulled **from the current SEBI circular at the start of every build**, version-stamped in the repo, re-checked at go-live, rendered in the initial HTML, never behind a "read more" and never overlapped by a sticky element [CX context doc 18-Sep]. Confirm the current text with compliance |
| **Two-entity regulatory strip**: SEBI broker reg. no. + AMFI ARN + exchange membership nos. + registered office + CIN, for Aikyam Capital AND Aikyam Wealth, side by side | Footer bottom strip, every page | [Sitemap v2 sheet] | Aikyam Wealth numbers missing (TO CONFIRM) |
| **Attention investor** block (update mobile/email with your broker; KYC is a one-time exercise; no need to issue cheques for IPOs, sign to authorise the bank) | Footer, every page | [Theme v1 08-Oct] (from client content doc) | Two "Click Here" links still unresolved: CDSL/NSDL e-voting URL and vernacular client registration documents URL [Placeholder Register Q13] |
| **Disclaimer** (website for general information only; not an offer, solicitation, advice or recommendation; "Investment in securities market are subject to market risks, read all the related documents carefully before investing.") | Footer, every page | [Theme v1 08-Oct] | Footer awaits compliance sign-off |
| **Caution notice for public** (fraudulent persons claiming association via WhatsApp groups and similar; receipts only in the name of Aikyam Capital Private Limited in designated bank accounts) | Footer, every page; also a Notices page (G) | [Theme v1 08-Oct] | Footer awaits compliance sign-off |
| **Grievance line**: "For any grievance or complaint about securities broking: grievances@aikyamcap.com" | Footer top | [Theme v1 08-Oct] | Which email leads is TO CONFIRM (Placeholder Q8) |
| **Grievance Redressal / SCORES / ODR** | Own G page; footer Support column links: Grievance Redressal, Investor Complaints, SCORES / ODR Portal | [Sitemap v2 sheet], [Theme v1 08-Oct] | |
| **Escalation matrix** (4 levels: Customer Care, Head of Customer Care, Compliance Officer, CEO; Mon to Fri 9:30 AM to 6:00 PM IST) and **Key Managerial Persons** | Own G page + footer Important links + PDFs | [Placeholder Register] (Escalation Matrix PDF) | Phone/email table in placeholders.md |
| **Investor Charter**: Stock Broker; Depository Participant (NSDL link); MF Distributor | Disclosures & Investor Charter G page; footer Legal | [Sitemap v2 sheet], [Placeholder Register] | MF Distributor charter source TO CONFIRM |
| **Investor Complaints data**: Stock Broking and NSDL DP | Footer + Disclosures page | [Placeholder Register] (on live site, not yet in build) | Add |
| **Important links PDFs**: Account Opening Form (KYC), Client Bank Details, KMP, Escalation Matrix, RMS Policy, Dormant Account Policy, Standard KYC Documents | Footer Important links column; Policies / Bank Accounts / Escalation pages | [Placeholder Register], [Theme v1 08-Oct] | Live paths are in placeholders.md |
| **Proprietary trading disclosure** ("Aikyam Capital Pvt. Ltd. is engaged in client based and proprietary trading ..." per SEBI/MRD/SE/Cir-42/2003, with compliance officer details) | Broking pages and footer | [Fact base 12-Oct] (old aikyamcap.com footer) | Recommended; wording TO CONFIRM |
| **Distributor disclaimer** (MF, IPO and bonds are not exchange-traded products; the member acts only as distributor; such disputes have no access to exchange redressal or arbitration) | Footer and MF/IPO pages | [Fact base 12-Oct] (Motilal pattern, recommended) | Recommended; wording TO CONFIRM |
| **SEBI no-guarantee line** ("registration granted by SEBI ... and certification from NISM in no way guarantee performance of the intermediary or provide any assurance of returns to investors") | Footer | [Fact base 12-Oct] (Motilal pattern, recommended) | Recommended; wording TO CONFIRM |
| **Distribution Fee / Commission Disclosure** | Own G page, Phase 2 (Aikyam Wealth) | [Sitemap v2 sheet] "check compliance requirement" | Whether trail commission disclosure is required is TO CONFIRM |
| **PMS Eligibility & Minimum Investment** (standard SEBI PMS ticket-size disclosure) | Own page, Phase 3 draft | [Sitemap v2 sheet] | |
| **Insurance licence details** | Aikyam Wealth disclosures | [Sitemap v2 sheet] | Pending the licence |
| **KYC partner notice** | Under every account-opening form | [Theme v1 08-Oct] | |
| **Brokerage cap line**: "Brokerage will never exceed the limits prescribed by SEBI." | Pricing block / page | [Theme v1 08-Oct] | |
| **Calculator disclaimer**: illustrative; assumes a constant return; "Mutual fund returns are not guaranteed." | Under every calculator | [Theme v1 08-Oct] | |
| **Market data block**: "Past performance does not guarantee future returns." plus vendor name and last-update time | Every data block | [Theme v1 08-Oct], [MO API Map 09-Oct] | |
| **Riskometer (SEBI)** | Every scheme detail page | [Theme v1 08-Oct], [Data Points 09-Oct] | |
| **Legal page stamps**: version, effective date, last updated | Top of every G page (d2 + last updated date) | [Theme v1 08-Oct], [Placeholder Register Q2, Q3] | Dates TO CONFIRM |

Also: remove any internal review notes from the published policy documents before publishing (Placeholder Q5). [Placeholder Register]

## 3. Registration and identity data

### Aikyam Capital Private Limited (broking)

| Item | Value | Source | Status |
|---|---|---|---|
| SEBI stock broker registration | INZ000321232 | Live Privacy Policy and homepage footer [Placeholder Register]; content doc [session 09-Sep]; theme [Theme v1 08-Oct] | **CONFIRMED** (in published client documents) |
| CIN | U67100MH2022PTC394087 | Client content doc footer [session 09-Sep]; theme | Client-supplied; footer sign-off pending |
| GST | 27AAXCA9480C1Z5 | Client content doc [session 09-Sep]; theme | Client-supplied; footer sign-off pending |
| Depository participant | IN-DP-854-2026; NSDL DP ID IN305066 | Client content doc [session 09-Sep]; theme | Client-supplied; footer sign-off pending. DP licence date TO CONFIRM [Fact base 12-Oct] |
| Exchange memberships | BSE 6899 · NSE 90419 · MCX 8136 · MSEI 80750 | Client content doc [session 09-Sep]; theme | Client-supplied; "confirm exact segments" [Sitemap v2 sheet] |
| Clearing memberships | BSECL 6899 · NCL M70106 · MCXCCL 8135 | [Theme v1 08-Oct] | Client-supplied; footer sign-off pending |
| Registered office | 1203, Level 12, Lotus Link Square, Near D.N. Nagar Metro Station, D. N. Nagar, New Link Road, Andheri (W), Mumbai 400053 | Escalation Matrix, website, Terms revision [Placeholder Register] | **CONFIRMED** |
| Corporate office | 1704, Level 17, Lotus Link Square (website, Escalation Matrix) vs 410, B Wing, Knox Plaza, Chincholi Bunder Road, Malad West, Mumbai 400064 (Terms revision) | [Placeholder Register] | **CONFLICT**. Likely Knox Plaza = Aikyam Wealth, Lotus Link = Aikyam Capital. TO CONFIRM (Q10) |
| Compliance officer | Compliance officer (Escalation Matrix Level 3; also Group COO per the corporate profile) | [Placeholder Register], [Fact base 12-Oct] | Name confirmed in published matrix |
| LinkedIn | linkedin.com/company/aikyam-capital-private-limited/ | [Placeholder Register] | Confirmed |

Not for ROOT, but on record: Aikyam Capital Management LLP is a Co-Investment Portfolio Manager under SEBI Registration No. INP000010025 (aikyamcap.com copy brief). That is a different entity; ROOT distributes third-party PMS. [Fact base 12-Oct]

### Aikyam Wealth Private Limited (distribution)

| Item | Value | Status |
|---|---|---|
| AMFI ARN | none in any document | **TO CONFIRM** (Placeholder Q4) |
| CIN | none | **TO CONFIRM** |
| Registered office | none (Knox Plaza is possibly its corporate office) | **TO CONFIRM** |
| PMS empanelments (which managers) | none | **TO CONFIRM** |
| Insurance licence (entity, IRDAI class, number) | none | **TO CONFIRM** |
| RA / IA registration (any entity) | none found | **TO CONFIRM** |

## 4. Open compliance items (owner: Compliance officer unless noted)

1. Clause in the Terms allocating services per entity. The Terms currently bind Aikyam Wealth to broking clauses 10, 11, 13 and 14 (Q1).
2. Sign-off on the regulatory footer marked "Wait for Confirmation" (Q6).
3. The compliance phone conflict: the Terms revision gives +91 22 6975 2600, which the Escalation Matrix lists against the CEO; the Compliance Officer's line is +91 22 6975 2604.
4. Aikyam Wealth ARN, CIN and office; the insurance entity and class; whether Bonds/FI and NPS are distributed (Wealth business head, Chief Business Officer Wealth); PMS empanelment list.
5. Whether trail commission / distribution fee disclosure is required on Pricing.
6. Whether any entity holds RA or IA registration. This decides "research" wording and any recommendations.
7. The current SEBI F&O risk disclosure text and version.
8. The exchange-filing window for launch creatives and paid landing pages.
9. Claims to back up or drop: bank-grade security, fast execution, institutional-grade research.
10. Terms version, effective and last-updated dates; Privacy Policy effective date; removal of internal review notes.
