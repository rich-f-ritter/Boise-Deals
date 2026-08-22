# Seasons at Meridian — Lease-Up Analysis: Source Coverage Assessment

*Prepared 2026-08-14; revised 2026-08-21 after the Aug 18–19 document drop (v5 rebuild).*

Goal: a month-by-month series from the start of lease-up covering (1) leases signed,
(2) leases expired, (3) renewals + renewal increase, (4) units leased to a new tenant +
new-lease trade-out — each on both a **gross** and an **effective** basis.

## What we have, and how far back it reaches

| Source | Coverage | Grain | Reaches lease-up start? |
|---|---|---|---|
| HelloData Unit Details (8/21/2026) | **Jun 2024 → Aug 2026** | 562 listing episodes | **Yes — the only continuous source** |
| Rent roll 1/1/2026 (backdated export) | roster as-of 1/1/26 | 360 units, 314 occupied | No |
| Rent rolls 7/07, 7/19, 8/04, 8/18/2026 | contemporaneous snapshots | 360 units | No |
| Rent roll w/ lease charges 7/09/2026 | charge-code detail | 2,666 charge rows | No |
| Concession Burn Off 6/21, 7/30, 8/19/2026 | **current residents only** (351 at 8/19) | Move In + *current* Lease Start + term + concessions + burn end date | Partially — move-ins reach 8/21/2024, but only 16 residents remain from 2024 |
| Renewal Trade-Outs (3ps) 5/10–7/9 + 6/19–8/19/2026 | **5/10/2026 – 8/19/2026** | 40 distinct renewals, exact prior/new gross + concession + effective | No |
| **New Lease Tradeouts (3ps) 6/19–8/19/2026** | **6/19/2026 – 8/19/2026** | 44 re-leases (incl. 14 signed future move-ins), exact prior/new gross + effective + days vacant | No |
| T12s (Jun25–May26, Jul25–Jun26, Aug25–Jul26) | **Jun 2025 → Jul 2026** | monthly GL | No — first 10 months of lease-up missing |

First move-in on record: **8/21/2024**. First HelloData listing: **6/1/2024**.

The 8/19 New Lease Tradeouts report is the single biggest upgrade since the first cut:
it is the exact, Yardi-native record of prior→new economics for every re-lease applied
6/19–8/19, which (a) replaces reconstruction for that window, (b) validates the
reconstruction method where the two overlap, and (c) reveals the **signed forward
book** — leases already executed for Sep–Nov move-ins.

## The gap, stated plainly

For **Aug 2024 – Dec 2025** (17 months, roughly the first half of the lease-up) there is
no roster snapshot, no lease-start data for anyone who has since left, no renewal report,
and (before Jun 2025) no financials. Every tenant who moved in and out during that window
is invisible to the Yardi sources. The pre-2026 period is built on HelloData proxies,
clearly flagged, and is not blended with the actuals.

## Known source quirks (carried forward — several are hard-won)

- Burn-off column *Lease Rent* is not always contract rent — H203 showed $386 and H213
  $342 where the roll shows $1,600 and $1,995. **Use rent-roll Actual Rent as the rent
  of record**; treat burn-off Lease Rent as a fallback only.
- Rent-roll "Actual Rent" is **gross face rent** — concessions at Seasons were paid as
  upfront dollar amounts, not amortized into the rate.
- **Corporate leases (16 units, 4 users, 4.4% of the property)**: Murata Machinery Inc
  (8 units — 4 in place, 4 future; H203 dropped, H111 substituted), Paragon Corporate
  Housing (7), Coleman Environmental Engineering (B307) and Wolff Corporate Housing
  (H111) — the latter two both move out 9/30/2026. Detection is by name pattern, so a
  new corporate user cannot silently enter the rent statistics.
- **Internal transfers** (same resident, unit→unit; 21 detected) are negotiated swaps,
  not arm's-length pricing (G103 books $2,140 on a ~$1,718-market A1). Both sides are
  flagged and excluded from rent statistics.
- **Yardi resident ids do not map 1:1 to tenancies**: an id can be carried across a
  transfer (t0033902, J108→G103) — tenancies are therefore keyed by id+unit, and
  duplicate departures created by id reassignment are collapsed.
- The trade-out report's *Movein* can differ from the roll's move-in by weeks (F312:
  6/13 roll vs 7/25 report) — report matching is by unit + resident name.
- The roll and the report can disagree on a future signer (E313: roll Charles Aiken,
  report Emily Malone). The roll is the roster of record; disagreements are flagged.
- A Future-section lease that vanishes from a later roll was **dropped** (Murata H203)
  — only futures on the latest roll count as live signings.
- T12 overlaps agree exactly EXCEPT Apr 2026: the Aug25–Jul26 statement restates
  concessions (4460) −$5,648.50 → −$6,466.00. Later file wins.
- HelloData `Term` is populated on ~45% of episodes; `Last Effective Rent` on all.
- The 1/1/2026 rent roll was exported ~Aug 2026: its roster and rents are as-of 1/1, but
  its Lease Expiration and Move Out columns reflect *current* lease records.

## Pipeline (v5)

```
build_leaseup.py   sources → events.csv + monthly.csv + stats.json + monthly_activity.json
build_workbook.py  events/monthly/stats + t12.py → 'Seasons at Meridian - Lease-Up Analysis.xlsx'
validate.py        ties the ledger to every source that can independently confirm it
build_model_tab.py + inject_tab.py → 'Lease-Up Bridge' tab in the TMG model copy
```

Every Summary figure is computed at build time — nothing hand-keyed. `validate.py`
reads its expected values from the source reports' own total rows at run time.

## Reports that would close the remaining gap

In descending order of value:

1. **Yardi lease history / lease audit** (every lease ever written per unit: start, end,
   term, gross rent, concession). One report; would make the entire analysis exact.
2. **Renewal + new-lease trade-out reports (3ps format) for windows before 5/10/2026.**
3. **Monthly resident activity / box score** from Aug 2024 (leases signed, move-ins,
   move-outs, notices per month).
4. **Historical month-end rent rolls**, Aug 2024 – Dec 2025.
5. **Monthly financials for Aug 2024 – May 2025** (pre-dates all three T12s).
