# Seasons at Meridian — v3 → v6 Model Diff (as of Aug 20, 2026)

**Purpose:** confirm and quantify the underwriting changes made between the model behind the Monday
8/17/26 IC deck (`in/TMG_Acquisitions_model_7.26 - Seasons_at_Meridian_v3.xlsm`) and the current model
(`in/TMG_Acquisitions_Seasons_at_Meridian_v6_July_T12.xlsm`). Basis for the 8/20 IC update email
(`Seasons-IC-Email-Draft-2026-08-20.md`). Both files committed in `in/`.

**RESOLVES CLAUDE.md reconciliation item #1:** the deck presented Monday 8/17 ties to the
`7.26 - v3` save ($122M bid / 4-yr hold / UIRR 8.75% / LIRR 11.91% / exit ~$402K/u 2030 @ ~5.00%).
Deck page 6 states "Base case UW UIRR 8.7%... exit ~$402K/unit in ~2030" — matches v3 CF S&U
C22/D22 and G45 exactly. The earlier audit anchors ($120.0M bid, 5-yr hold, exit 10/31/2031 @ 5.25%,
ULIRR 8.20/LIRR 11.21) are from an older save and are SUPERSEDED for deal-status purposes.
**v6 is now the live save** — but note its price input is still $122M; the intended submit is $119M
(model re-cut pending as of 8/20).

## Headline (both at $122M price input; 360 units; 4-yr hold, sale in FY Y4 ~2030)

| Metric (source cell) | v3 (Monday deck) | v6 (current) | Δ |
|---|---|---|---|
| Purchase price (Assumptions H5) | $122,000,000 | $122,000,000 | — (submit will be $119M) |
| Whisper (H6) | $125,000,000 | $125,000,000 | delta to guidance −2.4% |
| Acq date (Assumptions H4) | 10/31/2026 | 9/30/2026 | 1 mo earlier |
| UIRR (CF S&U C22) | 8.746% | 8.554% | **−19 bps** |
| LIRR (CF S&U D22) | 11.907% | 11.300% | **−61 bps** |
| Levered multiple (D23) | 1.528x | 1.494x | −0.034x |
| Investor IRR (Financing I14) | 9.42% | 9.10% | −32 bps |
| Y1 NOI (CF S&U D40) | $5,895,884 | $6,035,354 | **+$139,469** |
| Y1 cap (Assumptions E33) | 4.759% | 4.873% | +11 bps |
| T3 cap (D33) | 4.669% | 4.705% | +4 bps |
| Y1 market rent /u/mo (CF Annual K4) | $1,915 | $1,884.7 | **−1.6%** |
| Debt proceeds (CF S&U C6) | $76,742,744 (61.6% of sources) | $73,278,247 (58.9%) | −$3.46M |
| All-in rate (Financing G36) | 5.40% | 5.31% | −9 bps |
| Y1 interest (CF S&U D54) | $4,201,665 | $3,945,118 | −$256,548 |
| Equity at close (C8) | $47,749,568 | $51,048,988 | **+$3.30M** |
| Total equity (C18) | $49,073,842 | $52,229,691 | +$3.16M |
| Gross exit proceeds (G45) | $144,677,275 | $142,942,683 | −$1.73M |
| Exit $/u | $401,881 | $397,063 | −$4,818 |
| Y1 fiscal RE taxes (Op Proforma K49) | $509,808 | $504,124 | −$5,685 |
| Y1 insurance (K48) | $189,000 ($525/u) | $180,000 ($500/u) | −$9,000 |
| 4-yr capex budget incl. reserves (Capex M-col) | $1,368,000 ($3,800/u) | $1,225,555 ($3,404/u) | −$142,445 (see capex note) |

IRR mechanics reconciled per the uirr-lirr-bridge method (unlevered stream rebuild ties within ~7-15bp
using top-level CF S&U vectors; residual is Yr0 closing-cost/timing detail — headline numbers above are
the models' own reported returns, not reconstructions).

## The five changes confirmed, with mechanics

### 1. KEAndrews tax guidance (consultant Clayton House; report in `in/MilestoneGroupSeasonsAtMeridian.pdf`)
- v3 carried reassessment at 98.0% of the $122M price → 2027 AV $119.56M, +3.5%/yr AV growth.
- v6 adopts KEA's schedule dollar-for-dollar: 2027 AV **$120,625,000** (= 96.5% of the $125M guidance
  price KEA modeled; equals 98.87% of the $122M model price — Taxes C11 = 0.98873), CY2027 taxes
  **$532,861** (ties to KEA page 1 exactly), then $537,851 / $542,731 / $553,153 / $569,195
  (model CY28-31 vs KEA $537,851 / $542,731 / $553,366 / $563,899 — near years exact; model runs AV
  growth 3/3/4/5/5% vs KEA 3/3/4/4%, so model 2031 is ~$5K hotter = conservative).
- Y1 fiscal-year taxes actually DOWN $5.7K vs v3 (rate compression −2%/yr per KEA offsets the higher
  reassessment); out-years up slightly. Net ~neutral to returns but now third-party supported.
- **$119M nuance:** KEA's 96.5%-of-price method at a $119M actual price implies 2027 AV ~$114.8M and
  ~$26K less in 2027 taxes; v6 carries KEA's $125M-based dollars = conservative at the submit price.
- Consistent with the standing Idaho step-up rule (CLAUDE.md): toll paid once by the first
  institutional buyer; TMG models it correctly.

### 2. Insurance (Karen)
- $525/u → **$500/u**: Y1 $189,000 → $180,000 (Op Proforma K48), −$9K/yr escalating at 3%.
  Actuals for reference: seller carrying ~$117.7K/yr (T12) — UW still ~1.5x in-place.

### 3. CBRE debt soft quotes (Jay Wagley; PLA 8/18/26 in `in/Seasons_at_Meridian_PLA_8.18.26.pdf`;
   full extraction: `Seasons-CBRE-Debt-PLA-Extraction-2026-08-18.md`)
- v3 placeholder: generic Freddie fixed, 5.40% all-in (145 gross spread − 45 buydown), $76.74M.
- v6 selected quote: **Freddie 5-yr fixed CME max-leverage with max buydown — 5.31% all-in**
  (4.37% 5-yr UST + 1.40% gross spread − 0.46% buydown @ 2.00% cost), **$73.305M gross**
  ($73.278M modeled), ~58.6% LTV w/ buydown, full-term IO, 1.25x amort DSCR constraint, defeasance,
  2.6% financing fees incl. buydown. Scenario tab now carries labeled alternatives:
  ALT LIFECO 6.37%, Freddie forward (month 24+) 4.91%, PortCo floater 5.53%, Freddie floater 5.43%.
- Net effect: rate −9bp but proceeds −$3.46M → equity +$3.3M. This is most of the LIRR give-back
  (leverage 63% → 60% LTC) — real quotes replacing placeholder sizing.

### 4. Y1 market rent seasonality (asset management)
- Y1 avg market rent $1,915 → **$1,884.7** (−1.6%) = the current in-place weighted-avg market rent
  (Assumptions E100 $1,884.69) with the seasonal dip pattern experienced at Prelude post-close
  (deck pp. 4-5: ran ~$43/mo (~2.5%) light in Q1/Q2 post-close).
- Growth rates unchanged (+4/4/4/3.5%), so the whole path shifts down ~1.6%:
  Y1-Y5 now 1,885 / 1,960 / 2,038 / 2,120 / 2,194 (was 1,915 / 1,992 / 2,071 / 2,154 / 2,230).
- Exit-year NOI −$101K → gross exit −$1.73M at the ~5.0% exit cap. **This is the single biggest
  driver of the UIRR decline** — a terminal-value effect, not a Y1 effect (Y1 NOI actually rose).
- Support: HelloData T90 market $1,940; L5 executed new leases $1,885 — Y1 UW now equals today's
  executed level, zero recovery assumed in the average.

### 5. CapEx refinement (Justin)
- v6 Capex tab replaces the $/u allowance build with a line-item schedule ("Justin CapEx Sheet"):
  enhancement capex $825,555 + $10K/yr contingency = $865,555 over 4 yrs, front-loaded
  (Y1-4: $142.8K / $197.2K / $298.6K / $227.0K), + $250/u/yr reserves ($360K) = **$1,225,555 total
  ($3,404/u)**.
- **The −$485K ties to the budget carried into Monday and given to CBRE**, not to v3's model line:
  the CBRE PLA (8/18) shows "Budgeted CapEx $1,710,000 / $4,750/u"; $1,710,555 − $1,225,555 =
  **$485,000 exactly**. v3's model Capex tab itself carried a $950/u/yr allowance = $1,368,000
  (−$142K vs v6). i.e. the deck-era budget was $1.71M, v3's cash-flow allowance $1.37M, Justin's
  bottoms-up $1.23M.

## What the July T12 + 8/18 rent roll revealed (raw files in `in/07.2026_Seasons_T12.xlsx`,
## `in/RentRoll08_18_2026.xlsx`; v6 embeds the 8/4 RR — Assumptions E47 "IP Rents (8/4 RR)")

Occupancy / leasing (8/18/26 RR, computed this session — n=360, method: resident rows with actual
rent > 0 = occupied):
- **352/360 physically occupied = 97.8%** (8 vacant, 25 on notice). CBRE PLA (8/4 RR) had 96.67%;
  T12-avg physical was 86.8%. The lease-up is done.
- In-place rent (occupied, >$0): **$1,758/u** vs RR asking $1,960 → **loss-to-lease −10.3%** —
  the embedded mark-to-market we're buying.
- **64 move-ins since 6/1/26 at avg $1,920; 17 since 8/1 at avg $1,947** — new leases printing above
  the $1,885 Y1 UW and at the $1,940 T90 market level. (Deck p.5 trade-out table: May-Jul new leases
  $1,881 avg, +6.6% LTOs, 49 new leases vs 52 move-outs.)
- July 2026 month (raw T12): concessions **−$3,831 = 0.5% of GPR** (vs −$34.9K/mo T12 avg — burned
  off); vacancy loss −$29,794 (4.2%); GPR market rent $706,372 ($1,962/u).
- Model trailing anchors moved (v3 June-T12 → v6 July-T12): T12 phys occ 84.0% → 86.8%; T12 econ occ
  78.2% → 81.2%; T3 NOI $5.786M → $5.830M; T1 annualized NOI $6.306M (June) → $6.233M (July; July
  carries a $97K annualized turnover month and $89K annualized bad-debt month — one-month noise,
  both T3 and T12 improved).
- Y1 LTL assumption halved ($425K → $202K) — consistent with marking Y1 market rent to in-place
  market ($1,885) rather than a higher $1,915 (smaller gap left to burn).
- Y1 EGI +$136K and Y1 NOI +$139K vs v3; Y1 cap 4.76% → 4.87% at $122M.

## Returns walk (directional, at constant $122M)
- Near-year NOI UP (July T12 mark, taxes −$6K Y1, insurance −$9K, capex −$143K vs v3 model line):
  Y1 NCF +$249K.
- Out-year NOI DOWN (rent path −1.6% all years): Y4 NOI −$89K, Y5 −$101K → exit −$1.73M.
- Debt: rate −9bp (interest −$257K/yr) but proceeds −$3.46M / equity +$3.3M → levered drag.
- Net: UIRR 8.75% → 8.55% (−19bp), LIRR 11.91% → 11.30% (−61bp).

## At the $119M submit price (back-of-envelope, computed this session)
- Y1 cap **5.07%**; basis ~$330.6K/u = **+2.5% to the $322.5K/u replacement-cost work** (canonical
  `research/audit_2026-08/replacement_cost_analysis.md` v3).
- Holding v6 ops and debt dollars constant, shifting Yr0 by +$3.003M (price −$3M, title −0.1%):
  **UIRR ≈ 9.3%, LIRR ≈ 13.0%** (delta method vs stream reconstruction; +72bp / +180bp vs the $122M
  run). Upside not captured: KEA reassessment scaling to the lower price (~+$26K NOI 2027);
  possible debt re-size. Model re-cut at $119M still to be done — these are estimates, label as such.
- Vs process: $119M is $4M clear of the $115M current top offer (see
  `Seasons-Broker-Guidance-Naumann-2026-08-19.md`) and −4.8% to the $125M whisper.

## Provenance
- v3/v6 cell reads via openpyxl (cached values), sheets: CF S&U, Assumptions, Operating Proforma,
  Cash Flow (Annual), Taxes, Financing, Capex. Session date 8/20/2026.
- Deck: `in/Seasons_at_Meridian_Executive_Summary_08.17.2026.pdf` (13 pp; pp. 2/12/13 are image-only
  exhibits, text pages extracted).
- RR/T12 stats computed from the raw files as noted; RR occupancy method may differ slightly from
  Yardi's summary block (not re-tied to the sheet's own summary rows).
