"""Shared constants, column specs and helpers for the Giraffe lead engine.

Every rule that more than one script needs lives here, so the DB schema,
the scoring, the export and the Legend sheet can never drift apart.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
PROGRESS_DIR = ROOT / "progress"
DB_PATH = DATA_DIR / "leads.db"
STATES_PATH = CONFIG_DIR / "states.json"
EXCLUSIONS_PATH = CONFIG_DIR / "exclusions.txt"
COVERAGE_PATH = PROGRESS_DIR / "coverage.json"

# ---------------------------------------------------------------------------
# Controlled vocabularies (CLAUDE.md Sections 3, 4, 10, 11)
# ---------------------------------------------------------------------------

INDUSTRIES = [
    "Auto Components", "Engineering and Machinery", "Pumps and Motors",
    "Castings and Forgings", "Steel and Metals", "Wires and Cables",
    "Electrical Equipment", "Plastics and Packaging", "Chemicals and Dyes",
    "Pharma and API", "Agri Inputs", "Agri Machinery",
    "Food Processing and Edible Oils", "Dairy", "Textiles and Yarn",
    "Apparel and Hosiery", "Home Textiles", "Leather and Footwear",
    "Ceramics and Tiles", "Building Materials", "Furniture", "Wood and Plywood",
    "Paper and Printing", "Handicrafts and Home Decor", "Sports Goods",
    "Hand Tools and Hardware", "Bicycles and Parts", "Jewellery and Bullion",
    "Rubber and Tyres", "Glass", "Electronics", "Other",
]

SEGMENTS = {
    "SEG-EXPO": "Exhibits at trade fairs (2025 or 2026 editions).",
    "SEG-EXPORT": "Exporter, EPC member or export house.",
    "SEG-FRANCHISE": "Came from a franchise list or runs a franchise or dealer model.",
    "SEG-AGRI": "Agri inputs or agri machinery.",
    "SEG-AUTO": "Auto components.",
    "SEG-ENGG": "Engineering, machinery, pumps, castings, electricals, wires, hand tools.",
    "SEG-TEXTILE": "Yarn, fabric, apparel, hosiery, home textiles.",
    "SEG-CHEM-PHARMA": "Chemicals, dyes, pharma, API.",
    "SEG-BUILDMAT": "Ceramics, tiles, building materials, plywood, glass.",
    "SEG-FOOD": "Food processing, edible oils, dairy.",
    "SEG-JEWELLERY": "Jewellery and bullion.",
    "SEG-NEXTGEN": "Next-generation family director found.",
    "SEG-NOWEB": "No website of its own.",
    "CAPMKT": "SME-exchange listed or SME IPO DRHP filed: capital-markets narrative prospect.",
    "SEG-GIFTING": "Longterm_Broadcast only: EPC, road or government contractor; Diwali corporate gifting.",
}
SOURCE_TAG_RE = re.compile(r"^SRC-[A-Z0-9-]+$")  # e.g. SRC-FRANCHISE-INDIA (Section 11.2)

# Industry -> segment added automatically (researcher can add more by hand).
INDUSTRY_SEGMENT = {
    "Auto Components": "SEG-AUTO",
    "Engineering and Machinery": "SEG-ENGG",
    "Pumps and Motors": "SEG-ENGG",
    "Castings and Forgings": "SEG-ENGG",
    "Electrical Equipment": "SEG-ENGG",
    "Wires and Cables": "SEG-ENGG",
    "Hand Tools and Hardware": "SEG-ENGG",
    "Textiles and Yarn": "SEG-TEXTILE",
    "Apparel and Hosiery": "SEG-TEXTILE",
    "Home Textiles": "SEG-TEXTILE",
    "Chemicals and Dyes": "SEG-CHEM-PHARMA",
    "Pharma and API": "SEG-CHEM-PHARMA",
    "Ceramics and Tiles": "SEG-BUILDMAT",
    "Building Materials": "SEG-BUILDMAT",
    "Wood and Plywood": "SEG-BUILDMAT",
    "Glass": "SEG-BUILDMAT",
    "Food Processing and Edible Oils": "SEG-FOOD",
    "Dairy": "SEG-FOOD",
    "Agri Inputs": "SEG-AGRI",
    "Agri Machinery": "SEG-AGRI",
    "Jewellery and Bullion": "SEG-JEWELLERY",
}

REJECT_CODES = {
    "R1": "Verified revenue above ₹500 Cr",
    "R2": "Verified revenue below ₹50 Cr",
    "R3": "Popular or known brand (Wikipedia page, household name, heavy national media)",
    "R4": "Group company, MNC subsidiary, or PE/VC backed",
    "R5": "Listed on the NSE or BSE main board",
    "R6": "Modern website or branding (decay score 2 or less, recent redesign or agency credit)",
    "R7": "Not a manufacturer (trader, distributor, dealer, service firm)",
    "R8": "Wrong segment (aerospace, defence, global-standard precision engineering)",
    "R9": "Duplicate",
    "R10": "Existing Giraffe client or manual exclusion (config/exclusions.txt)",
    "R11": "Inactive, struck off, under liquidation or dormant",
    "R12": "Insufficient data after reasonable effort",
}

# Trigger type -> (score, description). Trigger_Score is derived from the type.
TRIGGER_TYPES = {
    "EC/CTE expansion": (5, "Environmental Clearance, Consent to Establish or EC public hearing for expansion or a new plant"),
    "Rating capex": (5, "Credit rating rationale that mentions capex or capacity expansion"),
    "MCA charge": (4, "New term loan or charge registered with MCA"),
    "State incentive": (4, "State investment subsidy or incentive approval"),
    "Regional news": (4, "Regional news of a new unit or investment"),
    "Trade fair": (3, "Exhibited at a trade fair, 2025 or 2026 edition"),
    "EPCG or machinery import": (3, "Capital machinery import or EPCG authorisation"),
    "Hiring": (2, "Hiring a first marketing, export or brand manager, or a plant head for a new unit"),
    "Pvt to Public or SME IPO": (2, "Pvt Ltd converted to Public Ltd, or SME IPO preparation"),
    "Exporter or association": (1, "Exporter or association member, no dated event"),
    "None": (0, "No trigger found"),
}
UNDATED_TRIGGERS = {"Exporter or association", "None"}

OFFERS = {
    "EXPO KIT": "Exhibitor with weak collateral: website, brochure and catalogue, 3D stall, corporate profile.",
    "ESSENTIALS + RETAINER": "₹50 to 150 Cr.",
    "PREMIUM + CAPITAL MARKETS": "₹150 to 500 Cr, or tagged CAPMKT, or a Pvt to Public Ltd conversion.",
}

STATUS_VALUES = ["New", "Called No Pickup", "Contacted", "Sample Sent", "Meeting Set",
                 "Proposal Sent", "Won", "Dropped"]
FU_STAGES = ["0", "1", "2", "3"]
SIZE_CONFIDENCE = ["High", "Medium", "Low"]
COVERAGE_STATUSES = ["Not Started", "In Progress", "Done", "N/A"]
SOURCE_TYPES = ["Rating rationale", "EC/CTE", "Trade fair", "Association", "Regional news",
                "Marketplace", "Maps listing", "Job post", "Company website", "Aggregator",
                "News", "Search results", "Other"]
CHECKLIST_SOURCES = [  # key, label used in STATE_CHECKLIST.md (Section 11.4)
    ("ratings", "ratings"), ("ec_cte", "EC/CTE"), ("expos", "expos"),
    ("associations", "associations"), ("regional_news", "regional news"),
    ("marketplaces", "marketplaces"), ("jobs", "jobs"),
]

FREE_EMAIL_PROVIDERS = {
    "gmail.com": "Gmail", "googlemail.com": "Gmail",
    "yahoo.com": "Yahoo", "yahoo.co.in": "Yahoo", "yahoo.in": "Yahoo", "ymail.com": "Yahoo",
    "rediffmail.com": "Rediffmail", "rediff.com": "Rediffmail",
    "hotmail.com": "Hotmail", "hotmail.co.in": "Hotmail", "live.com": "Hotmail",
    "outlook.com": "Hotmail", "msn.com": "Hotmail",
}
GENERIC_MAILBOXES = {
    "info", "sales", "contact", "contactus", "enquiry", "enquiries", "inquiry", "export",
    "exports", "marketing", "admin", "office", "mail", "support", "hr", "accounts",
    "purchase", "service", "care", "customercare", "business", "web", "webmaster", "hello",
}

# Hosts where many companies share one domain: never dedupe on the bare domain,
# and a storefront there does not count as the company's own website.
SHARED_PLATFORM_DOMAINS = {
    "indiamart.com", "tradeindia.com", "exportersindia.com", "justdial.com",
    "facebook.com", "instagram.com", "linkedin.com", "youtube.com", "twitter.com", "x.com",
    "blogspot.com", "wordpress.com", "wixsite.com", "weebly.com", "business.site",
    "sites.google.com", "google.com", "godaddysites.com", "webs.com", "jimdosite.com",
    "yellowpages.in", "sulekha.com", "alibaba.com", "made-in-china.com", "go4worldbusiness.com",
    "blogspot.in", "tripod.com", "webnode.com", "webnode.in", "hpage.com", "site123.me", "strikingly.com",
    "mystrikingly.com", "odoo.com", "ueniweb.com", "myshopify.com", "netlify.app", "vercel.app", "github.io",
    "web.app", "firebaseapp.com", "herokuapp.com", "azurewebsites.net", "wordpress.org",
}

INDIAN_SLDS = {"co", "net", "org", "gen", "firm", "ind", "ac", "edu", "gov", "res", "nic", "biz"}

# GSTIN state codes (first two digits) -> Lead_ID code, for a consistency warning.
GST_STATE_TO_CODE = {
    "01": "JK", "02": "HP", "03": "PB", "04": "CH", "05": "UK", "06": "HR", "07": "DL",
    "08": "RJ", "09": "UP", "10": "BR", "11": "SK", "12": "AR", "13": "NL", "14": "MN",
    "15": "MZ", "16": "TR", "17": "ML", "18": "AS", "19": "WB", "20": "JH", "21": "OD",
    "22": "CG", "23": "MP", "24": "GJ", "25": "DD", "26": "DD", "27": "MH", "28": "AP",
    "29": "KA", "30": "GA", "31": "LD", "32": "KL", "33": "TN", "34": "PY", "35": "AN",
    "36": "TG", "37": "AP", "38": "LA",
}

# ---------------------------------------------------------------------------
# Column specs: (name, sqlite type, group, definition). Drives schema + Legend.
# ---------------------------------------------------------------------------

ACTIVE_SPECS = [
    ("Lead_ID", "TEXT", "Priority", "Unique ID: state code plus 3-digit sequence (PB-001). One sequence per code, shared by Active and Longterm leads."),
    ("Tier", "TEXT", "Priority", "A, B or C (Section 10.7). Computed by scripts/score.py."),
    ("Priority_Score", "INTEGER", "Priority", "(Gap x 2) + (Trigger x 3) + (Contact x 2) + Wave bonus (Wave 1 +3, Wave 2 +1). Computed."),
    ("Company_Name", "TEXT", "Identity", "Name as shown on the company's own website or MCA record."),
    ("Industry", "TEXT", "Identity", "One value from the fixed Industry list (see Codes)."),
    ("Key_Products", "TEXT", "Identity", "Main products or capabilities, short list."),
    ("State", "TEXT", "Identity", "State or UT of the main plant."),
    ("City_Cluster", "TEXT", "Identity", "City or industrial area of the main plant; maps to a Section 7 cluster."),
    ("Plant_Locations", "TEXT", "Identity", "All known plant locations."),
    ("Wave", "INTEGER", "Identity", "Coverage wave 1 to 4 (Section 7). Derived from State and City_Cluster."),
    ("Website_URL", "TEXT", "Identity", "The company's own website. 'Not found' if none (then SEG-NOWEB)."),
    ("Year_Established", "INTEGER", "Identity", "Year founded or incorporated, as published by the company or MCA."),
    ("Legal_Entity", "TEXT", "Identity", "Pvt Ltd, Public Ltd (unlisted), LLP, Partnership, Proprietorship, etc."),
    ("CIN", "TEXT", "Identity", "MCA Corporate Identification Number, or LLPIN for an LLP."),
    ("GSTIN", "TEXT", "Identity", "GST registration number from a public, self-published source."),
    ("Revenue_Estimate_Cr", "REAL", "Size", "Annual turnover in ₹ Cr. Active leads must sit between 50 and 500."),
    ("Revenue_FY", "TEXT", "Size", "Financial year of the figure, e.g. FY2025."),
    ("Revenue_Source", "TEXT", "Size", "Source of the figure with its URL (rating rationale, aggregator, IndiaMART band, news)."),
    ("Size_Confidence", "TEXT", "Size", "High, Medium or Low (Section 5.2). Low is allowed only as Tier C with a Manual_Check note."),
    ("Employees", "TEXT", "Size", "Employee count or band, with the source when it is not the company site."),
    ("Exporter_Markets", "TEXT", "Size", "Export countries or regions; 'None' if domestic only."),
    ("Certifications", "TEXT", "Size", "Current certifications (ISO, CE, BIS, etc.)."),
    ("Key_Clients", "TEXT", "Size", "Named OEM, institutional or export clients, as published by the company."),
    ("Website_Decay_Score", "INTEGER", "Representation", "0 to 10 from scripts/audit_website.py (Section 5.1). No website = 10."),
    ("Decay_Evidence", "TEXT", "Representation", "Short proof for each decay point, e.g. '© 2016; ISO 9001:2008; gmail contact; no viewport'."),
    ("Corporate_Profile_Status", "TEXT", "Representation", "Starts with Current, Old or None (brochure or corporate profile PDF), then detail."),
    ("LinkedIn_Presence", "TEXT", "Representation", "Starts with Active (posts in last 90 days), Inactive or None, then URL or detail."),
    ("Social_Presence", "TEXT", "Representation", "Other channels (Facebook, Instagram, YouTube) and how active they are."),
    ("Google_Rating", "TEXT", "Representation", "Google Business rating and review count, e.g. '4.3 (56 reviews)', or 'Not found'."),
    ("Strength_Score", "INTEGER", "Representation", "0 to 10 (Section 10.1): revenue + proof points + scale + longevity + reach. Computed."),
    ("Visibility_Score", "INTEGER", "Representation", "0 to 10 (Section 10.2): website + profile + LinkedIn + Google + founder visibility. Computed."),
    ("Gap_Score", "INTEGER", "Representation", "Strength minus Visibility (-10 to +10): the representation gap. Computed."),
    ("Trigger_Type", "TEXT", "Trigger", "Highest trigger found, from the Trigger type list (see Codes)."),
    ("Trigger_Detail", "TEXT", "Trigger", "What happened, in one line (capacity, location, amount)."),
    ("Trigger_Date", "TEXT", "Trigger", "DD-MMM-YYYY (MMM-YYYY if only the month is known). Within 18 months; trade fairs: 2025 or 2026 editions."),
    ("Trigger_Source_URL", "TEXT", "Trigger", "URL that proves the trigger."),
    ("Trigger_Score", "INTEGER", "Trigger", "0 to 5 (Section 4), set by Trigger_Type. Computed."),
    ("Owner_Name", "TEXT", "People and contact", "Founder, promoter or MD."),
    ("Owner_Designation", "TEXT", "People and contact", "As published: Managing Director, Director, Proprietor, Partner."),
    ("Owner_Mobile", "TEXT", "People and contact", "Owner or director mobile, self-published only, stored as +91 XXXXX XXXXX."),
    ("Owner_Mobile_Source_URL", "TEXT", "People and contact", "Page where the owner or company published the mobile. No URL, no number."),
    ("Owner_Email", "TEXT", "People and contact", "Owner's direct email as published (not info@ or sales@)."),
    ("Next_Gen_Name", "TEXT", "People and contact", "Next-generation family director; '(probable)' unless the company states the relationship."),
    ("Next_Gen_Role", "TEXT", "People and contact", "Their role or designation."),
    ("Next_Gen_LinkedIn_URL", "TEXT", "People and contact", "LinkedIn URL taken from search results (LinkedIn is never fetched directly)."),
    ("Company_Phone", "TEXT", "People and contact", "Landline, company line or sales executive number."),
    ("Company_Email", "TEXT", "People and contact", "Generic company email (info@, sales@)."),
    ("Email_Type", "TEXT", "People and contact", "Own domain, Gmail, Yahoo, Rediffmail, Hotmail, Other domain or Not found. Computed."),
    ("Contact_Score", "INTEGER", "People and contact", "0 to 3 (Section 10.5). Computed."),
    ("G1_Manufacturer", "TEXT", "Checklist", "Y if the company owns and operates a plant in India."),
    ("G2_Size", "TEXT", "Checklist", "Y if turnover is ₹50 to 500 Cr with Medium or High confidence, or Low confidence parked as Tier C with Manual_Check."),
    ("G3_Not_Popular", "TEXT", "Checklist", "Y if none of the Section 3.2 exclusions apply."),
    ("G4_Weak_Representation", "TEXT", "Checklist", "Y if Website_Decay_Score is 3 or more, or there is no website. Computed."),
    ("G5_Right_Segment", "TEXT", "Checklist", "Y if not a Section 3.3 wrong segment."),
    ("Trigger_Found", "TEXT", "Checklist", "Y if Trigger_Score is above 0. Computed."),
    ("Owner_Contact_Found", "TEXT", "Checklist", "Y if an owner mobile or owner email was found. Computed."),
    ("Manual_Check", "TEXT", "Checklist", "Blank, or a short note of what a person must verify (captcha pages, blocked sources, Low size confidence)."),
    ("Broadcast_Segments", "TEXT", "Outreach", "Comma-separated tags (see Codes). Industry, SEG-EXPO, SEG-EXPORT, SEG-NEXTGEN and SEG-NOWEB are added automatically."),
    ("Recommended_Offer", "TEXT", "Outreach", "EXPO KIT, ESSENTIALS + RETAINER or PREMIUM + CAPITAL MARKETS (Section 10.8)."),
    ("Pitch_Hook", "TEXT", "Outreach", "One line, max 25 words, from verified findings only: one trigger plus one representation gap."),
    ("Research_Notes", "TEXT", "Outreach", "What the caller should know, with sources summarised."),
    ("Date_Researched", "TEXT", "Outreach", "DD-MMM-YYYY."),
    ("Assigned_To", "TEXT", "Calling tracker", "Caller name. Team fills."),
    ("FU_Stage", "TEXT", "Calling tracker", "Follow-up stage 0 to 3; drop after stage 3. Team fills."),
    ("Last_Contact_Date", "TEXT", "Calling tracker", "DD-MMM-YYYY. Team fills."),
    ("Status", "TEXT", "Calling tracker", "New, Called No Pickup, Contacted, Sample Sent, Meeting Set, Proposal Sent, Won, Dropped. Team fills."),
    ("Next_Action", "TEXT", "Calling tracker", "Team fills."),
    ("Drop_Reason", "TEXT", "Calling tracker", "Team fills when Status is Dropped."),
]
ACTIVE_COLUMNS = [s[0] for s in ACTIVE_SPECS]
SPEC_BY_NAME = {s[0]: s for s in ACTIVE_SPECS}
GROUP_COLUMNS: dict[str, list[str]] = {}
for _name, _type, _group, _def in ACTIVE_SPECS:
    GROUP_COLUMNS.setdefault(_group, []).append(_name)

LONGTERM_EXTRA_SPECS = [
    ("Reason_For_Longterm", "TEXT", "Outreach", "Why this lead is broadcast-only (e.g. road or EPC contractor: Diwali gifting prospect)."),
]
LONGTERM_COLUMNS = (["Lead_ID"] + GROUP_COLUMNS["Identity"] + GROUP_COLUMNS["People and contact"]
                    + ["Broadcast_Segments", "Reason_For_Longterm"])

REJECTED_SPECS = [
    ("Company_Name", "TEXT", "Rejected", "Company screened out."),
    ("State", "TEXT", "Rejected", "State or UT."),
    ("City", "TEXT", "Rejected", "City or industrial area."),
    ("Website_URL", "TEXT", "Rejected", "Website, if any."),
    ("Reject_Code", "TEXT", "Rejected", "R1 to R12 (see Codes)."),
    ("Reject_Evidence", "TEXT", "Rejected", "Short proof for the rejection."),
    ("Source_URL", "TEXT", "Rejected", "URL that proves the rejection."),
    ("Date", "TEXT", "Rejected", "DD-MMM-YYYY."),
]
REJECTED_COLUMNS = [s[0] for s in REJECTED_SPECS]

COVERAGE_SPECS = [
    ("Wave", "INTEGER", "State_Coverage", "Coverage wave 1 to 4."),
    ("State", "TEXT", "State_Coverage", "State or UT (Uttar Pradesh is split across Waves 1 and 2)."),
    ("Clusters_Planned", "INTEGER", "State_Coverage", "Number of Section 7 clusters for the state."),
    ("Clusters_Done", "INTEGER", "State_Coverage", "Clusters finished under the cluster stop rule."),
    ("Sources_Checked", "INTEGER", "State_Coverage", "URLs logged in Source_Log for the state."),
    ("Candidates_Screened", "INTEGER", "State_Coverage", "Active + Longterm + Rejected companies for the state."),
    ("Tier_A", "INTEGER", "State_Coverage", "Active Tier A leads."),
    ("Tier_B", "INTEGER", "State_Coverage", "Active Tier B leads."),
    ("Tier_C", "INTEGER", "State_Coverage", "Active Tier C leads."),
    ("Longterm", "INTEGER", "State_Coverage", "Longterm_Broadcast leads."),
    ("Rejected", "INTEGER", "State_Coverage", "Rejected companies."),
    ("Status", "TEXT", "State_Coverage", "Not Started, In Progress, Done or N/A."),
    ("Last_Updated", "TEXT", "State_Coverage", "DD-MMM-YYYY."),
    ("Notes", "TEXT", "State_Coverage", "Blockers, thin clusters, anything notable."),
]
COVERAGE_COLUMNS = [s[0] for s in COVERAGE_SPECS]

SOURCE_LOG_SPECS = [
    ("Date", "TEXT", "Source_Log", "DD-MMM-YYYY."),
    ("Lead_ID_or_Company", "TEXT", "Source_Log", "Lead_ID when the company became a lead, otherwise the company name or the query."),
    ("Source_Type", "TEXT", "Source_Log", "Rating rationale, EC/CTE, Trade fair, Association, Regional news, Marketplace, Maps listing, Job post, Company website, Aggregator, News, Search results, Other."),
    ("URL", "TEXT", "Source_Log", "Page consulted."),
    ("What_Was_Taken", "TEXT", "Source_Log", "Which facts came from it."),
]
SOURCE_LOG_COLUMNS = [s[0] for s in SOURCE_LOG_SPECS]

# Columns filled with 'Not found' on export when empty (never the tracker or Manual_Check).
NOT_FOUND_EXEMPT = set(GROUP_COLUMNS["Calling tracker"]) | {"Manual_Check"}

# ---------------------------------------------------------------------------
# Dates (DD-MMM-YYYY, month names fixed so the locale cannot change them)
# ---------------------------------------------------------------------------

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_INDEX = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}


def fmt_date(d: date) -> str:
    return f"{d.day:02d}-{MONTHS[d.month - 1]}-{d.year}"


def today_str() -> str:
    return fmt_date(date.today())


def parse_date(value) -> tuple[date | None, str]:
    """Parse DD-MMM-YYYY, MMM-YYYY or YYYY. Returns (date, precision).

    precision is 'day', 'month', 'year' or 'invalid'. Month and year precision
    return the first day of the period, which is only used for window checks.
    """
    if value is None:
        return None, "invalid"
    if isinstance(value, datetime):
        return value.date(), "day"
    if isinstance(value, date):
        return value, "day"
    s = str(value).strip()
    m = re.fullmatch(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})", s)
    if m and m.group(2).lower() in _MONTH_INDEX:
        try:
            return date(int(m.group(3)), _MONTH_INDEX[m.group(2).lower()], int(m.group(1))), "day"
        except ValueError:
            return None, "invalid"
    m = re.fullmatch(r"([A-Za-z]{3})-(\d{4})", s)
    if m and m.group(1).lower() in _MONTH_INDEX:
        return date(int(m.group(2)), _MONTH_INDEX[m.group(1).lower()], 1), "month"
    if re.fullmatch(r"(19|20)\d{2}", s):
        return date(int(s), 1, 1), "year"
    return None, "invalid"


def months_between(earlier: date, later: date) -> float:
    return (later.year - earlier.year) * 12 + (later.month - earlier.month) + (later.day - earlier.day) / 31.0


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

BLANK_MARKERS = {"", "not found", "n/a", "na", "-", "nil", "null", "unknown"}


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, (int, float)):
        return False
    return str(value).strip().lower() in BLANK_MARKERS


def sanitize_text(value):
    """Remove em dashes (Section 13). Spaced en dashes used as em dashes go too;
    unspaced en dashes in ranges such as 50–500 are kept."""
    if not isinstance(value, str):
        return value
    out = re.sub(r"\s*\u2014\s*", ", ", value)
    out = re.sub(r"\s+\u2013\s+", ", ", out)
    out = re.sub(r",\s*,", ",", out)
    out = re.sub(r"^\s*,\s*", "", out)
    return out.strip()


def word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.I)


def first_url(text) -> str | None:
    if not isinstance(text, str):
        return None
    m = URL_RE.search(text)
    return m.group(0).rstrip(".,;") if m else None


# ---------------------------------------------------------------------------
# Identity normalisation (used by dedupe and exclusions)
# ---------------------------------------------------------------------------

_LEGAL_SUFFIX_TOKENS = {"private", "pvt", "limited", "ltd", "llp", "opc", "p", "inc", "pl", "plc", "pvtltd"}
CITY_ALIASES = {
    "gurgaon": "gurugram", "bangalore": "bengaluru", "bombay": "mumbai", "madras": "chennai",
    "aurangabad": "chhatrapati sambhajinagar", "sambhajinagar": "chhatrapati sambhajinagar",
    "sas nagar": "mohali", "sahibzada ajit singh nagar": "mohali", "dera bassi": "derabassi",
    "calcutta": "kolkata", "baroda": "vadodara", "poona": "pune", "mysore": "mysuru",
    "tumkur": "tumakuru", "belgaum": "belagavi", "hubli": "hubballi", "hubli dharwad": "hubballi dharwad",
    "mangalore": "mangaluru", "cochin": "kochi", "vizag": "visakhapatnam", "allahabad": "prayagraj",
    "gobindgarh": "mandi gobindgarh", "yamuna nagar": "yamunanagar", "ganganagar": "sri ganganagar",
    "shri ganganagar": "sri ganganagar", "sonepat": "sonipat", "jagadhari": "jagadhri",
    "bhiwadi alwar": "bhiwadi", "trichy": "tiruchirappalli", "tirupur": "tiruppur",
}


def norm_company_name(name: str | None) -> str:
    if not name:
        return ""
    s = name.lower().replace("&", " and ")
    s = re.sub(r"\bm\s*/\s*s\.?\s+", " ", s)          # M/s prefix
    s = re.sub(r"\(\s*p\s*\)", " p ", s)              # (P) Ltd
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    tokens = s.split()
    if tokens and tokens[0] == "the":
        tokens = tokens[1:]
    while tokens and tokens[-1] in _LEGAL_SUFFIX_TOKENS:
        tokens.pop()
    if len(tokens) >= 2 and tokens[-2] == "and" and tokens[-1] in {"co", "company"}:
        tokens = tokens[:-2]
    return " ".join(tokens)


def norm_city(city: str | None) -> str:
    if not city:
        return ""
    s = re.sub(r"[^a-z ]+", " ", city.lower())
    s = " ".join(s.split())
    return CITY_ALIASES.get(s, s)


def split_cluster_cities(cluster_name: str) -> list[str]:
    """'Rajpura, Mohali and Derabassi' -> ['rajpura', 'mohali', 'derabassi']."""
    base = re.sub(r"\(.*?\)", "", cluster_name)
    parts = re.split(r",|\band\b|-", base)
    return [norm_city(p) for p in parts if norm_city(p)]


def host_of(url: str | None) -> str:
    if not url or is_blank(url):
        return ""
    u = url.strip()
    if not re.match(r"^[a-z][a-z0-9+.-]*://", u, re.I):
        u = "http://" + u
    host = (urlparse(u).hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def registrable_domain(host: str) -> str:
    labels = [l for l in host.split(".") if l]
    if len(labels) >= 3 and labels[-1] == "in" and labels[-2] in INDIAN_SLDS:
        return ".".join(labels[-3:])
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in {"co", "com", "org", "net"}:
        return ".".join(labels[-3:])   # e.g. example.co.uk, example.com.au
    return ".".join(labels[-2:]) if len(labels) >= 2 else host


def is_shared_platform(url: str | None) -> bool:
    host = host_of(url)
    return bool(host) and registrable_domain(host) in SHARED_PLATFORM_DOMAINS


def domain_key(url: str | None) -> str:
    """Dedupe key for a website. Shared platforms keep the subdomain or first path part."""
    host = host_of(url)
    if not host:
        return ""
    reg = registrable_domain(host)
    if reg in SHARED_PLATFORM_DOMAINS:
        if host != reg:
            return host
        u = url if re.match(r"^[a-z]+://", url, re.I) else "http://" + url
        first = (urlparse(u).path or "/").strip("/").split("/")[0].lower()
        return f"{reg}/{first}" if first else ""
    return reg


# ---------------------------------------------------------------------------
# Identifiers
# ---------------------------------------------------------------------------

_GST_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_RE = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")
CIN_RE = re.compile(r"^[LU]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}$")
LLPIN_RE = re.compile(r"^[A-Z]{3}-\d{4}$")


def gstin_checksum_ok(gstin: str) -> bool:
    total = 0
    for i, ch in enumerate(gstin[:14]):
        product = _GST_CHARS.index(ch) * (2 if i % 2 else 1)
        total += product // 36 + product % 36
    return _GST_CHARS[(36 - total % 36) % 36] == gstin[14]


def clean_gstin(value) -> str:
    return "" if is_blank(value) else re.sub(r"\s+", "", str(value)).upper()


def clean_cin(value) -> str:
    return "" if is_blank(value) else re.sub(r"\s+", "", str(value)).upper()


def normalize_mobile(value) -> str | None:
    """Return '+91 XXXXX XXXXX' for a valid Indian mobile, else None."""
    if is_blank(value):
        return None
    digits = re.sub(r"\D", "", str(value))
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != 10 or digits[0] not in "6789":
        return None
    return f"+91 {digits[:5]} {digits[5:]}"


def email_domain(email) -> str:
    if is_blank(email) or "@" not in str(email):
        return ""
    return str(email).strip().lower().rsplit("@", 1)[1]


def email_mailbox(email) -> str:
    if is_blank(email) or "@" not in str(email):
        return ""
    return str(email).strip().lower().split("@", 1)[0]


# ---------------------------------------------------------------------------
# Config loaders
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_states() -> dict:
    with open(STATES_PATH, encoding="utf-8") as f:
        return json.load(f)


def state_entries() -> list[dict]:
    return load_states()["states"]


def load_exclusions() -> list[str]:
    if not EXCLUSIONS_PATH.exists():
        return []
    out = []
    for line in EXCLUSIONS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def match_exclusion(company_name: str) -> tuple[str, str] | None:
    """(exclusion, 'exact' | 'similar'), or None.

    exact: same normalised name (a client under another legal suffix): reject R10.
    similar: one name starts with the other ("Kasturi India Textiles"): possibly a
    group company of a client, so flag it for a person to decide.
    """
    key = norm_company_name(company_name)
    if not key:
        return None
    similar = None
    for ex in load_exclusions():
        ekey = norm_company_name(ex)
        if not ekey:
            continue
        if key == ekey:
            return ex, "exact"
        if similar is None and (key.startswith(ekey + " ") or ekey.startswith(key + " ")):
            similar = (ex, "similar")
    return similar


def _state_matches(entry: dict, state: str) -> bool:
    s = (state or "").strip().lower()
    if not s:
        return False
    name = entry["state"].lower()
    base = re.sub(r"\s*\(.*\)$", "", name)
    return s in {name, base, entry["code"].lower()}


def resolve_state(state: str, city: str | None = None) -> tuple[dict | None, str | None]:
    """Find the states.json entry (and cluster name) for a state + city.

    Uttar Pradesh has two entries (Wave 1 West/NCR, Wave 2 rest); the city decides.
    Returns (entry, cluster_name). cluster_name is None when the city is outside
    the planned clusters (allowed, but worth a warning).
    """
    candidates = [e for e in state_entries() if _state_matches(e, state)]
    if not candidates:
        return None, None
    city_key = norm_city(city) if city else ""
    if city_key:
        for entry in candidates:
            for cl in entry["clusters"]:
                names = set(split_cluster_cities(cl["name"])) | {norm_city(a) for a in cl.get("areas", [])}
                names.add(norm_city(cl["name"]))
                if city_key in names or any(city_key.startswith(n + " ") or n.startswith(city_key + " ") for n in names if n):
                    return entry, cl["name"]
    return min(candidates, key=lambda e: e["wave"]), None


def wave_bonus(wave: int) -> int:
    return int(load_states()["wave_priority_bonus"].get(str(wave), 0))
