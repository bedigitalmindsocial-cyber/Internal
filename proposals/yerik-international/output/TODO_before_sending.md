# TODO before sending (status: DRAFT deck built)

## Blockers
- [ ] **Network access.** This cloud session's egress policy blocked yerikindia.com, both competitor sites, web.archive.org and all directories. Either allow these hosts in the environment settings, or run `node scripts/capture.mjs` on a local machine. Until then there are no screenshots and no page counts.
- [ ] **Domain.** The brief says `yerikinternational.com`, which does not resolve. The live site is `www.yerikindia.com`. Confirm with Rajveer.
- [ ] **Timing.** Go-ahead must come 35 days before the show. If the show is in early November, that date is now. Get the show date first.

## Screenshots (all missing)
| File | Source | Status |
|---|---|---|
| 01_home_desktop | capture.mjs | Missing (blocked) |
| 02_home_mobile | capture.mjs | Missing (blocked) |
| 03_phone_number | capture.mjs | Missing (blocked) |
| 04_product_page | capture.mjs | Missing (blocked) |
| 05_careers_form | capture.mjs (fills, never submits) | Missing (blocked) |
| 06_competitor_jrs | capture.mjs, `JRS_URL` (default jrsparts.com) | Missing. Confirm URL Disha showed |
| 07_competitor_machineparts | capture.mjs, `MP_URL` (default machineparts.co.in) | Missing. Confirm URL |
| 08_google_profile | `inputs/manual-screenshots/` | Missing. Capture unrelated photos and videos. Blur faces and names |
| 09_linkedin_pages | `inputs/manual-screenshots/` | Missing. Both pages named Yerik International. Crop out any other group company |
| 10_hiring_post | `inputs/manual-screenshots/` | Missing. One off-brand hiring post. Blur people |

## Other inputs missing
- [ ] `inputs/OPR_Yerik.pdf` (to confirm D01 2/10 and D02 1.5/10 scores)
- [ ] Giraffe Partners logo in `brand/`. The logo in giraffe-website/public/logo.png is **Life With Giraffe**: do not use.
- [ ] Fonts: the .pptx uses **Cambria** (titles, display) and **Calibri** (body) as fallbacks for PP Editorial New / Coolvetica / Neue Montreal, because those must be installed on every machine that opens a .pptx. Swap the `F` map in `scripts/build_pptx.js` if you want the brand fonts and they are installed.
- [ ] Slide 12 wireframe uses a placeholder orange (`E8772E`) for the dot accent. Replace with Yerik's exact orange once the brand sheet fixes it.
- [ ] Slide 16 due days for items 3 to 10 were proposed by Claude. Check them.
- [ ] Neev Seeds before/after images in `inputs/neev/` (optional)

## Placeholders in work/deck-content.yaml
Run `python3 scripts/lint_content.py` for the live list. Current build: 7 `[[PRICE]]` and 28 `[[CONFIRM]]` (shown highlighted in lilac in the deck).
