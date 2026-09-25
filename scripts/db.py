#!/usr/bin/env python3
"""SQLite store for the lead engine. data/leads.db is the single source of truth.

Usage (run from the repo root):
  python3 scripts/db.py init
  python3 scripts/db.py add-lead data/work/PB-lead.json [--dry-run]
  python3 scripts/db.py add-reject data/work/rejects.json
  python3 scripts/db.py unreject 12        # new evidence overturns rejection 12
  python3 scripts/db.py add-candidate --name "X Forgings" --state Punjab --city Ludhiana \
        --source-type "Rating rationale" --source-url https://... [--url https://x.com]
  python3 scripts/db.py candidates [--state PB] [--status NEW]
  python3 scripts/db.py set-candidate ID STATUS [--ref PB-004]
  python3 scripts/db.py log-source --ref "X Forgings" --type "Rating rationale" --url https://... \
        --what "FY25 revenue, promoters, capex" [--state Punjab] [--city Ludhiana]
  python3 scripts/db.py get PB-001
  python3 scripts/db.py stats

add-lead and add-reject take one JSON object or a list of them. add-lead runs
scripts/score.py (scoring + validation) and scripts/dedupe.py before writing.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import dedupe  # noqa: E402

KEY_COLUMNS = ["Key_GSTIN", "Key_CIN", "Key_Domain", "Key_Name", "Key_NameCity"]
LEAD_EXTRA = [("Pipeline", "TEXT"), ("Reason_For_Longterm", "TEXT"), ("State_Entry", "TEXT"),
              ("Cluster", "TEXT"), ("Score_Inputs", "TEXT"), ("Created_At", "TEXT"), ("Updated_At", "TEXT")]
CANDIDATE_STATUSES = ["NEW", "ACTIVE", "LONGTERM", "REJECTED", "PARKED"]


def _schema() -> str:
    lead_cols = [f'"{n}" {t}' + (" PRIMARY KEY" if n == "Lead_ID" else "") for n, t, _, _ in C.ACTIVE_SPECS]
    lead_cols += [f'"{n}" {t}' for n, t in LEAD_EXTRA] + [f'"{k}" TEXT' for k in KEY_COLUMNS]
    rej_cols = [f'"{n}" {t}' for n, t, _, _ in C.REJECTED_SPECS]
    rej_cols += ['"GSTIN" TEXT', '"CIN" TEXT', '"State_Entry" TEXT', '"Created_At" TEXT']
    rej_cols += [f'"{k}" TEXT' for k in KEY_COLUMNS]
    return f"""
CREATE TABLE IF NOT EXISTS leads ({", ".join(lead_cols)});
CREATE TABLE IF NOT EXISTS rejected (id INTEGER PRIMARY KEY AUTOINCREMENT, {", ".join(rej_cols)});
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Company_Name TEXT NOT NULL, State TEXT, City_Cluster TEXT, Website_URL TEXT,
    Discovery_Source_Type TEXT, Discovery_URL TEXT, Status TEXT DEFAULT 'NEW',
    Outcome_Ref TEXT, Notes TEXT, Date_Found TEXT, State_Entry TEXT,
    Key_GSTIN TEXT, Key_CIN TEXT, Key_Domain TEXT, Key_Name TEXT, Key_NameCity TEXT,
    Created_At TEXT, Updated_At TEXT);
CREATE TABLE IF NOT EXISTS source_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT, Lead_ID_or_Company TEXT, Source_Type TEXT, URL TEXT, What_Was_Taken TEXT,
    State_Entry TEXT, Created_At TEXT);
CREATE INDEX IF NOT EXISTS ix_leads_keys ON leads (Key_GSTIN, Key_CIN, Key_Domain, Key_NameCity);
CREATE INDEX IF NOT EXISTS ix_rej_keys ON rejected (Key_GSTIN, Key_CIN, Key_Domain, Key_NameCity);
CREATE INDEX IF NOT EXISTS ix_cand_keys ON candidates (Key_Domain, Key_NameCity);
"""


def connect(path: Path | str = C.DB_PATH) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(_schema())
    return conn


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _state_entry_name(state: str, city: str | None) -> tuple[str | None, str | None]:
    entry, cluster = C.resolve_state(state, city)
    return (entry["state"] if entry else None), cluster


# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------

def next_lead_id(conn: sqlite3.Connection, code: str) -> str:
    rows = conn.execute("SELECT Lead_ID FROM leads WHERE Lead_ID LIKE ?", (f"{code}-%",)).fetchall()
    nums = [int(r[0].split("-")[1]) for r in rows if r[0].split("-")[1].isdigit()]
    return f"{code}-{(max(nums) + 1) if nums else 1:03d}"


def upsert_lead(conn: sqlite3.Connection, row: dict) -> tuple[str, bool]:
    """Write an evaluated lead row (output of score.evaluate). Returns (Lead_ID, created)."""
    keys = dedupe.keys_for(row.get("Company_Name"), row.get("City_Cluster"), row.get("Website_URL"),
                           row.get("GSTIN"), row.get("CIN"))
    lead_id = row.get("Lead_ID")
    existing = None
    if lead_id:
        existing = conn.execute("SELECT Lead_ID FROM leads WHERE Lead_ID = ?", (lead_id,)).fetchone()
    matches = dedupe.find_matches(conn, keys, exclude_lead_id=lead_id if existing else None)
    # A candidate row is the discovery record of this same company, so it never blocks.
    hard = [m for m in matches if m["strength"] == "hard" and m["table"] != "candidates"]
    if hard:
        m = hard[0]
        fix = ("update that lead instead (put its Lead_ID in the JSON)" if m["table"] == "leads"
               else f"run 'db.py unreject {m['id']}' first if new evidence overturns the rejection")
        raise ValueError(f"Duplicate of {m['table']} {m['ref']} ({m['company']}) on {m['key']}: {fix}.")
    entry = C.resolve_state(row["State"], row.get("City_Cluster"))[0]
    if entry is None:
        raise ValueError(f"Unknown state '{row.get('State')}'")
    if lead_id and not existing:
        raise ValueError(f"Lead_ID {lead_id} does not exist: omit Lead_ID for a new lead")
    if not existing:
        lead_id = next_lead_id(conn, entry["code"])
    record = {c: row.get(c) for c in C.ACTIVE_COLUMNS}
    record["Lead_ID"] = lead_id
    record.update({
        "Pipeline": row["Pipeline"], "Reason_For_Longterm": row.get("Reason_For_Longterm"),
        "State_Entry": row.get("State_Entry"), "Cluster": row.get("Cluster"),
        "Score_Inputs": json.dumps(row.get("Score_Inputs") or {}, ensure_ascii=False),
        "Updated_At": _now(), **keys,
    })
    if existing:
        # Never overwrite what the calling team typed into the tracker columns.
        for col in C.GROUP_COLUMNS["Calling tracker"]:
            record.pop(col, None)
        sets = ", ".join(f'"{k}" = ?' for k in record if k != "Lead_ID")
        conn.execute(f"UPDATE leads SET {sets} WHERE Lead_ID = ?",
                     [v for k, v in record.items() if k != "Lead_ID"] + [lead_id])
        created = False
    else:
        record["Created_At"] = _now()
        if not record.get("Status"):
            record["Status"] = "New" if row["Pipeline"] == "ACTIVE" else None
        cols = ", ".join(f'"{k}"' for k in record)
        conn.execute(f"INSERT INTO leads ({cols}) VALUES ({', '.join('?' for _ in record)})",
                     list(record.values()))
        created = True
    # Close the loop on the discovery queue.
    for m in matches:
        if m["table"] == "candidates":
            conn.execute("UPDATE candidates SET Status = ?, Outcome_Ref = ?, Updated_At = ? WHERE id = ?",
                         (row["Pipeline"], lead_id, _now(), m["id"]))
    conn.commit()
    return lead_id, created


# ---------------------------------------------------------------------------
# Rejected, candidates, source log
# ---------------------------------------------------------------------------

def add_reject(conn: sqlite3.Connection, rej: dict) -> tuple[int | None, str]:
    missing = [k for k in ("Company_Name", "State", "Reject_Code", "Reject_Evidence") if C.is_blank(rej.get(k))]
    if missing:
        raise ValueError(f"Reject missing {missing}")
    code = str(rej["Reject_Code"]).upper().strip()
    if code not in C.REJECT_CODES:
        raise ValueError(f"Reject_Code must be R1 to R12, got {rej['Reject_Code']}")
    date_str = rej.get("Date") or C.today_str()
    if C.parse_date(date_str)[1] != "day":
        raise ValueError(f"Date must be DD-MMM-YYYY, got {date_str}")
    keys = dedupe.keys_for(rej["Company_Name"], rej.get("City"), rej.get("Website_URL"),
                           rej.get("GSTIN"), rej.get("CIN"))
    for m in dedupe.find_matches(conn, keys):
        if m["table"] == "rejected" and m["strength"] == "hard":
            return None, f"already rejected ({m['ref']}, {m['key']})"
        if m["table"] == "leads" and m["strength"] == "hard" and code != "R9":
            raise ValueError(f"{rej['Company_Name']} is already lead {m['ref']}; update or remove that lead first")
    state_entry, _ = _state_entry_name(rej["State"], rej.get("City"))
    record = {c: rej.get(c) for c in C.REJECTED_COLUMNS}
    record.update({"Reject_Code": code, "Date": date_str,
                   "Reject_Evidence": C.sanitize_text(rej["Reject_Evidence"]),
                   "GSTIN": C.clean_gstin(rej.get("GSTIN")) or None, "CIN": C.clean_cin(rej.get("CIN")) or None,
                   "State_Entry": state_entry, "Created_At": _now(), **keys})
    cols = ", ".join(f'"{k}"' for k in record)
    cur = conn.execute(f"INSERT INTO rejected ({cols}) VALUES ({', '.join('?' for _ in record)})",
                       list(record.values()))
    for m in dedupe.find_matches(conn, keys):
        if m["table"] == "candidates":
            conn.execute("UPDATE candidates SET Status = 'REJECTED', Outcome_Ref = ?, Updated_At = ? WHERE id = ?",
                         (code, _now(), m["id"]))
    conn.commit()
    return cur.lastrowid, "added"


def add_candidate(conn: sqlite3.Connection, name: str, state: str, city: str | None = None,
                  url: str | None = None, source_type: str | None = None, source_url: str | None = None,
                  notes: str | None = None) -> tuple[int | None, str]:
    keys = dedupe.keys_for(name, city, url, None, None)
    for m in dedupe.find_matches(conn, keys):
        if m["strength"] == "hard":
            return None, f"known: {m['table']} {m['ref']} ({m['company']}) via {m['key']}"
    excl = C.match_exclusion(name)
    if excl and excl[1] == "exact":
        return None, f"existing client or exclusion ({excl[0]}): reject R10"
    if excl:
        notes = f"{notes + '; ' if notes else ''}name close to client '{excl[0]}': check group link"
    state_entry, _ = _state_entry_name(state, city)
    cur = conn.execute(
        """INSERT INTO candidates (Company_Name, State, City_Cluster, Website_URL, Discovery_Source_Type,
           Discovery_URL, Status, Notes, Date_Found, State_Entry, Key_GSTIN, Key_CIN, Key_Domain, Key_Name,
           Key_NameCity, Created_At, Updated_At) VALUES (?, ?, ?, ?, ?, ?, 'NEW', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, state, city, url, source_type, source_url, notes, C.today_str(), state_entry,
         keys["Key_GSTIN"], keys["Key_CIN"], keys["Key_Domain"], keys["Key_Name"], keys["Key_NameCity"],
         _now(), _now()))
    conn.commit()
    return cur.lastrowid, "added"


def log_source(conn: sqlite3.Connection, ref: str, source_type: str, url: str, what: str,
               state: str | None = None, city: str | None = None, date_str: str | None = None) -> int:
    state_entry = _state_entry_name(state, city)[0] if state else None
    cur = conn.execute(
        "INSERT INTO source_log (Date, Lead_ID_or_Company, Source_Type, URL, What_Was_Taken, State_Entry, Created_At)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (date_str or C.today_str(), ref, source_type, url, C.sanitize_text(what), state_entry, _now()))
    conn.commit()
    return cur.lastrowid


def counts_by_state_entry(conn: sqlite3.Connection) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}

    def bump(entry, key, n):
        d = out.setdefault(entry or "(unmapped)", {"A": 0, "B": 0, "C": 0, "longterm": 0, "rejected": 0, "sources": 0})
        d[key] += n

    for r in conn.execute("SELECT State_Entry, Pipeline, Tier, COUNT(*) FROM leads GROUP BY 1, 2, 3"):
        bump(r[0], "longterm" if r[1] == "LONGTERM" else (r[2] or "C"), r[3])
    for r in conn.execute("SELECT State_Entry, COUNT(*) FROM rejected GROUP BY 1"):
        bump(r[0], "rejected", r[1])
    for r in conn.execute("SELECT State_Entry, COUNT(*) FROM source_log GROUP BY 1"):
        bump(r[0], "sources", r[1])
    for d in out.values():
        d["screened"] = d["A"] + d["B"] + d["C"] + d["longterm"] + d["rejected"]
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_json_items(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def main(argv=None) -> int:
    import score  # local import: score imports common only

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default=str(C.DB_PATH))
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    a = sub.add_parser("add-lead"); a.add_argument("file"); a.add_argument("--dry-run", action="store_true")
    a = sub.add_parser("add-reject"); a.add_argument("file")
    a = sub.add_parser("unreject"); a.add_argument("id", type=int)
    a = sub.add_parser("add-candidate")
    for flag in ("--name", "--state"):
        a.add_argument(flag, required=True)
    for flag in ("--city", "--url", "--source-type", "--source-url", "--notes"):
        a.add_argument(flag)
    a = sub.add_parser("candidates"); a.add_argument("--state"); a.add_argument("--status")
    a = sub.add_parser("set-candidate"); a.add_argument("id", type=int)
    a.add_argument("status", choices=CANDIDATE_STATUSES); a.add_argument("--ref"); a.add_argument("--notes")
    a = sub.add_parser("log-source")
    for flag in ("--ref", "--type", "--url", "--what"):
        a.add_argument(flag, required=True)
    for flag in ("--state", "--city", "--date"):
        a.add_argument(flag)
    a = sub.add_parser("get"); a.add_argument("lead_id")
    sub.add_parser("stats")
    args = p.parse_args(argv)

    conn = connect(args.db)
    if args.cmd == "init":
        print(f"Schema ready at {args.db}")
    elif args.cmd == "add-lead":
        failed = 0
        for item in _load_json_items(args.file):
            res = score.evaluate(item)
            name = item.get("Company_Name", "?")
            for w in res.warnings:
                print(f"  warn  [{name}] {w}")
            if res.errors:
                failed += 1
                for e in res.errors:
                    print(f"  ERROR [{name}] {e}")
                continue
            r = res.row
            summary = (f"Tier {r.get('Tier')} | Priority {r.get('Priority_Score')} | Gap {r.get('Gap_Score')} "
                       f"(S{r.get('Strength_Score')} V{r.get('Visibility_Score')}) | Trigger {r.get('Trigger_Score')} "
                       f"| Contact {r.get('Contact_Score')} | {r.get('Recommended_Offer')}"
                       if r["Pipeline"] == "ACTIVE" else "LONGTERM")
            if args.dry_run:
                print(f"  ok    [{name}] {summary} (dry run, not written)")
                continue
            try:
                lead_id, created = upsert_lead(conn, r)
            except ValueError as e:
                failed += 1
                print(f"  ERROR [{name}] {e}")
                continue
            print(f"  {'added' if created else 'updated'} {lead_id} [{name}] {summary}")
        return 1 if failed else 0
    elif args.cmd == "add-reject":
        failed = 0
        for item in _load_json_items(args.file):
            try:
                rid, msg = add_reject(conn, item)
                print(f"  {msg}: {item.get('Company_Name')} {item.get('Reject_Code')}")
            except ValueError as e:
                failed += 1
                print(f"  ERROR {e}")
        return 1 if failed else 0
    elif args.cmd == "unreject":
        r = conn.execute("SELECT Company_Name, Reject_Code FROM rejected WHERE id = ?", (args.id,)).fetchone()
        if not r:
            print(f"no rejected row {args.id}")
            return 1
        conn.execute("DELETE FROM rejected WHERE id = ?", (args.id,))
        conn.commit()
        print(f"removed rejection {args.id}: {r['Company_Name']} {r['Reject_Code']}")
    elif args.cmd == "add-candidate":
        cid, msg = add_candidate(conn, args.name, args.state, args.city, args.url, args.source_type,
                                 args.source_url, args.notes)
        print(f"candidate {cid}: {msg}" if cid else f"skipped: {msg}")
    elif args.cmd == "candidates":
        q, params = "SELECT * FROM candidates WHERE 1=1", []
        if args.state:
            entry = C.resolve_state(args.state)[0]
            codes = [e["state"] for e in C.state_entries() if entry and e["code"] == entry["code"]]
            q += f" AND State_Entry IN ({', '.join('?' for _ in codes)})"
            params += codes
        if args.status:
            q += " AND Status = ?"
            params.append(args.status.upper())
        for r in conn.execute(q + " ORDER BY id", params):
            print(f"{r['id']:>4} {r['Status']:<8} {r['Company_Name']} | {r['City_Cluster'] or ''} | "
                  f"{r['Website_URL'] or ''} | {r['Discovery_Source_Type'] or ''} {r['Discovery_URL'] or ''}")
    elif args.cmd == "set-candidate":
        conn.execute("UPDATE candidates SET Status = ?, Outcome_Ref = COALESCE(?, Outcome_Ref), "
                     "Notes = COALESCE(?, Notes), Updated_At = ? WHERE id = ?",
                     (args.status, args.ref, args.notes, _now(), args.id))
        conn.commit()
        print(f"candidate {args.id} -> {args.status}")
    elif args.cmd == "log-source":
        if args.type not in C.SOURCE_TYPES:
            print(f"Source type must be one of: {', '.join(C.SOURCE_TYPES)}")
            return 1
        print(f"source_log id {log_source(conn, args.ref, args.type, args.url, args.what, args.state, args.city, args.date)}")
    elif args.cmd == "get":
        r = conn.execute("SELECT * FROM leads WHERE Lead_ID = ?", (args.lead_id,)).fetchone()
        print(json.dumps(dict(r), ensure_ascii=False, indent=2) if r else "not found")
    elif args.cmd == "stats":
        totals = conn.execute("SELECT Pipeline, Tier, COUNT(*) FROM leads GROUP BY 1, 2").fetchall()
        print("Leads:", ", ".join(f"{r[0]} {r[1] or ''}: {r[2]}" for r in totals) or "none")
        print("Rejected:", conn.execute("SELECT COUNT(*) FROM rejected").fetchone()[0])
        print("Candidates:", ", ".join(f"{r[0]}: {r[1]}" for r in
                                      conn.execute("SELECT Status, COUNT(*) FROM candidates GROUP BY 1")) or "none")
        print("Sources logged:", conn.execute("SELECT COUNT(*) FROM source_log").fetchone()[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
