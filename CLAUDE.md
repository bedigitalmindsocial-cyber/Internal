# CLAUDE.md: Giraffe Industrial Marketing | India Manufacturer Lead Engine

## 0. How to use this file

- This is your standing brief. Read it fully at the start of every session.
- Then read `progress/STATE_CHECKLIST.md` and `progress/RUN_LOG.md`. Tell the user in 3 lines where you are resuming from, then continue. Never redo completed work.
- Work autonomously. Stop and ask the user only when:
  - web search or web fetch tools are unavailable,
  - a rule in this file conflicts with what you find,
  - you finish the calibration batch (Section 14) or a full Wave (Section 7).

---

## 1. Mission

Build a sorted, verified, deduplicated list of Indian **manufacturing companies with ₹50–500 Cr annual turnover** that are:

1. operationally strong (real plant, real customers, real scale),
2. poorly represented (outdated website, old or no corporate profile, weak digital presence), and
3. showing signs of expansion.

These are prospects for **Giraffe Industrial Marketing** (a Giraffe Partners division).

Cover India **state by state**, in the wave order in Section 7.

**Quality over quantity.** A state with 6 excellent, verified leads beats 60 weak ones. If a state produces few leads, that is fine: record it honestly in the checklist and move on.

---

## 2. Who we are (context for your judgment and for pitch hooks)

- **Giraffe Partners:** brand and communications consultancy based in Abohar (Punjab) and Delhi. 50+ brands, clients in 10+ countries.
- **Thesis, the representation gap:** many Indian manufacturers are operationally excellent but commercially underestimated because their website, corporate profile, catalogue and online presence look 10 years old.
- **What we sell:** brand strategy and identity, credibility website, corporate profile, brochure and catalogue, photoshoot and plant films, exhibition 3D stall design, flex and hoardings, social media, packaging, PR, and a monthly marketing retainer. Premium add-on: capital-markets narrative for companies preparing to raise capital or list.
- **Core pitch line:** "You have invested in the expo, but when someone Googles you after taking your card, what do they find?"
- **Who uses your output:** a caller (cold calls plus WhatsApp follow-ups, maximum 3 follow-ups, then drop) and segmented WhatsApp broadcast lists. Segment tags and pitch hooks directly drive outreach, so treat them seriously.

---

## 3. Ideal Customer Profile

### 3.1 Hard gates (a lead must pass ALL five to enter Active_Pipeline)

| Gate | Rule |
|---|---|
| **G1 Manufacturer** | Owns and operates at least one manufacturing plant in India. Pure traders, distributors, dealers and service firms are excluded. |
| **G2 Size** | Annual turnover ₹50–500 Cr with Size_Confidence Medium or High (Section 5.2). Low confidence is allowed only as Tier C with a Manual_Check note. |
| **G3 Not popular, not backed** | None of the exclusions in 3.2 apply. |
| **G4 Weak representation** | Website_Decay_Score ≥ 3, or no website at all. "They have branding, but not at the standard it should be" counts as a pass. |
| **G5 Right segment** | Not in the wrong-segment list in 3.3. |

### 3.2 Popularity and backing exclusions (reject with the code in brackets)

- Listed on the NSE or BSE main board (R5). **Exception:** SME-exchange listed, or has filed an SME IPO DRHP: keep the lead and tag it `CAPMKT`.
- Subsidiary or group company of a large business group, MNC or conglomerate (R4). Check the MCA holding company on public aggregator pages, and phrases like "a unit of" or "a [Group] company" on the website.
- PE or VC funded: news of funding rounds, or funding rounds listed on Tracxn or Crunchbase (R4).
- Has a Wikipedia page, or is a consumer household brand most Indians would recognise (R3).
- Heavy national media presence: roughly 10 or more national English business news articles about the company itself in the last 12 months (R3).
- Website redesigned within the last 24 months with a modern design (Website_Decay_Score ≤ 2), or the site credits a known agency with a recent year (R6).
- Verified revenue above ₹500 Cr (R1) or below ₹50 Cr (R2).
- Existing Giraffe clients (R10): Neev Seeds, Kasturi India, MW Wiretec, PJS Commodities. The user will add more in `config/exclusions.txt`. Always check that file.

### 3.3 Wrong segments

- **Reject (R8):** aerospace, defence and high-end precision engineering firms that already present at a global standard. Our own calls confirmed these do not need basic branding.
- **Do NOT reject, route to Longterm_Broadcast:** road construction, EPC contractors and government-contractor businesses. Low immediate branding need, but strong seasonal demand for Diwali corporate gifting. Tag `SEG-GIFTING`. They never go into Active_Pipeline.

### 3.4 Strong-fit signals (these boost priority, not required)

- Exhibits at trade fairs (Bharat Mandapam, Yashobhoomi, India Expo Mart, Jio World, BEC Mumbai, HITEX, BIEC, Chennai Trade Centre, Helipad Gandhinagar and similar).
- Exporter, Export Promotion Council member, or export house status holder.
- Supplies to large OEMs or institutional buyers.
- Family business with a next-generation director (roughly 25–40) who joined recently.
- Uses Gmail, Yahoo or Rediffmail as the official company email.
- Dealer or distributor network across several states.
- An expansion trigger from Section 4.

---

## 4. Trigger events (expansion signals) and where to find them

Only count triggers dated within the **last 18 months** (for trade fairs: 2025 or 2026 editions).

| Trigger_Score | Trigger | Where to look | Query templates |
|---|---|---|---|
| 5 | Capacity expansion or new plant approval: Environmental Clearance, Consent to Establish, EC public hearing notice | parivesh.nic.in; State Pollution Control Board consent lists and public hearing notices | `site:parivesh.nic.in "expansion" "{district}"` / `"public hearing" "expansion" "{district}" "TPA"` / `"consent to establish" "{city}" manufacturing` |
| 5 | Credit rating rationale that mentions capex or capacity expansion | acuite.in, infomerics.com, careratings.com, icra.in, indiaratings.co.in, crisilratings.com | `site:acuite.in "{city}" "capacity expansion"` / `site:infomerics.com "{city}" manufacturing capex` / `site:careratings.com "{city}" "debt-funded capex"` |
| 4 | New term loan or charge registered with MCA | Public pages on Tofler, The Company Check, Zauba Corp | `"{company}" charges` restricted to those sites |
| 4 | State investment subsidy or incentive approval | Invest Punjab, RIPS Rajasthan, Invest UP, Invest MP, Gujarat and Haryana committee minutes | `"state level empowered committee" minutes {state} manufacturing` / `"customised package" approved {state} unit` |
| 4 | Regional news of a new unit or investment | Regional-language press (Section 4.1) | Section 4.1 keywords plus the city |
| 3 | Exhibited at a trade fair in 2025 or 2026 | Exhibitor lists and PDF catalogues (Section 6.2) | `"{fair name}" 2026 exhibitor list` / `"{fair name}" exhibitors pdf` |
| 3 | Capital machinery import or EPCG authorisation | Volza and Seair free previews, news | `"{company}" EPCG` / `"{company}" import machinery` |
| 2 | Hiring a first marketing, export or brand manager, or a plant head for a new unit | Naukri, Indeed, LinkedIn job posts via search engine only | `site:naukri.com "marketing manager" manufacturing "{city}"` |
| 2 | Pvt Ltd converted to Public Ltd, or SME IPO preparation | MCA name change on aggregator pages, news | `"{company} limited" "formerly" "private limited"` |
| 1 | Exporter or association member, no dated event | EPC and association directories | Section 6.3 |

Trigger_Score for a lead = the highest single trigger found.

### 4.1 Regional-language news queries

Many of these companies only appear in regional press. Run these per cluster with the city name (in English and, where possible, in local script):

| Language | States | Keywords |
|---|---|---|
| Hindi | UP, MP, Rajasthan, Haryana, Bihar, Uttarakhand, HP, Chhattisgarh, Jharkhand, Delhi | "नई यूनिट", "नया प्लांट", "करोड़ का निवेश", "विस्तार" |
| Punjabi | Punjab | "ਨਵਾਂ ਪਲਾਂਟ", "ਨਿਵੇਸ਼" |
| Gujarati | Gujarat | "નવો પ્લાન્ટ", "કરોડનું રોકાણ" |
| Marathi | Maharashtra | "नवीन प्रकल्प", "कोटींची गुंतवणूक" |
| Tamil | Tamil Nadu | "புதிய தொழிற்சாலை" |
| Telugu | Telangana, Andhra Pradesh | "కొత్త పరిశ్రమ" |
| Kannada | Karnataka | "ಹೊಸ ಕಾರ್ಖಾನೆ" |
| Bengali | West Bengal | "নতুন কারখানা" |
| Odia | Odisha | "ନୂଆ କାରଖାନା" (fall back to Hindi and English if thin) |

Always confirm the company from its own website or registry data before accepting a news-derived lead.

---

## 5. Verification methods

### 5.1 Website decay audit (scripted: 1 point each, maximum 10)

Build `scripts/audit_website.py`. Fetch the homepage, the contact or about page, and one product page. Score one point for each:

1. Footer copyright year is 2020 or earlier, or there is no year at all.
2. Mentions withdrawn standards: **ISO 9001:2008, ISO 14001:2004 or OHSAS 18001.** All were superseded by 2021, so a page still showing them has not been updated since.
3. No HTTPS, or a certificate error.
4. No `<meta name="viewport">` tag (not mobile-friendly).
5. Official contact email on Gmail, Yahoo, Rediffmail or Hotmail.
6. Legacy tech: Flash or SWF, frames, `<marquee>`, visitor counters, "best viewed in", jQuery 1.x, WordPress generator tag below 5.0, table-based layout.
7. Mobile PageSpeed performance below 50 (use the PageSpeed Insights API if reachable; if not, skip this point and note it).
8. Broken images or links, placeholder or lorem ipsum text, "under construction".
9. Thin content: fewer than roughly 5 product or capability pages, no real plant photos, stock images only.
10. Corporate profile or brochure PDF: none downloadable, or the PDF metadata CreationDate is before 2021.

**No website at all = score 10**, tag `SEG-NOWEB`.

**Optional recency check:** Wayback Machine CDX API
`http://web.archive.org/cdx/search/cdx?url={domain}&output=json&fl=timestamp,digest&collapse=digest`
to estimate when the current design first appeared. If the current design first appears within the last 24 months AND the decay score is ≤ 2, reject R6.

Write Decay_Evidence as short text, for example: `© 2016; ISO 9001:2008; gmail contact; no viewport`.

### 5.2 Size verification (sets Size_Confidence)

- **High:** credit rating rationale, audited financials shown on public aggregator pages (Tofler, InstaFinancials, The Company Check), a DRHP, or the company's own disclosed figure with a financial year.
- **Medium:** IndiaMART or TradeIndia self-declared "Annual Turnover" band; a credible news figure; GST portal turnover slab (the GST taxpayer search has a captcha: mark it for manual check, never bypass it).
- **Low:** proxies only (employees, plant capacity, export volumes).

Always record Revenue_Source and Revenue_FY.

### 5.3 Popularity check (under 2 minutes per company, reject early)

Search `"{company}"` and `"{company}" news`. Check Wikipedia, NSE and BSE listing, and "subsidiary of" or "group company" wording.

### 5.4 Entity status

Check company status on public aggregator pages. Reject R11 if Strike Off, Under Liquidation or Dormant.

### 5.5 Time budget

Aim for about 6 minutes of tool calls per company. If identity or size cannot be established after reasonable effort, reject R12 or park it as Tier C with Manual_Check.

---

## 6. Sources playbook

### 6.1 Discovery order per cluster

1. Credit rating rationales (richest single source: revenue, promoters and capex in one document).
2. Environmental Clearance, Consent to Establish and public hearing notices.
3. Trade fair exhibitor lists and catalogues (6.2).
4. Export Promotion Council and industry association member directories (6.3).
5. Regional-language news (4.1).
6. B2B marketplaces (IndiaMART, TradeIndia, ExportersIndia): search-engine results and individual public profile pages only, for turnover band, year established, employee range and contact person.
7. Google Maps and business listings for "manufacturer" in named industrial areas (MIDC, GIDC, RIICO, SIDCUL, PSIEC, HSIIDC, UPSIDA and similar).
8. Job posts (trigger score 2).

### 6.2 Trade fairs to mine (find 2025 and 2026 editions, exhibitor lists or PDF catalogues)

IITF (Bharat Mandapam), IHGF Delhi Fair (India Expo Mart), Franchise India Expo, Aahar, ACMA Automechanika New Delhi, IMTEX (BIEC Bengaluru), Engimach (Gandhinagar), Plastindia and Plastivision, India Rubber Expo, ELECRAMA, CPHI and PMEC India, Pharmac, IIJS (Jio World and BEC Mumbai), Techtextil India, Kisan (Pune), EIMA Agrimach India, Stonemart (Jaipur), CODISSIA INTEC (Coimbatore), plus sector fairs at HITEX Hyderabad, Chennai Trade Centre, Auto Cluster Pune, Yashobhoomi (IICC Dwarka) and JECC Jaipur.

Also check Indian exhibitors in India pavilions at major foreign fairs: Hannover Messe, Automechanika Frankfurt, Canton Fair, Gulfood, Big 5 Dubai.

Exhibitor catalogues often list a contact person and mobile number published by the exhibitor. That is a valid self-published source. Record the URL.

### 6.3 Associations and export councils

- **Export Promotion Councils:** EEPC India, FIEO, CHEMEXCIL, PHARMEXCIL, PLEXCONCIL, TEXPROCIL, AEPC, CLE, EPCH, CAPEXIL, Sports Goods EPC, GJEPC.
- **Cluster associations (examples, discover more per cluster):** FOPSIA and UCPMA (Punjab), Faridabad Industries Association, Rajkot Engineering Association, Morbi Ceramic Association, CODISSIA and SIEMA (Coimbatore), MCCIA (Pune), MASSIA (Chhatrapati Sambhajinagar), KASSIA (Karnataka), public member lists of PHDCCI, CII and FICCI state chapters, and bullion and jewellery associations.

---

## 7. State-by-state coverage plan

The wave order is strategic:

- **Wave 1:** within driving distance of Abohar and Delhi. In-person factory visits are possible, so the close rate is highest.
- **Wave 2:** India's densest manufacturing states.
- **Wave 3:** mid-density states.
- **Wave 4:** quick scan only.

**Targets are upper bounds, not quotas:** Wave 1 up to 40 Active leads per state, Wave 2 up to 30, Wave 3 up to 15, Wave 4 up to 5. Fewer is fine.

**Cluster stop rule:** move to the next cluster when 3 consecutive discovery queries return no new qualifying candidates, or after 30 candidates screened in that cluster.

**Lead_ID codes:** PB, HR, DL, CH, RJ, HP, UK, UP, JK, GJ, MH, TN, KA, TG, MP, DD, AP, WB, OD, JH, CG, KL, GA, BR, PY, AS, ML, TR, SK, AR, MN, MZ, NL, LA, AN, LD. Format: `PB-001`.

### Wave 1

- **Punjab:** Ludhiana (hosiery, bicycles and parts, auto parts, hand tools, sewing machines), Jalandhar (sports goods, hand tools, rubber, pipe fittings, leather), Mandi Gobindgarh and Khanna (steel re-rolling, agri processing), Batala (foundry, agri implements, machine tools), Amritsar (textiles, food processing), Rajpura, Mohali and Derabassi (pharma, chemicals, engineering), Phagwara (auto parts), Bathinda, Abohar, Fazilka and Moga (cotton ginning, agri processing, dairy).
- **Haryana:** Faridabad (auto components, engineering), Gurugram, Manesar, Bawal and Dharuhera (auto components), Panipat (textiles, home furnishings, blankets), Sonipat, Kundli and Rai (food, engineering), Bahadurgarh (footwear), Yamunanagar and Jagadhri (plywood, utensils, metals), Karnal (agri implements, rice), Ambala (scientific instruments), Hisar (steel products).
- **Delhi:** Bawana, Narela, Okhla, Mayapuri, Wazirpur (steel), Naraina.
- **Chandigarh (UT):** Industrial Area Phase I and II.
- **Rajasthan:** Jaipur (Sitapura, VKI: engineering, textiles, gems), Bhiwadi, Neemrana and Alwar (auto, engineering), Jodhpur (handicrafts, guar gum, steel), Bhilwara (textiles), Kishangarh, Makrana and Udaipur (marble, minerals), Kota (stone, chemicals), Balotra (textile processing), Sri Ganganagar and Bikaner (edible oils, agri processing, namkeen).
- **Himachal Pradesh:** Baddi-Barotiwala-Nalagarh (pharma, FMCG), Kala Amb, Paonta Sahib, Parwanoo.
- **Uttarakhand:** Haridwar (SIDCUL), Rudrapur and Pantnagar, Kashipur, Selaqui, Sitarganj.
- **Uttar Pradesh (West and NCR belt):** Noida and Greater Noida (electronics, garments, engineering), Ghaziabad (engineering), Meerut (sports goods), Muzaffarnagar (paper, jaggery), Saharanpur (wood craft), Aligarh (locks, hardware), Moradabad (brassware), Agra (footwear, foundry), Khurja (ceramics), Firozabad (glass).
- **Jammu & Kashmir:** Jammu, Bari Brahmana, Kathua, Samba.

### Wave 2

- **Gujarat:** Rajkot (pumps, engines, auto parts, machine tools), Morbi, Wankaner and Thangadh (ceramic tiles, sanitaryware, clocks), Jamnagar (brass parts), Ahmedabad (Naroda, Vatva, Changodar, Sanand: pharma, textiles, engineering), Vapi, Ankleshwar, Bharuch and Dahej (chemicals, dyes), Surat (textiles), Vadodara (engineering, chemicals), Bhavnagar (plastics, ship-recycling linked), Mehsana and Kadi (cotton, edible oil), Gandhidham (timber, salt).
- **Maharashtra:** Pune (Chakan, Bhosari, Talegaon, Ranjangaon: auto, engineering), Chhatrapati Sambhajinagar (Waluj, Shendra: auto, pharma), Nashik (Ambad, Satpur: engineering, electrical), Kolhapur (foundry, auto), Ichalkaranji, Bhiwandi and Solapur (textiles, powerloom, towels), Thane, Taloja, Tarapur and Palghar (chemicals, pharma), Nagpur (Butibori, Hingna), Jalgaon (PVC pipes, dal mills, irrigation), Sangli and Satara (agri processing, engineering).
- **Tamil Nadu:** Coimbatore (pumps, motors, textile machinery, wet grinders, foundry), Tiruppur (knitwear), Karur (home textiles), Erode (textiles), Salem and Namakkal (steel, sago, truck body building), Hosur (auto, engineering), Chennai belt (Ambattur, Guindy, Sriperumbudur, Oragadam), Sivakasi (printing, packaging), Ranipet, Vellore, Ambur and Vaniyambadi (leather, footwear), Madurai, Rajapalayam.
- **Karnataka:** Bengaluru (Peenya, Bommasandra, Jigani: machine tools, engineering), Belagavi (foundry; skip aerospace), Hubballi-Dharwad, Mysuru, Tumakuru, Davanagere, Mangaluru.
- **Telangana:** Hyderabad (Jeedimetla, Patancheru, Balanagar, Cherlapally: pharma, bulk drugs, engineering), Sangareddy, Medak.
- **Madhya Pradesh:** Indore, Pithampur and Dewas (auto, pharma, engineering, food), Mandideep (Bhopal), Malanpur (Gwalior), Jabalpur, Ratlam, Neemuch.
- **Uttar Pradesh (rest):** Kanpur and Unnao (leather, textiles), Lucknow, Varanasi, Bhadohi and Mirzapur (carpets), Gorakhpur (GIDA), Prayagraj.
- **Dadra & Nagar Haveli and Daman & Diu:** Silvassa, Daman (plastics, textiles, packaging, engineering).

### Wave 3

- **Andhra Pradesh:** Visakhapatnam, Sri City, Nellore, Vijayawada (Auto Nagar), Guntur (chilli, spices), Kakinada (aqua feed, seafood), Anantapur.
- **West Bengal:** Howrah (engineering, foundry), Kolkata (Bantala leather), Durgapur and Asansol (steel, engineering), Haldia, Siliguri (tea processing).
- **Odisha:** Jharsuguda, Angul, Rourkela, Kalinga Nagar (metals, ancillaries), Cuttack, Balasore, Khordha.
- **Jharkhand:** Jamshedpur and Adityapur (auto components), Ranchi, Bokaro, Dhanbad.
- **Chhattisgarh:** Raipur (Urla, Siltara: steel, sponge iron, rolling), Bhilai, Korba.
- **Kerala:** Kochi (Kalamassery), Kollam (cashew), Alappuzha (coir), Kozhikode, Kannur.
- **Goa:** Verna, Kundaim (pharma, engineering).
- **Bihar:** Patna (Fatuha), Hajipur, Muzaffarpur, Bhagalpur (silk), Begusarai.
- **Puducherry:** industrial estates.

### Wave 4 (quick scan; mark N/A in the checklist if nothing qualifies)

Assam (Guwahati, tea, Tinsukia), Meghalaya (Byrnihat), Tripura (rubber), Sikkim (pharma), Arunachal Pradesh, Manipur, Mizoram, Nagaland, Ladakh, Andaman & Nicobar Islands, Lakshadweep.

---

## 8. Contact data rules (non-negotiable)

**Goal:** the owner or promoter's direct mobile, taken only from places where the owner or company published it themselves.

**Allowed sources for Owner_Mobile:**
- The company's own website (contact, about or management page).
- The company's own listings on IndiaMART, TradeIndia, ExportersIndia, Justdial or Google Business Profile, where the named contact person is the owner or a director.
- Publicly published trade fair exhibitor catalogues and association or EPC member directories.
- The owner's own public business profiles where a number is openly shown.

**Rules:**
- Every number needs an Owner_Mobile_Source_URL. No URL, no number.
- Never guess, construct or "complete" numbers or emails. Never mark a pattern-guessed email as found.
- Never use purchased, leaked or dumped databases, or Telegram and WhatsApp-group data lists.
- Never log in, and never bypass captchas, paywalls, rate limits or anti-bot measures. If blocked, add the URL to Manual_Check and move on.
- Do not fetch linkedin.com pages directly. Use search-engine result titles and snippets only, and store the LinkedIn URL from the result.
- Do not bulk-crawl IndiaMART, Justdial, TradeIndia or similar sites. Individual public page lookups only, at least 5 seconds between requests to the same domain, and respect robots.txt.
- Validate Indian mobiles: 10 digits starting with 6, 7, 8 or 9, stored as `+91 XXXXX XXXXX`. Landlines go in Company_Phone.
- If the only number found is a company line or a sales executive, put it in Company_Phone, leave Owner_Mobile blank and set Contact_Score accordingly.
- This data is for Giraffe's own one-to-one B2B outreach only.

---

## 9. People

- **Owner_Name and Owner_Designation:** from rating rationales ("promoted by"), the company website's management page, or the director list on public aggregator pages.
- **Next_Gen_Name (probable):** a director appointed in roughly the last 7 years who shares the founder's surname, or a family member shown as Director or Executive Director on the website or in LinkedIn search results. Always label it "(probable)" unless the company states the relationship.
- The next-gen successor is usually our internal champion; the founder usually holds the budget. Capture both wherever possible.

---

## 10. Scoring

### 10.1 Strength_Score (0–10)

| Component | Points |
|---|---|
| Revenue: ₹50–100 Cr = 1, ₹100–250 Cr = 2, ₹250–500 Cr = 3 | 0–3 |
| Proof points: certifications, exports, OEM or institutional clients, awards | 0–3 |
| Scale: plant capacity, multiple plants, 200+ employees | 0–2 |
| Longevity: 15+ years in business | 0–1 |
| Reach: dealer network in 3+ states, or exports to 3+ countries | 0–1 |

### 10.2 Visibility_Score (0–10)

| Component | Points |
|---|---|
| Website, from decay score: 0–2 → 4, 3–4 → 3, 5–6 → 2, 7–8 → 1, 9–10 → 0 | 0–4 |
| Corporate profile or brochure: current = 2, old = 1, none = 0 | 0–2 |
| LinkedIn company page: posts in last 90 days = 2, exists but inactive = 1, none = 0 | 0–2 |
| Google Business rating 4+ with 20+ reviews | 0–1 |
| Founder or leadership visible online (interviews, active LinkedIn) | 0–1 |

### 10.3 Gap_Score

`Gap_Score = Strength_Score − Visibility_Score` (range −10 to +10). This is the representation gap.

### 10.4 Trigger_Score (0–5)

Highest single trigger from Section 4, within the 18-month window.

### 10.5 Contact_Score (0–3)

- 3 = owner or director mobile, self-published, with source URL
- 2 = owner's direct email, or next-gen director's LinkedIn found
- 1 = company line or generic company email only
- 0 = nothing usable

### 10.6 Priority_Score

`Priority_Score = (Gap × 2) + (Trigger × 3) + (Contact × 2) + Wave bonus`
Wave bonus: Wave 1 = +3, Wave 2 = +1, others = 0.

### 10.7 Tier

- **A:** Gap ≥ 5 AND Trigger ≥ 3 AND Size_Confidence High or Medium AND Contact ≥ 2
- **B:** Gap ≥ 3 AND (Trigger ≥ 2 OR Contact ≥ 2)
- **C:** passes all gates but weaker, or Size_Confidence Low (with Manual_Check note)

### 10.8 Recommended_Offer (choose one primary)

- **EXPO KIT:** exhibitor with weak collateral. Website, brochure and catalogue, 3D stall, corporate profile.
- **ESSENTIALS + RETAINER:** ₹50–150 Cr.
- **PREMIUM + CAPITAL MARKETS:** ₹150–500 Cr, or tagged CAPMKT, or a Pvt to Public Ltd conversion.

### 10.9 Broadcast_Segments (multiple allowed, comma-separated)

`SEG-EXPO`, `SEG-EXPORT`, `SEG-FRANCHISE`, `SEG-AGRI`, `SEG-AUTO`, `SEG-ENGG`, `SEG-TEXTILE`, `SEG-CHEM-PHARMA`, `SEG-BUILDMAT`, `SEG-FOOD`, `SEG-JEWELLERY`, `SEG-NEXTGEN` (next-gen director found), `SEG-NOWEB` (no website), `CAPMKT`, `SEG-GIFTING` (Longterm_Broadcast only).

### 10.10 Pitch_Hook

One line, maximum 25 words. Humble, respectful Indian business register. Built ONLY from verified findings: one trigger plus one representation gap. No hype, no invented facts, no em dashes.

Shape examples (do not copy, adapt to the real findings):
- "Congratulations on the new Rajpura line, sir. When new buyers Google you, the website still shows 2016 plant photos."
- "Saw you exhibited at IMTEX 2026. After taking your card, buyers find a website that still lists ISO 9001:2008."

---

## 11. Output

### 11.1 Folder structure

```
./CLAUDE.md
./config/exclusions.txt        existing clients + manual exclusions, one per line
./config/states.json           built from Section 7 (wave, state, clusters, industries)
./input/                       optional user lists (e.g., Franchise India Expo database)
./data/leads.db                SQLite, single source of truth
./scripts/                     audit_website.py, wayback_check.py, score.py, dedupe.py, export_xlsx.py
./output/Giraffe_Leads_Master.xlsx
./output/Active_Pipeline.csv
./output/WAVE_{n}_SUMMARY.md
./progress/STATE_CHECKLIST.md
./progress/RUN_LOG.md
```

### 11.2 Files in `input/`

If `input/` contains files, process them BEFORE Wave 1: dedupe, apply the gates, audit websites, score, and write to the master. Tag each row with its source list name (for example `SRC-FRANCHISE-INDIA`) and add `SEG-FRANCHISE` where relevant.

### 11.3 Workbook: `output/Giraffe_Leads_Master.xlsx`

Sheets, in this order:
1. **Active_Pipeline**
2. **Longterm_Broadcast**
3. **Rejected**
4. **State_Coverage**
5. **Source_Log**
6. **Legend** (definition of every column, the scoring rules and all codes)

**Active_Pipeline columns, in this exact order:**

- **Priority:** Lead_ID, Tier, Priority_Score
- **Identity:** Company_Name, Industry, Key_Products, State, City_Cluster, Plant_Locations, Wave, Website_URL, Year_Established, Legal_Entity, CIN, GSTIN
- **Size:** Revenue_Estimate_Cr, Revenue_FY, Revenue_Source, Size_Confidence, Employees, Exporter_Markets, Certifications, Key_Clients
- **Representation:** Website_Decay_Score, Decay_Evidence, Corporate_Profile_Status, LinkedIn_Presence, Social_Presence, Google_Rating, Strength_Score, Visibility_Score, Gap_Score
- **Trigger:** Trigger_Type, Trigger_Detail, Trigger_Date, Trigger_Source_URL, Trigger_Score
- **People and contact:** Owner_Name, Owner_Designation, Owner_Mobile, Owner_Mobile_Source_URL, Owner_Email, Next_Gen_Name, Next_Gen_Role, Next_Gen_LinkedIn_URL, Company_Phone, Company_Email, Email_Type (own domain / Gmail etc.), Contact_Score
- **Checklist (Y/N):** G1_Manufacturer, G2_Size, G3_Not_Popular, G4_Weak_Representation, G5_Right_Segment, Trigger_Found, Owner_Contact_Found, Manual_Check (blank or a short note of what to verify)
- **Outreach:** Broadcast_Segments, Recommended_Offer, Pitch_Hook, Research_Notes, Date_Researched
- **Calling tracker (leave blank for the team):** Assigned_To, FU_Stage (0/1/2/3), Last_Contact_Date, Status, Next_Action, Drop_Reason

**Industry** must be one of: Auto Components, Engineering and Machinery, Pumps and Motors, Castings and Forgings, Steel and Metals, Wires and Cables, Electrical Equipment, Plastics and Packaging, Chemicals and Dyes, Pharma and API, Agri Inputs, Agri Machinery, Food Processing and Edible Oils, Dairy, Textiles and Yarn, Apparel and Hosiery, Home Textiles, Leather and Footwear, Ceramics and Tiles, Building Materials, Furniture, Wood and Plywood, Paper and Printing, Handicrafts and Home Decor, Sports Goods, Hand Tools and Hardware, Bicycles and Parts, Jewellery and Bullion, Rubber and Tyres, Glass, Electronics, Other.

**Sorting (Active_Pipeline):** Tier (A, B, C), then Priority_Score descending, then Wave ascending, then Revenue_Estimate_Cr descending.

**Formatting:** freeze the header row and the first 4 columns; auto-filter on; sensible column widths; wrap long text; Tier row colouring (A light green, B light amber, C light grey); clickable hyperlinks; dropdown validation on Status (New, Called No Pickup, Contacted, Sample Sent, Meeting Set, Proposal Sent, Won, Dropped) and FU_Stage (0, 1, 2, 3).

**Rejected columns:** Company_Name, State, City, Website_URL, Reject_Code, Reject_Evidence, Source_URL, Date.

**Reject codes:** R1 above ₹500 Cr; R2 below ₹50 Cr; R3 popular or known brand; R4 group, MNC or PE/VC backed; R5 main-board listed; R6 modern website or branding; R7 not a manufacturer; R8 wrong segment; R9 duplicate; R10 existing client; R11 inactive or struck off; R12 insufficient data after reasonable effort.

**Longterm_Broadcast columns:** the Identity and People and contact columns, plus Broadcast_Segments and Reason_For_Longterm.

**State_Coverage columns:** Wave, State, Clusters_Planned, Clusters_Done, Sources_Checked, Candidates_Screened, Tier_A, Tier_B, Tier_C, Longterm, Rejected, Status (Not Started / In Progress / Done / N/A), Last_Updated, Notes.

**Source_Log columns:** Date, Lead_ID or Company, Source_Type, URL, What_Was_Taken.

**CSV:** `output/Active_Pipeline.csv` mirrors Active_Pipeline (UTF-8 with BOM so Excel shows ₹ and Indian scripts correctly).

### 11.4 Progress checklist: `progress/STATE_CHECKLIST.md`

Update after EVERY cluster (not only every state), so a crashed or ended session loses nothing. Format:

```
## Wave 1
### Punjab [IN PROGRESS] screened: 42 | A: 6 | B: 9 | C: 4 | longterm: 2 | rejected: 21
- [x] Ludhiana: [x] ratings [x] EC/CTE [x] expos [x] associations [x] regional news [x] marketplaces [ ] jobs
- [ ] Jalandhar: [ ] ratings [ ] EC/CTE [ ] expos [ ] associations [ ] regional news [ ] marketplaces [ ] jobs
```

### 11.5 Run log: `progress/RUN_LOG.md`

Append one entry per session: date, states and clusters covered, counts by tier, blockers, sources that worked best, next step.

---

## 12. Execution loop (per cluster)

1. Discover candidates in the order of Section 6.1. Log every URL in Source_Log.
2. Dedupe against the DB. Key priority: GSTIN, then CIN, then website domain, then normalised company name + city.
3. Popularity and status screen (5.3, 5.4). Reject fast.
4. Website decay audit (5.1).
5. Size verification (5.2).
6. Trigger check (Section 4).
7. People and contacts (Sections 8 and 9).
8. Score and tier (Section 10). Write Pitch_Hook and Recommended_Offer.
9. Write to the DB. Update STATE_CHECKLIST.md.
10. After each STATE: export the xlsx and csv, update State_Coverage, append to RUN_LOG.md.
11. After each WAVE: write `output/WAVE_{n}_SUMMARY.md` containing the top 15 Tier A leads with a one-line reason each, the sources that yielded best, industries showing the most expansion, blockers, and a recommendation for the next wave. Then pause for the user.

---

## 13. Quality rules

- **Never fabricate.** Unknown = "Not found". Inferred values get "(inferred)".
- Every revenue figure, trigger and phone number needs a source URL.
- Keep your context lean: write findings to disk immediately, never paste full web pages into context, summarise.
- Spot-check at the end of each state: re-open 3 random Tier A leads and confirm the key fields still hold. Log the check in RUN_LOG.md.
- No em dashes in any generated text (hooks, notes, summaries). Use commas, colons or parentheses.
- Currency as ₹ and Cr. Dates as DD-MMM-YYYY.

---

## 14. First session

1. Create the folder structure, `config/states.json` from Section 7, and `config/exclusions.txt` with the existing clients listed in 3.2.
2. Build the scripts. Test `audit_website.py` on 5 real manufacturer websites and show the user the scores and evidence.
3. Process any files in `input/`.
4. Start Wave 1 with Punjab, Ludhiana.
5. **Calibration checkpoint:** stop after the first 10 Active leads. Show them to the user as a compact table (Company, City, Revenue + source, Decay evidence, Trigger, Owner contact found Y/N, Tier). Wait for feedback, adjust, then scale.
