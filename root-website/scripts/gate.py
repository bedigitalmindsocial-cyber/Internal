"""Gate: build + lint + shoot one page and print ONE JSON line (agents return it verbatim).

ok = the page built cleanly, lint has no errors, there is no overflow at 1440 or 390, and no placeholder
chip sits in the first screen at 1440 outside fine print (design direction v3).
Also writes review/NN-id/gate.json. Usage: python3 scripts/gate.py NN   (Bash timeout 300000)
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)


def run(cmd):
    r = subprocess.run([sys.executable, P("scripts", cmd[0])] + cmd[1:], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, (r.stdout + r.stderr)[-3000:]


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    page = next((p for p in sm["pages"] if f'{p["n"]:02d}' == argv[0] or p["id"] == argv[0]), None)
    if not page:
        print(json.dumps({"ok": False, "error": f"unknown page {argv[0]}"}))
        return 1
    name = page["file"][:-5]
    out = {"page": name, "ok": False}
    if not os.path.exists(P("pages", "src", page["file"])):
        out["error"] = "no source file"
        print(json.dumps(out))
        return 1
    code, log = run(["build.py", argv[0]])
    out["build_ok"] = code == 0
    if code != 0:
        out["build_log"] = log.strip().splitlines()[-3:]
    run(["lint.py", argv[0]])
    run(["shoot.py", argv[0]])
    lint = json.load(open(P("review", name, "lint.json"))) if os.path.exists(P("review", name, "lint.json")) else {}
    shots = json.load(open(P("review", name, "shots.json"))) if os.path.exists(P("review", name, "shots.json")) else {}
    out.update({
        "lint_errors": lint.get("errors", ["lint did not run"]), "lint_reviews": len(lint.get("reviews", [])),
        "overflow": bool(shots) and (shots["desktop"]["overflow"] or shots["mobile"]["overflow"]),
        "slices": {"desktop": shots.get("desktop", {}).get("slices"), "mobile": shots.get("mobile", {}).get("slices")},
        "states": lint.get("states", 0), "placeholders": lint.get("placeholders"),
        "notes": shots.get("notes", []), "sha": lint.get("sha"),
    })
    out["first_screen_placeholders"] = shots.get("desktop", {}).get("first_screen_ph", [])
    out["ok"] = (out["build_ok"] and not out["lint_errors"] and bool(shots) and not out["overflow"]
                 and not out["first_screen_placeholders"])
    tmp = P("review", name, f"gate.json.tmp{os.getpid()}")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, P("review", name, "gate.json"))
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
