"""Build Figma-ready pages.

Reads pages/src/NN-id.html (sections only, plus a JSON front-matter comment), wraps each in the shared
shell (header, footer, theme CSS) and writes self-contained files to figma/:
  figma/NN-id.html          the page in its default state
  figma/NN-id.states.html   one labelled frame per <template data-state="key" data-label="..."> block
Applied on the way:
  - theme/root-theme.css + theme/patterns.css + the page's <style data-page> are inlined
  - {{key}} tokens and <mark class="ph" data-ph="key"> placeholders are filled from memory/values.json
    (a key with no value yet renders as a visible placeholder chip), so one edit there updates every page
  - <svg><use href="#i-x"/></svg> icons become inline vectors with explicit stroke attributes
  - internal links (/pricing) become built file names (06-pricing.html) so the set clicks through
  - spine nodes get a real <i class="node-dot"> (pseudo-elements do not import as layers)
  - breadcrumb comes from the sitemap parent chain unless the front matter gives one
  - the header CTA and mobile bar follow the page's company and primary action (sitemap "cta")
  - no scripts, no motion: the page renders in its final state for html-to-Figma capture
Files are written atomically (temp file + rename), so parallel runs never leave half-written pages.

Usage: python3 scripts/build.py --all       every page with a source file, plus figma/index.html
       python3 scripts/build.py 01 09       only these page numbers (or ids); safe to run in parallel
Exit 1 if an icon, link, token or <use> could not be resolved, or the front matter is not valid JSON.
"""
import json, os, re, sys, html, datetime, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
read = lambda p: open(p, encoding="utf-8").read()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700'
         '&family=Red+Hat+Mono:wght@500;600&family=Tiro+Devanagari+Hindi:ital@0;1&display=swap">')

FRONT = re.compile(r"<!--page\s*(\{.*?\})\s*-->", re.S)
PAGE_CSS = re.compile(r"<style data-page>(.*?)</style>", re.S)
STATE = re.compile(r'<template data-state="([^"]+)"(?:\s+data-label="([^"]*)")?\s*>(.*?)</template>', re.S)
USE = re.compile(r'<svg([^>]*)>\s*<use href="#(i-[a-z0-9-]+)"\s*/?>\s*(?:</use>\s*)?</svg>')
TOKEN = re.compile(r"\{\{\s*([a-z0-9_.]+)\s*\}\}")
PH = re.compile(r'<mark class="ph([^"]*)" data-ph="([a-z0-9_.-]+)">(.*?)</mark>', re.S)
ICON_ATTRS = ' fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'


def write_atomic(path, text):
    tmp = f"{path}.tmp{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def load():
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    return sm, {p["url"]: p for p in sm["pages"]}


def fill_values(markup, values, problems):
    def tok(m):
        key = m.group(1)
        v = values.get(key)
        if v is None:
            problems.add(f"unknown token {{{{{key}}}}}")
            return m.group(0)
        if v.get("value") is None:
            return f'<mark class="ph" data-ph="{key}">{html.escape(v.get("label", key))}</mark>'
        return html.escape(v["value"], quote=False)

    def ph(m):
        key = m.group(2)
        v = values.get(key)
        if v and v.get("value") is not None:
            return html.escape(v["value"], quote=False)
        return m.group(0)
    markup = TOKEN.sub(tok, markup)
    return PH.sub(ph, markup)


def expand_icons(markup, icons, missing):
    def rep(m):
        attrs, name = m.group(1), m.group(2)
        ic = icons.get(name)
        if not ic:
            missing.add(name)
            return m.group(0)
        extra = f' viewBox="{ic["viewBox"]}" xmlns="http://www.w3.org/2000/svg" data-icon="{name}"'
        if "aria-hidden" not in attrs and "aria-label" not in attrs:
            extra += ' aria-hidden="true"'
        if "fill=" not in attrs:
            extra += ICON_ATTRS
        return f"<svg{attrs}{extra}>{ic['body']}</svg>"
    return USE.sub(rep, markup)


def rewrite_links(markup, by_url, unknown):
    def rep(m):
        url = m.group(1)
        path, _, frag = url.partition("#")
        path = path.rstrip("/") or "/"
        page = by_url.get(path)
        if not page:
            unknown.add(url)
            return m.group(0)
        return f'href="{page["file"]}' + (f"#{frag}" if frag else "") + '"'
    return re.sub(r'href="(/[^"]*)"', rep, markup)


def add_node_dots(markup):
    return re.sub(r'(<(h[1-6]|p|div|span)\b[^>]*\bclass="[^"]*\bnode\b[^"]*"[^>]*>)(?!<i class="node-dot")',
                  r'\1<i class="node-dot" aria-hidden="true"></i>', markup)


def auto_crumbs(page, by_url):
    chain, u, seen = [], page["url"], set()
    while u and u not in seen:
        seen.add(u)
        p = by_url.get(u)
        if not p:
            break
        chain.append(["Home" if u == "/" else p["title"], u])
        u = p.get("parent")
    return list(reversed(chain))


def crumbs(items):
    if not items or len(items) < 2:
        return ""
    li = []
    for i, (label, url) in enumerate(items):
        li.append(f'<li><span aria-current="page">{html.escape(label)}</span></li>' if i == len(items) - 1
                  else f'<li><a href="{url}">{html.escape(label)}</a></li>')
    return f'<nav class="wrap crumbs-bar" aria-label="Breadcrumb"><ol class="crumbs">{"".join(li)}</ol></nav>\n'


def mbar_for(page, front):
    if front.get("mbar") is False:
        return ""
    m = front.get("mbar") or {}
    cta = page["cta"]
    if m:
        label, href = m["label"], m["href"]
    elif cta["href"].startswith(("/open-account", "#s-apply", "#s-notify", "#s-form")):
        label, href = page["primary_cta"], cta["href"]
    else:
        label, href = "{{cta.primary}}", "/open-account/investing" if page["entity"] == "Wealth" else "/open-account/trading"
    return (f'<div class="mbar" data-sticky="bottom" aria-label="Mobile action bar"><a class="btn btn--ghost" href="/login">Login</a>'
            f'<a class="btn" href="{href}">{label}</a></div>')


def head(page, title, desc, css, page_css, stamp, kind):
    return f"""<!doctype html>
<!-- ROOT by Aikyam · page {page['n']:02d} of 75 · {page['title']} · {kind} · template {page['template']} · entity {page['entity']}
     Built {stamp} from pages/src/{page['file']} · page memory: memory/pages/{page['file'][:-5]}.md
     DRAFT for design review and Figma import. Exchange advertisement filing: required before publication (not filed).
     Not for publication until Aikyam compliance approves. -->
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{FONTS}
<style>
{css}
{('/* page: ' + page['id'] + ' */' + chr(10) + page_css) if page_css else ''}
</style>
</head>"""


def finish(doc, by_url, icons, values, problems):
    missing, unknown = set(), set()
    doc = fill_values(doc, values, problems)
    doc = expand_icons(doc, icons, missing)
    doc = add_node_dots(doc)
    doc = rewrite_links(doc, by_url, unknown)
    if missing:
        problems.add(f"missing icons {sorted(missing)}")
    if unknown:
        problems.add(f"unknown links {sorted(unknown)}")
    if "<use" in doc:
        problems.add('unexpanded <use> (write icons as <svg class="i"><use href="#i-name"/></svg>)')
    return doc


def build_page(page, by_url, shell, css, icons, values, stamp):
    problems = set()
    src = read(P("pages", "src", page["file"]))
    m = FRONT.search(src)
    try:
        front = json.loads(m.group(1)) if m else {}
    except json.JSONDecodeError as e:
        return {"file": page["file"], "problems": [f"front matter is not valid JSON: {e}"], "states": 0, "bytes": 0, "sha": ""}
    body = FRONT.sub("", src)
    page_css = "\n".join(x.strip() for x in PAGE_CSS.findall(body))
    body = PAGE_CSS.sub("", body)
    states = STATE.findall(body)
    body = STATE.sub("", body).strip()

    minimal = front.get("header", "min" if "minimal_header" in page["flags"] else "full") == "min"
    header = shell["header-min"] if minimal else shell["announce"] + shell["header"]
    if not minimal and page["nav"] not in ("none", "home"):
        header = header.replace(f'class="navlink" data-nav="{page["nav"]}"', f'class="navlink is-current" data-nav="{page["nav"]}"')
    if page["entity"] == "Wealth":  # the one primary action follows the page's company
        header = header.replace('class="btn btn--sm" href="/open-account/trading"', 'class="btn btn--sm" href="/open-account/investing"')
    header = header.replace(">Open free account<", ">{{cta.primary}}<")
    footer = shell["footer-min"] if front.get("footer", "min" if minimal else "full") == "min" else shell["footer"]
    mbar = "" if minimal else mbar_for(page, front)
    spine = '<div class="root-line" aria-hidden="true"><i></i></div>\n' if front.get("spine", True) else ""
    title = front.get("title") or f'{page["title"]} | ROOT by Aikyam'
    desc = front.get("description", "")
    bc = front.get("breadcrumb")
    if bc is None and page["url"] != "/" and not minimal:
        bc = auto_crumbs(page, by_url)
    cls = f"is-static no-spine-motion page-{page['id']} tpl-{page['template'].lower()}"

    doc = f"""{head(page, title, desc, css, page_css, stamp, 'page')}
<body class="{cls}">
{header}
<main class="{'spine' if spine else ''}" id="main">
{spine}{crumbs(bc)}{body}
</main>
{footer}
{mbar}
</body>
</html>
"""
    doc = finish(doc, by_url, icons, values, problems)
    write_atomic(P("figma", page["file"]), doc)

    states_file = P("figma", page["file"].replace(".html", ".states.html"))
    if states:
        frames = "\n".join(
            f'<section class="state-frame" id="state-{key}" aria-label="State: {html.escape(label or key)}"><div class="wrap">'
            f'<p class="state-label"><b>{html.escape(label or key)}</b> · state "{key}" · {page["title"]}</p>\n{content.strip()}\n</div></section>'
            for key, label, content in states)
        sdoc = f"""{head(page, 'States: ' + title, 'Interaction states for the designer', css, page_css, stamp, 'states board')}
<body class="{cls} states-board">
<main id="main">
{frames}
</main>
</body>
</html>
"""
        write_atomic(states_file, finish(sdoc, by_url, icons, values, problems))
    elif os.path.exists(states_file):
        os.remove(states_file)
    return {"file": page["file"], "states": len(states), "problems": sorted(problems),
            "bytes": len(doc.encode("utf-8")), "sha": hashlib.sha1(doc.encode("utf-8")).hexdigest()[:12]}


def index(sm, built_files):
    rows = []
    for p in sm["pages"]:
        ok = p["file"] in built_files
        st = p["file"].replace(".html", ".states.html")
        link = f'<a href="{p["file"]}">{html.escape(p["title"])}</a>' if ok else html.escape(p["title"])
        if ok and os.path.exists(P("figma", st)):
            link += f' · <a href="{st}">states</a>'
        rows.append(f'<tr><td class="num">{p["n"]:02d}</td><td>{link}</td><td>{p["template"]}</td><td>{p["phase"]}</td>'
                    f'<td>{p["entity"]}</td><td>{p["mode"]}</td><td>{"built" if ok else "to do"}</td></tr>')
    extra = "".join(f'<li><a href="{f}">{f}</a></li>' for f in ("00-kit.html", "00-import-test.html") if os.path.exists(P("figma", f)))
    write_atomic(P("figma", "index.html"),
        "<!doctype html><meta charset=utf-8><title>ROOT pages</title><style>body{font:15px system-ui;margin:32px}"
        "table{border-collapse:collapse}td,th{padding:6px 12px;border-bottom:1px solid #e2e8ef;text-align:left}</style>"
        f"<h1>ROOT by Aikyam: 75-page build</h1><p>{len(built_files)} of 75 built. Import the kit first.</p><ul>{extra}</ul>"
        "<table><tr><th>#</th><th>Page</th><th>Template</th><th>Phase</th><th>Entity</th><th>Mode</th><th>Status</th></tr>"
        + "".join(rows) + "</table>")


def main(argv):
    sm, by_url = load()
    shell = {k: read(P("shell", k + ".html")) for k in ("announce", "header", "header-min", "footer", "footer-min")}
    css = read(P("theme", "root-theme.css")) + "\n" + read(P("theme", "patterns.css"))
    icons = json.load(open(P("theme", "icons.json")))
    values = {k: v for k, v in json.load(open(P("memory", "values.json"), encoding="utf-8")).items() if not k.startswith("_")}
    stamp = datetime.date.today().strftime("%d-%b-%Y")
    want = {a for a in argv if not a.startswith("--")}
    if not want and "--all" not in argv and "--index" not in argv:
        print(__doc__.split("Usage:")[1])
        return 2
    report = []
    for p in sm["pages"]:
        if not os.path.exists(P("pages", "src", p["file"])):
            continue
        if want and f'{p["n"]:02d}' not in want and p["id"] not in want:
            continue
        report.append(build_page(p, by_url, shell, css, icons, values, stamp))
    built = {f for f in os.listdir(P("figma")) if re.match(r"\d\d-[a-z0-9-]+\.html$", f) and not f.startswith("00-")}
    if "--all" in argv or "--index" in argv:  # per-page builds run in parallel: only a full build rewrites the index
        index(sm, built)
    for r in report:
        print(f'{r["file"]:42s} {r["bytes"]//1024:4d} KB  states {r["states"]}  sha {r["sha"]}'
              + ("  !! " + "; ".join(r["problems"]) if r["problems"] else ""))
    print(f"built {len(report)} page(s); {len(built)} of 75 in figma/")
    return 1 if any(r["problems"] for r in report) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
