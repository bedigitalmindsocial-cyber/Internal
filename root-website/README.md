# ROOT by Aikyam: 75-page website build

Self-contained HTML pages in ROOT theme v1, built by a multi-agent workflow and handed to a UI/UX designer through Figma.

## For the designer: import into Figma
1. Open `figma/index.html` to see every page and its status.
2. Import a page with the html.to.design plugin: either open `figma/NN-name.html` in Chrome and capture it with the html.to.design Chrome extension, or host the `figma/` folder (any static host) and import by URL in the plugin. Capture at **1440** (desktop) and **390** (mobile) widths.
3. Install the three Google fonts in Figma first: Tiro Devanagari Hindi, Mukta, Red Hat Mono.
4. Gold-wash chips and dashed boxes (`.ph`) are placeholders for values Aikyam must confirm or images to source. Keep them visible until confirmed.
5. Each page's design decisions, rejected options, open questions and notes for you are in `memory/pages/NN-name.md`.

## For whoever runs the build
```
python3 scripts/status.py                 # where every page stands -> STATUS.md
python3 scripts/build.py [NN ...]         # wrap sources in the shell -> figma/
python3 scripts/lint.py [NN ...]          # claims, disclosures, headings, links -> review/NN-name/lint.json
python3 scripts/shoot.py [NN ...]         # 1440 and 390 screenshots + overflow check -> review/NN-name/
python3 scripts/make_sitemap.py           # regenerate sitemap.json after editing the page table
```
Screenshots need Playwright (`pip install playwright`) and the Chromium at /opt/pw-browsers (cloud sessions) or `playwright install chromium`.

The method is in `WORKFLOW.md` and `rules/page-method.md`. The workflow script for a wave is in `workflow/`.
