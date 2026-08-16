# Boise-Deals — Project Knowledge Base

Land-use / supply-threat analyses for Treasure Valley multifamily deals
(subjects so far: **Seasons at Meridian**, 2700 E Overland Rd, Meridian ID;
**Canyon Ridge**). Each subject has a run directory (`SeasonsMeridian/`,
`CanyonRidge/`) produced by the `land-use-analysis` skill (skill source is
versioned in `land-use-analysis/` at the repo root — that copy is authoritative).

## Current deliverables (rev. Aug 15, 2026 — post blind-spot audit + 46-agent deep dive)
- `SeasonsMeridian/Seasons at Meridian - Land Use Analysis.xlsx` + `... - Land Use Viewer.html`
  (fresh 92,790-parcel pull; vacant screen = PROPCODE **L + F**; 19-site reasoned ranking;
  `All Vacant Verdicts` sheet = all 552 clusters)
- `SeasonsMeridian/Seasons at Meridian - Supply Chart.xlsx` + `... - Supply Map.html`
  (47-row roster: 22 stabilized / 5 leasing / 5 UC / 15 proposed. **Numbering restarts at 1
  within each bucket — colour is the differentiator**, and PROPOSED is sorted most-likely-first
  by the P(deliver by YE2031) column. Owner/developer on every row; NOTES carry the IC
  conclusion only, with all evidence, file numbers, timelines and sources on the Diligence tab
  and source reconciliation on the Reconciliation Log. Map mirrors the same numbering/colours
  and has per-bucket toggle layers.)
- `research/audit_2026-08/` — the August 2026 audit: findings memos, parcel diligence,
  supply-map builders + data, Seasons II denial record, **552-cluster vacant-site verdicts**
  (`vacant_sites_verdicts.json`, also a workbook sheet) and the **shot-down MF register**
  (`graveyard_register.md`: 15 killed projects, ~2,100 units died in-ring 2024-25), plus
  **replacement-cost work** (`replacement_cost_analysis.md` **v3** + `replacement_cost_model.py`
  + `emblem_normalization.py`, anchored on the Emblem Meridian proforma & TMG Seasons model in
  `in/`): Seasons replacement cost **~$322.5k/unit (~$116.1M)**. Emblem's proforma carries
  **+83% more ancillary income than the subject actually collects** ($350.59 vs $191.94/u/mo);
  normalized, new supply needs **~$2,224/u/mo market rent** (NOT ~10% above market — see the
  live-model anchors below for the gap). Emblem's tax RATE (0.45%) matches TMG's own, but its
  assessed-value ramp lags construction by ~$212k across lease-up. Costs doubled 2014-2021 then
  plateaued (~+1.7%/yr); the financing break is **65%->55% LTC = equity/unit +38%**
  ($99.6k -> $137.0k). Ring construction lending ~zero since 2023.
- `SeasonsMeridian/Seasons at Meridian - Development Feasibility.docx` (5 pp, built by
  `research/audit_2026-08/build_feasibility_memo.py` off `development_feasibility.py`/`.json`,
  which read the LIVE TMG model rather than hard-coded figures). Three layered lenses —
  market feasibility, the buy-side moat, build-vs-buy — plus the two IC risk questions.

## LIVE TMG MODEL ANCHORS (v3 re-uploaded 8/15/2026 — supersedes all earlier figures)
Read these from `in/TMG_Seasons_at_Meridian_v3.xlsm`; do NOT reuse older numbers.
- Recommended bid **$120.0M = $333,333/u** (whisper $125M); total basis **$122.1M = $339,175/u**.
  (An earlier version of the model carried $118.0M/$327,778/u — that is stale.)
- Y1 cap **4.89%**, T3 TMG-adj cap 4.61%; exit **10/31/2031 @ 5.25% cap = $142.81M =
  $396,692/u** on a forward-12 exit NOI of $7,498,601. ULIRR 8.20% / **LIRR 11.21%** / ERM 1.63x.
- **Market rent is the comparison metric, and it is $1,915/u/mo in Year 1** (CF Annual row 4,
  HelloData market rent; starting weighted-avg market rent $1,884.69, in-place contract
  $1,750.68). Do not compare a developer's required rent against contract or T12 rent.
- Market-rent path Y1-Y5: 1,915 / 1,992 / 2,071 / 2,154 / 2,230 (+3.1%, then 4/4/4/3.5%).
- Price vs replacement cost **+3.3%**; total basis **+5.2%**. We do NOT buy below replacement.
- **Required rent gap = +16.1%** ($2,224 required vs $1,915 Y1 market).
- The model's `M5` note "~$315k/Unit RC" is STALE — ignore it; use our $322.5k/u work.
- **Idaho sale-triggered tax step-up** (`tax_stepup_analysis.py`, Taxes tab): assessed
  $92,993,300 (**77% of our price** — the developer's assessment never caught up with
  construction) steps to **$117,600,000 (98% of price)** on the 2027 roll; taxes
  **$419,111 -> $519,411 = +$100,300/yr (+23.9%)** = **$2.05M of value at the 4.89% Y1 cap,
  8bp of going-in yield**. TMG models this correctly.
  **The asymmetry is the point:** the toll is paid ONCE, by the first institutional buyer of
  merchant-built product. Our assessed value — reset in 2027, grown 3.5%/yr — reaches $139.7M
  by 2032 = **98% of our own exit price**, so OUR buyer's step-up is ~$21k of value (0.01%),
  versus ~$922k (0.9% of price, $3,604/u) for a buyer of Emblem (assessed only 87% of exit).
  **Rule: haircut every merchant-developer exit for reassessment; a second-generation trade
  needs no haircut.**

## THE SEASONS II LESSON (read before touching any analysis here)
In July 2026 the analysis missed the subject's own marketed Phase II
("Seasons at Meridian II" = city file **"Overland & Wells II" H-2022-0030**, 351u)
on the parcel touching the subject at 2600 E Overland. Three blind spots aligned:
1. Parcel is assessor-coded **F (ag-exempt farm)** → invisible to the L-only vacant screen.
2. Filed under the **subdivision name**, not the marketed brand → name searches missed it.
3. Not in CoStar/RealPage; its press was 2021-2023 → diligence sweeps missed it.

Resolution (researched Aug 2026, primary sources): it was **DENIED** by Meridian City
Council 10/25/2022 (findings 11/9/2022 — employment-land loss, failing Overland/Eagle
intersections, MF over-concentration next to Phase 1). Owner was and is **WinCo Foods**
(Morgan Stonehill never took title); site lot-split Feb 2025, marketed as retail pads
since Jan 2024. Dead as MF (~5% revival, earliest ~2030). Full record:
`research/audit_2026-08/seasons_II_overland_wells_II_status.md`.

### Standing rules derived from it (now hard-coded in the skills)
- **Phase A.5 first**: check the subject's own plat/DA for unbuilt phases; sweep the
  subject's developer + architect for sibling "II" projects; inventory every touching
  parcel regardless of assessor code.
- **Never trust the vacant code alone**: ag-exempt farms (PROPCODE F), large-lot
  homesteads, and stale-coded entitled parcels are swept individually within ~1.5 mi.
- **Alias-aware entitlement search**: query by address, parcel number, owner, and
  subdivision/plat name — never only by project brand.
- Supply-chart shadow scans start AT the subject (phased-plan check) before the ring.

## DEVELOPMENT FEASIBILITY — the two IC conclusions (`development_feasibility.py`)
**Q1 — how much rent growth before new supply pencils and suppresses us?**
The moat is self-limiting (our own rent growth is what restores a developer's feasibility),
so the question is whether it outlasts the hold. It does, on both bookends:
- Costs escalating at the observed **+1.7%/yr**: required rent outruns market rent the whole
  way. Gap **-15.3% (FY2027) -> -7.9% at our Oct-2031 exit -> still -1.8% in FY2036.** Never closes.
- Costs **flat in nominal dollars** (deliberately generous): feasibility is restored in
  **FY2031 — the exit year itself** (+0.2%).
- **Second line of defense = the ~4-year lag** (entitlement 12-24 mo + build 24-30 mo). To
  suppress Y4-Y5 rents a competitor had to be feasible in FY2027, needing market rents
  **+18.1% above our Y1 UW immediately** — a step-change, not a trend (UW has FY2027 at +3.1%).
- **Corollary to state out loud:** because the gap is this wide, our rent growth is NOT
  supply-constrained, so it must be defended on demand alone. The moat covers a supply shock,
  not a demand shock.

**Q2 — Quarterra needs ~$400k/u in Jan 2030 (2-yr-old); we need ~$397k/u in Oct 2031 (7-yr-old).**
- **Adjusted for tax basis the two are the same number:** Emblem $400,391/u -> **$396,787/u**
  after its buyer prices the step-up; ours $396,692 -> **$396,633/u**. Within **$154/unit**.
- **Age:** rolling Emblem's adjusted figure forward 21 mo at our own 3.54% appreciation CAGR
  gives $421,693/u for a 3.5-yr-old asset in Oct 2031; we underwrite a 7-yr-old at **94% of
  that** = ~1.7%/yr of relative obsolescence. Defensible for garden, but it IS an assumption.
- **The soft number is the cap rate:** we exit a 7-yr-old asset at **5.25%** while a merchant
  developer underwrites a 2-yr-old at **5.50%** — inverts the normal age/cap relationship.
  At 5.50% our exit is $136.34M = $378,717/u: **-$6.47M and -205bp of levered IRR
  (11.21% -> 9.16%)**. Recommend IC treat 5.50% as the downside case.
- The two risks are **compatible**: our UW does not generate enough rent growth to restore
  feasibility before we sell. They conflict only in a high-growth world.

## Ada County data facts (hard-won)
- Parcels: `services2.arcgis.com/dgGjZc6xAH5m5JyP/.../Parcels/FeatureServer/5`
  (PARCEL, ADDRESS, PROPCODE R/C/F/L/M, ZONING, ACRES, TOTALVALUE, SUBNM).
- **Owner names are not in any public Ada GIS layer**; the assessor portal is
  reCAPTCHA-gated. Ownership comes from hearing records, listings, news.
- PROPCODE F + near-zero TOTALVALUE = ag-exempt land — the canonical development
  pipeline (Syringa, Graycliff, Brighton plans, and the WinCo parcel all are/were F).
- Meridian hearing notices post to Nextdoor ("Public Hearing Notice ... City of
  Meridian"); agendas at meetings.municode.com (cc=MERIDIANID); many attachment PDFs
  are glyph-encoded (unextractable text) — use agenda HTML + news instead.
- boisedev.com 403s direct fetches — use search snippets / yahoo syndication / idahopress.

## Aug 15, 2026 — 46-agent pipeline + graveyard deep dive (`pipeline_likelihood_report.md`,
## `graveyard_report.md`, raw per-deal research in `raw/`)
- **Pipeline: 4,494 proposed units -> 1,221 probability-weighted (27%) by YE2031.** Only ONE deal
  (Outer Banks, 516u = 364 apts + 126 flats + 26 TH) has a building permit — and only 3 of its
  ~50 buildings are permitted; it carries 34% of the weighted total. 2027-29 is a
  supply vacuum (~120 wtd units/yr = 4-12% of the 2022-24 run-rate); 2030 is scenario-dependent.
- **Double-count RESOLVED:** "The 10" (559u) and Outer Banks (516u) are one lineage — The 10 was
  downsized to Outer Banks before the 12/14/2021 approval. Gateway (390u, GFI Meridian Investments
  — NOT "TGI Corp") is genuinely separate. Carry Outer Banks + Gateway; The 10 at zero.
- **Vanguard Village: CoStar's UC flag is WRONG** — bleed-over from the $50.7M Life Time club
  (C-NEW-2026-0003) in the same plat. Parcel raw/unplatted, zero permits, CUP likely lapsed ~Jul 2024.
- **Outer Banks upgraded to UNDER CONSTRUCTION**: permits C-MULTI-2025-0023/-0024 + a third
  issued 6/17/2026; GC Perryman. Current entitlement is H-2024-0026 (2021 CUP lapsed ~Dec 2023).
- **Entitlement clocks are the near-term risk:** The Judy ~9/10/26, Meridian OZ ~10/17/26,
  Gateway ~11/19/26 all expire within 90 days with no extension found; Record and 12548 W
  Overland already lapsed; Victory Flats is on a SECOND extension request.
- **Graveyard: 20 counted dead projects, ~4,365 units killed 2015-2026**, ~2,731 units with no
  successor entitlement. Same-site repeat kills: Lake Hazel & Five Mile (2x), Magic View (3x),
  1475 E Franklin (3x), Civic Block (2x), Tanner Creek (2x).

### Proposed pipeline, most-likely first (P = probability of delivering by YE2031)
1 Heritage Square 250u 38% (Pacific Cos + Ahlquist) · 2 Rolling Hill 200u 32% (Assemble) ·
3 Pine 43 MF 270u 30% (DRB) · 4 Meridian OZ 36u 30% (sold 8/7/26) · 5 12565 W Fairview 275u 25%
(sponsor UNVERIFIED) · 6 The Judy 162u 25% (Hawkins) · 7 Ascent Overland 138u 22% (MVRK, under
contract) · 8 Record 472u 20% (Brighton, LAPSED) · 9 Victory Flats 301u 20% (Welltower) ·
10 Emblem 250u 20% (Quarterra — does NOT own the land) · 11 Gateway 390u 15% (GFI Meridian) ·
12 Cole Denton 224u 15% (Kal Pacific) · 13 Vanguard 552u 12% (Endurance/Challenger) ·
14 Syringa 302u 12% (Hawkins) · 15 12548 W Overland 156u 12% (Hook Family Trust, LAPSED)

## Open follow-ups (as of Aug 15, 2026)
- Syringa Crossing: P&Z re-heard 8/6/2026 — outcome still unpublished (302u CUP at stake).
- Latitude Forty Three (H-2024-0059, 0.3 mi): final council vote pending (ITD TIA).
- Cloverdale Crossing (PLN25-00471, 12535 W Overland): no unit count pulled — add or document exclusion.
- Foxcroft Sub (Trilogy, Ten Mile & Pine, 216 apts approved 2021, phased last): status entirely unverified.
- Modern Craftsman Franklin (122 BTR): post-2023 status unverified; same sponsor (Baron) is exiting the Eagle Rd site.
- Emblem: Quarterra does NOT own the land — Baron Properties still marketing it. Watch for a closing.
- Owner pulls needed (manual assessor lookups): 1780 E Overland (R7100270310),
  1450 E Franklin (S1107449996), 104 W Cherry Ln (S1201449707), 785 S Locust Grove
  ($0-assessed exempt assemblage), S Standing Timber Way (S1130234045).
- `skills-updates/supply-chart/SKILL.md` — updated supply-chart skill; sync it into the
  claude.ai skill library (the container-local synced copy does not persist).
