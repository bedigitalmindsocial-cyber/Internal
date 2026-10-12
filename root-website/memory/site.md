# Site memory: decisions that apply to every page

Append-only, newest last. Each entry: date, decision, reason, source. Page agents read this before starting; only the orchestrator writes it (from page-agent proposals and the user's answers).

## Foundation (12-Oct-2026)
- Scope: 75 pages = theme v1's approved 73-page plan (3 phases) + 2 added pages: 74 Login (desk chooser) and 75 Paid campaign landing page (/lp/open-account, noindex). Additions are defaults pending user confirmation.
- Theme: ROOT website theme v1 (8 Oct 2026) is the design system. Aubergine ink (#1C0F2F), one gold spark (#C19C2F), Mist bands, Tiro Devanagari Hindi serif display over Mukta sans, Red Hat Mono for registration codes. A 1 px gold "root line" runs down the left gutter; every h2 sits on a node.
- Shell: one header (announcement bar, mega menus, Login, Open free account) and one footer (columns, two-entity registration strip, Attention Investors, disclaimer, caution notice) for all pages; template D uses the minimal header and short footer.
- Direction: "Motilal skeleton at ROOT scale": account-first (mobile + OTP), checkable trust facts instead of scale claims, one public pricing page, entity-tagged pages and forms.
- Primary CTA label across the site: "Open free account" (to /open-account/trading) until the client confirms "₹0 account opening" and whether one flow serves both entities (Q7).
- Placeholders: `<mark class="ph" data-ph="key">` inline, `ph ph--block` for blocks. Never invent numbers, prices, counts, dates, legal text.
- Static output: no JavaScript; first tab or first state shown; motion off. Interactions are described in each page memory for the designer.

## Decisions carried over from earlier sessions (12-Oct-2026 harvest; full list in context/decisions.md)
- One primary action per view: "Open free account" (same words in header, hero and footer); "Login" is always secondary. Product actions name the product ("Start a SIP", "Apply for IPO").
- The ROOT app is "coming soon" (APP_LIVE = false): store buttons shown disabled with a Coming soon badge; QR "will appear here at launch"; Get the App collects "tell me when it is live" sign-ups.
- Pricing is not approved (PRICING_APPROVED = false): charges cells read "Rate card to confirm" placeholders; "Brokerage will never exceed the limits prescribed by SEBI."
- Account opening: four indicative steps (mobile + OTP, verify PAN, Aadhaar via DigiLocker, link bank and e-sign) captioned "Steps shown are indicative and will be confirmed with the KYC partner's live flow." Under every form: "You will continue to our secure KYC partner to verify your PAN and Aadhaar. Activation is subject to KYC verification and exchange approval." Consent never pre-ticked (DPDP Act).
- Login destination at go-live: trade.rootbyaikyam.com/login (never the UAT link).
- Gold is a spark only: never text, buttons or surfaces. Aubergine must not read as black on phones. One dark band per page; footer stays light.
- Data pages: every number shows an as-on date and its source; missing values show as a dash, never 0%; illustrative names only (Example Industries Ltd).
- Giraffe writes marketing copy; the client supplies legal and regulatory text. Partner pages are marketing + lead form only.
- Name and tagline per theme v1 ("ROOT by Aikyam", "Where your wealth begins.") until locked in writing.
