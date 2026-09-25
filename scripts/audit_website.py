#!/usr/bin/env python3
"""Website decay audit (CLAUDE.md Section 5.1): ten checks, one point each.

Fetches the homepage, the contact (or about) page and one product page, then
scores:
   1 copyright year 2020 or earlier, or no year      6 legacy tech
   2 withdrawn standards (ISO 9001:2008 etc.)          7 mobile PageSpeed below 50
   3 no HTTPS or certificate error                     8 broken images/links, placeholder text
   4 no viewport meta tag                              9 thin content or stock-only images
   5 contact email on Gmail/Yahoo/Rediffmail/Hotmail  10 no brochure PDF, or PDF created before 2021

A failed fetch is never scored as "no website": sites that cannot be reached,
that sit behind anti-bot protection, or that this environment's network policy
blocks come back with status UNREACHABLE, SITE_BLOCKED or ENV_BLOCKED and no
score, so the lead gets a Manual_Check note instead of a wrong score.

Usage:
  python3 scripts/audit_website.py https://www.example.com [--json]
  python3 scripts/audit_website.py --no-website            # score 10, SEG-NOWEB
  python3 scripts/audit_website.py --batch sites.txt [--out output/audits.jsonl]
      (sites.txt: one URL per line, or "Company Name | URL")

PageSpeed (check 7) uses the PageSpeed Insights API. Set PSI_API_KEY (a free
Google Cloud API key) for a reliable quota; without it the check is skipped
and noted whenever the shared quota is exhausted.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup, UnicodeDammit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

USER_AGENT = "Mozilla/5.0 (compatible; GiraffeSiteAudit/1.0; single-page manual audit)"
ROBOTS_AGENT = "GiraffeSiteAudit"
PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
MAX_HTML_BYTES = 3_000_000
MAX_PDF_BYTES = 25_000_000

CHECK_NAMES = {
    1: "copyright_year", 2: "withdrawn_standards", 3: "https", 4: "viewport", 5: "free_email",
    6: "legacy_tech", 7: "pagespeed", 8: "broken_or_placeholder", 9: "thin_content", 10: "brochure_pdf",
}

CONTACT_RE = re.compile(r"contact|reach[\s_-]*us|get[\s_-]*in[\s_-]*touch|enquir|inquir", re.I)
ABOUT_RE = re.compile(r"about|profile|who[\s_-]*we[\s_-]*are|company|overview", re.I)
PRODUCT_RE = re.compile(r"product|range|catalog|catalogue|machine|capabilit|solution|equipment|"
                        r"categor|items?\b|infrastructure|facilit|manufactur|services?", re.I)
BROCHURE_RE = re.compile(r"brochure|profile|catalog|catalogue|company|corporate|product", re.I)
ASSET_EXT_RE = re.compile(r"\.(jpe?g|png|gif|webp|svg|ico|bmp|pdf|zip|rar|docx?|xlsx?|pptx?|mp4|mp3|css|js)$", re.I)
COPYRIGHT_RE = re.compile(
    r"(?:©|\(c\)|copyright)\s*(?:©|\(c\))?[^0-9©]{0,60}?\b((?:19|20)\d{2})\b"
    r"(?:\s*(?:-|–|—|to)\s*((?:19|20)\d{2})\b)?", re.I)
YEAR_BEFORE_COPYRIGHT_RE = re.compile(r"\b((?:19|20)\d{2})\s*(?:©|\(c\))", re.I)
COPYRIGHT_MARK_RE = re.compile(r"©|\(c\)|copyright", re.I)
STANDARDS = [
    ("ISO 9001:2008", re.compile(r"9001\s*[:\-–/_. ]?\s*2008", re.I)),
    ("ISO 14001:2004", re.compile(r"14001\s*[:\-–/_. ]?\s*2004", re.I)),
    ("OHSAS 18001", re.compile(r"ohsas", re.I)),
]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
MOBILE_RE = re.compile(r"(?<![\d])(?:\+?91[\s.-]*|0)?[6-9](?:[\s.-]?\d){9}(?![\d])")
PLACEHOLDER_PATTERNS = [
    ("lorem ipsum", re.compile(r"lorem ipsum|dolor sit amet", re.I)),
    ("under construction", re.compile(r"under construction", re.I)),
    ("placeholder text", re.compile(r"your (?:company|business) name here|insert (?:text|content) here|"
                                    r"dummy text|sample text here|add your (?:text|content)", re.I)),
]
COUNTER_RE = re.compile(r"visitor(?:s)?\s*(?:counter|count|no\.?|number)|hit\s*counter|you\s+are\s+visitor|"
                        r"visitors?\s+since|page\s*views?\s+since", re.I)
COUNTER_IMG_RE = re.compile(r"(?:hit|web|free|visitor)[-_]?counter|counter\.(?:digits|websiteout)|easycounter", re.I)
BEST_VIEWED_RE = re.compile(r"best\s+view(?:ed)?\s+(?:in|with|at|on)\b", re.I)
JQUERY1_RE = re.compile(r"jquery[.-]?(1\.\d+(?:\.\d+)?)(?:\.min)?\.js|jquery(?:\.min)?\.js\?ver=(1\.\d+(?:\.\d+)?)", re.I)
STOCK_RE = re.compile(r"shutterstock|istockphoto|gettyimages|depositphotos|dreamstime|123rf|freepik|pexels|"
                      r"unsplash|pixabay|adobestock|stock[-_]?photo|stock[-_]image", re.I)
PLANT_RE = re.compile(r"plant|factory|infra|facility|machin|shop[-_ ]?floor|production|manufactur|workshop|"
                      r"unit|foundry|mill|warehouse|team", re.I)
DEAD_SITE_TITLES = re.compile(r"index of /|account suspended|suspended page|domain (?:is )?for sale|"
                              r"buy this domain|parked|default web site page|^it works!?$|welcome to nginx|"
                              r"web ?site (?:is )?expired|future home of", re.I)
DEAD_SITE_BODY = re.compile(r"this account has been suspended|this domain (?:name )?(?:is|may be) for sale|"
                            r"sedoparking|parkingcrew|domain has expired|website is expired", re.I)


@dataclass
class Page:
    url: str
    final_url: str
    status: int
    html: str
    soup: BeautifulSoup    # full markup, scripts included (legacy-tech checks)
    tsoup: BeautifulSoup   # scripts and styles removed (text checks)
    text: str
    headers: dict


@dataclass
class FetchError:
    kind: str       # ENV_BLOCKED, SSL, CONNECT, TIMEOUT, HTTP, ROBOTS, OTHER
    detail: str


@dataclass
class Check:
    hit: bool = False
    evidence: str = ""
    skipped: str = ""
    notes: list = field(default_factory=list)


class Fetcher:
    """requests wrapper: per-host delay, robots.txt, capped downloads, error classes."""

    def __init__(self, delay: float = 1.0, timeout: float = 20.0, verify=True):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-IN,en;q=0.8"})
        # Passed per request: requests lets REQUESTS_CA_BUNDLE override a session-level verify.
        self.verify = verify
        self.delay, self.timeout = delay, timeout
        self._last: dict[str, float] = {}
        self._robots: dict[str, RobotFileParser | None] = {}
        self.requests_made = 0

    def _wait(self, url: str):
        host = urlparse(url).netloc
        gap = time.monotonic() - self._last.get(host, 0)
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last[host] = time.monotonic()

    @staticmethod
    def classify(exc: Exception) -> FetchError:
        msg = str(exc)
        if isinstance(exc, requests.exceptions.ProxyError):
            if "403" in msg or "407" in msg:
                return FetchError("ENV_BLOCKED", "this environment's network policy blocked the host")
            return FetchError("CONNECT", f"proxy could not reach the host ({msg[:120]})")
        if isinstance(exc, requests.exceptions.SSLError):
            return FetchError("SSL", msg[:160])
        if isinstance(exc, requests.exceptions.Timeout):
            return FetchError("TIMEOUT", "timed out")
        if isinstance(exc, requests.exceptions.ConnectionError):
            return FetchError("CONNECT", msg[:160])
        return FetchError("OTHER", msg[:160])

    def allowed(self, url: str) -> bool:
        p = urlparse(url)
        key = f"{p.scheme}://{p.netloc}"
        if key not in self._robots:
            rp = None
            try:
                self._wait(key + "/robots.txt")
                self.requests_made += 1
                r = self.s.get(key + "/robots.txt", timeout=self.timeout, allow_redirects=True, verify=self.verify)
                if r.status_code == 200 and "text/html" not in r.headers.get("Content-Type", ""):
                    rp = RobotFileParser()
                    rp.parse(r.text.splitlines())
            except requests.RequestException:
                rp = None   # unreachable robots.txt: the page fetch will surface the real error
            self._robots[key] = rp
        rp = self._robots[key]
        return True if rp is None else rp.can_fetch(ROBOTS_AGENT, url)

    def get(self, url: str, max_bytes: int = MAX_HTML_BYTES, check_robots: bool = True):
        if check_robots and not self.allowed(url):
            return None, FetchError("ROBOTS", "disallowed by robots.txt")
        try:
            self._wait(url)
            self.requests_made += 1
            r = self.s.get(url, timeout=self.timeout, allow_redirects=True, stream=True, verify=self.verify)
            body = b""
            for chunk in r.iter_content(65536):
                body += chunk
                if len(body) >= max_bytes:
                    break
            r.close()
            return (r, body), None
        except requests.RequestException as exc:
            return None, self.classify(exc)

    def status(self, url: str) -> int | FetchError:
        if not self.allowed(url):
            return FetchError("ROBOTS", "disallowed")
        try:
            self._wait(url)
            self.requests_made += 1
            r = self.s.head(url, timeout=self.timeout, allow_redirects=True, verify=self.verify)
            if r.status_code in (403, 405, 501):   # some servers refuse HEAD: retry with a tiny GET
                self._wait(url)
                self.requests_made += 1
                r = self.s.get(url, timeout=self.timeout, allow_redirects=True, stream=True, verify=self.verify)
                r.close()
            return r.status_code
        except requests.RequestException as exc:
            return self.classify(exc)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def make_page(url: str, resp, body: bytes) -> Page:
    # requests assumes ISO-8859-1 when the header has no charset, which mangles ₹ and ©;
    # UnicodeDammit honours a declared charset first, then the page's meta tag, then sniffs.
    m = re.search(r"charset=([\w-]+)", resp.headers.get("Content-Type", ""), re.I)
    html = UnicodeDammit(body, [m.group(1)] if m else []).unicode_markup or ""
    tsoup = BeautifulSoup(html, "lxml")
    for t in tsoup(["script", "style", "noscript", "template"]):
        t.decompose()
    text = " ".join(tsoup.get_text(" ").split())
    return Page(url, resp.url, resp.status_code, html, BeautifulSoup(html, "lxml"), tsoup, text, dict(resp.headers))


def site_key(url: str) -> str:
    return C.registrable_domain(C.host_of(url))


def clean_link(base: str, href: str) -> str | None:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#", "whatsapp:", "data:")):
        return None
    u = urlparse(urljoin(base, href.strip()))
    if u.scheme not in ("http", "https"):
        return None
    return urlunparse((u.scheme, u.netloc.lower(), u.path or "/", "", u.query, ""))


def internal_links(page: Page) -> list[tuple[str, str]]:
    """[(url, anchor text)] for same-site links, first occurrence order."""
    base_site, seen, out = site_key(page.final_url), set(), []
    for a in page.soup.find_all("a", href=True):
        u = clean_link(page.final_url, a["href"])
        if not u or site_key(u) != base_site:
            continue
        norm = u.rstrip("/")
        if norm in seen:
            continue
        seen.add(norm)
        out.append((u, " ".join(a.get_text(" ").split())[:80]))
    return out


def page_links(links, pattern, exclude: set) -> list[str]:
    hits = []
    for u, text in links:
        path = urlparse(u).path
        if u.rstrip("/") in exclude or ASSET_EXT_RE.search(path):
            continue
        if pattern.search(path) or pattern.search(text):
            hits.append(u)
    return hits


def decode_cfemail(hexstr: str) -> str | None:
    try:
        key = int(hexstr[:2], 16)
        return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))
    except ValueError:
        return None


def find_emails(page: Page) -> set[str]:
    found = set()
    for a in page.soup.find_all("a", href=True):
        h = a["href"]
        if h.lower().startswith("mailto:"):
            found.add(h[7:].split("?")[0].strip())
        m = re.search(r"/cdn-cgi/l/email-protection#([0-9a-f]+)", h, re.I)
        if m:
            found.add(decode_cfemail(m.group(1)) or "")
    for el in page.soup.select("[data-cfemail]"):
        found.add(decode_cfemail(el["data-cfemail"]) or "")
    text = re.sub(r"\s*[\[(]\s*at\s*[\])]\s*", "@", page.text, flags=re.I)
    text = re.sub(r"\s*[\[(]\s*dot\s*[\])]\s*", ".", text, flags=re.I)
    found.update(EMAIL_RE.findall(text))
    return {e.lower().strip(".") for e in found
            if e and "@" in e and not re.search(r"\.(png|jpe?g|gif|webp|svg)$", e, re.I)}


def find_mobiles(page: Page) -> list[dict]:
    out = []
    for m in MOBILE_RE.finditer(page.text):
        num = C.normalize_mobile(m.group(0))
        if num:
            s, e = max(0, m.start() - 50), min(len(page.text), m.end() + 20)
            out.append({"mobile": num, "page": page.final_url, "context": page.text[s:e]})
    return out


def pdf_created_year(data: bytes) -> tuple[int | None, str]:
    try:
        from pypdf import PdfReader
        meta = PdfReader(io.BytesIO(data)).metadata
        if meta and meta.creation_date:
            return meta.creation_date.year, "pdf metadata"
    except BaseException:   # truncated or odd PDFs (and pypdf's crypto import) fall back to a byte scan
        pass
    m = re.search(rb"/CreationDate\s*\(\s*D:(\d{4})", data) or re.search(rb"<xmp:CreateDate>(\d{4})", data)
    return (int(m.group(1)), "pdf metadata") if m else (None, "")


# ---------------------------------------------------------------------------
# The ten checks
# ---------------------------------------------------------------------------

def footer_text(page: Page) -> str:
    parts = [el.get_text(" ") for el in page.tsoup.find_all("footer")]
    for el in page.tsoup.find_all(attrs={"class": True}) + page.tsoup.find_all(attrs={"id": True}):
        ident = " ".join(el.get("class", [])) + " " + (el.get("id") or "")
        if re.search(r"footer|copyright|copy-right|bottom-bar", ident, re.I):
            parts.append(el.get_text(" "))
    return " ".join(" ".join(parts).split())


def check_copyright(pages: list[Page]) -> Check:
    years, marker, dynamic = [], False, False
    for p in pages:
        txt = footer_text(p) + " " + p.text[-4000:]
        for m in COPYRIGHT_RE.finditer(txt):
            years += [int(y) for y in m.groups() if y]
        years += [int(m.group(1)) for m in YEAR_BEFORE_COPYRIGHT_RE.finditer(txt)]
        marker = marker or bool(COPYRIGHT_MARK_RE.search(p.text))
        dynamic = dynamic or bool(re.search(r"getFullYear\s*\(|new Date\(\)\.getYear", p.html))
    years = [y for y in years if 1990 <= y <= date.today().year + 1]
    if years:
        y = max(years)
        return Check(y <= 2020, f"© {y}" if y <= 2020 else "", notes=[f"latest copyright year {y}"])
    if dynamic:
        return Check(False, notes=["copyright year is written by JavaScript (auto-updating)"])
    return Check(True, "© without year" if marker else "no copyright year")


def check_standards(pages: list[Page]) -> Check:
    found = []
    for p in pages:
        hay = [p.text] + [f"{i.get('alt', '')} {i.get('src', '')} {i.get('title', '')}" for i in p.soup.find_all("img")]
        hay += [a.get("href", "") for a in p.soup.find_all("a", href=True)]
        blob = " ".join(hay)
        for label, rx in STANDARDS:
            if label not in found and rx.search(blob):
                found.append(label)
    return Check(bool(found), ", ".join(found))


def check_viewport(home: Page) -> Check:
    has = home.soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)}) is not None
    return Check(not has, "" if has else "no viewport")


def check_email(pages: list[Page]) -> tuple[Check, list[str]]:
    emails = sorted(set().union(*(find_emails(p) for p in pages))) if pages else []
    free = sorted({C.FREE_EMAIL_PROVIDERS[C.email_domain(e)] for e in emails
                   if C.email_domain(e) in C.FREE_EMAIL_PROVIDERS})
    return Check(bool(free), " and ".join(f.lower() for f in free) + " contact" if free else ""), emails


def check_legacy(pages: list[Page]) -> Check:
    items = []

    def add(x):
        if x not in items:
            items.append(x)

    for p in pages:
        raw, soup = p.html, p.soup
        if re.search(r"\.swf\b|shockwave|swfobject", raw, re.I):
            add("Flash")
        if soup.find(["frameset", "frame"]):
            add("frames")
        if soup.find("marquee"):
            add("marquee")
        imgs = " ".join(i.get("src", "") for i in soup.find_all("img"))
        if COUNTER_RE.search(p.text) or COUNTER_IMG_RE.search(imgs):
            add("visitor counter")
        if BEST_VIEWED_RE.search(p.text):
            add("'best viewed in'")
        for s in soup.find_all("script", src=True):
            m = JQUERY1_RE.search(s["src"])
            if m:
                add(f"jQuery {m.group(1) or m.group(2)}")
        gen = soup.find("meta", attrs={"name": re.compile(r"^generator$", re.I)})
        if gen:
            m = re.search(r"wordpress\s+(\d+)\.(\d+)", gen.get("content", ""), re.I)
            if m and int(m.group(1)) < 5:
                add(f"WordPress {m.group(1)}.{m.group(2)}")
        layout_tables = [t for t in soup.find_all("table")
                         if any(t.has_attr(a) for a in ("cellpadding", "cellspacing", "bgcolor", "background"))
                         or (t.has_attr("width") and t.find("table"))]
        nested = any(t.find("table") for t in soup.find_all("table"))
        if len(layout_tables) >= 3 or (layout_tables and nested):
            add("table layout")
    return Check(bool(items), ", ".join(items))


def check_pagespeed(url: str, key: str | None, enabled: bool, timeout: float = 120) -> Check:
    if not enabled:
        return Check(skipped="PageSpeed check disabled (--no-psi)")
    params = {"url": url, "strategy": "mobile", "category": "performance"}
    if key:
        params["key"] = key
    try:
        r = requests.get(PSI_ENDPOINT, params=params, timeout=timeout)
    except requests.RequestException as exc:
        return Check(skipped=f"PageSpeed API unreachable ({Fetcher.classify(exc).kind})")
    if r.status_code != 200:
        why = "quota exhausted, set PSI_API_KEY" if r.status_code == 429 else f"HTTP {r.status_code}"
        return Check(skipped=f"PageSpeed API {why}")
    try:
        perf = r.json()["lighthouseResult"]["categories"]["performance"]["score"]
    except (KeyError, TypeError, ValueError):
        return Check(skipped="PageSpeed API returned no performance score")
    if perf is None:
        return Check(skipped="PageSpeed could not score the page")
    score = round(perf * 100)
    return Check(score < 50, f"mobile PageSpeed {score}" if score < 50 else "", notes=[f"mobile PageSpeed {score}"])


def check_broken_and_placeholder(pages: list[Page], home: Page, links, fetcher: Fetcher, max_checks: int) -> Check:
    found, notes = [], []
    img_urls = []
    for i in home.soup.find_all("img"):
        u = clean_link(home.final_url, i.get("src") or i.get("data-src") or "")
        if u and u not in img_urls:
            img_urls.append(u)
    broken_img = broken_link = inconclusive = 0
    for u in img_urls[:max_checks]:
        st = fetcher.status(u)
        if isinstance(st, int) and st in (404, 410):
            broken_img += 1
        elif not isinstance(st, int) and st.kind != "ROBOTS":
            inconclusive += 1
    nav = [u for u, _ in links if not ASSET_EXT_RE.search(urlparse(u).path) and u.rstrip("/") != home.final_url.rstrip("/")]
    for u in nav[:max_checks]:
        st = fetcher.status(u)
        if isinstance(st, int) and st in (404, 410):
            broken_link += 1
        elif not isinstance(st, int) and st.kind != "ROBOTS":
            inconclusive += 1
    if broken_img:
        found.append(f"{broken_img} broken image{'s' if broken_img > 1 else ''}")
    if broken_link:
        found.append(f"{broken_link} broken link{'s' if broken_link > 1 else ''}")
    for p in pages:
        for label, rx in PLACEHOLDER_PATTERNS:
            if label not in found and rx.search(p.text):
                found.append(label)
        title = (p.soup.title.get_text() if p.soup.title else "")
        if re.search(r"coming soon", title, re.I) and "coming soon" not in found:
            found.append("coming soon")
    notes.append(f"checked {min(len(img_urls), max_checks)} images, {min(len(nav), max_checks)} links")
    if inconclusive:
        notes.append(f"{inconclusive} checks inconclusive (network)")
    return Check(bool(found), ", ".join(found), notes=notes)


def check_thin(pages: list[Page], links_by_page: list, home: Page) -> Check:
    product_urls = set()
    for links in links_by_page:
        for u in page_links(links, PRODUCT_RE, {home.final_url.rstrip("/")}):
            product_urls.add(u.rstrip("/"))
    imgs = [f"{i.get('src', '')} {i.get('alt', '')}" for p in pages for i in p.soup.find_all("img")]
    stock = sum(1 for s in imgs if STOCK_RE.search(s))
    plant = sum(1 for s in imgs if PLANT_RE.search(s))
    found = []
    if len(product_urls) < 5:
        found.append(f"thin: {len(product_urls)} product/capability page{'s' if len(product_urls) != 1 else ''}")
    if stock and not plant:
        found.append("stock images only")
    return Check(bool(found), "; ".join(found),
                 notes=[f"{len(product_urls)} product/capability pages, {stock} stock images, {plant} plant-type images"])


def check_brochure(pages: list[Page], fetcher: Fetcher) -> tuple[Check, str]:
    pdfs = []
    for p in pages:
        for a in p.soup.find_all("a", href=True):
            u = clean_link(p.final_url, a["href"])
            if not u or not re.search(r"\.pdf$", urlparse(u).path, re.I):
                continue
            label = f"{urlparse(u).path} {a.get_text(' ')}"
            if BROCHURE_RE.search(label) and u not in pdfs:
                pdfs.append(u)
    if not pdfs:
        return Check(True, "no brochure PDF"), "None downloadable"
    got, err = fetcher.get(pdfs[0], max_bytes=MAX_PDF_BYTES)
    if not got:
        return Check(False, notes=[f"brochure {pdfs[0]} not fetched ({err.kind})"]), f"Unknown: {pdfs[0]} not fetched"
    resp, body = got
    if resp.status_code >= 400:
        return Check(True, f"brochure link broken (HTTP {resp.status_code})"), "None downloadable (broken link)"
    year, how = pdf_created_year(body)
    if year is None:
        lm = resp.headers.get("Last-Modified", "")
        m = re.search(r"\b(19|20)\d{2}\b", lm)
        if m:
            year, how = int(m.group(0)), "server Last-Modified"
    if year is None:
        return Check(False, notes=[f"brochure {pdfs[0]} has no creation date"]), f"Unknown date: {pdfs[0]}"
    old = year < 2021
    status = f"{'Old' if old else 'Current'} ({year}): {pdfs[0]}"
    return Check(old, f"brochure PDF {year}" if old else "", notes=[f"brochure dated {year} ({how})"]), status


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def _result(url, status, score=None, **extra) -> dict:
    out = {"input_url": url, "status": status, "score": score, "max_score": 10,
           "decay_evidence": "", "checks": {}, "skipped": [], "notes": [], "contacts_found": {},
           "suggested": {}, "manual_check": "", "audited_on": C.today_str()}
    out.update(extra)
    return out


def audit(url: str, fetcher: Fetcher | None = None, psi_key: str | None = None, use_psi: bool = True,
          max_checks: int = 8) -> dict:
    fetcher = fetcher or Fetcher()
    url = url.strip()
    if C.is_shared_platform(url):
        return _result(url, "PLATFORM_ONLY", 10, decay_evidence="only a marketplace or social page, no own website",
                       segments=["SEG-NOWEB"], suggested={"Website_URL": "Not found"},
                       manual_check="Confirm the company has no own website")
    if not re.match(r"^https?://", url, re.I):
        url = "http://" + url
    parsed = urlparse(url)
    https_url = urlunparse(("https", parsed.netloc, parsed.path or "/", "", parsed.query, ""))
    http_url = urlunparse(("http", parsed.netloc, parsed.path or "/", "", parsed.query, ""))

    checks: dict[int, Check] = {}
    got, err_https = fetcher.get(https_url)
    if got is None and err_https.kind == "ENV_BLOCKED":
        return _result(url, "ENV_BLOCKED", manual_check=f"Audit blocked by this environment's network policy ({parsed.netloc})")
    if got is None and err_https.kind == "ROBOTS":
        return _result(url, "ROBOTS_DISALLOWED", manual_check="robots.txt disallows the homepage: audit by hand")
    if got is not None:
        home = make_page(https_url, *got)
        on_http = home.final_url.lower().startswith("http://")
        checks[3] = Check(on_http, "redirects to HTTP" if on_http else "")
    else:
        got, err_http = fetcher.get(http_url)
        if got is None and err_http.kind == "ROBOTS":
            return _result(url, "ROBOTS_DISALLOWED", manual_check="robots.txt disallows the homepage: audit by hand")
        if got is None and err_http.kind == "ENV_BLOCKED":
            return _result(url, "ENV_BLOCKED", manual_check=f"Audit blocked by this environment's network policy ({parsed.netloc})")
        if got is None:
            return _result(url, "UNREACHABLE", notes=[f"https: {err_https.kind} {err_https.detail}",
                                                      f"http: {err_http.kind} {err_http.detail}"],
                           manual_check="Website did not load: check the domain by hand before scoring")
        home = make_page(http_url, *got)
        why = "HTTPS certificate error" if err_https.kind == "SSL" else "no HTTPS"
        checks[3] = Check(True, why, notes=[f"https attempt: {err_https.kind}"])

    if home.status in (401, 403, 429, 503) and len(home.text) < 2000:
        return _result(url, "SITE_BLOCKED", notes=[f"homepage HTTP {home.status} (anti-bot or access control)"],
                       manual_check=f"Site refused the audit (HTTP {home.status}): check by hand, do not bypass")
    if home.status >= 400:
        return _result(url, "UNREACHABLE", notes=[f"homepage HTTP {home.status}"],
                       manual_check=f"Homepage returned HTTP {home.status}: check the domain by hand")
    title = home.soup.title.get_text(" ").strip() if home.soup.title else ""
    if DEAD_SITE_TITLES.search(title) or DEAD_SITE_BODY.search(home.text[:5000]):
        return _result(url, "DEAD_SITE", 10, final_url=home.final_url,
                       decay_evidence=f"site not in use (\"{(title or home.text[:60])[:60]}\")",
                       segments=["SEG-NOWEB"], manual_check="Domain parked, suspended or default page: confirm no other website")

    js_shell = len(home.text) < 300 and len(re.findall(r"<script", home.html, re.I)) >= 2
    links_home = internal_links(home)
    exclude = {home.final_url.rstrip("/")}
    contact = (page_links(links_home, CONTACT_RE, exclude) or page_links(links_home, ABOUT_RE, exclude) or [None])[0]
    skip = exclude | ({contact.rstrip("/")} if contact else set())
    product = (page_links(links_home, re.compile(r"product", re.I), skip)
               or page_links(links_home, PRODUCT_RE, skip) or [None])[0]
    pages, links_by_page, notes = [home], [links_home], []
    for extra in (contact, product):
        if not extra:
            continue
        got, err = fetcher.get(extra)
        if got is None:
            notes.append(f"could not fetch {extra} ({err.kind})")
            continue
        pg = make_page(extra, *got)
        if pg.status < 400:
            pages.append(pg)
            links_by_page.append(internal_links(pg))
    notes.append("pages audited: " + ", ".join(p.final_url for p in pages))

    checks[1] = check_copyright(pages)
    checks[2] = check_standards(pages)
    checks[4] = check_viewport(home)
    checks[5], emails = check_email(pages)
    checks[6] = check_legacy(pages)
    checks[7] = check_pagespeed(home.final_url, psi_key, use_psi)
    checks[8] = check_broken_and_placeholder(pages, home, links_home, fetcher, max_checks)
    checks[9] = check_thin(pages, links_by_page, home)
    checks[10], profile_status = check_brochure(pages, fetcher)

    status = "OK"
    skipped = [f"{n} {CHECK_NAMES[n]}: {c.skipped}" for n, c in sorted(checks.items()) if c.skipped]
    manual = ""
    if js_shell:
        status = "PARTIAL_JS"
        for n in (1, 5, 8, 9, 10):   # content checks cannot be trusted on an empty JS shell
            checks[n] = Check(skipped="page is rendered by JavaScript; static audit unreliable")
        skipped = [f"{n} {CHECK_NAMES[n]}: {c.skipped}" for n, c in sorted(checks.items()) if c.skipped]
        manual = "JavaScript-rendered site: review decay points 1, 5, 8, 9, 10 by hand"
    score = sum(1 for c in checks.values() if c.hit)
    evidence = "; ".join(c.evidence for n, c in sorted(checks.items()) if c.hit and c.evidence)
    mobiles = [m for p in pages for m in find_mobiles(p)]
    seen, uniq_mobiles = set(), []
    for m in mobiles:
        if m["mobile"] not in seen:
            seen.add(m["mobile"])
            uniq_mobiles.append(m)
    return _result(
        url, status, score, final_url=home.final_url, decay_evidence=evidence,
        checks={f"{n}_{CHECK_NAMES[n]}": {"hit": c.hit, "evidence": c.evidence, "skipped": c.skipped,
                                         "notes": c.notes} for n, c in sorted(checks.items())},
        skipped=skipped, notes=notes, manual_check=manual,
        contacts_found={"emails": emails, "mobiles": uniq_mobiles},
        suggested={"Corporate_Profile_Status": profile_status},
        requests_made=fetcher.requests_made,
    )


def no_website_result(name: str = "") -> dict:
    return _result(name or "(none)", "NO_WEBSITE", 10, decay_evidence="No website found", segments=["SEG-NOWEB"])


def print_human(r: dict):
    head = f"{r['input_url']}  ->  status {r['status']}"
    print(head + (f", score {r['score']}/10" if r["score"] is not None else ", NOT SCORED"))
    if r["decay_evidence"]:
        print(f"  Decay_Evidence: {r['decay_evidence']}")
    for name, c in r.get("checks", {}).items():
        mark = "HIT " if c["hit"] else ("skip" if c["skipped"] else " -  ")
        detail = c["evidence"] or c["skipped"] or "; ".join(c["notes"])
        print(f"  [{mark}] {name:<24} {detail}")
    for n in r.get("notes", []):
        print(f"  note: {n}")
    cf = r.get("contacts_found") or {}
    if cf.get("emails"):
        print(f"  emails on site: {', '.join(cf['emails'])}")
    for m in cf.get("mobiles", []):
        print(f"  mobile on site: {m['mobile']}  (\"...{m['context']}...\")  {m['page']}")
    if r.get("manual_check"):
        print(f"  MANUAL CHECK: {r['manual_check']}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url", nargs="?")
    p.add_argument("--no-website", action="store_true")
    p.add_argument("--batch")
    p.add_argument("--out")
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-psi", action="store_true")
    p.add_argument("--psi-key", default=os.environ.get("PSI_API_KEY"))
    p.add_argument("--delay", type=float, default=1.0, help="seconds between requests to one host")
    p.add_argument("--timeout", type=float, default=20.0)
    p.add_argument("--max-checks", type=int, default=8, help="images and links probed for check 8")
    args = p.parse_args(argv)

    if args.no_website:
        r = no_website_result(args.url or "")
        print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else f"NO_WEBSITE: score 10, SEG-NOWEB")
        return 0
    targets = []
    if args.batch:
        for line in Path(args.batch).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                name, _, u = line.rpartition("|")
                targets.append((name.strip(), u.strip()))
    elif args.url:
        targets.append(("", args.url))
    else:
        p.error("give a URL, --batch FILE or --no-website")

    out_f = open(args.out, "a", encoding="utf-8") if args.out else None
    for name, u in targets:
        r = audit(u, Fetcher(args.delay, args.timeout), args.psi_key, not args.no_psi, args.max_checks)
        if name:
            r["company"] = name
        if out_f:
            out_f.write(json.dumps(r, ensure_ascii=False) + "\n")
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            if name:
                print(f"== {name}")
            print_human(r)
            print()
    if out_f:
        out_f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
