"""Build Figma-ready pages.

Reads pages/src/NN-id.html (sections only, plus a JSON front-matter comment), wraps each in the shared
shell (header, footer, theme CSS) and writes one self-contained file per page to figma/NN-id.html:
  - theme/root-theme.css + theme/patterns.css + the page's own <style data-page> are inlined
  - every <svg><use href="#i-x"/></svg> icon is expanded to an inline vector (Figma imports these as layers)
  - internal links (/pricing) are rewritten to the built file names (06-pricing.html) so the set clicks through
  - no scripts, no motion: the page renders in its final state for html-to-Figma capture

Usage: python3 scripts/build.py            build every page that has a source file (and figma/index.html)
       python3 scripts/build.py 01 09      build only these page numbers (or ids); safe to run in parallel
"""
import json, os, re, sys, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
read = lambda p: open(p, encoding="utf-8").read()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700'
         '&family=Red+Hat+Mono:wght@500;600&family=Tiro+Devanagari+Hindi:ital@0;1&display=swap">')

FRONT = re.compile(r"<!--page\s*(\{.*?\})\s*-->", re.S)
PAGE_CSS = re.compile(r"<style data-page>(.*?)</style>", re.S)
USE = re.compile(r'<svg([^>]*)>\s*<use href="#(i-[a-z0-9-]+)"\s*/>\s*</svg>')


def load():
    sm = json.load(open(P("sitemap.json"), encoding="utf-8"))
    return sm, {p["url"]: p for p in sm["pages"]}


def expand_icons(markup, icons, missing):
    def rep(m):
        attrs, name = m.group(1), m.group(2)
        ic = icons.get(name)
        if not ic:
            missing.add(name)
            return m.group(0)
        if "viewBox" not in attrs:
            attrs += f' viewBox="{ic["viewBox"]}"'
        if "aria-hidden" not in attrs and "aria-label" not in attrs:
            attrs += ' aria-hidden="true"'
        if "xmlns" not in attrs:
            attrs += ' xmlns="http://www.w3.org/2000/svg"'
        return f"<svg{attrs}>{ic['body']}</svg>"
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


def crumbs(items):
    if not items:
        return ""
    li = []
    for i, (label, url) in enumerate(items):
        last = i == len(items) - 1
        li.append(f'<li><span aria-current="page">{html.escape(label)}</span></li>' if last
                  else f'<li><a href="{url}">{html.escape(label)}</a></li>')
    return f'<nav class="wrap crumbs-bar" aria-label="Breadcrumb"><ol class="crumbs">{"".join(li)}</ol></nav>\n'


def build_page(page, by_url, shell, css, icons, stamp):
    src_path = P("pages", "src", page["file"])
    src = read(src_path)
    m = FRONT.search(src)
    front = json.loads(m.group(1)) if m else {}
    body = FRONT.sub("", src)
    page_css = "\n".join(x.strip() for x in PAGE_CSS.findall(body))
    body = PAGE_CSS.sub("", body).strip()

    minimal = front.get("header", "min" if "minimal_header" in page["flags"] else "full") == "min"
    header = shell["header-min"] if minimal else shell["announce"] + shell["header"]
    if not minimal and page["nav"] not in ("none", "home"):
        header = header.replace(f'class="navlink" data-nav="{page["nav"]}"', f'class="navlink is-current" data-nav="{page["nav"]}"')
    footer = shell["footer-min"] if front.get("footer", "min" if minimal else "full") == "min" else shell["footer"]
    mbar = "" if minimal else shell["mbar"]
    spine = '<div class="root-line" aria-hidden="true"><i></i></div>\n' if front.get("spine", True) else ""
    main_cls = "spine" if spine else ""

    title = front.get("title") or f'{page["title"]} | ROOT by Aikyam'
    desc = front.get("description", "")
    doc = f"""<!doctype html>
<!-- ROOT by Aikyam · page {page['n']:02d} of 75 · {page['title']} · template {page['template']} · entity {page['entity']}
     Built {stamp} from pages/src/{page['file']} · page memory: memory/pages/{page['file'][:-5]}.md
     DRAFT for design review and Figma import. Not for publication until Aikyam compliance approves. -->
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
</head>
<body class="is-static no-spine-motion page-{page['id']} tpl-{page['template'].lower()}">
{header}
<main class="{main_cls}" id="main">
{spine}{crumbs(front.get('breadcrumb'))}{body}
</main>
{footer}
{mbar}
</body>
</html>
"""
    missing, unknown = set(), set()
    doc = expand_icons(doc, icons, missing)
    doc = rewrite_links(doc, by_url, unknown)
    open(P("figma", page["file"]), "w", encoding="utf-8").write(doc)
    return {"file": page["file"], "missing_icons": sorted(missing), "unknown_links": sorted(unknown),
            "bytes": len(doc.encode("utf-8"))}


def index(sm, built_files):
    rows = []
    for p in sm["pages"]:
        ok = p["file"] in built_files
        link = f'<a href="{p["file"]}">{html.escape(p["title"])}</a>' if ok else html.escape(p["title"])
        rows.append(f'<tr><td class="num">{p["n"]:02d}</td><td>{link}</td><td>{p["template"]}</td><td>{p["phase"]}</td>'
                    f'<td>{p["entity"]}</td><td>{p["mode"]}</td><td>{"built" if ok else "to do"}</td></tr>')
    open(P("figma", "index.html"), "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8><title>ROOT pages</title><style>body{font:15px system-ui;margin:32px}"
        "table{border-collapse:collapse}td,th{padding:6px 12px;border-bottom:1px solid #e2e8ef;text-align:left}</style>"
        f"<h1>ROOT by Aikyam: 75-page build</h1><p>{len(built_files)} of 75 built.</p><table><tr><th>#</th><th>Page</th>"
        "<th>Template</th><th>Phase</th><th>Entity</th><th>Mode</th><th>Status</th></tr>" + "".join(rows) + "</table>")


def main(argv):
    sm, by_url = load()
    shell = {k: read(P("shell", k + ".html")) for k in ("announce", "header", "header-min", "footer", "footer-min", "mbar")}
    css = read(P("theme", "root-theme.css")) + "\n" + read(P("theme", "patterns.css"))
    icons = json.load(open(P("theme", "icons.json")))
    stamp = datetime.date.today().strftime("%d-%b-%Y")
    want = {a for a in argv if not a.startswith("--")}
    report = []
    for p in sm["pages"]:
        if not os.path.exists(P("pages", "src", p["file"])):
            continue
        if want and f'{p["n"]:02d}' not in want and p["id"] not in want:
            continue
        report.append(build_page(p, by_url, shell, css, icons, stamp))
    built = {f for f in os.listdir(P("figma")) if re.match(r"\d\d-.*\.html$", f)}
    if not want or "--index" in argv:  # per-page builds run in parallel: only a full build rewrites the index
        index(sm, built)
    for r in report:
        flag = "" if not (r["missing_icons"] or r["unknown_links"]) else "  !! "
        print(f'{r["file"]:42s} {r["bytes"]//1024:4d} KB{flag}'
              + (f' missing icons {r["missing_icons"]}' if r["missing_icons"] else "")
              + (f' unknown links {r["unknown_links"]}' if r["unknown_links"] else ""))
    print(f"built {len(report)} page(s); {len(built)} of 75 in figma/")
    return 1 if any(r["missing_icons"] or r["unknown_links"] for r in report) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
