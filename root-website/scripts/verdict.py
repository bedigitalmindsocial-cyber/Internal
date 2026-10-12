"""Record a reviewer's verdict for a page so it survives the session (review/NN-id/verdict.json).

Usage: python3 scripts/verdict.py NN pass|fix --score 84 [--must "s-hero: ..."]... [--note "..."] [--by reviewer]
Also sets the page memory status: pass -> reviewed, fix -> needs-fix.
"""
import argparse, datetime, hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

ap = argparse.ArgumentParser()
ap.add_argument("page"); ap.add_argument("verdict", choices=["pass", "fix"])
ap.add_argument("--score", type=int, default=0); ap.add_argument("--must", action="append", default=[])
ap.add_argument("--note", default=""); ap.add_argument("--by", default="reviewer")
a = ap.parse_args()
sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
page = next(p for p in sm["pages"] if f'{p["n"]:02d}' == a.page or p["id"] == a.page)
name = page["file"][:-5]
built = P("figma", page["file"])
sha = hashlib.sha1(open(built, "rb").read()).hexdigest()[:12] if os.path.exists(built) else None
os.makedirs(P("review", name), exist_ok=True)
rec = {"page": name, "verdict": a.verdict, "score": a.score, "must_fix": a.must, "note": a.note, "by": a.by,
       "sha": sha, "date": datetime.date.today().strftime("%d-%b-%Y")}
tmp = P("review", name, f"verdict.json.tmp{os.getpid()}")
json.dump(rec, open(tmp, "w"), indent=1, ensure_ascii=False)
os.replace(tmp, P("review", name, "verdict.json"))
mem = P("memory", "pages", name + ".md")
if os.path.exists(mem):
    s = open(mem, encoding="utf-8").read()
    s = re.sub(r"^status:.*$", "status: " + ("reviewed" if a.verdict == "pass" else "needs-fix"), s, count=1, flags=re.M)
    open(mem, "w", encoding="utf-8").write(s)
print(json.dumps(rec, ensure_ascii=False))
