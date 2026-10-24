"""
confidence_scoring_engine.py
----------------------------
Formal Confidence Scoring Engine for Economic Sizing.
Implements the mathematical audit scoring function:
    S = w_1 * S_id + w_2 * S_temp + w_3 * S_primacy - P_opacity

Where:
- S_id (Weight = 0.30): Statutory Identity Resolution Quality [0 - 100]
- S_temp (Weight = 0.25): Temporal Freshness Decay [0 - 100]
- S_primacy (Weight = 0.35): Data Source Primacy & Grounding [0 - 100]
- P_opacity: Structural Opacity Penalty [0 - 40]

Also updates client_deliverable_licensee_estimates.csv and emits data/confidence_scores.json.
"""

import os
import json
import csv
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CLIENT_CSV = os.path.join(DATA_DIR, "client_deliverable_licensee_estimates.csv")
OUT_JSON = os.path.join(DATA_DIR, "confidence_scores.json")

# Weights configuration
WEIGHTS = {
    "w_id": 0.30,
    "w_temp": 0.25,
    "w_primacy": 0.35
}

# Entity scoring profiles
ENTITY_PROFILES = [
    {
        "id": "IN-028",
        "name": "WK Kellogg Co",
        "s_id": 98, # Official SEC CIK 0001959348, exact legal entity match
        "s_temp": 95, # Filed 10-K for FY2024; Form 15-12G filed Oct 2025
        "s_primacy": 100, # Primary SEC EDGAR audited 10-K filing
        "p_opacity": 15, # Penalty for post-fiscal deregistration (Form 15-12G acquisition/deregistration)
        "rationale": "High statutory precision from SEC EDGAR 10-K, discounted slightly for recent Form 15-12G deregistration."
    },
    {
        "id": "IN-030",
        "name": "Banca Transilvania S.A.",
        "s_id": 100, # National Bank CUI 5022670 + BVB: TLV
        "s_temp": 100, # FY2024 statutory credit-institution filing
        "s_primacy": 100, # Direct Ministry of Finance credit institution ledger (web_inst_credit_2024)
        "p_opacity": 5, # Minor penalty for non-standard turnover metric (banking operating income)
        "rationale": "Perfect statutory grounding in central bank / MF registry. Accounting schema tailored to banking."
    },
    {
        "id": "IN-016",
        "name": "Yazaki Romania S.R.L.",
        "s_id": 100, # CUI 15412557 / RegCom J29/774/2003
        "s_temp": 100, # Official FY2024 audited balance sheet
        "s_primacy": 100, # Direct Ministry of Finance full accounts filing (web_bl_bs_sl_an2024)
        "p_opacity": 10, # Divergence between high factory headcount (3,623) and captive transfer processing turnover
        "rationale": "Direct statutory verification from Romanian MF. Slight opacity penalty due to captive automotive wire assembly pricing."
    },
    {
        "id": "IN-015",
        "name": "Google Ireland Limited",
        "s_id": 98, # Irish CRO CoNo 368047
        "s_temp": 92, # Audited Irish statutory annual accounts
        "s_primacy": 100, # Primary statutory filing with Irish Companies Registration Office
        "p_opacity": 25, # High structural transfer-pricing divergence (€86.6B booked turnover vs 4,882 campus staff)
        "rationale": "Audited statutory accounts exist, but extreme transfer-pricing distortion requires pricing override."
    },
    {
        "id": "IN-061",
        "name": "MARGOT BAKERY LIMITED",
        "s_id": 95, # UK Companies House CoNo 09689240 confirmed
        "s_temp": 95, # Active micro-entity balance sheet filed for current cycle
        "s_primacy": 75, # Calibrated unit-economic proxy (empirical median from 4,858 bakeries + deck oven bounds)
        "p_opacity": 15, # P&L legally withheld under UK micro-entity exemption
        "rationale": "High identity match; P&L withheld by law, but proxy is tightly bounded by physical shopfront capacity and calibrated on 4.8k bakeries."
    },
    {
        "id": "IN-065",
        "name": "Tischlerei Thunemann KG",
        "s_id": 92, # Amtsgericht Osnabrück HRA 205396
        "s_temp": 90, # Active registry status in Lower Saxony
        "s_primacy": 72, # German HWK craft guild benchmark + vehicle fleet sizing
        "p_opacity": 18, # § 264a HGB German small partnership P&L exemption
        "rationale": "Confirmed German craft partnership. Financial proxy grounded in verified master craftsman guild billing rates and fleet census."
    },
    {
        "id": "IN-094",
        "name": "Rolex SA",
        "s_id": 100, # Swiss ZEFIX CHE-105.962.823 / Geneva HR
        "s_temp": 95, # Continuous annual COSC certifications & Swiss manufacturing census
        "s_primacy": 78, # Volumetric proxy (COSC chronometer volumes + retail realization margins)
        "p_opacity": 22, # Ultra-secretive private foundation ownership (Fondation Hans Wilsdorf)
        "rationale": "Perfect legal identity; corporate secrecy countered by hard physical limit of official Swiss chronometer certifications."
    },
    {
        "id": "IN-056",
        "name": "Anysphere",
        "s_id": 90, # Delaware C-Corp File 6843901 (Cursor)
        "s_temp": 85, # Real-time developer adoption velocity (late-2024 / early-2025)
        "s_primacy": 60, # Venture capital round velocity multiples + developer seats
        "p_opacity": 20, # Private venture with extreme revenue velocity ($10M -> $150M in 14 months)
        "rationale": "High-velocity AI startup where static annual filings are obsolete; estimated via active developer seat metrics."
    },
    {
        "id": "IN-086",
        "name": "STEYN HOLDING S.A., SPF",
        "s_id": 95, # Luxembourg RCS B168536
        "s_temp": 95, # Active Luxembourg legal status
        "s_primacy": 100, # Luxembourg Statutory Law of 11 May 2007 (Art. 1)
        "p_opacity": 0, # Zero opacity: statutory restriction guarantees commercial turnover is exactly €0
        "rationale": "Statutory legal restriction: SPFs are legally prohibited from commercial trading. Commercial turnover is strictly €0."
    },
    {
        "id": "IN-071",
        "name": "Old Spice",
        "s_id": 85, # Trademark / Operating division of P&G (SEC CIK 0000080424)
        "s_temp": 95, # Form 10-K Grooming segment FY2024
        "s_primacy": 85, # SEC 10-K Grooming segment allocation + Euromonitor retail scanner shares
        "p_opacity": 25, # Brand without standalone legal personality; potential for contract scope breach
        "rationale": "Parent financials are 100% verified; divisional allocation carries ±20% uncertainty, with high contractual scope risk."
    },
    {
        "id": "IN-082",
        "name": "Wirecard AG",
        "s_id": 98, # Amtsgericht München HRB 169227
        "s_temp": 95, # Active liquidation estate (Insolvency Case 99 IN 1308/20)
        "s_primacy": 100, # German Insolvency Court Decrees & Administrator Records
        "p_opacity": 0, # Defunct entity: commercial revenue is unambiguously €0
        "rationale": "Confirmed insolvent zombie entity in liquidation. Commercial trading revenue is €0; active operating staff is 0."
    },
    {
        "id": "IN-075",
        "name": "Apex Group",
        "s_id": 10, # FAILED RESOLUTION: Clashes with 4 multi-billion corporations
        "s_temp": 20, # Insufficient metadata to date the target entity
        "s_primacy": 0, # Deliberate refusal to impute ungrounded guesses
        "p_opacity": 50, # Extreme polysemic collision
        "rationale": "FAIL-CLOSED: Deliberate refusal to impute guesses when country, domain, and tax ID are completely absent."
    },
    {
        "id": "IN-002",
        "name": "SIEMENS HEALTHINEERS",
        "s_id": 100, # DAX 40 constituent: Siemens Healthineers AG (HRB 16568)
        "s_temp": 100, # Audited IFRS Annual Report FY2024
        "s_primacy": 100, # Primary regulated exchange stock filings
        "p_opacity": 5, # Minor risk of confusion with parent Siemens AG (€77B)
        "rationale": "Publicly listed DAX 40 constituent. Audited consolidated accounts leave near-zero reporting ambiguity."
    }
]

def calculate_confidence_score(p):
    """Calculates audit confidence score [0 - 100]."""
    w1 = WEIGHTS["w_id"]
    w2 = WEIGHTS["w_temp"]
    w3 = WEIGHTS["w_primacy"]
    
    base_score = (w1 * p["s_id"]) + (w2 * p["s_temp"]) + (w3 * p["s_primacy"])
    final_score = max(0.0, min(100.0, base_score - p["p_opacity"]))
    
    # Assign letter grade
    if p["s_id"] <= 15:
        grade = "FAIL_CLOSED (Refused)"
        tier_label = "UNRESOLVED / REFUSED"
    elif final_score >= 90:
        grade = "A+ (Auditor Guaranteed)"
        tier_label = "STATUTORY_GOLD"
    elif final_score >= 80:
        grade = "A (High Defensibility)"
        tier_label = "STATUTORY_VERIFIED"
    elif final_score >= 65:
        grade = "B (Empirically Bounded Proxy)"
        tier_label = "CALIBRATED_PROXY"
    elif final_score >= 50:
        grade = "C (Velocity Multiple / Segment Estimate)"
        tier_label = "ESTIMATED_PROXY"
    else:
        grade = "D (Speculative / High Risk)"
        tier_label = "HIGH_UNCERTAINTY"
        
    return round(final_score, 1), grade, tier_label

def run_scoring_engine():
    scored_results = {}
    
    print("=" * 80)
    print("VERIDION AUDIT CONFIDENCE SCORING ENGINE - BATCH EXECUTION")
    print("=" * 80)
    print(f"{'ID':<8} {'Entity Name':<25} {'S_id':<6} {'S_temp':<8} {'S_prim':<8} {'P_opac':<8} {'Final Score':<12} {'Grade'}")
    print("-" * 80)
    
    for p in ENTITY_PROFILES:
        score, grade, tier_label = calculate_confidence_score(p)
        scored_results[p["id"]] = {
            "licensee_id": p["id"],
            "name": p["name"],
            "s_id": p["s_id"],
            "s_temp": p["s_temp"],
            "s_primacy": p["s_primacy"],
            "p_opacity": p["p_opacity"],
            "confidence_score": score,
            "confidence_grade": grade,
            "audit_tier": tier_label,
            "rationale": p["rationale"]
        }
        print(f"{p['id']:<8} {p['name'][:24]:<25} {p['s_id']:<6} {p['s_temp']:<8} {p['s_primacy']:<8} {p['p_opacity']:<8} {score:<12.1f} {grade}")

    # Write confidence scores JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(scored_results, f, indent=2, ensure_ascii=False)
        
    # Update client_deliverable_licensee_estimates.csv with Confidence_Score and Confidence_Grade
    rows = []
    with open(CLIENT_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        
        # Add new columns if not present
        if "Audit_Confidence_Score" not in fieldnames:
            fieldnames.append("Audit_Confidence_Score")
        if "Confidence_Grade" not in fieldnames:
            fieldnames.append("Confidence_Grade")
            
        for row in reader:
            lid = row.get("Licensee_ID")
            if lid in scored_results:
                row["Audit_Confidence_Score"] = str(scored_results[lid]["confidence_score"])
                row["Confidence_Grade"] = scored_results[lid]["confidence_grade"]
            rows.append(row)
            
    with open(CLIENT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print("-" * 80)
    print(f"Scoring complete! Emitted {OUT_JSON} and updated {CLIENT_CSV}")

if __name__ == "__main__":
    run_scoring_engine()
