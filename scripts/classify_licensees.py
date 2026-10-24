"""
Veridion Economic Data Science Task
Script: classify_licensees.py
Purpose: Classifies the 100 messy licensee names into structured corporate archetypes
         and information asymmetry tiers based on observational barriers and commercial risk.
"""

import os
import csv
import json
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "licensee_list.csv")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_CSV = os.path.join(DATA_DIR, "licensees_classified.csv")
OUTPUT_MD = os.path.join(DATA_DIR, "archetypes_summary.md")
OUTPUT_JSON = os.path.join(DATA_DIR, "archetypes.json")

# Define Archetypes and Tiers according to DEC-004 (Information Asymmetry Lens)
ARCHETYPES_DEF = {
    "TIER_1_PUBLIC_BENCHMARK": {
        "tier": "Tier 1: Full Transparency (Public Ground Truth)",
        "archetype": "Public Listed Corporations & Direct Filers",
        "barrier": "Minimal opacity. Audited Form 10-K, IFRS, or local exchange filings exist.",
        "proxy_strategy": "Direct registry extraction (SEC EDGAR, BVB, LSE). Used to calibrate proxy error baselines.",
        "commercial_risk": "Low entity ambiguity, but high risk of contract stagnation if historical seat pricing fails to track annual turnover growth.",
    },
    "TIER_2_TAX_TRANSFER_DISTORTION": {
        "tier": "Tier 2: Structural Distortions (Tax & Transfer Pricing Hubs)",
        "archetype": "Foreign Operating & Billing Hubs vs Manufacturing Plants",
        "barrier": "Entity revenue is decoupled from local physical footprint. Brass-plate billing hubs show astronomical booked revenue; local assembly plants show massive headcount with low margins.",
        "proxy_strategy": "Headcount-to-revenue divergence analysis. Cross-referencing local CRO/ONRC registry filings with LinkedIn and physical site counts.",
        "commercial_risk": "Severe mispricing. Pricing on revenue overcharges billing hubs (5k staff booking €80B); pricing on headcount under-bills global software consumption.",
    },
    "TIER_3_REGULATORY_EXEMPTION": {
        "tier": "Tier 3: Regulatory Black Box (Filing Exemptions)",
        "archetype": "Micro-SMEs, Artisanal Bakeries & Local Craftsmen",
        "barrier": "Statutory filing exemptions (UK Companies Act micro-entity rules, German §264a HGB for KG/UG). Balance sheets are abbreviated; Profit & Loss (turnover) is legally withheld.",
        "proxy_strategy": "Unit-economics & physical footprint proxies: daily transactions, oven/table capacity, storefront locations, guild/chamber registrations.",
        "commercial_risk": "Overcharging & customer churn. Automated models applying industry-average revenues overbill 6-person local workshops.",
    },
    "TIER_4_STRATEGIC_SECRECY": {
        "tier": "Tier 4: Strategic Secrecy (Private Conglomerates & Family Trusts)",
        "archetype": "Ultra-Secretive Private Titans & Family Foundations",
        "barrier": "Privately owned by foundations (e.g. Hans Wilsdorf) or private LLCs with no public stock filings.",
        "proxy_strategy": "Physical capacity & output proxies: production unit certifications (COSC watch movements), container fleet TEU capacity, logistics warehouse sqft.",
        "commercial_risk": "Massive revenue leakage. Multi-billion luxury or shipping giants paying standard private-company enterprise fees.",
    },
    "TIER_5_VELOCITY_DISTORTION": {
        "tier": "Tier 5: High Velocity (Hyper-Growth AI & Venture Startups)",
        "archetype": "VC-Backed DeepTech, Defense Tech & AI Startups",
        "barrier": "Historic corporate filings (if any) are obsolete in 90 days. Headcount is lean (20-100 staff), but ARR scales exponentially from $0 to $100M+.",
        "proxy_strategy": "Venture round valuation multiples, developer adoption velocity, GitHub traction, and enterprise seat deployment tracking.",
        "commercial_risk": "Severe under-pricing. Vendor charges small-team tier ($5k/yr) while client raises billions and deploys product to thousands of end-users.",
    },
    "TIER_6_CAPITAL_VS_OPERATIONS": {
        "tier": "Tier 6: Capital vs. Operations Illusion (Three People & a Mailbox)",
        "archetype": "Holding Vehicles, Wealth Management SPFs & Shells",
        "barrier": "Société de Gestion de Patrimoine Familial (Luxembourg SPF) or pure asset holding vehicles. Balance sheet assets exceed hundreds of millions, but commercial revenue and operating staff are near zero.",
        "proxy_strategy": "Statutory legal form identification (SPF, SICAV, Vermögensverwaltung). Discarding balance sheet equity as an operating proxy.",
        "commercial_risk": "Lost negotiations. Vendor attempts enterprise pricing on balance sheet scale to an entity requiring only 2 administrative licenses.",
    },
    "TIER_7_LEGAL_GHOSTS_DEFUNCT": {
        "tier": "Tier 7: Legal Ghosts & Defunct Entities",
        "archetype": "Product Brands, Bankrupt Estates & M&A Carve-Outs",
        "barrier": "The entity on the contract is either a marketing trade brand (no legal entity), an insolvent estate, or an entity dissolved through emergency acquisition.",
        "proxy_strategy": "Registry status verification (Amtsgericht insolvency decrees, commercial register dissolution, parent brand attribution rules).",
        "commercial_risk": "Legal unenforceability & bad debt write-offs. Software runs for defunct or dissolved entities where licenses cannot be legally recovered.",
    },
    "TIER_8_POLYSEMIC_AMBIGUITY": {
        "tier": "Tier 8: Polysemic & Zero-Metadata Noise",
        "archetype": "Ambiguous Generic Names (Missing Country/Address)",
        "barrier": "Generic corporate names (e.g. 'Apex Group', 'Meridian') with missing geographic and digital breadcrumbs.",
        "proxy_strategy": "Resolution Threshold Rule: explicitly categorizing as 'Unresolvable: Insufficient Disambiguation Signals' to prevent false-positive matching.",
        "commercial_risk": "Catastrophic misattribution. Conflating a local shipping agency with a multi-billion dollar hedge fund.",
    },
    "TIER_9_PUBLIC_SECTOR_UTILITIES": {
        "tier": "Tier 9: Non-Commercial & Regulated Public Institutions",
        "archetype": "Public Health Trusts, Municipal Utilities & Authorities",
        "barrier": "Non-commercial accounting. Revenue corresponds to tax appropriations, farebox tariffs, or statutory grants, not competitive market sales.",
        "proxy_strategy": "Public budget allocations, hospital bed count, passenger volume, municipal operating reports.",
        "commercial_risk": "Budget freeze / procurement failure. Public sector compliance requires bespoke licensing independent of commercial ARR models.",
    },
    "TIER_10_SPINOFFS_MAZE": {
        "tier": "Tier 10: The Conglomerate Matrix & Carve-Outs",
        "archetype": "Corporate Spin-Offs, Separated Divisions & Subsidiaries",
        "barrier": "Independent public listing while retaining parent naming heritage (e.g. Siemens Healthineers, Siemens Energy).",
        "proxy_strategy": "Ownership stake & consolidation test: verify parent 10-K consolidation (>50% vs deconsolidated public spin-offs).",
        "commercial_risk": "Contract arbitrage. Spun-off multi-billion standalone entities sharing licenses under parent conglomerate umbrella discounts.",
    }
}

# Mapping rules for all 100 rows
def classify_licensee(row_id, name, address, country, website):
    name_upper = name.upper()
    
    # Tier 10: Siemens & Spinoff Maze
    if "SIEMENS" in name_upper:
        if "HEALTHINEERS" in name_upper:
            return "TIER_10_SPINOFFS_MAZE", "IN-002: Standalone public medical spin-off (majority Siemens AG owned)"
        elif "ENERGY" in name_upper or "GAMESA" in name_upper:
            return "TIER_10_SPINOFFS_MAZE", "IN-007/008: Deconsolidated energy spin-off (standalone DAX company)"
        elif "MOBILITY" in name_upper or "INDUSTRY SOFTWARE" in name_upper:
            return "TIER_10_SPINOFFS_MAZE", "Operating division / wholly owned industrial subsidiary"
        else:
            return "TIER_10_SPINOFFS_MAZE", "Regional operating subsidiary of Siemens AG conglomerate"
    
    # Specific Spinoffs
    if row_id in ["IN-026", "IN-027", "IN-028", "IN-029"]:
        if row_id == "IN-028":
            return "TIER_1_PUBLIC_BENCHMARK", "WK Kellogg Co: 2023 spin-off from Kellogg Company, public listed (NYSE: KLG)"
        return "TIER_10_SPINOFFS_MAZE", f"{name}: Public corporate carve-out / spin-off"
    
    # Tier 1: Public Benchmarks & Regulated Public Giants
    if row_id in ["IN-011", "IN-012", "IN-013", "IN-014", "IN-025", "IN-030", "IN-037"]:
        return "TIER_1_PUBLIC_BENCHMARK", f"Publicly listed enterprise with direct audited annual filings"
        
    # Tier 2: Foreign Operating & Tax/Transfer Hubs
    if row_id == "IN-015":
        return "TIER_2_TAX_TRANSFER_DISTORTION", "Google Ireland Limited: Primary EMEA billing & tax routing hub (~€86B turnover, ~4.9k employees)"
    if row_id in ["IN-016", "IN-017", "IN-018", "IN-019", "IN-020", "IN-021", "IN-022", "IN-023", "IN-024"]:
        return "TIER_2_TAX_TRANSFER_DISTORTION", f"Foreign manufacturing/distribution operating subsidiary of multinational group"
        
    # Tier 3: Regulatory Filing Exemptions (Bakeries & Carpenters)
    if any(k in name_upper for k in ["BAKERY", "PANIFICATIE", "TISCHLEREI"]):
        return "TIER_3_REGULATORY_EXEMPTION", "Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions"
        
    # Tier 4: Strategic Secrecy (Private Giants)
    if row_id in ["IN-093", "IN-094", "IN-095", "IN-096", "IN-097", "IN-098", "IN-099", "IN-100", "IN-091", "IN-092"]:
        if row_id == "IN-094":
            return "TIER_4_STRATEGIC_SECRECY", "Rolex SA: 100% owned by Hans Wilsdorf Foundation; zero public P&L; estimated via COSC production"
        elif row_id == "IN-093":
            return "TIER_4_STRATEGIC_SECRECY", "MSC: Family-owned Swiss shipping titan; estimated via TEU fleet capacity"
        return "TIER_4_STRATEGIC_SECRECY", "Large private/family conglomerate with no public equity disclosure"
        
    if row_id == "IN-090":
        return "TIER_1_PUBLIC_BENCHMARK", "Arcos Dorados: Publicly listed McDonald's master franchisee (NYSE: ARCO)"

    # Tier 5: Velocity Distortion (High Growth AI / DeepTech Startups)
    if row_id in ["IN-049", "IN-050", "IN-051", "IN-052", "IN-053", "IN-054", "IN-055", "IN-056", "IN-057", "IN-058", "IN-059"]:
        if row_id == "IN-056":
            return "TIER_5_VELOCITY_DISTORTION", "Anysphere (Cursor): Rapid ARR growth ($100M+ ARR), venture-backed Delaware C-Corp"
        return "TIER_5_VELOCITY_DISTORTION", "High-growth venture-backed tech / defense startup with private unfiled accounts"

    # Tier 6: Capital vs Operations (Holding SPFs & Wealth Shells)
    if row_id in ["IN-085", "IN-086"] or "SPF" in name_upper:
        return "TIER_6_CAPITAL_VS_OPERATIONS", "Luxembourg SPF / Wealth Holding vehicle: substantial assets, 0 operational headcount, €0 commercial turnover"
    if row_id in ["IN-036", "IN-038", "IN-039", "IN-040", "IN-041", "IN-042"]:
        return "TIER_6_CAPITAL_VS_OPERATIONS", "Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue"

    # Tier 7: Legal Ghosts & Defunct Entities
    if row_id == "IN-082":
        return "TIER_7_LEGAL_GHOSTS_DEFUNCT", "Wirecard AG: Insolvent / bankrupt since June 2020; active commercial operations ceased"
    if row_id in ["IN-079", "IN-080", "IN-081", "IN-084"]:
        return "TIER_7_LEGAL_GHOSTS_DEFUNCT", f"Acquired / absorbed entity ({name}): absorbed into parent (UBS, Broadcom, Synopsys, Forvia)"
    if row_id in ["IN-068", "IN-069", "IN-070", "IN-071", "IN-072"]:
        if row_id == "IN-071":
            return "TIER_7_LEGAL_GHOSTS_DEFUNCT", "Old Spice: Consumer product brand owned by Procter & Gamble; no independent legal entity"
        elif row_id == "IN-069":
            return "TIER_7_LEGAL_GHOSTS_DEFUNCT", "Uber Eats: Commercial service brand of Uber Technologies, Inc."
        return "TIER_7_LEGAL_GHOSTS_DEFUNCT", "Trade brand / division requiring parent entity attribution"

    # Tier 8: Polysemic & Zero-Metadata Noise
    if row_id in ["IN-073", "IN-074", "IN-075", "IN-076", "IN-078"]:
        return "TIER_8_POLYSEMIC_AMBIGUITY", "Generic polysemic corporate name lacking disambiguating geographic/domain metadata"

    # Tier 9: Public Sector & Non-Commercial Utilities
    if row_id in ["IN-043", "IN-044", "IN-045", "IN-046", "IN-047", "IN-048"]:
        return "TIER_9_PUBLIC_SECTOR_UTILITIES", "Public authority, healthcare trust, or municipal utility funded by public budget/tariffs"

    # Tier 1 Financial Institutions
    if row_id in ["IN-031", "IN-032", "IN-033", "IN-034", "IN-035"]:
        return "TIER_1_PUBLIC_BENCHMARK", "Regulated banking / mutual insurance institution (operating income / NII metrics)"

    # Fallback
    return "TIER_1_PUBLIC_BENCHMARK", "Standard commercial enterprise"

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
            
    print(f"Loaded {len(rows)} licensee rows from {INPUT_CSV}\n")
    
    tier_counts = defaultdict(int)
    classified_records = []
    grouped_by_tier = defaultdict(list)
    
    for r in rows:
        row_id = r["id"]
        name = r["licensee_name"]
        addr = r["address"]
        country = r["country"]
        web = r["website"]
        
        tier_key, notes = classify_licensee(row_id, name, addr, country, web)
        tier_info = ARCHETYPES_DEF[tier_key]
        
        record = {
            "id": row_id,
            "licensee_name": name,
            "input_address": addr,
            "input_country": country,
            "input_website": web,
            "tier_key": tier_key,
            "tier_name": tier_info["tier"],
            "archetype": tier_info["archetype"],
            "observational_barrier": tier_info["barrier"],
            "proxy_strategy": tier_info["proxy_strategy"],
            "commercial_risk": tier_info["commercial_risk"],
            "classification_notes": notes
        }
        
        classified_records.append(record)
        tier_counts[tier_key] += 1
        grouped_by_tier[tier_key].append(record)

    # 1. Write Classified CSV
    fieldnames = list(classified_records[0].keys())
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classified_records)
    print(f"Saved enriched classification to: {OUTPUT_CSV}")

    # 2. Write JSON structure
    json_export = {
        "metadata": {
            "total_licensees": len(rows),
            "tier_distribution": dict(tier_counts)
        },
        "archetype_definitions": ARCHETYPES_DEF,
        "grouped_entities": {
            tier_key: {
                "metadata": ARCHETYPES_DEF[tier_key],
                "count": len(items),
                "entities": items
            }
            for tier_key, items in grouped_by_tier.items()
        }
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_export, f, indent=2)
    print(f"Saved JSON database to: {OUTPUT_JSON}")

    # 3. Write Markdown Summary
    md_lines = [
        "# Licensee Base Stratification & Archetype Taxonomy",
        f"**Source Dataset:** `licensee_list.csv` ({len(rows)} licensees)  ",
        "**Governing ADR:** [DEC-004: Information Asymmetry Lens](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-004-stratification-framework-the-information-asymmetry-lens)  \n",
        "---",
        "## Executive Summary: Distribution Across Tiers\n",
        "| Tier Code | Archetype & Observational Tier | Count | Representative Sample Entity | Primary Estimation Proxy |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    # Priority sample representatives for each tier
    rep_map = {
        "TIER_1_PUBLIC_BENCHMARK": "IN-028: WK Kellogg Co / IN-030: Banca Transilvania",
        "TIER_2_TAX_TRANSFER_DISTORTION": "IN-015: Google Ireland Limited / IN-016: Yazaki Romania",
        "TIER_3_REGULATORY_EXEMPTION": "IN-061: MARGOT BAKERY LIMITED / IN-065: Tischlerei Thunemann",
        "TIER_4_STRATEGIC_SECRECY": "IN-094: Rolex SA / IN-093: MSC",
        "TIER_5_VELOCITY_DISTORTION": "IN-056: Anysphere (Cursor) / IN-053: Mistral AI",
        "TIER_6_CAPITAL_VS_OPERATIONS": "IN-086: STEYN HOLDING S.A., SPF",
        "TIER_7_LEGAL_GHOSTS_DEFUNCT": "IN-071: Old Spice (Brand) / IN-082: Wirecard (Insolvent)",
        "TIER_8_POLYSEMIC_AMBIGUITY": "IN-075: Apex Group",
        "TIER_9_PUBLIC_SECTOR_UTILITIES": "IN-046: NHS Greater Glasgow / IN-044: TfL",
        "TIER_10_SPINOFFS_MAZE": "IN-002: SIEMENS HEALTHINEERS / IN-007: Siemens Energy"
    }

    for tier_key, info in ARCHETYPES_DEF.items():
        count = tier_counts[tier_key]
        rep = rep_map.get(tier_key, "N/A")
        md_lines.append(f"| `{tier_key}` | **{info['archetype']}** | {count} | {rep} | {info['proxy_strategy'][:60]}... |")

    md_lines.extend(["\n---", "## Detailed Archetype Breakdowns\n"])

    for tier_key, info in ARCHETYPES_DEF.items():
        items = grouped_by_tier[tier_key]
        md_lines.extend([
            f"### {info['tier']}",
            f"**Archetype:** {info['archetype']}  ",
            f"**Population in List:** {len(items)} companies  ",
            f"**The Observational Barrier:** {info['barrier']}  ",
            f"**Defensible Proxy Strategy:** {info['proxy_strategy']}  ",
            f"**Commercial Software Pricing Risk:** {info['commercial_risk']}  \n",
            "**Member Licensees:**",
            "| ID | Name | Country | Input Address / Notes |",
            "| :--- | :--- | :--- | :--- |"
        ])
        for it in items:
            loc = it["input_address"] or it["input_country"] or "Missing"
            md_lines.append(f"| {it['id']} | **{it['licensee_name']}** | {it['input_country'] or 'N/A'} | {it['classification_notes']} |")
        md_lines.append("\n")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Saved Markdown report to: {OUTPUT_MD}\n")

    # Print Terminal Overview
    print("="*80)
    print("STRATIFIED ARCHETYPE DISTRIBUTION (N=100)")
    print("="*80)
    for tier_key, info in ARCHETYPES_DEF.items():
        count = tier_counts[tier_key]
        print(f"[{count:2d} rows] {info['tier']}")
        print(f"          Archetype: {info['archetype']}")
        print(f"          Risk:      {info['commercial_risk'][:75]}...")
    print("="*80)

if __name__ == "__main__":
    main()
