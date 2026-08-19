# Seasons at Meridian — CBRE Debt Quote (PLA) vs. TMG Underwriting

**Source:** CBRE Preliminary Loan Analysis dated **8/18/2026** (`CBRE PLA 8.18.26.pdf`, 5 pp:
loan sizing grid, CBRE operating-statement UW, T12, tax summary, net-rental-collections detail).
**Compared against:** live TMG model `in/TMG_Seasons_at_Meridian_v3.xlsm` (v3, re-uploaded 8/15/2026),
Financing tab. Analysis date 8/19/2026.

---

## Bottom line

1. **Pricing came in *better* than the model; proceeds came in *worse*.** The model carries a
   5-yr fixed, full-term-IO loan at **$76.74M @ 5.40%** (Tsy 4.40% + 1.45% gross spread − 45bp
   buydown, 2.6% fees). CBRE's closest execution — Freddie 5-yr CME max leverage with buydown —
   prices at **5.31%** (Tsy 4.37% + 1.40% spread − 46bp buydown @ 2% cost) but sizes to only
   **$73.31M gross / $71.84M net**. That is **−$3.4M of proceeds** vs. the model.
2. **The proceeds cut is entirely a lender-NCF re-underwrite, not spread widening.** The model's
   debt sizing is toggled to CBRE's DSF NCF of **$6,157,303 (as of 8/5/26)** (Financing C51).
   This PLA cuts the same CBRE DSF As-Is NCF to **$5,766,584 — a $390,719 (−6.3%) haircut in
   13 days.** At the model's own 6.419% constant and 1.25x DSCR, the new NCF supports only
   ~$71.9M. **Get the 8/5 → 8/18 NCF bridge from CBRE** — we do not have the 8/5 backup to
   decompose it.
3. **Estimated LIRR impact ≈ −65 to −70bp (≈ 11.21% → ~10.5%)** on the Freddie 5-yr bought-down
   execution: equity rises ~$4.3M (proceeds −$3.44M plus ~$0.9M more upfront cost: 2% buydown +
   2% closing ≈ $2.93M vs. the model's $1.995M financing fees), partly offset by −$255k/yr of
   IO interest (5.31% on $73.3M vs. 5.40% on $76.7M). Two independent calibrations of an annual
   levered-CF replica of the model (one matched to the 11.21% LIRR, one to the 8.20% UIRR) both
   land the delta at −0.65% to −0.70%. Without the buydown the delta is ≈ −0.9%; a LifeCo
   max-leverage execution ≈ −1.2%.
4. **A further ~$1.0M proceeds risk is hiding in the tax line.** CBRE underwrites RE taxes at
   **$440,067** (in-place 2026 AV of $92.99M grown 5% per appraiser = $97.6M AV — i.e. **no
   sale-triggered step-up**). Our own work (`tax_stepup_analysis.py`, and TMG models it) has the
   2027 roll stepping to ~$117.6M AV → **$519,411**. If the lender's appraiser catches the
   step-up, NCF drops $79,344 → ~**−$1.0M of proceeds** at the bought-down constant. Treat
   quoted proceeds as the ceiling, not the floor.
5. **The quote is sized at the $125M whisper, not our $120M bid — and it doesn't matter for
   proceeds.** Every fixed-rate column is DSCR-constrained (1.25x amort), not LTV-constrained,
   so proceeds are price-invariant. At our $120M bid the bought-down Freddie loan is 61.1% LTV
   (vs. 58.6% at $125M), still inside the 65% cap. CBRE's "As-Is NCF Cap Rate 4.61%" on $125M
   coincidentally equals our T3 TMG-adj cap — different numerator (their NCF), same optics.

---

## The menu (9 executions quoted)

| Execution | Loan | Rate | Structure | Binding constraint | LTV @$125M |
|---|---|---|---|---|---|
| **Freddie 5-yr fixed (CME max lev)** | $69.315M | 5.77% (UST+1.40%) | Full-term IO, 35-yr am, defeasance | 1.25x amort DSCR | 55.5% |
| **→ with 46bp buydown @2.00%** | **$73.305M** | **5.31%** | same | 1.25x | 58.6% |
| Freddie 7-yr fixed | $68.427M | 5.88% (UST+1.35%) | IO 6-7?, 35-yr am, defeasance | 1.25x | 54.7% |
| Freddie 7-yr floater | $68.427M | 5.45% (SOFR+1.80%) | 1-yr lockout, 1% | fixed-rate-equiv DSCR | 54.7% |
| Fannie DUS T2 5-yr | $68.902M | 5.82% (UST+1.45%) | IO 2-5, 35-yr am, YM | 1.25x | 55.1% |
| → with 45bp buydown @2.00% | $72.765M | 5.37% | same | 1.25x | 58.2% |
| Fannie DUS T2 7-yr | $68.023M | 5.93% (UST+1.40%) | IO 6-7, 35-yr am, YM | 1.25x | 54.4% |
| LifeCo max leverage 5-yr | $76.888M | 6.37% (UST+2.00%) | IO 3-5, 30-yr am, YM, 65% LTC | 7.50% as-is DY / 1.00x | 61.5% |
| LifeCo lower-leverage 5-yr | $67.756M | 5.87% (UST+1.50%) | Full-term IO, 30-yr am, YM | 55% LTV/LTC, 8.0% DY | 54.2% |
| Debt fund 70% LTV | $87.5M + $1.71M FF = $89.21M | 6.15% (SOFR+2.50%) | 3+1+1, full IO, min-interest | 70% LTV / 6.25% DY | 70.0% |
| Debt fund 65% | $79.54M + $1.71M FF = $81.25M | 6.00% (SOFR+2.35%) | 3+1+1, full IO | 7.25% as-is DY | 63.6% |

Rates as of 8/18/26: 5-yr UST 4.37%, 7-yr 4.53%, SOFR 3.65%, 30D avg SOFR 3.64%.

**Reading the menu:**
- **Freddie 5-yr with buydown is the model's structure and the best fixed-rate proceeds/rate
  combination.** It matches the model loan exactly in form: effective ~11/1/26 close, 5-yr term,
  full-term IO, 35-yr amort constant for sizing, exit at 10/31/2031 = maturity. Two caveats vs.
  the model: (a) Freddie fixed is **defeasance**, not the YM + 3-mo open the model assumes —
  costless if we exit at maturity as underwritten, expensive if we sell early (footnote 2: flex
  prepay quotes available on request — get them); (b) footnote 3: **all agency sizings assume
  the 35-yr amort waiver is granted.** At 30-yr amort the sizing constant rises ~6.3%→~6.7% and
  proceeds drop ~$4M. Confirm waiver likelihood with CBRE.
- **The buydown is a proceeds play, not a rate play.** $1.466M (2%) buys 46bp for 5 yrs ≈ $337k/yr
  ≈ NPV-neutral on rate alone, but sizing at the lower constant adds **+$3.99M of proceeds**
  (CBRE shows $2.52M "benefit of buydown" net of cost). LIRR is ~25bp better with the buydown
  than without (~10.55% vs ~10.3%). Take it.
- **LifeCo max leverage is the only quote that matches the model's proceeds ($76.9M vs $76.7M) —
  at 6.37%, 97bp over the model rate,** with only 3 yrs IO and a 30-yr amort tail. Costs ~120bp
  of LIRR. Only interesting if proceeds are the binding objective.
- **Debt funds are negative leverage** at a 4.61% going-in NCF yield: 6.00-6.15% coupon,
  0.88-0.99x amort DSCR, min-interest prepay. They also fund the $1.71M capex. Not our profile
  for a stabilized 2024 asset; useful only as a bridge if agency sizing deteriorates further.
- **Agency affordability tailwind:** 100% of units ≤120% AMI, 45.6% ≤80% AMI → **45.6%
  mission-driven**, which is what supports the tight 1.40% spread. The 7-yr Freddie floater at
  SOFR+1.80% = 5.45% with 1-yr lockout is the sale-flexibility alternative if defeasance flex
  prices badly.

## CBRE's NCF vs. ours ($5.767M vs. the model)

CBRE UW (col "Projected"): GPR $7,593,540 (8/4/26 RR annualized) − concessions $39,724 (T1 level)
− **vacancy 5.75%** ($434,344) − bad debt $24,505 → NRI $7,094,967; + other income $1,013,485 (T3)
= EGI $8,108,452; − expenses $2,269,868 (28%) = **NOI $5,838,584**; − $200/u reserves = **NCF
$5,766,584**.

vs. TMG Y1 (Financing tab): revenue $8,344,342, expenses $2,383,348, reserves $90,000 → CF before
DS $5,870,994.

| Line | CBRE UW | TMG Y1 (debt-sizing) | Note |
|---|---|---|---|
| Revenue/EGI | $8,108,452 | $8,344,342 | CBRE −2.8%: 5.75% UW vacancy vs. actual 3.3% econ-vac trend; T1 concessions carried |
| Expenses | $2,269,868 | $2,383,348 | CBRE **lighter** — almost entirely the tax line ($440k vs. our $519k post-step-up) |
| Taxes | $440,067 | $519,411 | **CBRE has no sale reassessment** — the ~$1.0M proceeds risk above |
| Insurance | $174,600 ($485/u) | — | Borrower Y1 PF, +48% over T12 $118k — lender took the PF number |
| Reserves | $72,000 ($200/u) | $90,000 ($250/u) | PCA could move CBRE's number |
| **NCF** | **$5,766,584** | **$5,870,994** | CBRE −1.8% vs. TMG; −6.3% vs. CBRE's own 8/5 figure |

The T12 pages confirm the lease-up shape we underwrote: economic occupancy 57.6% (Jul-25) →
93.4% (Jun-26), concessions burned off from 9.4% of GPR (Sep-25) to ~2.5%, T3 NRI +4.3% over T6.
Physical occupancy 96.67% on the 8/4/26 rent roll. Nothing in the operating history argues with
our revenue UW; the fight with the lender is vacancy factor (5.75% vs. ~4%) and the concession
trail (they UW to T1 concessions, which is favorable).

## What this does to the deal (at our $120M bid)

| | Model (Financing tab) | Freddie 5-yr w/ buydown | Delta |
|---|---|---|---|
| Proceeds | $76.74M | $73.31M gross | −$3.44M |
| Rate (all-in) | 5.40% | 5.31% | −9bp |
| IO interest/yr | $4.20M | $3.95M | −$255k |
| Upfront debt cost | $1.995M (2.6%) | ~$2.93M (2% buydown + 2% est. closing) | +$0.94M |
| Equity | $45.75M ($127k/u) | ~$50.1M (~$139k/u) | +$4.3M (+9.5%) |
| LIRR | 11.21% | **~10.5%** | **−65 to −70bp** |

(LIRR deltas from an annual replica of the model's levered cash flows, calibrated two ways —
to the model's 11.21% LIRR and separately to its 8.20% UIRR; both give −0.65% to −0.70%.
Directionally robust; re-run inside the live model for the IC number.)

## Action items

1. **Ask CBRE for the 8/5 → 8/18 DSF NCF bridge** ($6,157,303 → $5,766,584). If it's the
   insurance PF + 5.75% vacancy + reserves, there may be room to claw back with the 8/4 RR,
   T3 collections support ("Support Req. @ Close" is noted on every T3-based line) and a PCA.
2. **Update the model's Lender Debt Sizing NOI (Financing C51) to $5,766,584** and re-run —
   proceeds fall to ~$71.9-73.3M depending on whether the buydown constant is reflected; re-cut
   LIRR/equity for IC.
3. **Pressure-test the two agency assumptions that flatter the quote:** the 35-yr amort waiver
   (footnote 3) and the missing tax step-up (worth ~$1.0M of proceeds if caught by appraisal).
4. **Get the flex-prepay iteration** (footnote 2) priced vs. defeasance — our 10/31/2031 exit
   sits at maturity, but the Q2 risk case (5.50% exit cap world) may argue for sale flexibility;
   the 7-yr floater at 5.45% is the benchmark to beat.
5. Decision framing for IC: the quote confirms the model's *rate* (actually 9bp inside it) and
   its *structure*, but the market clears ~$3.4M less *proceeds* than underwritten. At ~10.5%
   LIRR the deal still works at $120M; it leans harder on the whisper-vs-bid spread at $125M.
