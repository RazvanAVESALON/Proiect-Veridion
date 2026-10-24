"""
Veridion Economic Data Science Task
Script: verify_figures.py
Purpose: Fail-closed provenance gate (DEC-009).
         Every figure that reaches the client file must come out of a fetch performed by THIS
         script, and carry: source_url, retrieved_at, raw value, period, method.
         Anything that cannot be re-fetched is WITHHELD (shown as a visible gap with a reason),
         never shipped with a confidence label.

Outputs:
  data/verified_figures.json                    - fetch log (one record per figure / status fact)
  data/client_deliverable_licensee_estimates.csv - gated client file
  data/provenance_audit.md                      - verified vs. previously shipped values + red flags
"""

import csv
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SUPERSEDED_CSV = os.path.join(DATA_DIR, "superseded", "client_deliverable_v0_unverified.csv")
OUT_LOG = os.path.join(DATA_DIR, "verified_figures.json")
OUT_CSV = os.path.join(DATA_DIR, "client_deliverable_licensee_estimates.csv")
OUT_AUDIT = os.path.join(DATA_DIR, "provenance_audit.md")

SEC_HEADERS = {"User-Agent": "VeridionResearch economic-intelligence@veridion-analyst.com"}
WEB_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# data.gov.ro, Ministry of Finance annual filings FY2024 (dataset situatii_financiare_2024)
MF_FILES = {
    "BL_BS_SL": {
        "path": os.path.join(DATA_DIR, "web_bl_bs_sl_an2024.txt"),
        "url": "https://data.gov.ro/dataset/d3caacb6-2c08-445e-94e6-8d36d00ab250/resource/f89140dc-20dd-494f-912a-d1a482188885/download/web_bl_bs_sl_an2024.txt",
        "fields": {"turnover": "I13", "employees": "I20"},
    },
    "INST_CREDIT": {
        "path": os.path.join(DATA_DIR, "web_inst_credit_2024.txt"),
        "url": "https://data.gov.ro/dataset/d3caacb6-2c08-445e-94e6-8d36d00ab250/resource/e6d67782-6319-456c-ae0a-a8123ef5a994/download/web_instit_de_credit_an2024.txt",
        # legend: I18 = Venituri totale din exploatare, net ; I23 = Cifra de afaceri neta ; no headcount column
        "fields": {"operating_income": "I18", "turnover": "I23"},
    },
}
BNR_2024_URL = "https://curs.bnr.ro/files/xml/years/nbrfxrates2024.xml"

FIGURES = []  # fetch log


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record(entity_id, field, value, unit, period, source_url, method, raw=None):
    rec = {
        "entity_id": entity_id, "field": field, "value": value, "unit": unit, "period": period,
        "source_url": source_url, "retrieved_at": now(), "method": method, "raw": raw,
    }
    FIGURES.append(rec)
    return rec


# ----------------------------------------------------------------------------- fetchers
def ensure_mf_file(key):
    spec = MF_FILES[key]
    if not os.path.exists(spec["path"]):
        r = requests.get(spec["url"], timeout=120)
        r.raise_for_status()
        with open(spec["path"], "wb") as f:
            f.write(r.content)
    return spec


def mf_row(key, cui):
    spec = ensure_mf_file(key)
    with open(spec["path"], encoding="utf-8", errors="ignore") as f:
        header = f.readline().strip().split(",")
        for line in f:
            if line.startswith(f"{cui},"):
                return spec, dict(zip(header, line.strip().split(",")))
    return spec, None


def bnr_eur_avg_2024():
    """Annual average EUR/RON from the National Bank of Romania daily fixings."""
    r = requests.get(BNR_2024_URL, headers=WEB_HEADERS, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    vals = [float(el.text) for el in root.iter() if el.tag.endswith("Rate") and el.attrib.get("currency") == "EUR"]
    return (sum(vals) / len(vals), len(vals)) if vals else (None, 0)


def sec_submissions(cik):
    return requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=SEC_HEADERS, timeout=30).json()


def sec_annual_revenue(cik):
    facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=SEC_HEADERS, timeout=60).json()
    gaap = facts["facts"].get("us-gaap", {})
    best = None
    for key in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"]:
        for u in gaap.get(key, {}).get("units", {}).get("USD", []):
            if not u.get("form", "").startswith("10-K") or "start" not in u:
                continue
            days = (datetime.fromisoformat(u["end"]) - datetime.fromisoformat(u["start"])).days
            if not 350 <= days <= 380:  # full fiscal year only (this is what tripped the old $640M figure)
                continue
            if best is None or u["end"] > best[1]["end"]:
                best = (key, u)
    return best


EMP_RE = re.compile(
    r"(?:approximately|about|roughly|had|employed)\s+([\d,]{3,9})\s+(?:full[- ]time\s+)?(?:employees|people|associates)",
    re.I,
)


def sec_10k_employees(cik, sub):
    rec = sub["filings"]["recent"]
    for form, accn, doc, fdate in zip(rec["form"], rec["accessionNumber"], rec["primaryDocument"], rec["filingDate"]):
        if form != "10-K":
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn.replace('-', '')}/{doc}"
        html = requests.get(url, headers=SEC_HEADERS, timeout=60).text
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).replace("&#160;", " ").replace("&nbsp;", " ")
        m = EMP_RE.search(text)
        if m:
            start = max(0, m.start() - 120)
            return int(m.group(1).replace(",", "")), url, fdate, text[start:m.end() + 60].strip()
        return None, url, fdate, None
    return None, None, None, None


def companies_house(number):
    base = f"https://find-and-update.company-information.service.gov.uk/company/{number}"
    prof = requests.get(base, headers=WEB_HEADERS, timeout=30).text
    hist = requests.get(base + "/filing-history", headers=WEB_HEADERS, timeout=30).text
    name = re.search(r"<h1[^>]*>\s*(.*?)\s*</h1>", prof, re.S)
    status = re.search(r'id="company-status"[^>]*>\s*(.*?)\s*<', prof, re.S)
    hist_txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", hist))
    accounts = re.findall(r"((?:Micro company|Total exemption full|Total exemption small|Unaudited abridged|Full) accounts made up to \d{1,2} \w+ \d{4})", hist_txt)
    return base, (name.group(1).strip() if name else None), (status.group(1).strip() if status else None), accounts


def zefix(name):
    url = "https://www.zefix.ch/ZefixREST/api/v1/firm/search.json"
    r = requests.post(url, json={"name": name, "languageKey": "en", "maxResults": 5}, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}, timeout=30)
    if r.status_code != 200:
        return url, None
    exact = [f for f in r.json().get("list", []) if f.get("name", "").upper() == name.upper()]
    return url, (exact[0] if exact else None)


# ----------------------------------------------------------------------------- entity verifications
def build():
    rows = {}
    eur, n_days = None, 0
    try:
        eur, n_days = bnr_eur_avg_2024()
        record("FX", "EURRON_avg_2024", round(eur, 4), "RON per EUR", "2024", BNR_2024_URL, f"Mean of {n_days} BNR daily fixings")
    except Exception as e:  # fail closed: no EUR conversion, RON stays
        print("BNR fetch failed:", e)

    def eur_note(ron):
        return f" (≈ €{ron / eur / 1e6:,.1f}M at BNR 2024 avg {eur:.4f})" if eur else ""

    # --- IN-016 Yazaki Romania (MF long-form filing)
    spec, r = mf_row("BL_BS_SL", 15412557)
    row = {"id": "IN-016", "input": "Yazaki Romania S.R.L.", "entity": "YAZAKI ROMANIA S.R.L.", "statutory_id": "RO CUI 15412557", "flags": []}
    if r:
        t = int(r["I13"]); e = int(r["I20"])
        record("IN-016", "turnover", t, "RON", "FY2024", spec["url"], "MF annual filing, field I13 (Cifra de afaceri neta)", r)
        record("IN-016", "employees", e, "persons (annual average)", "FY2024", spec["url"], "MF annual filing, field I20 (Numar mediu de salariati)")
        row.update(status="Files FY2024 accounts (living)", revenue=f"{t:,} RON{eur_note(t)}", revenue_def="Net turnover (cifra de afaceri neta)", rev_src=spec["url"],
                   employees=f"{e:,}", emp_def="Annual average employees", emp_src=spec["url"], period="FY2024", verdict="VERIFIED",
                   note=f"CAEN {r['CAEN']}. Turnover/employee ≈ {t / e:,.0f} RON.")
    rows["IN-016"] = row

    # --- IN-030 Banca Transilvania (MF credit-institution filing; no headcount column)
    spec, r = mf_row("INST_CREDIT", 5022670)
    row = {"id": "IN-030", "input": "Banca Transilvania S.A.", "entity": "BANCA TRANSILVANIA S.A.", "statutory_id": "RO CUI 5022670", "flags": []}
    if r:
        oi = int(r["I18"])
        record("IN-030", "operating_income_net", oi, "RON", "FY2024", spec["url"], "MF credit-institution filing, field I18 (Venituri totale din exploatare, net)", r)
        row.update(status="Files FY2024 accounts (living)", revenue=f"{oi:,} RON{eur_note(oi)}", revenue_def="Net operating income (banks have no 'turnover'; standalone bank, not group)",
                   rev_src=spec["url"], employees="WITHHELD", emp_def="", emp_src="", period="FY2024", verdict="PARTIAL",
                   note="Headcount is not a column in the credit-institution file; next source: BT annual report / BNR disclosure.")
    rows["IN-030"] = row

    # --- IN-028 WK Kellogg Co (SEC)
    cik = "0001959348"
    sub = sec_submissions(cik)
    forms = list(zip(sub["filings"]["recent"]["form"], sub["filings"]["recent"]["filingDate"]))
    row = {"id": "IN-028", "input": "WK Kellogg Co", "entity": "WK Kellogg Co", "statutory_id": f"SEC CIK {cik}", "flags": []}
    dereg = [d for f, d in forms if f in ("15-12G", "15-12B", "15-15D", "25-NSE")]
    sub_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    if dereg:
        record("IN-028", "status_event", "SEC deregistration (Form 15)", None, dereg[0], sub_url, "SEC submissions feed")
        row["flags"].append(f"Deregistered from SEC on {dereg[0]}; no ticker listed. Likely acquired — confirm acquirer before licensing at group level.")
    best = sec_annual_revenue(cik)
    emp, emp_url, emp_date, emp_raw = sec_10k_employees(cik, sub)
    facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    if best:
        key, u = best
        record("IN-028", "revenue", u["val"], "USD", f"{u['start']}..{u['end']}", facts_url, f"XBRL us-gaap:{key}, full-year duration, {u['form']} accn {u['accn']}")
    if emp:
        record("IN-028", "employees", emp, "persons", f"10-K filed {emp_date}", emp_url, "Regex on 10-K Human Capital text", emp_raw)
    row.update(status=("DEREGISTERED " + dereg[0]) if dereg else "SEC registrant",
               revenue=f"{best[1]['val']:,} USD" if best else "WITHHELD", revenue_def="Net sales (US GAAP, last full fiscal year filed)", rev_src=facts_url if best else "",
               employees=f"{emp:,}" if emp else "WITHHELD", emp_def="Employees per last 10-K" if emp else "", emp_src=emp_url or "",
               period=f"FY ending {best[1]['end']}" if best else "", verdict="VERIFIED (stale: last filing before deregistration)" if best else "WITHHELD",
               note="Figures describe the last year as a standalone filer. Current scope depends on the acquirer.")
    rows["IN-028"] = row

    # --- IN-071 Old Spice -> P&G parent (SEC). Brand-level figures are NOT verifiable -> withheld.
    cik = "0000080424"
    sub = sec_submissions(cik)
    best = sec_annual_revenue(cik)
    emp, emp_url, emp_date, emp_raw = sec_10k_employees(cik, sub)
    facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    if best:
        record("IN-071", "parent_revenue", best[1]["val"], "USD", f"{best[1]['start']}..{best[1]['end']}", facts_url, f"XBRL us-gaap:{best[0]}, full-year, accn {best[1]['accn']}")
    if emp:
        record("IN-071", "parent_employees", emp, "persons", f"10-K filed {emp_date}", emp_url, "Regex on 10-K text", emp_raw)
    rows["IN-071"] = {
        "id": "IN-071", "input": "Old Spice", "entity": "The Procter & Gamble Company (brand owner)", "statutory_id": f"SEC CIK {cik}",
        "status": "Brand, not a legal entity", "revenue": "WITHHELD (brand)", "revenue_def": "", "rev_src": "",
        "employees": "WITHHELD (brand)", "emp_def": "", "emp_src": "", "period": "", "verdict": "SCOPE QUESTION",
        "flags": [f"Contract names a brand. Parent P&G: revenue {best[1]['val']:,} USD (FY ending {best[1]['end']})" + (f", ~{emp:,} employees" if emp else "") + ". Which entity signed must be read from the contract."] if best else [],
        "note": "Brand-level revenue is not published; previous $1.45B figure had no fetchable source.",
    }

    # --- IN-061 Margot Bakery (Companies House): identity + filing category verified, financials withheld
    url, name, status, accounts = companies_house("09689240")
    record("IN-061", "identity", name, None, None, url, "Companies House profile page")
    record("IN-061", "company_status", status, None, None, url, "Companies House profile page")
    if accounts:
        record("IN-061", "accounts_category", accounts[0], None, None, url + "/filing-history", "Companies House filing history (most recent)")
    rows["IN-061"] = {
        "id": "IN-061", "input": "MARGOT BAKERY LIMITED", "entity": name or "MARGOT BAKERY LIMITED", "statutory_id": "UK CoNo 09689240",
        "status": status or "unknown", "revenue": "WITHHELD", "revenue_def": "", "rev_src": "", "employees": "WITHHELD", "emp_def": "", "emp_src": "",
        "period": "", "verdict": "MATCHED, NOT SIZED", "flags": [],
        "note": (f"Latest filing: '{accounts[0]}'. " if accounts else "") + "Small-company filing regime means turnover is not published; proxy must be rebuilt from observed inputs.",
    }

    # --- IN-094 Rolex SA (ZEFIX): identity verified, financials withheld
    url, firm = zefix("Rolex SA")
    if firm:
        record("IN-094", "identity", firm.get("name"), None, None, url, "ZEFIX firm search (exact name)", {k: firm.get(k) for k in ("uid", "status", "legalSeat", "ehraid")})
    rows["IN-094"] = {
        "id": "IN-094", "input": "Rolex SA", "entity": (firm or {}).get("name", "ROLEX SA"), "statutory_id": f"CH UID {(firm or {}).get('uid', '?')}",
        "status": (firm or {}).get("status", "unknown"), "revenue": "WITHHELD", "revenue_def": "", "rev_src": "", "employees": "WITHHELD",
        "emp_def": "", "emp_src": "", "period": "", "verdict": "MATCHED, NOT SIZED", "flags": [],
        "note": "Private, no filing duty. Previous COSC-based derivation used unsourced volume and margin inputs.",
    }

    # --- Rows with no fetch at all -> withheld with explicit reason
    not_fetched = {
        "IN-002": ("SIEMENS HEALTHINEERS", "Listed (Frankfurt); next source: annual report PDF / Unternehmensregister."),
        "IN-015": ("Google Ireland Limited", "Next source: CRO filed accounts (paid document) or parent 10-K segment notes."),
        "IN-056": ("Anysphere", "Private; previous files disagreed 10x on ARR and headcount. No registry publishes either."),
        "IN-065": ("Tischlerei Thunemann KG", "Previous files disagreed on town, activity and revenue. Needs Handelsregister + Impressum fetch."),
        "IN-082": ("Wirecard AG", "Insolvency is public record, but not fetched here; zero-revenue logic pending registry confirmation."),
        "IN-086": ("STEYN HOLDING S.A., SPF", "SPF form is stated in the client's own name; registry number conflicted across files. Pending RCS/LBR fetch."),
    }
    for k, (inp, why) in not_fetched.items():
        rows[k] = {"id": k, "input": inp, "entity": "NOT CONFIRMED", "statutory_id": "", "status": "", "revenue": "WITHHELD", "revenue_def": "", "rev_src": "",
                   "employees": "WITHHELD", "emp_def": "", "emp_src": "", "period": "", "verdict": "WITHHELD", "flags": [], "note": why}
    rows["IN-075"] = {"id": "IN-075", "input": "Apex Group", "entity": "UNRESOLVABLE", "statutory_id": "", "status": "", "revenue": "WITHHELD", "revenue_def": "",
                      "rev_src": "", "employees": "WITHHELD", "emp_def": "", "emp_src": "", "period": "", "verdict": "REFUSED MATCH", "flags": [],
                      "note": "Name with no country/domain collides with several unrelated groups. Ask the account owner for country or domain."}
    return rows


# ----------------------------------------------------------------------------- outputs
def write_csv(rows):
    cols = ["Licensee_ID", "Input_Name", "Matched_Entity", "Statutory_ID", "Entity_Status", "Revenue", "Revenue_Definition", "Revenue_Source",
            "Employees", "Employees_Definition", "Employees_Source", "Period", "Verification", "Red_Flags", "Notes"]
    order = ["IN-028", "IN-030", "IN-016", "IN-015", "IN-061", "IN-065", "IN-094", "IN-056", "IN-086", "IN-071", "IN-082", "IN-075", "IN-002"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for k in order:
            r = rows[k]
            w.writerow([r["id"], r["input"], r["entity"], r["statutory_id"], r["status"], r["revenue"], r["revenue_def"], r["rev_src"],
                        r["employees"], r["emp_def"], r["emp_src"], r["period"], r["verdict"], " | ".join(r["flags"]), r["note"]])


def to_num(s):
    try:
        return float(str(s).replace(",", ""))
    except ValueError:
        return None


def write_audit(rows):
    old = {}
    if os.path.exists(SUPERSEDED_CSV):
        with open(SUPERSEDED_CSV, encoding="utf-8") as f:
            old = {r["Licensee_ID"]: r for r in csv.DictReader(f)}
    by = {}
    for fig in FIGURES:
        by.setdefault(fig["entity_id"], {})[fig["field"]] = fig

    lines = ["# Provenance Audit: verified vs. previously shipped", f"Generated {now()} by `scripts/verify_figures.py` (DEC-009).", "",
             "| ID | Field | Previously shipped | Verified now | Δ | Source |", "| :-- | :-- | --: | --: | --: | :-- |"]
    checks = [("IN-016", "turnover", "Annual_Revenue_Best_Est", None), ("IN-016", "employees", "Employee_Count_Best_Est", None),
              ("IN-030", "operating_income_net", None, 8217313387), ("IN-028", "revenue", "Annual_Revenue_Best_Est", None),
              ("IN-028", "employees", "Employee_Count_Best_Est", None), ("IN-071", "parent_revenue", None, 84039000000)]
    fx = by.get("FX", {}).get("EURRON_avg_2024", {}).get("value")
    for eid, field, old_col, old_val in checks:
        fig = by.get(eid, {}).get(field)
        prev = old_val if old_val is not None else to_num(old.get(eid, {}).get(old_col, ""))
        if eid == "IN-016" and field == "turnover" and prev:
            prev = prev * fx if fx else None  # old file shipped EUR; compare in RON
        if not fig:
            lines.append(f"| {eid} | {field} | {prev:,.0f} | not fetched | – | – |" if prev else f"| {eid} | {field} | – | not fetched | – | – |")
            continue
        delta = f"{(fig['value'] - prev) / prev * 100:+.1f}%" if prev else "–"
        lines.append(f"| {eid} | {field} | {prev:,.0f} | {fig['value']:,} {fig['unit']} | {delta} | [{fig['method'][:40]}]({fig['source_url']}) |")
    lines += ["", "Note: IN-030 previous value was quoted in RON inside the derivation text; IN-071 previous parent figure was quoted in the notes.", "",
              "## Red flags raised by the gate"]
    for r in rows.values():
        for fl in r["flags"]:
            lines.append(f"- **{r['id']}**: {fl}")
    counts = {}
    for r in rows.values():
        key = r["verdict"].split(" (")[0]
        counts[key] = counts.get(key, 0) + 1
    lines += ["", "## Coverage", ""] + [f"- {k}: {v}" for k, v in sorted(counts.items())]
    with open(OUT_AUDIT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    rows = build()
    with open(OUT_LOG, "w", encoding="utf-8") as f:
        json.dump(FIGURES, f, indent=2, ensure_ascii=False, default=str)
    write_csv(rows)
    write_audit(rows)
    print(f"{len(FIGURES)} fetched facts logged -> {OUT_LOG}")
    for r in rows.values():
        print(f"  {r['id']:7} {r['verdict']:45} rev={r['revenue'][:40]:40} emp={r['employees']}")
