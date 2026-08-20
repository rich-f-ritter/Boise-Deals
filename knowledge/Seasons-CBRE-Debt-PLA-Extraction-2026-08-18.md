# Seasons at Meridian — CBRE Debt PLA Extraction (dated 8/18/2026)

**Source:** `in/Seasons_at_Meridian_PLA_8.18.26.pdf` — CBRE Debt & Structured Finance preliminary
loan analysis / loan sizing comparison (Jay Wagley team), 5 pp. Prepared for The Milestone Group.
Inputs CBRE used: purchase price **$125.0M** ($347,222/u), budgeted capex $1,710,000 ($4,750/u —
the pre-Justin-refinement budget; see model-diff note), rent roll dated 8/4/2026, occupancy 96.67%,
As-Is NCF cap 4.61%, CBRE DSF As-Is NCF $5,766,584, Borrower Y1 NCF $6,125,726.
Index rates 8/18/26: 5-yr UST 4.37%, 7-yr UST 4.53%, SOFR 3.65%, 30D avg SOFR 3.64%.

## Sizing grid (base, before buydown)

| Program | Amount | Term / IO | Rate | Constraint | Prepay |
|---|---|---|---|---|---|
| Freddie CME Max Lev 5-yr fixed | $69,315,000 | 5 yr / full IO | 5.77% (UST+1.40) | 1.25x amort DSCR | Defeasance |
| Freddie CME Max Lev 7-yr fixed | $68,427,000 | 7 yr / IO 6-7 | 5.88% (UST+1.35) | 1.25x | Defeasance |
| Freddie CME floating | $68,427,000 | 7 yr | 5.45% (SOFR+1.80) | fixed-rate equiv | 1yr lockout, 1% |
| Fannie DUS Tier 2 5-yr | $68,902,000 | 5 yr / IO 2-5 | 5.82% (UST+1.45) | 1.25x | YM |
| Fannie DUS Tier 2 7-yr | $68,023,000 | 7 yr / IO 6-7 | 5.93% (UST+1.40) | 1.25x | YM |
| LifeCo hybrid max-lev | $76,888,000 | 5 yr / IO 3-5 | 6.37% (UST+2.00) | 7.50% As-Is DY | YM |
| LifeCo fixed | $67,756,000 | 5 yr / full IO | 5.87% (UST+1.50) | 1.20x / 8.0% DY | YM |
| Debt fund 70% LTV floater | $87.5M ($1.71M future) | 3+1+1 | 6.15% (SOFR+2.50) | 0.90x / 80% LTV | min interest |
| Debt fund 65% LTV floater | $79.5M ($1.71M future) | 3+1+1 | 6.00% (SOFR+2.35) | 1.00x / 70% LTV | min interest |

## Rate-buydown optionality (the trade TMG selected)

| Program | Spread benefit | Cost | Net spread | Rate w/ BD | Gross loan w/ BD | LTV w/ BD | DSCR |
|---|---|---|---|---|---|---|---|
| **Freddie 5-yr fixed (SELECTED)** | **(0.46%)** | **2.00%** | **0.94%** | **5.31%** | **$73,305,000** | **58.6%** | **1.25x** |
| Freddie 7-yr fixed | (0.35%) | 2.00% | 1.00% | 5.53% | $71,370,000 | 57.1% | 1.25x |
| Freddie floating | (0.30%) | 1.00% | 1.50% | 5.15% | $69,916,000 | 55.9% | 1.34x |
| Fannie 5-yr | (0.45%) | 2.00% | 1.00% | 5.37% | $72,765,000 | 58.2% | 1.25x |
| Fannie 7-yr | (0.35%) | 2.00% | 1.05% | 5.58% | $70,938,000 | 56.8% | 1.25x |

Buydown benefit (Freddie 5-yr): +$3.99M gross proceeds and −46bp rate for a $1.466M fee;
"Benefit of Buy Down" per CBRE = $2,523,900 net. Closing costs est. 2% of loan. 35-yr amort waiver
assumed; Freddie IO tiered for refi test (no waiver assumed).

## As modeled in v6
Financing tab "FREDDIE FIXED (MAX BD)": $73,278,247 proceeds (≈ PLA's $73.305M), all-in 5.31%,
Actual/360 (effective ~5.38% on 365-day dollars), 60-mo IO, effective 9/30/26, 2.6% financing fees
(incl. buydown), open period 3 mo — modeled payoff at par + prepay penalty rows at exit.
Alternatives carried in scenario columns: ALT LIFECO 6.37%, Freddie fixed forward (month 24+)
4.91%, PortCo floater (mo 1-24) 5.53%, Freddie floater 5.43%.

## Affordability metrics (PLA)
Mission-driven 45.6%; 99.17% of units ≤100% AMI; 45.56% ≤80% AMI. GSE market type: Standard;
green financing: No.

## PLA operating-statement page (CBRE UW vs trailing, for reference)
CBRE UW NRI $7,094,967 ("assumes steady/improving collections through close"; UW = 08/04/2026 RR
annualized, 5.75% vacancy factor, 2.5% mgmt fee, $200/u reserves); June T3 NRI annualized
$7,063,035; RE taxes UW $440,067 (2026 AV grown 5% per appraiser — NOTE: differs from KEAndrews
sale-reassessment schedule TMG underwrites; CBRE's is a lender UW convention, not our tax case).
