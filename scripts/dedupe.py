#!/usr/bin/env python3
"""Deduplication against the lead DB (CLAUDE.md Section 12, step 2).

Key priority: GSTIN (matched on its PAN part, so one company registered in two
states is still one company), then CIN, then website domain, then normalised
company name + city. A name match in a different or unknown city is reported
as a soft match: shown as a warning, never blocking.

Usage:
  python3 scripts/dedupe.py check --name "Sharma Forgings Pvt Ltd" --city Ludhiana \
        [--url sharmaforgings.com] [--gstin 03ABCDE1234F1Z5] [--cin U27100PB...]
  python3 scripts/dedupe.py scan          # duplicate groups already inside the DB
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

TABLES = {  # table -> (reference expression, company column)
    "leads": ("Lead_ID", "Company_Name"),
    "rejected": ("'REJ-' || id || ' ' || Reject_Code", "Company_Name"),
    "candidates": ("'CAND-' || id || ' ' || Status", "Company_Name"),
}


def keys_for(name, city, url, gstin, cin) -> dict:
    name_key = C.norm_company_name(name)
    city_key = C.norm_city(city)
    return {
        "Key_GSTIN": C.clean_gstin(gstin) or None,
        "Key_CIN": C.clean_cin(cin) or None,
        "Key_Domain": C.domain_key(url) or None,
        "Key_Name": name_key or None,
        "Key_NameCity": f"{name_key}|{city_key}" if name_key and city_key else None,
    }


def _pan(gstin: str | None) -> str | None:
    return gstin[2:12] if gstin and len(gstin) == 15 else None


def find_matches(conn: sqlite3.Connection, keys: dict, exclude_lead_id: str | None = None) -> list[dict]:
    """Return matches in key-priority order: [{table, id, ref, company, key, strength}]."""
    checks = []
    pan = _pan(keys.get("Key_GSTIN"))
    if pan:
        checks.append(("GSTIN (PAN)", "substr(Key_GSTIN, 3, 10) = ?", pan, "hard"))
    if keys.get("Key_CIN"):
        checks.append(("CIN", "Key_CIN = ?", keys["Key_CIN"], "hard"))
    if keys.get("Key_Domain"):
        checks.append(("domain", "Key_Domain = ?", keys["Key_Domain"], "hard"))
    if keys.get("Key_NameCity"):
        checks.append(("name+city", "Key_NameCity = ?", keys["Key_NameCity"], "hard"))
    if keys.get("Key_Name"):
        checks.append(("name only", "Key_Name = ?", keys["Key_Name"], "soft"))

    seen, out = set(), []
    for label, where, value, strength in checks:
        for table, (ref_expr, company_col) in TABLES.items():
            id_col = "Lead_ID" if table == "leads" else "id"
            q = f"SELECT {id_col} AS rid, {ref_expr} AS ref, {company_col} AS company FROM {table} WHERE {where}"
            for r in conn.execute(q, (value,)):
                if table == "leads" and exclude_lead_id and r["rid"] == exclude_lead_id:
                    continue
                if (table, r["rid"]) in seen:
                    continue
                seen.add((table, r["rid"]))
                out.append({"table": table, "id": r["rid"], "ref": r["ref"], "company": r["company"],
                            "key": label, "strength": strength})
    return out


def scan(conn: sqlite3.Connection) -> list[str]:
    """Report duplicate groups already in the DB (should be empty)."""
    problems = []
    for key in ("Key_CIN", "Key_Domain", "Key_NameCity"):
        q = (f"SELECT {key} AS k, GROUP_CONCAT(Lead_ID, ', ') AS ids FROM leads "
             f"WHERE {key} IS NOT NULL GROUP BY {key} HAVING COUNT(*) > 1")
        problems += [f"leads share {key} = {r['k']}: {r['ids']}" for r in conn.execute(q)]
    q = ("SELECT substr(Key_GSTIN, 3, 10) AS k, GROUP_CONCAT(Lead_ID, ', ') AS ids FROM leads "
         "WHERE Key_GSTIN IS NOT NULL GROUP BY k HAVING COUNT(*) > 1")
    problems += [f"leads share PAN {r['k']}: {r['ids']}" for r in conn.execute(q)]
    for key in ("Key_CIN", "Key_Domain", "Key_NameCity"):
        q = (f"SELECT l.Lead_ID AS lid, r.id AS rid, r.Reject_Code AS code FROM leads l "
             f"JOIN rejected r ON l.{key} = r.{key} WHERE l.{key} IS NOT NULL")
        problems += [f"lead {r['lid']} also rejected as REJ-{r['rid']} {r['code']} ({key})" for r in conn.execute(q)]
    for r in conn.execute("SELECT Lead_ID, Company_Name FROM leads"):
        ex = C.match_exclusion(r["Company_Name"])
        if ex and ex[1] == "exact":
            problems.append(f"lead {r['Lead_ID']} {r['Company_Name']} matches exclusion '{ex[0]}' (R10)")
    return problems


def main(argv=None) -> int:
    import db

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default=str(C.DB_PATH))
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--name", required=True)
    for flag in ("--city", "--url", "--gstin", "--cin"):
        c.add_argument(flag)
    sub.add_parser("scan")
    args = p.parse_args(argv)
    conn = db.connect(args.db)

    if args.cmd == "check":
        excl = C.match_exclusion(args.name)
        if excl and excl[1] == "exact":
            print(f"EXCLUDED: matches '{excl[0]}' in config/exclusions.txt (reject R10)")
        elif excl:
            print(f"CAUTION: name is close to client '{excl[0]}': check for a group link")
            excl = None
        gst = C.clean_gstin(args.gstin)
        if gst and not (C.GSTIN_RE.match(gst) and C.gstin_checksum_ok(gst)):
            print(f"warning: GSTIN {gst} fails the format or checksum test")
        matches = find_matches(conn, keys_for(args.name, args.city, args.url, args.gstin, args.cin))
        if not matches:
            print("new: no match in leads, rejected or candidates")
        for m in matches:
            print(f"{m['strength'].upper():<5} {m['table']:<10} {m['ref']} | {m['company']} | via {m['key']}")
        return 2 if excl or any(m["strength"] == "hard" for m in matches) else 0
    problems = scan(conn)
    print("\n".join(problems) if problems else "clean: no duplicates found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
