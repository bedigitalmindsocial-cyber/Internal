"""Writes sitemap.json: the 75-page plan (theme v1's 73 approved pages + 2 additions).
Edit the PAGES table, then run: python3 scripts/make_sitemap.py"""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# n, id, title, url, template, phase, entity, nav, golden, audiences, primary_cta, flags
PAGES = [
 # Phase 1 (25): live 2 Nov 2026 per theme v1
 (1,"home","Home","/","HOME",1,"Both","home",True,"U1 U2 U3 U4 U5","Open free account (mobile + OTP)","fo_risk regulated_numbers"),
 (2,"invest","Invest","/invest","A",1,"Both","invest",False,"U1 U4 U5","Start investing","mf_risk distributor_disclaimer"),
 (3,"trade","Trade","/trade","A",1,"Capital","trade",True,"U2 U3","Start trading","fo_risk"),
 (4,"plan-and-tools","Plan & Tools","/plan","A",1,"Both","plan",False,"U1 U4","Try the SIP calculator","mf_risk"),
 (5,"learn","Learn","/learn","A",1,"Both","learn",False,"U1 U2","Read the getting started guide",""),
 (6,"pricing","Pricing","/pricing","A",1,"Both","pricing",False,"U2 U1","Open free account","regulated_numbers distributor_disclaimer"),
 (7,"about","About ROOT and the Aikyam Group","/about","F",1,"Both","about",True,"U9 U1 U5","Open free account","regulated_numbers"),
 (8,"help-centre","Help Centre","/help","A",1,"Both","help",False,"U7","Raise a ticket",""),
 (9,"start-trading","Start Trading","/open-account/trading","D",1,"Capital","none",True,"U2 U1","Get OTP","minimal_header fo_risk regulated_numbers"),
 (10,"start-investing","Start Investing","/open-account/investing","D",1,"Wealth","none",False,"U1 U4","Get OTP","minimal_header mf_risk distributor_disclaimer"),
 (11,"get-the-app","Get the App","/app","D",1,"Both","none",False,"U1 U2 U7","Tell me when the app is live","minimal_header coming_soon"),
 (12,"aikyam-capital","Aikyam Capital","/about/aikyam-capital","F",1,"Capital","about",False,"U9","Open trading account","regulated_numbers"),
 (13,"aikyam-wealth","Aikyam Wealth","/about/aikyam-wealth","F",1,"Wealth","about",False,"U9 U5","Start investing","regulated_numbers distributor_disclaimer"),
 (14,"leadership","Leadership","/about/leadership","F",1,"Both","about",False,"U9 U5","Contact us",""),
 (15,"contact","Contact","/contact","F",1,"Both","help",False,"U7 U5 U6","Request a callback","regulated_numbers"),
 (16,"disclosures","Disclosures and Investor Charter","/legal/disclosures","G",1,"Both","none",False,"U9","Download the investor charter","regulated_numbers legal_text_client_supplied"),
 (17,"grievance-redressal","Grievance Redressal, SCORES and ODR","/legal/grievance-redressal","G",1,"Both","none",True,"U7 U9","Raise a complaint","regulated_numbers legal_text_client_supplied"),
 (18,"escalation-matrix","Escalation Matrix and Key Managerial Persons","/legal/escalation-matrix","G",1,"Both","none",False,"U7 U9","Raise a complaint","regulated_numbers legal_text_client_supplied"),
 (19,"policies","Policies","/legal/policies","G",1,"Both","none",False,"U9","Download a policy","legal_text_client_supplied"),
 (20,"client-bank-accounts","Client Bank Accounts","/legal/client-bank-accounts","G",1,"Capital","none",False,"U7 U9","Copy account details","regulated_numbers legal_text_client_supplied"),
 (21,"kyc-documents","KYC and Account Opening Documents","/legal/kyc-documents","G",1,"Both","none",False,"U1 U9","Open free account","legal_text_client_supplied"),
 (22,"risk-disclosure","Risk Disclosure","/legal/risk-disclosure","G",1,"Capital","none",False,"U2 U9","Read the full document","fo_risk legal_text_client_supplied"),
 (23,"notices","Notices and Caution to the Public","/legal/notices","G",1,"Both","none",False,"U9 U7","Report a fraud attempt","legal_text_client_supplied"),
 (24,"terms","Terms and Conditions","/legal/terms","G",1,"Both","none",False,"U9","Download PDF","legal_text_client_supplied"),
 (25,"privacy","Privacy Policy","/legal/privacy","G",1,"Both","none",False,"U9","Download PDF","legal_text_client_supplied"),
 # Phase 2 (25): live 8 Dec 2026 per theme v1
 (26,"mutual-funds","Mutual Funds","/invest/mutual-funds","A",2,"Wealth","invest",False,"U1 U4","Start a SIP","mf_risk distributor_disclaimer"),
 (27,"fund-explorer","Fund Explorer","/invest/mutual-funds/explore","B",2,"Wealth","invest",False,"U1 U4","View a scheme","illustrative_data mf_risk distributor_disclaimer"),
 (28,"sip","SIP","/invest/sip","A",2,"Wealth","invest",False,"U1 U4","Start a SIP","mf_risk distributor_disclaimer"),
 (29,"scheme-detail","Scheme Detail (example)","/invest/mutual-funds/example-flexi-cap-fund","B",2,"Wealth","invest",True,"U1 U4","Invest in this fund","illustrative_data mf_risk distributor_disclaimer"),
 (30,"distribution-commission","Distribution Fee and Commission Disclosure","/legal/distribution-commission","G",2,"Wealth","none",False,"U9 U1","Download the commission table","regulated_numbers distributor_disclaimer legal_text_client_supplied"),
 (31,"ipo","IPO","/ipo","A",2,"Capital","invest",False,"U3","Apply for an IPO","distributor_disclaimer"),
 (32,"upcoming-ipos","Upcoming IPOs","/ipo/upcoming","B",2,"Capital","invest",False,"U3","Apply","illustrative_data distributor_disclaimer"),
 (33,"ipo-calendar","IPO Calendar and Allotment Status","/ipo/calendar","B",2,"Capital","invest",False,"U3","Check allotment","illustrative_data"),
 (34,"ipo-detail","IPO Detail (example)","/ipo/example-ipo","B",2,"Capital","invest",False,"U3","Apply for this IPO","illustrative_data distributor_disclaimer"),
 (35,"equity","Equity","/trade/equity","A",2,"Capital","trade",False,"U2 U1","Start trading",""),
 (36,"intraday-delivery","Intraday and Delivery","/trade/intraday-delivery","A",2,"Capital","trade",False,"U2","Start trading",""),
 (37,"futures-options","Futures and Options","/trade/futures-options","A",2,"Capital","trade",False,"U2","Activate F&O","fo_risk"),
 (38,"currency-commodity","Currency and Commodity","/trade/currency-commodity","A",2,"Capital","trade",False,"U2","Start trading","fo_risk"),
 (39,"stock-detail","Stock Detail (example)","/stocks/example","B",2,"Capital","trade",False,"U2 U1","Buy on ROOT","illustrative_data licence_check"),
 (40,"markets","Markets and Indices","/markets","B",2,"Capital","trade",False,"U2","Open free account","illustrative_data licence_check"),
 (41,"calculators","Calculators","/tools","A",2,"Both","plan",False,"U1 U2 U4","Use a calculator",""),
 (42,"sip-calculator","SIP Calculator","/tools/sip-calculator","C",2,"Wealth","plan",True,"U1 U4","Start a SIP","mf_risk"),
 (43,"lumpsum-calculator","Lumpsum Calculator","/tools/lumpsum-calculator","C",2,"Wealth","plan",False,"U1 U4","Start investing","mf_risk"),
 (44,"retirement-calculator","Retirement Calculator","/tools/retirement-calculator","C",2,"Wealth","plan",False,"U4","Plan for retirement","mf_risk"),
 (45,"brokerage-calculator","Brokerage Calculator","/tools/brokerage-calculator","C",2,"Capital","plan",False,"U2","Open free account","regulated_numbers"),
 (46,"margin-calculator","Margin Calculator","/tools/margin-calculator","C",2,"Capital","plan",False,"U2","Activate F&O","fo_risk"),
 (47,"span-calculator","SPAN Calculator","/tools/span-calculator","C",2,"Capital","plan",False,"U2","Activate F&O","fo_risk"),
 (48,"risk-profiler","Risk Profiler","/tools/risk-profiler","C",2,"Both","plan",False,"U1 U4","See funds that match your profile","licence_check mf_risk"),
 (49,"retirement-planning","Retirement Planning","/plan/retirement","C",2,"Wealth","plan",False,"U4","Start a retirement SIP","mf_risk"),
 (50,"child-education-planning","Child Education Planning","/plan/child-education","C",2,"Wealth","plan",False,"U4","Start an education SIP","mf_risk"),
 # Phase 3 (23): 13 Jan 2027 per theme v1, plus 2 additions to reach 75
 (51,"insurance","Insurance","/insurance","H",3,"TBC","invest",False,"U8","Tell me when it is live","coming_soon"),
 (52,"life-insurance","Life Insurance","/insurance/life","H",3,"TBC","invest",False,"U8","Tell me when it is live","coming_soon"),
 (53,"health-insurance","Health Insurance","/insurance/health","H",3,"TBC","invest",False,"U8","Tell me when it is live","coming_soon"),
 (54,"general-insurance","Motor, Travel and Home Insurance","/insurance/general","H",3,"TBC","invest",False,"U8","Tell me when it is live","coming_soon"),
 (55,"bonds","Bonds and Fixed Income","/invest/bonds","H",3,"Wealth","invest",False,"U5","Tell me when it is live","coming_soon distributor_disclaimer"),
 (56,"nps","NPS","/invest/nps","H",3,"Wealth","invest",False,"U4","Tell me when it is live","coming_soon"),
 (57,"pms","PMS","/invest/pms","H",3,"Wealth","invest",True,"U5","Talk to the wealth team","coming_soon distributor_disclaimer licence_check"),
 (58,"pms-strategies","Empanelled PMS Strategies","/invest/pms/strategies","H",3,"Wealth","invest",False,"U5","Talk to the wealth team","coming_soon distributor_disclaimer licence_check"),
 (59,"pms-managers","PMS Manager Profiles","/invest/pms/managers","H",3,"Wealth","invest",False,"U5","Talk to the wealth team","coming_soon distributor_disclaimer licence_check"),
 (60,"pms-eligibility","PMS Eligibility and Minimum Investment","/invest/pms/eligibility","H",3,"Wealth","invest",False,"U5","Check if PMS suits you","coming_soon distributor_disclaimer"),
 (61,"partner","Partner with ROOT","/partner","F",3,"Both","none",False,"U6","Apply to partner",""),
 (62,"distributor-partner","Distributor Partner Programme","/partner/distributor-programme","F",3,"Wealth","none",False,"U6","Apply as a distributor partner","distributor_disclaimer"),
 (63,"authorised-person","Authorised Person Programme","/partner/authorised-person","F",3,"Capital","none",False,"U6","Apply as an Authorised Person","regulated_numbers"),
 (64,"tax-saving","Tax Saving","/plan/tax-saving","E",3,"Wealth","plan",False,"U1 U4","Start an ELSS SIP","mf_risk"),
 (65,"guide-getting-started","Guide: Getting Started","/learn/guides/getting-started","E",3,"Both","learn",True,"U1","Open free account",""),
 (66,"guide-mutual-funds","Guide: Mutual Funds","/learn/guides/mutual-funds","E",3,"Wealth","learn",False,"U1 U4","Start a SIP","mf_risk"),
 (67,"guide-pms","Guide: PMS","/learn/guides/pms","E",3,"Wealth","learn",False,"U5","Talk to the wealth team","distributor_disclaimer licence_check"),
 (68,"guide-insurance","Guide: Insurance","/learn/guides/insurance","E",3,"TBC","learn",False,"U8","Tell me when it is live","coming_soon"),
 (69,"guide-trading-basics","Guide: Trading Basics","/learn/guides/trading-basics","E",3,"Capital","learn",False,"U2","Start trading","fo_risk"),
 (70,"glossary","Glossary","/learn/glossary","E",3,"Both","learn",False,"U1","Read the getting started guide",""),
 (71,"careers","Careers","/careers","F",3,"Both","none",False,"Talent","See open roles",""),
 (72,"press","Press and Media","/press","E",3,"Both","none",False,"U9","Media contact",""),
 (73,"raise-ticket","Raise a Ticket","/help/raise-ticket","F",3,"Both","help",False,"U7","Submit ticket",""),
 (74,"login","Login","/login","D",3,"Both","none",False,"U7 U6","Log in to the right desk","minimal_header added"),
 (75,"lp-open-account","Paid Campaign Landing Page","/lp/open-account","D",3,"Capital","none",False,"U2 U1","Get OTP","minimal_header noindex fo_risk regulated_numbers added"),
]
# Red-team round 1 (12-Oct-2026) corrections, applied on top of PAGES
OVERRIDES = {
 1:  {"flags+": "mf_risk distributor_disclaimer illustrative_data"},
 2:  {"cta_href": "/open-account/investing"},
 22: {"flags+": "fo_page"},
 37: {"primary_cta": "Open trading account", "flags+": "fo_page"},
 38: {"flags+": "fo_page"},
 46: {"primary_cta": "Open trading account", "flags+": "fo_page"},
 47: {"primary_cta": "Open trading account", "flags+": "fo_page"},
 48: {"primary_cta": "See product categories for your risk level"},
 57: {"flags+": "pms"}, 58: {"flags+": "pms"}, 59: {"flags+": "pms"}, 60: {"flags+": "pms"}, 67: {"flags+": "pms"},
 61: {"template": "P", "primary_cta": "Choose your partner programme", "flags+": "regulated_numbers"},
 62: {"template": "P", "golden": True, "flags+": "regulated_numbers"},
 63: {"template": "P", "flags+": "fo_risk"},
 69: {"flags+": "fo_page"},
}

TEMPLATES = {
 "HOME":"Home: hero with lead bar, ticker, trust pillars, products, pricing, steps, goals, calculator, features, markets, group, learn, FAQ, app band, final CTA, risk",
 "A":"Hub: breadcrumb + d1 + creds hero, sticky lead form right, product cards 3-up, pillars or steps, calculator teaser, FAQ, dark band (app or closing CTA), risk, footer",
 "B":"Detail/data: breadcrumb + name + price, chart + range tabs, quote card with lead capture, stat blocks, data tables, riskometer or IPO dates, disclaimers + source",
 "C":"Calculator: breadcrumb + d1, calculator above the fold, start CTA, how it works, formula + worked example, FAQ",
 "D":"Account opening: logo-only header, d1 + creds, sticky form right, Rs 0 numeral + charges, four steps + documents, FAQ, short footer + risk",
 "E":"Article: thumbnail + d1 + read time, 66ch body with tables and callouts, inline calculator or CTA, related guides",
 "F":"Company: d1 + lead, group root diagram, people grid, credential wall, closing CTA band",
 "G":"Legal: d2 + last updated, numbered clauses with sticky contents list, download PDF",
 "H":"Coming soon: d1 + Coming soon badge, what it is and who it is for, tell-me-when-live dialog, related live products",
 "P":"Partner programme: d1 + who it is for + apply form right, eligibility and certifications, how it works (steps), what partners get (payouts as placeholders), partner obligations and code of conduct, which company signs the agreement, FAQ",
}

SITE = {"cta_label": "Open free account", "app_live": False, "pricing_approved": False,
        "login_url_at_launch": "https://trade.rootbyaikyam.com/login"}


def cta_for(url, tpl, ent, flags):
    """Where the page's primary action goes, which company receives the data, and the event it fires."""
    fe = "Aikyam Wealth" if ent == "Wealth" else "Aikyam Capital"
    if url.startswith("/open-account/") or url == "/lp/open-account":
        return {"href": "#s-open", "form_entity": fe, "event": "account_start"}
    if "coming_soon" in flags:
        return {"href": "#s-notify", "form_entity": fe, "event": "notify_signup"}
    if tpl == "P":
        return {"href": "#s-apply", "form_entity": fe, "event": "partner_lead"}
    if url in ("/contact", "/help/raise-ticket"):
        return {"href": "#s-form", "form_entity": "Aikyam Capital", "event": "ticket_raised" if "ticket" in url else "callback_request"}
    if url == "/login":
        return {"href": "#s-desks", "form_entity": None, "event": "login_click"}
    if tpl == "G":
        return {"href": "#s-contents", "form_entity": None, "event": "document_download"}
    if ent == "Wealth":
        return {"href": "/open-account/investing", "form_entity": "Aikyam Wealth", "event": "account_start"}
    return {"href": "/open-account/trading", "form_entity": "Aikyam Capital", "event": "account_start"}
pages=[]
for n,pid,title,url,tpl,ph,ent,nav,golden,aud,cta,flags in PAGES:
    o = OVERRIDES.get(n, {})
    tpl = o.get("template", tpl); golden = o.get("golden", golden); cta = o.get("primary_cta", cta)
    fl = flags.split() + [f for f in o.get("flags+", "").split() if f not in flags.split()]
    pages.append(dict(n=n,id=pid,file=f"{n:02d}-{pid}.html",title=title,url=url,template=tpl,phase=ph,
        entity=ent,nav=nav,mode="golden" if golden else "derivative",audiences=aud.split(),
        primary_cta=cta,cta=cta_for(url,tpl,ent,fl),flags=fl,status="todo"))
    if "cta_href" in o:
        pages[-1]["cta"] = {"href": o["cta_href"], "form_entity": "Aikyam Wealth" if "investing" in o["cta_href"] else "Aikyam Capital", "event": "account_start"}
urls = {p["url"] for p in pages}
for p in pages:  # parent: the hub above this page (breadcrumbs, "back to" links, journey context)
    u = p["url"]
    if u == "/":
        p["parent"] = None
    elif u.startswith("/legal/"):
        p["parent"] = "/" if u == "/legal/disclosures" else "/legal/disclosures"
    elif u.startswith("/tools/"):
        p["parent"] = "/tools"
    elif u.startswith("/open-account/") or u in ("/login", "/lp/open-account", "/app"):
        p["parent"] = "/"
    else:
        parts = u.strip("/").split("/")
        p["parent"] = next(("/" + "/".join(parts[:i]) for i in range(len(parts) - 1, 0, -1)
                            if "/" + "/".join(parts[:i]) in urls), "/")
golden_of = {p["template"]: p["file"] for p in pages if p["mode"] == "golden"}
for p in pages:
    p["golden_file"] = None if p["mode"] == "golden" else golden_of[p["template"]]
assert len(pages)==75 and len({p['url'] for p in pages})==75
gold={p['template'] for p in pages if p['mode']=='golden'}
assert gold==set(TEMPLATES), gold
json.dump({"version":2,"site":SITE,"source":"ROOT theme v1 (73-page plan, 3 phases) + 2 added pages (login, lp-open-account)",
  "templates":TEMPLATES,"pages":pages}, open(os.path.join(HERE,"sitemap.json"),"w"), indent=1, ensure_ascii=False)
print("wrote", len(pages), "pages;", sum(p['mode']=='golden' for p in pages), "golden")
