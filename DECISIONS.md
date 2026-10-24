# Project Decision Log (ADR System)
**Project:** Veridion - Numbers Nobody Publishes (Economic Data Scientist Task)  
**Maintained by:** Data Science & Research Team  
**Governing Skill:** [.agents/skills/decision-logger/SKILL.md](file:///d:/Proiect%20Veridion/.agents/skills/decision-logger/SKILL.md)

---

## Index of Decisions

| ID | Title | Date | Status | Phase |
| :--- | :--- | :--- | :--- | :--- |
| [DEC-001](#dec-001-sampling-strategy-stratified-adversarial-sampling) | Sampling Strategy: Stratified Adversarial Sampling vs. Random Sampling | 2026-10-23 | ACCEPTED | Part 1: The Match |
| [DEC-002](#dec-002-estimation-methodology-the-detective-route-bottom-up-proxies) | Estimation Route: Detective (Bottom-up Proxies) vs. Quant Route | 2026-10-23 | ACCEPTED | Part 2: The Estimate |
| [DEC-003](#dec-003-automated-decision-logging-adr-governance) | Automated Decision Logging & ADR Governance | 2026-10-23 | ACCEPTED | Project Governance |
| [DEC-004](#dec-004-stratification-framework-the-information-asymmetry-lens) | Stratification Framework: The Information Asymmetry Lens | 2026-10-23 | ACCEPTED | Part 1: Sampling & Match |
| [DEC-005](#dec-005-evidence-harvesting-primary-statutory-apis-vs-commercial-aggregators) | Evidence Harvesting: Primary Statutory APIs vs. Commercial Aggregators | 2026-10-23 | ACCEPTED | Part 1: Evidence Harvesting |
| [DEC-006](#dec-006-proxy-estimation-framework--deliverable-schema-the-detective-triad) | Proxy Estimation Framework & Deliverable Schema (The Detective Triad) | 2026-10-24 | ACCEPTED | Part 2: The Estimate |
| [DEC-007](#dec-007-part-5-romanian-register-scalability-check) | Register Scalability & Living Entity Definition (Part 5) | 2026-10-24 | ACCEPTED | Part 5: The Register |

---

### [DEC-001] Sampling Strategy: Stratified Adversarial Sampling
- **Date & Phase:** 2026-10-23 | Part 1: The Match
- **Status:** ACCEPTED
- **Context & Problem Statement:** The client provided 100 messy licensee names in `licensee_list.csv`. We must select an evaluation sample to prove whether revenue and headcount can be built defensibly.
- **Decision Taken:** Implement **Stratified Adversarial Sampling** (12–15 entities) targeting 10 distinct corporate archetypes (corporate spin-offs, subsidiaries, brands without legal entity, bankrupt/zombie firms, secretive private giants, tax-haven wealth shells, VC-backed tech startups, and local craftsmen).
- **Alternatives Considered & Discarded:**
  - *Simple Random Sampling:* Rejected. Due to extreme corporate skewness, random selection risks picking mostly simple listed firms (where 10-K filings exist) or clustered duplicates, hiding the failure modes of the pipeline.
  - *Evaluating all 100 rows:* Rejected. High risk of superficial/shallow matching ("googled it") without defensible derivation chains.
- **Rationale & Evidence:** The prompt explicitly states: *"A small sample chosen to be difficult teaches us more than a large one chosen to be finishable."* Edge cases test the boundaries of data defensibility.
- **Assumptions & Downstream Impact:**
  - Provides a high-stress testbed for both entity resolution and proxy modeling.
  - Feeds directly into the README Part 1 ("why this sample").

---

### [DEC-002] Estimation Methodology: The Detective Route (Bottom-up Proxies)
- **Date & Phase:** 2026-10-23 | Part 2: The Estimate
- **Status:** ACCEPTED
- **Context & Problem Statement:** Part 2 mandates choosing exactly one route: the Detective Route (bottom-up proxies per company) or the Quant Route (ML model trained on Romanian open data `data.gov.ro`).
- **Decision Taken:** Choose **The Detective Route**.
- **Alternatives Considered & Discarded:**
  - *The Quant Route:* Rejected for the sample estimation. While statistically clean for Romanian filings, predicting global multinational entities (e.g., San Francisco tech startups or London bakeries) based solely on Romanian CAEN regression introduces severe geographic and macroeconomic mismatch that is harder to defend in front of a commercial auditor across the table.
- **Rationale & Evidence:** Veridion's commercial core value is finding and defending indirect proxies where no public registry exists. The Detective Route allows building custom, defensible derivations (headcount-to-revenue benchmarks, location multipliers, fleet sizing, licensing bounds) with explicit uncertainty ranges.
- **Downstream Impact:**
  - The Romanian open data will still be utilized rigorously in **Part 5 (The Register)** to assess scalability across 4M+ companies.

---

### [DEC-003] Automated Decision Logging & ADR Governance
- **Date & Phase:** 2026-10-23 | Project Governance
- **Status:** ACCEPTED
- **Context & Problem Statement:** Every step and proxy needs an auditable trail so that client analysts can trace derivations and understand discarded dead ends.
- **Decision Taken:** Created a specialized skill `decision-logger` in [.agents/skills/decision-logger/SKILL.md](file:///d:/Proiect%20Veridion/.agents/skills/decision-logger/SKILL.md) and established [DECISIONS.md](file:///d:/Proiect%20Veridion/DECISIONS.md) as the single source of truth for architectural, methodological, and data decisions.
- **Downstream Impact:** Directly powers the final project *Cut List* and documentation integrity.

---

### [DEC-004] Stratification Framework: The Information Asymmetry Lens
- **Date & Phase:** 2026-10-23 | Part 1: Sampling & Match
- **Status:** ACCEPTED
- **Context & Problem Statement:** The sample must be categorized in a way that reveals scalable data acquisition and estimation patterns rather than arbitrary industry groupings.
- **Decision Taken:** Adopt **Option A (The Information Asymmetry Lens)** covering 7 distinct tiers of observational barriers, selecting 11 representative entities:
  1. *Tier 1 (Public Ground Truth Calibration):* `IN-028` WK Kellogg Co & `IN-030` Banca Transilvania S.A.
  2. *Tier 2 (Tax & Transfer Pricing Distortion):* `IN-015` Google Ireland Limited & `IN-016` Yazaki Romania S.R.L.
  3. *Tier 3 (Regulatory Filing Exemptions - Micro SME):* `IN-061` MARGOT BAKERY LIMITED & `IN-065` Tischlerei Thunemann KG.
  4. *Tier 4 (Strategic Secrecy - Private Titans):* `IN-094` Rolex SA.
  5. *Tier 5 (Velocity Distortion - High Growth AI):* `IN-056` Anysphere (makers of Cursor).
  6. *Tier 6 (Capital vs Operations - Wealth Shell SPF):* `IN-086` STEYN HOLDING S.A., SPF.
  7. *Tier 7 (Legal Ghosts, Defunct & Polysemic):* `IN-071` Old Spice (Brand only), `IN-082` Wirecard AG (Insolvent), `IN-075` Apex Group (Polysemic unresolvable).
- **Alternatives Considered & Discarded:**
  - *Option B (Commercial Arbitrage exclusively):* Retained as a secondary business analysis layer (connecting data opacity directly to contract pricing risk), but not as the primary sampling partition.
  - *Option C (Pairwise Stress Test):* Discarded as standalone; pairwise contrasts (e.g., Google Ireland vs Yazaki Romania) are subsumed inside Tier 2.
- **Rationale & Evidence:** Veridion's technical core competence is overcoming opacity barriers. Grouping by observational mechanisms tests the exact boundary where algorithmic retrieval works versus where specialized physical/unit-economic proxies are mandatory.
- **Assumptions & Downstream Impact:**
  - Governs Part 1 Match Table and Part 2 Proxy Derivations.
  - Feeds the final Cut List by documenting why standalone sector classification was abandoned.

---

### [DEC-005] Evidence Harvesting: Primary Statutory APIs vs. Commercial Aggregators
- **Date & Phase:** 2026-10-23 | Part 1: Evidence Harvesting & Verification
- **Status:** ACCEPTED
- **Context & Problem Statement:** To verify matched entities and extract auditable financials, we must decide whether to scrape third-party commercial aggregators (e.g. ListaFirme.ro in Romania, Endole in the UK, North Data in Germany, Pappers in France, ZoomInfo in the US) or query primary statutory government registers directly.
- **Decision Taken:** Build a multi-jurisdiction Evidence Harvester (`scripts/harvest_company_evidence.py`) that queries primary government and regulatory APIs directly:
  1. *United States:* SEC EDGAR REST API (Form 10-K audited XBRL facts for listed entities & parents)
  2. *United Kingdom:* UK Companies House Service API (`service.gov.uk` statutory filing history and micro-entity exemptions)
  3. *Romania:* ANAF v9 REST Web Service (`webservicesp.anaf.ro`)
  4. *Switzerland:* Federal Commercial Registry ZEFIX REST API (`zefix.ch`)
  5. *Germany:* Official Register Portal (`handelsregister.de`) & statutory Impressum disclosures (§ 5 TMG)
- **Alternatives Considered & Discarded:**
  - *Scraping Commercial Aggregators (ListaFirme, North Data, Pappers):* Rejected and discarded. Live testing proved that commercial portals deploy aggressive Cloudflare anti-bot blocks (HTTP 403 / 429) and paywalls. Crucially, commercial aggregators fail commercial auditor interrogation because their modeled numbers suffer from 1–2 year reporting lags and uncalibrated industry guesses. **(Added to Cut List)**.
  - *Unstructured Web Search Scraping ("We Googled It"):* Rejected. Explicitly forbidden by the task prompt as indefensible across the table. **(Added to Cut List)**.
- **Rationale & Evidence:** Direct statutory government endpoints provide free, high-speed, legally binding data with exact timestamps, official registration numbers (CIK, CoNo, CUI, CHE, HRB), and verifiable filing categories.
- **Assumptions & Downstream Impact:**
  - Generates verifiable evidence dossiers in `data/evidence_dossiers/`.
  - Directly powers the Part 1 Match & Resolution table and populates the required submission Cut List.

---

### [DEC-006] Proxy Estimation Framework & Deliverable Schema (The Detective Triad)
- **Date & Phase:** 2026-10-24 | Part 2: The Estimate
- **Status:** ACCEPTED
- **Context & Problem Statement:** The client's prompt mandates: *"The client's analyst will interrogate every figure. A number alone rarely survives that interrogation. Deciding what must travel with each figure for it to stand in that meeting is part of the work... Each value carries the reasoning that produced it, written so we can disagree with it, and an answer to: how wrong could this be?"*
- **Decision Taken:** Implement a **Defensibility Quadruplet Schema** for every sample row:
  1. **Dual Metric Structure:** Report both statutory/modeled turnover AND honest operational sizing metric (e.g. for transfer-pricing billing hubs, report both booked turnover and local active headcount to prevent catastrophic software overbilling).
  2. **Asymmetric Uncertainty Bounds:** Deliver `[Min_Bound, Best_Estimate, Max_Bound]` reflecting structural opacity rather than symmetric arbitrary percentages.
  3. **Explicit Falsification Condition ("How Wrong Could This Be?"):** Every figure explicitly specifies the sensitivity boundary (e.g. seasonal variance, price elasticity, subcontractor dilution).
  4. **Scalability Index & Reproducibility Tier:** Categorize how many firms across the global economy carry the proxy (e.g., COSC watch movements: <15 firms; transaction-density retail proxies: ~2.5M firms; SEC EDGAR XBRL: ~10k firms).
- **Alternatives Considered & Discarded:**
  - *Single Point Estimates (e.g. "Revenue: $40M"):* Rejected. Fails client auditor interrogation; conceals modeling risk.
  - *Standard ±15% Symmetric Error Bands:* Rejected as statistically fraudulent. A micro-bakery or an AI hyper-growth startup does not have symmetric error; a startup's upside error can be +300% while its downside is limited by cash runway. **(Added to Cut List)**.
  - *Imputing unresolvable entities (guessing Apex Group):* Rejected. Explicitly classified as `UNRESOLVABLE` to preserve data integrity.
- **Rationale & Evidence:** An honest gap is an auditable finding; an ungrounded guess destroys commercial trust.
- **Assumptions & Downstream Impact:**
  - Direct schema contract for `client_deliverable_licensee_estimates.csv`.
  - Directly feeds Part 2 of README.

---

### [DEC-007] Part 5: Romanian Register Scalability & Living Entity Definition
- **Date & Phase:** 2026-10-24 | Part 5: The Register
- **Status:** ACCEPTED
- **Context & Problem Statement:** To evaluate scalability of our proxy across the complete Romanian register (`OD_FIRME.csv`, 4,116,356 historical entries), we must separate the living from the dead in one line, map our best proxy to the register, and report the 3 mandatory numbers.
- **Decision Taken:**
  1. *Living Entity Separation Rule:* Defined as: *"A company is classified as living if its unique statutory fiscal code (CUI) submitted active annual accounts for fiscal year 2024 in the Ministry of Finance registry (`web_uu_an2024`), separating operating commercial entities from historical dissolved partnerships, struck-off entities, and defunct shells."*
  2. *Best Proxy Selection:* Mapped the **Physical Unit-Economic Capacity & Footprint Proxy** across consumer-facing retail, automotive workshops, and hospitality craft production (CAENs 4711, 4520, 5610, 5630, 1071, 9602, 1623, 3109).
  3. *Empirical Verification:*
     - Total registered: 4,116,356
     - Total living filers: 822,292 (19.98% of registry)
     - Inside proxy line: **108,115 companies**
     - Share of living register: **13.15%**
     - Top 3 industries: (1) CAEN 4711 Grocery Retail (38,668 / 35.8%), (2) CAEN 4520 Auto Repair Bays (16,637 / 15.4%), (3) CAEN 5610 Restaurants (15,680 / 14.5%).
- **Alternatives Considered & Discarded:**
  - *Assuming all 4.1M entities are active:* Rejected. Historical ONRC records contain 3.3M dissolved/struck-off sole proprietorships and liquidations since 1990.
  - *Scraping real-time ONRC web portals:* Rejected in favor of the full statutory open data snapshot.
- **Rationale & Evidence:** Proves that physical unit-economic proxies scale to over 100,000 active companies in a single mid-sized European economy.
- **Assumptions & Downstream Impact:**
  - Feeds directly into Part 5 of the README and populates the Cut List.




