#!/usr/bin/env python3
"""Scoring and validation for one lead (CLAUDE.md Sections 3, 8, 10, 13).

The researcher writes the facts; this script derives everything that follows
from a rule, so scores stay consistent across sessions:
  Wave, Strength/Visibility/Gap, Trigger_Score (from Trigger_Type), Contact_Score,
  Priority_Score, Tier, Recommended_Offer (unless overridden), Email_Type, G2, G4,
  Trigger_Found, Owner_Contact_Found, automatic Broadcast_Segments.

It also refuses records that break the non-negotiables: a mobile without a
source URL, a malformed mobile, a failed gate in Active_Pipeline, a trigger
outside the 18-month window, an over-long pitch hook, and so on.

Input JSON: the Active_Pipeline column names, plus
  "Pipeline": "ACTIVE" (default) or "LONGTERM", "Reason_For_Longterm" for LONGTERM,
  "Score_Inputs": {"proof_points": 0-3, "scale": 0-2, "reach": 0-1,
                   "founder_visible": 0-1, "pvt_to_public": false,
                   "next_gen_confirmed": false}

Usage:
  python3 scripts/score.py data/work/lead.json          # evaluate, print, write nothing
  python3 scripts/score.py --recompute-all [--write]  # re-score every lead in the DB
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

GATE_REJECT_HINT = {
    "G1_Manufacturer": "R7 not a manufacturer",
    "G2_Size": "R1 above ₹500 Cr, R2 below ₹50 Cr, or R12 if size cannot be established",
    "G3_Not_Popular": "R3 popular, R4 group/MNC/PE-VC, or R5 main-board listed",
    "G4_Weak_Representation": "R6 modern website",
    "G5_Right_Segment": "R8 wrong segment (or Longterm_Broadcast for EPC/road/government contractors)",
}
WEBSITE_POINTS = {0: 4, 1: 4, 2: 4, 3: 3, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0}
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


@dataclass
class Result:
    row: dict
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


def _num(value):
    if value is None or C.is_blank(value):
        return None
    if isinstance(value, (int, float)):
        return value
    s = re.sub(r"[₹,\s]|cr\.?$", "", str(value), flags=re.I)
    try:
        return float(s)
    except ValueError:
        return None


def _int_in(value, lo, hi):
    n = _num(value)
    if n is None or int(n) != n or not lo <= n <= hi:
        return None
    return int(n)


def _yn(value) -> str | None:
    if value is True:
        return "Y"
    if value is False:
        return "N"
    s = str(value or "").strip().upper()
    return {"Y": "Y", "YES": "Y", "N": "N", "NO": "N"}.get(s)


def _leading_word(value, allowed: dict, blank_default=None):
    if C.is_blank(value):
        return blank_default
    first = re.split(r"[\s:(,;.-]+", str(value).strip(), maxsplit=1)[0].lower()
    return allowed.get(first)


def parse_google_rating(value) -> tuple[float | None, int | None]:
    if C.is_blank(value):
        return None, None
    s = str(value)
    rating = next((float(x) for x in re.findall(r"\d(?:\.\d+)?", s) if float(x) <= 5), None)
    m = re.search(r"(\d[\d,]*)\s*(?:google\s*)?reviews?", s, re.I)
    return rating, (int(m.group(1).replace(",", "")) if m else None)


def split_segments(value) -> list[str]:
    if C.is_blank(value):
        return []
    return [s.strip().upper() for s in re.split(r"[,;]", str(value)) if s.strip()]


def email_type(company_email, owner_email, website_url) -> str:
    email = company_email if not C.is_blank(company_email) else owner_email
    dom = C.email_domain(email)
    if not dom:
        return "Not found"
    if dom in C.FREE_EMAIL_PROVIDERS:
        return C.FREE_EMAIL_PROVIDERS[dom]
    site = C.domain_key(website_url)
    return "Own domain" if site and C.registrable_domain(dom) == site else "Other domain"


def recommended_offer(segments: set, revenue, pvt_to_public: bool) -> str:
    if "CAPMKT" in segments or pvt_to_public:
        return "PREMIUM + CAPITAL MARKETS"
    if "SEG-EXPO" in segments:
        return "EXPO KIT"
    if revenue is not None and revenue >= 150:
        return "PREMIUM + CAPITAL MARKETS"
    return "ESSENTIALS + RETAINER"


def evaluate(lead: dict, research_date: date | None = None) -> Result:
    row = dict(lead)
    res = Result(row=row)
    warn, err = res.warnings.append, res.errors.append

    # --- text hygiene: no em dashes anywhere (Section 13) -----------------------
    for k, v in list(row.items()):
        if isinstance(v, str):
            if "\u2014" in v or " \u2013 " in v:
                warn(f"{k}: em dash replaced")
            row[k] = C.sanitize_text(v)

    pipeline = str(row.get("Pipeline") or "ACTIVE").upper()
    if pipeline not in {"ACTIVE", "LONGTERM"}:
        err(f"Pipeline must be ACTIVE or LONGTERM, got {pipeline}")
        return res
    row["Pipeline"] = pipeline
    active = pipeline == "ACTIVE"

    researched, prec = C.parse_date(row.get("Date_Researched") or C.today_str())
    if prec != "day":
        err(f"Date_Researched must be DD-MMM-YYYY, got {row.get('Date_Researched')}")
        researched = date.today()
    research_date = research_date or researched
    row["Date_Researched"] = C.fmt_date(researched)

    # --- identity -----------------------------------------------------------------
    for req in ("Company_Name", "State", "City_Cluster", "Industry"):
        if C.is_blank(row.get(req)):
            err(f"{req} is required")
    if res.errors:
        return res
    excl = C.match_exclusion(row["Company_Name"])
    if excl and excl[1] == "exact":
        err(f"matches existing client or exclusion '{excl[0]}': reject R10")
    elif excl:
        warn(f"name is close to existing client '{excl[0]}': confirm it is not a group company before outreach")

    ind = {i.lower(): i for i in C.INDUSTRIES}.get(str(row["Industry"]).strip().lower())
    if not ind:
        err(f"Industry '{row['Industry']}' is not in the fixed list")
    row["Industry"] = ind or row["Industry"]

    entry, cluster = C.resolve_state(row["State"], row["City_Cluster"])
    if not entry:
        err(f"State '{row['State']}' not found in config/states.json")
        return res
    row["State"] = re.sub(r"\s*\(.*\)$", "", entry["state"])
    row["State_Entry"], row["Cluster"], row["Wave"] = entry["state"], cluster, entry["wave"]
    if cluster is None:
        warn(f"City '{row['City_Cluster']}' is outside the planned clusters for {entry['state']} (allowed)")

    website = row.get("Website_URL")
    no_website = C.is_blank(website)
    if not no_website and C.is_shared_platform(website):
        err("Website_URL is a marketplace or social page, not the company's own site: "
            "leave Website_URL blank (no website, SEG-NOWEB) and mention the page in Research_Notes")
    if no_website:
        row["Website_URL"] = "Not found"

    year = _int_in(row.get("Year_Established"), 1800, research_date.year)
    if not C.is_blank(row.get("Year_Established")) and year is None:
        err(f"Year_Established '{row.get('Year_Established')}' is not a valid year")
    row["Year_Established"] = year if year is not None else row.get("Year_Established")

    gstin = C.clean_gstin(row.get("GSTIN"))
    if gstin:
        if not C.GSTIN_RE.match(gstin) or not C.gstin_checksum_ok(gstin):
            err(f"GSTIN {gstin} fails the format or checksum test (typo?)")
        elif C.GST_STATE_TO_CODE.get(gstin[:2]) != entry["code"]:
            warn(f"GSTIN {gstin} is registered in another state ({gstin[:2]}); fine if it is a branch GSTIN")
        row["GSTIN"] = gstin
    cin = C.clean_cin(row.get("CIN"))
    if cin:
        if not (C.CIN_RE.match(cin) or C.LLPIN_RE.match(cin)):
            err(f"CIN/LLPIN {cin} has an invalid format")
        elif cin.startswith("L"):
            warn("CIN starts with L (listed company): confirm SME exchange (keep, tag CAPMKT) "
                 "vs main board (reject R5)")
        row["CIN"] = cin

    # --- size -----------------------------------------------------------------------
    revenue = _num(row.get("Revenue_Estimate_Cr"))
    conf = {c.lower(): c for c in C.SIZE_CONFIDENCE}.get(str(row.get("Size_Confidence") or "").strip().lower())
    manual = "" if C.is_blank(row.get("Manual_Check")) else str(row.get("Manual_Check")).strip()
    row["Manual_Check"] = manual or None
    if active:
        if revenue is None:
            err("Revenue_Estimate_Cr must be a number in ₹ Cr")
        if conf is None:
            err("Size_Confidence must be High, Medium or Low")
        if C.is_blank(row.get("Revenue_FY")):
            err("Revenue_FY is required (e.g. FY2025)")
        if not C.first_url(row.get("Revenue_Source")):
            err("Revenue_Source must include the source URL (Section 13)")
        if conf == "Low" and not manual:
            err("Size_Confidence Low needs a Manual_Check note saying what to verify")
    row["Revenue_Estimate_Cr"] = revenue if revenue is not None else row.get("Revenue_Estimate_Cr")
    row["Size_Confidence"] = conf or row.get("Size_Confidence")

    # --- representation -----------------------------------------------------------
    decay = _int_in(row.get("Website_Decay_Score"), 0, 10)
    if no_website:
        if decay not in (None, 10):
            warn("No website, so Website_Decay_Score is set to 10")
        decay = 10
        if C.is_blank(row.get("Decay_Evidence")):
            row["Decay_Evidence"] = "No website found"
    elif active and decay is None:
        err("Website_Decay_Score (0 to 10 from scripts/audit_website.py) is required")
    if active and not no_website and C.is_blank(row.get("Decay_Evidence")):
        err("Decay_Evidence is required")
    row["Website_Decay_Score"] = decay

    profile_pts = _leading_word(row.get("Corporate_Profile_Status"), {"current": 2, "old": 1, "none": 0})
    if profile_pts is None:
        if active:
            warn("Corporate_Profile_Status should start with Current, Old or None: scored as None")
        profile_pts = 0
        if C.is_blank(row.get("Corporate_Profile_Status")):
            row["Corporate_Profile_Status"] = "None found"
    linkedin_pts = _leading_word(row.get("LinkedIn_Presence"), {"active": 2, "inactive": 1, "none": 0})
    if linkedin_pts is None:
        if active:
            warn("LinkedIn_Presence should start with Active, Inactive or None: scored as None")
        linkedin_pts = 0
        if C.is_blank(row.get("LinkedIn_Presence")):
            row["LinkedIn_Presence"] = "None found"
    rating, reviews = parse_google_rating(row.get("Google_Rating"))
    google_pt = 1 if rating is not None and rating >= 4.0 and (reviews or 0) >= 20 else 0

    inputs = dict(row.get("Score_Inputs") or {})
    comp = {}
    for key, hi in (("proof_points", 3), ("scale", 2), ("reach", 1), ("founder_visible", 1)):
        v = _int_in(inputs.get(key), 0, hi)
        if v is None and active:
            err(f"Score_Inputs.{key} must be an integer 0 to {hi}")
        comp[key] = v or 0
        inputs[key] = v
    row["Score_Inputs"] = inputs

    # --- trigger -----------------------------------------------------------------
    ttype_raw = row.get("Trigger_Type")
    ttype = "None" if C.is_blank(ttype_raw) else {t.lower(): t for t in C.TRIGGER_TYPES}.get(str(ttype_raw).strip().lower())
    if ttype is None:
        err(f"Trigger_Type '{ttype_raw}' is not in the list: {', '.join(C.TRIGGER_TYPES)}")
        ttype = "None"
    tscore = C.TRIGGER_TYPES[ttype][0]
    given = _num(row.get("Trigger_Score"))
    if given is not None and int(given) != tscore:
        warn(f"Trigger_Score {int(given)} replaced by {tscore} (set by Trigger_Type '{ttype}')")
    row["Trigger_Type"], row["Trigger_Score"] = ttype, tscore
    if tscore > 0:
        if C.is_blank(row.get("Trigger_Detail")):
            err("Trigger_Detail is required when a trigger is found")
        if not C.first_url(row.get("Trigger_Source_URL")):
            err("Trigger_Source_URL is required when a trigger is found (Section 13)")
    if ttype not in C.UNDATED_TRIGGERS:
        tdate, tprec = C.parse_date(row.get("Trigger_Date"))
        if tdate is None:
            err("Trigger_Date must be DD-MMM-YYYY (or MMM-YYYY) for a dated trigger")
        else:
            if tprec != "day":
                warn(f"Trigger_Date '{row.get('Trigger_Date')}' is approximate ({tprec} precision)")
            if ttype == "Trade fair":
                if tdate.year < research_date.year - 1:
                    err(f"Trade fair edition {tdate.year} is too old: only {research_date.year - 1} or "
                        f"{research_date.year} editions count")
            elif C.months_between(tdate, research_date) > 18:
                err(f"Trigger dated {row.get('Trigger_Date')} is outside the 18-month window")
            if tdate > research_date and ttype != "Trade fair":
                warn("Trigger_Date is in the future: confirm it is an approval or announcement date")
    elif C.is_blank(row.get("Trigger_Date")):
        row["Trigger_Date"] = None

    # --- people and contact -------------------------------------------------------
    mobile_raw = row.get("Owner_Mobile")
    mobile = C.normalize_mobile(mobile_raw)
    if not C.is_blank(mobile_raw) and mobile is None:
        err(f"Owner_Mobile '{mobile_raw}' is not a valid Indian mobile (landlines go in Company_Phone)")
    src = row.get("Owner_Mobile_Source_URL")
    if mobile:
        if not C.first_url(src):
            err("Owner_Mobile has no Owner_Mobile_Source_URL: no URL, no number (Section 8)")
        elif "linkedin.com" in str(src).lower():
            err("Owner_Mobile_Source_URL cannot be LinkedIn (contact details there sit behind a login)")
    row["Owner_Mobile"] = mobile
    for col in ("Owner_Email", "Company_Email"):
        v = row.get(col)
        if not C.is_blank(v) and not EMAIL_RE.match(str(v).strip()):
            err(f"{col} '{v}' is not a valid email address")
    owner_email_ok = not C.is_blank(row.get("Owner_Email"))
    if owner_email_ok and C.email_mailbox(row["Owner_Email"]) in C.GENERIC_MAILBOXES:
        err(f"Owner_Email '{row['Owner_Email']}' is a generic mailbox: move it to Company_Email")
        owner_email_ok = False
    ng = row.get("Next_Gen_Name")
    if not C.is_blank(ng) and "(probable)" not in str(ng) and not inputs.get("next_gen_confirmed"):
        row["Next_Gen_Name"] = f"{str(ng).strip()} (probable)"
        warn("Next_Gen_Name labelled '(probable)' (set Score_Inputs.next_gen_confirmed if the company states it)")
    li = row.get("Next_Gen_LinkedIn_URL")
    if not C.is_blank(li) and "linkedin.com/" not in str(li).lower():
        err("Next_Gen_LinkedIn_URL must be a linkedin.com URL taken from search results")
    if mobile and C.first_url(src) and "linkedin.com" not in str(src).lower():
        contact = 3
    elif owner_email_ok or not C.is_blank(li):
        contact = 2
    elif not C.is_blank(row.get("Company_Phone")) or not C.is_blank(row.get("Company_Email")):
        contact = 1
    else:
        contact = 0
    row["Contact_Score"] = contact
    row["Email_Type"] = email_type(row.get("Company_Email"), row.get("Owner_Email"), row.get("Website_URL"))
    row["Owner_Contact_Found"] = "Y" if (mobile or owner_email_ok) else "N"
    row["Trigger_Found"] = "Y" if tscore > 0 else "N"

    # --- segments -----------------------------------------------------------------
    segs = split_segments(row.get("Broadcast_Segments"))
    for s in segs:
        if s not in C.SEGMENTS and not C.SOURCE_TAG_RE.match(s):
            err(f"Unknown Broadcast_Segments tag '{s}'")
    auto = []
    if ind and C.INDUSTRY_SEGMENT.get(ind):
        auto.append(C.INDUSTRY_SEGMENT[ind])
    if no_website:
        auto.append("SEG-NOWEB")
    if not C.is_blank(ng):
        auto.append("SEG-NEXTGEN")
    if ttype == "Trade fair":
        auto.append("SEG-EXPO")
    exp = row.get("Exporter_Markets")
    if not C.is_blank(exp) and str(exp).strip().lower() not in {"none", "domestic", "domestic only", "no"}:
        auto.append("SEG-EXPORT")
    for s in auto:
        if s not in segs:
            segs.append(s)
    if active and "SEG-GIFTING" in segs:
        err("SEG-GIFTING leads never go into Active_Pipeline: set Pipeline to LONGTERM")
    row["Broadcast_Segments"] = ", ".join(segs)

    # --- LONGTERM stops here: no scores, no gates -----------------------------------
    if not active:
        if C.is_blank(row.get("Reason_For_Longterm")):
            err("Reason_For_Longterm is required for LONGTERM leads")
        if "SEG-GIFTING" not in segs:
            warn("LONGTERM lead without SEG-GIFTING: check the routing reason")
        for col in ("Tier", "Priority_Score", "Strength_Score", "Visibility_Score", "Gap_Score"):
            row[col] = None
        return res

    # --- gates --------------------------------------------------------------------
    for g in ("G1_Manufacturer", "G3_Not_Popular", "G5_Right_Segment"):
        v = _yn(row.get(g))
        if v is None:
            err(f"{g} must be Y or N")
        row[g] = v
    in_range = revenue is not None and 50 <= revenue <= 500
    row["G2_Size"] = "Y" if in_range and (conf in ("High", "Medium") or (conf == "Low" and manual)) else "N"
    row["G4_Weak_Representation"] = "Y" if (decay is not None and decay >= 3) else "N"
    for g, hint in GATE_REJECT_HINT.items():
        if row.get(g) == "N":
            err(f"{g} = N: an Active lead must pass all five gates; reject instead ({hint})")

    # --- scores ---------------------------------------------------------------------
    rev_pts = 0 if revenue is None or revenue < 50 else 1 if revenue < 100 else 2 if revenue < 250 else 3
    longevity = 1 if year is not None and research_date.year - year >= 15 else 0
    strength = rev_pts + comp["proof_points"] + comp["scale"] + longevity + comp["reach"]
    visibility = (WEBSITE_POINTS.get(decay, 0) + profile_pts + linkedin_pts + google_pt
                  + comp["founder_visible"])
    gap = strength - visibility
    priority = gap * 2 + tscore * 3 + contact * 2 + C.wave_bonus(entry["wave"])
    if conf == "Low":
        tier = "C"
    elif gap >= 5 and tscore >= 3 and contact >= 2:
        tier = "A"
    elif gap >= 3 and (tscore >= 2 or contact >= 2):
        tier = "B"
    else:
        tier = "C"
    row.update({"Strength_Score": strength, "Visibility_Score": visibility, "Gap_Score": gap,
                "Priority_Score": priority, "Tier": tier})
    inputs["_derived"] = {"revenue_pts": rev_pts, "longevity": longevity,
                          "website_pts": WEBSITE_POINTS.get(decay, 0), "profile_pts": profile_pts,
                          "linkedin_pts": linkedin_pts, "google_pt": google_pt}

    # --- offer and hook -------------------------------------------------------------
    rule_offer = recommended_offer(set(segs), revenue,
                                   bool(inputs.get("pvt_to_public")) or ttype == "Pvt to Public or SME IPO")
    given_offer = row.get("Recommended_Offer")
    if C.is_blank(given_offer):
        row["Recommended_Offer"] = rule_offer
    else:
        canon = {o.lower(): o for o in C.OFFERS}.get(str(given_offer).strip().lower())
        if not canon:
            err(f"Recommended_Offer must be one of {', '.join(C.OFFERS)}")
        elif canon != rule_offer:
            warn(f"Recommended_Offer override '{canon}' (rule suggests '{rule_offer}')")
        row["Recommended_Offer"] = canon or given_offer
    hook = row.get("Pitch_Hook")
    if C.is_blank(hook):
        err("Pitch_Hook is required for Active leads")
    else:
        n = C.word_count(str(hook))
        if n > 25:
            err(f"Pitch_Hook has {n} words (max 25)")
        if "!" in str(hook):
            warn("Pitch_Hook uses '!': keep the register humble")
        if tscore == 0:
            warn("Pitch_Hook should pair one verified trigger with one gap, but no trigger was found")

    # --- tracker sanity (team-owned, validated only if present) ---------------------
    if not C.is_blank(row.get("Status")) and row["Status"] not in C.STATUS_VALUES:
        err(f"Status must be one of {', '.join(C.STATUS_VALUES)}")
    if not C.is_blank(row.get("FU_Stage")) and str(row["FU_Stage"]) not in C.FU_STAGES:
        err("FU_Stage must be 0, 1, 2 or 3")
    return res


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _row_to_input(r: dict) -> dict:
    lead = {k: r[k] for k in r.keys() if k in C.ACTIVE_COLUMNS or k in ("Pipeline", "Reason_For_Longterm")}
    lead["Score_Inputs"] = {k: v for k, v in json.loads(r.get("Score_Inputs") or "{}").items() if k != "_derived"}
    return lead


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?")
    p.add_argument("--recompute-all", action="store_true")
    p.add_argument("--write", action="store_true")
    p.add_argument("--db", default=str(C.DB_PATH))
    args = p.parse_args(argv)

    if args.recompute_all:
        import db
        conn = db.connect(args.db)
        rows = [dict(r) for r in conn.execute("SELECT * FROM leads")]
        changed = bad = 0
        for r in rows:
            research = C.parse_date(r.get("Date_Researched"))[0]
            res = evaluate(_row_to_input(r), research)
            if res.errors:
                bad += 1
                print(f"{r['Lead_ID']} ERRORS: {'; '.join(res.errors)}")
                continue
            diffs = {c: (r.get(c), res.row.get(c)) for c in
                     ("Tier", "Priority_Score", "Strength_Score", "Visibility_Score", "Gap_Score",
                      "Trigger_Score", "Contact_Score", "Recommended_Offer", "Broadcast_Segments")
                     if r.get(c) != res.row.get(c)}
            if diffs:
                changed += 1
                print(f"{r['Lead_ID']}: " + "; ".join(f"{k} {a} -> {b}" for k, (a, b) in diffs.items()))
                if args.write:
                    res.row["Lead_ID"] = r["Lead_ID"]
                    db.upsert_lead(conn, res.row)
        print(f"{len(rows)} leads, {changed} changed, {bad} with errors" + ("" if args.write else " (dry run)"))
        return 1 if bad else 0

    if not args.file:
        p.error("give a lead JSON file or --recompute-all")
    with open(args.file, encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else [data]
    failed = 0
    for item in items:
        res = evaluate(item)
        r = res.row
        print(f"== {r.get('Company_Name')} ({r.get('Pipeline')})")
        if r.get("Pipeline") == "ACTIVE" and not res.errors:
            print(f"   Tier {r['Tier']} | Priority {r['Priority_Score']} | Strength {r['Strength_Score']} "
                  f"| Visibility {r['Visibility_Score']} | Gap {r['Gap_Score']} | Trigger {r['Trigger_Score']} "
                  f"| Contact {r['Contact_Score']} | Wave {r['Wave']}")
            print(f"   Offer: {r['Recommended_Offer']} | Segments: {r['Broadcast_Segments']}")
        for w in res.warnings:
            print(f"   warn  {w}")
        for e in res.errors:
            print(f"   ERROR {e}")
        failed += bool(res.errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
