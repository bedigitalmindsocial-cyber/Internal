# Mandatory blocks (use verbatim; the lint checks for them by sitemap flag)

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
      </div>
    </div>
  </div>
</section>
```
Place it as the last section of the page (just above the footer). If the page has other disclosures, they share this band.

## mf_risk: mutual fund risk line
"Mutual fund investments are subject to market risks, read all scheme related documents carefully."
Place it next to the first MF call to action and again in the closing disclosure band.

## distributor_disclaimer (Aikyam Wealth distribution, and IPO/bonds offered by the broker)
"Mutual funds, IPOs and bonds are not exchange traded products. Aikyam Wealth Private Limited acts only as a distributor (AMFI ARN <mark class="ph" data-ph="amfi-arn">to confirm</mark>). Disputes arising from distribution activity do not have access to the exchange investor redressal forum or arbitration mechanism."
On IPO pages (broker), name Aikyam Capital Private Limited as the trading member acting as distributor.

## illustrative_data
`<p class="illus">Illustrative data. Not real prices or returns.</p>` directly under every chart, table or card that shows market or fund numbers.

## coming_soon
`<span class="soon">Coming soon</span>` next to the h1, and a "Tell me when it is live" form (mobile number) that names the entity collecting the data. No prices, no providers, no product claims until the product is cleared.

## licence_check (RA, IA, PMS distribution, market data)
- No stock picks, target prices, model portfolios, "recommended funds", or "best funds" lists. A risk profiler shows a risk category and categories of products, never named schemes as advice.
- PMS: "empanelled for distribution"; name the third-party SEBI-registered portfolio manager; state the ₹50 lakh SEBI minimum.
- Stock and market pages: "Data shown is illustrative. Live data will come from a licensed market-data vendor."

## regulated_numbers
Registration numbers, member codes, ARN, CIN, DP ids: use the values in `context/facts.md` section 9 (theme v1, pending compliance confirmation) and placeholders for anything listed as TO CONFIRM.

## Proprietary trading disclosure (broking pages that describe Aikyam Capital)
"Aikyam Capital Private Limited is engaged in client based and proprietary trading on various exchanges."
