# Land Use & Developable-Land Analysis — Seasons at Meridian — Decisions Log

Run date: 2026-07-14. Analyst: land-use-analysis pipeline + reasoned per-site research review.
This log records every subjective judgment call and data note behind the deliverable, so the
analysis is auditable and reproducible.

## 1. Subject location (verified point)
- Address: 2700 E Overland Rd, Meridian, ID 83642 — Seasons at Meridian.
- Verified point: 43.591935, -116.360877 (ArcGIS World GeocodeServer, PointAddress, score 100).
- Seasons at Meridian is an apartment community on E Overland Rd in southeast Meridian, ~0.5 mi south of I-84 near S Eagle Rd, in the heart of the Treasure Valley's fastest-growing residential submarket. No airport overlay applies here.

## 2. Analysis area
- 5.0-mile geodesic radius around the subject point (user request: "5-mi radius, most granularity possible").
  A true geodesic circle (≈ 50,200 acres) built in a local azimuthal projection; every parcel whose
  representative point falls inside is included.
- Area spans: central and south Meridian; the Ten Mile Interchange specific-area plan; the Overland / Eagle Rd / Locust Grove / Meridian Rd / Lake Hazel growth corridors; the Chinden / SH-20-26 employment frontier; west Boise and a sliver of Garden City to the east; and unincorporated Ada County (city Areas of Impact) at the fringes.

## 3. Parcel data source + the owner-data gap (the central constraint)
- Ada County Assessor Parcels, ArcGIS FeatureServer layer 5 (services2.arcgis.com/dgGjZc6xAH5m5JyP),
  pulled via POST + OBJECTID paging with checkpoint/resume.
- Fields used: PARCEL (account), ADDRESS (situs), PROPCODE (land-use class), LEGAL1-5, TOTALVALUE,
  HOMEEXEMPT (homestead), SUBNM (subdivision), ACRES, ZONING (assessor string).
- **Owner names are NOT available in any Ada County public GIS layer, and the county's PropertyLookup
  portal is reCAPTCHA-gated and licensed "for reference only" — so a bulk owner roll cannot be produced.**
  This is a hard, documented limit of Idaho public data (owner names were removed from the free GIS).
  Consequence: "who owns what, since when, who they are, what they will do with it" is answered by
  TARGETED PER-SITE RESEARCH on the material developable sites (development applications, city staff
  reports, BoiseDev/COMPASS/Idaho Statesman reporting, Idaho Secretary of State business registry),
  NOT by a parcel-level owner field. See the Ownership & Intent sheet. Where an owner could not be
  identified from public records, it is labeled "not publicly identified" — never fabricated.

## 4. Land-use source & granularity
- Ada County PROPCODE single-letter property class: R = Residential, C = Commercial, F = Farm,
  L = Land (vacant), M = Manufactured. Crosswalk to canonical buckets: R, M -> Single Family
  Residential; C -> Commercial; F -> Agricultural/Rural; L -> Vacant Land; blank -> Other/Unclassified.
- Land use and zoning are treated as INDEPENDENT layers (a commercial-zoned parcel can carry
  residential use, etc.) — neither is "corrected" from the other.

## 5. Zoning sources + honest gaps
- Ada County publishes ONE countywide Zoning layer (FeatureServer 22) carrying a CITY field. To avoid
  cross-city zone-code collisions (e.g. Boise "R-2" vs Meridian "R-2" mean different things), the layer
  was split by CITY into SEVEN jurisdiction sources — City of Boise, City of Meridian, Ada County
  (unincorporated), City of Kuna, City of Eagle, City of Garden City, City of Star — each crosswalked
  on its own ordinance. 0 unmapped zone codes and 0 unmapped land-use codes in either study area.

## 6. Zoning crosswalk corrections (verified against the ordinances)
- Boise (2023 Modern Zoning Code): R-3 and the MX-1..MX-5 / MX-U / MX-H mixed-use districts permit
  multifamily by-right (MX has NO maximum density) -> High. MX-1 was upgraded from Medium to High on
  that basis. R-2 (two-family/low-density) -> Medium. R-1A/B/C -> Low. A-1/A-2 -> Ag/Rural, Low.
  SP-01..04 Specific Plans -> Planned/Overlay, Unknown.
- Meridian (UDC): R-40 and R-15 are the multifamily districts (Med-High/High-Density Residential) -> High;
  NOTE Meridian requires a Conditional Use Permit for multifamily even in R-15/R-40, but these districts
  exist specifically for apartments, so they are treated as High with the CUP nuance documented.
  R-8 -> Medium; R-2/R-4 -> Low; TN-R -> Medium; TN-C / O-T -> Mixed Use High; C-C/C-G -> Commercial,
  Medium (MF conditional in commercial); L-O -> Office; I-L/M-E/H-E -> Industrial.
- Ada County: confirmed R1..R20 = max dwelling units/acre, so R12/R20 -> Multifamily/High, R8 -> Medium,
  R1/R2/R4 -> Single-Family/Low, R6 -> Low; RUT (Rural-Urban Transition) and RR (Rural Residential)
  -> Ag/Rural Low; RP = Rural Preservation (foothills) -> Ag/Rural, Low (often conservation-restricted);
  RSW treated as a residential-subdivision district (Low) — a documented assumption; M1/M2/M3 -> Industrial.
  (Ada County enacted a new Title 8 zoning code Dec 2024; the GIS codes reflect the mapped base zones.)

## 7. Future Land Use (Comprehensive Plan) enrichment — new vs the prior run
- Every parcel was additionally joined to the adopted Future Land Use / comp-plan designation
  (Boise "LandUse", Meridian "class2", Ada County "CATEGORY"), by representative point, city plan taking
  priority over the coarse county layer. FLU = what the land is PLANNED for; for vacant land it is the
  strongest rezone-likely signal (e.g. a parcel zoned Low today but designated "High Density" / "Mixed Use"
  / "MU-C" is an apartment-supply site in waiting). FLU designation + a residential-intensification intent
  tier is carried on every parcel and summarized on the Future Land Use sheet.

## 8. "Vacant" definition
- PROPCODE 'L' = Land (vacant lots + HOA/condo common-area land, much of it $0 value). Treated as
  undeveloped for the developable-land screen; HOA commons, detention/irrigation/open-space lots,
  floodplain, foothills-preservation and airport land are then removed (see 9).

## 9. Developable inventory — the mechanical filters + the owner-cluster FIX
- The prior run clustered vacant parcels by owner; because Ada County owner is null, that collapsed into
  ADJACENCY-ONLY clustering and produced meaningless mega-blobs (e.g. a single "8,606-ac / 146-parcel"
  and "14,109-ac / 202-parcel" cluster spanning a dozen different zones and owners). **This run replaces
  that with a PER-PARCEL developable inventory** (each vacant parcel stands on its own), plus a separate
  contiguity grouping (contig_group) that shows contiguous vacant blocks WITHOUT falsely fusing them into
  one "owner."
- A vacant parcel is kept as "developable" if it is NOT an HOA/condo/detention/irrigation/open-space lot
  (flagged from LEGAL/SUBNM text — the key improvement enabled by pulling the legal fields), has public
  base zoning, is not Parks/Open-Space or Slope-Protection in the comp plan, is >= 1.0 acre, and passes a
  Polsby-Popper compactness floor (0.16) that drops road slivers and pipestems.
- A research-priority score (contiguous-block size + MF-threat + FLU intent + proximity) orders which
  sites got deep ownership/intent research; it is a triage aid, not the final judgment.

## 10. Ownership & intent — reasoned per site
- For each material developable site, ownership, tenure, owner identity, and development intent were
  researched from public development applications, city P&Z / Council staff reports, BoiseDev / COMPASS /
  KTVB / Idaho Statesman reporting, and the Idaho Secretary of State business registry. Each dossier
  carries a confidence rating and its sources. Dormant raw-land sites with no application are reported as
  such, with the comp-plan-planned use and current use, rather than inventing an owner or a project.

## 11. Sources & vintage
- Parcels/zoning/FLU: AdaCountyGIS ArcGIS Online, pulled 2026-07-14. Assessor values are the current roll.
- Ordinances: Boise Modern Zoning Code (2023), Meridian UDC, Ada County Title 8 (2024).
- Ownership/intent reporting is dated per source in the Ownership & Intent sheet (mostly 2019-2026).

---

# AUGUST 2026 RE-RUN — BLIND-SPOT AUDIT & CORRECTED METHODOLOGY

Re-run date: 2026-08-14. Trigger: the July run missed the subject's own marketed Phase II
("Seasons at Meridian II" / Overland & Wells II, H-2022-0030) on the touching parcel at
2600 E Overland — assessor-coded F (ag-exempt farm), so it never entered the PROPCODE-L
vacant screen, and filed under the subdivision name, so brand-name searches missed it.

## A. Phase A.5 — Subject master-plan & adjacency sweep (new mandatory gate)
1. **Phased-plan check:** The subject IS Phase 1 of a two-phase Morgan Stonehill plan inside
   the WinCo Wells subdivision (DA Inst. #2016-060157). Phase II = 351 units (345 at hearing)
   on 11.65 of the 18 ac at 2600 E Overland — **DENIED by City Council 10/25/2022** (Findings
   of Denial adopted 11/9/2022: employment-land loss, failing Overland/Eagle intersections,
   MF over-concentration next to Phase 1). No CUP ever issued; no re-application through
   Aug 2026. Owner of record was and remains **WinCo Foods, LLC** (Morgan Stonehill never took
   title); WinCo lot-split the parcel Feb 2025 along the future Cinema Dr extension and has
   marketed it since Jan 2024 (Colliers) as big-box/pad retail ground leases. Verdict:
   documented DEAD MF site, ~5% de-novo revival, earliest plausible delivery ~2030.
   Full paper trail: research/audit_2026-08/seasons_II_overland_wells_II_status.md.
2. **Same-developer sweep:** Morgan Stonehill's 69-project index lists no other Treasure
   Valley project; architect NG+P's "Seasons at Meridian II — Concept Design/Entitlements"
   page is stale pre-denial marketing (fails the recency lens).
3. **Touching-parcel inventory** (research/audit_2026-08/touching_parcels.json): S1117438630
   (the WinCo parcel, above) + five ~1-ac county-R1 homes on S Loder Pl (un-annexed enclave;
   assemblage-watch only). Across-the-ROW neighbors: Bonito Sub commercial (E), Gramercy (S),
   Magic View/Freeway Dr (N).

## B. Vacant-screen correction
- `vacant_buckets` widened from PROPCODE L only to **L + F (ag-exempt farm)** — farms are the
  canonical sell-and-develop pipeline (Syringa, Graycliff, Brighton plans all began as F).
  Result: 552 candidate clusters (vs 481 L-only); the 2600 E Overland parcel is now the #1
  nearest candidate, as it should have been in July.
- Large-lot homesteads (R/M ≥5 ac, 443 in ring) were swept by reasoning (not auto-candidates):
  closest are the Magic View RUT 5-ac lots (0.3-0.6 mi) — now the Latitude Forty Three
  79-home for-sale application (H-2024-0059, council pending) — and Victory Rd RUT acreage
  (county rural-residential; benign).

## C. Ring-wide entitlement re-audit (research/audit_2026-08/ring_sweep_findings.md)
- **Missed and now added:** Pine 43 expansion H-2024-0071 (approved 10/21/2025 — 270-unit MF
  CUP entitled now + up to ~604 vertically-integrated units; legacy-name filing); Outer Banks
  516u (groundbreaking expected 2026); District at Ten Mile ~1,800-unit master plan (broke
  ground May 2026, retail-led coverage); Modern Craftsman Franklin 122 BTR (2023 filing,
  status unverified).
- **Corrections:** Cole Denton now 224u (May 2026 refile); Syringa now 302u CUP (remanded;
  re-heard 8/6/2026, outcome unpublished); Emblem formal plans filed June 2026 (250u).
- **Confirmed dead:** Newkirk 216u→for-sale homes; Village at Meridian 549u expansion
  scrapped; The Hummingbird expired; Overland & Wells II denied (above).
- Root causes across all misses: (1) modifications filed under legacy master-plan names,
  (2) plat-style names with no apartment brand, (3) approval swaps on parcels with a dead
  prior deal, (4) assessor farm coding. All four are now standing checks in the skill.

## D. Ranking (Aug 2026)
Reasoned ranking rewritten (in/reasoned_ranking.json): Pine 43, Outer Banks, Emblem, Records
(dormant-entitled), Tanner Creek, Graycliff R-40, Ten Mile/District node lead; 2600 E Overland
carried as Low-Watch (dead, documented); Latitude 43 Low (for-sale SF); Kleiner Trust 72 ac
Low-Watch (inert). Unverifiable items are labeled as data gaps, never guessed.

## Refresh — August 23, 2026 (full re-pull + recheck)
- Trigger: user-flagged "discrepancies" (1999 S Gedalio Ln, 2015 E Victory Rd) — both verified
  correct against the live roll (see `research/audit_2026-08/landuse_zoning_spotcheck_2026-08-23.md`);
  a full data refresh was then run to bring every layer current.
- Re-pulled everything: 92,792 parcels (July: 92,790), 1,545 zoning polys (7 jurisdictions),
  112,605 attribute rows, FLU (Boise 149 / Meridian 582 / Ada 25 polys). Zero unmapped zone or
  land-use codes. Bucket shifts vs July are noise-level: Vacant Land 10,810 → 10,800 (lots built
  out), SFR +13, Commercial +1, Ag −1.
- Developable-vacant clusters: 552 → 554. Two clusters changed composition via replats
  (S Linder Rd 391-ac cluster: one parcel renumbered R6961010010→R6961010011; S Meridian Rd
  cluster: 69.4→70.2 ac with two renumbered Kuna parcels incl. a C-1 sliver). Two genuinely new
  clusters, both reasoned Low: 12408 W AMITY RD (11.38 ac, Ada RSW, 2.32 mi — SF plat trajectory)
  and an unaddressed 3.12-ac Meridian R-4 pair at the NW edge (4.46 mi). All 552 prior verdicts
  re-join the fresh cluster set with no orphans; the 19-site reasoned ranking re-joins unchanged.
- Entitlement recheck (web, 8/23): Syringa Crossing (H-2025-0007) was re-heard by P&Z 8/6/2026
  after Council remanded the April denial recommendation — outcome NOT yet published; noted in
  ranking #6. Rolling Hill (Assemble) confirmed APPROVED by Council 5/19/2026 at 200u + 19.5k sf
  commercial (already carried as pipeline in the supply chart; its site is not vacant-coded land).
  Emblem (2820 S Eagle) June 2026 early plans already reflected in ranking #3. Hawkins' new
  252-unit Ustick/McDermott filing (BoiseDev 8/6/2026) is OUTSIDE the 5-mi ring — noted, excluded.
  Centrepoint 213u + Delano 84u verified already tracked in the supply roster (no gap).
