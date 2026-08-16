# Seasons at Meridian — Economy & Demand IC Deck: Extraction and Red-Team Notes

**Captured 2026-08-16** from `Seasons_at_Meridian__IC_Slides__Economy_and_Demand.html` (2 slides + footnotes).
Purpose: preserve every quantitative claim, the argument structure, and the vulnerabilities an IC member
could probe — so the deck can be defended (or corrected) without re-extraction.

## Slide 1 — Boise Economy (Where the Job Growth Comes From)

**QCEW jobs table (UI tax records, Ada + Canyon, Q4-25 vs Q4-24; ~97% coverage; pulled 8/14/26):**

| Sector | Jobs | % of growth | Avg wage (Ada) |
|---|---|---|---|
| Health care & social assistance | +4,161 | 45% | $66,560 |
| Construction | +2,159 | 23% | $93,860 |
| State + local government | +1,946 | 21% | $55–60K |
| Admin & support | +916 | 10% | $60,736 |
| Retail + wholesale | +896 | 10% | $50–107K |
| Food service + transport/logistics | +661 | 7% | $27–60K |
| Office economy & mfg (prof/finance/info/federal/mfg) | **−1,999** | — | $94–255K |
| **Total** | **+9,196** | **+2.4% YoY** | $70,637 blended |

Detail: St. Luke's $1.1B tower; Saint Alphonsus $450M program; hospital postings +44% YoY; construction
driven by Micron ID1/ID2 (~4,500 peak construction), $700M airport, Meta Kuna, District at Ten Mile; HP
exits '27; Micron direct ≈ 1.6% of metro jobs; state-gov line predates 2026 budget cuts (−7.4% YoY by
Jun-26 — deck itself flags "expect it to flip").

**CES payroll survey vs QCEW:** CES T3M YoY: 2021 +11.0% → 2026 +0.4%, vs QCEW +2.4%. Deck's argument: CES
is the outlier (shutdown collection break; birth-death model undercounted 9 of 10 fast-growth metros,
Boise worst at −1.4pp); CES re-benchmark to QCEW lands prelim 8/28/26, final early 2027.

**Population/migration (Placer.ai device panel, years ending June):** +15,390 (+2.0%) '22; +12,582 (+1.6%)
'23; +12,189 (+1.5%) '24; +13,042 (+1.6%) '25; **+18,769 (+2.2%) '26** — best of panel, ~4× US; net
domestic migration +11.6K (~2× YoY) — MSA #5 of 925 CBSAs; Ada #8 of 3,126 counties; base "Placer adjusted
853.6K."

**In-migration ZIPs (YE Jun-26):** #1 **83642 S. Meridian (subject): +2,417 net, +3.5%, accel +1,077**;
#2 83687 N. Nampa +1,604/+3.4%; #3 83706 Boise Bench +1,025/+2.8%; #4 83669 Star +836/+3.6%. Subject ZIP
absorbing at 2.4× metro rate; N. Meridian 83646 decelerated −511; ~1,100 HHs formed in 83642 in 12 mo.

**Origin metros (net YE Jun-26, prior yr, origin MHHI):** LA +670 (+980, $96K); SF +600 (+229, $136K,
2.6×); Riverside +523 (+541, $90K); DC +338 (+166, $127K, 2.0×); Seattle/Portland/Sacramento +801 (+310,
$97–115K, 2.6×). California = 47% of net inflow; in-mover HHI ≈ 1.0× incumbent.

**Labor tiles:** ID wage growth '25 +4.7% (3rd in US); MSA unemployment 3.4% vs US 4.4%; SW Idaho postings
+11% YoY; RNs #1 posted role.

**Catalysts (dated, committed vs announced):** Micron ID1 first DRAM 2027 (construction completes '26;
semis postings +92%); ID2 2028; Air Liquide $150–250M '28; Amazon same-day Nampa 400 jobs; Tractor Supply
DC 500; Meta Kuna +125MW; $1.55B hospital openings '28–30; $140M West Ada schools; +$74M FAA; TRI ~500
jobs; Heritage Square 120K SF + ~250u; ISU Meridian 950K SF; Franklin Sensors 90→180; Diode Kuna $1B+
(pre-construction); District Ph-1 '27 (Target, Life Time 200+, In-N-Out, 2 hotels, ~500K SF industrial);
SH-16 '27; Gowen F-16 '27; ValorC3 DC '27; Costco #2 late-26.

## Slide 2 — ZIP 83642 & the Seasons Tenant Base

**Source: seller Demographics Report w/Roommates 7/10/26 (305 units / 613 occupants; screened n=280) +
7/9/26 RR (95.0% occupied).**

- Median HH income $89,280 screened (see `Seasons-Demographics-Cohort-Analysis.md` for basis reconciliation)
- Median coverage **3.89× vs $1,915 Y1 UW rent**; 75% of HHs ≥3.0×
- Median age 27.5 (city 37.5); 51% aged 18–29; 50% dual-earner; 34% roommate HHs
- 366 distinct employers; largest 4.0% (St. Luke's, 19 residents); Micron-direct 2.0%
- Employer map counts: St. Luke's 19, Saint Alphonsus 13, Micron 10 (11 mi), Amazon 7, Chick-fil-A 5,
  Albertsons 5, ICCU 4, ICOM 4, Idaho State Police 4, West Ada SD 4, State of Idaho 4, Boise State 3,
  Starbucks 3, self-employed 10, gig 5, retired 5
- Industry capture (% employed tenants / % metro job growth / median screened HHI): Healthcare
  19.3%/45%/$100.8K; Construction 13.0%/23%/$101.1K; Food service 9.2%/4%/$81.7K; Tech/semis 8.4%/—/$90.8K;
  Prof services 8.4%/—/$98.1K; Government 7.5%/21%/$93.9K; Transport 6.1%/3%/$102.3K. (Healthcare workers
  individually median ~$55K; households ~$101K via dual-earner pairing.)
- Renter-HH formation 2,500–3,500/yr metro (internal method: QCEW + Placer channels) vs ~1,100 units
  delivering 2026; ~1,100 HHs formed in 83642 ≈ 7× the property's annual turn
- Own-vs-rent: >$2,000/mo spread ($550K Redfin Jul-26 median home ≈ $3,700+/mo at ~6.5% vs ~$1,700 rents);
  deck flags "rate-sensitive"
- First turn: 71% of initial leases carried ~1.2 mo free ($2,058 avg); burn-off → +9.5% renewal / +10.7%
  new-lease effective trade-outs; retention 42% cumulative (~50% recent months ex-July); 23 days avg vacant

## Argument structure (as built)

1. Jobs are real and well-mixed (QCEW hard count; Micron only ~1.6% direct)
2. Pre-empt the bear case (CES +0.4% is a survey artifact; benchmark scheduled)
3. Funded catalyst runway 2026→2030
4. Migration engine re-accelerating, fed by high-income coastal metros
5. Funnel to the subject: #1 in-migration ZIP is the subject's own
6. The rent roll proves it (industries mirror growth map; diversified employers)
7. Demand > supply; renting > owning
8. Already converting (burn-off trade-outs +9.5–10.7%)

## Red-team: gaps and vulnerabilities (keep private; prep answers)

- **Placer.ai dependence:** the entire population/migration/ZIP edifice is device-panel data,
  client-provided, no Census cross-check; ranks are Placer's own.
- **Renter-HH formation 2,500–3,500/yr is an internal estimate** (derivation not shown; ±40% range).
- **Jobs table vintage:** Q4-25 vs Q4-24 — 8 months old; the state-gov component (21% of growth) has
  since flipped (−7.4% YoY by Jun-26); no ex-government re-cut shown.
- **CES argument is unresolved by construction:** the vindicating benchmark lands 8/28/26–early '27 —
  after IC. If it doesn't revise up, +0.4% stands.
- **Micron indirect exposure never quantified:** construction (23% of growth) is heavily Micron build-out
  and rolls off after '26; '27–'28 catalysts are Micron-ecosystem; no permanent-job count anywhere.
- **Healthcare "diversification" is a two-system duopoly** (St. Luke's + Saint Alphonsus).
- **No supply side in the deck:** "~1,100 units delivering 2026" unsourced; no 2027–28 pipeline, no
  submarket vacancy/concessions. (Now covered by the supply slides + `Seasons-Proposed-Pipeline-Audit.md`.)
- **Subject's own history cuts against the tight-market frame:** 71% of initial leases concessed ~1.2 mo;
  retention 42% cumulative; "~50% recent months **ex-July**" quietly excludes the latest month.
- **Highest-wage sectors are shrinking** (office/mfg −1,999 at $94–255K; HP exits '27) — blended-wage
  impact unaddressed.
- **Employer resident counts are system-wide, mapped to nearest facility** (St. Luke's 19 ≠ facility census).
- **Incomes are screened application-time, n=280 of 305** — fine for cohort trends, stale for current
  coverage of long-tenured units.
- **No downside scenario:** migration reversal, rate cuts un-trapping the 18–29 cohort, Micron delay, or
  CES being right.
