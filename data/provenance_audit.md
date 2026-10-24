# Provenance Audit: verified vs. previously shipped
Generated 2026-10-24T14:19:46+00:00 by `scripts/verify_figures.py` (DEC-009).

| ID | Field | Previously shipped | Verified now | Δ | Source |
| :-- | :-- | --: | --: | --: | :-- |
| IN-016 | turnover | 1,095,406,920 | 1,095,214,991 RON | -0.0% | [MF annual filing, field I13 (Cifra de af](https://data.gov.ro/dataset/d3caacb6-2c08-445e-94e6-8d36d00ab250/resource/f89140dc-20dd-494f-912a-d1a482188885/download/web_bl_bs_sl_an2024.txt) |
| IN-016 | employees | 3,623 | 3,623 persons (annual average) | +0.0% | [MF annual filing, field I20 (Numar mediu](https://data.gov.ro/dataset/d3caacb6-2c08-445e-94e6-8d36d00ab250/resource/f89140dc-20dd-494f-912a-d1a482188885/download/web_bl_bs_sl_an2024.txt) |
| IN-030 | operating_income_net | 8,217,313,387 | 8,187,030,378 RON | -0.4% | [MF credit-institution filing, field I18 ](https://data.gov.ro/dataset/d3caacb6-2c08-445e-94e6-8d36d00ab250/resource/e6d67782-6319-456c-ae0a-a8123ef5a994/download/web_instit_de_credit_an2024.txt) |
| IN-028 | revenue | 2,760,000,000 | 2,708,000,000 USD | -1.9% | [XBRL us-gaap:RevenueFromContractWithCust](https://data.sec.gov/api/xbrl/companyfacts/CIK0001959348.json) |
| IN-028 | employees | 3,150 | 3,280 persons | +4.1% | [Regex on 10-K Human Capital text](https://www.sec.gov/Archives/edgar/data/1959348/000162828025007817/klg-20241228.htm) |
| IN-071 | parent_revenue | 84,039,000,000 | 87,032,000,000 USD | +3.6% | [XBRL us-gaap:Revenues, full-year, accn 0](https://data.sec.gov/api/xbrl/companyfacts/CIK0000080424.json) |

Note: IN-030 previous value was quoted in RON inside the derivation text; IN-071 previous parent figure was quoted in the notes.

## Red flags raised by the gate
- **IN-028**: Deregistered from SEC on 2025-10-06; no ticker listed. Likely acquired — confirm acquirer before licensing at group level.
- **IN-071**: Contract names a brand. Parent P&G: revenue 87,032,000,000 USD (FY ending 2026-06-30), ~104,000 employees. Which entity signed must be read from the contract.

## Coverage

- MATCHED, NOT SIZED: 2
- PARTIAL: 1
- REFUSED MATCH: 1
- SCOPE QUESTION: 1
- VERIFIED: 2
- WITHHELD: 6
