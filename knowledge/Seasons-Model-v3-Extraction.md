# Seasons at Meridian — v3 Model Extraction (TMG_Acquisitions_model_7.26)

**Extracted 2026-08-16** from `TMG_Acquisitions_model_7.26 - Seasons_at_Meridian_v3.xlsm` (59 tabs).
360u, 2024 build, Meridian ID | Seller: Carlyle | Broker: CBRE | **First-round bid date 8/19/2026** (One Pager C10).
This supersedes the $118M / 5-yr-hold figures in `Seasons-Meridian-Replacement-Cost-and-Supply-Economics.md` §1.

## Pricing & Returns (Assumptions tab unless noted)

| Item | Value | Cell |
|---|---|---|
| Purchase price (recommended bid) | **$122,000,000** ($338,889/u; $363.44/SF) | H5, I5, J5; One Pager C14 |
| Whisper / guidance | $125,000,000 ($347,222/u); delta −2.4% | H6, H7 |
| T3 TMG-Adj cap / Y1 cap at $122M | 4.53% / 4.76% | K5, L5 |
| Caps at whisper $125M | 4.39% T3 / 4.63% Y1 | K6, L6 |
| T12 actual / TMG-adj cap | 3.80% / 3.50% (lease-up year) | C33, C34 |
| UIRR | **8.75%**, 1.368x, 5.27% avg cash yield | L12, L15, L16 |
| LIRR | **11.91%**, 1.528x, 4.71% avg cash yield | L17, L20, L21 |
| Investor IRR | **9.42%**, 1.388x, 4.20% avg cash yield | L22, L25, L26 |
| Hold / dates | **4 yrs**; acq 10/31/2026, exit **10/31/2030** | M32, M44, H4 |
| Exit cap / F12 ANOI / exit value | **5.00%** / $7,252,502 / **$144,677,275** ($401,881/u, $431/SF) | M33, M36, M39–M41 |
| Exit MF adj / exit tax reassess drag | 2.5% / −$18,638 | M34, M38 |
| Closing costs | $347K total; financing fees $1,995,311 (2.6%) | G13–G17, G21 |
| Reserves/capex | $250/u/yr reserves + $700/u budgeted = $950/u/yr; $3,800/u over hold; **VA capex $0** | G41, D146–D148, G44, B166 |
| Working capital | $150K, returned Y5 | O33, O34 |
| Total uses / basis | $124.49M / $123.82M ($343,948/u) | G27, K37, K38 |
| NOI path Y1→Y5 | $5.896M / $6.231M / $6.667M / $7.067M / $7.343M | Cash Flow (Annual) K59:O59 |

## Financing (Financing tab)

| Item | Value | Cell |
|---|---|---|
| New Loan #1 (active) | $76,742,744, 5-yr term, **fixed** | G30, G25, G39 |
| Rate | 4.40% UST + 1.45% spread − 0.45% buydown = **5.40%** all-in (Act/360); 5.475% w/ amortized fees | G47, G33–G36; Assumptions I37 |
| IO | **Full-term IO** (60 mo; 420-mo amort never engages) | G27, G28 |
| LTV / LTC | 62.9% / 61.6% | Assumptions I38, I39 |
| Sizing | Min DSCR 1.25 on **lender NOI $6,157,303 ("CBRE DSF UW as of 08.05.26")** → $76.7M binding; 65% LTV → $79.3M | G45, C51, G51–G53 |
| DSCR on TMG NOI | **T3 1.11x / Y1 1.17x** (below the 1.25 used to size) | Assumptions I40, I41 |
| Debt yield | T3 7.20% / Y1 7.57% | E61, G61 |
| Prepay | Yield maintenance; 3-mo open window | G32, G42, G29 |
| Rate cap | None (fixed); stale Chatham SOFR cap grid (5/5/26) at L3:Q16 unused | — |

## Rents / Occupancy (Rent & Occ Data; Cash Flow (Annual))

- **Y1 quarterly market-rent path (row 5):** 4Q26 $1,875 (S5) / 1Q27 $1,855 (T5) / 2Q27 $1,935 (U5) /
  3Q27 $1,995 (V5) → **Y1 avg $1,915** (W5). Seasonal index 0.979 / 0.969 / 1.010 / 1.042 (S6:V6).
- Historical asking: 3Q24 $1,832 → 4Q25 trough $1,691 → 3Q26 $1,939 (J5:R5).
- Starting market rent (8/4/26 RR + L5) $1,884.69; avg contract $1,750.68 (E100, K100) → **in-place LTL ~7.1%**.
- **Annual market growth (B35):** Y1 +1.6% eff. / Y2–Y4 **4.0%** / Y5 3.5% / Y6+ 3.0%. Vendor consensus
  3.55% avg (CoStar 1.96% / RealPage 5.35% / Yardi 3.33%) — Supply tab J37:P42.
- **AGPR growth (LTL burn):** +3.7 / +5.0 / +6.1 / +5.3 / +3.8% (E177:I177); LTL % of GPR −5.14% Y1 →
  −0.90% Y5, terminal ~−0.72% (E176:O176).
- **Occupancy:** T12 84.0% (lease-up), T3 96.2%, Y1+ flat **94.5%** phys (C38:E38; E183); economic occ Y1 93.0%.
- **Concessions:** T12 −$83.7/u/mo (~4.5% GPR); UW 1.0% → 0.5% → 0.25% → **0% from Y4** (C186, E186:H186).
- Y1 opex $6,636/u vs T12 $5,608/u (+18.3%): taxes $1,416 vs $1,067, insurance $525 vs $328, turnover
  $175 vs $73, R&M $175 vs $29; RUBS income +25.4% (C190:D204).

## Taxes (Taxes tab)

- Reassessment ON for sale, 2027, at **98% of price** (C10, C11, G4) — more conservative than the 95%
  TMG convention. 2027 assessed $119.56M (G5) vs current $92.99M (C5).
- Levy 0.4507% (C7); levy drift −2%/yr Y1–Y7 then +1% (D16:N16); assessment +3.5%/yr (D17).
- 2026 taxes $419,111; **Y1 fiscal $509,808 ($1,416/u)**; 2028 $534,353 (F12, D31, E31).

## Sensitivity (Sensitivity tab) — ⚠️ partially stale

Live outputs: UIRR 8.75% (H31), LIRR 11.91% (H32), Y4 avg mkt rent $2,083.81 (H33).

**UIRR grid — outer-yr rent var (±1.5%) × exit cap (AG22:AM28), at var 0:**
4.25% → 11.12% | 4.50% → 10.17% | 4.75% → 9.29% | 5.00% → 8.45% | 5.25% → 7.66% | 5.50% → 6.90% | 5.75% → 6.17%.
At 5.0%: +1.5% rent → 10.10%, −1.5% → 6.92%.

**LIRR grid (U22:AB28), at var 0:**
4.25% → 18.94% | 4.50% → 16.97% | 4.75% → 15.05% | 5.00% → 13.17% | 5.25% → 11.32% | 5.50% → 9.51% | 5.75% → 7.66%.
At 5.0%: +1.5% → 16.83%, −1.5% → 9.54%. Y1-growth grid (U33:AB40): ±1.5% outer-yr rent ≈ ±3.6 pts LIRR.

**Stale-grid artifacts (fix before IC):**
1. "LIRR: Purchase Price vs Exit Cap" grid axis is **$70.75M–$72.25M ($196–201K/u)** — another deal's axis (V9:AB9, V17).
2. Both PP-vs-cap grids contain values **identical to the rent-variance grids** — never re-run; meaningless as shown.
3. Grid base cells (8.45% / 13.17%) don't tie to live outputs (8.75% / 11.91%) — grids ran under earlier
   assumptions; LIRR grid overstates base ~1.3 pts, UIRR understates ~0.3 pts.

## DD tabs

- **'Pre vs Post DD Y1 NOI' and 'TMG vs Mgmt Y1 NOI' are EMPTY** — placeholder tabs, no data.
- **'DD Update' (hidden, C3):** "After a thorough due diligence, no material issues were uncovered with no
  material adverse changes to the underwriting… asset is in good physical condition and Milestone plans to
  extend the useful life of multiple building components through a proactive capex strategy." The 19-item
  checklist has no statuses filled in.
- DD evidence that DID move numbers: RE taxes +33%, insurance +60%, turnover/R&M normalized up, trash RUBS
  re-set to T3-annualized (I&E X72), Vanguard Village moved UC→Proposed after Aug-2026 permit audit,
  lender NOI updated to CBRE DSF UW 08.05.26.

## Other model-evident findings

**Strengths:** lease-up done (63.7% Jul-25 → 96.3% Jun-26 → 96.1% at 8/4 RR; Lease-Up Bridge G23–G34);
LTL 7.1% drives AGPR ~5.3% CAGR on 4% market growth; 661u UC in 5 mi on the -07.15 roster (448 Y1 / 213 Y2);
sub-loan-constant fixed debt, no cap exposure; Y1 path evidence-anchored ($1,939 T90 > first two UW
quarters); concession UW grounded (HD effective = asking by Jul-26); 98% tax step conservative; One Pager:
1-mi rent-to-income 14.3% vs MSA 23.9% / US 32.8%; hard-corner I-84/Eagle Rd site (B35).

**Risks:** 24bp entry-to-exit cap spread (4.76% → 5.00%); broker guidance column runs 5.25% exit → LIRR
8.55% (One Pager D23, D27); rent growth above consensus (4.0% Y2–Y4 vs 3.3–3.6%; CoStar ~2.1%); market
printed −7.7% 3Q24→4Q25; DSCR 1.11x/1.17x on TMG NOI (loan fits only on CBRE lender NOI); model/One Pager
disagreements (5.30%/2.0% vs 5.40%/2.6% financing); hidden Exec Summary still shows "Blackstone" seller
with $74M column; Lease-Up Bridge helper #REF!s from Jan-2027; demand assumption raised 500→700u/yr between
supply-tab vintages; no value-add lever — returns rest on market growth + LTL burn + exit cap.

**Version note:** the -07.15 S&A tab carried Emblem in Bear only; the current IC slides assign eight
proposed projects (~2,300u incl. Emblem Y4) TMG delivery years in the base case — see
`Seasons-Proposed-Pipeline-Audit.md`.
