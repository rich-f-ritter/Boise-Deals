# Boise-Deals — Project Knowledge Base

Land-use / supply-threat analyses for Treasure Valley multifamily deals
(subjects so far: **Seasons at Meridian**, 2700 E Overland Rd, Meridian ID;
**Canyon Ridge**). Each subject has a run directory (`SeasonsMeridian/`,
`CanyonRidge/`) produced by the `land-use-analysis` skill (skill source is
versioned in `land-use-analysis/` at the repo root — that copy is authoritative).

## Current deliverables (rev. Aug 14, 2026 — post blind-spot audit)
- `SeasonsMeridian/Seasons at Meridian - Land Use Analysis.xlsx` + `... - Land Use Viewer.html`
  (fresh 92,790-parcel pull; vacant screen = PROPCODE **L + F**; 19-site reasoned ranking)
- `SeasonsMeridian/Seasons at Meridian - Supply Chart.xlsx` + `... - Supply Map.html`
  (46-row roster incl. Outer Banks #33; Diligence tab carries the full audit)
- `research/audit_2026-08/` — the August 2026 audit: findings memos, parcel diligence,
  supply-map builders + data, Seasons II denial record, **552-cluster vacant-site verdicts**
  (`vacant_sites_verdicts.json`, also a workbook sheet) and the **shot-down MF register**
  (`graveyard_register.md`: 15 killed projects, ~2,100 units died in-ring 2024-25)

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

## Open follow-ups (as of Aug 14, 2026)
- Syringa Crossing: P&Z re-heard 8/6/2026 — pull the result (302u CUP at stake).
- Latitude Forty Three (H-2024-0059, 0.3 mi): final council vote pending (ITD TIA).
- Records (Brighton 472u): CUP validity/expiry unverified — confirm with Meridian planning.
- Modern Craftsman Franklin (122 BTR): post-2023 status unverified.
- Verify The 10 (559u, abandoned) footprint vs Outer Banks (#33) / Gateway (#39) split at Franklin & Ten Mile.
- Apex Zenith (Brighton, Lake Hazel & Meridian) + Victory & Ten Mile 142-ac pre-app: new watch items from Aug 2026 sweep.
- Owner pulls needed (manual assessor lookups): 1780 E Overland (R7100270310),
  1450 E Franklin (S1107449996), 104 W Cherry Ln (S1201449707), 785 S Locust Grove
  ($0-assessed exempt assemblage), S Standing Timber Way (S1130234045).
- `skills-updates/supply-chart/SKILL.md` — updated supply-chart skill; sync it into the
  claude.ai skill library (the container-local synced copy does not persist).
