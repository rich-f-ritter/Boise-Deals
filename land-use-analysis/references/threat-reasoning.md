# The reasoned vacant-threat assessment (the core analytical output)

The "most concerning vacant parcels" ranking is a **reasoned judgment, not a deterministic
score.** `prepare_candidates.py` does only mechanical prep; you reason over its output and
write `in/reasoned_ranking.json`, which `finalize_topN.py` renders.

Why not a formula: a mechanical score (threat tier × acres × proximity) surfaces false
positives — HOA common areas / detention ponds / greenbelts zoned PD, remnant slivers,
floodplain, non-developable tracts, gov/airport land. Judgment is required: is the parcel
genuinely developable, is the PD actually entitled for MF, is the owner a developer vs an
HOA, is it the relevant submarket?

## Inputs
- `in/vacant_candidates.json` — clusters after mechanical filters (compactness, owner rules,
  data-gap, min acreage), each with: acres, parcel_count, min_dist_mi, owner, owner_type,
  zoning (`juris:code`), `zoning_threat_baseline`, compactness, location, lat/lon, parcels.
- The classified parcels + the zoning crosswalk + your knowledge of the submarket. Do
  **targeted research** where it changes the call (read a PD/PUD concept plan, check whether a
  corridor is actively adding apartments, confirm an owner is a developer vs an HOA/SPE).

## How to reason each candidate
For each plausible candidate ask:
1. **Developable?** Real buildable site, or a remnant/detention/greenbelt/floodplain/access
   sliver that slipped the filters? Drop the latter.
2. **MF basis?** By-right MF zoning (High) is the strongest threat. For PD/overlay (Unknown),
   what does the negotiated plan actually entitle? For corridor/mixed (Medium), how real is
   residential? For Low base zoning, is there genuine **rezoning optionality** given momentum
   (large single-owner tract on an active corridor) → call it "Low-Watch", not High.
3. **Owner.** Developer / homebuilder / investor SPE raises concern; HOA / church / school /
   gov / utility removes it.
4. **Submarket + distance.** Far parcels in a different submarket (e.g. >3 mi across a barrier)
   are de-prioritized even if large — say so.

## Output: `in/reasoned_ranking.json`
```json
{
  "headline": "one-paragraph supply-threat conclusion for the workbook + viewer",
  "ranking": [
    { "match": {"account": "12345"},                      // OR owner_prefix + location_prefix
      "reasoned_threat": "High|Medium|Low|Low-Watch|Unknown",
      "rationale": "why it is (or isn't) a concerning MF-supply site; cite the plan/corridor/owner" }
  ]
}
```
- Rank in concern order (most concerning first). 10 is typical; fewer is fine if that's the
  honest set. `reasoned_threat` is free text (so "Low-Watch" is allowed); the workbook color-
  keys on the leading word.
- Prefer `match.account` (exact) when you can; otherwise `owner_prefix` + `location_prefix`.

## Blind spots the mechanical vacant screen WILL have (sweep these by hand)

Case study (Seasons at Meridian, ID, 2026): the subject's own **351-unit Phase II** sat on the
parcel immediately next door and was missed by every layer of the analysis — the parcel was
assessor-coded **F (ag-exempt farm, $29.9k assessed on 18 ac)** so it never entered the
PROPCODE-L vacant screen; it was zoned C-G (MF only by CUP) so even in the screen it would have
ranked Medium; and its entitlement (a 2022 DA-mod + CUP) was filed as **"Overland and Wells II"**
— the subdivision name, not the "Seasons" brand — so name searches found nothing. Three
independent screens, three blind spots, one 500-ft miss.

Standing rules derived from it:
1. **Ag-exempt / farm-coded parcels are vacant-land-in-waiting.** In any growth corridor they
   are the primary land pipeline (locally: Syringa Crossing, Graycliff, and the Brighton master
   plans all began as this class). Enumerate every one within ~1.5 mi of the subject and reason
   over each individually — owner, zoning, FLU, listing/entitlement history.
2. **The touching parcels get individual dossiers, always** — every parcel adjacent to the
   subject, whatever its code, gets owner/zoning/entitlement checked (Phase A.5).
3. **The subject's own phasing is checked first** — if the subject is any phase of a larger
   plan, later phases are threat candidate #1 (Phase A.5).
4. **Entitlement search is alias-aware** — query by address, parcel/account number, owner
   entity, developer, and subdivision/plat name. A hit under any alias beats a miss under the
   marketed name.
5. **Large-lot homesteads (one house on development-scale acreage)** near the subject get the
   same treatment as farms.

## Always write the decisions log
Write `Tables/decisions_log.md` capturing every judgment call: subject point/override,
analysis-area choice, data sources used + rejected + coverage gaps, land-use source &
granularity, zoning crosswalk corrections, the vacant definition, the mechanical pre-filters,
and the reasoning behind the ranking + headline. This feeds the workbook's "Assumptions &
Decisions" sheet and is a hard requirement — these analyses must be auditable and reproducible.
```
# Land Use Analysis — <Subject> — Decisions Log
## 1. Subject location (verified point)
## 2. Analysis area
## 3. Parcel data source(s) + any degraded/missing coverage
## 4. Land-use source & granularity
## 5. Zoning sources + honest gaps
## 6. Zoning crosswalk corrections
## 7. "Vacant" definition
## 8. Vacant-threat assessment — reasoned, with the mechanical pre-filters listed
## 9. Sources & vintage
```
