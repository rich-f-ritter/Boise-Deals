# Seasons at Meridian — Concession Timing Reconciliation (T12 vs HelloData vs Turnover Analysis)

*Analysis date: 2026-08-14*

## Question

The latest T12 (Jul 2025–Jun 2026) still shows concessions in the T1 (Jun 2026: **–$15,484**),
but HelloData and the First Turn / turnover analysis imply there are no concessions on new
leases anymore. Which is right — and did the concessions just hit late?

## Answer

**Both sources are right, and yes — the concessions hit late.** No lease **signed** since
**April 27, 2026** carries any concession (confirmed in both HelloData and the Yardi
Concession Burn Off reports). The concessions in the recent T12 months are the delayed GL
posting of leases signed in **February–April 2026**, when the property was still offering
~1 month free. The lag between signing and GL recognition is **3–5 months**, from two
stacked delays:

1. **Pre-leasing lag (signing → move-in): median 36 days across all conceding 2026
   leases (48 days for the Apr–Jul move-ins), max 112 days.**
   Units go off market (≈ signing) well before move-in. Every one of the 18 conceding
   Apr–Jul 2026 move-ins signed by 4/27/2026. Examples: H313 signed 3/19 → moved in 6/30;
   I110 signed 3/31 → moved in 7/20.
2. **Posting lag (move-in → GL): the free month posts ~month 2 of the lease.**
   Per the 7/30/2026 burn-off "Projection by Unit" section, each concession posts as a
   single lump roughly the second month after move-in: June move-ins post in August, the
   two July move-ins post in September.

Renewals are a non-factor: **1 of 64 renewals** received a concession ($500 total) —
consistent with the turnover analysis (+1.7% gross vs +9.2% effective renewal trade-outs
coming from concession burn-off, not renewal discounts).

## T12 tie-out

T12 concession line (4460-0000), Jul 2025–Jun 2026:

| Month | T12 concessions | Explanation |
|---|---:|---|
| Jul–Dec 2025 | –$30K to –$60K/mo | lease-up era: 2–8 weeks free, broadly granted |
| Jan 2026 | –$16,841 | tail of fall 2025 signings |
| Feb 2026 | –$19,502 | " |
| Mar 2026 | –$16,344 | " |
| Apr 2026 | –$5,648 | trough — Feb/Mar move-in cohorts had few concessions |
| May 2026 | –$16,064 | Mar–Apr signing cohort's free months posting |
| **Jun 2026 (T1)** | **–$15,484** | **6/21 burn-off "Current Month" column = –$13,712** from current residents; remainder ≈ since-departed residents |
| Jul 2026 (proj) | –$4,407 | 7/30 burn-off projection |
| Aug 2026 (proj) | –$12,661 | June move-ins' second-month-free — **not** new concessions |
| Sep 2026 (proj) | –$3,265 | July move-ins (signed in March) |
| Oct 2026+ (proj) | $0 | fully burned off, absent a policy change |

Expect the August statement to still show a ~$13K concession line; it is the known tail,
not evidence of renewed concessions.

## Concession frequency/depth by move-in month (new leases, current residents, 7/30 burn-off)

| Move-in month | Leases | With concession | Freq | Avg concession (conceding) |
|---|---:|---:|---:|---:|
| Nov 2025 | 19 | 7 | 37% | $1,641 |
| Dec 2025 | 20 | 5 | 25% | $1,897 |
| Jan 2026 | 5 | 1 | 20% | $3,288 |
| Feb 2026 | 26 | 2 | 8% | $2,014 |
| Mar 2026 | 28 | 5 | 18% | $1,667 |
| Apr 2026 | 17 | 9 | 53% | $1,845 |
| May 2026 | 9 | 2 | 22% | $1,802 |
| Jun 2026 | 16 | 7 | 44% | $1,855 |
| Jul 2026 | 30 | 2 | 7% | $1,632 |

The Apr–Jun "spike" is a signing-cohort artifact: those move-ins signed Feb–Apr, the last
months of the advertised special. By **signing month**, concessions are ~20–45% of leases
through April, then a hard **0% from May 2026 onward** (see cross-tab below).

## Data caveat: HelloData over-flags concession *frequency* during the concession era

Cross-tab of all 125 matched 2026 new-lease move-ins (HelloData episode ↔ Yardi burn-off),
by signing (off-market) month:

| Signing month | n | HelloData shows conc. | Yardi shows conc. | Both | HD only | Yardi only |
|---|---:|---:|---:|---:|---:|---:|
| Dec 2025 | 7 | 7 | 2 | 2 | 5 | 0 |
| Jan 2026 | 14 | 14 | 1 | 1 | 13 | 0 |
| Feb 2026 | 34 | 34 | 5 | 5 | 29 | 0 |
| Mar 2026 | 25 | 25 | 11 | 11 | 14 | 0 |
| Apr 2026 | 16 | 16 | 7 | 7 | 9 | 0 |
| May 2026 | 9 | 0 | 0 | 0 | 0 | 0 |
| Jun 2026 | 13 | 0 | 0 | 0 | 0 | 0 |
| Jul 2026 | 7 | 0 | 0 | 0 | 0 | 0 |

- HelloData stamped the **advertised** special (~7.7% ≈ 1 month free on a 13-month term) on
  **100%** of listings during Dec–Apr; Yardi shows only **~20–45% actually received** one.
  There are zero Yardi-only cases. So at this property: HelloData effective rent =
  *advertised special*; burn-off = *actually granted*.
- Where both agree, **depth matches well**: Yardi avg $1,865 ≈ one month ≈ HelloData's 8.3%.
- Implication: HelloData **overstated** total concession cost during the winter, and is
  accurate now that the advertised special is gone.

## Watch items

1. The burn-off projection covers **existing leases only**. Last fall the property gave
   $43–60K/month during lease-up; if leasing softens into fall 2026, new concessions could
   reappear on fall signings. HelloData will show it in real time (advertised specials), and
   the granted amounts will lag into the GL by 3–5 months per the mechanics above.
2. Rent gains on concession-free signings are real: new-lease rents rose from ~$1,600–1,690
   (Feb–Mar move-in cohorts) to ~$1,880–1,960 (Jun–Jul) with zero concessions on anything
   signed since May — genuine pricing power, not just concession-optics.

## Sources

All source documents live on branch `claude/seasons-meridian-rent-roll-rinebr` under
`SeasonsMeridian/documents/`:

- `t12/T12_Jul2025-Jun2026.xlsx` — concession GL line 4460-0000 (accrual)
- `concession-burnoff/ConcessionBurnOff_AsOf_2026-06-21.xlsx`, `_2026-07-30.xlsx` — per-resident
  current-lease concessions, lease start dates, concession end dates, "Current Month" postings,
  and the forward "Projection by Unit" section
- `hellodata/HelloData_UnitDetails_2026-08-12.csv` — 535 listing episodes; Last Asking vs Last
  Effective Rent; off-market date ≈ signing date (median 15 days before move-in overall)
- `renewal-reports/RenewalTradeouts_2026-05-10_to_2026-07-09.xlsx` — renewal concession detail
- First Turn Analysis workbook (`SeasonsMeridian/analysis/first-turn/`) — cohort/turnover context

Reproduce the tables with `python3 concession_timing.py` (fetches the documents from the
rent-roll branch via `git archive`).
