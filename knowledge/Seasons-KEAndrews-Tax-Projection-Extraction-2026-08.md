# Seasons at Meridian — KEAndrews Property Tax Projection (extraction)

**Source:** `in/MilestoneGroupSeasonsAtMeridian.pdf` — KEAndrews (est. 1978, Rockwall TX) property
tax projection for The Milestone Group; consultant **Clayton House** (chouse@keatax.com,
469-331-1349). Received ~8/2026, incorporated into model v6 (see
`Seasons-v3-to-v6-Model-Diff-2026-08-20.md`). Parcel R9464160100, Code Area 03, Ada County, 15.64 AC.
KEA modeled purchase price **$125,000,000** (the guidance price), acquisition "Late 2026".

## Projection schedule

| Assessment yr | Total market value | $/u | Est. rate | Est. taxes | $/u |
|---|---|---|---|---|---|
| 2026 (anchor) | $92,993,300 | $258,315 | 0.4507% | $419,161 | $1,164 |
| 2027 (Y1) | $120,625,000 | $335,069 | 0.4417% | $532,861 | $1,480 |
| 2028 (Y2) | $124,243,750 | $345,121 | 0.4329% | $537,851 | $1,494 |
| 2029 (Y3) | $127,971,063 | $355,475 | 0.4242% | $542,731 | $1,508 |
| 2030 (Y4) | $133,090,306 | $369,695 | 0.4157% | $553,366 | $1,537 |
| 2031 (Y5) | $138,413,918 | $384,483 | 0.4074% | $563,899 | $1,566 |

## Methodology (KEA notes page)
- 2026 anchor $92,993,300 = completed building per Ada County Assessment Notice (1/1/2026 lien
  date); 2026 tax applies 2025 confirmed levy 0.4507% (actual bill issues Nov 2026).
- **2027 = $120,625,000 = 96.5% of the $125M purchase price**, "consistent with Ada County assessor
  practice." Idaho is non-disclosure (no automatic sale-price notification) but Ada assessors have
  construction cost/loan/public-record access and routinely assess MF at/near completed cost.
- AV growth: +3.0% (2028, 2029), +4.0% (2030, 2031). Levy rate compresses ~2%/yr (Treasure Valley
  base-growth pattern), 0.4507% → 0.4074% by 2031.
- Levy 0.4507% = 11 districts; largest: Meridian City 0.1979%, Ada County 0.1483%, ACHD 0.0479%.
  Confirmed from 2025 consolidated bill (both Property Roll and Subsequent Roll at 0.004506896).
  No non-ad-valorem fees.
- Billing in arrears: Nov bill, due 12/20 (1st half) / 6/20 (2nd half). 2025 bills: $283,017.76
  (Property Roll, due 12/22/25) + $45,203.28 (Subsequent Roll, due 6/22/26). Closing late 2026 lands
  ~concurrent with the 2026 bill — **confirm proration treatment in the PSA**. Appeals: Ada BOE,
  deadline 4th Monday of June (Idaho Code §63-501A).

## How v6 uses it
Taxes tab reassmt % input 0.98873 (× $122M price = KEA's $120,625,000 exactly); AV growth vector
3/3/4/5/5% (2031 5% vs KEA 4% → model $569,195 CY2031 vs KEA $563,899, ~$5K conservative); rate
compression −2%/yr matching KEA. Model CY taxes 2027/2028/2029 tie to KEA to the dollar.

## Notes / implications
- Prior TMG assumption (v3 and the audit's step-up work): reassessment to 98% of price. KEA's
  96.5%-of-price on the $125M guidance lands at a HIGHER dollar AV than 98% × $122M — because it is
  anchored to guidance, not our price. At a $119M actual price, KEA's method implies 2027 AV
  ~$114.8M and 2027 taxes ~$507K (~$26K/yr less than modeled) — v6 is conservative for the submit.
- Supersedes (for deal UW) the audit's internally-derived step-up estimate ($117.6M AV /
  $519,411 2027 taxes in `tax_stepup_analysis.py` / CLAUDE.md anchors) — same asymmetry thesis,
  now with third-party support. Keep the audit work for the exit-side haircut rule.
- CBRE's lender UW (PLA 8/18) instead grows the in-place 2026 AV 5% per appraiser ($97.6M,
  $440K taxes) — a lender convention; do not mix with the KEA sale-reassessment case.
