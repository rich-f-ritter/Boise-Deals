1. Subject resolution — geocoded 2700 E Overland Rd, Meridian, ID 83642 to 43.591935, -116.360877 (verified against satellite + parcel).
2. Analysis area — 5.0-mile geodesic radius; every parcel whose representative point falls inside is included.
3. Parcels — Ada County Assessor (no owner field). Land use from PROPCODE; value, subdivision, homestead,
   legal text and assessor acreage joined for enrichment.
4. Zoning — one countywide Ada layer split by CITY into 7 jurisdictions; each district crosswalked to a
   category + a multifamily-supply threat tier (High=by-right, Medium=conditional, Low=not permitted,
   Unknown=planned/overlay) against the actual ordinance.
5. Future Land Use — adopted comp-plan designation joined to every parcel (city plan over county) as the
   "what it's planned for" / rezone-likely signal.
6. Developable inventory — per-parcel (not owner-blob) vacant land, after removing HOA/common/detention/
   open-space lots, data-gap zoning, non-buildable comp-plan land, sub-1-acre lots, and road slivers;
   contiguous blocks grouped without fusing owners.
7. Ownership & intent — researched per material site (who owns it, since when, who they are, what they plan)
   from development applications, city staff reports, local reporting, and the Idaho business registry.
8. Deliverables — this workbook (fully auditable), an interactive HTML map viewer (land use / zoning /
   vacant-threat), and a head-to-head developable-land comparison with Canyon Ridge.

## Supply-chart integration (added July 2026)

9. Supply chart — a 5-mile competitive Supply Chart (CoStar + RealPage + HelloData
   reconciliation, `<deal>/supply/`) now sits on top of this land-use analysis:
   - `supply_crosswalk.csv` (this folder) maps every under-construction / proposed /
     lease-up deal in the supply chart to the nearest developable-vacant parcel in
     this analysis. A pipeline deal sitting on a developable parcel means that
     acreage is already tracked supply — count it once, not as additional latent land.
   - The land-use dossier sites that are genuinely apartment-competitive but NOT in
     any vendor pipeline feed the supply chart's Diligence sheet as `type=shadow`
     watch rows (plotted on the companion map); they are documentation, not forecast
     supply.
   - Direction of flow: land-use analysis = latent capacity (could be built);
     supply chart = tracked pipeline (is being built / formally proposed). The
     crosswalk is the bridge that prevents double-counting between the two.
