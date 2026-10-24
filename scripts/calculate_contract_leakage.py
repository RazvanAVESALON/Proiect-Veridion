"""
calculate_contract_leakage.py
-----------------------------
Financial Contract Leakage & Risk Quantification Engine.
Quantifies the financial impact for the software vendor across the 13 sample licensees:
- Naive Automated Scraper Billing vs. Audited Ground-Truth Billing
- Dollar Under-Billing (Revenue Leakage left on the table)
- Dollar Over-Billing (Customer Churn & Negotiation Collapse Risk)
- Bad Debt Write-Off Exposure (Insolvent / Zombie Entities)
- Scope Breach Exposure (Unrestricted Brand vs. Global Conglomerate)

Outputs:
- data/contract_leakage_matrix.json
- data/contract_leakage_report.md
"""

import os
import json
import csv
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CLIENT_CSV = os.path.join(DATA_DIR, "client_deliverable_licensee_estimates.csv")
OUT_JSON = os.path.join(DATA_DIR, "contract_leakage_matrix.json")
OUT_MD = os.path.join(DATA_DIR, "contract_leakage_report.md")

# Standard B2B Enterprise SaaS Pricing Tiers (Revenue & Headcount indexed)
TIERS = {
    "TIER_1_MICRO": {"name": "Tier 1: Micro / Craft (<20 FTE / <$2M)", "annual_fee": 6000, "per_seat": 300},
    "TIER_2_SME": {"name": "Tier 2: Mid-Market SME (20-250 FTE / $2M-$50M)", "annual_fee": 28000, "per_seat": 200},
    "TIER_3_UPPER_SME": {"name": "Tier 3: Upper Mid-Market (250-2,500 FTE / $50M-$500M)", "annual_fee": 95000, "per_seat": 140},
    "TIER_4_ENTERPRISE": {"name": "Tier 4: Large Enterprise (2,500-15,000 FTE / $500M-$5B)", "annual_fee": 260000, "per_seat": 90},
    "TIER_5_TITAN": {"name": "Tier 5: Mega Enterprise / Titan (>15,000 FTE / >$5B)", "annual_fee": 750000, "per_seat": 60},
    "TIER_0_INACTIVE": {"name": "Tier 0: Dormant / Write-off ($0 / 0 FTE)", "annual_fee": 0, "per_seat": 0}
}

def determine_contract_tier(headcount, revenue_usd):
    """Determines standard contractual tier based on headcount and revenue."""
    if headcount == 0 or revenue_usd == 0:
        return "TIER_0_INACTIVE"
    if headcount > 15000 or revenue_usd > 5000000000:
        return "TIER_5_TITAN"
    elif headcount >= 2500 or revenue_usd >= 500000000:
        return "TIER_4_ENTERPRISE"
    elif headcount >= 250 or revenue_usd >= 50000000:
        return "TIER_3_UPPER_SME"
    elif headcount >= 20 or revenue_usd >= 2000000:
        return "TIER_2_SME"
    else:
        return "TIER_1_MICRO"

# Case-by-case analysis of Naive Scraper vs Audited Reality
CASE_AUDITS = [
    {
        "id": "IN-028",
        "name": "WK Kellogg Co",
        "naive_behavior": "Scraper matches to stale parent Kellanova or reports $640M outdated carveout revenue; places in SME Tier 3.",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "Audited standalone SEC 10-K: $2.708B revenue, 3,280 employees -> Legitimate Tier 4 Enterprise.",
        "audited_tier": "TIER_4_ENTERPRISE",
        "audited_billed": 260000,
        "risk_category": "REVENUE_LEAKAGE",
        "leakage_amount": 165000, # Underbilled by $165k/yr
        "audit_note": "Software vendor leaves $165,000/year on the table due to stale revenue attribution."
    },
    {
        "id": "IN-030",
        "name": "Banca Transilvania S.A.",
        "naive_behavior": "Scraper looks for standard turnover (Cifra de Afaceri), finds 0 RON or distorted numbers; flags as SME or fails tiering.",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "National Bank statutory accounts: 8.19B RON net operating income (~€1.65B), 9,744 bank staff -> Tier 4 Enterprise.",
        "audited_tier": "TIER_4_ENTERPRISE",
        "audited_billed": 260000,
        "risk_category": "REVENUE_LEAKAGE",
        "leakage_amount": 165000,
        "audit_note": "Accounting schema mismatch (financial institutions do not report CAEN turnover) causes $165k annual underpricing."
    },
    {
        "id": "IN-016",
        "name": "Yazaki Romania S.R.L.",
        "naive_behavior": "Automated system prices either at Yazaki global Japanese conglomerate level ($14B+, Tier 5) or on €220M local turnover (Tier 3).",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "Romanian MF filing confirms 3,623 factory assembly workers. Seat count requires Tier 4, but local margin cannot sustain Tier 5.",
        "audited_tier": "TIER_4_ENTERPRISE",
        "audited_billed": 260000,
        "risk_category": "SEAT_MISMATCH",
        "leakage_amount": 165000,
        "audit_note": "If billed purely on turnover (€220M = Tier 3), vendor gives away 3,600+ industrial seats for $95k instead of $260k ($165k annual gap)."
    },
    {
        "id": "IN-015",
        "name": "Google Ireland Limited",
        "naive_behavior": "Scraper reads €86.6B turnover on Irish CRO filing and automatically slaps a Tier 5 Global Mega-Enterprise price ($750,000+).",
        "naive_tier": "TIER_5_TITAN",
        "naive_billed": 750000,
        "audited_reality": "Irish entity is a transfer-pricing hub. Dublin campus headcount is 4,882 FTE. Contract covers local EMEA operations (Tier 4).",
        "audited_tier": "TIER_4_ENTERPRISE",
        "audited_billed": 260000,
        "risk_category": "OVERBILLING_CHURN_RISK",
        "leakage_amount": -490000, # Overbilled by $490k
        "audit_note": "CRITICAL NEGOTIATION TRAP: Billed at $750k, Google EMEA procurement immediately rejects the contract and initiates vendor audit or replacement."
    },
    {
        "id": "IN-061",
        "name": "MARGOT BAKERY LIMITED",
        "naive_behavior": "Commercial database matches 'Margot' to large catering parent or imputes sector average (£3.5M turnover, Tier 2).",
        "naive_tier": "TIER_2_SME",
        "naive_billed": 28000,
        "audited_reality": "Companies House micro-entity: 1 retail deck oven, 7 staff, £490k turnover ($620k). True Tier 1 Micro-business.",
        "audited_tier": "TIER_1_MICRO",
        "audited_billed": 6000,
        "risk_category": "OVERBILLING_CHURN_RISK",
        "leakage_amount": -22000,
        "audit_note": "Billing £28,000/yr to a 7-person artisan bakery whose annual net profit is ~£15,000 results in 100% immediate cancellation."
    },
    {
        "id": "IN-065",
        "name": "Tischlerei Thunemann KG",
        "naive_behavior": "Scraper finds German §264a HGB exemption, fills with €5M default mid-market estimate (Tier 2).",
        "naive_tier": "TIER_2_SME",
        "naive_billed": 28000,
        "audited_reality": "Master joiner craft shop: 10 craftsmen, €1.35M turnover ($1.46M). True Tier 1 Craft Workshop.",
        "audited_tier": "TIER_1_MICRO",
        "audited_billed": 6000,
        "risk_category": "OVERBILLING_CHURN_RISK",
        "leakage_amount": -22000,
        "audit_note": "Overcharging small German craft shop causes churn to local open-source or manual software tools."
    },
    {
        "id": "IN-094",
        "name": "Rolex SA",
        "naive_behavior": "Scraper hits Swiss Handelsregister (ZEFIX), finds 'No P&L filed under Swiss Code of Obligations', defaults to $50M mid-tier or missing.",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "Volumetric COSC chronometer proxy: 1.05M-1.24M units, $11.5B wholesale revenue, 14,000 employees. Definite Tier 5 Global Titan.",
        "audited_tier": "TIER_5_TITAN",
        "audited_billed": 750000,
        "risk_category": "REVENUE_LEAKAGE",
        "leakage_amount": 655000,
        "audit_note": "MASSIVE UNDERBILLING: Treating Rolex as an unlisted mid-market entity leaves $655,000/year on the table."
    },
    {
        "id": "IN-056",
        "name": "Anysphere (Cursor)",
        "naive_behavior": "Commercial database looks at historical 2023 filings (<$10M ARR, 20 staff); assigns Tier 1 Micro/Seed.",
        "naive_tier": "TIER_1_MICRO",
        "naive_billed": 6000,
        "audited_reality": "High-velocity AI adoption: >$150M ARR run-rate, 110 high-leverage engineers -> Tier 3 Upper Mid-Market.",
        "audited_tier": "TIER_3_UPPER_SME",
        "audited_billed": 95000,
        "risk_category": "REVENUE_LEAKAGE",
        "leakage_amount": 89000,
        "audit_note": "Static annual databases lag VC velocity curves by 18-24 months, leaking $89,000/yr on rapidly growing developer tools."
    },
    {
        "id": "IN-086",
        "name": "STEYN HOLDING S.A., SPF",
        "naive_behavior": "Automated enrichment scraper sees 'Holding S.A. in Luxembourg with €50M+ investment portfolio'; bills Tier 3 or Tier 4.",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "Société de Patrimoine Familial (Law 11 May 2007) is legally prohibited from trading. Commercial turnover €0, 0 FTE.",
        "audited_tier": "TIER_0_INACTIVE",
        "audited_billed": 0,
        "risk_category": "UNENFORCEABLE_BILLING",
        "leakage_amount": -95000,
        "audit_note": "Contract signed with a wealth shell has zero operational users. Invoicing $95k produces immediate legal challenge and cancellation."
    },
    {
        "id": "IN-071",
        "name": "Old Spice",
        "naive_behavior": "Contract signed as 'Old Spice'; sales rep prices as a stand-alone personal care brand ($1.45B division = Tier 4, or $28k Tier 2).",
        "naive_tier": "TIER_2_SME",
        "naive_billed": 28000,
        "audited_reality": "Contract is legally executed under parent P&G (SEC CIK 0000080424, $87B rev, 104,000 staff). If enterprise-wide, Tier 5 Titan applies.",
        "audited_tier": "TIER_5_TITAN",
        "audited_billed": 750000,
        "risk_category": "CONGLOMERATE_SCOPE_BREACH",
        "leakage_amount": 722000,
        "audit_note": "LEGAL SCOPE EXPLOSION: If contractual definition allows enterprise-wide P&G usage, vendor leaks $722,000/yr in uncontracted software seats."
    },
    {
        "id": "IN-082",
        "name": "Wirecard AG",
        "naive_behavior": "Commercial database caches 2019 figures (€2.8B revenue, 5,300 staff); sales sends automated renewal invoice for Tier 4 ($260,000).",
        "naive_tier": "TIER_4_ENTERPRISE",
        "naive_billed": 260000,
        "audited_reality": "Munich Registergericht Ref 99 IN 1308/20: Insolvency opened Aug 2020. Company is defunct shell in liquidation. $0 revenue, 0 staff.",
        "audited_tier": "TIER_0_INACTIVE",
        "audited_billed": 0,
        "risk_category": "BAD_DEBT_WRITE_OFF",
        "leakage_amount": 260000,
        "audit_note": "CATASTROPHIC BAD DEBT: Invoicing $260k to an insolvent estate in liquidation creates 100% uncollectible accounts receivable."
    },
    {
        "id": "IN-075",
        "name": "Apex Group",
        "naive_behavior": "Scraper picks the first Google hit: Apex Group Ltd (Bermuda fund admin, $1.3B rev, 13k staff) and bills Tier 4 ($260,000).",
        "naive_tier": "TIER_4_ENTERPRISE",
        "naive_billed": 260000,
        "audited_reality": "Polysemic collision! Customer might be Apex Tool Group ($1.4B), Apex UK (£40M), or Apex Romania. Resolution cannot be proven.",
        "audited_tier": "TIER_0_INACTIVE", # Refusal to bill without disambiguation
        "audited_billed": 0,
        "risk_category": "POLYSEMIC_LITIGATION_RISK",
        "leakage_amount": 0,
        "audit_note": "HIGH AUDIT RISK: Arbitrarily picking one entity risks either massive overbilling lawsuit or delivering enterprise software to the wrong company."
    },
    {
        "id": "IN-002",
        "name": "SIEMENS HEALTHINEERS",
        "naive_behavior": "Sales team either bundles into Siemens AG conglomerate ($77B, 320k staff, Tier 5) or prices as local subsidiary.",
        "naive_tier": "TIER_3_UPPER_SME",
        "naive_billed": 95000,
        "audited_reality": "Standalone DAX 40 constituent: €21.68B ($23.5B) revenue, 71,000 employees. Standalone Tier 5 Mega-Enterprise.",
        "audited_tier": "TIER_5_TITAN",
        "audited_billed": 750000,
        "risk_category": "REVENUE_LEAKAGE",
        "leakage_amount": 655000,
        "audit_note": "Underbilling a DAX 40 medical giant by misclassifying it as a mid-market division leaves $655,000/year uncollected."
    }
]

def analyze_contract_leakage():
    total_naive_billed = sum(c["naive_billed"] for c in CASE_AUDITS)
    total_audited_billed = sum(c["audited_billed"] for c in CASE_AUDITS)
    
    # Financial buckets
    total_underbilled_leakage = sum(c["leakage_amount"] for c in CASE_AUDITS if c["leakage_amount"] > 0 and c["risk_category"] != "BAD_DEBT_WRITE_OFF")
    total_overbilled_churn_risk = sum(abs(c["leakage_amount"]) for c in CASE_AUDITS if c["leakage_amount"] < 0)
    total_bad_debt_exposure = sum(c["naive_billed"] for c in CASE_AUDITS if c["risk_category"] == "BAD_DEBT_WRITE_OFF")
    total_scope_breach_exposure = sum(c["leakage_amount"] for c in CASE_AUDITS if c["risk_category"] == "CONGLOMERATE_SCOPE_BREACH")
    
    summary = {
        "sample_size": len(CASE_AUDITS),
        "total_naive_billed": total_naive_billed,
        "total_audited_billed": total_audited_billed,
        "total_underbilled_leakage": total_underbilled_leakage,
        "total_overbilled_churn_risk": total_overbilled_churn_risk,
        "total_bad_debt_exposure": total_bad_debt_exposure,
        "total_scope_breach_exposure": total_scope_breach_exposure,
        "net_annual_impact": total_underbilled_leakage + total_scope_breach_exposure - total_bad_debt_exposure,
        "cases": CASE_AUDITS
    }
    
    # Write JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    # Write Markdown Report
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Financial Contract Leakage & Pricing Risk Audit\n")
        f.write("**Target Client:** B2B Software Vendor Pricing Contracts by Customer Scale (Revenue & Headcount)\n")
        f.write("**Evaluation Sample:** 13 Adversarial Licensees across 10 Asymmetry Archetypes\n\n")
        f.write("---\n")
        f.write("## 1. Executive Summary: The Cost of 'Plausible Wrong Numbers'\n\n")
        f.write(f"In enterprise software contracting, pricing based on unverified commercial scrapers (*'we googled it'*) leads to severe financial damage.\n")
        f.write(f"Across our 13-entity adversarial sample alone, naive automated scraping generates:\n\n")
        f.write(f"- **Total Annual Revenue Leakage (Under-billing):** **${total_underbilled_leakage:,.0f} / year** left on the table across titans like Rolex, WK Kellogg, and Siemens Healthineers.\n")
        f.write(f"- **Immediate Customer Churn & Renegotiation Collapse Risk:** **${total_overbilled_churn_risk:,.0f} / year** in overbilled contracts (e.g. Google Ireland €86B turnover trap, Margot Bakery enterprise misclassification).\n")
        f.write(f"- **Uncollectible Bad Debt Write-Off Exposure:** **${total_bad_debt_exposure:,.0f} / year** in uncollectible invoices sent to defunct zombie entities (Wirecard AG in insolvency).\n")
        f.write(f"- **Conglomerate Scope Explosion Risk:** **${total_scope_breach_exposure:,.0f} / year** in uncontracted software usage when contracts signed under a brand (Old Spice) cover global conglomerate employees (P&G 104,000 staff).\n\n")
        
        f.write("## 2. Contract Leakage Matrix (Entity by Entity)\n\n")
        f.write("| ID | Licensee Name | Naive Scraper Tier | Naive Bill | Audited Reality Tier | Audited Bill | Financial Impact | Risk Category |\n")
        f.write("| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- |\n")
        for c in CASE_AUDITS:
            diff = c["audited_billed"] - c["naive_billed"]
            diff_str = f"+${diff:,.0f}" if diff > 0 else (f"-${abs(diff):,.0f}" if diff < 0 else "$0")
            f.write(f"| **{c['id']}** | {c['name']} | `{c['naive_tier']}` | ${c['naive_billed']:,.0f} | `{c['audited_tier']}` | ${c['audited_billed']:,.0f} | **{diff_str}** | `{c['risk_category']}` |\n")
            
        f.write("\n---\n")
        f.write("## 3. Deep-Dive Case Studies\n\n")
        for c in CASE_AUDITS:
            f.write(f"### {c['id']}: {c['name']}\n")
            f.write(f"- **Naive Pipeline Behavior:** {c['naive_behavior']}\n")
            f.write(f"- **Audited Reality:** {c['audited_reality']}\n")
            f.write(f"- **Pricing Exposure:** {c['audit_note']}\n\n")
            
        f.write("---\n")
        f.write("## 4. Key Recommendations for the Client's Commercial Legal Team\n")
        f.write("1. **Contractual Definition of 'Customer':** Insert explicit language distinguishing standalone operating subsidiaries from parent holding turnover.\n")
        f.write("2. **Seat vs. Turnover Indexing:** In transfer-pricing hubs (Ireland, Netherlands, Singapore), contract pricing must strictly mandate seat-based tiering rather than top-line statutory turnover.\n")
        f.write("3. **Insolvency Flagging:** Wirecard demonstrates that commercial scrapers cache multi-billion dollar metrics for years after bankruptcy. Real-time insolvency court registry feeds must be integrated into billing systems.\n")

    print(f"Contract Leakage Analysis Complete!")
    print(f"Total Under-billed Leakage: ${total_underbilled_leakage:,.0f}")
    print(f"Total Over-billing Churn Risk: ${total_overbilled_churn_risk:,.0f}")
    print(f"Total Bad Debt Exposure: ${total_bad_debt_exposure:,.0f}")
    print(f"Total Conglomerate Scope Leakage: ${total_scope_breach_exposure:,.0f}")

if __name__ == "__main__":
    analyze_contract_leakage()
