#!/usr/bin/env python3
"""Merge search-stage research into an UNVERIFIED candidate workbook for one cluster.

Used when only web search is available (no page fetches): candidates carry the
facts search results support, each with its source URL, but they have NOT had
the website decay audit, owner-contact capture or registry checks, so they are
kept out of Active_Pipeline. The workbook says so on every sheet.

Input: one or more JSON files, each {"candidates": [...], "screened_out": [...]}
in the research-agent schema (company_name, city_area, products, industry,
is_manufacturer, revenue_cr, revenue_fy, revenue_source, revenue_url, rating,
rating_url, expansion_*, trade_fair*, sme_listing, promoters, website, exports,
popularity_or_group_flags, notes ...).

Usage:
  python3 scripts/candidates_xlsx.py --cluster Ludhiana --state Punjab --prefix LDH \
      data/work/ludhiana_*.json [--out output/Candidates_Ludhiana_UNVERIFIED.xlsx] [--no-db]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

RATING_HOSTS = ("acuite", "careratings", "careedge", "icra", "indiaratings", "crisil", "infomerics", "brickwork")
SIGNAL_SCORE = {t: s for t, (s, _) in C.TRIGGER_TYPES.items()}
FIT_FILL = {"Strong": "E2F0D9", "Good": "FFF2CC", "Check": "EDEDED"}
COLUMNS = [
    ("Cand_ID", 10), ("Fit", 8), ("Company_Name", 30), ("Website_URL", 24), ("Directors", 34), ("Next_Gen", 24),
    ("Owner_Mobile", 26), ("Contact_Page_1", 30), ("Contact_Page_2", 30), ("Contact_Page_3", 30),
    ("Industry", 20), ("Key_Products", 32), ("Area", 18), ("Revenue_Cr", 10), ("Revenue_FY", 10), ("Revenue_Source", 30), ("Revenue_Source_URL", 30),
    ("Size_Confidence", 22), ("Rating", 26), ("Signal_Type", 16), ("Signal_Detail", 36), ("Signal_Date", 12),
    ("Signal_Source_URL", 30), ("Other_Signals", 30), ("Promoters", 26), ("Year_Established", 10),
    ("Exports", 22), ("Screen_Check", 26), ("Likely_Offer", 22), ("Likely_Segments", 24), ("Still_To_Verify", 40),
    ("Notes", 40), ("All_Source_URLs", 50),
]
WRAP = {"Directors", "Next_Gen", "Owner_Mobile", "Contact_Page_1", "Contact_Page_2", "Contact_Page_3", "Company_Name", "Key_Products", "Revenue_Source", "Size_Confidence", "Rating", "Signal_Detail",
        "Other_Signals", "Promoters", "Exports", "Screen_Check", "Still_To_Verify", "Notes", "All_Source_URLs",
        "Likely_Offer", "Likely_Segments"}
URL_COLS = {"Website_URL", "Revenue_Source_URL", "Signal_Source_URL"}
THIN = Side(style="thin", color="D9D9D9")


def _blank(v) -> bool:
    return C.is_blank(v) or str(v).strip().lower() in {"none", "none found", "no"}


def _nf(v) -> bool:
    """Blank, or a researcher's 'Not found (...)' note rather than a value."""
    return _blank(v) or str(v).strip().lower().startswith("not found")


def flags_clear(v) -> bool:
    """Researchers write 'None found (...)' or 'No stock listing, group link or Wikipedia page found'."""
    t = str(v or "").strip().lower()
    return _blank(v) or t.startswith("none found") or (t.startswith("no ") and "found" in t)


def flexible_date(value) -> tuple[date | None, str]:
    d, prec = C.parse_date(value)
    if d:
        return d, prec
    s = str(value or "").strip().replace(",", "")
    s = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", s)
    for fmt, prec in (("%B %d %Y", "day"), ("%b %d %Y", "day"), ("%d %B %Y", "day"), ("%d %b %Y", "day"),
                      ("%Y-%m-%d", "day"), ("%d/%m/%Y", "day"), ("%d-%m-%Y", "day"), ("%B %Y", "month"),
                      ("%b %Y", "month"), ("%b-%y", "month")):
        try:
            return datetime.strptime(s, fmt).date(), prec
        except ValueError:
            continue
    m = re.search(r"\b(20\d{2})\b", s)
    return (date(int(m.group(1)), 1, 1), "year") if m else (None, "invalid")


def signal_type_for(kind: str, url: str) -> str:
    kind = (kind or "").lower()
    if "fair" in kind:
        return "Trade fair"
    if "sme" in kind or "ipo" in kind or "drhp" in kind:
        return "Pvt to Public or SME IPO"
    if "ec" in kind.split("/") or "cte" in kind or "clearance" in kind or "consent" in kind:
        return "EC/CTE expansion"
    if "incentive" in kind or "state" in kind:
        return "State incentive"
    if any(h in (url or "").lower() for h in RATING_HOSTS):
        return "Rating capex"
    return "Regional news"


def extract_signals(c: dict) -> list[dict]:
    # Explicit typed signals (researcher-curated) come first; field-derived ones follow.
    out = [dict(sig) for sig in c.get("signals_explicit", []) if isinstance(sig, dict)]
    if not _blank(c.get("expansion_signal")):
        kind = c.get("expansion_type") or ""
        out.append({"type": signal_type_for(kind, c.get("expansion_url", "")), "detail": c["expansion_signal"],
                    "date": c.get("expansion_date", ""), "url": c.get("expansion_url", "")})
    if not _blank(c.get("trade_fair")):
        out.append({"type": "Trade fair", "detail": c["trade_fair"], "date": c.get("trade_fair_date", ""),
                    "url": c.get("trade_fair_url", "")})
    if not _blank(c.get("sme_listing")):
        url = c.get("expansion_url", "") if "ipo" in (c.get("expansion_type") or "").lower() else ""
        out.append({"type": "Pvt to Public or SME IPO", "detail": c["sme_listing"],
                    "date": c.get("expansion_date", ""), "url": url or c.get("flags_url", "")})
    return out


def when_text(d: date, prec: str) -> str:
    return C.fmt_date(d) if prec == "day" else f"{C.MONTHS[d.month - 1]}-{d.year}" if prec == "month" else str(d.year)


def signal_valid(sig: dict, today: date) -> tuple[bool, str]:
    d, prec = flexible_date(sig.get("date"))
    if not C.first_url(sig.get("url")):
        return False, "no source URL"
    if d is None:
        return False, "date unclear"
    if sig["type"] == "Trade fair":
        return (d.year >= today.year - 1), f"{when_text(d, prec)} ({d.year} edition)"
    # Year-only dates start on 1 Jan, so they pass only when the whole year sits inside the window.
    return C.months_between(d, today) <= 18, when_text(d, prec)


FIELD_GROUPS = [  # fields that must travel together when two sweeps disagree
    ("revenue_cr", "revenue_fy", "revenue_source", "revenue_url"),
    ("promoters", "promoters_url"),
    ("rating", "rating_url"),
]


def name_key(name) -> str:
    return C.norm_company_name(re.sub(r"\(.*?\)", " ", str(name or "")))


def _fy_rank(fy) -> str:
    m = re.search(r"(20\d{2})", str(fy or ""))
    return m.group(1) if m else ""


def merge(records: list[dict]) -> list[dict]:
    by_key: dict[str, dict] = {}
    for rec in records:
        key = name_key(rec.get("company_name"))
        if not key:
            continue
        if key not in by_key:
            base = dict(rec)
            base["company_name"] = re.sub(r"\s*\(.*?\)\s*", " ", str(rec["company_name"])).strip()
            base["signals"] = extract_signals(rec)
            base["sources"] = set()
            base["found_by"] = {rec.get("_found_by", "")}
            by_key[key] = base
        else:
            base = by_key[key]
            grouped = {f for g in FIELD_GROUPS for f in g}
            special = grouped | {"is_manufacturer", "manufacturer_evidence", "popularity_or_group_flags",
                                 "flags_url", "review_note", "company_name", "signals_explicit"}
            for k, v in rec.items():
                if k.startswith("_") or k in special:
                    continue
                if _blank(base.get(k)) and not _blank(v):
                    base[k] = v
            # Revenue: take the other sweep's figure when ours is missing or older (whole group moves).
            new_rev = isinstance(rec.get("revenue_cr"), (int, float))
            old_rev = isinstance(base.get("revenue_cr"), (int, float))
            if new_rev and (not old_rev or _fy_rank(rec.get("revenue_fy")) > _fy_rank(base.get("revenue_fy"))):
                for k in FIELD_GROUPS[0]:
                    base[k] = rec.get(k)
            for group in FIELD_GROUPS[1:]:
                if _blank(base.get(group[0])) and not _blank(rec.get(group[0])):
                    for k in group:
                        base[k] = rec.get(k)
            # Manufacturer: evidenced "Yes" beats "Unclear".
            if (str(base.get("is_manufacturer", "")).lower() != "yes"
                    and str(rec.get("is_manufacturer", "")).lower() == "yes"):
                base["is_manufacturer"] = "Yes"
                base["manufacturer_evidence"] = rec.get("manufacturer_evidence")
            # Flags: a real flag from any sweep is kept; "none found" never overwrites it.
            f_old, f_new = base.get("popularity_or_group_flags"), rec.get("popularity_or_group_flags")
            if not flags_clear(f_new):
                if flags_clear(f_old):
                    base["popularity_or_group_flags"], base["flags_url"] = f_new, rec.get("flags_url")
                elif str(f_new) != str(f_old):
                    base["popularity_or_group_flags"] = f"{f_old} | {f_new}"
            if not _blank(rec.get("review_note")):
                base["review_note"] = "; ".join(x for x in [base.get("review_note"), rec["review_note"]] if not _blank(x))
            base["signals"] += extract_signals(rec)
            base["found_by"].add(rec.get("_found_by", ""))
        for v in rec.values():
            if isinstance(v, str):
                for u in C.URL_RE.findall(v):
                    by_key[key]["sources"].add(u.rstrip(".,;"))
    return list(by_key.values())


def reason_code(reason: str) -> str:
    """Best-effort reject code for a researcher's free-text screen-out reason ('' when unclear)."""
    explicit = re.search(r"\b(R1[0-2]|R[1-9])\b", reason or "")
    if explicit:
        return explicit.group(1)
    r = (reason or "").lower()
    rules = [("R10", r"existing client"), ("R5", r"main[\s-]*board|listed on (the )?(nse|bse)"),
             ("R4", r"subsidiary|group company|part of .* group|\bmnc\b|pe[/ -]?vc|private equity|venture"),
             ("R3", r"wikipedia|household|popular|well[- ]known brand|consumer brand"),
             ("R1", r"above (rs\.? ?|₹)?500|over (rs\.? ?|₹)?500|> ?500"), ("R2", r"below (rs\.? ?|₹)?50\b|under (rs\.? ?|₹)?50\b|< ?50\b"),
             ("R11", r"struck off|strike off|liquidation|dormant|inactive"),
             ("R8", r"aerospace|defen[cs]e"),
             ("R7", r"not a manufacturer|trader|trading|distribut|dealer|nbfc|financ|hotel|real estate|logistic|"
                    r"service|gas distribution|hospital|school|retail")]
    for code, rx in rules:
        if re.search(rx, r):
            return code
    return ""


def screen(c: dict, today: date) -> tuple[str | None, str]:
    """Return (reject_code, reason) when the brief's gates already rule the company out."""
    if not _blank(c.get("review_note")):
        return None, ""   # a researcher flagged this for a human decision: keep it visible as Check
    if str(c.get("is_manufacturer", "")).strip().lower() == "no":
        return "R7", f"not a manufacturer ({c.get('manufacturer_evidence') or 'per source'})"
    excl = C.match_exclusion(c.get("company_name", ""))
    if excl and excl[1] == "exact":
        return "R10", f"existing client ({excl[0]})"
    flags = "" if flags_clear(c.get("popularity_or_group_flags")) else str(c.get("popularity_or_group_flags") or "")
    if re.search(r"main[\s-]*board", flags, re.I) or (re.search(r"listed on (the )?(nse|bse)\b", flags, re.I)
                                                      and not re.search(r"sme|emerge", flags, re.I)):
        return "R5", f"main-board listed ({flags})"
    if re.search(r"wikipedia", flags, re.I) and not re.search(r"no wikipedia", flags, re.I):
        return "R3", f"has a Wikipedia page ({flags})"
    if re.search(r"subsidiary of|part of [\w\s&.]+ group|group company|\bmnc\b|private equity|venture capital|pe[- ]funded|vc[- ]funded",
                 flags, re.I) and not re.search(r"no (group|subsidiary)", flags, re.I):
        return "R4", f"group, MNC or PE/VC backed ({flags})"
    rev = c.get("revenue_cr")
    fy = str(c.get("revenue_fy") or "")
    fy_year = int(m.group(1)) if (m := re.search(r"(20\d{2})", fy)) else None
    if isinstance(rev, (int, float)):
        if rev > 500:
            return "R1", f"revenue ₹{rev:g} Cr ({fy or 'FY not stated'}) above ₹500 Cr"
        if rev < 50 and fy_year and fy_year >= today.year - 2:
            return "R2", f"revenue ₹{rev:g} Cr ({fy}) below ₹50 Cr"
    return None, ""


PAGE_PRIORITY = ["IndiaMART", "TradeIndia", "Justdial", "ExportersIndia", "Exhibitor page",
                 "Association directory", "Google Business", "Company contact page", "Other"]
NEXTGEN_RE = re.compile(r"next-gen \(probable|possible next-gen|^next-gen:", re.I)
OWNER_ROLE_RE = re.compile(r"director|chairman|\bcmd\b|\bmd\b|managing|owner|proprietor|promoter|partner|\bceo\b|"
                           r"founder|president", re.I)
DOUBT_RE = re.compile(r"not an mca director|not on (the )?mca board|likely staff|placeholder|unreliable|dealer|"
                      r"another firm|not an owner|directors page|profile page|published by the company", re.I)
BROKER_RE = re.compile(r"rocketreach|zoominfo|easyleadz|lusha|apollo\.io|signalhire|contactout|truecaller|"
                       r"leadiq|seamless\.ai|datanyze|slintel", re.I)


def enrich_fields(c: dict) -> dict:
    """Directors, next-gen and owner contact pages from the enrichment sweep (never data brokers)."""
    e = c.get("_enrich") or {}
    dirs = [d for d in e.get("directors") or [] if isinstance(d, dict) and not _blank(d.get("name"))]
    fmt = lambda d: d["name"] + (f" ({d['designation']})" if not _blank(d.get("designation")) else "") + (
        f", since {d['appointed']}" if not _blank(d.get("appointed")) else "")
    nextgen = [fmt(d) for d in dirs if NEXTGEN_RE.search(str(d.get("note", "")))]
    pages = [pg for pg in e.get("owner_contact_pages") or []
             if isinstance(pg, dict) and C.first_url(pg.get("url")) and not BROKER_RE.search(pg.get("url", ""))]
    rank = {t.lower(): i for i, t in enumerate(PAGE_PRIORITY)}

    def person(pg) -> str:
        t = str(pg.get("listed_contact_person") or "").strip()
        return "" if not t or re.match(r"not (found|shown|named)", t, re.I) else t

    def owner_named(pg) -> bool:
        t = person(pg)
        return bool(t) and bool(OWNER_ROLE_RE.search(t)) and not DOUBT_RE.search(t)

    # Owner-named listings first, then one page per type in priority order, then the rest.
    ordered, seen_types = [], set()
    by_rank = sorted(pages, key=lambda pg: rank.get(str(pg.get("type", "Other")).lower(), len(PAGE_PRIORITY)))
    for pg in [x for x in by_rank if owner_named(x)]:
        ordered.append(pg)
    for pg in by_rank:
        t = str(pg.get("type", "Other")).lower()
        if pg not in ordered and t not in seen_types:
            ordered.append(pg)
            seen_types.add(t)
    ordered += [pg for pg in by_rank if pg not in ordered]
    pages = ordered
    out = {"Directors": "; ".join(fmt(d) for d in dirs) or "Not found",
           "Next_Gen": "; ".join(nextgen) or "Not found",
           "Owner_Mobile": ("Open Contact_Page_1-3; use a number only if it belongs to the owner or a director"
                            if pages else "Not found yet: no self-published listing found")}
    if pages and owner_named(pages[0]):
        out["Owner_Mobile"] = (f"Likely on Contact_Page_1 ({pages[0].get('type')}), which names "
                               f"{person(pages[0])[:70]}. Confirm the number is theirs before calling")
    for i in range(3):
        if i < len(pages):
            pg = pages[i]
            who = f": {person(pg)[:70]}" if person(pg) else ""
            out[f"Contact_Page_{i + 1}"] = (f"{pg.get('type') or 'Page'}{who}", C.first_url(pg["url"]))
        else:
            out[f"Contact_Page_{i + 1}"] = ""
    site = e.get("website")
    if not _blank(site) and not C.is_shared_platform(site):
        out["_website"] = site
    return out


def assess(c: dict, today: date) -> dict:
    valid, other, seen = [], [], set()
    for s in c["signals"]:
        key = (s.get("type"), C.first_url(s.get("url")) or s.get("detail"))
        if key in seen:
            continue
        seen.add(key)
        ok, when = signal_valid(s, today)
        s["_when"] = when
        (valid if ok else other).append(s)
    valid.sort(key=lambda s: SIGNAL_SCORE.get(s["type"], 0), reverse=True)
    best = valid[0] if valid else None
    rev = c.get("revenue_cr") if isinstance(c.get("revenue_cr"), (int, float)) else None
    in_band = rev is not None and 50 <= rev <= 500
    manuf = str(c.get("is_manufacturer", "")).strip().lower() == "yes"
    clear = flags_clear(c.get("popularity_or_group_flags")) and _blank(c.get("review_note"))
    if in_band and manuf and clear and best and SIGNAL_SCORE.get(best["type"], 0) >= 3:
        fit = "Strong"
    elif in_band and manuf and clear:
        fit = "Good"
    else:
        fit = "Check"
    src = f"{c.get('revenue_source') or ''} {c.get('revenue_url') or ''}".lower()
    if rev is None:
        size_conf = "Not found"
    elif any(h in src for h in RATING_HOSTS) or "drhp" in src or "prospectus" in src:
        size_conf = "Medium (search extract of rating or DRHP; High once the document is opened)"
    elif "indiamart" in src or "tradeindia" in src or "band" in src:
        size_conf = "Medium (self-declared turnover band)"
    else:
        size_conf = "Medium (search extract)"
    ex = enrich_fields(c)
    site_found = not _nf(c.get("website")) or "_website" in ex
    todo = ["website decay audit", "owner mobile from the contact pages (owner or director only)",
            "MCA status and holding company"]
    if rev is None:
        todo.insert(0, "turnover")
    elif not in_band:
        todo.insert(0, f"turnover (₹{rev:g} Cr is outside ₹50-500 Cr or dated)")
    if not manuf:
        todo.insert(0, "confirm own plant (manufacturer)")
    if not site_found:
        todo.append("find website, or confirm none (SEG-NOWEB)")
    segs = [C.INDUSTRY_SEGMENT[c["industry"]]] if C.INDUSTRY_SEGMENT.get(c.get("industry")) else []
    if any(s["type"] == "Trade fair" for s in valid):
        segs.append("SEG-EXPO")
    if not _blank(c.get("exports")) and not str(c.get("exports")).lower().startswith("not"):
        segs.append("SEG-EXPORT")
    if any(s["type"] == "Pvt to Public or SME IPO" for s in c["signals"]):
        segs.append("CAPMKT")
    import score as _score   # same Section 10.8 rule the Active pipeline uses
    offer = _score.recommended_offer(set(segs), rev, False)
    return {
        "Fit": fit,
        "Company_Name": c.get("company_name"),
        "Industry": c.get("industry") if c.get("industry") in C.INDUSTRIES else (c.get("industry") or "Not found"),
        "Key_Products": c.get("products") or "Not found",
        "Area": c.get("city_area") or "Ludhiana",
        "Website_URL": (c.get("website") if not _nf(c.get("website")) and not C.is_shared_platform(c.get("website"))
                        else ex.get("_website") or "Not found"),
        **{k: v for k, v in ex.items() if not k.startswith("_")},
        "Revenue_Cr": rev if rev is not None else "Not found",
        "Revenue_FY": c.get("revenue_fy") or ("Not found" if rev is None else ""),
        "Revenue_Source": c.get("revenue_source") or "Not found",
        "Revenue_Source_URL": c.get("revenue_url") or "",
        "Size_Confidence": size_conf,
        "Rating": c.get("rating") or "Not found",
        "Signal_Type": best["type"] if best else "None within window",
        "Signal_Detail": best["detail"] if best else "",
        "Signal_Date": best["_when"] if best else "",
        "Signal_Source_URL": best["url"] if best else "",
        "Other_Signals": "; ".join(f"{s['type']}: {s['detail']} ({s['_when']})" for s in (valid[1:] + other)),
        "Promoters": c.get("promoters") or "Not found",
        "Year_Established": c.get("year_established") or "Not found",
        "Exports": c.get("exports") or "Not found",
        "Likely_Offer": offer + " (provisional)",
        "Likely_Segments": ", ".join(segs) or "Not found",
        "Screen_Check": "; ".join(x for x in [c.get("popularity_or_group_flags") or "None found",
                                              ("REVIEW: " + c["review_note"]) if not _blank(c.get("review_note")) else ""] if x),
        "Still_To_Verify": "; ".join(todo),
        "Notes": "; ".join(x for x in [c.get("manufacturer_evidence") if manuf else "", c.get("notes") or ""] if x),
        "All_Source_URLs": "\n".join(sorted(c["sources"])),
        "_score": SIGNAL_SCORE.get(best["type"], 0) if best else 0,
        "_rev": rev or 0,
    }


def _write(ws, headers, rows, widths, fill_key=None, fills=None, url_cols=(), wrap=()):
    ws.append(headers)
    for i, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=i)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="2F5496")
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 16)
    ws.row_dimensions[1].height = 32
    for r, row in enumerate(rows, 2):
        fill = PatternFill("solid", fgColor=fills[row[fill_key]]) if fill_key and row.get(fill_key) in (fills or {}) else None
        for i, h in enumerate(headers, 1):
            v = row.get(h)
            link = None
            if isinstance(v, tuple):
                v, link = v
            cell = ws.cell(row=r, column=i, value=C.sanitize_text(v) if isinstance(v, str) else v)
            cell.alignment = Alignment(wrap_text=h in wrap, vertical="top")
            cell.border = Border(bottom=THIN)
            if fill:
                cell.fill = fill
            target = link or (C.first_url(v) if isinstance(v, str) else None)
            if not target and h in url_cols and isinstance(v, str) and "." in v and " " not in v and not C.is_blank(v):
                target = "http://" + v
            if target:
                cell.hyperlink = target
                cell.font = Font(color="1F4E79", underline="single" if (h in url_cols or link) else None)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(len(rows) + 1, 2)}"


SWEEP_LABELS = {"acuite": "Acuité ratings sweep", "agencies": "CARE, ICRA, CRISIL, Infomerics, India Ratings, Brickwork sweep",
                "fairs": "Trade fairs and exporters sweep", "news_sme": "Expansion news and SME IPO sweep"}


def coverage_line(path) -> str:
    stem = Path(path).stem
    label = next((v for k, v in SWEEP_LABELS.items() if stem.endswith(k)), stem)
    st = json.loads(Path(path).read_text(encoding="utf-8")).get("sweep_status") or {}
    parts = [("Complete" if st.get("complete") else "Incomplete") if "complete" in st else ""]
    for key, name in (("reason", ""), ("covered", "Covered"), ("worked_best", "Worked best"), ("yield", "Yield"),
                      ("not_covered", "Not covered")):
        if st.get(key):
            parts.append(f"{name}: {st[key]}" if name else str(st[key]))
    return f"{label}: " + ". ".join(x.rstrip(".") for x in parts if x) + "."


def build(inputs: list[Path], cluster: str, state: str, prefix: str, out: Path, use_db: bool = True,
          today: date | None = None, enrich: list[Path] | None = None) -> dict:
    today = today or date.today()
    enrich_map = {}
    for path in enrich or []:
        for e in json.loads(Path(path).read_text(encoding="utf-8")):
            for nm in re.split(r"\s+and\s+(?=[A-Z])", e.get("company_name", "")):   # "Osho Forge Limited and Emson Gears Limited"
                if name_key(nm):
                    enrich_map.setdefault(name_key(nm), e)
    cands, screened = [], []
    for path in inputs:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        label = Path(path).stem
        for c in data.get("candidates", []):
            c["_found_by"] = label
            cands.append(c)
        for s in data.get("screened_out", []):
            screened.append({"Company_Name": s.get("company_name"), "Reject_Code": reason_code(s.get("reason")),
                             "Reason": s.get("reason"), "Source_URL": s.get("url"), "Found_By": label})
    merged = merge(cands)
    for c in merged:
        c["_enrich"] = enrich_map.get(name_key(c.get("company_name")))
    rows, follow = [], []
    for path in inputs:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        items = list(data.get("follow_ups", [])) + list((data.get("sweep_notes") or {}).get("unresolved_names_for_follow_up", []))
        for f in items:
            follow.append({"Lead": f, "Detail": "", "Source_URL": C.first_url(f) or "", "Found_By": Path(path).stem})
        for u in data.get("unresolved_leads", []):
            follow.append({"Lead": u.get("lead"), "Detail": u.get("detail"), "Source_URL": u.get("url"),
                           "Found_By": Path(path).stem})
    agent_rejects = {}
    for srow in screened:
        k = name_key(srow["Company_Name"])
        if k and srow.get("Reject_Code") and srow["Reject_Code"] != "R12":
            agent_rejects.setdefault(k, srow)
    for c in merged:
        hit = agent_rejects.get(name_key(c.get("company_name")))
        if hit and _blank(c.get("review_note")):
            screened.append({"Company_Name": c.get("company_name"), "Reject_Code": hit["Reject_Code"],
                             "Reason": f"{hit['Reason']} (from another sweep)", "Source_URL": hit["Source_URL"],
                             "Found_By": ", ".join(sorted(c["found_by"]))})
            continue
        thin = (str(c.get("is_manufacturer", "")).strip().lower() != "yes"
                and not isinstance(c.get("revenue_cr"), (int, float)) and not c["signals"])
        code, why = screen(c, today)
        if not code and thin:
            follow.append({"Lead": c.get("company_name"), "Detail": f"Manufacturer status and size unknown. "
                           f"{c.get('products') or ''}. {c.get('notes') or ''}".strip(),
                           "Source_URL": c.get("rating_url") or c.get("revenue_url") or "",
                           "Found_By": ", ".join(sorted(c["found_by"]))})
            continue
        if code:
            screened.append({"Company_Name": c.get("company_name"), "Reject_Code": code, "Reason": why,
                             "Source_URL": c.get("revenue_url") or c.get("flags_url") or c.get("rating_url") or "",
                             "Found_By": ", ".join(sorted(c["found_by"]))})
        else:
            rows.append(assess(c, today))
    # Drop screened-out duplicates of names that survived, and repeat rejections.
    kept = {name_key(r["Company_Name"]) for r in rows}
    seen, uniq = set(), []
    for s in screened:
        k = name_key(s["Company_Name"])
        if not k or k in kept or k in seen:
            continue
        seen.add(k)
        uniq.append(s)
    screened = uniq
    order = {"Strong": 0, "Good": 1, "Check": 2}
    rows.sort(key=lambda r: (order[r["Fit"]], -r["_score"], -r["_rev"], r["Company_Name"] or ""))
    for i, r in enumerate(rows, 1):
        r["Cand_ID"] = f"{prefix}-C{i:02d}"

    wb = Workbook()
    ws = wb.active
    ws.title = "Candidates"
    headers = [h for h, _ in COLUMNS]
    _write(ws, headers, rows, dict(COLUMNS), "Fit", FIT_FILL, URL_COLS, WRAP)
    ws.freeze_panes = "D2"   # ID, fit and company stay visible while scrolling
    ws4 = wb.create_sheet("Follow_Up")
    _write(ws4, ["Lead", "Detail", "Source_URL", "Found_By"], follow,
           {"Lead": 60, "Detail": 70, "Source_URL": 50, "Found_By": 22}, url_cols={"Source_URL"},
           wrap={"Lead", "Detail"})
    ws4.freeze_panes = "B2"
    ws2 = wb.create_sheet("Screened_Out")
    _write(ws2, ["Company_Name", "Reject_Code", "Reason", "Source_URL", "Found_By"], screened,
           {"Company_Name": 34, "Reject_Code": 10, "Reason": 60, "Source_URL": 50, "Found_By": 24},
           url_cols={"Source_URL"}, wrap={"Reason", "Company_Name"})
    ws2.freeze_panes = "B2"
    counts = {k: sum(1 for r in rows if r["Fit"] == k) for k in order}
    readme = [
        ["UNVERIFIED CANDIDATES: " + cluster.upper() + ", " + state.upper()],
        [f"Built {C.fmt_date(today)} from web search results only. Not the Active pipeline."],
        [""],
        ["WHY UNVERIFIED"],
        ["This environment's network policy blocks opening web pages, so every fact here comes from search result "
         "summaries of the linked documents. None of these companies has had the website decay audit, owner-contact "
         "capture or MCA checks yet, so none can enter Active_Pipeline until the pages can be opened."],
        [""],
        ["WHAT IS SOLID"],
        ["Each company name, product line, revenue figure, rating and signal carries the URL it came from. Nothing "
         "was estimated: 'Not found' means search did not show it. No phone numbers are written into this sheet, "
         "because numbers read from search summaries cannot be checked against the source page; the Contact_Page "
         "links take you to the page itself."],
        [""],
        ["HOW TO GET THE OWNER'S MOBILE"],
        ["Open Contact_Page_1 to 3. They are the company's own listings (IndiaMART, TradeIndia, Justdial, exhibitor "
         "or association pages), where owners often publish their own mobile. Use a number only if the listing names "
         "the owner or a director as the contact person; an office line or a sales executive's number is a company "
         "line, not the owner's. Never use data-broker sites (RocketReach, ZoomInfo and similar), Truecaller or bought "
         "lists: CLAUDE.md Section 8 rules them out. Directors come from MCA records via public aggregators; Next_Gen "
         "is a probable family successor, not confirmed."],
        [""],
        ["FIT"],
        [f"Strong ({counts['Strong']}): manufacturer, ₹50-500 Cr from a stated figure, no popularity or group flag, "
         "and a trigger within the brief's window (score 3 or more)."],
        [f"Good ({counts['Good']}): same, but no qualifying trigger found yet."],
        [f"Check ({counts['Check']}): turnover missing or outside the band, manufacturer status unclear, or a flag to review."],
        [""],
        ["SIGNAL WINDOW"],
        ["Triggers count only within 18 months of the build date; trade fairs count for the current or previous "
         "year's edition. Older signals are listed under Other_Signals for context."],
        [""],
        ["COVERAGE AND GAPS"],
    ] + [[coverage_line(pth)] for pth in inputs] + [
        [""],
        ["NEXT STEP"],
        ["Once web pages can be opened: audit each website (decay score 3+ required), confirm turnover from the "
         "source document, capture the owner's self-published mobile, check MCA status and holding company, then "
         "score and move qualifying companies into Giraffe_Leads_Master.xlsx."],
    ]
    ws3 = wb.create_sheet("Read_Me", 0)
    for line in readme:
        ws3.append(line)
    ws3.column_dimensions["A"].width = 120
    for row in ws3.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if cell.value and str(cell.value).isupper():
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="2F5496")
    wb.active = 1
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)

    if use_db:
        import db
        conn = db.connect()
        for r in rows:
            site = r["Website_URL"] if r["Website_URL"] != "Not found" else None
            cid, _ = db.add_candidate(conn, r["Company_Name"], state, cluster, site, "Search results",
                                      r["Revenue_Source_URL"] or r["Signal_Source_URL"] or None,
                                      f"{r['Cand_ID']} {r['Fit']}: unverified search-stage candidate")
            for u in r["All_Source_URLs"].split("\n"):
                if u:
                    db.log_source(conn, r["Company_Name"], "Search results", u,
                                  "Search-stage facts (unverified): see candidate workbook", state, cluster)
    return {"candidates": len(rows), "screened_out": len(screened), **counts, "out": str(out)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="+")
    p.add_argument("--cluster", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--prefix", required=True)
    p.add_argument("--out")
    p.add_argument("--no-db", action="store_true")
    p.add_argument("--enrich", nargs="*", default=[], help="website/directors/contact-page JSON files")
    args = p.parse_args(argv)
    out = Path(args.out or C.OUTPUT_DIR / f"Candidates_{args.cluster.replace(' ', '_')}_UNVERIFIED.xlsx")
    res = build([Path(x) for x in args.inputs], args.cluster, args.state, args.prefix, out, not args.no_db,
                enrich=[Path(x) for x in args.enrich])
    print(f"{res['candidates']} candidates (Strong {res['Strong']}, Good {res['Good']}, Check {res['Check']}), "
          f"{res['screened_out']} screened out -> {res['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
