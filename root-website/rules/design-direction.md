# Design direction v3 (after the pilot review, 12-Oct-2026)

**User feedback on the pilot (Home, Start Trading, Start Investing):** too compliance-heavy; the hero and first screen lack balance and impact; copy sounds legal; not visual enough. The pages were correct but not desirable.

**Target feel:** a premium, confident, calm Indian fintech. Think Motilal Oswal's polish and account-first clarity with Groww's simplicity, in ROOT's aubergine and gold. Compliance stays at 100%, placed and styled as quiet assurance instead of the headline.

**Persuasion rule (impeccable, persuade mode):** the opening must make the offer intelligible and desirable, put the real action in its working form on the first screen, and show something only this product can prove. Avoid the generic product page: a headline over subcopy and a button, then a row of equal cards.

## 1. The first screen (5-second test at 1440 and 390)
- **Left:** a short label, then the h1 (8 words or fewer; the outcome for the visitor; serif with at most one italic phrase), then one lead sentence (20 words or fewer; no legal company names), then the action in its working form, then **at most 3 proof points** (icon, short label, and a small mono registration code where it applies). Home and hubs use the inline mobile bar (theme v1 hero); template D uses the compact form card on the right.
- **Right:** a product visual. On Home and hubs this is an illustrative app screen (phone mockup or floating UI cards). On template D it is the compact form card: label, mobile field, consent line, button, and one line of fine print.
- Vertically centre the two columns; no empty quadrant at 1440. Everything needed to understand the offer sits above the fold.
- **No placeholder chips in the first screen** outside fine print (the gate fails it). If a value is unknown, write copy that doesn't need it: "See all charges", not "Account opening: [to confirm]".

## 2. Compliance, placed with care (verbatim texts unchanged)
- One-line disclosures (MF risk line, hand-off line, receiver line) go in **fine print** under the action: `<p class="fine">`. Longer blocks go in **one closing disclosure band** above the footer.
- F&O risk box: full and never collapsed, but **in context**. On Home it sits inside the Trade door, directly above the F&O row (user decision 12-Oct-2026; compliance to confirm). On F&O pages it comes right after the hero. Elsewhere it goes before the first F&O promotion. Style it as a calm inset panel, not an alarm.
- **Company names** go in labels, receiver lines, door headers, fine print and the footer, never in the h1 or lead. The voice is "ROOT"; the legal entity is stated once, plainly, where the visitor acts. Example label: "Trading and demat account · Aikyam Capital Private Limited".
- Registration numbers appear once in the hero proof points (small mono) and in the footer strip. Don't repeat them in every section.

## 3. Copy and tone
- Second person, benefit first, plain Indian English. Lead with what the visitor gets, then how, then the fine print. One idea per sentence; body sentences 18 words or fewer.
- Headings either answer the visitor's question ("What will I pay?", "What do I need to keep ready?") or state a benefit ("Start with your mobile number"). No regulatory phrasing in headings.
- Before and after, from the pilot:
  - "A trading and demat account with Aikyam Capital Private Limited, the SEBI-registered stock broker behind ROOT by Aikyam. Trade shares and ETFs, and add futures and options (F&O), currency and commodity when you are ready." becomes "Buy shares and ETFs, apply for IPOs, and add more segments when you're ready." with the entity in the label above the h1.
  - "Each product names the company that provides it." becomes nothing: the door labels already say it.
  - "Know what you pay before you start." stays: it is a benefit and a promise kept on the page.
- Draft wording for the client to approve (consent line, hand-off variants, microcopy) is written as **realistic draft copy**, marked `data-draft="consent"` (invisible) and listed in memory section 9. **Placeholders are for facts only**: numbers, prices, dates, registration values, names, payouts.

## 4. Visual richness
- At 1440, every screen height carries a visual anchor: an illustrative product UI (order ticket, SIP card, portfolio card, IPO card, KYC step card, built from theme parts as `.ui-card`), a theme illustration (rings, root-line motif, group diagram), icon tiles, an SVG data visual, or an art-directed image slot.
- Product UI is illustrative and captioned ("Illustrative screen"), with example names and no real tickers or prices. It shows what using ROOT feels like.
- **Image slots** (`figure.img-slot`): a soft Mist surface with a small icon and art direction (subject, mood, crop, ratio), e.g. "Photo: a 30-year-old professional checking a SIP on her phone at home, natural light, 4:5". Never a large dashed box. Real Aikyam people only after shoots; no stock traders at monitors.
- Use tables only when comparison needs them; otherwise use stat tiles, cards or icon lists.

## 5. Density and length
- Home and hubs: show less, link more. 7 to 9 sections, each with one idea and one action.
- Pricing on Home and hubs: 3 stat tiles (or 3 rows) plus "See all charges". Full rate tables live on the Pricing page.
- A placeholder in body copy is a quiet dashed underline, not a filled chip (theme v3 style). It stays visible but doesn't shout.

## 6. Rubric change
Add **Desirability, weight 3**: would a 30-year-old professional in Mumbai, Pune or Ludhiana want to use this after five seconds? It sits alongside "answers its questions" and "moves to the next step". A compliant but dull option loses to a compliant and desirable one.
