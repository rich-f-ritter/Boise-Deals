# Replacement Cost & Development Feasibility — Seasons at Meridian
### v3, Aug 2026 — Emblem proforma VETTED and normalized; replacement cost revised up.
### (v2 took Emblem at face value. v1 used a flat 65% LTC. Both superseded.)

> **v3 headline changes:** (1) Emblem's proforma carries **~$351/unit/mo of ancillary income —
> +83% vs what the subject actually collects**; normalized, the market rent new supply really
> needs is **~$2,224/unit/mo, not the $2,069 advertised**, i.e. **+23.8% above the subject's
> market rent**, not the ~10% v2 implied. (2) Emblem's tax **rate** is fine (0.45%, matches TMG's
> own), but its assessed-value **ramp** lags actual construction by ~$212k across lease-up, and the
> sale-triggered reassessment it never bears costs a buyer $47,891/yr ≈ $871k of exit value. (3) Replicating
> *Seasons specifically* costs **~$322,530/unit (~$116.1M)**, above the raw Emblem number, because
> of the subject's amenity package and superior land. Detail: `emblem_normalization.py`.

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

---

# v3 ADDENDUM — Vetting the Emblem underwriting

## A. The ancillary-income problem (the whole story)

Emblem's proforma advertises a $2,069/unit market rent. It clears its 6.80% yield on cost only
because it also books **$350.59/unit/month of ancillary income**. The subject collects
**$191.94/unit/month (T12)** — Emblem is **+83%**.

| $/unit/month | Emblem | Seasons actual | Normalized | Why |
|---|---|---|---|---|
| Garage / covered parking | 86.72 | 25.87 | **45.00** | Emblem charges 536 spaces (2.09/unit) at $41.42 — nearly every stall paid. Suburban Meridian garden competes with free surface parking; defensible = garages ~$100/mo at ~45% penetration |
| RUBS / utility billback | 95.79 | 45.61 | **65.00** | $95.79 ≈ 100% recovery of a ~$114/u utility load; market recovery is 55–70% |
| Managed WiFi (bulk internet) | 108.00 | — | **45.00** | Gross charge has an offsetting ISP cost inside utilities (Emblem utilities $114/u/mo vs subject $66); only net margin is comparable |
| Pet fees | 10.50 | — | **10.50** | market |
| Other income | 49.58 | 50.95 | **50.00** | in line |
| *(subject Revenue Share — the WiFi analogue)* | — | 69.50 | — | already reflected above |
| **TOTAL** | **350.59** | **191.94** | **215.50** | |

The normalized figure ($215.50) is still a **12% premium to the subject**, which new construction
earns through better submetering and real garages. It is simply not +83%.

## B. Expenses — Emblem is conservative, and the tax RATE is fine
My v2 suspicion that Emblem understated the tax **rate** was **wrong**. Emblem underwrites
**0.45%** on market value; **TMG's own Seasons model uses the identical 0.45%** (Taxes tab), and
the subject's actual effective rate is 0.41% ($384,244 on $92.99M assessed). Insurance ($481/u vs
subject $328/u) and total opex ($8,281/u vs subject $5,608/u, **+48%**) are both **conservative**.

## B2. Taxes — testing the assessed VALUE, not just the rate
Three separate tests; the assessed value is light in **timing**, not in level:

**(a) Construction-completion lag — $211,898 deferred.** The tax study assumes the assessor
recognizes **27%** of improvements for tax year 2029 when the construction curve says **~47%**
is actually built, and **73%** for 2030 when **~99%** is built:

| Tax yr | Assumed complete | Actually built | Assumed improvement value | Tax understated |
|---|---|---|---|---|
| 2029 | 27% | ~47% | $14,797,000 | **$97,025** |
| 2030 | 73% | ~99% | $51,731,000 | **$114,872** |
| | | | | **$211,898** |

This lands squarely in the lease-up years, where merchant-developer IRR is most sensitive.

**(b) Stabilized assessed value — light vs its own exit, but consistent with Idaho practice.**
$89,670,000 = **$350,273/unit** — 115% of its own cost but only **87% of its own $400,391/unit
exit value**. Before calling that aggressive: **the subject sits at 80% of market while unsold**
($258,315/u assessed vs a $321,222/u price). So 87% on a no-sale hold is normal for Idaho.
**Not the smoking gun.**

**(c) The real exposure — the sale-triggered step-up Emblem never bears.** Idaho reassesses to
~98% of sale price (TMG models exactly this for the subject). On a $102.5M exit the **buyer's**
assessed value steps to $100,450,000 (**$392,383/u**) and taxes to **$471,025 ($1,840/u)** versus
Emblem's terminal **$423,134 ($1,653/u)** — **$47,891/yr the buyer eats, worth $870,745 of value
at a 5.50% cap ($3,401/unit)**. Emblem's exit is overstated by roughly that much.

**(d) Sanity check:** Emblem's stabilized $1,653/unit still exceeds the subject's $1,413/unit
post-reassessment run-rate. **The per-unit level is fine; the aggression is in the timing.**

## C. What market rent does new supply REALLY need?

Holding Emblem's own 6.80% yield-on-cost target and normalizing only the ancillary stack:

- Ancillary shortfall: **$464,242/year**
- Tax normalization (assessor keeps pace with construction): **$67,719/year**
- → NOI falls to $4,814,751 → **YoC drops to 6.18%**
- To hold 6.80%, base market rent must rise **$175/unit/mo (2030 $)**
- **Required market rent today: ~$2,224/unit/mo ($2.37/SF)** vs the $2,069 advertised (**+7.5% understated**)

| Compared to the subject's **market** rent (HelloData, per the TMG model) | Gap new supply must clear |
|---|---|
| T12 (6/30/26) $1,752 | **+27.0%** |
| T6 annualized $1,796 | **+23.8%** |
| YE2026 $1,818 | **+22.3%** |

**So the feasibility gap is ~22–27%, not the ~10% v2 reported.** New market-rate supply in this
submarket needs roughly **$2,225/unit/mo of market rent** — about $430/unit/mo above where the
subject's market rents sit — before a merchant developer earns a normal return. That is the
moat, quantified correctly, and it is far deeper than v2 suggested.

## D. Seasons replacement cost — the case for MORE than the raw Emblem number

Emblem is a *middle-income-targeted* product; Seasons is *resort-style*. Replicating the subject:

| | $/unit |
|---|---|
| Emblem all-in cost (base) | 304,530 |
| + Amenity/spec premium — subject has a 10,000 SF clubhouse + 30,000+ SF community space (golf simulator, resort pool, dog parks) vs Emblem's 7,300 SF clubhouse; ~55 extra SF/unit at $250–300/SF | +14,000 |
| + Land premium — Eagle/Overland node with I-84 frontage and Village/Topgolf adjacency vs Emblem's Eagle/Victory site; the touching WinCo parcel is being marketed for **retail** ground lease, which prices above MF land | +6,000 |
| − Density/scale efficiency — 360 units at 23/acre vs Emblem 256 at ~20/acre | −2,000 |
| **SEASONS REPLICA COST TODAY** | **$322,530** |

**≈ $116.1M for 360 units; sensible range $315k–$330k/unit ($113M–$119M).**

## E. Basis vs replacement — the punchline

| | $/unit | Total |
|---|---|---|
| Subject's actual 2022 development cost | $284,658 | $102.5M |
| **Replacement cost today** | **$322,530** | **$116.1M** |
| **TMG purchase price** | **$327,778** | **$118.0M** |
| TMG total basis (price + closing + capex) | $333,614 | $120.1M |
| *(whisper price)* | *$347,222* | *$125.0M* |

**We are acquiring at ~+1.6% vs replacement cost; total basis is +3.4% above it.**
*(Correction: an earlier draft used $115.64M as the price — that is the post-sale **assessed**
value, i.e. 98% of the $118.0M actually being paid.)* The subject is not being bought at a
discount to replacement, it is being bought slightly **through** it — and the protection comes
entirely from the fact that **no merchant developer can start here until market rents rise ~25%**.

---

# F. THE SALE-TRIGGERED TAX STEP-UP — the structural transfer, and we are living it

Idaho reassesses to **~98% of sale price** on transfer. That single rule means a merchant
developer's exit proforma is **structurally optimistic**, because it capitalizes an NOI carrying
the *development-era* assessment while the buyer inherits a stepped-up bill.

## F1. The worked example is our own deal
| | |
|---|---|
| Purchase price | **$118,000,000** ($327,778/unit) |
| Assessed BEFORE sale | $92,993,300 — only **79%** of what we are paying |
| Assessed AFTER sale (98% of price) | $115,640,000 |
| Taxes, T12 (the seller's load) | $384,244 ($1,067/unit) |
| Taxes, post-reassessment | $510,754 ($1,419/unit) |
| **Step-up we absorb** | **$126,510/yr (+33%, $351/unit)** |

That $126,510 comes **straight out of our NOI** and therefore our cap rate:
- Capitalized at our 5.01% Y1 cap = **$2,526,511 of value ($7,018/unit)**
- Y1 NOI is $6,013,812; un-stepped it would be $6,140,322
- **Going-in yield on basis: 5.007% actual vs 5.113% un-stepped — 11 bp we hand to the seller**

The seller capitalized an NOI carrying the old tax load. We pay for the step-up in perpetuity.

## F2. The same arithmetic destroys part of Emblem's exit
Emblem's $102.5M exit at a 5.50% cap implies **$5,637,500** of NOI — carrying Emblem's terminal
tax of $423,134. A buyer is reassessed to 98% of whatever they pay, so the honest price solves a
circularity (price → assessment → tax → NOI → price):

| | |
|---|---|
| Buyer's price at a **true** 5.50% cap | **$101,693,890** ($397,242/unit) |
| Buyer's assessed value | $99,660,012 |
| Buyer's taxes | $467,470 (vs Emblem's $423,134) |
| **Emblem's exit is overstated by** | **$806,110 ($3,149/unit, 0.8%)** |

If Emblem holds out for $102.5M, the buyer's real going-in cap is **5.453%, not 5.50%**.

## F3. What it does to feasibility
- Development margin: **+31.5% stated → +30.4% buyer-adjusted**
- $806,110 of profit erased = **2.3% of the $35.1M equity check**
- Restoring it needs $44,336 more NOI = **+$14.11/unit/mo** of market rent (2026 dollars) —
  stacked on top of the ancillary and tax-lag normalizations

**The general rule for every deal in the supply chart:** in Idaho, roughly **0.8–1.0% of a
developer's exit value (≈2–3% of the equity check) transfers to the buyer at closing** via
reassessment. Developer exit assumptions in this market should be haircut accordingly — and our
own underwriting already models the mirror image, which is why Seasons' taxes jump 33% on day one
and stay there.

**Caveats:** the amenity and land premiums in section D are analyst estimates, not bid documents;
the normalized ancillary stack is judgment calibrated to one comparable (the subject's own
actuals); Emblem's 6.80% YoC is its 2030 figure (the book advertises 6.65%), and using 6.65%
would lower the required rent by roughly $40/unit/mo.
