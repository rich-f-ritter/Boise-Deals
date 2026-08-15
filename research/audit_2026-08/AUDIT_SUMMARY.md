# August 2026 Blind-Spot Audit — Summary Memo
**Subject:** Seasons at Meridian (2700 E Overland Rd, Meridian ID) · 5-mile ring
**Date:** August 14, 2026 · Trigger: user found "Seasons at Meridian II" marketed next door

## 1. What happened
The July 2026 land-use analysis and supply chart both missed the subject's own marketed
351-unit Phase II on the touching parcel (2600 E Overland). Cause: three independent
blind spots — assessor farm coding (PROPCODE F, not L), a city filing name ("Overland &
Wells II") different from the marketing name, and absence from CoStar/RealPage feeds.

## 2. What Phase II actually is (primary-source resolution)
**DENIED and dead.** H-2022-0030 (MDA + CUP, 345u at hearing) denied by City Council
10/25/2022; Findings of Denial adopted 11/9/2022 (employment-land loss, failing
Overland/Eagle intersections, MF over-concentration next to Phase 1). No CUP ever
issued → no extension possible; no re-application through Aug 2026. Owner WinCo Foods
(never Morgan Stonehill) lot-split the 18 ac Feb 2025 and markets it as retail pads
(Colliers, since Jan 2024). ~5% de-novo revival; earliest delivery ~2030. The denial
precedent is a mild positive for the subject. Details + sources:
`seasons_II_overland_wells_II_status.md`.

## 3. Ring-wide re-audit results (`ring_sweep_findings.md`, `close_in_parcels_diligence.md`)
**Real misses now incorporated (~1,900 units):**
- Pine 43 expansion H-2024-0071 (approved 10/21/2025): 270u CUP tracked, but up to
  **604 more vertically-integrated units** + 30 TH in the same MDA were uncounted.
- **Outer Banks** (Franklin & Ten Mile): 516u entitled, groundbreaking expected 2026 —
  was an unquantified watch row; now Supply Chart pipeline row #33.
- **District at Ten Mile**: 222-ac plan broke ground May 2026; ~1,800 res units
  (400 TH near-term) in no vendor feed — shadow row.
- Corrections: Cole Denton 200→224u; Syringa 322→302u (remanded, re-heard 8/6/2026);
  Modern Craftsman Franklin 122 BTR flagged for verification.
**Close-in all-clear:** Latitude 43 (0.3 mi) = 79 for-sale SF homes; Kleiner Trust 72 ac
inert; nearest live risk = idle C-G farms at 1780 E Overland & 1450 E Franklin (watch).

## 4. What was rebuilt (all committed on claude/seasons-meridian-land-use-ntbhtq)
- Land Use Analysis xlsx + 26.5MB interactive Viewer (fresh 92,790-parcel pull;
  vacant screen widened to PROPCODE L+F; 19-site reasoned ranking; decisions log
  carries the full audit trail).
- Supply Chart xlsx (46-row roster, corrected units, extended forecast formulas,
  Diligence tab with the denial record + 7 new shadow rows) + new self-contained
  Supply Map html (45 numbered pins on parcel centroids + 18 shadow/dead pins).
- Skills hardened: land-use-analysis (repo copy authoritative) gained mandatory
  Phase A.5 + farm/large-lot sweep + alias-aware search; supply-chart skill's shadow
  scan now starts at the subject (updated copy: `skills-updates/supply-chart/SKILL.md`
  — needs syncing to the claude.ai skill library).

## 5. Process lessons (generalized)
1. The subject's own master plan is threat candidate #1 — check it before any screen.
2. Assessor vacant codes lie by omission: ag-exempt farms, large-lot homesteads, and
   entitled-but-stale-coded parcels must be reasoned individually near the subject.
3. City files ≠ marketing names: search by address / parcel / owner / subdivision.
4. Vendor feeds miss legacy-name modifications, plat-named projects, and approval
   swaps on dead-deal parcels — the shadow scan exists precisely for these.
5. Verify "still alive" both directions: the scariest-looking find here (a 351-unit
   phase next door) turned out to be a documented denial — research the outcome, not
   just the application.

---

# AUGUST 15 ADDENDUM — deep-dive phase (46-agent workflow + cost/feasibility work)

## New deliverables in this folder
| File | What it is |
|---|---|
| `pipeline_likelihood_report.md` | All 16 proposed deals: probability of delivering by YE2031, most-likely quarter, tiers, expected delivery curve, 16 chart corrections, missing deals, open questions |
| `graveyard_report.md` | 20 dead projects / ~4,365 units killed 2015-2026: census, year-by-year timeline, causes, eras, executive summary on why development is harder today, "so what" for underwriting |
| `replacement_cost_analysis.md` (**v3**) | Replacement cost + the Emblem vetting/normalization + the tax step-up |
| `construction_loan_cost_analysis.py` / `.json` | Yardi 118-loan tape → all-in cost by vintage at a given LTC |
| `replacement_cost_model.py` / `.json` | Seasons-comparable cohort, time-varying LTC, replacement cost |
| `emblem_normalization.py` / `.json` | Ancillary + expense + assessed-value normalization; solves required market rent |
| `tax_stepup_analysis.py` / `.json` | Idaho sale-triggered reassessment: our own step-up and the developer-exit haircut |
| `raw/` | Full per-deal, per-project and sweep research output (~520k chars) |
| `in/` | Source files: Yardi loan tape, Emblem equity book + merchant model, TMG Seasons model v3 |

## The four numbers that matter
1. **Pipeline: 4,494 proposed → 1,221 probability-weighted units (27%) by YE2031.** Only one deal
   (Outer Banks) has a permit; 2027-29 averages ~120 weighted units/yr vs a 2022-24 run-rate of
   1,000-3,000.
2. **Replacement cost ~$322,530/unit (~$116.1M)** vs a $118.0M purchase price — we buy at **+1.6%**.
3. **New supply needs ~$2,224/u/mo market rent — +23.8% above the subject's $1,796.** That gap,
   not cost inflation, is the moat.
4. **Graveyard: ~4,365 units killed, ~2,731 with no successor entitlement.**

## Method corrections logged (so they are not repeated)
- Flat-LTC cost modeling is wrong post-2022 — leverage fell 65% → 55% (Emblem is the anchor).
- Product mix must be screened before taking any median (v1's "$249k 2025 median" was n=2 townhomes).
- A developer's advertised rent is not the required rent — normalize ancillary income first.
- Purchase price ≠ assessed value: Idaho assesses at 98% of price, so the assessed figure in a
  tax tab is 2% below the real price.
- Structured-output schemas at depth caused a 44/46 agent failure in the first workflow attempt;
  plain-text agent returns succeeded 46/46. Prefer text + a synthesis pass.
