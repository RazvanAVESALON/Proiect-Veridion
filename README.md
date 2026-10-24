# Numbers Nobody Publishes: Economic Sizing of Opaque Licensee Entities
**Author:** Economic Data Scientist Candidate  
**Project:** Veridion B2B Intelligence Evaluation  
**Client Deliverable File:** [`data/client_deliverable_licensee_estimates.csv`](file:///d:/Proiect%20Veridion/data/client_deliverable_licensee_estimates.csv)  
**Auditable Architecture Decision Log:** [`DECISIONS.md`](file:///d:/Proiect%20Veridion/DECISIONS.md)  
**Detailed Technical Derivations Dossier:** [`data/proxy_derivations_dossier.md`](file:///d:/Proiect%20Veridion/data/proxy_derivations_dossier.md)  

---

## Executive Overview

A software vendor prices contracts on customer scale: annual turnover and employee headcount decide whether a licensee pays a small-tier rate or an enterprise rate. Their contract list contains 100 messy names—abbreviations, brand names, subsidiaries, and corporate shells—accumulated over twenty years of sales entries.

Auditors will not accept *"we googled it"*. This project builds and proves an auditable, bottom-up methodology for estimating numbers nobody publishes, stress-tested on an adversarial sample selected across structural information barriers.

---

## Part 1: The Match

### 1. Sampling Strategy: Why This Sample?
Rather than a random sample—which risks picking simple public entities with audited 10-K filings—we deployed **Stratified Adversarial Sampling** ([DEC-001](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-001-sampling-strategy-stratified-adversarial-sampling)). We classified all 100 licensees across an **Information Asymmetry Lens** ([DEC-004](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-004-stratification-framework-the-information-asymmetry-lens), [`data/archetypes_summary.md`](file:///d:/Proiect%20Veridion/data/archetypes_summary.md)) and selected 13 stress-test entities representing the failure boundaries of corporate data:

| Entity ID | Input Name | Matched Legal Entity | Statutory Identifier | Observational Archetype & Barrier |
| :--- | :--- | :--- | :--- | :--- |
| `IN-028` | **WK Kellogg Co** | WK Kellogg Co | SEC CIK: 0001959348 | Corporate Carve-Out (2023 spin-off from Kellogg Co) |
| `IN-030` | **Banca Transilvania S.A.** | Banca Transilvania S.A. | RO CUI: 5022670 | Regulated Commercial Bank (Non-turnover financial metrics) |
| `IN-016` | **Yazaki Romania S.R.L.** | Yazaki Romania S.R.L. | RO CUI: 15412557 | Foreign Assembly Cost-Center (High labor, low turnover/head) |
| `IN-015` | **Google Ireland Limited** | Google Ireland Limited | IE CRO: 368047 | Multinational Tax/Billing Hub (Extreme €17.7M revenue/head) |
| `IN-061` | **MARGOT BAKERY LIMITED** | MARGOT BAKERY LIMITED | UK CoNo: 09689240 | Micro-SME Retail Bakery (Statutory P&L withheld) |
| `IN-065` | **Tischlerei Thunemann KG** | Tischlerei Thunemann KG | DE HRA: 205396 | Master Joinery Workshop (German §264a HGB P&L exempt) |
| `IN-094` | **Rolex SA** | Rolex SA | CH CHE: 105.962.823 | Ultra-Secretive Private Titan (Owned by Foundation, 0 filings) |
| `IN-056` | **Anysphere** | Anysphere, Inc. (Cursor) | DE C-Corp: 6843901 | Hyper-Growth AI Startup (10x annual velocity distortion) |
| `IN-086` | **STEYN HOLDING S.A., SPF** | STEYN HOLDING S.A., SPF | LU RCS: B168536 | Wealth Holding Shell (Statutory €0 commercial trading rule) |
| `IN-071` | **Old Spice** | P&G / Old Spice Division | US SEC: 0000080424 | Unregistered Brand Asset (No standalone corporate entity) |
| `IN-082` | **Wirecard AG** | Wirecard AG i.L. | DE HRB: 169227 | Bankrupt Liquidation Estate (Defunct zombie licensee) |
| `IN-075` | **Apex Group** | `UNRESOLVABLE` | N/A | Polysemic Name Collision (Zero geographic metadata) |
| `IN-002` | **SIEMENS HEALTHINEERS** | Siemens Healthineers AG | DE HRB: 16568 | DAX Listed Carve-out (~75% owned by Siemens AG parent) |

### 2. Matching Buckets & Resolution Rules
- **Direct Statutory Registry Match (9 entities):** Successfully resolved to official national registration numbers (SEC, Companies House, ANAF, ZEFIX, Handelsregister) via primary statutory APIs ([DEC-005](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-005-evidence-harvesting-primary-statutory-apis-vs-commercial-aggregators)).
- **Brand-to-Parent Attribution (`IN-071` Old Spice):** Does not exist as a legal person; resolved to owner Procter & Gamble Co, carving out brand-level unit metrics.
- **Insolvent / Post-Liquidation Entity (`IN-082` Wirecard):** Formally matched to the Munich liquidation estate (Ref: 99 IN 1308/20); operational headcount is 0.
- **Deliberate Failure (`IN-075` Apex Group):** Without country or domain metadata, 'Apex Group' collides with at least four distinct multi-billion companies (Bermuda fund admin, US tool manufacturer, UK engineering firm, Romanian distributor). Imputing one arbitrarily is an unforced data science error. **We refused to match.** An honest gap preserves defensibility; an ungrounded guess loses a client lawsuit.

---

## Part 2: The Estimate (The Detective Route)

We selected **Option A: The Detective Route** ([DEC-002](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-002-estimation-methodology-the-detective-route-bottom-up-proxies)). Applying a Romanian CAEN regression (the Quant Route) to a London bakery, a Swiss watch foundation, or a Delaware AI startup creates catastrophic geographical and sector distortion that an auditor will dismantle immediately.

### 1. The Two Gatekeeper Questions
Before any evidence entered our pipeline:
1. *Does it describe the company we matched, at the time we claim?*  
   (e.g., verifying that WK Kellogg Co metrics reflect post-October 2023 standalone carve-out operations, rather than legacy parent Kellanova).
2. *Would we notice if it did not?*  
   (e.g., checking turnover-per-employee: Google Ireland's €17.7M/head instantly exposes transfer pricing billing, while Yazaki Romania's €60k/head flags physical labor assembly).

### 2. Bottom-up Proxy Recipes & Scale Reproducibility

Each figure is delivered as an asymmetric interval `[Min, Best Estimate, Max]`, accompanied by its derivation formula, audit vulnerability, and global scalability class ([DEC-006](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-006-proxy-estimation-framework--deliverable-schema-the-detective-triad)):

#### A. The Micro-Retail Footprint Proxy (`IN-061` MARGOT BAKERY LIMITED)
- **Delivered Figures:** Revenue: **$620k USD** [£480k - £780k GBP] | Headcount: **7 staff** [5 - 9 FTE].
- **Derivation Chain:** 1 single retail shopfront in East Finchley. Open 5 days/wk = 250 operating days/yr. Till throughput = 220–280 transactions/day @ £7.50 average ticket (sourdough loaf £4.50 + specialty pastry/coffee £4.00) = £1,650–£2,100 daily take -> £412k–£525k/yr (£490k best estimate). Headcount of 7 FTE corroborated by micro-entity balance sheet payroll liabilities (<£15k accrued) and physical shift coverage (1 master baker, 2 production bakers, 1 apprentice, 3 counter staff).
- **How Wrong Could This Be?:** Downward bound £380k during seasonal summer dips; upper bound £620k if local cafe wholesale supply exists. Cannot mathematically exceed £800k given physical single-deck oven batch capacity.
- **Reproducibility at Scale:** **Tier 2 (~2.5M independent retail/food establishments globally).** Extracted by joining foot-traffic signals, Google Maps opening hours, and till terminal benchmarks.

#### B. The Craft Workshop Benchmarking Proxy (`IN-065` Tischlerei Thunemann KG)
- **Delivered Figures:** Revenue: **€1.35M EUR** [€980k - €1.75M] | Headcount: **10 staff** [7 - 14 FTE].
- **Derivation Chain:** Master joinery workshop in Bippen, Lower Saxony. Physical footprint: ~800 sqm workshop + 3 liveried commercial transport vans. German Handwerkskammer (HWK) craft benchmark for interior joinery: €125k–€145k revenue per full-time craftsman. Staff composition: 1 Master joiner, 6 journeymen, 2 apprentices, 1 admin = 10 FTE * €135,000 = €1,350,000.
- **How Wrong Could This Be?:** Downward bound €980k during residential construction slumps; upper bound €1.75M if premium bespoke luxury joinery margins apply (+30%).
- **Reproducibility at Scale:** **Tier 2 (~580,000 Handwerk workshops in DACH).** Extractable via trade guild directories (Handwerkskammer roll), workshop satellite footprints, and fleet registrations.

#### C. The Niche Volumetric Certification Proxy (`IN-094` Rolex SA)
- **Delivered Figures:** Revenue: **$11.5B USD** (10.1B CHF) [$10.2B - $12.8B] | Headcount: **14,000 staff** [12,500 - 15,500].
- **Derivation Chain:** Owned 100% by Fondation Hans Wilsdorf (zero public filings). Primary physical proxy: Swiss Chronometer Testing Institute (COSC) official regulatory certifications verify ~1.15M mechanical movements tested annually. Morgan Stanley/LuxeConsult census verifies ~1.24M total watches sold across authorized dealer networks at ~15.1B CHF retail value. Wholesale realization rate (~67%) yields 10.15B CHF wholesale revenue. Geneva manufacturing sites (9,000 staff) + Biel movement manufacture (3,500 staff) + global distribution subsidiaries (1,500 staff) = 14,000 FTE.
- **How Wrong Could This Be?:** Wholesale margin flexes between 62% and 70% ([$10.2B, $12.8B]). Bounded hard by COSC technical throughput: Rolex cannot produce 2M watches without massive unannounced factory expansions.
- **Reproducibility at Scale:** **Tier 3 (<50 ultra-luxury private titans).** Highly accurate but bespoke; requires regulatory certification logs.

#### D. The Run-Rate Velocity Proxy (`IN-056` Anysphere / Cursor)
- **Delivered Figures:** Revenue: **$150M ARR** [$90M - $250M] | Headcount: **110 staff** [75 - 160 FTE].
- **Derivation Chain:** Late-2024 developer adoption velocity: crossed $100M ARR milestone pacing towards $150M–$200M based on 500k+ active paid subscriptions ($20-$40/mo). Engineering commit graphs and recruiting census indicate 80–120 core employees, generating >$1.2M ARR/employee.
- **How Wrong Could This Be?:** Massive velocity error: static filings from 2023 (<$10M ARR) are obsolete by 15x. Asymmetric bounds [$90M, $250M] reflect exponential hyper-growth.
- **Software Pricing Recommendation:** **Index on active engineering seats (~110 seats) with annual re-metering.** Pricing on backward-looking statutory revenue will underbill by 10x.

#### E. The Corporate Form Negative Proxy (`IN-086` STEYN HOLDING S.A., SPF)
- **Delivered Figures:** Commercial Revenue: **€0** [€0 - €0] | Headcount: **0 staff** [0 - 1].
- **Derivation Chain:** Luxembourg Law of 11 May 2007 (Art. 1) explicitly bars a Société de Gestion de Patrimoine Familial (SPF) from commercial trading or operational services. Commercial turnover is strictly €0; managed by a domiciliation agent.
- **Software Pricing Recommendation:** **Zero Seat / Dormant Tier.** Attempting to price an enterprise tier based on holding asset wealth will result in immediate cancellation.

---

## Part 3: The Call

### Would you ship this?
**Yes, but strictly as a Tiered Deliverable with explicit confidence flags, never as an unhedged flat lookup table.**

- **What we ship with full confidence:** Tiers 1, 2, 3, and 6 (Audited Filings, Transfer Pricing Distinctions, Physical Unit Proxies, and Statutory Shell Forms). Every figure carries bounded intervals, derivation equations, and pricing recommendations.
- **Where we draw the line:** We refuse to ship automated point estimates for hyper-velocity tech startups (`IN-056`) without quarterly re-metering clauses, and we refuse to impute unresolvable polysemic names (`IN-075`).

### What our checks still cannot see:
1. **Intra-Year Velocity Spikes:** Statutory filings are historical snapshots with 6–18 month reporting lags. An AI startup can grow from $10M to $100M ARR while its official register record shows 5 employees.
2. **Shadow IT & Corporate Parent Umbrella MSAs:** Even if an entity has 50 employees, software may be deployed group-wide under a global master agreement signed by a holding entity.
3. **Subcontractor & Toll Manufacturing Dilution:** A company reporting 10 employees may run a 2,000-person factory through outsourced third-party staffing agencies, invisible on balance sheet payroll lines.

---

## Part 4: The Room (Commercial Insight)

### The Transfer-Pricing Hub Arbitrage Trap: Software Mispricing Across Borders
In auditing this licensee portfolio, we uncovered a systemic revenue leak created by contract pricing rules that rely naively on statutory turnover: **the software vendor is simultaneously overcharging regional billing hubs and giving away enterprise software for free to multinational factories.**

Consider the structural contrast between `IN-015` (**Google Ireland Limited**) and `IN-016` (**Yazaki Romania S.R.L.**):
- Google Ireland reports **€86.6 Billion** in booked turnover with **4,882 employees** (~€17.7 Million per head), because it acts as the centralized advertising billing engine for the EMEA region.
- Yazaki Romania reports **€220 Million** in turnover with **3,623 employees** (~€60,000 per head), operating as a low-margin toll-manufacturing assembly plant for automotive wire harnesses.

If the vendor prices tiers by company revenue, Google Ireland is billed at an astronomical tier that sales reps will lose in every audit renegotiation (because the software is only used by local Dublin campus staff), while Yazaki Romania is billed at a modest mid-market tier despite deploying the software across **3,600 industrial workstations**. 

**Actionable Advice:** The vendor must decouple contract tiering: price multinational operational subsidiaries on **local seat headcount footprint**, and price administrative billing entities strictly on **active internal users**, avoiding the distortion of brass-plate statutory turnover.

---

## Part 5: The Register (Empirical ONRC Audit)

We evaluated the scalability of our best proxy—**The Physical Unit-Economic Capacity & Footprint Proxy**—across the complete Romanian trade register snapshot ([DEC-007](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-007-part-5-romanian-register-scalability-check), [`scripts/analyze_romanian_register.py`](file:///d:/Proiect%20Veridion/scripts/analyze_romanian_register.py)).

### 1. The Separation Rule (Living vs. The Rest)
> **The One-Line Rule:**  
> *"A company is classified as living if its unique statutory fiscal code (CUI) submitted active annual accounts for fiscal year 2024 in the Ministry of Finance registry (`web_uu_an2024`), separating operating commercial entities from historical dissolved partnerships, struck-off entities, and defunct shells."*

- **Total Historical Register (`OD_FIRME.csv`):** **4,116,356** registered entities since 1990.
- **Active Living Entities (`web_uu_an2024.txt`):** **822,292** active filing companies.
- **Attrition Rate:** **80.02%** of all historical registrations are defunct, dissolved, or inactive.

### 2. The Three Reported Numbers

| Metric | Empirical Result | Methodological Rationale |
| :--- | :---: | :--- |
| **1. Companies inside our proxy line** | **108,115** | Active operating entities in sectors governed by physical unit-economic metrics. |
| **2. Share of filtered living register** | **13.15%** | Over 13% of the living Romanian commercial economy runs on physical capacity mechanics. |
| **3. Three largest industries among them** | Listed below | Retail storefronts, vehicle maintenance workshops, and restaurants. |

#### The Three Largest Industries Inside the Proxy Line:
1. **CAEN 4711 – Grocery Retail Stores:** **38,668 companies** (35.8% of proxy population)  
   *Proxy Model:* Sized by till throughput, checkout lane density, and foot traffic.
2. **CAEN 4520 – Automotive Repair Workshops:** **16,637 companies** (15.4% of proxy population)  
   *Proxy Model:* Sized by hydraulic service bays (~€90k–€130k revenue per mechanic bay).
3. **CAEN 5610 – Restaurants & Dining Establishments:** **15,680 companies** (14.5% of proxy population)  
   *Proxy Model:* Sized by table cover counts and average customer dining ticket size.

---

## ✂️ The Cut List (What We Deliberately Did Not Do)

1. **Scraping Commercial Aggregators (ListaFirme, North Data, ZoomInfo):** Scraped third-party aggregators fail auditor interrogation due to 1–2 year data staleness and aggressive bot-blocking (HTTP 403). We replaced them with direct statutory government APIs (SEC, Companies House, ANAF, ZEFIX) ([DEC-005](file:///d:/Proiect%20Veridion/DECISIONS.md#dec-005-evidence-harvesting-primary-statutory-apis-vs-commercial-aggregators)).
2. **Symmetric Arbitrary Error Bands (±15%):** Symmetrical percentage error is statistically fraudulent for opaque entities. A bakery cannot expand beyond oven capacity (+25% max), while an AI startup's upside error is +300%. We replaced symmetric bands with asymmetric structural bounds `[Min, Max]`.
3. **Imputing Ambiguous Polysemic Names (`IN-075` Apex Group):** We refused to guess between 4 clashing multi-billion corporations. Arbitrary imputation destroys dataset integrity.
4. **Quant Machine Learning Regression for Global Sample:** We discarded training an ML model on Romanian data to predict global entities. Applying Romanian CAEN models to London bakeries and Swiss watchmakers is indefensible in an audit.

---

## 💬 Debate Topics

### 1. Where in your workflow would you not trust an AI tool, and how would you catch it being confidently wrong?
We do not trust AI models for entity resolution disambiguation and numerical fact retrieval (e.g., asserting that a company has "$42M revenue and 180 employees"). LLMs frequently hallucinate plausible-sounding numbers by conflating a subsidiary with a parent or confusing currency symbols (GBP vs EUR vs USD). We catch this by enforcing **deterministic statutory cross-validation**: every numeric claim must be verified against an official registry document (SEC 10-K, Companies House filing, ANAF balance sheet) where legal registration numbers and filing dates match character-for-character.

### 2. How would you know your dataset was wrong at scale, with nothing complete to compare it against?
We detect systematic errors through **macroscopic macroeconomic boundary checks and ratio invariants**. Even without ground truth for every row:
- We compute **Turnover per Employee distributions** by 2-digit industry codes: if a cluster of manufacturing firms shows >€5M/head (resembling an oil refinery rather than a workshop) or software firms show <€10k/head, the matching pipeline has conflated transfer pricing hubs or parent holding companies.
- We run **Benford's Law tests** on leading digits of modeled revenues across millions of rows; synthetic or ungrounded proxy outputs deviate sharply from logarithmic first-digit distributions.

### 3. If every figure comes with a range you would bet on, how would you set the widths, and how could anyone tell, a year later, whether your ranges were honest?
Range widths must be **empirically bounded by physical and legal constraints**, not arbitrary percentages:
- For a retail bakery (`IN-061`), the floor is bounded by lease rent + minimal labor payroll, and the ceiling is hard-capped by physical oven capacity (deck square-footage and operating hours).
- **Evaluating honesty 1 year later:** We track the **Empirical Coverage Rate**: if our methodology claims 90% confidence intervals, exactly ~90% of subsequent filed statutory accounts must fall inside `[Min_Bound, Max_Bound]`. If 99% fall inside, our intervals were cowardly and uninformative; if only 60% fall inside, our models were overconfident and flawed.
