"""Tests for score.py, db.py and dedupe.py. All companies here are fictional.

Run from the repo root: python3 -m pytest -q tests
"""
import copy
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import common as C  # noqa: E402
import db  # noqa: E402
import dedupe  # noqa: E402
import score  # noqa: E402

RESEARCH = date(2026, 9, 25)

BASE = {
    "Company_Name": "Fictional Precision Tools Pvt Ltd",
    "Industry": "Hand Tools and Hardware",
    "Key_Products": "Spanners, pliers",
    "State": "Punjab",
    "City_Cluster": "Ludhiana",
    "Plant_Locations": "Focal Point, Ludhiana",
    "Website_URL": "https://www.fictional-tools.example.com",
    "Year_Established": 1988,
    "Legal_Entity": "Pvt Ltd",
    "GSTIN": "03AAPFU0939F1Z5",   # fictional, checksum-valid
    "Revenue_Estimate_Cr": 142,
    "Revenue_FY": "FY2025",
    "Revenue_Source": "Rating rationale 12-Jan-2026 https://ratings.example.org/r/1.pdf",
    "Size_Confidence": "High",
    "Employees": "250",
    "Exporter_Markets": "UAE, Kenya",
    "Website_Decay_Score": 6,
    "Decay_Evidence": "© 2016; ISO 9001:2008; gmail contact; no viewport",
    "Corporate_Profile_Status": "None downloadable",
    "LinkedIn_Presence": "Inactive (last post 2023)",
    "Google_Rating": "4.2 (31 reviews)",
    "Score_Inputs": {"proof_points": 2, "scale": 1, "reach": 1, "founder_visible": 0},
    "Trigger_Type": "Rating capex",
    "Trigger_Detail": "Debt-funded capex for a new forging line",
    "Trigger_Date": "12-Jan-2026",
    "Trigger_Source_URL": "https://ratings.example.org/r/1.pdf",
    "Owner_Name": "A. Fictional",
    "Owner_Designation": "Managing Director",
    "Owner_Mobile": "090000 00001",
    "Owner_Mobile_Source_URL": "https://www.fictional-tools.example.com/contact",
    "Company_Email": "fictionaltools@gmail.com",
    "G1_Manufacturer": "Y", "G3_Not_Popular": "Y", "G5_Right_Segment": "Y",
    "Pitch_Hook": "Congratulations on the new forging line, sir. Buyers who Google you still find a 2016 website.",
    "Date_Researched": "25-Sep-2026",
}


def lead(**overrides):
    d = copy.deepcopy(BASE)
    d.update(overrides)
    return d


def ev(d):
    return score.evaluate(d, RESEARCH)


def test_base_lead_scores_match_hand_calculation():
    r = ev(lead())
    assert r.errors == []
    row = r.row
    assert (row["Strength_Score"], row["Visibility_Score"], row["Gap_Score"]) == (7, 4, 3)
    assert row["Trigger_Score"] == 5 and row["Contact_Score"] == 3
    assert row["Priority_Score"] == 3 * 2 + 5 * 3 + 3 * 2 + 3
    assert row["Tier"] == "B"
    assert row["Wave"] == 1
    assert row["Owner_Mobile"] == "+91 90000 00001"
    assert row["Email_Type"] == "Gmail"
    assert row["Recommended_Offer"] == "ESSENTIALS + RETAINER"
    assert row["Broadcast_Segments"] == "SEG-ENGG, SEG-EXPORT"
    assert row["G2_Size"] == "Y" and row["G4_Weak_Representation"] == "Y"


def test_high_decay_makes_tier_a():
    r = ev(lead(Website_Decay_Score=9))
    assert r.errors == []
    assert r.row["Gap_Score"] == 5 and r.row["Tier"] == "A"


def test_mobile_needs_source_url():
    r = ev(lead(Owner_Mobile_Source_URL=None))
    assert any("no URL, no number" in e for e in r.errors)


def test_landline_rejected_as_mobile():
    r = ev(lead(Owner_Mobile="0161 2345678"))
    assert any("not a valid Indian mobile" in e for e in r.errors)


def test_linkedin_cannot_source_a_mobile():
    r = ev(lead(Owner_Mobile_Source_URL="https://www.linkedin.com/in/someone"))
    assert any("LinkedIn" in e for e in r.errors)


def test_em_dash_removed_and_long_hook_rejected():
    r = ev(lead(Pitch_Hook="Congratulations sir — new line"))
    assert "—" not in r.row["Pitch_Hook"] and r.errors == []
    r = ev(lead(Pitch_Hook=" ".join(["word"] * 26)))
    assert any("max 25" in e for e in r.errors)


def test_modern_site_fails_g4():
    r = ev(lead(Website_Decay_Score=2))
    assert any("G4_Weak_Representation" in e and "R6" in e for e in r.errors)


def test_revenue_out_of_band_fails_g2():
    r = ev(lead(Revenue_Estimate_Cr=620))
    assert any("G2_Size" in e for e in r.errors)


def test_trigger_window():
    assert any("18-month" in e for e in ev(lead(Trigger_Date="01-Feb-2025")).errors)
    fair = lead(Trigger_Type="Trade fair", Trigger_Date="Jan-2025", Trigger_Detail="Exhibited at IMTEX 2025")
    r = ev(fair)
    assert r.errors == [] and "SEG-EXPO" in r.row["Broadcast_Segments"]
    assert r.row["Recommended_Offer"] == "EXPO KIT"
    assert any("too old" in e for e in ev(dict(fair, Trigger_Date="Jan-2024")).errors)


def test_trigger_score_follows_type():
    r = ev(lead(Trigger_Type="Hiring", Trigger_Score=5, Trigger_Date="01-Aug-2026"))
    assert r.row["Trigger_Score"] == 2 and any("replaced" in w for w in r.warnings)


def test_low_confidence_needs_manual_check_and_is_tier_c():
    assert any("Manual_Check" in e for e in ev(lead(Size_Confidence="Low", Website_Decay_Score=9)).errors)
    r = ev(lead(Size_Confidence="Low", Website_Decay_Score=9, Manual_Check="Verify turnover (GST slab)"))
    assert r.errors == [] and r.row["Tier"] == "C" and r.row["G2_Size"] == "Y"


def test_existing_client_blocked():
    r = ev(lead(Company_Name="Kasturi India Pvt Ltd"))
    assert any("R10" in e for e in r.errors)


def test_generic_owner_email_blocked():
    r = ev(lead(Owner_Email="info@fictional-tools.example.com"))
    assert any("generic mailbox" in e for e in r.errors)


def test_next_gen_labelled_probable():
    r = ev(lead(Next_Gen_Name="B. Fictional", Next_Gen_LinkedIn_URL="https://in.linkedin.com/in/bfictional"))
    assert r.row["Next_Gen_Name"] == "B. Fictional (probable)"
    assert "SEG-NEXTGEN" in r.row["Broadcast_Segments"]


def test_no_website_scores_ten_and_tags_noweb():
    r = ev(lead(Website_URL="", Website_Decay_Score=None, Decay_Evidence=None))
    assert r.errors == []
    assert r.row["Website_Decay_Score"] == 10 and "SEG-NOWEB" in r.row["Broadcast_Segments"]


def test_marketplace_url_is_not_a_website():
    r = ev(lead(Website_URL="https://www.indiamart.com/fictional-tools/"))
    assert any("marketplace" in e for e in r.errors)


def test_capmkt_offer_and_bad_gstin():
    r = ev(lead(Broadcast_Segments="CAPMKT"))
    assert r.row["Recommended_Offer"] == "PREMIUM + CAPITAL MARKETS"
    assert any("checksum" in e for e in ev(lead(GSTIN="03AAPFU0939F1ZV")).errors)


def test_longterm_gifting_route():
    r = ev(lead(Pipeline="LONGTERM", Industry="Building Materials", Broadcast_Segments="SEG-GIFTING",
                Reason_For_Longterm="Road EPC contractor: Diwali gifting prospect"))
    assert r.errors == [] and r.row["Tier"] is None
    assert any("never go into Active" in e for e in ev(lead(Broadcast_Segments="SEG-GIFTING")).errors)


def test_up_wave_split():
    assert ev(lead(State="Uttar Pradesh", City_Cluster="Meerut", GSTIN=None)).row["Wave"] == 1
    assert ev(lead(State="Uttar Pradesh", City_Cluster="Kanpur", GSTIN=None)).row["Wave"] == 2


# --------------------------------------------------------------------------- DB


@pytest.fixture()
def conn(tmp_path):
    return db.connect(tmp_path / "t.db")


def test_db_insert_dedupe_and_ids(conn):
    cid, msg = db.add_candidate(conn, "Fictional Precision Tools", "Punjab", "Ludhiana",
                                "fictional-tools.example.com", "Rating rationale", "https://ratings.example.org/r/1.pdf")
    assert cid and msg == "added"
    # Same company again (different legal suffix, www prefix) is caught.
    again, msg = db.add_candidate(conn, "Fictional Precision Tools Private Limited", "Punjab", "Ludhiana",
                                  "https://www.fictional-tools.example.com/")
    assert again is None and "known" in msg

    r = ev(lead())
    lead_id, created = db.upsert_lead(conn, r.row)
    assert (lead_id, created) == ("PB-001", True)
    cand = conn.execute("SELECT Status, Outcome_Ref FROM candidates WHERE id = ?", (cid,)).fetchone()
    assert tuple(cand) == ("ACTIVE", "PB-001")

    # A second record for the same GSTIN PAN (other state registration) is a duplicate.
    dup = ev(lead(Company_Name="Fictional Tools Exports", Website_URL="https://other.example.net",
                  GSTIN="27AAPFU0939F1ZV", City_Cluster="Ludhiana"))
    with pytest.raises(ValueError, match="Duplicate"):
        db.upsert_lead(conn, dup.row)

    # Updating via Lead_ID keeps the tracker columns the team typed.
    conn.execute("UPDATE leads SET Status = 'Contacted', FU_Stage = '1' WHERE Lead_ID = 'PB-001'")
    upd = ev(lead(Lead_ID="PB-001", Website_Decay_Score=9))
    assert db.upsert_lead(conn, upd.row) == ("PB-001", False)
    row = conn.execute("SELECT Tier, Status, FU_Stage FROM leads WHERE Lead_ID = 'PB-001'").fetchone()
    assert tuple(row) == ("A", "Contacted", "1")

    other = ev(lead(Company_Name="Another Fictional Forge", Website_URL="https://forge.example.net", GSTIN=None))
    assert db.upsert_lead(conn, other.row)[0] == "PB-002"
    assert dedupe.scan(conn) == []


def test_reject_flow(conn):
    rid, msg = db.add_reject(conn, {"Company_Name": "Big Listed Fictional Ltd", "State": "Punjab",
                                    "City": "Ludhiana", "Reject_Code": "r5",
                                    "Reject_Evidence": "NSE main board — listed", "Source_URL": "https://x.example"})
    assert rid and msg == "added"
    stored = conn.execute("SELECT Reject_Code, Reject_Evidence FROM rejected").fetchone()
    assert stored["Reject_Code"] == "R5" and "—" not in stored["Reject_Evidence"]
    assert db.add_reject(conn, {"Company_Name": "Big Listed Fictional Limited", "State": "Punjab",
                                "City": "Ludhiana", "Reject_Code": "R5", "Reject_Evidence": "listed"})[0] is None
    blocked = ev(lead(Company_Name="Big Listed Fictional Ltd", Website_URL="https://big.example.org", GSTIN=None))
    with pytest.raises(ValueError, match="unreject"):
        db.upsert_lead(conn, blocked.row)
    counts = db.counts_by_state_entry(conn)
    assert counts["Punjab"]["rejected"] == 1 and counts["Punjab"]["screened"] == 1


def test_similar_client_name_is_flagged_not_blocked():
    r = ev(lead(Company_Name="Kasturi India Textiles Pvt Ltd"))
    assert r.errors == [] and any("close to existing client" in w for w in r.warnings)


def test_unknown_lead_id_is_refused(conn):
    with pytest.raises(ValueError, match="does not exist"):
        db.upsert_lead(conn, ev(lead(Lead_ID="PB-050")).row)
