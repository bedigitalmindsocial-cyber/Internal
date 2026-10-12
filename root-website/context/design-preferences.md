# Design-process preferences the user has stated

Compiled 12-Oct-2026. Sources: [session 12-Oct skills] ("UI/UX skills"), [session 12-Oct Impeccable] ("Impeccable skill cloud installation"), [session 09-Sep], [session 16-Sep], [session 06-Sep], [Theme v1 08-Oct], [MO UI Teardown 08-Oct], [Placeholder Register], [Sitemap v2 sheet], [Fact base 12-Oct], [CX context doc 18-Sep].

## 1. Skills the user wants used

The user's request on 12-Oct (paraphrased from typed messages): "install all the UI UX skills", then "/impeccable Install this skill in cloud" together with **/frontend-design, /better-ui, /better-colors, /better-layout, /ui-ux-pro-max, /design-motion-principles**, "from the local to cloud". [session 12-Oct Impeccable], [session 12-Oct skills]

| Skill | Upstream | Status on 12-Oct |
|---|---|---|
| `impeccable` + 4 helper agents (asset-producer, documenter, finish-reviewer, manual-edit-applier) | pbakaus/impeccable (Apache 2.0) | Installed at project level in `.claude/skills/` via draft PR bedigitalmindsocial-cyber/Internal#2. **Not on the current branch** (`claude/nice-bardeen-dzt4r4` has no `.claude/skills`). Upstream auto-hooks deliberately left out. Runs in reduced mode in the cloud (its engine download from GitHub is blocked) |
| `better-ui`, `better-colors`, `better-layout` | jakubkrehel/skills (MIT) | Installed in PR #2. They reference 4 sibling skills (typography, accessibility, writing, interface) that were not added; offered on request |
| `design-motion-principles` | kylezantos/design-motion-principles | Installed in PR #2 |
| `frontend-design` | Anthropic plugin | Already available in cloud as `/frontend-design:frontend-design` |
| `ui-ux-pro-max` | nextlevelbuilder/ui-ux-pro-max-skill | **Not installed**: the safety check blocked it because it ships a Python CLI. User options: retry and approve, or upload the local copy as an account skill |
| Account skills already synced | giraffe-website, page-cro, copywriting, site-architecture | Available |
| Plugins suggested (install card) | Design (Anthropic: critique, design systems, handoff, accessibility, UX copy), frontend-design, Figma (official), design-skills, Axe Accessibility, Mobile Design System, Claude2Figma, AI Ready Design System, figma-suite | Offered; the low-risk set is Design, frontend-design, Figma, Axe. Install status unknown |

Practical note: new sessions only get the project skills after PR #2 is merged into the default branch (`claude/dreamy-cori-dsb1sb`). [session 12-Oct Impeccable]

## 2. Critique and review rules

No explicit critique checklist was typed by the user in these sessions. The working rules that recur across the user's approved artifacts and decisions:

- **System, not skin.** Borrow Motilal Oswal's structure and calm; never its brand assets or claims. [MO UI Teardown 08-Oct], [Fact base 12-Oct]
- **No invented numbers or proof.** Placeholders stay visibly tinted (`[●]`, "to confirm" chips) so they cannot ship unnoticed. Illustrative screens are captioned. [Placeholder Register], [Theme v1 08-Oct]
- **Compliance gates live in code** as booleans (`PRICING_APPROVED`, `APP_LIVE`); unconfirmed figures sit in data attributes a reviewer can read in source without them rendering. [CX context doc 18-Sep], [Placeholder Register]
- **Contrast and accessibility:** gold never as text or button (2.6:1); a 2px focus ring with 3px offset; status never by colour alone; reduced-motion respected. [Theme v1 08-Oct]
- **Zero typo tolerance.** Clients proofread to punctuation level and have pushed back on "basic hygiene" errors. [CX context doc 18-Sep]
- **Voice lint before anything ships:** no em dashes, no exclamation marks, no buzzwords or superlatives, calm Indian English. The user's proposal pipeline checks for em dashes and "!" on every render. [session 09-Sep]
- **Cut bloat:** fewer, tighter sections; "cut sections, not padding". [MO UI Teardown 08-Oct]
- **Spot the compliance trap before the build**, not after (Direct Plans, IFA, sub-broker, Terms entity). These catches are part of what Giraffe sells. [CX context doc 18-Sep]
- **Dark mode:** the client does not want the dark colour to read as black on phones. [session 09-Sep]

## 3. Figma and handoff

- Design is delivered as **developer-ready Figma**: IA, URL map, wireframes, design system, desktop and mobile designs, plus marketing copy for every page. A design-only deliverable must be complete enough for the client's own developers to build from. [session 09-Sep]
- The client's scope deck asks for an **interactive prototype with premium micro-interactions**, a Next.js front end, a custom Node CMS, CRM integration, training and QA. [session 16-Sep]
- The theme is the shared parts list: "Every page in the 73-page sitemap is built from these tokens, components and templates. Nothing new gets invented page by page." Tokens go into the Next.js theme, and components reference token names only, never raw hex. [Theme v1 08-Oct]
- Theme v1 was prepared for a **Phase 1 design workshop** (08-Oct-2026). [Theme v1 08-Oct]
- **HTML-to-Figma import:** no user statement about it was found in the sessions read. The current build folder's own brief (`root-website/CLAUDE.md`) sets the method: self-contained HTML pages in `figma/` for import into Figma and refinement by a UI/UX designer. The Figma connector was available in the 12-Oct sessions. [session 12-Oct skills]
- The Login and e-KYC redesign may be **design-only Figma screens** that the platform vendor implements; this is still TO CONFIRM. [session 06-Sep]

## 4. Reference sites the user or client named

- Structure: NJ Wealth (E-Wealth account, partner network, "Client Desk" naming) and FundsIndia (goal tools before products). Footer: Groww, Zerodha, Upstox. [Sitemap v2 sheet], [session 09-Sep]
- Look and feel: Motilal Oswal ("the client wants Motilal Oswal's look and feel as inspiration"; later the "true replica" for structure). [MO UI Teardown 08-Oct], [Fact base 12-Oct]
