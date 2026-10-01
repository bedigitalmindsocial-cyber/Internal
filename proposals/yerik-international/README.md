# Yerik International: 30-day proposal deck

Source brief: the Yerik proposal prompt (Lovish, 01-Oct-2026). Call notes: `inputs/Yerik_MOM.pdf`.

**Status: DRAFT deck built** (`output/Yerik_Proposal_DRAFT.pptx` + `.pdf`). 7 prices, 28 confirm items and all 10 screenshots still open: see `output/TODO_before_sending.md`.

## Files
| Path | What |
|---|---|
| `work/facts.md` | Every fact the deck may use, with its source, plus conflicts (C1–C14) |
| `work/deck-content.yaml` | **All slide text and prices. Edit this file to add prices.** |
| `work/sitemaps/current.md`, `new.md` | Site maps (current one from search index only) |
| `scripts/lint_content.py` | Checks banned words, em dashes, `!`, 40-word limit; lists placeholders |
| `scripts/capture.mjs` | Gentle crawl + raw screenshots. Never submits a form |
| `scripts/build_pptx.js`, `scripts/to_pdf.py` | Deck builder (.pptx) and PDF export |
| `output/TODO_before_sending.md` | Everything still missing |
| `output/cover_message.txt` | Draft WhatsApp/email note from Disha |

## Commands
```bash
python3 scripts/lint_content.py              # language rules + placeholder list
node scripts/capture.mjs                     # needs access to yerikindia.com + competitor sites
JRS_URL=https://... MP_URL=https://... node scripts/capture.mjs   # override competitor URLs
```
## Build the deck
```bash
npm install                 # once: pptxgenjs, js-yaml
npm run deck                # builds output/*.pptx, then PDF via LibreOffice (needs Impress)
```
- Edit prices and wording in `work/deck-content.yaml` only, then rebuild.
- While any `[[PRICE]]` or `[[CONFIRM...]]` is left, the file is `Yerik_Proposal_DRAFT` with a DRAFT watermark and placeholders highlighted in lilac. With none left it becomes `Yerik_Proposal_v1`.
- Screenshots: drop `01_home_desktop.jpg` etc. into `work/screenshots/annotated/` (or `raw/`, or `inputs/manual-screenshots/` for 08–10). Grey "Screenshot needed" boxes are replaced on the next build.
- If bare `soffice` hangs, set `SOFFICE` to a wrapper command.
