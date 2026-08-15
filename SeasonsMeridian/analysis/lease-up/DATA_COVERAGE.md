# Seasons at Meridian — Lease-Up Analysis: Source Coverage Assessment

*Prepared 2026-08-14, before building the monthly lease-up table.*

Goal: a month-by-month series from the start of lease-up covering (1) leases signed,
(2) leases expired, (3) renewals + renewal increase, (4) units leased to a new tenant +
new-lease trade-out — each on both a **gross** and an **effective** basis.

## What we have, and how far back it reaches

| Source | Coverage | Grain | Reaches lease-up start? |
|---|---|---|---|
| HelloData Unit Details (8/14/2026) | **Jun 2024 → Aug 2026** | 555 listing episodes, 353 of 360 units | **Yes — the only continuous source** |
| Rent roll 1/1/2026 (backdated export) | roster as-of 1/1/26 | 360 units, 314 occupied | No |
| Rent rolls 7/07, 7/19, 8/04/2026 | contemporaneous snapshots | 360 units | No |
| Rent roll w/ lease charges 7/09/2026 | charge-code detail | 2,666 charge rows | No |
| Concession Burn Off 6/21 & 7/30/2026 | **current residents only** (347) | Move In + *current* Lease Start + term + concessions | Partially — move-ins reach 8/21/2024, but only 16 residents remain from 2024 |
| Renewal Trade-Outs (3ps) | **5/10/2026 – 7/9/2026 only** | 23 renewals, exact prior/new gross + concession + effective | No |
| T12 (Jun25–May26, Jul25–Jun26) | **Jun 2025 → Jun 2026** | monthly GL | No — first 10 months of lease-up missing |

First move-in on record: **8/21/2024**. First HelloData listing: **6/1/2024**.

## The gap, stated plainly

For **Aug 2024 – Dec 2025** (17 months, roughly the first half of the lease-up) there is
no roster snapshot, no lease-start data for anyone who has since left, no renewal report,
and (before Jun 2025) no financials. Every tenant who moved in and out during that window
is invisible to the Yardi sources.

What survives from that period:

- **Burn-off**: only 16 current residents moved in during 2024 — and *all 16 have already
  renewed at least once*, so their initial lease terms and initial rents are not directly
  recoverable from the burn-off (it shows the current lease only). Several show ~546-day
  move-in→lease-start gaps, which could be one renewal off an 18-month initial lease **or**
  two successive renewals — the sources cannot distinguish these.
- **HelloData**: 537 dated off-market episodes, distributed across every month from Jun 2024
  forward. Chaining episodes within a unit yields **184 unit-level re-lease events**
  (prior listing → next listing) spanning 2025Q1 – 2026Q3, on both asking and effective bases.

So the pre-2026 period can be built on HelloData proxies, but not on Yardi actuals.

## Known source quirks (carried forward)

- Burn-off column *Lease Rent* is not always contract rent — H203 shows $386 and H213 $342
  where the 8/4 rent roll shows $1,600 and $1,995. **Use rent-roll Actual Rent as the rent
  of record**; treat burn-off Lease Rent as a fallback only.
- Rent-roll "Actual Rent" is **gross face rent** — concessions at Seasons were paid as
  upfront dollar amounts, not amortized into the rate.
- Two corporate leases identified: **Coleman Environmental Engineering (B307)** and
  **Murata Machinery Inc (H203**, future move-in 8/30/2026**)**.
- HelloData `Term` is populated on 250 of 555 episodes; `Last Effective Rent` on all 555.
- The 1/1/2026 rent roll was exported ~Aug 2026: its roster and rents are as-of 1/1, but its
  Lease Expiration and Move Out columns reflect *current* lease records.

## Reports that would close the gap

In descending order of value:

1. **Yardi lease history / lease audit** (every lease ever written per unit: start, end,
   term, gross rent, concession). One report; would make the entire analysis exact.
2. **Renewal trade-out reports (3ps format) for all windows outside 5/10–7/9/2026** —
   the format already in hand is exactly right, it just needs more periods.
3. **Monthly resident activity / box score** from Aug 2024 (leases signed, move-ins,
   move-outs, notices per month) — the direct answer to "leases signed per month".
4. **Historical month-end rent rolls**, Aug 2024 – Dec 2025.
5. **Monthly financials for Aug 2024 – May 2025** (pre-dates both T12s).
