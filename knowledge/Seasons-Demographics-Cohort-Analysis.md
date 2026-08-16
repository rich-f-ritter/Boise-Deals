# Seasons at Meridian — Move-In Cohort Income Analysis

**Run 2026-08-16.** Sources: `Seasons_at_Meridian_Demographic_Analysis.xlsx` (Data – Households tab,
screened income) joined to `RentRoll08_04_2026` (move-in date, first row per unit). Demographics report
vintage 7/10/26; move-ins after 7/10/26 excluded (income data cannot cover them).

## Method

- Join key: unit number. 284 income-reporting units in the demo workbook; 357 units with move-in dates on
  the 8/4 RR.
- Exclusions: 4 units moved in after the 7/10 report date; 4 units reporting $0 income; 1 unit not on the
  RR; unit **B307 already excluded at source** ($2.9M "household income" under a business name — flagged
  "Suspect income – excluded from screened"). No other screened income exceeds $400K.
- Clean sample: **n = 275** households.
- Incomes are screened at application (move-in), so a cohort comparison is like-for-like: each cohort's
  income is measured at its own entry date. The staleness critique of screening data does not apply to a
  cohort trend (it applies to using old incomes for *current* coverage).

## Results

| Move-in cohort | n | Median HHI | Mean HHI | Median age | Median rent | Coverage |
|---|---|---|---|---|---|---|
| 2024 (lease-up) | 13 | $86,400 | $80,737 | 26.8 | $1,995 | 3.61× |
| 1H25 | 63 | $74,400 | $92,433 | 30.1 | $1,715 | 3.62× |
| 2H25 | 105 | $92,700 | $101,805 | 27.2 | $1,695 | 4.56× |
| 1H26 | 91 | $95,004 | $100,695 | 29.4 | $1,699 | 4.66× |
| Jul-26 | 3 | $120,000 | $166,712 | 30.1 | $2,180 | 4.59× |

**Headline comparisons:**

- **CY-26 move-ins: median $96,618 (n=94) vs pre-2026 standing base $86,400 (n=181) = +11.8%.**
- T12 move-ins (Aug-25+): median $93,000 (n=181) vs earlier residents $83,208 (n=94) = +11.8%.
- Distribution: CY-26 p25/50/75 = $69,960 / $96,618 / $121,242 vs pre-2026 $65,256 / $86,400 / $120,000 —
  the middle of the distribution moved, not the tail.
- Share of households ≥$100K: **CY-26 49% vs pre-2026 39%.**
- CY-26 median coverage vs $1,915 Y1 UW rent: **4.20×**.
- Median age flat across cohorts (~27–30): same renter profile, higher income — not a demographic shift.

## Interpretation

The income low point is the **1H25 cohort ($74,400)** — signed at peak concessions (~1.2 months free on
71% of initial leases), when discounted effective rents qualified lower-income applicants. As concessions
burned off (67/67 leases concessed a year ago → 0/49 now), entering incomes stepped up for three
consecutive cohorts while coverage never fell below ~3.6×. This is the direct rebuttal to "concession
burn-off will drive attrition/credit risk": pricing discipline has been upgrading the tenant base.

## Median HHI basis reconciliation (why different documents show different medians)

| Basis | Median | Source |
|---|---|---|
| **Screened (canonical)** | **$89,280** | Analysis workbook Data – Households, n=280 |
| Workbook Summary tab | $88,638 | Same file, slightly different exclusion set |
| Model Demographics Summary tab | $87,684 | v3 model, its own exclusion set |
| As-reported | $93,288 | Inflated by data-entry errors — do not use |

The deck's 3.89× median coverage = $89,280 ÷ ($1,915 × 12) exactly — so **$89.3K is the number that makes
the deck internally consistent.** ACS benchmark: Meridian renter median $61,922 → base screens ~44% above
the local renter median.

## Caveats

- **Survivorship:** the pre-2026 median is measured on residents still in place at 8/4/26 — the comparison
  is "recent move-ins vs the standing base," not "vs everyone who ever lived here." (This is also the
  comparison that matters for forward revenue.)
- Jul-26 cohort is n=3 — directional only, do not quote alone.
- The 2024 cohort (n=13) is the surviving remnant of lease-up-era signings (42% cumulative retention), not
  a representative 2024 sample.
- Screened income excludes 23 occupant records reporting >$15K/mo that are almost certainly annual
  salaries entered as monthly (per the workbook's Data Quality tab); the source report also contains a
  cartesian join inflating raw rows ~52% — the workbook's cleaned tabs handle both.
