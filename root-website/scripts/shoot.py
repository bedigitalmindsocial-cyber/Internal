"""Render built pages in Chromium and save review screenshots, plus layout checks.

For each figma/NN-id.html:
  review/NN-id/desktop.png        full page at 1440 wide (for people)
  review/NN-id/desktop-01.png ... 1440 x 1400 slices (for reviewer agents, one screen at a time)
  review/NN-id/mobile.png         full page at 390 wide
  review/NN-id/mobile-01.png ...  390 x 1400 slices
Checks: horizontal overflow (elements wider than the viewport) at both widths, and whether the brand
fonts loaded (if Google Fonts is blocked, screenshots use fallbacks: layout is still checkable).

Usage: python3 scripts/shoot.py [NN|id ...]
"""
import glob, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
CHROME = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome") or [None])[0]
SLICE = 1400

OVERFLOW_JS = """() => {
  const w = document.documentElement.clientWidth, out = [];
  for (const el of document.querySelectorAll('main *, header *, footer *')) {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > w + 1 || r.left < -1)) {
      const s = getComputedStyle(el);
      if (s.position === 'fixed' || s.visibility === 'hidden' || s.opacity === '0') continue;
      let p = el.parentElement, clipped = false;
      while (p) { const ps = getComputedStyle(p); if (/(hidden|auto|scroll|clip)/.test(ps.overflowX)) { clipped = true; break; } p = p.parentElement; }
      if (!clipped) out.push((el.className && el.className.baseVal === undefined ? '.' + String(el.className).trim().split(/\\s+/).join('.') : el.tagName.toLowerCase()) + ' right=' + Math.round(r.right));
    }
  }
  return {scrollWidth: document.documentElement.scrollWidth, width: w, offenders: [...new Set(out)].slice(0, 8)};
}"""


def shoot(page_file, pw):
    name = page_file[:-5]
    out_dir = P("review", name)
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, "*.png")):
        os.remove(f)  # only this page's folder
    result = {"file": page_file}
    browser = pw.chromium.launch(executable_path=CHROME) if CHROME else pw.chromium.launch()
    for label, width in (("desktop", 1440), ("mobile", 390)):
        ctx = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto("file://" + P("figma", page_file), wait_until="load", timeout=30000)
        try:
            pg.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        fonts = pg.evaluate("() => ['Mukta','Tiro Devanagari Hindi'].map(f => document.fonts.check('16px \"' + f + '\"'))")
        ov = pg.evaluate(OVERFLOW_JS)
        height = pg.evaluate("() => document.documentElement.scrollHeight")
        pg.screenshot(path=os.path.join(out_dir, f"{label}.png"), full_page=True)
        n = 0
        for top in range(0, height, SLICE):
            n += 1
            pg.screenshot(path=os.path.join(out_dir, f"{label}-{n:02d}.png"), full_page=True,
                          clip={"x": 0, "y": top, "width": width, "height": min(SLICE, height - top)})
        result[label] = {"height": height, "slices": n, "fonts_loaded": all(fonts),
                         "overflow": ov["scrollWidth"] > ov["width"] + 1 or bool(ov["offenders"]),
                         "offenders": ov["offenders"]}
        ctx.close()
    browser.close()
    return result


def main(argv):
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    want = set(argv)
    files = [p["file"] for p in sm["pages"] if os.path.exists(P("figma", p["file"]))
             and (not want or f'{p["n"]:02d}' in want or p["id"] in want)]
    results = []
    with sync_playwright() as pw:
        for f in files:
            r = shoot(f, pw)
            results.append(r)
            d, m = r["desktop"], r["mobile"]
            print(f'{f:40s} desktop {d["height"]:5d}px x{d["slices"]:2d}  mobile {m["height"]:5d}px x{m["slices"]:2d}'
                  f'  fonts {"ok" if d["fonts_loaded"] else "FALLBACK"}'
                  + (f'  OVERFLOW desktop {d["offenders"]}' if d["overflow"] else "")
                  + (f'  OVERFLOW mobile {m["offenders"]}' if m["overflow"] else ""))
    for r in results:  # one file per page, so parallel agents never overwrite each other
        json.dump(r, open(P("review", r["file"][:-5], "shots.json"), "w"), indent=1)
    return 1 if any(r["desktop"]["overflow"] or r["mobile"]["overflow"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
