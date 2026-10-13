"""Print the Workflow `args` for a run: python3 workflow/wave_args.py 01 09 10 > /tmp/args.json
Also writes each page's brief (scripts/pack.py) so agents start from one file."""
import json, os, subprocess, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sm = json.load(open(os.path.join(ROOT, "sitemap.json"), encoding="utf-8"))
want = set(sys.argv[1:])
pages = []
for p in sm["pages"]:
    if f'{p["n"]:02d}' in want or p["id"] in want:
        q = dict(p)
        q["template_desc"] = sm["templates"][p["template"]]
        pages.append(q)
subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "pack.py")] + [f'{p["n"]:02d}' for p in pages],
               check=True, capture_output=True)
print(json.dumps({"date": datetime.date.today().strftime("%d-%b-%Y"), "pages": pages}, ensure_ascii=False))
