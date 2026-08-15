# Replacement Cost & Construction-Finance Analysis — Treasure Valley
### Backed into from Yardi construction-loan data at 65% LTC · Aug 2026

**Source:** Yardi construction-loan export, 118 loans across 84 properties, Boise MSA
(Boise 46, Meridian 26, Nampa 23, Eagle 7, Caldwell 7, Garden City 4, Kuna 3, Star 2),
originations 2012–2026. Reproduce with
`python construction_loan_cost_analysis.py in/Boise_Construction_Loans_Yardi.xlsx`.

**Method.** Loans are aggregated per property (many deals carry 2–3 tranches), then
implied all-in cost = total loan ÷ 0.65, divided by unit count. Deals where subsidized
lenders (Idaho Housing/IHFA, federal/local government) fund >20% of the stack are
segmented out of the cost trend — their capital stacks are not 65% LTC. Three implausible
outliers excluded (partial/phased loans): Regency at River Valley ($46k/u),
Jules on 3rd ($694k/u), BB Living at The Oaks ($643k/u). Clean market-rate n = 68.

**Caveat on the 65% assumption.** Yardi reports the loan, not the budget. The *level* of
implied cost moves with the LTC assumption; the *escalation trend* does not (it scales
every year identically). Treat absolute $/unit as indicative, the trend as robust.

---

## 1. All-in cost per unit has roughly 2.5×'d in a decade

| Era | n | Median implied all-in $/unit |
|---|---|---|
| 2012–2016 | 10 | **$125,259** |
| 2017–2019 | 19 | $174,359 |
| 2020–2021 | 14 | $258,732 |
| 2022–2023 | 17 | **$299,145** |
| 2024–2026 | 8 | $259,288 * |

**2014 → 2024 median: $124,644 → $312,412 per unit = +151%, a 9.6% CAGR.**
Index (2014 = 100): 2016 = 138 · 2018 = 134 · 2019 = 162 · 2020 = 202 · 2021 = 222 ·
2022 = 234 · 2023 = 244 · **2024 = 251** · 2025 = 200*.

\* The 2024–2026 era median and the 2025 reading are **thin and mix-distorted** (n = 2 in
2025: Kuna Commons and Tauri, both suburban/townhome product on cheaper land). Do not read
the dip as deflation — the 2024 median ($312k) is the series high, and the deals that would
have printed high numbers in 2025–26 simply never financed (see §2).

## 2. The more important finding: construction finance has largely stopped

| Year | Deals financed | Units | Loan volume | **Inside the 5-mi ring** |
|---|---|---|---|---|
| 2018 | 7 | 1,386 | $117M | 4 deals / 1,092u |
| 2019 | 10 | 1,266 | $216M | 3 / 508u |
| 2021 | 14 | 2,249 | $496M | 2 / 185u |
| **2022** | **13** | **3,043** | **$555M** | **5 / 1,567u** |
| 2023 | 5 | 1,098 | $183M | **0 / 0** |
| 2024 | 7 | 1,025 | $193M | 1 / 125u (Wesley Ph II) |
| 2025 | 3 | 560 | $70M | 2 / 368u (Dorado*, Tauri) |
| 2026 YTD | 1 | 86 | $27M | **0 / 0** |

Valley-wide unit volume fell **~82% from the 2022 peak** (3,043 → 560 units in 2025).
Inside the subject's 5-mile ring, **only three construction loans have closed since
January 2023** — and one of them (Dorado Station) is 100% income-restricted.

**Subsidy is now carrying the market.** Affordable share of financed units:
25% (2014–19) → **5% (2020–22)** → **23% (2023–26)**. The only 2026 origination in the
entire dataset is The Finch (Roundhouse, 86u, Boise) — an IHFA-supported deal. Market-rate
garden product is not clearing the bar; LIHTC and gap-funded deals are.

## 3. The subject is at replacement cost — and that is the moat

**Seasons at Meridian** appears in the data: $66.61M construction loan, originated
**12/8/2022**, 360 units → **implied all-in ~$102.5M ≈ $284,657/unit** at 65% LTC.

- 2023+ market-rate median basis: **$282,439/unit** (n = 12) — the subject was built
  essentially *at* today's replacement cost, not below it.
- A merchant developer replicating it today faces ~$285–310k/unit all-in against a rent
  structure that has been flat-to-down since 2023 — which is precisely why the ring's
  pipeline is full of entitled-but-unbuilt deals, and why ~2,100 units died in-ring in
  2024–25 (see `graveyard_register.md`).

### Ring construction loans, 2012 → 2025 (the escalation, deal by deal)
$100k/u Retreat at Union Square (2012) → $126k Red Tail (2013) → $125k Heron Village (2014)
→ $101k Touchstone (2015) → $194k Stonesthrow (2016) → $141k Easton Village (2017) →
$174k Pennwood (2018) → $163k Silver Ridge (2019) → $215k Village East (2019) →
$227k Meritage West (2021) → $365k Telluride (2021) → $273k Altair (2022) →
$291k The Aren (2022) → **$285k Seasons at Meridian (2022)** → $430k Wesley Ph II (2024)
→ $247k Tauri (2025).

## 4. Underwriting implications
1. **New supply is capital-constrained, not just entitlement-constrained.** Every deal in
   the proposed pipeline must clear ~$285k+/unit basis; the ones that pencil are subsidized
   or land-advantaged (developer-owned land inside a master plan).
2. **The 2027–2029 delivery forecast should lean bearish.** Construction loans lead
   deliveries by ~18–24 months; the near-absence of 2024–2026 ring originations means
   2026–2028 ring deliveries are largely already knowable — and thin.
3. **Watch the loan tape, not the entitlement tape.** An approved project without a
   construction loan is not supply. This dataset is the cleanest early-warning signal we
   have; refresh it quarterly and reconcile against the Supply Chart's proposed rows.
4. **Replacement-cost support for the subject's basis** is genuine but not a rent thesis —
   costs justify *not building*, they do not by themselves push rents.

**Open items:** loan amounts are senior-stack as reported and may omit mezzanine/preferred
equity; a few properties carry phase-level loans that understate whole-project cost
(Dovetail's $129k/u is a Phase-level artifact); Yardi coverage of small (<50u) deals is
incomplete.
