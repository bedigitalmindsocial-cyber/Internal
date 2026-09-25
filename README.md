# Giraffe Industrial Marketing: India Manufacturer Lead Engine

The standing brief is [CLAUDE.md](CLAUDE.md). Progress lives in
[progress/STATE_CHECKLIST.md](progress/STATE_CHECKLIST.md) and [progress/RUN_LOG.md](progress/RUN_LOG.md).

## Setup

```bash
pip install -r requirements.txt
python3 scripts/db.py init
python3 -m pytest -q tests        # offline tests on fictional fixtures
```

Needs normal internet access (company websites, rating agencies, MCA aggregators,
archive.org). Optional: `PSI_API_KEY` (free Google Cloud key) for PageSpeed, decay point 7.

## Per-lead workflow (CLAUDE.md Section 12)

| Step | Command |
|---|---|
| Log a discovered candidate | `python3 scripts/db.py add-candidate --name "..." --state Punjab --city Ludhiana --source-type "Rating rationale" --source-url URL [--url SITE]` |
| Dedupe check | `python3 scripts/dedupe.py check --name "..." --city Ludhiana [--url] [--gstin] [--cin]` |
| Website decay audit | `python3 scripts/audit_website.py https://site` (or `--no-website`) |
| Recency check (optional, R6) | `python3 scripts/wayback_check.py site.com --decay N` |
| Log each source used | `python3 scripts/db.py log-source --ref "..." --type "Rating rationale" --url URL --what "..." --state Punjab --city Ludhiana` |
| Score and save a lead | write `data/work/<name>.json` (template below), then `python3 scripts/score.py FILE` and `python3 scripts/db.py add-lead FILE` |
| Reject | `python3 scripts/db.py add-reject FILE` with `{"Company_Name", "State", "City", "Website_URL", "Reject_Code", "Reject_Evidence", "Source_URL"}` |
| Tick a cluster | `python3 scripts/progress.py mark Punjab Ludhiana --sources ratings,ec_cte --done` |
| Export workbook + CSV | `python3 scripts/export_xlsx.py` |

`score.py` derives Wave, all scores, Tier, Trigger_Score (from Trigger_Type), Contact_Score,
Email_Type, G2, G4 and the automatic segments, and refuses records that break the brief:
a mobile without a source URL, a failed gate in Active_Pipeline, a trigger outside 18 months,
a pitch hook over 25 words, an existing client. `audit_website.py` never scores a site it could
not load: those come back UNREACHABLE, SITE_BLOCKED or ENV_BLOCKED for a Manual_Check note.

### Lead JSON template

```json
{
  "Pipeline": "ACTIVE",
  "Company_Name": "", "Industry": "", "Key_Products": "", "State": "", "City_Cluster": "",
  "Plant_Locations": "", "Website_URL": "", "Year_Established": 1990, "Legal_Entity": "", "CIN": "", "GSTIN": "",
  "Revenue_Estimate_Cr": 0, "Revenue_FY": "FY2025", "Revenue_Source": "what + URL", "Size_Confidence": "High",
  "Employees": "", "Exporter_Markets": "", "Certifications": "", "Key_Clients": "",
  "Website_Decay_Score": 0, "Decay_Evidence": "", "Corporate_Profile_Status": "None|Old (2016)|Current (2024)",
  "LinkedIn_Presence": "Active|Inactive|None ...", "Social_Presence": "", "Google_Rating": "4.3 (56 reviews)",
  "Score_Inputs": {"proof_points": 0, "scale": 0, "reach": 0, "founder_visible": 0,
                   "pvt_to_public": false, "next_gen_confirmed": false},
  "Trigger_Type": "Rating capex", "Trigger_Detail": "", "Trigger_Date": "DD-MMM-YYYY", "Trigger_Source_URL": "",
  "Owner_Name": "", "Owner_Designation": "", "Owner_Mobile": "", "Owner_Mobile_Source_URL": "", "Owner_Email": "",
  "Next_Gen_Name": "", "Next_Gen_Role": "", "Next_Gen_LinkedIn_URL": "", "Company_Phone": "", "Company_Email": "",
  "G1_Manufacturer": "Y", "G3_Not_Popular": "Y", "G5_Right_Segment": "Y", "Manual_Check": "",
  "Broadcast_Segments": "", "Recommended_Offer": "", "Pitch_Hook": "", "Research_Notes": "",
  "Date_Researched": "DD-MMM-YYYY"
}
```

Trigger types and scores, reject codes, segments and industries are in `scripts/common.py`
and on the Legend sheet of the workbook.

## Data protection

Lead data (owner names, mobiles) is for Giraffe's own one-to-one outreach only (CLAUDE.md Section 8).
While this repository is public, `data/*.db`, `data/work/`, `input/` and `output/` are git-ignored.
Make the repository private before removing that guard.
