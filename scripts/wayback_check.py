#!/usr/bin/env python3
"""Wayback Machine recency check (CLAUDE.md Section 5.1, optional step).

Estimates when the site's CURRENT design first appeared. A raw CDX digest
changes whenever any byte of the page changes, so instead this script compares
a structural fingerprint (stylesheets, scripts, generator, navigation labels,
logo, theme classes) of the live homepage with archived snapshots, using a
binary search over one snapshot per month: typically 6 to 9 archive fetches.

R6 rule: current design first seen within the last 24 months AND decay score
2 or less -> reject R6. Pass --decay to get that verdict directly.

Usage:
  python3 scripts/wayback_check.py example.com [--decay 2] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
from audit_website import Fetcher, UnicodeDammit  # noqa: E402

ARCHIVE_BASE = "https://web.archive.org"   # tests point this at a local fake archive
MATCH = 0.5        # Jaccard similarity at or above this = same design
CLEAR_CHANGE = 0.3  # the snapshot before the first match below this = confident boundary


def _norm_asset(src: str) -> str:
    name = urlparse(src).path.rsplit("/", 1)[-1].lower()
    name = re.sub(r"[.-]?[0-9a-f]{8,}", "", name)      # build hashes
    name = re.sub(r"\d+(?:\.\d+)*", "", name)          # version numbers
    return name


def fingerprint(html: str) -> set[str]:
    soup = BeautifulSoup(html, "lxml")
    tokens: set[str] = set()
    for link in soup.find_all("link", href=True):
        if "stylesheet" in " ".join(link.get("rel") or []).lower():
            tokens.add("css:" + _norm_asset(link["href"]))
    for s in soup.find_all("script", src=True):
        if "archive.org" not in s["src"]:
            tokens.add("js:" + _norm_asset(s["src"]))
    gen = soup.find("meta", attrs={"name": re.compile(r"^generator$", re.I)})
    if gen and gen.get("content"):
        tokens.add("gen:" + re.sub(r"[\d.]+", "", gen["content"]).strip().lower())
    nav = soup.find("nav") or soup.find("header") or soup.body or soup
    for a in nav.find_all("a")[:40]:
        text = " ".join(a.get_text(" ").split()).lower()
        if 1 < len(text) < 40:
            tokens.add("nav:" + text)
    for img in soup.find_all("img"):
        blob = f"{img.get('src', '')} {img.get('alt', '')} {' '.join(img.get('class') or [])}".lower()
        if "logo" in blob:
            tokens.add("logo:" + _norm_asset(img.get("src", "")))
    if soup.body:
        for el in soup.body.find_all(True, limit=150):
            for cls in el.get("class") or []:
                if not re.search(r"\d", cls) and len(cls) > 3:
                    tokens.add("cls:" + cls.lower())
    return tokens


def similarity(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def ts_to_date(ts: str) -> date:
    return date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))


def check(domain_or_url: str, fetcher: Fetcher | None = None, max_fetches: int = 10, live_html: str | None = None,
          today: date | None = None) -> dict:
    fetcher = fetcher or Fetcher(delay=1.5, timeout=30)
    today = today or date.today()
    host = C.host_of(domain_or_url)
    out = {"domain": host, "status": "OK", "snapshots": 0, "first_archived": None, "last_archived": None,
           "current_design_first_seen": None, "months_since": None, "recent_redesign": None,
           "confidence": None, "fetches": 0, "notes": []}
    got, err = fetcher.get(f"{ARCHIVE_BASE}/cdx/search/cdx?url={host}&output=json&fl=timestamp,digest,statuscode"
                           f"&collapse=digest&filter=statuscode:200", check_robots=False)
    if got is None:
        out["status"] = "ENV_BLOCKED" if err.kind == "ENV_BLOCKED" else "ERROR"
        out["notes"].append(f"CDX query failed: {err.kind} {err.detail}")
        return out
    try:
        rows = json.loads(got[1] or b"[]")
    except ValueError:
        out.update(status="ERROR", notes=["CDX returned non-JSON"])
        return out
    snaps = [r[0] for r in rows[1:] if r and r[0].isdigit()]
    if not snaps:
        out["status"] = "NO_ARCHIVE"
        return out
    monthly, seen = [], set()
    for ts in sorted(snaps):                      # one snapshot per month keeps the search short
        if ts[:6] not in seen:
            seen.add(ts[:6])
            monthly.append(ts)
    out.update(snapshots=len(snaps), first_archived=C.fmt_date(ts_to_date(monthly[0])),
               last_archived=C.fmt_date(ts_to_date(monthly[-1])))

    cache: dict[str, float] = {}

    def snap_fp(ts: str) -> set[str] | None:
        got, err = fetcher.get(f"{ARCHIVE_BASE}/web/{ts}id_/http://{host}/", check_robots=False)
        out["fetches"] += 1
        if got is None or got[0].status_code >= 400:
            return None
        return fingerprint(UnicodeDammit(got[1]).unicode_markup or "")

    if live_html is None:
        got, err = fetcher.get(f"https://{host}/")
        if got is None:
            got, err = fetcher.get(f"http://{host}/")
        live_html = UnicodeDammit(got[1]).unicode_markup if got else None
    if live_html:
        live = fingerprint(live_html)
    else:
        live = snap_fp(monthly[-1]) or set()
        out["notes"].append("live site not reachable: latest snapshot used as the current design")

    def sim(i: int) -> float:
        ts = monthly[i]
        if ts not in cache:
            if out["fetches"] >= max_fetches:
                raise RuntimeError("fetch budget used up")
            fp = snap_fp(ts)
            cache[ts] = similarity(live, fp) if fp is not None else -1.0
        return cache[ts]

    try:
        if sim(len(monthly) - 1) < MATCH:
            # Archive has not caught the current design yet: it is newer than the last snapshot.
            last = ts_to_date(monthly[-1])
            out.update(current_design_first_seen=None, confidence="medium",
                       recent_redesign=C.months_between(last, today) <= 24)
            out["notes"].append(f"current design not in the archive; it post-dates {C.fmt_date(last)}")
            return out
        lo, hi = 0, len(monthly) - 1              # invariant: sim(hi) >= MATCH
        while lo < hi:
            mid = (lo + hi) // 2
            s = sim(mid)
            if s >= MATCH:
                hi = mid
            else:
                lo = mid + 1
    except RuntimeError:
        out["notes"].append("fetch budget used up: boundary approximate")
        hi = min((i for i, ts in enumerate(monthly) if cache.get(ts, -1) >= MATCH), default=len(monthly) - 1)
        out["confidence"] = "low"
    first = ts_to_date(monthly[hi])
    months = round(C.months_between(first, today), 1)
    out.update(current_design_first_seen=C.fmt_date(first), months_since=months, recent_redesign=months <= 24)
    if out["confidence"] is None:
        if hi == 0:
            out["confidence"] = "high"
            out["notes"].append("design unchanged since the first archived snapshot")
        else:
            before = cache.get(monthly[hi - 1])
            out["confidence"] = "high" if before is not None and 0 <= before < CLEAR_CHANGE else "medium"
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("domain")
    p.add_argument("--decay", type=int, help="Website_Decay_Score, to apply the R6 rule")
    p.add_argument("--max-fetches", type=int, default=10)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    r = check(args.domain, max_fetches=args.max_fetches)
    if args.decay is not None and r["recent_redesign"] is not None:
        r["r6_reject"] = bool(r["recent_redesign"] and args.decay <= 2)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"{r['domain']}: {r['status']}, {r['snapshots']} snapshots "
              f"({r['first_archived']} to {r['last_archived']})")
        print(f"  current design first seen: {r['current_design_first_seen'] or 'not archived yet'}"
              f" | recent (24 months): {r['recent_redesign']} | confidence: {r['confidence']} | fetches: {r['fetches']}")
        if "r6_reject" in r:
            print(f"  R6 verdict (decay {args.decay}): {'REJECT R6' if r['r6_reject'] else 'keep'}")
        for n in r["notes"]:
            print(f"  note: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
