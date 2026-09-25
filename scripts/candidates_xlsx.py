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
    ("Cand_ID", 10), ("Fit", 8), ("Company_Name", 30), ("Industry", 20), ("Key_Products", 32), ("Area", 18),
    ("Website_URL", 26), ("Revenue_Cr", 10), ("Revenue_FY", 10), ("Revenue_Source", 30), ("Revenue_Source_URL", 30),
    ("Size_Confidence", 22), ("Rating", 26), ("Signal_Type", 16), ("Signal_Detail", 36), ("Signal_Date", 12),
    ("Signal_Source_URL", 30), ("Other_Signals", 30), ("Promoters", 26), ("Year_Established", 10),
    ("Exports", 22), ("Screen_Check", 26), ("Still_To_Verify", 40), ("Notes", 40), ("All_Source_URLs", 50),
]
WRAP = {"Company_Name", "Key_Products", "Revenue_Source", "Size_Confidence", "Rating", "Signal_Detail",
        "Other_Signals", "Promoters", "Exports", "Screen_Check", "Still_To_Verify", "Notes", "All_Source_URLs"}
URL_COLS = {"Website_URL", "Revenue_Source_URL", "Signal_Source_URL"}
THIN = Side(style="thin", color="D9D9D9")


def _blank(v) -> bool:
    return C.is_blank(v) or str(v).strip().lower() in {"none", "none found", "no"}


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
    out = []
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


def signal_valid(sig: dict, today: date) -> tuple[bool, str]:
    d, prec = flexible_date(sig.get("date"))
    if not C.first_url(sig.get("url")):
        return False, "no source URL"
    if d is None:
        return False, "date unclear"
    if sig["type"] == "Trade fair":
        return (d.year >= today.year - 1), f"{d.year} edition"
    if sig["type"] == "Pvt to Public or SME IPO":
        return C.months_between(d, today) <= 18, C.fmt_date(d) if prec == "day" else str(d.year)
    return C.months_between(d, today) <= 18, (C.fmt_date(d) if prec == "day" else f"{C.MONTHS[d.month - 1]}-{d.year}")


def merge(records: list[dict]) -> list[dict]:
    by_key: dict[str, dict] = {}
    for rec in records:
        key = C.norm_company_name(rec.get("company_name"))
        if not key:
            continue
        if key not in by_key:
            base = dict(rec)
            base["signals"] = extract_signals(rec)
            base["sources"] = set()
            base["found_by"] = {rec.get("_found_by", "")}
            by_key[key] = base
        else:
            base = by_key[key]
            for k, v in rec.items():
                if k.startswith("_"):
                    continue
                if _blank(base.get(k)) and not _blank(v):
                    base[k] = v
            # Prefer the most recent revenue year when two sources disagree.
            fy_new, fy_old = str(rec.get("revenue_fy") or ""), str(base.get("revenue_fy") or "")
            if rec.get("revenue_cr") not in (None, "") and fy_new > fy_old:
                for k in ("revenue_cr", "revenue_fy", "revenue_source", "revenue_url"):
                    base[k] = rec.get(k)
            base["signals"] += extract_signals(rec)
            base["found_by"].add(rec.get("_found_by", ""))
        for v in rec.values():
            if isinstance(v, str):
                for u in C.URL_RE.findall(v):
                    by_key[key]["sources"].add(u.rstrip(".,;"))
    return list(by_key.values())


def reason_code(reason: str) -> str:
    """Best-effort reject code for a researcher's free-text screen-out reason ('' when unclear)."""
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
    if str(c.get("is_manufacturer", "")).strip().lower() == "no":
        return "R7", f"not a manufacturer ({c.get('manufacturer_evidence') or 'per source'})"
    excl = C.match_exclusion(c.get("company_name", ""))
    if excl and excl[1] == "exact":
        return "R10", f"existing client ({excl[0]})"
    flags = str(c.get("popularity_or_group_flags") or "")
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


def assess(c: dict, today: date) -> dict:
    valid, other = [], []
    for s in c["signals"]:
        ok, when = signal_valid(s, today)
        s["_when"] = when
        (valid if ok else other).append(s)
    valid.sort(key=lambda s: SIGNAL_SCORE.get(s["type"], 0), reverse=True)
    best = valid[0] if valid else None
    rev = c.get("revenue_cr") if isinstance(c.get("revenue_cr"), (int, float)) else None
    in_band = rev is not None and 50 <= rev <= 500
    manuf = str(c.get("is_manufacturer", "")).strip().lower() == "yes"
    flags_clear = _blank(c.get("popularity_or_group_flags"))
    if in_band and manuf and flags_clear and best and SIGNAL_SCORE.get(best["type"], 0) >= 3:
        fit = "Strong"
    elif in_band and manuf and flags_clear:
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
    todo = ["website decay audit", "owner mobile (self-published only)", "MCA status and holding company"]
    if rev is None:
        todo.insert(0, "turnover")
    elif not in_band:
        todo.insert(0, f"turnover (₹{rev:g} Cr is outside ₹50-500 Cr or dated)")
    if not manuf:
        todo.insert(0, "confirm own plant (manufacturer)")
    if _blank(c.get("website")):
        todo.append("find website, or confirm none (SEG-NOWEB)")
    segs = []
    if best and best["type"] == "Trade fair":
        segs.append("SEG-EXPO")
    if any(s["type"] == "Pvt to Public or SME IPO" for s in c["signals"]):
        segs.append("CAPMKT")
    return {
        "Fit": fit,
        "Company_Name": c.get("company_name"),
        "Industry": c.get("industry") if c.get("industry") in C.INDUSTRIES else (c.get("industry") or "Not found"),
        "Key_Products": c.get("products") or "Not found",
        "Area": c.get("city_area") or "Ludhiana",
        "Website_URL": c.get("website") if not _blank(c.get("website")) else "Not found",
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
        "Screen_Check": c.get("popularity_or_group_flags") or "None found",
        "Still_To_Verify": "; ".join(todo),
        "Notes": "; ".join(x for x in [c.get("manufacturer_evidence") if manuf else "", c.get("notes") or "",
                                       ("Segments: " + ", ".join(segs)) if segs else ""] if x),
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
            cell = ws.cell(row=r, column=i, value=C.sanitize_text(v) if isinstance(v, str) else v)
            cell.alignment = Alignment(wrap_text=h in wrap, vertical="top")
            cell.border = Border(bottom=THIN)
            if fill:
                cell.fill = fill
            target = C.first_url(v) if isinstance(v, str) else None
            if not target and h in url_cols and isinstance(v, str) and "." in v and " " not in v and not C.is_blank(v):
                target = "http://" + v
            if target:
                cell.hyperlink = target
                cell.font = Font(color="1F4E79", underline="single" if h in url_cols else None)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(len(rows) + 1, 2)}"


def build(inputs: list[Path], cluster: str, state: str, prefix: str, out: Path, use_db: bool = True,
          today: date | None = None) -> dict:
    today = today or date.today()
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
    rows = []
    for c in merged:
        code, why = screen(c, today)
        if code:
            screened.append({"Company_Name": c.get("company_name"), "Reject_Code": code, "Reason": why,
                             "Source_URL": c.get("revenue_url") or c.get("flags_url") or c.get("rating_url") or "",
                             "Found_By": ", ".join(sorted(c["found_by"]))})
        else:
            rows.append(assess(c, today))
    # Drop screened-out duplicates of names that survived, and repeat rejections.
    kept = {C.norm_company_name(r["Company_Name"]) for r in rows}
    seen, uniq = set(), []
    for s in screened:
        k = C.norm_company_name(s["Company_Name"])
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
    ws.freeze_panes = "D2"
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
         "was estimated: 'Not found' means search did not show it. No phone numbers or emails are listed, because "
         "numbers read from search summaries cannot be checked against the source page."],
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
    args = p.parse_args(argv)
    out = Path(args.out or C.OUTPUT_DIR / f"Candidates_{args.cluster.replace(' ', '_')}_UNVERIFIED.xlsx")
    res = build([Path(x) for x in args.inputs], args.cluster, args.state, args.prefix, out, not args.no_db)
    print(f"{res['candidates']} candidates (Strong {res['Strong']}, Good {res['Good']}, Check {res['Check']}), "
          f"{res['screened_out']} screened out -> {res['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
