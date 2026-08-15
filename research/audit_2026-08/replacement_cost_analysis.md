# Replacement Cost & Development Feasibility — Seasons at Meridian
### v2, Aug 2026 — rebuilt on the Emblem Meridian proforma. Supersedes the v1 flat-65%-LTC read.

**Sources:** (1) Yardi construction-loan export — 118 loans / 84 properties, Boise MSA,
2012–2026; (2) **Emblem Meridian equity book + merchant model** (Quarterra, 256u
garden+BTR, Meridian, underwritten 2026 for 2028 delivery) — the hard anchor.
Reproduce: `python construction_loan_cost_analysis.py in/Boise_Construction_Loans_Yardi.xlsx`
then `python replacement_cost_model.py`.

---

## What v1 got wrong
v1 applied a flat 65% LTC to every vintage and reported a 2025 median of ~$249k/unit.
Two errors: **(a) leverage is not constant** — Emblem's construction loan is
$42,877,793 against $77,959,624 of cost = **exactly 55.0% LTC**, so a flat 65% understates
post-2022 cost by ~18%; and **(b) product mix** — the thin 2024-25 sample was townhome and
small-infill product, not garden. Both are corrected here.

**The LTC schedule is now anchored on two real deals:**
| Vintage | LTC | Anchor |
|---|---|---|
| ≤2022 | 65% | Seasons' own $66.61M loan (12/2022) ÷ 0.65 = $102.5M, matching the "$100 million-plus" figure reported at groundbreaking |
| 2023 | 60% | transition vintage |
| 2024+ | **55%** | Emblem Meridian, $42.88M ÷ $77.96M = 55.0% |

**Comp screen** (to make the tape Seasons-comparable): market-rate only, 100+ units, core
submarkets (Boise/Meridian/Eagle/Garden City), conventional garden/mid-rise only. Excluded
with reasons logged in the script: student (LOCAL Boise), BTR (BB Living, Modern Craftsman
Black Cat), townhome (Tauri, Stonesthrow, Cimarron, Alpine Landing), downtown/urban infill
with structured parking (Jules on 3rd, Denton, North End Lofts, Boardwalk, Crosshatch, Mill
at Loggers Creek, Timbers at Harris Ranch), and loan artifacts (Regency partial, Dovetail
phase-level, Wesley Ph II spanning phases). Cohort n = 26.

---

## 1. The Emblem anchor — what a Meridian garden deal actually costs today

| | Total | Per unit | Per SF | % of cost |
|---|---|---|---|---|
| Land + acquisition | $9,092,960 | $35,519 | $38 | 11.7% |
| **Hard costs + 5% contingency** | **$54,579,077** | **$213,200** | **$227** | **70.0%** |
| Soft costs (A&E, permits/fees $4.46M, insurance $1.42M, interest, FF&E, O&A) | $14,287,587 | $55,811 | $59 | 18.3% |
| **TOTAL PROJECT COST** | **$77,959,624** | **$304,530** | **$324** | 100% |
| Construction loan | $42,877,793 | $167,491 | | 55.0% LTC |
| **Equity** | **$35,081,831** | **$137,038** | | **45.0%** |

## 2. Seasons at Meridian replacement cost ≈ $306k/unit ≈ $110M

Three independent routes converge tightly:

| Route | $/unit | Total (360u) |
|---|---|---|
| A — Emblem $/unit applied to 360 units | $304,530 | $109.6M |
| B — Emblem $/SF × Seasons' 931 avg SF | $301,935 | $108.7M |
| C — 2022 garden-cohort median escalated at the Seasons→Emblem rate | $311,699 | $112.2M |
| **Conclusion** | **~$306,000** | **~$110M** |

**Seasons' own 2022 basis was $284,658/unit ($102.5M).** Replacement cost today is
**+7.5%** — i.e. the subject is at, not below, replacement cost.

## 3. The corrected escalation curve (garden cohort, time-varying LTC)

| Era | n | Median $/unit |
|---|---|---|
| 2012–2016 | 7 | $125,874 |
| 2017–2019 | 9 | $163,805 |
| 2020–2021 | 4 | $272,510 |
| 2022 | 5 | $291,375 |
| 2026 (Emblem anchor) | 1 | $304,530 |

**The shape matters more than the level:** costs roughly **doubled 2014→2021** (~+9%/yr),
then **plateaued 2022→2026 (~+1.7%/yr)**. Development did not get harder because hard
costs kept exploding — they largely stopped. It got harder for the reasons below.

## 4. Why development is harder now — three mechanisms, quantified

**(a) Equity per unit +38%.** Cost rose modestly but leverage fell from 65% to 55%:
- 2022 vintage: $284,658/u × 35% equity = **$99,630/unit**
- 2026 vintage: $304,530/u × 45% equity = **$137,038/unit**

For a 360-unit Seasons clone that is **$49M of equity today vs $36M in 2022** — a
~$13M larger check for the same building, before any change in return hurdles.

**(b) The rent required to justify a new build exceeds what the market pays.**
Emblem underwrites a **6.65% yield on cost** — which on $304,530/unit demands
~$20,250 NOI/unit/yr (~$1,688/mo NOI). Emblem's underwritten gross rent is **$2,069/mo**
(939 SF, $2.20/SF, in 2028 dollars). **Seasons achieves $1,874/mo today** (931 SF, $2.01/SF,
95% occupied — from the equity book's own T-12 comp set). A new build needs
**~10% higher rents than the subject earns today**, plus three years of growth, just to
clear its own underwriting.

**(c) The margin is thin enough to fail on small errors.** 6.65% YoC against a 5.50% exit
cap is a **115bp spread → ~21% untrended development margin**. A 50bp cap move or a 5%
cost overrun erases most of it. That is why so many entitled deals sit: they pencil on
paper and fail at the investment committee.

## 5. Corroboration from the loan tape (v1 finding, still stands)
Construction-loan volume fell **~82% from the 2022 peak** (3,043 units financed in 2022 →
560 in 2025). Inside the 5-mile ring: **5 loans in 2022, zero in 2023, one in 2024, two in
2025, zero in 2026 YTD.** Affordable share of financed units went 5% (2020–22) → 23%
(2023–26); the only 2026 origination in the dataset is an IHFA-supported deal.
Emblem's own equity book corroborates independently: Meridian had **zero deliveries in
2025**, and the pipeline is "down nearly 50% from 2023."

## 6. Underwriting implications
1. **Seasons is at replacement cost (~$306k/unit, ~$110M)** — a buyer is not paying above
   the cost to rebuild, and a competitor cannot undercut the subject on basis.
2. **The supply moat is an equity-and-rent moat, not a cost moat.** New product needs
   ~10% more rent than the market pays; until rents rise or caps compress, entitled deals
   stay entitled. Track the loan tape, not the entitlement tape.
3. **What would break the moat:** a 100bp cap-rate rally or a ~10% rent surge would make
   the entitled pipeline (Pine 43, Outer Banks, Records, Emblem) financeable quickly —
   several of these are shovel-ready. Supply is deferred, not cancelled.
4. **Emblem is the closest live threat and its own book proves the point** — Quarterra
   underwrites 2028 delivery precisely because it expects supply scarcity in 2028-29.

**Caveats:** the LTC schedule is calibrated on two anchors, not a survey; Yardi reports
senior debt and may omit mezzanine/preferred; the 2023–25 core-submarket sample is thin
(n=4 before product screening), so the Emblem anchor — not the tape — carries the
"today" conclusion; opex/vacancy load in the required-rent math is assumed, not from the model.
