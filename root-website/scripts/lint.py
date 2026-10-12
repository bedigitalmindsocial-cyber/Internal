"""Automatic checks on built pages (figma/NN-id.html). Cheap, run on every page, every time.

Checks: one h1 and no skipped heading levels; no scripts; no em dashes; forbidden phrases and claims;
required disclosures from the page's sitemap flags; inline styles limited to CSS custom properties;
unresolved internal links; placeholder count; invented-number patterns.

Usage: python3 scripts/lint.py [NN|id ...]   (default: every built page)
Writes review/NN-id/lint.json and prints one line per page. Exit 1 if any page has an error.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

# (pattern, message, severity). Severity "error" blocks a page; "review" needs a human or reviewer to clear it.
FORBIDDEN = [
    (r"\bzero commission\b|\bcommission[- ]free\b", "Aikyam Wealth earns commission on regular plans", "error"),
    (r"\bdirect plans?\b", "ARN distributor cannot deal in Direct Plans (check entity)", "review"),
    (r"\bIFA\b|independent financial advis", "Use 'Distributor Partner Programme', never IFA", "error"),
    (r"\bsub[- ]?brokers?\b", "Category abolished: use 'Authorised Person'", "error"),
    (r"\bguarantee(d|s)?\b|\bassured returns?\b|\brisk[- ]free\b|\bsure[- ]shot\b", "No guarantee or assurance language", "error"),
    (r"\b(no\.? ?1|number one|#1|best broker|lowest brokerage|cheapest)\b", "Comparative or superlative claim", "error"),
    (r"\btrusted by\b|\bhappy (investors|customers|clients)\b", "Borrowed-authority claim; ROOT is new", "error"),
    (r"\bseamless(ly)?\b|\bunlock\b|\belevate\b|\bempower\b|\brevolutioni[sz]e\b|\bnext[- ]gen\b", "House style: banned buzzword", "error"),
    (r"\badvis(e|or|ors|ory)\b|\badvic(e)\b", "Implies IA/RA registration; check context", "review"),
    (r"\b(stock )?tips\b|\bstock ideas?\b|\bresearch reports?\b|\btarget price\b|\bbuy call\b|\bAI[- ]led\b", "Research/advice content needs an RA licence", "error"),
    (r"\bclick here\b", "Links must say where they go", "error"),
]
NEGATED = re.compile(r"\b(not|no|never|cannot|in no way|does not|do not)\b[^.]*$", re.I)
NUMBER_CLAIM = re.compile(r"\b\d[\d,.]*\s*(\+|lakh\+?|lakhs|crore\+?|cr\+?|mn\+?|million\+?|k\+)?\s*(clients|customers|investors|users|traders|downloads|accounts)\b", re.I)
REQUIRED = {
    "fo_risk": (r"9 out of 10 individual traders", "F&O risk disclosure block missing"),
    "mf_risk": (r"mutual fund investments are subject to market risks", "MF risk line missing"),
    "distributor_disclaimer": (r"not exchange[- ]traded products", "Distributor disclaimer missing"),
    "coming_soon": (r'class="soon"|Coming soon', "Coming-soon badge missing"),
    "illustrative_data": (r"[Ii]llustrative", "Illustrative-data label missing"),
}


def text_of(doc):
    doc = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", doc, flags=re.S)
    doc = re.sub(r"<!--.*?-->", " ", doc, flags=re.S)
    doc = re.sub(r"<svg.*?</svg>", " ", doc, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", doc))


def main_of(doc):
    m = re.search(r"<main[^>]*>(.*)</main>", doc, re.S)
    return m.group(1) if m else doc


def lint(page):
    path = P("figma", page["file"])
    doc = open(path, encoding="utf-8").read()
    main = main_of(doc)
    txt, main_txt = text_of(doc), text_of(main)
    errors, reviews, info = [], [], {}

    heads = [int(h) for h in re.findall(r"<h([1-6])[\s>]", main)]
    if heads.count(1) != 1:
        errors.append(f"expected exactly one h1 in main, found {heads.count(1)}")
    for a, b in zip(heads, heads[1:]):
        if b > a + 1:
            errors.append(f"heading level skips from h{a} to h{b}")
            break
    if "<script" in doc:
        errors.append("contains <script>; pages must be static")
    # em dash never; a spaced en dash only inside a numeric range (₹412 – ₹433, 6 – 12 Nov)
    if "—" in main_txt or re.search(r"(?<![\d%])\s–\s|\s–\s(?![\d₹])", main_txt):
        errors.append("em dash or spaced en dash in copy (use commas, colons or parentheses)")
    for pat, msg, sev in FORBIDDEN:
        hits = sorted({m.group(0) for m in re.finditer(pat, main_txt, re.I)
                       if not (pat.startswith(r"\bguarantee") and NEGATED.search(main_txt[max(0, m.start() - 30):m.start()]))})
        if hits:
            (errors if sev == "error" else reviews).append(f"{msg}: {', '.join(hits[:4])}")
    for m in NUMBER_CLAIM.finditer(main_txt):
        reviews.append(f"number claim needs a source or placeholder: '{m.group(0)}'")
    for flag in page["flags"]:
        if flag in REQUIRED and not re.search(REQUIRED[flag][0], doc, re.I):
            errors.append(REQUIRED[flag][1])
    bad_style = [s for s in re.findall(r'style="([^"]*)"', main) if not all(
        d.strip().startswith("--") for d in s.split(";") if d.strip())]
    if bad_style:
        reviews.append(f"{len(bad_style)} inline style(s) beyond custom properties, e.g. '{bad_style[0][:60]}'")
    unresolved = sorted(set(re.findall(r'href="(/[^"]*)"', doc)))
    if unresolved:
        errors.append(f"unresolved internal links: {unresolved[:6]}")
    imgs_no_alt = len(re.findall(r"<img(?![^>]*\balt=)[^>]*>", main))
    if imgs_no_alt:
        errors.append(f"{imgs_no_alt} <img> without alt")
    info["placeholders"] = len(re.findall(r'class="ph(\s|")|class="ph ph--block"', main))
    info["sections"] = len(re.findall(r"<section\b", main))
    info["words"] = len(main_txt.split())
    return {"file": page["file"], "errors": errors, "reviews": reviews, **info}


def main(argv):
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    want = set(argv)
    out = []
    for p in sm["pages"]:
        if not os.path.exists(P("figma", p["file"])):
            continue
        if want and f'{p["n"]:02d}' not in want and p["id"] not in want:
            continue
        r = lint(p)
        out.append(r)
        state = "FAIL" if r["errors"] else ("REVIEW" if r["reviews"] else "PASS")
        print(f'{state:6s} {r["file"]:40s} sections {r["sections"]:2d}  words {r["words"]:5d}  placeholders {r["placeholders"]:2d}')
        for e in r["errors"]:
            print("   error :", e)
        for e in r["reviews"]:
            print("   review:", e)
    for r in out:  # one file per page, so parallel agents never overwrite each other
        d = P("review", r["file"][:-5])
        os.makedirs(d, exist_ok=True)
        json.dump(r, open(os.path.join(d, "lint.json"), "w"), indent=1)
    return 1 if any(r["errors"] for r in out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
