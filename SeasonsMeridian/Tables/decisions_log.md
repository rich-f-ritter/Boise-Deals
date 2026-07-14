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
