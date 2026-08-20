# Seasons at Meridian — First-Turn Analysis: Data Notes

*Last updated: 2026-08-12*

Purpose: analyze how the first turn of the rent roll is performing — retention ratio,
renewal trade-outs, and new-lease trade-outs for the initial lease-up tenant cohort.

## Property basics (from rent rolls)

- **360 units**, Yardi-managed ("3pseason" property code), lease-up began ~Jun 2024 (first HelloData listings), first move-ins Aug 2024.
- Unit types (Aug-4-2026 roll): A1_Seas 115 (1x1, 693sf), A2_Seas 44 (1x1, 746sf), B1_Seas 30 (2x2, 1092sf), B2_Seas 72 (2x2, 1141sf), B3a_Seas 12 (1165sf), B3b_Seas 30, C1a_Seas 10 (3x2, 1328sf), C1b_Seas 19, S1_Seas 14 (studio, 517sf).
- Occupancy: 314/360 (87%) on 1/1/2026 → 346/360 (96%) on 8/4/2026.
- One corporate lease identified (Coleman Environmental Engineering, B307) — exclude from trade-out stats.

## Source documents (documents/)

| File | What it is | Caveats |
|---|---|---|
| rent-rolls/RentRoll_AsOf_2026-01-01_BACKDATED | Yardi rent roll "As Of 1/1/2026" | **BACKDATED — generated ~Aug 2026** (`Month Year = 08/2026`). Roster (who was in each unit) is as-of 1/1 and reliable. Lease Expiration and Move Out columns pull from CURRENT lease records: 115 rows show move-outs that happened Feb–Sep 2026; expirations already reflect renewals signed after Jan 1. **Actual Rent appears to be the as-of-January charge** (39 stayers show rents that differ from the Aug roll — verified against the renewal trade-out report: e.g., A211 Valdez 1520→1570 matches report exactly). |
| rent-rolls/RentRoll_AsOf_2026-07-07, _07-19, _08-04 | Contemporaneous Yardi rent rolls | Genuine snapshots (generated at/near as-of date). No Lease Start column — only Move In / Lease Expiration / Move Out. |
| rent-rolls/RentRoll_withLeaseCharges_AsOf_2026-07-09 | Rent roll + charge-code detail per unit | Charge codes: rentres (base rent), utilpest, utiltras, internet ($85 mandatory?), parkres, etc. Base rent `rentres` ties to Actual Rent on plain rolls. Use for all-in cost / other-income analysis. |
| t12/T12_Jun2025-May2026, T12_Jul2025-Jun2026 | Yardi 12-month accrual statements, monthly detail | Use to tie out concessions, LTL, vacancy at property level. |
| hellodata/HelloData_UnitDetails_2026-08-12.csv | 535 listing episodes, 353 distinct units, Jun 2024 → Aug 2026 | See validation below. |
| renewal-reports/RenewalTradeouts_2026-05-10_to_2026-07-09.xlsx | **Yardi/3ps renewal trade-out report — the authoritative renewal record** | Only covers renewals with new start dates 5/10/2026–7/9/2026 (23 renewals). Has old expiration, new start, prior/new term, prior/new GROSS rent, prior/new total concession + amortized, prior/new EFFECTIVE rent, gross % and effective % increase. |
| concession-burnoff/ConcessionBurnOff_AsOf_2026-06-21.xlsx, _2026-07-30.xlsx | **Yardi Concession Burn Off — the only source with LEASE START DATE per resident.** Per current resident: Move In, Lease Start (current lease), Lease Term, Market Rent, Lease Rent, current-lease concessions ($ total), concession end date, remaining. | Two sections per file: the burn-off table, then a "Projection by Unit" section (skip rows with term '0.00' / parse sections separately). Asterisk on Lease Start = mid-month start footnote. Current residents only (~348) — no former residents. **Lease Start > Move In ⇒ renewal directly observable: 65 renewals as of 7/30** (one false positive: A204 Campagni LS = MI+1 day; use a >45-day threshold). Concession fields cover CURRENT lease only — a renewed tenant's initial-lease concession must come from the renewal report or HelloData. |

## Key findings so far

1. **Concessions on initial leases were upfront dollar amounts** (e.g., $1,000–$3,990 ≈ 2–8 weeks free), NOT amortized into the monthly rate. So rent-roll "Actual Rent" = **gross face rent**. Renewal report confirms: May–Jul 2026 renewals averaged **+1.7% gross** but **+9.2% effective** (concession burn-off is most of the economics). Any trade-out analysis must show both bases.
2. **Renewals are frequently flat on gross rent** (7 of 23 in the report window had 0.0% gross increase). Therefore rent-change between two rent-roll snapshots UNDERCOUNTS renewals — flat renewals are invisible without the renewal report or lease dates.
3. **HelloData validated against the rent roll** (2026 move-ins, n=71 matched within ±30 days): 64/71 exact match between Last Asking Rent and rent-roll Actual Rent (median diff $0). Units go off-market a **median 15 days before move-in**. Another 50 move-ins match an episode at 31–90 days (pre-leased further ahead); 14 have no nearby episode (never listed / transfers). → HelloData Last Asking Rent is a reliable proxy for executed new-lease rent here; note it is *gross* asking, and Last Effective Rent reflects concession-adjusted.
4. **HelloData contains only marketed units → new leases. Renewals never appear.** A HelloData episode ending near a move-in confirms a new lease.
5. HelloData floorplan labels map to rent-roll unit types: A1→A1_Seas, A2→A2_Seas, B1→B1_Seas, B2→B2_Seas, B3→B3a/B3b_Seas, C1→C1a/C1b_Seas, S1→S1_Seas. HelloData `Term` (populated 250/535) gives the initial lease term → can reconstruct initial lease expirations.

## Jan-1 cohort classification (preliminary, vs 8/4/2026 roll, by Resident ID)

314 occupied units on 1/1/2026:

- **104 moved out** (103 units re-leased, 1 still vacant)
- **39 stayed with a rent change** → confident renewals (gross trade-out preview: +3.1% avg / +2.5% median)
- **4 stayed past expiration with no new lease** (MTM holdover)
- **87 stayed, flat rent, implied term >16.5 months** → mix of flat renewals and long initial leases; renewal report resolves those renewed 5/10–7/9; earlier flat renewals still ambiguous
- **80 stayed, initial lease clearly not yet expired**

Preview new-lease trade-out (prior tenant final gross rent → new tenant gross rent, n=91): **+5.1% avg / +3.8% median**.

## Analysis architecture (how the sources fit together)

Initial lease terms were heavily staggered (7/30 burn-off term distribution: 12mo ×173, 18mo ×63, plus 9/13/15/16/17mo tranches) — so implied-term heuristics alone were never going to work; the burn-off Lease Start column is what makes renewal identification exact.

Per-unit first-turn ledger, built in this priority order:
1. **Roster & tracking:** Jan-1-2026 roll roster (reliable) → track each Resident ID into the 7/07, 7/19, 8/04 rolls. Moved out = ID gone. New tenant = different ID in unit.
2. **Renewal identification:** burn-off Lease Start > Move In (+45d threshold) as of 6/21 or 7/30 → renewal + exact renewal date + new term. Renewal report adds prior/new detail for the 5/10–7/9 window. Rent-change signature (Jan roll vs Aug roll) as cross-check.
3. **Gross trade-outs:** renewal = prior gross (Jan roll actual / renewal report / 6-21 burn-off pre-renewal Lease Rent) → new gross (Aug roll actual). New lease = prior tenant's final gross → replacement tenant's gross.
4. **Effective trade-outs:** prior-lease concessions from renewal report (exact, in-window) else HelloData episode (Last Asking − Last Effective, amortized over term) else 0-flag; new-lease/renewal concessions from burn-off Current Lease Concessions (exact $, term-amortized). Tie total concessions to the T12 concession line as a sanity check.
5. **HelloData roles:** validate executed rents (64/71 exact vs rent roll), supply initial-lease concessions for pre-May renewals and departed tenants, and confirm new-lease vs renewal (an episode ending near a move-in = marketed new lease; renewals never listed).

## Open items

- Small blind spot: tenants who renewed AND moved out before 6/21/2026 are invisible to the burn-off (rare — first expirations only began ~late 2025; will bound-check via rent-change signature).
- Decide MTM/holdover treatment and retention denominator convention (proposed: retention = renewals ÷ leases reaching first expiration; skips count as move-outs; MTM separate line).
- Corporate lease (B307 Coleman Environmental) excluded from trade-out stats.
- Optional gap-fillers from seller if easy to get: renewal trade-out reports for periods before 5/10/2026 and after 7/9/2026 (exact prior-concession detail for early renewals).
