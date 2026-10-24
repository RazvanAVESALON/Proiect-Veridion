# Licensee Base Stratification & Archetype Taxonomy
**Source Dataset:** `licensee_list.csv` (100 licensees)  
**Governing ADR:** [DEC-004: Information Asymmetry Lens](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-004-stratification-framework-the-information-asymmetry-lens)  

---
## Executive Summary: Distribution Across Tiers

| Tier Code | Archetype & Observational Tier | Count | Representative Sample Entity | Primary Estimation Proxy |
| :--- | :--- | :--- | :--- | :--- |
| `TIER_1_PUBLIC_BENCHMARK` | **Public Listed Corporations & Direct Filers** | 14 | IN-028: WK Kellogg Co / IN-030: Banca Transilvania | Direct registry extraction (SEC EDGAR, BVB, LSE). Used to ca... |
| `TIER_2_TAX_TRANSFER_DISTORTION` | **Foreign Operating & Billing Hubs vs Manufacturing Plants** | 10 | IN-015: Google Ireland Limited / IN-016: Yazaki Romania | Headcount-to-revenue divergence analysis. Cross-referencing ... |
| `TIER_3_REGULATORY_EXEMPTION` | **Micro-SMEs, Artisanal Bakeries & Local Craftsmen** | 13 | IN-061: MARGOT BAKERY LIMITED / IN-065: Tischlerei Thunemann | Unit-economics & physical footprint proxies: daily transacti... |
| `TIER_4_STRATEGIC_SECRECY` | **Ultra-Secretive Private Titans & Family Foundations** | 10 | IN-094: Rolex SA / IN-093: MSC | Physical capacity & output proxies: production unit certific... |
| `TIER_5_VELOCITY_DISTORTION` | **VC-Backed DeepTech, Defense Tech & AI Startups** | 11 | IN-056: Anysphere (Cursor) / IN-053: Mistral AI | Venture round valuation multiples, developer adoption veloci... |
| `TIER_6_CAPITAL_VS_OPERATIONS` | **Holding Vehicles, Wealth Management SPFs & Shells** | 8 | IN-086: STEYN HOLDING S.A., SPF | Statutory legal form identification (SPF, SICAV, Vermögensve... |
| `TIER_7_LEGAL_GHOSTS_DEFUNCT` | **Product Brands, Bankrupt Estates & M&A Carve-Outs** | 10 | IN-071: Old Spice (Brand) / IN-082: Wirecard (Insolvent) | Registry status verification (Amtsgericht insolvency decrees... |
| `TIER_8_POLYSEMIC_AMBIGUITY` | **Ambiguous Generic Names (Missing Country/Address)** | 5 | IN-075: Apex Group | Resolution Threshold Rule: explicitly categorizing as 'Unres... |
| `TIER_9_PUBLIC_SECTOR_UTILITIES` | **Public Health Trusts, Municipal Utilities & Authorities** | 6 | IN-046: NHS Greater Glasgow / IN-044: TfL | Public budget allocations, hospital bed count, passenger vol... |
| `TIER_10_SPINOFFS_MAZE` | **Corporate Spin-Offs, Separated Divisions & Subsidiaries** | 13 | IN-002: SIEMENS HEALTHINEERS / IN-007: Siemens Energy | Ownership stake & consolidation test: verify parent 10-K con... |

---
## Detailed Archetype Breakdowns

### Tier 1: Full Transparency (Public Ground Truth)
**Archetype:** Public Listed Corporations & Direct Filers  
**Population in List:** 14 companies  
**The Observational Barrier:** Minimal opacity. Audited Form 10-K, IFRS, or local exchange filings exist.  
**Defensible Proxy Strategy:** Direct registry extraction (SEC EDGAR, BVB, LSE). Used to calibrate proxy error baselines.  
**Commercial Software Pricing Risk:** Low entity ambiguity, but high risk of contract stagnation if historical seat pricing fails to track annual turnover growth.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-011 | **Fastenal Company** | N/A | Publicly listed enterprise with direct audited annual filings |
| IN-012 | **Tata Consultancy Services Limited** | IN | Publicly listed enterprise with direct audited annual filings |
| IN-013 | **Koc Holding A.S.** | TR | Publicly listed enterprise with direct audited annual filings |
| IN-014 | **Kakao Corp.** | KR | Publicly listed enterprise with direct audited annual filings |
| IN-025 | **Sandoz Group AG** | CH | Publicly listed enterprise with direct audited annual filings |
| IN-028 | **WK Kellogg Co** | US | WK Kellogg Co: 2023 spin-off from Kellogg Company, public listed (NYSE: KLG) |
| IN-030 | **Banca Transilvania S.A.** | RO | Publicly listed enterprise with direct audited annual filings |
| IN-031 | **Shinhan Bank** | KR | Regulated banking / mutual insurance institution (operating income / NII metrics) |
| IN-032 | **Credit Mutuel** | FR | Regulated banking / mutual insurance institution (operating income / NII metrics) |
| IN-033 | **LV=** | GB | Regulated banking / mutual insurance institution (operating income / NII metrics) |
| IN-034 | **HDI Global SE** | DE | Regulated banking / mutual insurance institution (operating income / NII metrics) |
| IN-035 | **The Wawanesa Mutual Insurance Company** | CA | Regulated banking / mutual insurance institution (operating income / NII metrics) |
| IN-037 | **EQT AB** | SE | Publicly listed enterprise with direct audited annual filings |
| IN-090 | **Arcos Dorados Holdings Inc.** | N/A | Arcos Dorados: Publicly listed McDonald's master franchisee (NYSE: ARCO) |


### Tier 2: Structural Distortions (Tax & Transfer Pricing Hubs)
**Archetype:** Foreign Operating & Billing Hubs vs Manufacturing Plants  
**Population in List:** 10 companies  
**The Observational Barrier:** Entity revenue is decoupled from local physical footprint. Brass-plate billing hubs show astronomical booked revenue; local assembly plants show massive headcount with low margins.  
**Defensible Proxy Strategy:** Headcount-to-revenue divergence analysis. Cross-referencing local CRO/ONRC registry filings with LinkedIn and physical site counts.  
**Commercial Software Pricing Risk:** Severe mispricing. Pricing on revenue overcharges billing hubs (5k staff booking €80B); pricing on headcount under-bills global software consumption.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-015 | **Google Ireland Limited** | IE | Google Ireland Limited: Primary EMEA billing & tax routing hub (~€86B turnover, ~4.9k employees) |
| IN-016 | **Yazaki Romania S.R.L.** | RO | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-017 | **Nestle Pakistan Limited** | PK | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-018 | **Unilever Nigeria Plc** | NG | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-019 | **IKEA Industry Slovakia s.r.o.** | SK | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-020 | **Cargill Agricultura S.R.L.** | RO | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-021 | **Toyota Kirloskar Motor Private Limited** | IN | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-022 | **Mercedes-Benz Romania S.R.L.** | RO | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-023 | **Toyota Motor Manufacturing (UK) Limited** | GB | Foreign manufacturing/distribution operating subsidiary of multinational group |
| IN-024 | **Coca-Cola HBC Romania S.R.L.** | RO | Foreign manufacturing/distribution operating subsidiary of multinational group |


### Tier 3: Regulatory Black Box (Filing Exemptions)
**Archetype:** Micro-SMEs, Artisanal Bakeries & Local Craftsmen  
**Population in List:** 13 companies  
**The Observational Barrier:** Statutory filing exemptions (UK Companies Act micro-entity rules, German §264a HGB for KG/UG). Balance sheets are abbreviated; Profit & Loss (turnover) is legally withheld.  
**Defensible Proxy Strategy:** Unit-economics & physical footprint proxies: daily transactions, oven/table capacity, storefront locations, guild/chamber registrations.  
**Commercial Software Pricing Risk:** Overcharging & customer churn. Automated models applying industry-average revenues overbill 6-person local workshops.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-060 | **OLIVIER'S BAKERY LTD** | GB | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-061 | **MARGOT BAKERY LIMITED** | GB | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-062 | **ZAITUN BAKERY LTD** | GB | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-063 | **ALIN PANIFICATIE S.R.L.** | RO | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-064 | **PANIFICATIE MOLDOVA SRL** | N/A | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-065 | **Tischlerei Thunemann KG** | DE | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-066 | **Tischlerei Moller e.K.** | DE | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-067 | **Gunter Buchbender Tischlerei** | DE | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-077 | **Tischlerei Rose UG** | DE | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-083 | **LEVE BAKERY LTD** | GB | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-087 | **BAKERY BAKERY LTD** | GB | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-088 | **PANIFICATIE STRAJA S.R.L.** | RO | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |
| IN-089 | **Tischlerei Holtzum UG** | DE | Micro-SME / craft enterprise qualifying for statutory balance sheet & P&L filing exemptions |


### Tier 4: Strategic Secrecy (Private Conglomerates & Family Trusts)
**Archetype:** Ultra-Secretive Private Titans & Family Foundations  
**Population in List:** 10 companies  
**The Observational Barrier:** Privately owned by foundations (e.g. Hans Wilsdorf) or private LLCs with no public stock filings.  
**Defensible Proxy Strategy:** Physical capacity & output proxies: production unit certifications (COSC watch movements), container fleet TEU capacity, logistics warehouse sqft.  
**Commercial Software Pricing Risk:** Massive revenue leakage. Multi-billion luxury or shipping giants paying standard private-company enterprise fees.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-091 | **Ace Hardware Corporation** | US | Large private/family conglomerate with no public equity disclosure |
| IN-092 | **REWE Group** | DE | Large private/family conglomerate with no public equity disclosure |
| IN-093 | **MSC Mediterranean Shipping Company S.A.** | CH | MSC: Family-owned Swiss shipping titan; estimated via TEU fleet capacity |
| IN-094 | **Rolex SA** | CH | Rolex SA: 100% owned by Hans Wilsdorf Foundation; zero public P&L; estimated via COSC production |
| IN-095 | **Uline, Inc.** | US | Large private/family conglomerate with no public equity disclosure |
| IN-096 | **Southern Glazer's Wine & Spirits, LLC** | US | Large private/family conglomerate with no public equity disclosure |
| IN-097 | **Reyes Holdings, L.L.C.** | US | Large private/family conglomerate with no public equity disclosure |
| IN-098 | **Prime Healthcare Services, Inc.** | US | Large private/family conglomerate with no public equity disclosure |
| IN-099 | **Drury Hotels Company, LLC** | US | Large private/family conglomerate with no public equity disclosure |
| IN-100 | **Perdue Farms Inc.** | US | Large private/family conglomerate with no public equity disclosure |


### Tier 5: High Velocity (Hyper-Growth AI & Venture Startups)
**Archetype:** VC-Backed DeepTech, Defense Tech & AI Startups  
**Population in List:** 11 companies  
**The Observational Barrier:** Historic corporate filings (if any) are obsolete in 90 days. Headcount is lean (20-100 staff), but ARR scales exponentially from $0 to $100M+.  
**Defensible Proxy Strategy:** Venture round valuation multiples, developer adoption velocity, GitHub traction, and enterprise seat deployment tracking.  
**Commercial Software Pricing Risk:** Severe under-pricing. Vendor charges small-team tier ($5k/yr) while client raises billions and deploys product to thousands of end-users.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-049 | **Blue Origin** | US | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-050 | **Anduril Industries, Inc.** | US | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-051 | **Sierra Space Corporation** | US | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-052 | **Helsing** | DE | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-053 | **Mistral AI** | FR | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-054 | **DRUID AI** | RO | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-055 | **FintechOS** | RO | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-056 | **Anysphere** | US | Anysphere (Cursor): Rapid ARR growth ($100M+ ARR), venture-backed Delaware C-Corp |
| IN-057 | **Isar Aerospace** | DE | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-058 | **Tekever** | PT | High-growth venture-backed tech / defense startup with private unfiled accounts |
| IN-059 | **Lovable** | SE | High-growth venture-backed tech / defense startup with private unfiled accounts |


### Tier 6: Capital vs. Operations Illusion (Three People & a Mailbox)
**Archetype:** Holding Vehicles, Wealth Management SPFs & Shells  
**Population in List:** 8 companies  
**The Observational Barrier:** Société de Gestion de Patrimoine Familial (Luxembourg SPF) or pure asset holding vehicles. Balance sheet assets exceed hundreds of millions, but commercial revenue and operating staff are near zero.  
**Defensible Proxy Strategy:** Statutory legal form identification (SPF, SICAV, Vermögensverwaltung). Discarding balance sheet equity as an operating proxy.  
**Commercial Software Pricing Risk:** Lost negotiations. Vendor attempts enterprise pricing on balance sheet scale to an entity requiring only 2 administrative licenses.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-036 | **Baillie Gifford & Co** | GB | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-038 | **Ferd AS** | NO | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-039 | **Temasek Holdings (Private) Limited** | SG | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-040 | **Bregal Investments** | N/A | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-041 | **Goodman Group** | AU | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-042 | **P3 Logistic Parks** | N/A | Private Equity, Sovereign Wealth, or Asset Manager: metrics driven by AUM rather than commercial revenue |
| IN-085 | **MIDGARD HOLDING** | LU | Luxembourg SPF / Wealth Holding vehicle: substantial assets, 0 operational headcount, €0 commercial turnover |
| IN-086 | **STEYN HOLDING S.A., SPF** | LU | Luxembourg SPF / Wealth Holding vehicle: substantial assets, 0 operational headcount, €0 commercial turnover |


### Tier 7: Legal Ghosts & Defunct Entities
**Archetype:** Product Brands, Bankrupt Estates & M&A Carve-Outs  
**Population in List:** 10 companies  
**The Observational Barrier:** The entity on the contract is either a marketing trade brand (no legal entity), an insolvent estate, or an entity dissolved through emergency acquisition.  
**Defensible Proxy Strategy:** Registry status verification (Amtsgericht insolvency decrees, commercial register dissolution, parent brand attribution rules).  
**Commercial Software Pricing Risk:** Legal unenforceability & bad debt write-offs. Software runs for defunct or dissolved entities where licenses cannot be legally recovered.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-068 | **DEGIRO** | NL | Trade brand / division requiring parent entity attribution |
| IN-069 | **Uber Eats** | N/A | Uber Eats: Commercial service brand of Uber Technologies, Inc. |
| IN-070 | **Nespresso** | CH | Trade brand / division requiring parent entity attribution |
| IN-071 | **Old Spice** | US | Old Spice: Consumer product brand owned by Procter & Gamble; no independent legal entity |
| IN-072 | **Currys PC World** | GB | Trade brand / division requiring parent entity attribution |
| IN-079 | **Credit Suisse AG** | CH | Acquired / absorbed entity (Credit Suisse AG): absorbed into parent (UBS, Broadcom, Synopsys, Forvia) |
| IN-080 | **VMware, Inc.** | US | Acquired / absorbed entity (VMware, Inc.): absorbed into parent (UBS, Broadcom, Synopsys, Forvia) |
| IN-081 | **ANSYS, Inc.** | US | Acquired / absorbed entity (ANSYS, Inc.): absorbed into parent (UBS, Broadcom, Synopsys, Forvia) |
| IN-082 | **Wirecard AG** | DE | Wirecard AG: Insolvent / bankrupt since June 2020; active commercial operations ceased |
| IN-084 | **HELLA GmbH & Co. KGaA** | DE | Acquired / absorbed entity (HELLA GmbH & Co. KGaA): absorbed into parent (UBS, Broadcom, Synopsys, Forvia) |


### Tier 8: Polysemic & Zero-Metadata Noise
**Archetype:** Ambiguous Generic Names (Missing Country/Address)  
**Population in List:** 5 companies  
**The Observational Barrier:** Generic corporate names (e.g. 'Apex Group', 'Meridian') with missing geographic and digital breadcrumbs.  
**Defensible Proxy Strategy:** Resolution Threshold Rule: explicitly categorizing as 'Unresolvable: Insufficient Disambiguation Signals' to prevent false-positive matching.  
**Commercial Software Pricing Risk:** Catastrophic misattribution. Conflating a local shipping agency with a multi-billion dollar hedge fund.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-073 | **Phoenix Group** | N/A | Generic polysemic corporate name lacking disambiguating geographic/domain metadata |
| IN-074 | **Orion Corporation** | N/A | Generic polysemic corporate name lacking disambiguating geographic/domain metadata |
| IN-075 | **Apex Group** | N/A | Generic polysemic corporate name lacking disambiguating geographic/domain metadata |
| IN-076 | **National Grid** | N/A | Generic polysemic corporate name lacking disambiguating geographic/domain metadata |
| IN-078 | **Meridian** | N/A | Generic polysemic corporate name lacking disambiguating geographic/domain metadata |


### Tier 9: Non-Commercial & Regulated Public Institutions
**Archetype:** Public Health Trusts, Municipal Utilities & Authorities  
**Population in List:** 6 companies  
**The Observational Barrier:** Non-commercial accounting. Revenue corresponds to tax appropriations, farebox tariffs, or statutory grants, not competitive market sales.  
**Defensible Proxy Strategy:** Public budget allocations, hospital bed count, passenger volume, municipal operating reports.  
**Commercial Software Pricing Risk:** Budget freeze / procurement failure. Public sector compliance requires bespoke licensing independent of commercial ARR models.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-043 | **HUS Group** | FI | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |
| IN-044 | **Transport for London** | GB | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |
| IN-045 | **Stadtwerke Muenchen GmbH** | DE | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |
| IN-046 | **NHS Greater Glasgow and Clyde** | GB | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |
| IN-047 | **Port Authority of New York and New Jersey** | US | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |
| IN-048 | **Institut Pasteur** | FR | Public authority, healthcare trust, or municipal utility funded by public budget/tariffs |


### Tier 10: The Conglomerate Matrix & Carve-Outs
**Archetype:** Corporate Spin-Offs, Separated Divisions & Subsidiaries  
**Population in List:** 13 companies  
**The Observational Barrier:** Independent public listing while retaining parent naming heritage (e.g. Siemens Healthineers, Siemens Energy).  
**Defensible Proxy Strategy:** Ownership stake & consolidation test: verify parent 10-K consolidation (>50% vs deconsolidated public spin-offs).  
**Commercial Software Pricing Risk:** Contract arbitrage. Spun-off multi-billion standalone entities sharing licenses under parent conglomerate umbrella discounts.  

**Member Licensees:**
| ID | Name | Country | Input Address / Notes |
| :--- | :--- | :--- | :--- |
| IN-001 | **Siemens S.A. de C.V.** | MX | Regional operating subsidiary of Siemens AG conglomerate |
| IN-002 | **SIEMENS HEALTHINEERS** | N/A | IN-002: Standalone public medical spin-off (majority Siemens AG owned) |
| IN-003 | **Siemens Industry Software (Shanghai) Co., Ltd.** | CN | Operating division / wholly owned industrial subsidiary |
| IN-004 | **Siemens Ltd.** | N/A | Regional operating subsidiary of Siemens AG conglomerate |
| IN-005 | **SIEMENS MOBILITY LIMITED** | GB | Operating division / wholly owned industrial subsidiary |
| IN-006 | **Siemens Ltda.** | BR | Regional operating subsidiary of Siemens AG conglomerate |
| IN-007 | **Siemens Energy** | N/A | IN-007/008: Deconsolidated energy spin-off (standalone DAX company) |
| IN-008 | **Siemens Gamesa Renewable Energy, S.A.** | ES | IN-007/008: Deconsolidated energy spin-off (standalone DAX company) |
| IN-009 | **SIEMENS PTE. LTD.** | SG | Regional operating subsidiary of Siemens AG conglomerate |
| IN-010 | **Siemens Canada Limited** | CA | Regional operating subsidiary of Siemens AG conglomerate |
| IN-026 | **Solstice Advanced Materials** | US | Solstice Advanced Materials: Public corporate carve-out / spin-off |
| IN-027 | **Amentum Holdings, Inc.** | US | Amentum Holdings, Inc.: Public corporate carve-out / spin-off |
| IN-029 | **Qnity Electronics, Inc.** | US | Qnity Electronics, Inc.: Public corporate carve-out / spin-off |

