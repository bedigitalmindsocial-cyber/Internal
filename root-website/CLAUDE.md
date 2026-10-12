# ROOT by Aikyam website build (this folder only)

This folder is a separate project from the lead engine in the repo root. When working here, the repo-root CLAUDE.md (manufacturer leads) does not apply.

## What this is
75 self-contained HTML pages for rootbyaikyam.com (ROOT by Aikyam: Aikyam Capital broking + Aikyam Wealth mutual fund distribution), built in ROOT theme v1, for import into Figma and refinement by a UI/UX designer.

## Start of every session
1. Run `python3 scripts/status.py` and read `STATUS.md`, `WORKFLOW.md`, `memory/site.md` and the open rows of `memory/questions.md`.
2. Tell the user in 3 lines where the build stands (pages done by status, current wave, questions waiting on them), then continue the current wave. Never redo a page whose memory status is `approved` unless the user asks.

## Files
- `sitemap.json` (from `scripts/make_sitemap.py`): the 75 pages, templates, entities, flags, golden/derivative.
- `context/`: business facts and decisions from earlier sessions (non-confidential). `private/` is gitignored and holds the confidential fact base and the original theme artifact.
- `rules/`: the page method, HTML rules, voice and claims, compliance blocks.
- `theme/`: theme CSS, extensions (`patterns.css`), icons, `sections-reference.html` (theme homepage sections as a pattern source).
- `shell/`: header, footer, minimal header, short footer, announcement bar, mobile bar.
- `pages/src/`: what agents write (sections + front matter). `figma/`: built, self-contained pages for Figma import.
- `memory/`: page memories, site decisions, pattern library, question log.
- `review/`: screenshots and per-page lint and layout reports (gitignored).
- `workflow/`: the workflow script used to run waves.

## Rules that never bend
No invented numbers, claims, legal text, testimonials or ratings: use `<mark class="ph">` placeholders. Name the Aikyam company on every conversion. No em dashes. No JavaScript in pages. Mandatory disclosures by sitemap flag.
