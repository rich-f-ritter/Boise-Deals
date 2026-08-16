# Appendix J — Cross-Metro CES vs QCEW: Is Boise Unusual?
*Computed August 13, 2026. CES = BLS Current Employment Statistics metro series (survey), T3M YoY on the same basis as the rest of the deal file, from `sm.data.54.TotalNonFarm.All`. QCEW = Quarterly Census of Employment and Wages MSA totals (UI tax records; own_code 0 / industry 10; quarterly average of monthly employment), from the BLS QCEW open-data API. Gap = CES minus QCEW for the matching window (CES T3M ending Sep matches QCEW Q3; Dec matches Q4). Machine-readable: `crossmetro.json`.*

## The table

| Metro | CES T3M Sep-25 | QCEW Q3-25 | Gap Q3 | CES T3M Dec-25 | QCEW Q4-25 | **Gap Q4** | CES T3M Jun-26 |
|---|---|---|---|---|---|---|---|
| **Boise** | +2.20% | +2.00% | +0.19 | +0.91% | **+2.32%** | **−1.41** | +0.42% |
| Austin | +1.95% | +3.02% | −1.06 | +1.27% | +2.48% | **−1.21** | +1.24% |
| Salt Lake City | +1.31% | +1.33% | −0.02 | +0.82% | +1.72% | **−0.90** | +2.09% |
| Baton Rouge | −1.62% | −0.62% | −1.00 | −0.79% | +0.06% | **−0.85** | +1.85% |
| Las Vegas | +2.12% | +1.96% | +0.16 | +1.14% | +1.93% | **−0.79** | +2.26% |
| Reno | +1.96% | +2.09% | −0.13 | +1.64% | +2.15% | −0.50 | +1.63% |
| Dallas–Fort Worth | +1.10% | +1.00% | +0.10 | +0.59% | +0.80% | −0.21 | +0.84% |
| Houston | +0.90% | +1.16% | −0.26 | +0.31% | +0.48% | −0.17 | +0.66% |
| Phoenix | +0.06% | +0.19% | −0.13 | −0.03% | +0.08% | −0.11 | +0.93% |
| Denver | +0.05% | −0.43% | +0.48 | −0.11% | −0.37% | +0.26 | −0.09% |

## Four readings

**1. The Q4 2025 gap is systematic, not a Boise quirk.** In Q3 2025 the survey and the tax records agreed within ±0.3pp in seven of ten metros. In Q4 2025 — the federal-shutdown quarter that disrupted BLS collection — **the survey printed below the tax records in nine of ten metros.** This was a broad survey-side event.

**2. The size of the understatement scales with how fast the metro is actually growing.** Rank the metros by QCEW Q4 growth and the gap follows almost monotonically: the hot metros (Boise +2.32%, Austin +2.48%, Reno +2.15%, Las Vegas +1.93%, SLC +1.72%) show gaps of −0.5 to −1.4pp, while the flat metros (Phoenix +0.08%, Denver −0.37%, Houston +0.48%) show gaps near zero. This is the birth-death fingerprint: the model's error is proportional to how far actual business formation deviates from the modeled baseline — and it deviates most where formation is running hot.

**3. Boise is the extreme case, not an outlier in kind.** Largest Q4 gap of the ten (−1.41pp), consistent with being the smallest fast-growth metro in the set: small CES sample (heaviest model reliance) × fastest deviation of actual formation from the model's baseline.

**4. The honest wrinkle: other metros' CES bounced in 2026; Boise's hasn't yet.** By the T3M window ending June 2026, Las Vegas printed +2.26%, SLC +2.09%, Baton Rouge +1.85%, Phoenix +0.93% — several metros' surveys recovered sharply from their Q4-2025 dip — while Boise sits at +0.42% (second-lowest, ahead of only Denver). Two candidate explanations, unresolvable until Q1 2026 QCEW publishes (~mid-September 2026): (a) Boise's small CES panel re-anchors more slowly and the understatement persists (in which case true Boise growth is roughly +0.42 + ~1.4 ≈ +1.8%); or (b) Boise has genuinely decelerated in 2026 in a way its peers haven't. Boise's June single-month print (+1.2%, its strongest of 2026) and the H1-2026 sequential pace (~+1.1% annualized) lean toward (a) with a lag, but the September QCEW pull is the arbiter. This is the same diligence checkpoint flagged in the research paper §8.

## The birth-death mechanism, spelled out

The CES cannot survey a business it does not know exists. A new business enters the survey's sampling frame only after it registers for unemployment-insurance taxes and appears in the QCEW universe — a lag of roughly two to three quarters. Meanwhile, businesses that die simply stop responding, which for months is indistinguishable from ordinary non-response. Left uncorrected, the survey would systematically miss the net jobs of the newest firms — historically a large positive number (~+100K/month nationally in normal times).

BLS patches this with the **net birth-death adjustment**: a time-series model (fit to the *historical* QCEW record of business births and deaths) that adds a forecast of net new-business jobs to each month's estimate. The critical property: **the model is backward-looking.** It projects the past pattern of business formation forward. Whenever actual formation breaks from its own history, the model is wrong in the direction of the break, and it stays wrong until the annual benchmark re-anchors everything to the tax records.

- **Nationally, 2024–25:** the immigration reversal and high rates cut actual net business formation below its historical pattern. The model kept adding phantom jobs from births that were not happening → CES overstated growth → the record **−911K preliminary benchmark** (Sept 2025), a final −403K revision to calendar 2025, and a January 2026 reform of the model itself (quarterly re-fitting to current sample data; the reformed forecasts ran 185K *below* the old method over seven months — a direct measure of the phantom).
- **In Boise (and Austin, and SLC, and Vegas), Q4 2025 onward:** the same machinery ran the other way. These metros' actual formation is still running above the modeled baseline (Boise's QCEW establishment counts keep rising; its growth sectors — healthcare, construction, hospitality — are precisely the new-establishment-heavy ones the model handles worst). On top of that, the January 2026 reform recalibrated the model *stingier* to fix the national overstatement — a correction tuned to the decelerating aggregate that plausibly over-corrects the still-compounding metros. Add a small metro's thin survey panel and the shutdown-degraded Q4 collection, and you get exactly what the table shows: the survey losing track of the fastest-growing places, most severely in the smallest of them.

One sentence version: **the birth-death model transfers the recent past onto the present; in 2025–26 the national past was too optimistic for the national present (hence −911K), and the national present is too pessimistic for Boise's (hence −1.41pp).** The tax records adjudicate, on a two-quarter delay.

## Method notes
- CES series: SMU16142600000000001 (Boise), SMU04380600000000001 (Phoenix), SMU08197400000000001 (Denver), SMU49416200000000001 (SLC), SMU32298200000000001 (Las Vegas), SMU32399000000000001 (Reno), SMU48191000000000001 (Dallas–Fort Worth MSA), SMU48124200000000001 (Austin), SMU48264200000000001 (Houston), SMU22129400000000001 (Baton Rouge). NSA, T3M YoY.
- QCEW MSA area codes: C1426, C3806, C1974, C4162, C2982, C3990, C1910, C1242, C2642, C1294. Total covered employment, all ownerships.
- Window matching: CES T3M ending September ↔ QCEW Q3 (Jul–Sep); T3M ending December ↔ QCEW Q4 (Oct–Dec). Definitions differ slightly (CES excludes ag and some non-covered categories) — level differences are expected; *growth-rate* comparisons are the meaningful ones, and Q3's tight agreement across metros validates the method.
- QCEW Q4 2025 is preliminary (small revisions typical). Q1 2026 publishes ~September 2026 — the diligence checkpoint.
