# Mandatory blocks (use verbatim; the lint checks for them by sitemap flag)

Presentation (design direction v3): the words are verbatim and never collapsed, but the frame is calm. One-liners go in `p.fine` under the action; longer blocks go in one closing disclosure band above the footer; the F&O box may be the inset variant (`risk-box risk-box--inset`) when placed in context.

The footer already carries: the registration strip, Attention Investors, the general disclaimer ("Investment in securities market are subject to market risks, read all the related documents carefully before investing.") and the caution notice. Pages add the blocks below according to their flags.

## fo_risk: F&O risk disclosure (SEBI circular of 19-May-2023; never collapsed, never in small grey type)
```html
<section class="band band--mist band--tight" id="s-risk" aria-labelledby="h-risk">
  <div class="wrap">
    <div class="risk-box">
      <svg class="i i--lg"><use href="#i-alert"/></svg>
      <div class="stack" style="--gap:10px">
        <h2 class="h3" id="h-risk">Risk disclosures on derivatives</h2>
        <ul>
          <li>9 out of 10 individual traders in equity Futures and Options Segment incurred net losses.</li>
          <li>On an average, loss makers registered net trading loss close to Rs. 50,000.</li>
          <li>Over and above net trading losses, loss makers expended an additional 28% of net trading losses as transaction costs.</li>
          <li>Those making net trading profits incurred between 15% to 50% of such profit as transaction cost.</li>
        </ul>
        <p class="xs">Source: {{fo.risk_source}}. <mark class="ph" data-ph="fo-risk-current">Aikyam compliance to confirm this is the current prescribed text</mark></p>
      </div>
    </div>
  </div>
</section>
```
Placement (lint checks it):
- Pages flagged `fo_page` (F&O, currency and commodity, margin and SPAN calculators, trading basics guide, risk disclosure): the box is the **second section, directly after the hero**, before any F&O call to action.
- Other `fo_risk` pages: before the first content that promotes F&O, and always **above the dark band** and the closing CTA. Never the last thing on the page, never under a sticky bar. It may sit in context as `<div class="risk-box risk-box--inset" id="s-risk">` inside the product block, directly above the F&O item (Home: inside the Trade door, user decision 12-Oct-2026, Aikyam compliance to confirm).
- F&O facts (lot sizes, margins, expiries, eligibility) change often: do not state figures from memory. Use placeholders and link to the exchange (nseindia.com) for current values.

## mf_risk: mutual fund risk line
"Mutual fund investments are subject to market risks, read all scheme related documents carefully."
Place it as fine print (`p.fine`) under the first MF call to action, and again in the closing disclosure band.

## distributor_disclaimer (Aikyam Wealth distribution, and IPO/bonds offered by the broker)
"Mutual funds, IPOs and bonds are not exchange traded products. Aikyam Wealth Private Limited acts only as a distributor (AMFI ARN {{reg.wealth.arn}}). Disputes arising from distribution activity do not have access to the exchange investor redressal forum or arbitration mechanism."
On IPO pages (broker), name Aikyam Capital Private Limited as the trading member acting as distributor.

## illustrative_data
`<p class="illus">Illustrative data. Not real prices or returns.</p>` directly under every chart, table or card that shows market or fund numbers.

## coming_soon
`<span class="soon">Coming soon</span>` next to the h1, and a "Tell me when it is live" form (mobile number) that names the entity collecting the data. No prices, no providers, no product claims until the product is cleared.

## pms (PMS pages)
- State the SEBI minimum investment: "{{pms.minimum}}" (lint checks for "50 lakh").
- Say the strategies are "empanelled for distribution" by Aikyam Wealth Private Limited, and name the third-party SEBI-registered portfolio manager for each strategy (placeholder names until confirmed). Never "our PMS".
- Fees, exit loads and lock-ins: placeholders until confirmed. No performance figures.

## partner (template P pages)
- Mutual fund distributors (Distributor Partner Programme, Aikyam Wealth): need NISM Series V-A certification and an ARN from AMFI; staff who deal with investors need an EUIN; they follow the AMFI code of conduct. Never "IFA".
- Authorised Persons (Aikyam Capital): approved by the stock exchanges on the broker's application; eligibility, certification and deposit requirements as per exchange rules (placeholders until Aikyam confirms). Never "sub-broker" except to explain that the category was replaced.
- Payouts, revenue share and incentives: placeholders only ("Payout grid to confirm"). No "earn up to", no "passive income".
- Name the company that signs the partner agreement and the data receiver on the application form.

## licence_check (RA, IA, PMS distribution, market data)
- No stock picks, target prices, model portfolios, "recommended funds", or "best funds" lists. A risk profiler shows a risk category and categories of products, never named schemes as advice.
- PMS: "empanelled for distribution"; name the third-party SEBI-registered portfolio manager; state the ₹50 lakh SEBI minimum.
- Stock and market pages: "Data shown is illustrative. Live data will come from a licensed market-data vendor."

## regulated_numbers
Registration numbers, member codes, ARN, CIN, DP ids, contacts: always as `{{tokens}}` from `memory/values.json` (listed in the brief). Never type them literally; unknown values render as placeholder chips by themselves.

## proprietary: trading disclosure (broking pages that describe Aikyam Capital)
"Aikyam Capital Private Limited is engaged in client based and proprietary trading on various exchanges."
