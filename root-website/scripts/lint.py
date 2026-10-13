"""Automatic checks on built pages (figma/NN-id.html). Cheap; run on every page, every time.

Errors block a page; reviews go to the reviewer agent. Checks:
  structure   one h1, no skipped heading levels, every <section> has an id="s-...", a [data-primary] action,
              no <script>, no <use> or {{token}} left, <img> has alt, internal links resolve
  copy        em dashes; claims registry (rules/claims.json): blocked, unconfirmed (only inside a placeholder),
              review; invented-number patterns. Visible text, alt/aria-label/title attributes, title and description.
  compliance  disclosures required by sitemap flags, checked inside <main> only (the header mega menu also carries
              the F&O line, so a whole-document check would pass by accident); F&O box placement; PMS facts;
              topics on the page that suggest a missing flag (review)
  seo         title length, description present and length, unique titles and descriptions across built pages,
              at least 3 internal links in the page body
  states      template D pages need 3+ interaction states; pages with a form need 2+ (error and success)
  trace       every section id named in the page memory's question table (section 4) exists on the page
Front matter "lint_allow": ["sub-broker", ...] downgrades those matched words from error to review
(the reviewer must agree they are needed, e.g. explaining that sub-brokers became Authorised Persons).

Usage: python3 scripts/lint.py [NN|id ...]   (default: every built page)
Writes review/NN-id/lint.json (atomic). Exit 1 if any page has an error.
"""
import json, os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

NEGATED = re.compile(r"\b(not|no|never|cannot|in no way|does not|do not|nor)\b[^.]*$", re.I)
NUMBER_CLAIM = re.compile(
    r"\b\d[\d,.]*\s*(\+|lakh\+?|lakhs|crore\+?|cr\+?|mn\+?|million\+?|k\+)?\s*"
    r"(clients|customers|investors|users|traders|downloads|accounts|AMCs|schemes|funds|partners|cities|branches|years of)\b", re.I)
FO_BULLETS = ["9 out of 10 individual traders", "loss makers registered net trading loss",
              "additional 28% of net trading losses", "15% to 50% of such profit"]
REQUIRED = {
    "mf_risk": (r"mutual fund investments are subject to market risks", "MF risk line missing in the page body"),
    "distributor_disclaimer": (r"not exchange[- ]traded products", "distributor disclaimer missing in the page body"),
    "coming_soon": (r'class="soon"|\bComing soon\b', "Coming-soon badge missing in the page body"),
    "illustrative_data": (r"\billustrative\b", "Illustrative-data label missing in the page body"),
}
TOPIC_HINTS = [  # (pattern in page body, flag that should then be present, message)
    (r"\bmutual funds?\b|\bSIPs?\b", "mf_risk", "page talks about mutual funds: add the MF risk line?"),
    (r"\bF&amp;O\b|\bF&O\b|\bfutures\b|\boptions trading\b|\bderivatives?\b", "fo_risk", "page talks about F&O: add the F&O risk box?"),
]


def text_of(doc):
    doc = re.sub(r"<(style|script|template)[^>]*>.*?</\1>", " ", doc, flags=re.S)
    doc = re.sub(r"<!--.*?-->", " ", doc, flags=re.S)
    doc = re.sub(r"<svg.*?</svg>", " ", doc, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", doc)).replace("&amp;", "&")


def main_of(doc):
    m = re.search(r"<main[^>]*>(.*)</main>", doc, re.S)
    return m.group(1) if m else doc


def sections_of(main):
    out = []
    for m in re.finditer(r"<section\b([^>]*)>", main):
        sid = re.search(r'\bid="([^"]*)"', m.group(1))
        out.append((m.start(), sid.group(1) if sid else "", m.group(0)))
    return out


def section_body(main, sid):
    m = re.search(r'<section\b[^>]*id="%s"[^>]*>(.*?)</section>' % re.escape(sid), main, re.S)
    return m.group(1) if m else ""


def attr_text(doc, main):
    parts = re.findall(r'\b(?:alt|aria-label|title)="([^"]*)"', main)
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', doc)
    return " ".join(parts + [t.group(1) if t else "", d.group(1) if d else ""])


def load_front(page):
    src = P("pages", "src", page["file"])
    if not os.path.exists(src):
        return {}
    m = re.search(r"<!--page\s*(\{.*?\})\s*-->", open(src, encoding="utf-8").read(), re.S)
    try:
        return json.loads(m.group(1)) if m else {}
    except json.JSONDecodeError:
        return {}


def trace_ids(page):
    path = P("memory", "pages", page["file"][:-5] + ".md")
    if not os.path.exists(path):
        return None
    md = open(path, encoding="utf-8").read()
    m = re.search(r"## 4\..*?\n(.*?)\n## ", md, re.S)
    if not m:
        return []
    rows = [r for r in m.group(1).splitlines() if r.startswith("|") and not re.match(r"\|\s*-", r)][1:]  # drop the header row
    out = []
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        must = any(c.upper() == "MUST" for c in cells)
        out.append((must, re.findall(r"\bs-[a-z0-9-]+", r)))
    return out


def lint(page, claims, cta_label):
    path = P("figma", page["file"])
    doc = open(path, encoding="utf-8").read()
    main = main_of(doc)
    front = load_front(page)
    allow = [a.lower() for a in front.get("lint_allow", [])]
    vis = text_of(main)
    vis_no_ph = text_of(re.sub(r'<mark class="ph[^"]*"[^>]*>.*?</mark>|<div class="ph ph--block"[^>]*>.*?</div>', " ", main, flags=re.S))
    attrs = attr_text(doc, main)
    errors, reviews = [], []

    def hit(sev, msg, words):
        words = sorted(set(words))
        if sev == "error" and words and all(w.lower() in allow for w in words):
            reviews.append(f"{msg}: {', '.join(words[:4])} (allowed by front matter; reviewer to confirm)")
        else:
            (errors if sev == "error" else reviews).append(f"{msg}: {', '.join(words[:4])}")

    # structure
    heads = [int(h) for h in re.findall(r"<h([1-6])[\s>]", main)]
    if heads.count(1) != 1:
        errors.append(f"expected exactly one h1 in the page body, found {heads.count(1)}")
    for a, b in zip(heads, heads[1:]):
        if b > a + 1:
            errors.append(f"heading level skips from h{a} to h{b}")
            break
    secs = sections_of(main)
    bad_ids = [sid or "(no id)" for _, sid, _ in secs if not sid.startswith("s-")]
    if bad_ids:
        errors.append(f"section ids must start with 's-': {bad_ids[:5]}")
    if "data-primary" not in main:
        errors.append("no element marked data-primary (the page's primary action)")
    if "<script" in doc:
        errors.append("contains <script>; pages must be static")
    if "<use" in doc or "{{" in doc:
        errors.append("unexpanded <use> icon or {{token}} left in the output")
    if re.findall(r"<img(?![^>]*\balt=)[^>]*>", main):
        errors.append("<img> without alt")
    unresolved = sorted(set(re.findall(r'href="(/[^"]*)"', doc)))
    if unresolved:
        errors.append(f"unresolved internal links: {unresolved[:6]}")
    bad_style = [s for s in re.findall(r'style="([^"]*)"', main) if not all(
        d.strip().startswith("--") for d in s.split(";") if d.strip())]
    if bad_style:
        reviews.append(f"{len(bad_style)} inline style(s) beyond custom properties, e.g. '{bad_style[0][:60]}'")

    # copy and claims
    if "—" in vis or re.search(r"(?<![\d%])\s–\s|\s–\s(?![\d₹])", vis):
        errors.append("em dash or spaced en dash in copy (use commas, colons or parentheses)")
    scan = vis + " " + attrs
    for pat, msg in claims["blocked"]:
        words = [m.group(0) for m in re.finditer(pat, scan, re.I)
                 if not ("guarantee" in m.group(0).lower() and NEGATED.search(scan[max(0, m.start() - 40):m.start()]))]
        if words:
            hit("error", msg, words)
    scan_no_ph = vis_no_ph + " " + attrs
    for pat, msg in claims["unconfirmed"]:
        words = [m.group(0) for m in re.finditer(pat, scan_no_ph, re.I)]
        if words:
            hit("error", f"unconfirmed claim outside a placeholder ({msg})", words)
    scan_review = scan.replace(cta_label, " ").replace("toll-free", " ")
    for pat, msg in claims["review"]:
        words = [m.group(0) for m in re.finditer(pat, scan_review, re.I)]
        if words:
            hit("review", msg, words)
    for m in NUMBER_CLAIM.finditer(vis_no_ph):
        reviews.append(f"number claim needs a source or placeholder: '{m.group(0)}'")

    # compliance (inside <main> only)
    flags = page["flags"]
    for flag, (pat, msg) in REQUIRED.items():
        if flag in flags and not re.search(pat, main, re.I):
            errors.append(msg)
    if "fo_risk" in flags:
        at = main.find('id="s-risk"')
        box = main[at:at + 6000] if at >= 0 else ""
        missing = [b for b in FO_BULLETS if b not in box]
        if missing:
            errors.append(f"F&O risk box (element id s-risk) missing or incomplete: {missing[:2]}")
        if at >= 0:
            dark = [pos for pos, _, tag in secs if "band--dark" in tag]
            if dark and at > dark[0]:
                errors.append("F&O risk box sits below the dark band; it must come before it")
            order = [sid for _, sid, _ in secs]
            if "fo_page" in flags and ("s-risk" not in order or order.index("s-risk") > 1):
                errors.append("on F&O pages the risk box is its own section directly after the hero (second section)")
    if "pms" in flags:
        if not re.search(r"50 lakh|\{\{pms\.minimum\}\}", main, re.I):
            errors.append("PMS page must state the SEBI minimum investment (₹50 lakh)")
        if not re.search(r"empanelled", main, re.I):
            errors.append("PMS page must say the strategies are empanelled for distribution")
    for pat, flag, msg in TOPIC_HINTS:
        if flag not in flags and re.search(pat, vis, re.I):
            reviews.append(msg)

    # seo
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    title = t.group(1).strip() if t else ""
    d = re.search(r'<meta name="description" content="([^"]*)"', doc)
    desc = d.group(1).strip() if d else ""
    if not desc:
        errors.append("meta description is empty (front matter 'description')")
    elif not 70 <= len(desc) <= 165:
        reviews.append(f"description is {len(desc)} characters (aim for 70 to 160)")
    if len(title) > 70:
        reviews.append(f"title is {len(title)} characters (aim for 70 or fewer)")
    links = re.findall(r'href="(\d\d-[a-z0-9-]+\.html)', main)
    if len(set(links) - {page["file"]}) < 3:
        reviews.append("fewer than 3 internal links in the page body (parent hub, next step, related)")

    # states
    sfile = P("figma", page["file"].replace(".html", ".states.html"))
    n_states = len(re.findall(r'class="state-frame"', open(sfile, encoding="utf-8").read())) if os.path.exists(sfile) else 0
    if page["template"] == "D" and page["id"] != "login" and n_states < 3:
        errors.append(f"template D needs 3+ interaction states (OTP sent, error, verified/next); found {n_states}")
    elif "<form" in main and n_states < 2:
        reviews.append(f"page has a form but only {n_states} interaction state(s); add error and success states")

    # trace against page memory
    tr = trace_ids(page)
    if tr is not None:
        ids = {sid for _, sid, _ in secs}
        missing = sorted({i for _, row in tr for i in row if i not in ids})
        if missing:
            errors.append(f"memory section 4 cites section ids not on the page: {missing[:6]}")
        unmapped = sum(1 for must, row in tr if must and not row)
        if unmapped:
            errors.append(f"{unmapped} MUST question(s) in memory section 4 name no section id")

    info = {"placeholders": len(re.findall(r'class="ph[ "]', main)), "sections": len(secs),
            "words": len(vis.split()), "states": n_states, "title": title, "description": desc,
            "sha": hashlib.sha1(doc.encode("utf-8")).hexdigest()[:12]}
    return {"file": page["file"], "errors": errors, "reviews": reviews, **info}


def write_atomic(path, obj):
    tmp = f"{path}.tmp{os.getpid()}"
    json.dump(obj, open(tmp, "w"), indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def main(argv):
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    claims = json.load(open(P("rules", "claims.json"), encoding="utf-8"))
    values = json.load(open(P("memory", "values.json"), encoding="utf-8"))
    cta_label = values.get("cta.primary", {}).get("value") or "Open free account"
    want = set(argv)
    built = [p for p in sm["pages"] if os.path.exists(P("figma", p["file"]))]
    out = []
    for p in built:
        if want and f'{p["n"]:02d}' not in want and p["id"] not in want:
            continue
        out.append(lint(p, claims, cta_label))
    # uniqueness across every built page (reads the others' last lint results)
    seen = {}
    for p in built:
        f = P("review", p["file"][:-5], "lint.json")
        r = next((x for x in out if x["file"] == p["file"]), None) or (json.load(open(f)) if os.path.exists(f) else None)
        if r:
            for key in ("title", "description"):
                if r.get(key):
                    seen.setdefault((key, r[key]), []).append(r["file"])
    for r in out:
        for key in ("title", "description"):
            others = [f for f in seen.get((key, r.get(key)), []) if f != r["file"]]
            if r.get(key) and others:
                r["errors"].append(f"{key} duplicates {others[0]}")
    for r in out:
        d = P("review", r["file"][:-5])
        os.makedirs(d, exist_ok=True)
        write_atomic(os.path.join(d, "lint.json"), r)
        state = "FAIL" if r["errors"] else ("REVIEW" if r["reviews"] else "PASS")
        print(f'{state:6s} {r["file"]:40s} sections {r["sections"]:2d}  words {r["words"]:5d}  '
              f'placeholders {r["placeholders"]:2d}  states {r["states"]}')
        for e in r["errors"]:
            print("   error :", e)
        for e in r["reviews"]:
            print("   review:", e)
    return 1 if any(r["errors"] for r in out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
