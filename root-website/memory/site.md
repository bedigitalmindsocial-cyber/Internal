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

## Red-team round 1 (12-Oct-2026)
- Primary action per page comes from sitemap.json "cta": Wealth pages go to /open-account/investing, Capital and Both pages to /open-account/trading; Home also offers "Only mutual funds? Start investing" as its secondary path. The header button and mobile bar follow the page's company automatically.
- Registration numbers, CTA label, contacts and prices are `{{tokens}}` from memory/values.json; unknown ones render as placeholder chips. One edit there updates all 75 pages.
- Partner pages use their own template P (golden: 62 Distributor Partner Programme).
- F&O risk box: second section on F&O pages; above the dark band on every other page that promotes F&O.
- Theme v1 claims that are not yet provable stay out of copy or inside placeholders: bank-grade security, fast or reliable execution, institutional-grade or open-architecture research, instant pledge, MTF (rules/claims.json).
- The phone mockup illustration is used on Home and Get the App only; elsewhere use placeholders or theme rings.

## Pilot (12-Oct-2026): defaults adopted from the pilot's proposals (user may override at gate 1)
- No "one account", "single account" or "everything" copy until Q7 (one flow or two) is answered. Home h1 default: "Stocks, IPOs and mutual funds, in one place."
- Theme v1 blocks whose copy must not be reused: the trust pillars (execution and research claims), the ticker (invented values on real indices), the markets module and SIP projection on Home (Phase 2 data), the goal-progress phone card. Use the pilot's "facts list" and "two-entity credential ledger with verify links" instead.
- On fo_risk pages that are not F&O pages, the hero, title and description do not name F&O, and the risk box sits directly before the first section that promotes F&O (on Home: second section). Template D pages flagged fo_risk (09, 75) put it second.
- Every lead form: one unticked, required consent checkbox with compliance-supplied wording (placeholder `consent-mobile` for Aikyam Capital forms, `consent-mobile-wealth` for Aikyam Wealth forms); a receiver line naming the company and its registration token; the hand-off line. Aikyam Wealth forms say "Activation is subject to KYC verification" plus a placeholder for other checks (not "exchange approval").
- Customer-facing phone: `{{contact.helpdesk_phone}}`, never the main line (listed against the CEO in the Escalation Matrix).
- While the app is not live, the app band merges into the closing CTA on Home (one dark band); it splits back when APP_LIVE flips.
- Goal tiles on Home collapse to one "Plan by goal" link until the goal pages go live (8 Dec).
- "Fully online" is held until the KYC flow is confirmed to have no offline step; use "online" and "on your phone or computer".
- Phase 2 and 3 targets linked from Phase 1 pages fall back at go-live to their Phase 1 hub (/plan, /learn, /pricing); designs keep the final URLs.
- Analytics events add switch_to_investing and switch_to_trading for the cross-door links.

## Gate 1 answers (12-Oct-2026, user)
- Home h1: "Stocks, IPOs and mutual funds, in one place." (kept).
- Home F&O risk box: inside the Trade door, directly above the F&O row (verbatim, never collapsed; Aikyam compliance to confirm this placement is sufficient).
- Repo: the user is making it private; keep pushing everything.
- Pilot revision requested on all four fronts: less compliance-heavy feel, hero and first screen, copy and tone, visual richness. Response: rules/design-direction.md (v3) and a revise run of 01, 09, 10 before Wave 1.
- Consent wording master (draft, pending compliance): 09's form card, `data-draft="consent"` "I agree to the Privacy Policy and allow Aikyam Capital to call, SMS or WhatsApp me about this application." (Aikyam Wealth forms: same with Aikyam Wealth, `data-draft="consent-wealth"`). Every lead form copies it verbatim, so one approval covers all.
- Gate 1b (12-Oct-2026, user): revised pilot approved (01, 09, 10 status approved). Wave 1 (golden pages 03, 07, 17, 29, 42, 57, 62, 65) approved to run.
