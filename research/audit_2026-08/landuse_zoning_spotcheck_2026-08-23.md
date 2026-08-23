# Land Use vs Zoning — spot-check of two flagged parcels (Aug 23, 2026)

Two parcels in the Seasons at Meridian Land Use Viewer / Analysis workbook were flagged as
"serious discrepancies" between the LAND USE layer and the ZONING layer:

1. **1999 S Gedalio Ln** — zoning shows *Meridian Med-High Density Res (15 du/ac)* while the
   surrounding land-use layer shows *Single Family Residential*.
2. **2015 E Victory Rd** — land use shows *Single Family Residential* while zoning shows
   *County Rural-Urban Transition (RUT)*.

Both were re-verified against the **live Ada County Assessor parcel service**
(`services2.arcgis.com/dgGjZc6xAH5m5JyP/.../Parcels/FeatureServer/5`) on **2026-08-23**.
**Verdict: neither is an error.** The deliverable matches the county of record, and the
"mismatch" is the land-use-vs-zoning distinction the analysis is built on.

## Why the two layers are supposed to disagree

- **LAND USE** = what is physically on the parcel *today*, from the assessor's property
  class (PROPCODE: R improved residential / C commercial / F ag-exempt farm / L vacant land
  / M manufactured home).
- **ZONING** = what the ordinance *legally allows* on the parcel, from the countywide zoning
  layer split by jurisdiction.

They are independent layers by design (Decisions Log §4: neither is "corrected" from the
other), and the *difference between them is the analytic signal*: vacant or under-built land
inside a high-density zone is latent apartment supply; a built-out subdivision inside the
same zone is not.

## Parcel 1 — 1999 S Gedalio Ln (R5862020750)

| Field | Deliverable | Live county (8/23/2026) |
|---|---|---|
| PROPCODE | L (vacant) | **L** |
| Land-use bucket | Vacant Land | — (matches: L → Vacant Land) |
| Zoning | Meridian Med-High Density Res (15 du/ac) | **R-15** |
| Acres | 0.78 | 0.785 |
| Assessed value | — | **$0** |
| Legal | — | Lot 75 Blk 03, **Movado Sub No 02** |

- The parcel itself is a **0.78-acre, $0-assessed HOA common-area lot** in Movado
  Subdivision No. 02. The workbook's Parcels sheet correctly shows it as *Vacant Land*
  (not SFR), and it was correctly **excluded from the developable-vacant screen** (HOA
  common area, sub-1-acre).
- The surrounding sea of yellow on the land-use layer is the rest of **Movado — a Meridian
  subdivision annexed and zoned R-15 but built out as dense detached single-family / patio
  homes** (neighboring lots run 0.13–0.19 ac, all PROPCODE R). Meridian routinely zones
  compact detached product R-15; the district caps density at 15 du/ac, it does not mandate
  apartments.
- So: zoning layer red (R-15, multifamily-capable district) + land-use layer yellow (built
  single-family homes) is **both true simultaneously**, and it is exactly why Movado is *not*
  a supply threat despite its high-density zoning — the land is already consumed.

## Parcel 2 — 2015 E Victory Rd (S1129120742)

| Field | Deliverable | Live county (8/23/2026) |
|---|---|---|
| PROPCODE | R (improved residential) | **R** |
| Land-use bucket | Single Family Residential | — (matches: R → SFR bucket) |
| Zoning | County Rural-Urban Transition | **RUT** |
| Acres | 59.17 | 60.4 (minor assessor update; not material) |
| Assessed value | — | $563,700 |
| Homestead exemption | — | **−$61,163 (owner-occupied home on site)** |

- This is a **~60-acre unincorporated-county parcel with an owner-occupied homestead on
  it** (the homestead exemption on the roll proves the house). The assessor therefore codes
  it R → land-use bucket *Single Family Residential*.
- **RUT is Ada County's holding zone for exactly this**: rural land with scattered homes
  in a city Area of Impact, awaiting annexation. One house on 60 acres in a RUT zone *is*
  single-family use under rural-transition zoning — consistent, not contradictory.
- Threat classification is correct: RUT → *Agricultural/Rural, Low* (multifamily not
  permitted by base zone).
- Post-Seasons-II coverage check: because "large-lot homesteads" must be swept individually
  near the subject, this parcel **is captured in the ranchette sweep**
  (`SeasonsMeridian/in/farm_ranchette_parcels.json`, ranchette list, 59.23 ac) and is
  rendered in the occupied-large-lot overlay of *Vacant Land by Zoning (interactive)*. As
  latent land it would require annexation + rezone (multi-year, public process) before it
  could threaten supply; it is a watch parcel, not pipeline.

## Minor nits observed while verifying (not errors in the flagged parcels)

1. **Zoning Grouping sheet, Meridian R-15/R-40 note**: the sheet says multifamily is
   "BY-RIGHT — no special approval needed," while the Decisions Log (§6) correctly records
   that Meridian's UDC requires a **Conditional Use Permit** for multifamily even in
   R-15/R-40 (the districts exist for apartments, hence still tiered High). The Decisions
   Log wording is the accurate one; read the sheet's "by-right" as "High tier."
2. **Zoning Grouping sheet, City of Eagle row**: Eagle's "R-15" is labeled with the
   *Meridian* description ("Meridian Med-High Density Res (15 du/ac)"). Eagle uses its own
   ordinance; the label text was reused from the Meridian crosswalk. Tier (High) is
   unaffected for the study area — no Eagle R-15 parcels are in the 5-mi Seasons ring's
   developable set.

## Reading rule (add to standard practice)

When the LAND USE layer and the ZONING layer disagree, that is information, not error:

- **Vacant/farm use + high-density zone** → latent supply (the screen's core signal).
- **Built SFR use + high-density zone** (Movado) → consumed land, no threat.
- **SFR/homestead use + RUT/ag zone** (2015 E Victory) → rural holding pattern; threat only
  via annexation + rezone; tracked in the ranchette overlay.

Verified against live county data 2026-08-23; no rebuild of the deliverables is warranted.
