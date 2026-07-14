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
