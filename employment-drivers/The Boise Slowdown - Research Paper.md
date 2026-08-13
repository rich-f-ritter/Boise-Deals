---
title: "The Boise Slowdown: Signal, Noise, and the Story Beneath the Trailing Three-Month Number"
subtitle: "Employment research for the Seasons at Meridian acquisition · Boise City MSA"
author: "Prepared for Milestone — Seasons at Meridian deal file"
date: "August 13, 2026"
---

# Executive Summary

The trailing-3-month (T3M) year-over-year payroll growth figure for the Boise MSA — **+0.42% as of the window ending June 2026**, down from +2.48% a year earlier — prompted this investigation: is there a story behind it, and a cause? There is. Six findings, in order of importance:

**Finding 1 — A large share of the measured slowdown is a measurement artifact, and the hard data says Boise was still growing ~2.4% through the end of 2025.** The CES survey figures behind the T3M number diverged abruptly from the QCEW hard counts (actual unemployment-insurance tax records covering ~97% of jobs) beginning in Q4 2025 — precisely when the 43-day federal shutdown disrupted BLS data collection. QCEW shows Ada County **+2.51%** and Canyon County **+2.09%** year-over-year in Q4 2025, versus the CES print of +0.91% for the same window. At the sector level the divergence is starker: QCEW shows Ada County health care **+7.1%**, construction **+6.7%**, and accommodation & food services **+2.0%** — the three sectors CES portrays as collapsing. Boise's CES history will be re-benchmarked to these hard counts in early 2027; the expected direction is a **substantial upward revision**.

**Finding 2 — The remainder of the slowdown is real, and it is overwhelmingly national — a labor-supply event, not a Boise demand failure.** A shift-share decomposition shows Boise's *local* outperformance collapsed from **+7,900 jobs/year** (window ending June 2025) to **+700** (June 2026): had Boise's sectors merely grown at national rates, it would have added +1,061 jobs; it added +1,733. The national stall itself is historic — calendar-2025 US payroll growth was **+181,000 for the entire year** after benchmark revisions — and its dominant cause is the immigration reversal: net US migration went **negative in 2025 for the first time in at least fifty years**, cutting break-even payroll growth from ~250K/month (2023) to roughly **zero**. Boise, a metro whose growth premium is imported through in-migration, decelerates mechanically and at higher amplitude when the national migration engine stops.

**Finding 3 — What is genuinely soft locally is specific, identifiable, and mostly policy- or weather-driven.** Four sectors account for the entire measured deceleration: government (Idaho's ~$4B of cumulative tax cuts produced a projected deficit and 4% agency cuts — state government employment is **−7.4%** YoY, federal −5.0%), leisure & hospitality (consumer discretionary churn plus the worst ski winter in years — *not* a tourism collapse; Boise Airport set its fourth consecutive passenger record), education & health (a Medicaid contract change, small-provider closures, and big-system cost discipline — while hospital job postings run **+44%** YoY), and construction (normalization from an extreme 2024–25 pace, plus the Micron/Exyte contract termination). Meanwhile the QCEW hard counts locate the *true* local softness where CES shows strength: **finance (−1.8%), professional services (−1.5%), and manufacturing (−1.4%)** — consistent with the HP exit, Albertsons erosion, and tech consolidation documented in the v2 memo.

**Finding 4 — The labor market is supply-constrained, not demand-collapsed.** The labor force is contracting (−0.8% T3M), participation fell a full point in six months (62.8% → 61.8%), ICE enforcement is at unprecedented levels in Idaho, and the population is aging — yet unemployment sits at 3.4% (US: 4.4%), job postings are **up 11%** year-over-year, and Idaho's wage growth is the **third-fastest in the nation**. Prices rising while quantities stall is the signature of a supply constraint. For an apartment owner this distinction is decisive: a supply-constrained labor market with fast wage growth supports rents; a demand collapse would not.

**Finding 5 — The timeline matters: the trough is behind us on current data.** The sequential run-rate bottomed in H2 2025 (−0.3% annualized — the shutdown, the Exyte termination, the state fiscal-year cuts) and recovered to **~+1.1% annualized in H1 2026**. The T3M YoY figure of +0.42% carries the H2-2025 trough in its base and mechanically understates the current pace.

**Finding 6 — The 2027–2030 catalyst stack is unusually visible.** Micron's first Boise DRAM output (mid-2027) with semiconductor job postings already +92%; the ID2 fab (2028); ~$1.55B of hospital openings (2028–2030); the District at Ten Mile Phase 1 (spring 2027); SH-16 freeway completion (2027); the Gowen Field F-16 mission (2027); and the $700M airport program. Nationally, the re-acceleration channels are immigration normalization, rate cuts, and tariff sunset. IDOL's own forecast is +1.2%/year; with break-even payroll growth near zero, even modest prints in 2027 will coincide with a tight labor market.

**Underwriting synthesis:** the defensible reading of Boise employment for underwriting purposes is a **true current growth trend of roughly +1.5% to +2.5%** (hard-count basis), against a published CES figure of +0.4% that is likely to be revised up. We recommend underwriting to **+1.0–1.5%** — below the hard-data trend for conservatism, above the artifact-depressed CES print — while recognizing that Boise apartment demand is only partially payroll-coupled (retirees, remote workers, and priced-out would-be buyers rent without appearing in local payrolls). This paper also corrects the prior memo's replacement-cost analysis (Section 9): institutional replacement cost for a Seasons-equivalent is **~$300–340K/unit**, Class A 2020s-vintage clearing prices in Ada County are **~$250–340K/unit**, and a ~$328K/unit valuation is replacement-cost *parity* at the metro's best node — while the construction pipeline sits at 2–3.5% of inventory because development math remains broken by a 25–35% rent gap.

---

# 1. The Number in Question

All figures below are computed directly from raw BLS Current Employment Statistics (CES) state-and-area flat files (series IDs in Appendix A of the deal file's `appendix/E`), as the 3-month average ending in the stated month versus the same 3-month average one year earlier (NSA-on-NSA; the aligned windows make the comparison seasonally clean).

| T3M window ending | YoY % | YoY jobs |
|---|---|---|
| Jun 2023 | +2.85% | +10,933 |
| Dec 2023 | +3.24% | +12,667 |
| Jun 2024 | +2.70% | +10,633 |
| Dec 2024 | +1.77% | +7,133 |
| Jun 2025 | +2.48% | +10,033 |
| Sep 2025 | +2.20% | +8,933 |
| Dec 2025 | +0.91% | +3,733 |
| Mar 2026 | +0.51% | +2,067 |
| **Jun 2026** | **+0.42%** | **+1,733** |

Two features stand out. First, the deceleration is not gradual: the series holds above +2% through September 2025 and then loses 1.3 points in a single quarter. Second, the collapse window (Q4 2025) coincides with three simultaneous events: the 43-day federal government shutdown (October 1 – November 12, 2025, which disrupted BLS collection — the Boise labor-force series is literally missing October 2025), the Micron/Exyte contract termination (effective September 2, 2025; 200+ layoffs), and the arrival of Idaho's state fiscal austerity. That coincidence motivates the first and most important question: how much of the measured cliff is real?

# 2. Finding 1: The Measurement Artifact

## 2.1 Two datasets, one economy

CES — the source of every headline payroll number and of the T3M figure — is a *survey* of ~120,000 businesses nationally, extrapolated with a "birth-death" model for firms too new to be sampled. It is benchmarked once a year to the QCEW — the Quarterly Census of Employment and Wages — which is not a survey at all but the administrative record of unemployment-insurance tax filings, covering roughly 97% of jobs. Between benchmarks, CES for a mid-sized metro like Boise rests on a thin local sample plus modeled small-business behavior.

QCEW hard counts for the Boise MSA's two principal counties (pulled from the BLS QCEW open-data API for this paper):

| County | Q3 2025 YoY | Q4 2025 YoY | Q4 2025 jobs added |
|---|---|---|---|
| Ada | +2.13% | **+2.51%** | +7,306 |
| Canyon | +1.79% | **+2.09%** | +1,890 |
| **Combined** | **+2.05%** | **+2.41%** | **+9,196** |

Against this, CES printed +2.20% (T3M ending Sep 2025) — closely aligned with QCEW — and then **+0.91% for the window ending December 2025, a gap of 1.5 percentage points against the tax records for the identical period.** The divergence opens in exactly the quarter the shutdown disrupted collection.

## 2.2 The sector-level evidence is more striking than the total

QCEW by sector, Ada County, Q4 2025 vs Q4 2024 (private ownership):

| Sector | QCEW Q4 2025 YoY | CES narrative for the same period |
|---|---|---|
| Health care & social assistance | **+7.14%** (+3,186) | "sharp deceleration" |
| Construction | **+6.65%** (+1,502) | "halving" |
| Accommodation & food services | **+2.03%** (+514) | "collapse" |
| Arts, entertainment & recreation | +0.92% | collapse |
| Retail trade | +0.01% | — |
| Manufacturing | −1.38% | flat-to-positive |
| Professional/scientific/technical | −1.54% | improving |
| Finance & insurance | −1.83% | improving |
| Educational services | −2.29% | — |

The surveys disagree *in both directions*. CES understates the sectors where new-establishment growth is concentrated (health care, construction, hospitality — precisely the sectors the birth-death model handles worst in a fast-growth metro), and overstates the white-collar sectors. The QCEW picture — booming healthcare and construction, growing hospitality, genuinely soft finance/professional/manufacturing — is also the picture that matches the observable facts on the ground: ~$1.55B of hospital construction, the Micron buildout, record airport traffic, versus the HP exit announcement, Albertsons erosion, Clearwater's take-private, and Kount/Cradlepoint shrinkage.

## 2.3 The national benchmark asymmetry

Nationally, the benchmark story runs the *other* way: the March 2025 preliminary benchmark was **−911,000** (the largest on record), the final benchmark cut calendar-2025 growth by 403,000, and BLS reformed the birth-death model in January 2026 (quarterly updates; the reformed model's forecasts ran 185K below the old method). Nationally, CES had been *overstating* growth during the immigration reversal. This is not a contradiction of the Boise finding — it is its complement: the birth-death model over-imputes new-business jobs where business formation is slowing (the national aggregate) and under-imputes where formation is still running hot (Boise, where QCEW establishment counts keep rising). Small-area CES noise then compounds the problem. The Chicago Fed's caution applies to both: in a period of population-control turbulence, the unemployment rate is currently a more reliable cyclical signal than the payroll delta. Boise's is 3.4%.

Additional corroboration that the "collapse" is partly statistical: Idaho DOL itself flagged that a portion of the 2026 labor-force decline reflects **BLS population-model benchmark revisions** rather than behavior ("Idaho receives benchmark adjustments for 2025 labor force statistics," April 6, 2026), and the state-level Business Employment Dynamics data — which do show a soft Q3 2025 (statewide net −6,800 private jobs) — measure statewide quarterly net change, dominated by seasonal and non-metro components, and are not inconsistent with positive metro-level YoY growth in the tax records.

## 2.4 What to expect, and when

The CES state-and-area benchmark that will re-anchor Boise's 2025–26 history to the QCEW arrives with the **March 2026 reference-period benchmark, published in early 2027**. Given a demonstrated 1.5-point gap through Q4 2025, the base case is a material upward revision to Boise's late-2025/2026 payroll history. QCEW for Q1 2026 (publishing September 2026) and Q2 2026 (December 2026) are the near-term checkpoints: **we recommend re-pulling Ada/Canyon QCEW in mid-September 2026** — during diligence — to test whether the hard counts stayed near +2% into 2026. If they did, the CES +0.42% should be discounted heavily. If QCEW too has rolled over toward +1% or below, the slowdown is more real than this paper's base case and the conservative end of the underwriting range applies.

*Caveats in the other direction, stated plainly:* QCEW Q4 2025 is preliminary and subject to (historically small) revision; unauthorized workers exiting covered employment depress QCEW itself, meaning neither dataset fully captures the enforcement effect; and 2026 CES weakness cannot be directly tested against QCEW until September 2026. The finding is not "the slowdown is fake"; it is "the level of the cliff is exaggerated by the survey, and the tax records show a metro still compounding at roughly twice the published rate through the last verifiable quarter."

# 3. Finding 2: The Real Slowdown Is National — a Labor-Supply Event

## 3.1 Shift-share: Boise's growth premium evaporated; Boise did not break

A shift-share decomposition asks: if each Boise sector had grown at its national sector's rate, what would Boise's total growth have been, and how much did Boise deviate locally?

| T3M window ending | Expected at national rates | Actual | Local residual |
|---|---|---|---|
| Jun 2025 | +2,165 | +10,033 | **+7,869** |
| Jun 2026 | +1,061 | +1,733 | **+673** |

Boise still outgrows the nation — the local residual remains positive — but the *premium* collapsed by ~7,200 jobs/year. Sector-level residuals (window ending June 2026) show where Boise still outperforms and where it does not:

| Sector | US T3M YoY | Boise T3M YoY | Local residual |
|---|---|---|---|
| Financial activities | −1.03% | +2.17% | **+3.20pp** |
| Other services | +0.69% | +2.59% | +1.90pp |
| Construction (incl. mining/logging) | +0.44% | +2.32% | +1.89pp |
| Trade/transport/utilities | −0.16% | +1.70% | +1.86pp |
| Prof & business services | +0.13% | +1.08% | +0.95pp |
| Government | −1.03% | −0.74% | +0.29pp |
| Manufacturing | −0.40% | −0.32% | +0.08pp |
| Information | −2.96% | −4.44% | −1.49pp |
| Education & health | +2.28% | +0.65% | **−1.63pp** |
| Leisure & hospitality | +0.88% | −4.18% | **−5.06pp** |

Boise outperforms the nation in seven of ten sectors — including construction (Micron) and, notably, the office-economy sectors in the CES data. Its two measured underperformances are leisure & hospitality (a −5pp local residual — Section 4 shows this is one part real local churn, one part the ski winter, and one part survey artifact) and education & health (which the QCEW contradicts outright). **The proximate cause of the Boise T3M slowdown is that the United States stopped adding jobs.**

## 3.2 Why the nation stalled: the supply side

The national record is stark: after final benchmarks, **US payrolls grew by 181,000 jobs in all of calendar 2025** (vs +1.46M in 2024); the trailing-12-month average as of July 2026 is +34K/month; the July 2026 print was −23K. Yet the unemployment rate has held between 4.1% and 4.6%. Jobs growth near zero with a stable unemployment rate is arithmetically possible only if labor-force growth is near zero — which it is:

- **Net US migration turned negative in 2025 for the first time in at least half a century** (AEI/Brookings: −295K to −10K; CBO: ~+400K; the Dallas Fed estimates net *unauthorized* migration averaged **−55K/month in H2 2025**, heading to −89K/month by mid-2026).
- **Break-even payroll growth** — the monthly gain needed to hold unemployment steady — fell from ~250K/month in 2023 to approximately **zero** (Dallas Fed: ~−3K/month average Aug–Dec 2025; St. Louis Fed 2026 range: 15–87K; Fed Board concurs).
- Fed Chair Powell's Jackson Hole framing — a "curious kind of balance" from "a marked slowing in both the supply of and demand for workers," attributed "much more" to immigration — remains the canonical description.

Demand is not absent from the story — the hires rate touched 3.1% in February 2026 (matching the April 2020 low), the private diffusion index spent most of 2025 below 50, and the "low-hire, low-fire" regime is hard on new entrants — but the supply-side signature (stable unemployment, slowing labor force, top-decile wage growth in supply-constrained states) dominates, nationally and in Idaho.

## 3.3 The other national channels, briefly

- **Federal workforce and spending:** the federal civilian workforce shrank ~10% (−238K) in 2025; the Washington DC metro is −3.0% YoY — the country's worst — cleanly identifying the channel. Idaho, a federal-lands state with ~11–14K federal civilian jobs concentrated in Boise (BLM, Forest Service, NIFC), imports this directly: Idaho federal employment is −5.0% YoY.
- **Tariffs:** effective rates reached ~14.3% (highest since 1939) before the February 2026 Supreme Court decision struck the IEEPA tariffs (replaced at ~10.5%); manufacturing employment fell for a third consecutive year (magnitude of tariff attribution contested — see Contested-Claims Register); tariff passthrough pushed the Fed's 2026 PCE projection to 3.6%, freezing the policy rate at 3.50–3.75% through 2026 to date.
- **Rates:** mortgage rates ≥6% throughout; May 2026 housing starts printed the lowest since May 2020. (Construction *employment* nationally held up better than starts partly because enforcement shrank the construction labor force even as demand fell — a supply cushion with obvious Idaho relevance.)
- **AI and entry-level hiring:** credible occupation-level evidence of displacement among young workers in exposed occupations (Stanford/ADP: ~16% relative decline for ages 22–25 in the most-exposed roles); no consensus aggregate effect (Yale Budget Lab finds none). We assign it no payroll-point estimate.

# 4. Finding 3: What Is Genuinely Soft Locally — Four Sectors, Four Causal Chains

The contribution decomposition isolates the deceleration precisely. Between the windows ending June 2025 and June 2026, total T3M growth fell 2.06 points. The sector contributions:

| Sector | Contribution, Jun-25 window | Contribution, Jun-26 window | Swing |
|---|---|---|---|
| Education & health | +0.97pp | +0.10pp | **−0.87pp** |
| Leisure & hospitality | +0.15pp | −0.43pp | **−0.57pp** |
| Construction | +0.66pp | +0.22pp | **−0.44pp** |
| Government | +0.23pp | −0.10pp | **−0.33pp** |
| Manufacturing | +0.12pp | −0.02pp | −0.14pp |
| All other sectors (net) | +0.35pp | +0.63pp | **+0.28pp** |
| **Total** | **+2.48pp** | **+0.42pp** | **−2.06pp** |

Everything outside four sectors *improved*. The four:

## 4.1 Government (−0.33pp swing): a self-inflicted fiscal squeeze — the clearest causal chain

Five years of Idaho income-tax cuts (~$4B cumulative, including $450M+ in 2025) met a revenue slowdown; by October 2025 the state projected an unconstitutional $56.6M FY2026 deficit. The response: holdbacks, then 4% cuts to most agencies ($131.3M) in the 2026 session. **State government employment: −7.4% YoY (June 2026).** Federal: −5.0% (DOGE-era RIFs; Interior cut ~2,000 with BLM reductions concentrated in state offices; the shutdown furloughed Forest Service/BLM statewide). Local: three school bonds failed in November 2025; West Ada has lost 1,213 students since 2022–23 (~$2.5M less state funding next year); Boise State closed one college and merged two others in March 2026. This is policy, not economy — and its impulse largely resets: the FY2026 cuts annualize, and Idaho state revenues stabilize or the legislature cuts again, but a second −7% state-government year is not the base case.

## 4.2 Leisure & hospitality (−0.57pp swing): churn plus snow, not a tourism collapse

The real components: a consumer discretionary pullback hitting mid-market dining (P.F. Chang's, Blaze Pizza, ~50 documented Boise-area closures in 2025, after 58 restaurant closures in 2024 — the BLS BED data confirm establishment closures drove the losses); the **worst ski winter in years** (Bogus Basin at ~40% of average snowfall; statewide arts/entertainment/recreation −9.3% YoY); and cost pressure on low-margin operators after two years of 4–5% wage growth. What it is *not*: a visitation decline — Boise Airport set its fourth consecutive record (5.2M+ passengers in 2025) and January 2026 ran ahead of January 2025. And per Section 2, QCEW shows Ada County accommodation & food services *up* 2.0% through Q4 2025 — the CES collapse overstates whatever churn is real. A snow-normal 2026–27 winter mechanically reverses the recreation component.

## 4.3 Education & health (−0.87pp swing): a hiring pause the tax records don't confirm

The identifiable real pieces: Blue Cross of Idaho's 135 layoffs after losing the Medicaid dual-eligible contract; small-provider closures (BED: closing establishments accounted for 4,818 gross losses in Q3 2025 statewide); big-system cost discipline at St. Luke's and Saint Alphonsus (no layoffs or formal freezes found — attrition management, with Fitch noting "ongoing cost containment"). The counter-evidence: **QCEW Ada County health care +7.1% YoY in Q4 2025** and hospital job postings +44% YoY in April 2026 with RNs the top-posted occupation. Forward risks are real and dated: Medicaid work requirements effective January 2027, provider rate cuts July 2027, OBBBA federal Medicaid cuts from 2027 (partially offset by Idaho's ~$186M/year from the Rural Health Transformation Program). Forward supports are equally dated: the $1.1B St. Luke's tower (2029–30 opening), the $450M Saint Alphonsus program (2028), both of which must staff up ahead of opening.

## 4.4 Construction (−0.44pp swing): normalization, not rollover

From +7.4% (T3M Jun 2025) to +2.3% — still the metro's growth leader, and QCEW says +6.7% through Q4 2025. The real events: the Micron/Exyte GC termination (200+ construction-management layoffs September 2025; Hoffman took over; total site headcount effect not public), single-family permit softness (West region −20% YoY in January 2026), and the multifamily pipeline collapse (a supply-side positive for this deal). The committed pipeline — Micron ID1/ID2, both hospital programs, the airport, Meta/Diode, the District — underwrites the sector's floor through at least 2028.

## 4.5 Where the softness actually is

The QCEW cross-section (Section 2.2) locates the genuine local weakness in **finance & insurance (−1.8%), professional/scientific/technical services (−1.5%), manufacturing (−1.4%), and educational services (−2.3%)** — the white-collar office economy. This is exactly the pattern the v2 memo documented anecdotally: HP's announced exit (~1,100–1,700 jobs by end-2027), Albertsons corporate erosion, Clearwater's take-private, Cradlepoint/Ericsson and Kount/Equifax shrinkage, Wells Fargo ops wind-downs. For Seasons specifically, this is the demand segment to watch — the corridor's office parks — though Section 2's caution cuts both ways: CES shows these same sectors *improving*, and the truth likely sits between.

# 5. Finding 4: A Supply-Constrained Labor Market

The evidence assembles into a consistent picture:

| Indicator | Reading | Signal |
|---|---|---|
| Labor force (T3M YoY) | −0.79% | contracting supply |
| Labor-force participation (Idaho) | 62.8% → 61.8% (Jan–Jun 2026) | contracting supply |
| Household employment (derived, T3M YoY) | −0.86% | fell before payrolls |
| Unemployment (T3M) | 3.4% (US 4.4%) | no slack build |
| Initial claims (Idaho, April 2026) | ~776/week | no layoff wave |
| Job postings (SW Idaho, April 2026) | +11% YoY (28,057) | demand present |
| Hospital postings | +44% YoY | demand present |
| Semiconductor postings | +92% YoY | demand present |
| Wage growth (Idaho, 2025) | +4.7%, 3rd-fastest in US | prices rising as quantities stall |

Rising job postings, rising wages, flat unemployment, and a shrinking labor force describe an economy short of workers, not short of jobs. The supply channels: the national migration reversal (Idaho's in-migration continues — United Van Lines still ranks Idaho top-inbound — but smaller and older, with family/retirement now the top stated reasons; retirees add population and housing demand without adding labor force); unprecedented ICE enforcement (the Wilder raid, October 2025; construction-site actions in Eagle/Emmett, August 2026; the Idaho Dairymen's Association telling legislators up to 70% of dairy labor may be unauthorized); aging (wages fell from 61% to 56% of Idaho personal income, 2010–2025, as retirement income grew); and a statistical component IDOL itself flags (population-model revisions).

**Implication for the asset:** a supply-constrained labor market with top-3 wage growth is materially better for apartment demand than the payroll number implies. Renters' incomes are rising ~4–5%/year; the people not appearing in CES payrolls (retirees, remote workers, the self-employed) still lease apartments; and school-enrollment declines in West Ada — driven by housing costs pricing out young families — are, perversely, a renter-retention signal for the own-vs-rent spread documented in the v2 memo.

# 6. Finding 5: Timeline and Momentum — the Trough Is Behind Us on Current Data

Sequential momentum (T3M level vs. six months prior, annualized, NSA — compared against like halves to control seasonality):

| Period | Annualized pace |
|---|---|
| H2 2024 (Jun→Dec 2024) | +2.84% |
| H1 2025 (Dec 2024→Jun 2025) | +2.12% |
| **H2 2025 (Jun→Dec 2025)** | **−0.29%** |
| **H1 2026 (Dec 2025→Jun 2026)** | **+1.13%** |

The contraction was concentrated in H2 2025 — the quarter of the shutdown, the Exyte termination, the state fiscal cuts, and (per Section 2) degraded survey collection. H1 2026 is running at roughly +1.1% annualized, and June 2026 printed +1.2% YoY single-month, the year's strongest. Because the T3M YoY statistic carries the H2-2025 trough in its base for another two quarters, **the published number will look worse than the current pace through year-end 2026 even if nothing further improves.**

# 7. Finding 6: The Forward Catalyst Stack, 2027–2030

Boise's near-term catalysts are unusually dated and visible; the honest column of risks sits beside them.

**Catalysts:** Micron ID1 first DRAM output mid-2027 (~2,000 permanent fab jobs ramping through 2028+; semiconductor postings already +92%, and IDOL projects a 400–500-person semiconductor-tech shortage); Micron ID2 (late 2028); St. Luke's tower and Saint Alphonsus Nampa/Meridian openings staffing up 2028–2030; District at Ten Mile Phase 1 (spring 2027 — Target, Life Time, hotels); SH-16 freeway completion (2027); Gowen Field F-16 conversion (2027); airport program through 2029; Meta Kuna operational (late 2026). Nationally: immigration normalization (the single biggest swing factor — Brookings' 2026 scenarios span ~1.1M workers/year), Fed cuts if tariff-driven inflation fades post-Section 122 expiry, and the fiscal impulse CBO expects in 2026–27.

**Risks:** a second state-budget-cut year; OBBBA Medicaid cuts landing on hospital margins from 2027; memory-cycle risk at Micron (deeply cyclical; the 2022–23 downturn produced Boise layoffs); construction air-pocket post-2028 when the megaprojects deliver simultaneously; the white-collar erosion continuing (HP exit completes 2027); and the national break-even logic cutting both ways — with labor-force growth near zero, any national demand shock translates quickly into negative prints.

**Interpretation discipline for 2027:** with break-even near zero, a healthy 2027 labor market may print only +30–70K/month nationally and low-single-digit thousands in Boise. Judge slack by the unemployment rate, participation, and wage growth — not the payroll delta.

# 8. Underwriting Synthesis

1. **The employment growth number to carry:** the hard-count trend through the last verifiable quarter is ~+2.4%; the artifact-depressed CES print is +0.42%; the sequential 2026 pace is ~+1.1%. We recommend **+1.0–1.5%/year** as the underwriting assumption — deliberately below the hard-data trend — with **+2.0–2.5%** as the upside case if the September 2026 QCEW confirms continuation, and ~0% as the stress case (which, note, the market already survived in H2 2025 with 94%+ occupancy and stable rents).
2. **Diligence checkpoint (September 2026):** re-pull Ada/Canyon QCEW Q1 2026. This single free data pull is the highest-information test available of whether the slowdown is artifact or real, and it lands during a typical diligence window.
3. **Demand is only partially payroll-coupled.** Absorption of ~2,500 units/year against near-zero measured job growth in 2025–26 is itself the proof: migration (including non-working migrants), household un-bundling, and the $1,500–1,900/month own-vs-rent spread drive Boise apartment demand alongside payrolls.
4. **The wage story is the rent story.** Third-fastest wage growth in the nation, concentrated in a supply-constrained market, is the fundamental support for the ~3% rent growth the metro is printing — and for more once the 2026–27 supply trough bites.
5. **Watch the white-collar column.** The QCEW-confirmed softness (finance, professional services) maps to the subject's corridor office parks. The v2 memo's watch list (HP wind-down, Albertsons, Blue Cross landing spot, Meridian-South office backfill) remains the right early-warning set for the top of the subject's renter income distribution.

# 9. Corrigendum: Replacement Cost and Class A Clearing Prices

The v2 memo asserted that Boise trades cleared at $165–222K/unit (~$200K average) against replacement cost of ~$220–280K/unit, and characterized at/above-replacement pricing as a 30–60% premium to market. **That analysis was wrong**, and this section replaces it.

## 9.1 Why it was wrong

The range came from a single brokerage report (Lee & Associates Q2 2025) whose trailing-12-month "top transactions" consisted of three sub-institutional deals: a 2017-vintage 2-story Nampa asset ($165K/unit), a 102-unit 2023 build in west Boise ($221.7K/unit — only ~$205/SF), and a 76-unit infill deal ($200K/unit). Idaho is a non-disclosure state; the public tape is thin and skews small, old, and Canyon County. The same brokerage's own quarterly series printed **$348K/unit average in Q1 2025** — the quarters in which institutional newer-vintage product actually trades triple the average.

## 9.2 The corrected Class A record

Institutional-size, 2018+ vintage Ada County trades (prices mostly undisclosed — Idaho non-disclosure — buyers/sellers verified):

| Date | Property | City | Units | Vintage | Parties |
|---|---|---|---|---|---|
| Feb 2021 | Indigo → Cortland South Meridian | Meridian (Overland/Ten Mile) | 336 | ~2019 | Cortland (buyer) |
| Jun 2021 | Kennedy Wilson portfolio (Lofts at Ten Mile, Jasper, Towne Sq + dev site) | Meridian/Boise | 640+ | 2018–20 | $143M reported (~$210K+/unit blended) |
| Jan 2022 | Prelude at Paramount | Meridian | 280 | 2018/19 | Pacific Development Partners ← Brighton/Pacific Partners (IPA) |
| Jun 2022 | The Addison + Franklin at Ten Mile | Boise + Meridian | 605 | <5 yrs old | Cortland (buyer) |
| Dec 2024 | Verraso Village (BTR, avg 1,840 SF) | Meridian | 96 | 2016/18 | MJW ← undisclosed (3.2% assumable) |
| **Dec 2025** | **Prelude at Paramount** | **Meridian** | **280** | **2018** | **The Milestone Group ← Pacific Development Partners (IPA)** |

Milestone's own Prelude print — above $222K/unit for a 2018-vintage asset at ~1,016 SF average units — is fully consistent with this record and with the only reported-price 2020s trade ($205/SF): $222K/unit on Prelude is only ~$219/SF. **The defensible clearing range for 150+ unit, 2020s-vintage Class A garden product in Ada County is approximately $250–340K/unit ($230–300/SF)**, with the Eagle/I-84 and Ten Mile nodes at the top of the band.

## 9.3 Replacement cost, rebuilt from local anchors

- **Seasons itself cost "$100 million-plus" for 360 units at January-2023 pricing — ≥$278K/unit** (developer, via Multifamily Dive). Escalated at 3–5%/year, today's rebuild is **~$305–330K/unit**.
- Village Apartments (336-unit, 4-story, Meridian): a **$202K/unit senior construction loan alone** (2022); at 60–65% LTC → ~$300–335K/unit total cost.
- Roundhouse (2023): building a Fowler-equivalent costs "100–125% more" than its 2015 bid.
- Suburban Meridian MF land at Seasons density: ~$25–40K/unit; construction financing at ~7%.

**All-in for a Seasons-equivalent today: ~$300–340K/unit.** A ~$328K/unit valuation is therefore **replacement-cost parity, not a premium to it** — at the metro's most supply-protected node (per the location-premium memo: ~26 acres of by-right MF land within 1.5 miles, zero 10+ acre sites).

## 9.4 The development math stays broken — which is the thesis

Against ~$320K/unit cost and a required ~6.0–6.5% yield-on-cost (vs a ~5.2% market cap), new construction needs ~$2,500–2,700/month blended rents versus ~$1,950–2,000 in place at Seasons — a **25–35% rent gap**. That is why metro completions fell 64% in 2025, under-construction inventory sits at 2–3.5% of stock, and Seasons' own entitled Phase 2 (351 units) remains parked in concept design. Local cap-rate context: TOK pegs Treasure Valley multifamily at ~5.2% (2025); at $328K/unit, a realistic Seasons NOI implies ~4.7–5.2% — inside the quoted Class A band.

**Corrected bottom line:** the buyer at ~$328K/unit is not paying 30–60% over the market; they are paying approximately what the asset would cost to build, in a market where nobody can build (the rent gap), at the node where nobody could build even if the math worked (the land moat). The prior framing — "the premium must show up in rents because it will not show up in basis" — inverts: **basis at replacement parity plus a dead pipeline is the margin of safety**, and the employment findings of this paper (supply-constrained labor market, wage growth, artifact-depressed payroll prints, 2027–30 catalyst stack) support the demand side of that thesis.

---

# Appendix I: Methodology

**T3M construction:** 3-month arithmetic mean of NSA CES employment ending in the stated month, compared to the identical window one year prior. Sources: BLS SM flat files (`sm.data.13.Idaho`, `sm.data.54.TotalNonFarm.All`), series IDs in `appendix/E` of the deal file; US comparisons from FRED (PAYNSA and SA supersector series for shift-share).

**Shift-share:** expected sector change = Boise sector base employment (prior-year T3M) × national sector T3M YoY growth; local residual = actual − expected. National sector rates use SA series (YoY comparisons are insensitive to seasonal adjustment).

**QCEW:** BLS QCEW open-data API, county area files (16001 Ada, 16027 Canyon), total covered employment = own_code 0 / industry 10, quarterly average of the three monthly employment levels; sector rows own_code 5 (private), 2-digit NAICS. Q4 2025 is the latest available quarter (published June 2026); Q1 2026 publishes ~September 2026.

**Household employment:** derived as labor force × (1 − unemployment rate) from FRED BOIS216LFN and BOIS216URN (LAUS). October 2025 is missing from the source series (shutdown-period gap).

**Momentum:** T3M level vs the T3M level six months earlier, annualized ((a/b)² − 1); NSA, therefore compared only against like halves of prior years.

# Appendix II: Contested-Claims Register

1. **AI displacement magnitude** — occupation-level effects credible (Stanford/ADP); aggregate effect unproven (Yale Budget Lab finds none). No payroll attribution assigned.
2. **Tariff job-loss attribution** — direction (negative-to-zero for manufacturing) is consensus; magnitude contested (CAP −89K vs Cato/AEI near-zero).
3. **2025 net migration level** — Brookings (−295K to −10K) vs CBO (+400K); enforcement-driven voluntary exit is the swing variable.
4. **Supply vs demand shares of the national stall** — Fed/Goldman lean supply; COVID-low hires rate argues meaningful demand weakness. Treated as joint.
5. **Boise QCEW-CES divergence** — our artifact finding rests on preliminary Q4 2025 QCEW; it reverses only if QCEW revisions are unusually large or Q1–Q2 2026 QCEW confirms the CES cliff.
6. **Micron site headcount post-Exyte** — termination and 200+ layoffs documented; net site construction employment change not public.

# Appendix III: Evidence Gaps

1. Boise hotel occupancy/RevPAR 2025–26 (STR data needed).
2. Ada–Canyon building-permit counts for 2025–H1 2026 (COMPASS/Census BPS pull recommended).
3. Formal hospital-system hiring-policy statements (none public; visible only in aggregate data).
4. Quantified immigration-enforcement employment effects for the Boise MSA.
5. Prelude at Paramount price confirmation (non-disclosure; client holds the actual figure).
6. Paired Eagle-vs-Ten-Mile land comps (CoStar pull recommended).

# Appendix IV: Source Base

This paper synthesizes three commissioned research streams (national causes; Boise local causes; Class A comps & replacement cost — preserved in full with URLs as deal-file appendices G, H, and I), the two prior research streams behind the v2 memo (appendices A–D), and original computation (appendix E + `t3m_sectors.json`). Principal primary sources: BLS (CES flat files, QCEW API, BED, OEWS, JOLTS, benchmark documentation), FRED, Idaho Department of Labor (releases, EORAC 2026 outlook), Idaho Capital Sun, BoiseDev, Idaho Statesman/Press, Idaho EdNews, Dallas/St. Louis/Cleveland/Chicago/KC Federal Reserve Banks, Brookings/AEI, CBO, Yale Budget Lab, Stanford Digital Economy Lab, IPA/Marcus & Millichap, Lee & Associates, TOK Commercial, CBRE, Colliers, MMG, REBusinessOnline, Multi-Housing News, Multifamily Dive, and City of Meridian records. ~200 distinct citations across the appendix set.
