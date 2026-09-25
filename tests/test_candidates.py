"""candidates_xlsx.py: merge, screening and workbook on fictional research output."""
import json
import sys
from datetime import date
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import candidates_xlsx as X  # noqa: E402

TODAY = date(2026, 9, 25)
A = {"candidates": [
    {"company_name": "Fictional Knit Pvt Ltd", "is_manufacturer": "Yes", "industry": "Apparel and Hosiery",
     "revenue_cr": 180, "revenue_fy": "FY2025", "revenue_source": "Acuite 12-Jan-2026",
     "revenue_url": "https://www.acuite.in/x.pdf", "expansion_signal": "Debt-funded capex for new knitting unit",
     "expansion_date": "12-Jan-2026", "expansion_url": "https://www.acuite.in/x.pdf",
     "popularity_or_group_flags": "None found", "website": "fictionalknit.example"},
    {"company_name": "Fictional Listed Forge Ltd", "is_manufacturer": "Yes", "revenue_cr": 300, "revenue_fy": "FY2025",
     "popularity_or_group_flags": "Listed on NSE main board", "flags_url": "https://nse.example"},
    {"company_name": "Fictional Big Steel Pvt Ltd", "is_manufacturer": "Yes", "revenue_cr": 900, "revenue_fy": "FY2025",
     "revenue_url": "https://careratings.com/y.pdf"},
    {"company_name": "Fictional Traders", "is_manufacturer": "No", "manufacturer_evidence": "trading house"},
], "screened_out": [{"company_name": "Fictional Hotels Pvt Ltd", "reason": "hotel", "url": "https://h.example"}]}
B = {"candidates": [
    {"company_name": "FICTIONAL KNIT PRIVATE LIMITED", "trade_fair": "Knit Show 2026", "trade_fair_date": "Mar-2026",
     "trade_fair_url": "https://fair.example/2026", "promoters": "A. Fictional"},
    {"company_name": "Fictional Cycle Parts", "is_manufacturer": "Yes", "revenue_cr": 75, "revenue_fy": "FY2025",
     "revenue_source": "IndiaMART band Rs 50-100 Crore", "revenue_url": "https://www.indiamart.com/fcp/",
     "expansion_signal": "New plant", "expansion_date": "July 17, 2024", "expansion_url": "https://news.example/a",
     "popularity_or_group_flags": "None found"},
    {"company_name": "Fictional Tools", "is_manufacturer": "Unclear"},
], "screened_out": []}


def test_merge_screen_and_workbook(tmp_path):
    (tmp_path / "a.json").write_text(json.dumps(A))
    (tmp_path / "b.json").write_text(json.dumps(B))
    res = X.build([tmp_path / "a.json", tmp_path / "b.json"], "Ludhiana", "Punjab", "LDH",
                  tmp_path / "c.xlsx", use_db=False, today=TODAY)
    assert (res["candidates"], res["Strong"], res["Good"], res["Check"]) == (3, 1, 1, 1)
    wb = load_workbook(tmp_path / "c.xlsx")
    assert wb.sheetnames == ["Read_Me", "Candidates", "Screened_Out"]
    ws = wb["Candidates"]
    head = [c.value for c in ws[1]]
    first = {h: ws.cell(row=2, column=i + 1).value for i, h in enumerate(head)}
    assert first["Cand_ID"] == "LDH-C01" and first["Fit"] == "Strong"
    assert first["Company_Name"] == "Fictional Knit Pvt Ltd"          # merged across both files
    assert first["Signal_Type"] == "Rating capex" and first["Promoters"] == "A. Fictional"
    assert "Trade fair" in first["Other_Signals"]
    second = {h: ws.cell(row=3, column=i + 1).value for i, h in enumerate(head)}
    assert second["Fit"] == "Good" and second["Signal_Type"] == "None within window"   # 2024 news is too old
    assert "self-declared" in second["Size_Confidence"]
    reasons = {r[0].value: r[1].value for r in wb["Screened_Out"].iter_rows(min_row=2)}
    assert reasons == {"Fictional Listed Forge Ltd": "R5", "Fictional Big Steel Pvt Ltd": "R1",
                       "Fictional Traders": "R7", "Fictional Hotels Pvt Ltd": "R7"}
