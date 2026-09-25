#!/usr/bin/env python3
"""Coverage tracking and progress/STATE_CHECKLIST.md rendering (CLAUDE.md 11.4).

Cluster and state progress live in progress/coverage.json (committed: it holds
no contact data). Lead counts come from data/leads.db. The checklist is
regenerated between the GENERATED markers; text outside them is kept.

Usage:
  python3 scripts/progress.py mark Punjab Ludhiana --sources ratings,ec_cte,expos [--done] [--note "..."]
  python3 scripts/progress.py state Punjab --status Done [--note "..."]
  python3 scripts/progress.py render
  python3 scripts/progress.py summary

Source keys: ratings, ec_cte, expos, associations, regional_news, marketplaces, jobs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

CHECKLIST_PATH = C.PROGRESS_DIR / "STATE_CHECKLIST.md"
BEGIN, END = "<!-- BEGIN GENERATED: scripts/progress.py render -->", "<!-- END GENERATED -->"
SOURCE_KEYS = [k for k, _ in C.CHECKLIST_SOURCES]


def load_coverage(path: Path = C.COVERAGE_PATH) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"states": {}}


def save_coverage(cov: dict, path: Path = C.COVERAGE_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _entry_for(state: str, cluster: str | None = None) -> dict:
    exact = [e for e in C.state_entries() if e["state"].lower() == state.strip().lower()]
    if exact:
        return exact[0]
    entry, _ = C.resolve_state(state, cluster)
    if not entry:
        raise SystemExit(f"Unknown state '{state}'")
    return entry


def state_record(cov: dict, entry: dict) -> dict:
    rec = cov["states"].setdefault(entry["state"], {"status": "Not Started", "notes": "", "last_updated": None,
                                                    "clusters": {}})
    for cl in entry["clusters"]:
        rec["clusters"].setdefault(cl["name"], {**{k: False for k in SOURCE_KEYS}, "done": False, "notes": ""})
    return rec


def mark(cov: dict, state: str, cluster: str, sources: list[str], done: bool, note: str | None) -> str:
    entry = _entry_for(state, cluster)
    rec = state_record(cov, entry)
    names = {c.lower(): c for c in rec["clusters"]}
    cname = names.get(cluster.strip().lower()) or C.resolve_state(entry["state"], cluster)[1]
    if cname is None or cname not in rec["clusters"]:
        raise SystemExit(f"'{cluster}' is not a planned cluster of {entry['state']}: {', '.join(rec['clusters'])}")
    cl = rec["clusters"][cname]
    for s in sources:
        if s not in SOURCE_KEYS:
            raise SystemExit(f"Unknown source key '{s}'. Use: {', '.join(SOURCE_KEYS)}")
        cl[s] = True
    if done:
        cl["done"] = True
    if note:
        cl["notes"] = C.sanitize_text(note)
    if rec["status"] == "Not Started":
        rec["status"] = "In Progress"
    rec["last_updated"] = C.today_str()
    return f"{entry['state']} / {cname}"


def set_state(cov: dict, state: str, status: str, note: str | None) -> str:
    entry = _entry_for(state)
    rec = state_record(cov, entry)
    canon = {s.lower(): s for s in C.COVERAGE_STATUSES}.get(status.strip().lower())
    if not canon:
        raise SystemExit(f"Status must be one of {', '.join(C.COVERAGE_STATUSES)}")
    rec["status"] = canon
    if note:
        rec["notes"] = C.sanitize_text(note)
    rec["last_updated"] = C.today_str()
    return entry["state"]


def db_counts() -> dict:
    if not C.DB_PATH.exists():
        return {}
    import db
    return db.counts_by_state_entry(db.connect())


def coverage_rows(cov: dict, counts: dict) -> list[dict]:
    """One row per state entry, in wave order: feeds State_Coverage and the checklist."""
    rows = []
    for entry in C.state_entries():
        rec = state_record(cov, entry)
        n = counts.get(entry["state"], {})
        clusters = rec["clusters"]
        rows.append({
            "Wave": entry["wave"], "State": entry["state"], "Clusters_Planned": len(entry["clusters"]),
            "Clusters_Done": sum(1 for c in clusters.values() if c["done"]),
            "Sources_Checked": n.get("sources", 0), "Candidates_Screened": n.get("screened", 0),
            "Tier_A": n.get("A", 0), "Tier_B": n.get("B", 0), "Tier_C": n.get("C", 0),
            "Longterm": n.get("longterm", 0), "Rejected": n.get("rejected", 0),
            "Status": rec["status"], "Last_Updated": rec.get("last_updated"), "Notes": rec.get("notes") or "",
            "_clusters": clusters, "_entry": entry,
        })
    return rows


def render_checklist(rows: list[dict]) -> str:
    out, wave = [], None
    for r in rows:
        if r["Wave"] != wave:
            wave = r["Wave"]
            out.append(f"\n## Wave {wave}")
        out.append(f"### {r['State']} [{r['Status'].upper()}] screened: {r['Candidates_Screened']} | "
                   f"A: {r['Tier_A']} | B: {r['Tier_B']} | C: {r['Tier_C']} | longterm: {r['Longterm']} | "
                   f"rejected: {r['Rejected']}")
        if r["Notes"]:
            out.append(f"_Note: {r['Notes']}_")
        for cl in r["_entry"]["clusters"]:
            c = r["_clusters"][cl["name"]]
            boxes = " ".join(f"[{'x' if c[k] else ' '}] {label}" for k, label in C.CHECKLIST_SOURCES)
            line = f"- [{'x' if c['done'] else ' '}] {cl['name']}: {boxes}"
            if c.get("notes"):
                line += f" ({c['notes']})"
            out.append(line)
    return "\n".join(out).strip() + "\n"


def write_checklist(rows: list[dict], path: Path = CHECKLIST_PATH):
    body = render_checklist(rows)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        head, rest = existing.split(BEGIN, 1)
        tail = rest.split(END, 1)[1]
    else:
        head, tail = existing or "# State checklist\n\n", ""
    path.write_text(f"{head}{BEGIN}\n{body}{END}{tail}", encoding="utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mark")
    m.add_argument("state"); m.add_argument("cluster")
    m.add_argument("--sources", default=""); m.add_argument("--done", action="store_true"); m.add_argument("--note")
    s = sub.add_parser("state")
    s.add_argument("state"); s.add_argument("--status", required=True); s.add_argument("--note")
    sub.add_parser("render")
    sub.add_parser("summary")
    args = p.parse_args(argv)

    cov = load_coverage()
    if args.cmd == "mark":
        what = mark(cov, args.state, args.cluster, [x for x in args.sources.split(",") if x], args.done, args.note)
        save_coverage(cov)
        print(f"marked {what}")
    elif args.cmd == "state":
        print(f"{set_state(cov, args.state, args.status, args.note)} -> {args.status}")
        save_coverage(cov)
    rows = coverage_rows(cov, db_counts())
    if args.cmd in ("mark", "state", "render"):
        save_coverage(cov)
        write_checklist(rows)
        print(f"rendered {CHECKLIST_PATH.relative_to(C.ROOT)}")
    if args.cmd == "summary":
        for r in rows:
            if r["Status"] != "Not Started" or r["Candidates_Screened"]:
                print(f"W{r['Wave']} {r['State']:<36} {r['Status']:<12} clusters {r['Clusters_Done']}/"
                      f"{r['Clusters_Planned']} screened {r['Candidates_Screened']} A{r['Tier_A']} B{r['Tier_B']} "
                      f"C{r['Tier_C']} LT{r['Longterm']} R{r['Rejected']}")
        print(f"{sum(1 for r in rows if r['Status'] == 'Not Started')} of {len(rows)} state entries not started")
    return 0


if __name__ == "__main__":
    sys.exit(main())
