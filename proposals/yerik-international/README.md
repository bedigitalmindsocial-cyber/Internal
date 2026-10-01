# Yerik International: 30-day proposal deck

Source brief: the Yerik proposal prompt (Lovish, 01-Oct-2026). Call notes: `inputs/Yerik_MOM.pdf`.

**Status: checkpoint (brief section 13).** Facts, site maps and slide content are drafted. Screenshots are not captured and the visual deck is not built yet.

## Files
| Path | What |
|---|---|
| `work/facts.md` | Every fact the deck may use, with its source, plus conflicts (C1–C14) |
| `work/deck-content.yaml` | **All slide text and prices. Edit this file to add prices.** |
| `work/sitemaps/current.md`, `new.md` | Site maps (current one from search index only) |
| `scripts/lint_content.py` | Checks banned words, em dashes, `!`, 40-word limit; lists placeholders |
| `scripts/capture.mjs` | Gentle crawl + raw screenshots. Never submits a form |
| `output/TODO_before_sending.md` | Everything still missing |
| `output/cover_message.txt` | Draft WhatsApp/email note from Disha |

## Commands
```bash
python3 scripts/lint_content.py              # language rules + placeholder list
node scripts/capture.mjs                     # needs access to yerikindia.com + competitor sites
JRS_URL=https://... MP_URL=https://... node scripts/capture.mjs   # override competitor URLs
```
The deck build command (`python3 build.py`: HTML at 1920×1080 → PDF via Playwright, DRAFT watermark while placeholders remain) is added after the checkpoint is approved.
