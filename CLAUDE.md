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
  `in/`): Seasons replacement cost **~$322.5k/unit (~$116.1M)**; TMG purchase price is
  **$118.0M = $327,778/u (+1.6% vs replacement)** — NOTE $115.64M is the post-sale ASSESSED
  value (98% of price), not the price; total basis $333.6k/u (+3.4%). Emblem's proforma carries
  **+83% more ancillary income than the subject actually collects** ($350.59 vs $191.94/u/mo);
  normalized, new supply needs **~$2,224/u/mo market rent = +23.8% above the subject's $1,796**
  (NOT ~10%). Emblem's tax RATE (0.45%) matches TMG's own, but its assessed-value ramp lags
  construction by ~$212k across lease-up. Costs doubled 2014-2021 then plateaued (~+1.7%/yr);
  the financing break is **65%->55% LTC = equity/unit +38%** ($99.6k -> $137.0k).
  Ring construction lending ~zero since 2023.
- **Idaho sale-triggered tax step-up** (`tax_stepup_analysis.py`): Idaho reassesses to ~98% of
  sale price. OUR OWN deal is the worked example — Seasons' taxes go $384,244 -> $510,754
  (**+$126,510/yr, +33%**) = $2.53M of value at our 5.01% Y1 cap and **11bp of going-in yield**.
  Applied to a developer's exit, ~0.8-1.0% of exit value (~2-3% of the equity check) transfers
  to the buyer; Emblem's $102.5M exit solves to $101.69M for a buyer at a true 5.50% cap.
  **Rule: haircut every merchant-developer exit in this market for reassessment.**

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
