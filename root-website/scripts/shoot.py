"""Render built pages in Chromium: review screenshots plus layout checks.

For each figma/NN-id.html:
  review/NN-id/desktop.png, mobile.png       full page at 1440 and 390 wide (for people)
  review/NN-id/desktop-01.png ...            1440 x 1400 slices of the header + page body (for reviewer agents;
  review/NN-id/mobile-01.png ...             the shared footer is left out of the slices)
  review/NN-id/states-desktop.png            the states board, if the page has one
  review/NN-id/shots.json                    the checks below, with the sha of the file that was shot
Checks: horizontal overflow at both widths; whether the brand fonts loaded; where the [data-primary] action sits
(it should be inside the first screen at 1440 and within the first 1.5 screens at 390).

At most 4 Chromium renders run at once across all parallel agents (file-lock semaphore), and each page renders
into a temp folder that is swapped in at the end, so a killed run keeps the previous screenshots.
Usage: python3 scripts/shoot.py [NN|id ...]     (give agents a 300000 ms Bash timeout)
"""
import fcntl, glob, hashlib, json, os, shutil, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
CHROME = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome") or [None])[0]
SLICE, SLOTS = 1400, 4

OVERFLOW_JS = """() => {
  const w = document.documentElement.clientWidth, out = [];
  for (const el of document.querySelectorAll('main *, header *, footer *')) {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > w + 1 || r.left < -1)) {
      const s = getComputedStyle(el);
      if (s.position === 'fixed' || s.visibility === 'hidden' || s.opacity === '0' || s.display === 'none') continue;
      let p = el.parentElement, clipped = false;
      while (p) { const ps = getComputedStyle(p); if (/(hidden|auto|scroll|clip)/.test(ps.overflowX)) { clipped = true; break; } p = p.parentElement; }
      if (!clipped) out.push((typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\\s+/).join('.') : el.tagName.toLowerCase()) + ' right=' + Math.round(r.right));
    }
  }
  return {scrollWidth: document.documentElement.scrollWidth, width: w, offenders: [...new Set(out)].slice(0, 8)};
}"""
GEOM_JS = """() => {
  const main = document.querySelector('main'), prim = document.querySelector('main [data-primary]');
  const r = prim ? prim.getBoundingClientRect() : null;
  return {mainBottom: main ? Math.ceil(main.getBoundingClientRect().bottom + scrollY) : document.documentElement.scrollHeight,
          primaryTop: r ? Math.round(r.top + scrollY) : null,
          primaryText: prim ? prim.textContent.trim().slice(0, 40) : null};
}"""


class Slot:
    """Cross-process semaphore: take one of SLOTS lock files, waiting if all are busy."""
    def __enter__(self):
        os.makedirs(P("review", ".locks"), exist_ok=True)
        while True:
            for i in range(SLOTS):
                fh = open(P("review", ".locks", f"chromium-{i}.lock"), "w")
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.fh = fh
                    return self
                except BlockingIOError:
                    fh.close()
            time.sleep(1.5)

    def __exit__(self, *a):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()


def render(pw, path, out_dir, label, width, slice_to_main=True):
    browser = pw.chromium.launch(executable_path=CHROME) if CHROME else pw.chromium.launch()
    try:
        ctx = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto("file://" + path, wait_until="load", timeout=60000)
        try:
            pg.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        fonts = pg.evaluate("() => ['Mukta','Tiro Devanagari Hindi'].map(f => document.fonts.check('16px \"' + f + '\"'))")
        ov = pg.evaluate(OVERFLOW_JS)
        geo = pg.evaluate(GEOM_JS)
        height = pg.evaluate("() => document.documentElement.scrollHeight")
        pg.screenshot(path=os.path.join(out_dir, f"{label}.png"), full_page=True)
        end = min(height, geo["mainBottom"] + 40) if slice_to_main else height
        n = 0
        for top in range(0, end, SLICE):
            n += 1
            pg.screenshot(path=os.path.join(out_dir, f"{label}-{n:02d}.png"), full_page=True,
                          clip={"x": 0, "y": top, "width": width, "height": min(SLICE, end - top)})
        return {"height": height, "slices": n, "fonts_loaded": all(fonts),
                "overflow": ov["scrollWidth"] > ov["width"] + 1 or bool(ov["offenders"]), "offenders": ov["offenders"],
                "primary_top": geo["primaryTop"], "primary_text": geo["primaryText"]}
    finally:
        browser.close()


def shoot(page_file, pw):
    name = page_file[:-5]
    final_dir = P("review", name)
    tmp_dir = P("review", f".tmp-{name}-{os.getpid()}")
    os.makedirs(tmp_dir, exist_ok=True)
    path = P("figma", page_file)
    sha = hashlib.sha1(open(path, "rb").read()).hexdigest()[:12]
    result = {"file": page_file, "sha": sha}
    with Slot():
        for label, width in (("desktop", 1440), ("mobile", 390)):
            result[label] = render(pw, path, tmp_dir, label, width)
        states = P("figma", page_file.replace(".html", ".states.html"))
        if os.path.exists(states):
            result["states_board"] = render(pw, states, tmp_dir, "states-desktop", 1440, slice_to_main=False)
    d, m = result["desktop"], result["mobile"]
    notes = []
    if d["primary_top"] is None:
        notes.append("no [data-primary] element")
    else:
        if d["primary_top"] > 900:
            notes.append(f"primary action starts at {d['primary_top']}px on desktop (below the first screen)")
        if m["primary_top"] is not None and m["primary_top"] > 1266:
            notes.append(f"primary action starts at {m['primary_top']}px on mobile (below 1.5 screens)")
    result["notes"] = notes
    os.makedirs(final_dir, exist_ok=True)
    for f in glob.glob(os.path.join(final_dir, "*.png")):
        os.remove(f)
    for f in os.listdir(tmp_dir):
        os.replace(os.path.join(tmp_dir, f), os.path.join(final_dir, f))
    shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp = os.path.join(final_dir, f"shots.json.tmp{os.getpid()}")
    json.dump(result, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(final_dir, "shots.json"))
    return result


def main(argv):
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    want = set(argv)
    files = [p["file"] for p in sm["pages"] if os.path.exists(P("figma", p["file"]))
             and (not want or f'{p["n"]:02d}' in want or p["id"] in want)]
    bad = False
    with sync_playwright() as pw:
        for f in files:
            r = shoot(f, pw)
            d, m = r["desktop"], r["mobile"]
            bad = bad or d["overflow"] or m["overflow"]
            print(f'{f:40s} desktop {d["height"]:5d}px x{d["slices"]:2d}  mobile {m["height"]:5d}px x{m["slices"]:2d}'
                  f'  fonts {"ok" if d["fonts_loaded"] else "FALLBACK"}'
                  + (f'  states-board {r["states_board"]["height"]}px' if "states_board" in r else "")
                  + (f'  OVERFLOW desktop {d["offenders"]}' if d["overflow"] else "")
                  + (f'  OVERFLOW mobile {m["offenders"]}' if m["overflow"] else "")
                  + ("".join(f"  NOTE {n}" for n in r["notes"])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
