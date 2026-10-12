---
page: 09-start-trading
title: Start Trading
url: /open-account/trading
template: D
mode: golden
entity: Capital
status: reviewed
version: 4
updated: 12-Oct-2026
---

## 1. Job
This page exists so that a trader or first-time investor who has decided to open an account can see exactly which account they are opening (trading and demat, with Aikyam Capital Private Limited), what it costs, what KYC involves and what F&O needs, and start with their mobile number and an OTP, and leaves ready to complete KYC with Aikyam Capital's KYC partner.

Golden page for template D: 10 Start Investing, 11 Get the App, 74 Login and 75 Paid landing page inherit its section layouts (see 6.6).

## 2. Journey
- Arrives from: the "Open free account" button in the full header, hero and footer of every Capital and Both page (Home, Trade, Pricing, Equity, F&O, Currency and Commodity, IPO, About); the mobile bar of those pages; Home's hero lead bar (the number is carried over, see the OTP-sent state in 6.2); Google ("open trading and demat account online", "open demat account online", "open trading account"); aikyamcap.com's handoff to ROOT. Paid campaigns go to 75 /lp/open-account, not here.
- Awareness level: product-aware to ready to act. They chose to open an account; they now check that ROOT is a real broker, what it costs and what the process asks of them.
- Stage: Act.
- Previous page / next page(s): previous `/` (Home), `/trade`, `/pricing`, `/trade/futures-options`. Next: the OTP-sent state on this page, then the KYC partner's flow (host TO CONFIRM: ekyc.rootbyaikyam.com or the vendor URL), then `{{url.login}}` once the account is active. Side door: `/open-account/investing` (Aikyam Wealth) for visitors who only want to invest.
- Success:
  - Primary action: "Get OTP" (form submit in `#s-open`, marked `data-primary`, the only one on the page). Event `account_start` on a valid submit; downstream `otp_verified` and `kyc_submitted` fire on the KYC host.
  - Secondary action (at most one): "Investing only? Open an investing account with Aikyam Wealth" link to `/open-account/investing`. Event to define (proposed `switch_to_investing`).
  - Utility, not counted: Login in the minimal header.
- Search: query "open trading and demat account online". Title "Open a trading and demat account online | ROOT by Aikyam" (56 characters). Description "Open a trading and demat account with Aikyam Capital Private Limited, a SEBI-registered broker. Start with your mobile number and an OTP." (138 characters).

## 3. Users and their anxieties
**U2 Active traders** (primary; intraday, delivery, F&O, currency, commodity)
1. "What will I actually pay per order, brokerage plus all the other charges?"
2. "Can I get F&O switched on, and what proof will they ask for?"
3. "ROOT is new. Is this a real, registered broker I can check, or an app that disappears?"

**U1 New and first-time investors**
1. "Will this take long and ask for documents I don't have to hand?"
2. "If I type my number, will I start getting sales calls?"
3. "What if Aadhaar or PAN fails halfway? Do I lose everything, and is my data safe with them?"

Also reading this page: U9 diligence readers (Aikyam compliance treats it as an advertisement draft; exchanges may see it with filings).

## 4. Questions this page answers
Ordered as the visitor asks them (judge reorder: cost now comes before the form questions, and the app question follows "how long"). Page order follows this order with three exceptions: (a) the F&O risk box (14) sits second on the page, directly after the hero, for compliance (see 6.4); (b) 17 (activation and where to log in) is answered at the end of s-steps, so it comes before the charges and F&O questions 12 to 16, because it closes the process block; (c) 18 (NRI, joint and company accounts, SHOULD) is answered only in s-faq, after s-fo. Question 11 is answered visibly in s-steps (third docs strip) directly after question 10, and repeated in FAQ 2. The quoted words are the answering copy the builder keeps (wording may be polished; facts and section ids stay).

| # | Question (in the visitor's words) | MUST/SHOULD | Source | Answered in section: "answering words" |
|---|---|---|---|---|
| 1 | Which account am I opening here: trading and demat with Aikyam Capital, investing with Aikyam Wealth, or both? | MUST | Mandatory, account opening | s-hero: "A trading and demat account with Aikyam Capital Private Limited, the SEBI-registered stock broker behind ROOT by Aikyam" (side door under the form card: "Investing only? Open an investing account with Aikyam Wealth"); s-faq: "Investing accounts are opened by Aikyam Wealth Private Limited on the Start Investing page" |
| 2 | ROOT is new to me. Is it a registered broker I can check myself? | MUST | Page-specific: U2 and U1 anxiety for a new brand with almost no branded search (fact base: Google Business Profile views flat at 350 to 500 a month); Motilal pattern ADAPT (checkable facts instead of scale claims) | s-hero creds: "SEBI-registered stock broker {{reg.capital.sebi}}", "Member of NSE, BSE, MCX and MSEI", "NSDL depository participant {{reg.capital.dp}}"; s-faq: "You can check this registration yourself on the SEBI website" |
| 3 | What does it cost me to open the account? | MUST | Mandatory, every page | s-hero cred: "Account opening {{pricing.account_opening}}"; s-charges numeral card: "Account opening {{pricing.account_opening}}" |
| 4 | Which Aikyam company provides this, and which company receives my details if I act here? | MUST | Mandatory, every page | s-open: "Your number goes to Aikyam Capital Private Limited, SEBI registration {{reg.capital.sebi}}"; s-faq: "Aikyam Capital Private Limited ... opens your trading and demat account" |
| 5 | What happens after I click Get OTP? | MUST | Mandatory, every page | s-open: "We send a one-time password (OTP) to this number" and "You will continue to our secure KYC partner to verify your PAN and Aadhaar" |
| 6 | If I give my number, will someone call me? | MUST | Page-specific: Motilal pattern ADOPT (mobile + OTP first so drop-offs become callable leads); DPDP rule (consent never pre-ticked); U1 anxiety | s-open: "It is used to send your OTP and continue your application" plus the unticked consent box whose wording comes from compliance (`consent-mobile`, same key and wording as Home) |
| 7 | How long does it take, and is it fully online? | MUST | Mandatory, account opening | s-steps: "On your phone or computer, in about [kyc-duration placeholder]" ("fully online" held until confirmed, see section 10) |
| 8 | Do I need the app to open my account? | SHOULD | Page-specific: client decision (account opening live on the web, app coming soon, APP_LIVE = false); the announcement bar on every full-header page sends people here with that message | s-steps: "The ROOT app for iOS and Android is coming soon. You can open your account on the web today." |
| 9 | Which documents do I need? | MUST | Mandatory, account opening | s-steps: "Keep these ready: PAN card, Aadhaar linked to your mobile, bank account details, a photo of your signature" |
| 10 | What happens if my KYC fails or I stop halfway? | MUST | Mandatory, account opening | s-steps: "Stopped halfway? Come back with the same mobile number" plus the `kyc-fail` block; s-faq repeats it |
| 11 | Is my data safe, and who is the KYC partner? | MUST | Mandatory, account opening | s-steps (third docs strip "Your details and the KYC partner"): "KYC is completed with our KYC partner, {{kyc.vendor}}, on behalf of Aikyam Capital Private Limited. Your details are used to open and service your account, as set out in our Privacy Policy." plus the `data-security` block; s-faq item 2 repeats it; s-open handoff line |
| 12 | What does each order cost: brokerage and statutory charges? | MUST | Mandatory, trading F&O | s-charges: brokerage rows (rate-card tokens) and "Statutory and exchange charges are set by the government, the exchanges and SEBI" |
| 13 | Do I pay anything every year to keep the demat account? | SHOULD | Page-specific: search query "demat account AMC charges"; Motilal pattern ADAPT (show ₹0 only where confirmed) | s-charges: "Annual maintenance charge (AMC): {{pricing.amc}}" |
| 14 | What can I lose trading F&O? | MUST | Mandatory, trading F&O | s-risk: "9 out of 10 individual traders in equity Futures and Options Segment incurred net losses" (verbatim box) |
| 15 | Am I eligible for F&O, and what proof of income do I need? | MUST | Mandatory, trading F&O | s-fo: "F&O is an optional segment. Before it is switched on, you share one proof of income. You can ask for F&O while you open your account" plus the accepted-proofs placeholder list |
| 16 | Where do I find current lot sizes, margins and expiry dates? | MUST | Mandatory, trading F&O | s-fo: "They change often, so we do not print them here. Check the current figures on the NSE website" |
| 17 | When can I start trading, and where do I log in? | SHOULD | Page-specific: search query "when can I start trading after opening demat account"; client decision (login moves to trade.rootbyaikyam.com at go-live, never the UAT link) | s-steps: "Activation is subject to KYC verification and exchange approval. When your account is active, log in at {{url.login}}." |
| 18 | Can NRIs, joint holders or companies open an account here? | SHOULD | Page-specific: search query "NRI demat account" (Motilal runs /nri-demat-account); NRI is deferred until a PIS bank tie-up exists | s-faq: "This page opens accounts for resident Indian individuals. NRI accounts are not available on ROOT yet." |

Counts: 12 mandatory (all MUST), 6 page-specific (2 MUST, 4 SHOULD).

## 5. What this page must not say
- "₹0", "free" or "zero" account opening, or "zero AMC", outside a placeholder: `{{pricing.account_opening}}` and `{{pricing.amc}}` are not confirmed. The primary button reads "Get OTP", never "Open free account".
- Any brokerage, DP or AMC figure, and never Motilal Oswal's rates as stand-ins. No "no hidden charges", "lowest brokerage", "cheapest". No "per order" in the brokerage column or copy: it presumes a flat-fee plan before the rate card exists (Q8).
- Durations or speed: "account in X minutes", "instant activation", "fast, reliable execution", "instant pledge", MTF or "pay later". Activation is always "subject to KYC verification and exchange approval".
- "Fully online" as an absolute (headings, head lines, creds) until the client tech head confirms that no step is offline (Aadhaar not linked to the mobile, video IPV, courier, wet signature). "Online" in the h1 and "on your phone or computer" are fine.
- Security superlatives: "bank-grade security", "100% secure", "your data is never shared"; no "secure" or "securely" beyond the approved handoff line (same rule as Home).
- F&O figures from memory (lot sizes, margins, expiry days, leverage), and F&O promotion before the risk box ("trade F&O with high leverage", "multiply your capital").
- "One account for everything" or "single account" for trading and mutual funds (Q7 open). This page does not say mutual funds can be bought with this account; the side door names Aikyam Wealth.
- The word "mutual fund" or "SIP" anywhere it is avoidable (it pulls the MF risk line in; the side door says "investing account").
- Advice or research language: tips, stock ideas, research reports, recommendations, advisor.
- Counts, ratings, awards, testimonials, "trusted by", comparisons with other brokers.
- Urgency or incentives for opening an account ("open today", "limited period", cashback, contests): prohibited for brokers.
- Final consent or legal wording drafted by Giraffe: the consent label is a placeholder for compliance. No Giraffe-drafted contact promises either ("we only call you if...", "we never call", "the box is never ticked for you").
- The KYC vendor's name typed literally (use `{{kyc.vendor}}`), the UAT login link (use `{{url.login}}`), registration numbers typed literally (tokens only).
- App store links, QR codes or install claims (app coming soon). IPO claims ("apply in a few taps"): not this page's job.
- "Sub-broker", "IFA", "Direct plans".
- "Get OTP" on a link that only scrolls to the form: a label says what happens, so jump links read "Start with your mobile number".
- Links to pages that are not live at the Phase 1 launch (2 Nov): `/tools/margin-calculator` (Phase 2) and `/login` (Phase 3) in the page body. Login in the body uses `{{url.login}}`.

## 6. Sections and layout decisions
Judge ruling 12-Oct-2026: these decisions are final for the builder and supersede the strategist's provisional picks (kept as history in 6.3). Scores use the method rubric, each criterion 1 to 5 times its weight: Q answers (x3), N next step (x3), T trust and compliance (x3, veto), S scannable (x2), M mobile 390 (x2), P pattern consistency (x1), F Figma editability (x1). Maximum 75.

Two facts the strategist's plan missed, which shape every decision below:
- **Template D has no mobile bar.** `scripts/build.py` renders no `.mbar` on minimal-header pages (front matter `mbar` is ignored there), and `theme/patterns.css` says so ("template D has no mobile bar"). At 390 the only ways to the form are the hero card and the in-page links back to `#s-open`. A site proposal to add a one-button bar is raised separately; this page must work without it.
- **Two planned links are dead at the Phase 1 launch:** `/tools/margin-calculator` (page 46, Phase 2) and `/login` (page 74, Phase 3).

### 6.1 Final decisions
| # | Section id | Answers | Final layout | Why (one line) | Rejected and why |
|---|---|---|---|---|---|
| 1 | s-hero | 1, 2, 3 | **B refined** (judge 69): copy left (d1, a lead that names Aikyam Capital, five creds), the s-open card right and top-aligned with the h1, the side-door link directly under the card | Answers which account, is it real and what it costs in the order asked, with the simplest structure for Figma | A (59): a one-row lead bar has no room for the receiver line, consent and states. C sticky rail (63): grid row spans and a relaxed `.hero` overflow import poorly, the gain is desktop only, and it narrows s-risk and s-steps to 7/12 |
| 2 | s-open | 4, 5, 6, 11 | **B refined** (judge 71): labelled card; receiver line directly above the button, handoff directly below it; the "Already have an account? Login" line cut (the minimal header carries Login) | Who gets my number, what happens next and the consent box all sit at the point of action, with one button | A (59): consent and receiver squeezed into xs text. C (59): an account chooser presumes one onboarding (Q7 open) and puts a decision before the field; the side-door link does that job |
| 3 | s-risk | 14 | **Pattern verbatim, R1**: second section, directly after the hero | The strictest placement (the fo_page rule) on the page that opens the F&O-capable account; it matches Home and lets the hero name F&O | R2 (after the steps): the hero form and the steps link would be account CTAs that include F&O before the box. Close call raised to the user (ask_user) |
| 4 | s-steps | 7, 8, 9, 10, 11, 17 | **D, judge merge** (69): theme row of four steps; under it three `.docs` strips ("Keep these ready", "If you stop or a check fails" and, added in the 12-Oct fix round, "Your details and the KYC partner"); an activation and login line; a band link to `#s-open` | Answers the halfway and failure questions inside the block with one calm strip instead of four failure lines, and keeps the theme pattern Home also uses | B vertical with a recovery line per step (63): four "if this fails" lines, three of them placeholder chips, make failure the subject of the block, and it adds a new vertical pattern. A (64): failure and halfway answers only in the FAQ. C (53): a timeline of durations the KYC partner has not given |
| 5 | s-charges | 3, 12, 13 | **A refined** (judge 70): numeral card (account opening slot, AMC and DP lines, link to the form) + a two-column `table.data.data--stack` (Segment, Brokerage) + one statutory note + band CTA | Keeps the template's signature numeral and separates one-off fees from order costs, with no repeated column | A as specified (66): the third column repeats "At notified rates" in every row and the theme hides the last `data--fluid` column at 390 anyway; the token inside `.big` would render a 96 px nowrap chip. B fee strip (64): drops the numeral, lower reuse. C tabs (52): **veto**, rows visible only through interaction. Home's ledger (61): one list mixes one-off and per-order costs |
| 6 | s-fo | 15, 16 | **B refined** (judge 66): split, short lead left, two cards right (proof of income; where current numbers come from); margin calculator link dropped until page 46 is live | Two jobs, two cards, and the exchange link is a primary element | A pillars (62): four equal items for two jobs. C inline Q&A (53): duplicates the FAQ. Folding both answers into the FAQ (62): U2's second anxiety deserves a visible block |
| 7 | s-faq | 1, 2, 4, 10, 11, 18 | **Pattern** FAQ accordion (split, native details, first item open), six items | Standard section. Cut two items that repeat a visible answer: "Can I add F&O later?" (s-fo) and "When will the app be available?" (s-steps) | (standard, no exploration) |
| 8 | s-final | (5) | **Pattern** closing CTA on a white band: button "Start with your mobile number" to `#s-open` (not `data-primary`), ghost side door "Investing only? Start with Aikyam Wealth", company named, handoff line; both buttons full width below 640 px | With no mobile bar on template D, this is the phone visitor's way back to the form at the end of the page | Strategist's "Get OTP" label on a link that only scrolls: the label must say what happens. A dark band: not needed (keeps s-risk trivially above it) |

### 6.2 Final section plan and content outline
Order on the page: s-hero (with s-open nested) · s-risk · s-steps · s-charges · s-fo · s-faq · s-final. Template D skeleton followed with two stated changes: steps come before charges (the risk box must follow the hero; the process answers decide whether a visitor finishes today, while the charges block is mostly "to confirm" chips until the rate card is approved and the account-opening charge already sits in the hero creds), and an F&O block is added (the trading F&O questions need a home that a link cannot replace). Strongest argument against steps first: U2 is the primary audience and cost is their first anxiety. Mitigation: the cost cred in the hero links to `#s-charges`.

**s-hero** (`section.hero`, `hero-grid` 7/5, page CSS `align-items:start` so the card top-aligns with the h1)
- h1 `d1`: "Open your trading and demat account, *online.*"
- Lead (one paragraph, two sentences; replaces the separate entity line): "A trading and demat account with Aikyam Capital Private Limited, the SEBI-registered stock broker behind ROOT by Aikyam. Trade shares and ETFs, and add F&O, currency and commodity when you are ready." (segments to confirm, section 10)
- Creds (`ul.creds`, five, theme order): shield "SEBI-registered stock broker" + `{{reg.capital.sebi}}` (mono); chart "Member of NSE, BSE, MCX and MSEI" + "Member codes in the footer"; lock "NSDL depository participant" + `{{reg.capital.dp}}`; sprout "Backed by Aikyam Capital Group" + "Capital markets to asset management"; rupee "Account opening" + `{{pricing.account_opening}}` + link "See all charges" to `#s-charges` (fix round: this cred spans both columns, `li.cred-cost`, and the chip and the link share one `.cost-line`, so it reads as two lines like the other four).
- Right column: the s-open card, then the side-door link (`hero-alt`): "Investing only? Open an investing account with Aikyam Wealth" to `/open-account/investing` ("Aikyam Wealth" and the arrow sit in one `.link-tail` span, so the arrow never wraps onto a line of its own). At 390 the order is h1, lead, creds, card, side door, so nothing secondary sits between the proof and the form.
- No rings, no phone (the card is the right column's content).

**s-open** (`<section id="s-open">` nested in the hero's right column; card r16, shadow-1; contains the `<form>`)
- Tag above the heading: "Step 1 of 4 · Trading and demat account".
- h2 (class `h3`): "Start with your mobile number".
- `fgroup`: label "Mobile number"; `field` with `.pre` "+91"; placeholder "10-digit mobile number"; help "We send a one-time password (OTP) to this number."
- `check` (unticked, required by default as on Home): label `<mark class="ph" data-ph="consent-mobile">Consent wording from Aikyam compliance</mark>` and a "Privacy Policy" link (`/legal/privacy`). No Giraffe-written promise about calls next to it.
- Receiver line (`xs`, directly above the button): "Your number goes to Aikyam Capital Private Limited, SEBI registration {{reg.capital.sebi}}. It is used to send your OTP and continue your application." (Home's lead bar must use the same sentence; orchestrator to align.)
- Button `btn btn--lg` full width, `type="submit"`, `data-primary`: "Get OTP" + arrow.
- `handoff` (verbatim, directly below the button): "You will continue to our secure KYC partner to verify your PAN and Aadhaar. Activation is subject to KYC verification and exchange approval."
- States (`<template data-state>`): **otp-sent** (masked number, "Change number", OTP boxes with the length as a placeholder, resend timer as a placeholder value; this is also the state a visitor sees on arrival when Home's lead bar hands over the number); **invalid-number** (`fgroup.is-error` "Enter a 10-digit mobile number"); **consent-missing** (error under the box; keep only if compliance makes the box required); **otp-wrong** (`alert--err`, wrong or expired OTP, resend link); **verified** (`alert--ok` "Number verified", button "Continue to KYC with {{kyc.vendor}}", plus its `btn is-loading` variant); **existing-account** ("This number already has an Aikyam Capital account." with a "Log in" link to `https://{{url.login}}`, not `/login`).

**s-risk** (`band band--mist band--tight`): the fo_risk block verbatim from the brief, including the source line with `{{fo.risk_source}}` and the `fo-risk-current` placeholder. Never collapsed, never under a sticky element.

**s-steps** (`band`; theme "Process steps" markup)
- h2 `d2 node`: "Open your account in four steps." (theme line, same as Home)
- Head: "On your phone or computer, in about `<mark class="ph" data-ph="kyc-duration">time to confirm</mark>`. The ROOT app for iOS and Android is coming soon, so open your account on the web today."
- `ol.steps` (four, theme copy): 1 "Enter your mobile number" / "We send a one-time password to confirm it's you."; 2 "Verify your PAN" / "Your PAN details are checked with the income tax records."; 3 "Share Aadhaar with DigiLocker" / "Fetch your address from DigiLocker, with your consent." (theme said "securely": Home bars "secure" beyond the approved handoff line); 4 "Link your bank and e-sign" / "Add a bank account, then sign with your Aadhaar OTP."
- `.docs` strip 1, "Keep these ready": PAN card; Aadhaar linked to your mobile (for the OTP); Bank account details; A photo of your signature; "For F&O only: one proof of income" (link to `#s-fo`).
- `.docs` strip 2, "If you stop or a check fails": "Stopped halfway? Come back with the same mobile number and `<mark class="ph" data-ph="kyc-resume">pick up where you stopped</mark>`." then `<div class="ph ph--block" data-ph="kyc-fail">What happens when the PAN, Aadhaar or bank check does not go through, and the route if Aadhaar is not linked to your mobile: to confirm with the KYC partner</div>`.
- `.docs` strip 3, "Your details and the KYC partner" (fix round, answers MUST question 11 in the visible flow): "KYC is completed with our KYC partner, {{kyc.vendor}}, on behalf of {{reg.capital.name}}. Your details are used to open and service your account, as set out in our Privacy Policy." (link `/legal/privacy`) then `<div class="ph ph--block" data-ph="data-security">Security measures Aikyam can state, to confirm</div>`. At 900 px and up the three strips share a 17rem label column so their content starts at the same x.
- `small`: "Activation is subject to KYC verification and exchange approval. When your account is active, log in at {{url.login}}."
- `band-cta`: link "Start with your mobile number" to `#s-open`; `xs` (verbatim decision) "Steps shown are indicative and will be confirmed with the KYC partner's live flow."

**s-charges** (`band band--mist`, `price-grid` 4/8)
- h2 `d2 node`: "Know what you pay before you trade." (theme line)
- Head: "Brokerage is set by Aikyam Capital. Statutory and exchange charges are set by the government, the exchanges and SEBI, and appear on your contract note."
- Numeral card (`.zero`): label "Account opening"; numeral slot `<div class="big">{{pricing.account_opening}}</div>` with the page CSS rule `.zero .big .ph{font:500 var(--fs-sm)/1.4 var(--sans); white-space:normal}` so the unconfirmed chip renders at body size and wraps, and a confirmed value renders as the serif numeral with no markup change; "Annual maintenance charge (AMC): {{pricing.amc}}"; "DP charge when you sell shares from your demat: {{pricing.dp_charge}}"; ghost link "Start with your mobile number" to `#s-open`. Fix round: the card hugs its content (`align-self:start`) instead of stretching to the table's height, so the link sits directly under the fees.
- Table (`tablewrap` + `table.data.data--stack`, two columns, each cell with a `td-label`; visible caption "Brokerage by segment (rate card to be confirmed)"): Segment, Brokerage. Rows: Equity delivery `{{pricing.delivery}}`; Equity intraday `{{pricing.intraday}}`; Futures `{{pricing.futures}}`; Options `{{pricing.options}}`; Currency and commodity `{{pricing.currency_commodity}}`. Fix round: only the Brokerage cell carries a `td-label`; at 390 the segment name is the row title (600 weight), so "Segment" is not repeated five times.
- Note under the table: "On top of brokerage, statutory and exchange charges apply: Securities Transaction Tax (STT) or Commodities Transaction Tax (CTT), exchange transaction charges, SEBI turnover fees, stamp duty and GST."
- `band-cta`: link "See the full list of charges" (`/pricing`); `xs` "Brokerage will never exceed the limits prescribed by SEBI."

**s-fo** (`band`, `split`)
- h2 `d2 node`: "F&O needs one more step: proof of income." (neutral, matches question 15; replaces "Want to trade F&O?")
- Left: "F&O is an optional segment. Before it is switched on, you share one proof of income. You can ask for F&O while you open your account `<mark class="ph" data-ph="fo-activation-when">or later, to confirm</mark>`." Link "Read the full risk disclosure" (`/legal/risk-disclosure`).
- Right card 1, "Proof of income we accept": `<div class="ph ph--block" data-ph="fo-income-proofs">List to confirm with Aikyam compliance, for example: bank statement, latest ITR acknowledgement, salary slip or Form 16, net worth certificate, demat holdings statement</div>`.
- Right card 2, "Current lot sizes, margins and expiries": "They change often, so we do not print them here. Check the current figures on the NSE website." Links: "NSE: contract specifications and expiry calendar" (nseindia.com, external); "What each F&O order costs" (`#s-charges`). Add "Estimate margins with the margin calculator" (`/tools/margin-calculator`) only when page 46 goes live (Phase 2).

**s-faq** (pattern: `split`, left stack + `faq` details, first item open)
- Left: h2 `d2 node` "Questions before you start."; lead "Can't find yours? Talk to us and a real person replies." (`/contact`); `small` "For complaints about securities broking: {{contact.grievance_email}}"; link "Visit the Help Centre" (`/help`).
- Items, in this order:
  1. (open) "Which company opens and holds my account?": "Aikyam Capital Private Limited, a SEBI-registered stock broker ({{reg.capital.sebi}}) and NSDL depository participant ({{reg.capital.dp}}), opens your trading and demat account. ROOT by Aikyam is its retail brand. You can check this registration yourself on the SEBI website." (external link to sebi.gov.in; exact search page to confirm, same question as Home) + proprietary line verbatim: "Aikyam Capital Private Limited is engaged in client based and proprietary trading on various exchanges." (source uses `{{reg.capital.name}}` for the company name, so it follows values.json; the rendered text is verbatim) This item stays the open one, because it carries a disclosure.
  2. "Is my data safe, and who is the KYC partner?": "KYC is completed with our KYC partner, {{kyc.vendor}}, on behalf of Aikyam Capital Private Limited. Your details are used to open and service your account, as set out in our Privacy Policy." + `<div class="ph ph--block" data-ph="data-security">Security measures Aikyam can state, to confirm</div>`.
  3. "What if a check does not go through, or I stop halfway?": the same words and placeholders as the s-steps strip 2.
  4. "I only want to invest, not trade. Is this the right page?": "Investing accounts are opened by Aikyam Wealth Private Limited on the Start Investing page." (link) + `<mark class="ph" data-ph="one-flow">one onboarding for both, to confirm</mark>`.
  5. "Can NRIs, joint holders or companies open an account here?": "This page opens accounts for resident Indian individuals. NRI accounts are not available on ROOT yet." + `<div class="ph ph--block" data-ph="account-types">Joint, minor, HUF and company accounts, to confirm</div>`.
  6. "How do I raise a complaint?": "Write to {{contact.grievance_email}}. If you are not satisfied with the response, you can use SEBI's SCORES portal or the Smart ODR portal (online dispute resolution)." with both portals linked (scores.sebi.gov.in, smartodr.in) and `<mark class="ph" data-ph="escalation-text">Compliance to confirm wording</mark>` after it (Giraffe wording about a regulatory process). Link `/legal/grievance-redressal`.

**s-final** (pattern closing CTA, white band)
- h2 `d2 node`: "Open your account with Aikyam Capital."
- Row: `btn btn--lg` link "Start with your mobile number" to `#s-open` (not `data-primary`); `btn btn--ghost btn--lg` "Investing only? Start with Aikyam Wealth" to `/open-account/investing` (names the company, like the hero side door). Below 640 px the row stacks and both buttons are full width.
- `handoff`: "You will continue to our secure KYC partner to verify your PAN and Aadhaar."

Internal links in the body (all live at Phase 1): `/open-account/investing`, `/pricing`, `/legal/privacy`, `/legal/risk-disclosure`, `/legal/grievance-redressal`, `/help`, `/contact`. External: nseindia.com, sebi.gov.in, `https://{{url.login}}`.

### 6.3 Options explored (strategist specs, strategist and judge scores)
Full three-line specs and hypotheses are in the strategist's v1 (git history); the essentials and both scores are kept here.

#### s-hero
| Option | Spec | Strategist | Judge |
|---|---|---|---|
| A · Pattern "Hero · proof before form" | `hero-grid` 7/5; one-row lead bar under the creds in the copy column; theme rings right | 59 | 59 (Q3 N4 T4 S4 M4 P5 F5) |
| **B · Copy left, labelled form card right** | card top-aligned with the h1, natural height, not sticky in the static file | 69 | **69** (Q5 N4 T5 S5 M4 P4 F5) after the judge refinements |
| C · Sticky rail | 7/5 rail from the hero to the end of s-steps; card sticky at 96 px | 66 | 63 (Q5 N4 T5 S4 M4 P3 F2): its N 5 was desktop only; at 390 it is B, and no mobile bar helps either option |
- Judge refinements to B: the entity line merges into the lead (the company was named three times in the first screen); the side door moves under the card (secondary link after the primary at 390); the cost cred links to `#s-charges` for U2.
- Strongest argument against B: template D says "sticky form right". Kept because the static file cannot show stickiness, `.hero{overflow:hidden}` makes a sticky card inside the hero inert, and the band links plus s-final bring desktop and phone readers back; the designer may prototype stickiness (rail structure) for production.

#### s-open
| Option | Spec | Strategist | Judge |
|---|---|---|---|
| A · Pattern lead bar | one row (+91 field, "Get OTP"), consent one xs line, no heading | 59 | 59 |
| **B · Labelled card** | step tag, h2, labelled field with help, unticked consent, receiver, full-width button, handoff, states in place | 71 | **71** (Q5 N4 T5 S5 M5 P4 F5) |
| C · Account chooser card | B plus a segmented control "Trading and demat / Investing only" | 59 | 59 |
- Judge refinements to B: receiver line moved above the button (read before the click); Login line cut (header has it; `/login` is Phase 3); consent key `consent-mobile` shared with Home; the "only with your consent" and "the box is never ticked for you" lines cut (Giraffe-drafted contact promise; meta copy).
- Strongest argument against B: more visible parts than a lead bar may lower starts for ready-to-act traffic. Kept because the consent box and receiver line are mandatory here either way; the card gives them room without hiding them.

#### s-steps
| Option | Spec | Strategist | Judge |
|---|---|---|---|
| A · Pattern "Process steps" | row of four on the gold connector, docs strip, band CTA, caption | 61 | 64 (Q3 N4 T5 S5 M4 P5 F5) |
| B · Vertical steps with a recovery line each, docs card beside | `split` 7/5; vertical connector; "If this step does not go through" xs line per step | 67 | 63 (Q5 N4 T5 S3 M4 P3 F4) |
| C · Steps plus an after-submit timeline | row of four, a second row "After you submit" with time placeholders, docs table | 53 | 53 |
| **D · Judge merge: A's row + two `.docs` strips** | row of four; strip "Keep these ready"; strip "If you stop or a check fails" (resume line + one `kyc-fail` block); activation and login line; band link | (new) | **69** (Q5 N4 T5 S5 M4 P4 F5) |
- Why D: it keeps B's real gain (the failure and halfway answers inside the block, a MUST) without B's cost: three per-step placeholder chips and four repeated failure lines that make a calm process read as risky. It reuses the theme `.steps` and `.docs` markup twice, so Home's steps and this golden stay one pattern.
- Strongest argument against D: B answers "what if it fails here?" at the step where the fear arises. Answer: this block is a preview, not the live form; the KYC host shows step-level errors, and the per-step answers are not known yet (one block, one question to the KYC partner).

#### s-charges
| Option | Spec | Strategist | Judge |
|---|---|---|---|
| **A · Pattern "Charges block"** | `price-grid` 4/8; numeral card; table | 67 | 66 as specified (M 3: hidden third column, 96 px chip); **70** refined (Q5 N4 T5 S5 M4 P5 F5) |
| B · Fee strip and order anatomy | three fee tiles, then brokerage by segment beside a list of statutory charges | 64 | 64 |
| C · Segment tabs | one panel shown, others as states | 52 | 52, **veto** (content visible only through interaction) |
| Home's two ledgers (reference) | one Charge, Rate table, no numeral until ₹0 is confirmed | (not explored) | 61 |
- Judge refinements to A: two columns (Segment, Brokerage) in `data data--stack`; the statutory column becomes one note; "per order" dropped from the header; the numeral slot keeps the token but the page CSS renders an unconfirmed chip at body size.
- Strongest argument against A: while the charge is unconfirmed the numeral card shows a small chip where a big ₹0 should be, which looks unfinished. Kept on purpose: the gap must be visible until Aikyam confirms (section 10), and the confirmed value fills the numeral with no layout change.

#### s-fo
| Option | Spec | Strategist | Judge |
|---|---|---|---|
| A · Pattern "Pillars · editorial 2x2" | four hairline pillars | 62 | 62 |
| **B · Split with two cards** | lead and risk-disclosure link left; "Proof of income we accept" and "Current lot sizes, margins and expiries" cards right | 68 | **66** (Q5 N3 T5 S5 M4 P4 F5) |
| C · Inline Q&A | three open details items | 53 | 53 |
| Fold into the FAQ (judge check) | two FAQ items, no section | (not explored) | 62 (S 3: U2's eligibility answer would sit in an accordion) |
- Judge refinements to B: neutral h2; margin calculator link removed until page 46 is live (Phase 2), so the card has no dead end at launch.
- Strongest argument against B: a section the template skeleton does not list. Kept because two trading F&O MUST questions need an on-page answer and the paid page (75) inherits it.

### 6.4 Placement of the F&O risk box (s-risk)
- **R1 · Second section, directly after the hero. FINAL (default).** The hero can then name F&O, currency and commodity plainly (question 1 for U2), and every later mention (the documents strip's income-proof pointer, F&O rows in charges, s-fo) sits after the box. It meets the strictest rule (the `fo_page` placement) on a page whose account includes F&O, matches Home, and gives the paid page 75 a placement compliance can approve once.
- **R2 · After s-steps, before s-charges and s-fo.** Keeps the process first for U1 and keeps the loss statistic out of the first scroll. Requires a hero that never mentions F&O and a documents list without the income-proof pointer, and still leaves the hero form and the steps link as account CTAs before the box.
- Strongest argument against R1: a first-time investor who never meant to trade F&O meets a loss statistic right under the form, which may lower starts. Kept because the account opened here is the one that carries F&O, SEBI's intent is visibility before promotion, and compliance is a veto criterion. Raised to the user as a close call (ask_user).

### 6.5 Notes for the builder
- One `data-primary`: the "Get OTP" submit in `#s-open`. Every other route to the form (cost cred link, steps band link, numeral card link, s-final button) is a plain link to `#s-open` or `#s-charges`, labelled for what it does.
- `s-open` is a `<section>` nested in the hero's right column so the trace and the `#s-open` anchor both work; its heading is an h2 styled `h3`. Lint's section order then lists s-hero, s-open, s-risk: fine on this page (no `fo_page` flag), but a page that adds `fo_page` would need s-open as a `div`.
- No mobile bar on template D: do not set or rely on front matter `mbar` (the build ignores it on minimal-header pages). Check at 390 that the "Get OTP" button sits within 1.5 screens (the five creds come first); if it does not, shorten the lead to one sentence before cutting a cred.
- `.ph` is `white-space:nowrap` in `theme/patterns.css`: keep inline placeholder labels to 30 characters or fewer (they overflow at 390 otherwise) and put longer ones in `ph ph--block`. The keys above are written to fit.
- Page CSS (tokens only, short): `.page-start-trading .hero-grid{align-items:start}` and `.zero .big .ph{font:500 var(--fs-sm)/1.4 var(--sans); white-space:normal}`. Name both in memory section 7 for promotion.
- The table is `data data--stack` (two columns) so it stacks with labels at 390; do not use `data--fluid` (the theme hides its last column on phones).
- The side-door copy avoids the words "mutual fund" and "SIP" so the lint does not ask for the MF risk line on a Capital page.
- Login in the body uses `https://{{url.login}}`; the minimal header's `/login` is a shell matter (site proposal).

### 6.6 What derivatives inherit
- 10 Start Investing (Wealth): inherit 09 s-hero (B refined), s-open (B refined; receiver "Aikyam Wealth Private Limited, AMFI ARN {{reg.wealth.arn}}"; same consent key unless compliance sets a Wealth one), s-steps (D with three docs strips: Wealth documents with no F&O pointer, the stop-or-fail strip, and the details-and-KYC-partner strip naming Aikyam Wealth), s-faq, s-final. Drop s-risk and s-fo; place the MF risk line next to the first investing CTA and the distributor disclaimer before s-final; explore only its "what you pay" block (commission disclosure, not brokerage).
- 11 Get the App: inherit s-hero (B refined) with a notify card (`#s-notify`, receiver named) in place of the OTP card; no steps or charges.
- 74 Login: inherit the minimal header, short footer and the s-hero composition (B refined) with desk cards instead of a form.
- 75 Paid landing page: inherit every 09 section and the R1 risk placement; campaign copy only; noindex.

## 7. Components and patterns
- Reused (theme v1 / pattern library): Hero · proof before form (`section.hero`, `hero-grid`, `hero-copy`, `ul.creds`, `root-seed`, `handoff`, `hero-alt`); form controls (`fgroup`, `field` + `.pre`, `fhelp`, `check`, `otp`, `btn btn--lg`, `btn.is-loading`, `alert--ok/--err/--info`); Mandatory disclosure (`risk-box`, verbatim); Process steps (`ol.steps`, `.dot`) + `.docs`; Charges block (`price-grid`, `.zero`, `tablewrap` + `table.data.data--stack` with `td-label`); `split`; FAQ accordion (`faq`, native details, first item open); Closing CTA (`final`, `.row`); `band-cta`; placeholders (`mark.ph`, `div.ph.ph--block`).
- New patterns (all CSS in the page's `<style data-page>`, tokens only; proposed for `theme/patterns.css`):
  - **Form card · template D** (`section.form-card#s-open` in the hero's right column, `.hero-side` stack under it): label tag, h2 styled h3, labelled field with help, unticked consent, receiver line above the button, full-width submit, handoff below. CSS: `.form-card`, `.form-card form`, `.form-card .btn{width:100%}`, `.hero-side`, `.states-board .form-card{max-width:30rem}`, `.page-start-trading .hero-grid{align-items:start}`. Reuse: 10 Start Investing (receiver Aikyam Wealth), 11 Get the App (notify card), 75 Paid landing page.
  - **Docs strip, used three times** (`.docs + .docs{margin-top:16px}`; at 900 px and up `.page-start-trading .docs{grid-template-columns:17rem minmax(0,1fr)}` so all strips share one label column; strips 2 and 3 have a `.stack` with a line and a `ph--block` on the right; `.docs .ph{white-space:normal}`): "Keep these ready", "If you stop or a check fails", "Your details and the KYC partner". Reuse: 10, 75.
  - **Charges block with a body-size placeholder in the numeral slot**: `.zero .big .ph{font:500 var(--fs-sm)/1.4 var(--sans); white-space:normal}`, `.zero .fees`, `.page-start-trading .zero{align-self:start; justify-content:flex-start}` (the card hugs its content instead of stretching to the table; replaces the earlier `.zero > .link{margin-top:auto}`), visible table caption `.data caption`. Two-column stacked table: only the value cell carries a `td-label`; below 640 px the first cell is the row title (`.data--stack td:first-child{font-weight:600; color:var(--aub)}`). Reuse: 06 Pricing, 75.
  - **Info card / F&O eligibility split** (`split` with lead left, two `.info-card` right; `.info-card .links`). Reuse: 37 F&O, 38 Currency and Commodity, 75.
  - **Wrapping link** (`a.link.link--wrap`: inline, arrow follows the last word instead of sitting at the far edge when the label wraps; the last word or name and the icon sit in `span.link-tail{white-space:nowrap}` so the arrow never wraps alone). Reuse: any long link label (side doors, external links).
  - **Cost cred** (`.creds li.cred-cost{grid-column:1/-1}` + `.cost-line{display:flex; flex-wrap:wrap; gap:4px 12px}`): a cred whose value is a chip plus a link spans both cred columns so it stays two lines. Reuse: 10, 75, any hero with a cost cred.
  - **Closing CTA, full-width buttons on phones**: below 640 px `.final .row{flex-direction:column; align-items:stretch; align-self:stretch; width:100%}` and `.final .row .btn{width:100%}`. Reuse: every page with two closing buttons (candidate for patterns.css).
  - **FAQ on a Mist band**: `.band--mist .faq summary .pm{background:var(--paper)}`.
- Fixes proposed for `theme/patterns.css` (found while building; affect every page):
  1. `.ph--block` inherits `white-space:nowrap` from `.ph`, so block placeholders run off one line (gate overflow at 390). Add `.ph--block{white-space:normal}`. This page carries it in page CSS meanwhile.
  2. The unscoped `.steps{grid-template-columns:repeat(var(--cols, 4), ...)}` comes after the theme's breakpoints and keeps four squeezed columns at 390. Scope it to `@media (min-width: 900px)` or repeat the theme's 2-column (899) and 1-column (640) rules after it. This page carries the restore in page CSS meanwhile.
  3. `.form-card .ph,.risk-box .ph{white-space:normal}`: long inline chips (the verbatim risk-box `fo-risk-current` note, the consent chip) must wrap inside narrow cards.
  4. `.fgroup > label` (600, line-height 1.2) also hits a `label.check` placed inside an error `fgroup` (consent-missing state), making the consent text bold and tight. Add `.fgroup > .check{font:400 var(--fs-sm)/1.45 var(--sans)}`. This page carries it in page CSS meanwhile.
- **Curated 12-Oct-2026**: all page CSS moved to `theme/patterns.css` (form card and hero side, cost cred, docs strips, charges block, info card, FAQ on Mist, closing CTA on phones, wrapping link, site fixes); the page has no `<style data-page>` block now. The numeral card's hug rule became the modifier `.zero.zero--top` (added to the markup). Markup in `theme/components.html`.

## 8. Actions and measurement
- Primary action and event: "Get OTP" (`button[type=submit][data-primary]` in `#s-open`, the only `data-primary` on the page); the form carries `data-event="account_start"` and `data-form-entity="Aikyam Capital"`. Measured position: top 485 px at 1440 (first screen), 1077 px at 390 (inside 1.5 screens, limit 1266).
- Secondary action and event: side door "Investing only? Open an investing account with Aikyam Wealth" to `/open-account/investing`, `data-event="switch_to_investing"` (proposed). Routes back to the form, not counted: cost cred "See all charges" (`#s-charges`), steps band link, numeral card link and s-final button "Start with your mobile number" (`#s-open`).
- Downstream (KYC host): `otp_verified`, `kyc_submitted`.

## 9. Compliance
- Disclosures on the page: F&O risk box (`#s-risk`) verbatim from rules/compliance-blocks.md, second section directly after the hero (R1), with `{{fo.risk_source}}` and the `fo-risk-current` placeholder; no dark band on the page. Proprietary trading line verbatim in FAQ 1 (open item; company name via `{{reg.capital.name}}`). "Brokerage will never exceed the limits prescribed by SEBI." under charges. Handoff line verbatim under the form and in s-final; "Activation is subject to KYC verification and exchange approval." under the form and in s-steps. "Steps shown are indicative and will be confirmed with the KYC partner's live flow." in s-steps. Short footer (shell) carries the registration strip and the market-risk line.
- Placeholders used (data-ph keys): consent-mobile, fo-risk-current, kyc-duration, kyc-resume, kyc-fail, fo-activation-when, fo-income-proofs, data-security (s-steps strip 3 and FAQ 2), one-flow, account-types, escalation-text (FAQ 6, grievance escalation wording for compliance), otp-length (states), otp-resend (states). Tokens that render as chips until confirmed: pricing.account_opening, pricing.amc, pricing.dp_charge, pricing.delivery, pricing.intraday, pricing.futures, pricing.options, pricing.currency_commodity, kyc.vendor. Tokens with values: reg.capital.name, reg.capital.sebi, reg.capital.dp, reg.wealth.name, contact.grievance_email, url.login, fo.risk_source. 25 placeholders on the default page.
- Entity statements: hero lead ("A trading and demat account with Aikyam Capital Private Limited, the SEBI-registered stock broker behind ROOT by Aikyam"); receiver line directly above "Get OTP" ("Your number goes to Aikyam Capital Private Limited, SEBI registration INZ000321232. It is used to send your OTP and continue your application."); FAQ 1 (Aikyam Capital opens and holds the account, ROOT is its retail brand); s-steps strip 3 and FAQ 2 (KYC partner acts on behalf of Aikyam Capital Private Limited); FAQ 4 (investing accounts by Aikyam Wealth Private Limited); s-final h2 "Open your account with Aikyam Capital." and the ghost side door "Investing only? Start with Aikyam Wealth".
- Words kept out (section 5): no "free", "zero", "₹0", "fully online", "secure" beyond the approved handoff line, "mutual fund", "SIP", "per order", durations, F&O figures. Lint: 0 errors, 0 reviews.

## 10. Open questions for Aikyam
| Question | Why it matters | Default used meanwhile | Owner |
|---|---|---|---|
| Is opening a trading and demat account ₹0? | The hero cred and the numeral slot in s-charges show it; "free" wording and the site-wide CTA label depend on it | `{{pricing.account_opening}}` chip in the cred and the numeral slot (body size until confirmed); the button reads "Get OTP" | Broking business head |
| Rate card: brokerage per segment, DP charge, AMC | Answers "what does each order cost" and "do I pay every year" | `{{pricing.*}}` chips ("Rate card to confirm"); column headed "Brokerage", not "per order" | Broking business head |
| One onboarding flow or two (Q7): can this flow also open an investing account with Aikyam Wealth? | Decides the side door, FAQ 4 and whether "one account" may ever be said | Two doors; this page opens the Aikyam Capital trading and demat account; side-door link; `one-flow` placeholder | Client tech head |
| KYC partner name, and the live step order; does the flow start with mobile and OTP? | Answers "who is the KYC partner"; the four steps are indicative | `{{kyc.vendor}}` chip; theme v1's four steps with the indicative caption | Client tech head |
| Time to complete onboarding, and typical time to activation | Answers "how long does it take" and "when can I start trading" | `kyc-duration` placeholder; no activation time stated | Client tech head (with the KYC partner) |
| What happens when a user stops halfway, and when PAN, Aadhaar or bank checks fail (including Aadhaar not linked to the mobile)? | MUST question 10 | `kyc-resume` and `kyc-fail` placeholders (one block in s-steps and FAQ 3) | Client tech head (with the KYC partner) |
| Consent at the mobile-number step: exact wording, and is the box required to continue (DPDP Act)? | Mobile-first only pays off if drop-offs may be called back lawfully; Home and 09 must use the same wording | One unticked checkbox, required, with placeholder `consent-mobile`; no Giraffe-written promise about calls | Compliance officer |
| F&O activation: accepted proofs of income, during onboarding or later, any other checks | MUST question 15 | `fo-income-proofs` placeholder block with commonly accepted examples; `fo-activation-when` placeholder | Compliance officer |
| Which segments and exchanges are live at launch (equity, F&O, currency, commodity; MSEI)? | The hero lead and a cred name them | Lead names all four segments; cred names NSE, BSE, MCX and MSEI (client-doc) | Compliance officer |
| OTP channel (SMS, WhatsApp), length and resend interval | The OTP-sent state | "OTP to this number"; states show the OTP boxes and a timer value as placeholders | Client tech head |
| Account types: resident individuals only? NRI, joint, minor, HUF, company | Question 18 | "Resident Indian individuals"; "NRI accounts are not available on ROOT yet"; others as an `account-types` placeholder | Broking business head |
| What can Aikyam state about data protection (storage, encryption, KRA and CKYC sharing)? | MUST question 11 | Visible in s-steps (third docs strip) and FAQ 2: KYC partner on behalf of Aikyam Capital, Privacy Policy link, `data-security` placeholder; no security adjectives beyond the approved handoff line | Compliance officer |
| Grievance escalation wording: may the page say "If you are not satisfied with the response, you can use SEBI's SCORES portal or the Smart ODR portal", and are scores.sebi.gov.in and smartodr.in the right links? | FAQ 6 describes a regulatory process in Giraffe wording | Sentence kept with both portals linked and an `escalation-text` placeholder; `/legal/grievance-redressal` link | Compliance officer |
| Is every step online for resident individuals (no video IPV, courier or wet signature)? | Decides whether "fully online" may be said; Home already bars it as an absolute | h1 says "online"; steps head says "on your phone or computer"; "fully online" held | Client tech head |
| Where does "Get OTP" post: an OTP step on this page, ekyc.rootbyaikyam.com, or the vendor URL? And does Home's lead bar hand the number over? | States and the handoff copy assume the OTP happens on this page; Home's default posts the number here | OTP on this page (OTP-sent state also shown on arrival from Home), then the handoff to the KYC partner | Client tech head |
| If the mobile number already has an account, do we send the user to login? | One of the form states | State "This number already has an Aikyam Capital account." with "Log in" to `{{url.login}}` | Client tech head |
| Which official pages should "check it yourself" link to (SEBI intermediary search, exchange member lookups, AMFI ARN search)? | Question 2 promises a check the visitor can make | FAQ 1 links to sebi.gov.in; exact search page to confirm | Compliance officer |
| Does Start Trading count as an advertisement that needs exchange filing? | Publication timeline for this page and the paid page 75 | Treated as a draft until compliance approves | Compliance officer |
| Proprietary trading disclosure: wording and placement on broking pages | The brief recommends it; wording is TO CONFIRM | Verbatim brief line in FAQ 1 (kept as the open item) | Compliance officer |
| F&O risk box: directly after the hero, or after the steps? | Sets what the hero may say and what the paid page inherits | Directly after the hero (R1), judge default | Giraffe |
| Template D pages have no mobile bar (build.py skips it on minimal-header pages): add a one-button "Get OTP" bar? | The Motilal template D pattern (ADOPT) has a fixed bottom CTA on mobile; without it the form is only reachable by scrolling or in-page links | No bar; in-page links to `#s-open` and the closing CTA | Giraffe |
| Where does Login point before /login (page 74, Phase 3) exists? | The minimal header links /login, which is dead from 2 Nov until 13 Jan | Page body uses `{{url.login}}`; header link is a shell decision | Giraffe |
| Which NSE page should "NSE: contract specifications and expiry calendar" open? | The F&O card promises current lot sizes and expiries; the home page is a weak landing | Link to nseindia.com home page, external icon | Compliance officer |
| KYC partner name length, for the "Continue to KYC with [partner]" button | The verified state names the partner above the button because the placeholder overflowed it | Button "Continue to KYC" with "KYC partner: {{kyc.vendor}}, on behalf of Aikyam Capital Private Limited" above it | Client tech head |
| Promote the two patterns.css fixes (`.ph--block` wrapping; `.steps` columns overriding the theme breakpoints) | Every page with a block placeholder or a steps row overflows or squeezes at 390 until fixed | Fixed in this page's CSS only | Giraffe (orchestrator) |

## 11. Notes for the Figma designer
- States board `figma/09-start-trading.states.html` (one frame each, the form card at its real width): `sending-otp` (Get OTP loading), `otp-sent` (OTP boxes, masked number, "Change number", resend timer as a placeholder; also the state on arrival from Home's lead bar with the number carried over), `otp-resend-ready` (timer ended), `invalid-number` (`fgroup.is-error`), `consent-missing` (keep only if compliance makes the box required), `otp-wrong` (`alert--err`), `verified` (`alert--ok`, "Continue to KYC", KYC partner named under it), `verified-loading` (handover in progress), `existing-account` (`alert--info`, "Log in" to `https://{{url.login}}`). Card footer: every state that continues to KYC ends with the same handoff line under its button (one form-card component with a fixed footer); `existing-account` is the only state without it, because that visitor logs in instead of going to KYC. The states board renders Mukta and Red Hat Mono; `shots.json` reports `fonts_loaded: false` there only because the check also tests Tiro Devanagari Hindi, which no state card uses.
- OTP: six boxes follow the theme kit; the real length is a placeholder (`otp-length`). Masked number "+91 98XXXXXX21" is a display example, not data.
- "Continue to KYC" button: the brief asked for "Continue to KYC with {{kyc.vendor}}"; the vendor chip made the button overflow the card, so the partner is named on the line above the button instead. Restore the longer label once the vendor name is known and short.
- Sticky: template D says "sticky form right". The static file shows the card in flow (`.hero{overflow:hidden}` would make a sticky card inert). Prototype stickiness for production with a rail if wanted (judge note in 6.3). No mobile bar on template D (build skips it); phone visitors return to the form through the in-page links and the s-final button. A one-button mobile bar is an open site proposal (section 10).
- Focus and keyboard: field focus ring (`.field:focus-within`), OTP box focus, auto-advance between OTP boxes, paste of the full OTP, numeric keypad (`inputmode="numeric"`) are behaviours to specify in the prototype.
- Numeral slot in the charges card: while `{{pricing.account_opening}}` is unconfirmed it renders as a body-size chip; a confirmed value fills the serif numeral with no layout change (keep the `.big` frame).
- FAQ: first item (company, registration, proprietary trading line) is open by default and must stay open; other items open one at a time.
- External links: SEBI (sebi.gov.in) and NSE (nseindia.com) open the home pages until compliance names the exact search and contract-specification pages; mark them with the external icon (`i-ne` on NSE).
- Imagery: none. No photos, no phone mockup on this page (theme rule); the gold root seed tops the spine at 1440 and is hidden below 900 px.
- Import notes: the inline `link--wrap` arrow (side door, NSE link) imports as text plus a vector; make it a link component with a trailing icon. Three `.docs` strips (one label column, 17rem at desktop) and two `.info-card`s should become instances of one component each. Side door and NSE link: the last word(s) and the icon form one unbreakable `.link-tail`.

## 12. Change log
- 12-Oct-2026 v1: briefed by the strategist (sections 1 to 6 and 10). Golden options for s-hero, s-open, s-steps, s-charges and s-fo plus the risk-box placement; picks are provisional until the judge decides.
- Judge 12-Oct-2026 (v2): questions reordered to visitor order (cost before the form questions; app after "how long"); question 2 now answered with a SEBI check link in FAQ 1; question 6 answered with what the number is used for plus the compliance consent box (Giraffe-drafted contact promise cut); question 17 reworded to "When can I start trading, and where do I log in?". Section 6 rewritten as final: hero B and form card B kept with refinements (entity line merged into the lead, side door moved under the card, receiver line above the button, Login line cut, consent key `consent-mobile` shared with Home); s-steps changed from B (vertical, per-step failure lines) to D (theme row plus two `.docs` strips; three per-step placeholders merged into `kyc-fail`; h2 back to the theme line, "fully online" held, "securely" dropped from step 3); s-charges A refined (two-column `data--stack` table, statutory column folded into a note, "per order" dropped, body-size chip rule for the numeral slot); s-fo B refined (neutral h2, Phase 2 margin calculator link removed); FAQ cut from 8 to 6 items; s-final button relabelled "Start with your mobile number". Recorded that template D has no mobile bar and that /login and /tools/margin-calculator are not live at the Phase 1 launch. Added must-not-say lines and three section 10 rows (check-it-yourself link, mobile bar on D, Login before page 74).
- Built 12-Oct-2026 (v3, builder): `pages/src/09-start-trading.html` written to the section 6 decisions; gate ok (3 runs: block placeholders overflowing at 390, then layout fixes after the screenshot review). Screenshot fixes: steps restored to 2 and 1 columns below 900 and 640 px (patterns.css override bug), `.ph--block` made to wrap (patterns.css bug), side-door and NSE links keep the arrow after the last word, numeral card content grouped at the top, spacing in the cost cred. Copy deviations from 6.2: steps head says "You can open your account on the web today." (not "so open your account on the web today", to avoid an urgency reading); the verified state names the KYC partner above a "Continue to KYC" button (vendor chip overflowed the button). Nine interaction states on the states board. Sections 7 to 9 and 11 filled; status built.
- Fix 12-Oct-2026 (v4, builder, status built): reviewer verdict "fix" (score 84). Blocking: MUST question 11 was answered only in collapsed FAQ 2; added a third `.docs` strip "Your details and the KYC partner" to s-steps after "If you stop or a check fails", with FAQ 2's answer ("KYC is completed with our KYC partner, {{kyc.vendor}}, on behalf of {{reg.capital.name}}. Your details are used to open and service your account, as set out in our Privacy Policy.") and the `data-security` block; FAQ 2 kept; section 4 row 11 now names s-steps and the section 4 intro now lists the real order exceptions (14 second; 17 before 12 to 16; 18 only in s-faq). Minor: proprietary line uses `{{reg.capital.name}}` (renders verbatim); FAQ 6 links SCORES (scores.sebi.gov.in) and Smart ODR (smartodr.in) and adds an `escalation-text` placeholder for compliance (section 10 row). Cheap improvements: side-door arrow kept on the text line (`.link-tail` around "Aikyam Wealth" and the icon; same on the NSE link); cost cred spans both cred columns with the chip and "See all charges" on one line; s-fo lead says "You can ask for F&O while you open your account"; stacked table at 390 shows the segment as the row title with only the "Brokerage" label; numeral card hugs its content at 1440 (`align-self:start`); s-final buttons full width below 640 px and the ghost reads "Investing only? Start with Aikyam Wealth"; handoff line added to otp-resend-ready, invalid-number, consent-missing, otp-wrong and verified-loading (existing-account excepted). Found in the slices and fixed: the three docs strips share a 17rem label column at 900 px and up; the consent label in consent-missing no longer turns bold (`.fgroup > .check`, proposed for patterns.css). Gate ok on every run (5 runs, all `"ok": true`); placeholders 22 to 25; Get OTP at 485 px (1440) and 1077 px (390). States-board `fonts_loaded: false` is a shoot.py check artifact (it tests Tiro, unused on the board); Mukta and Red Hat Mono render.
- Curated 12-Oct-2026 (pattern curator): `<style data-page>` removed (all rules promoted to `theme/patterns.css`); `.zero` became `.zero.zero--top`. Gate ok, slices unchanged (4 desktop, 6 mobile); 1440 pixel-identical. Two intended site-fix changes: at 390 every chip in main now wraps with cloned padding (as Home), so some chips break inside rather than move to the next line (same page height); in the consent-missing state the consent text is body colour (aub-80) instead of aub.
