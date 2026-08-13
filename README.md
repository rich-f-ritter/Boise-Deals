# Boise Deals — Developable-Land Analysis: Canyon Ridge vs Seasons at Meridian

A granular, parcel-level land-use and **developable-land availability** comparison of the areas around
two Treasure Valley apartment communities, built to answer: *who owns the developable land nearby, since
when, who they are, and what they are going to do with it.*

- **Canyon Ridge** — 2552 E Gowen Rd, SE Boise (by the Boise Airport / Gowen Field)
- **Seasons at Meridian** — 2700 E Overland Rd, SE Meridian

Each area is analyzed within a **5.0-mile radius**. This is a substantially expanded, corrected, and
owner-researched successor to an earlier Canyon Ridge-only draft.

## Headline finding

**Seasons at Meridian sits on ~8× the apartment-ready developable land as Canyon Ridge — and near Seasons
it is already being built out by the region's largest master developers.**

| Metric (5-mi radius) | Canyon Ridge | Seasons at Meridian |
|---|---:|---:|
| Parcels classified | 28,026 | 92,773 |
| Total developable vacant land | 502 parcels · 12,323 ac | 891 parcels · 3,901 ac |
| **Apartment-ready** (MF-zoned *or* comp-plan multifamily) | **44 parcels · 143 ac** | **228 parcels · 1,130 ac** |
| …within 2 miles of the subject | 9 parcels · 40 ac | 89 parcels · 309 ac |
| Multifamily-by-right (High) land | 32 parcels · 102 ac | 96 parcels · 507 ac |
| Active residential/apartment pipeline | Minimal | Heavy & ongoing |

Canyon Ridge's larger *raw* vacant acreage is Micron's chip fabs + Simplot rangeland (planned for ~20,000
future homes but **stalled** for lack of a second wildfire-evacuation road), the Boise Airport and its
Airport-Influence-Area overlay that **prohibits new housing**, city-owned Gateway East industrial parks
(Boyer, Flint), and foothills land now being converted to open space — almost none of it can become
competing apartments. Near Seasons, the land is controlled by **Brighton Corporation** (Ten Mile Crossing;
the 800-ac Pinnacle/Apex community with a rumored Costco town center), **Ball Ventures Ahlquist**,
**Hawkins Companies**, **Quarterra/Lennar**, **CBH Homes**, **Star Development** and others, with apartment
projects already built, approved, or proposed (Aren 396, The Flats 235, Outer Banks 516, Graycliff 224,
Tanner Creek 280, Emblem 250, Overland/Assemble 200, and more).

## Deliverables

- **`summary/Treasure Valley - Development Opportunity Summary Map.html`** — the combined **development-opportunity
  summary map**. One interactive map of both areas that reframes raw parcels into *what governs apartment supply*:
  competing/ready apartment land, Micron's campus, the airport & its influence-area "moat" (new housing barred),
  industrial, long-term land-bank, and context. Like-kind parcels are **dissolved into labeled sections** (click any
  for owner/intent); off-limits categories are **hatched** so go-vs-no-go reads in five seconds. Built and refined
  over three agent-reviewed iterations.
- **`comparison/Canyon Ridge vs Seasons - Developable Land Comparison.html`** — the head-to-head report:
  scorecard, supply-by-intent charts, the synthesis-map summary, and all 30 researched ownership/intent dossiers
  (also published as a shareable Claude artifact).
- **`CanyonRidge/Canyon Ridge - Land Use Analysis.xlsx`** and **`SeasonsMeridian/Seasons at Meridian - Land
  Use Analysis.xlsx`** — the full auditable workbooks. Sheets: Overview · Assumptions & Decisions ·
  Ownership & Intent · Supply Summary · Developable Inventory · Parcels (every classified parcel, enriched) ·
  Land-Use Grouping · Zoning Grouping (7 jurisdictions) · Future Land Use · Data Sources · Methodology.
- **`*/… - Land Use Viewer.html`** — self-contained interactive maps (Land Use / Zoning / Vacant-Threat over
  satellite & street basemaps). Canyon Ridge ~15 MB; Seasons ~46 MB (92k parcels, canvas-rendered).
- **`*/Tables/*.csv`** — the underlying tables (developable inventory, supply summary, FLU summary,
  crosswalks, decisions log).

## Underwriting knowledge base (`knowledge/`)

- **`knowledge/Seasons-Meridian-Replacement-Cost-and-Supply-Economics.md`** — full cross-deal analysis
  (2026-08-13): Seasons bid vs. replacement cost / replacement value, rent-to-pencil today **and at exit**,
  pro forma normalization (Meridian ~0.45% vs Boise ~0.92% taxes; garage/wifi other-income differences),
  the Emblem (Quarterra) & Hawkins ("The Judy") development equity books, the Canyon Ridge award, and how our
  Prelude at Paramount acquisition anchors the market coherence map. Includes risk register and open items.
- **`knowledge/deal_metrics.json`** — machine-readable key metrics for all five deals + pencil-rent analysis.

## How it was built (`land-use-analysis/`)

A config-driven pipeline over public GIS, with the locale-specific knowledge and the ownership/intent
research reasoned per run:

1. **Pull** Ada County Assessor parcels + one countywide zoning layer (split by `CITY` into 7 jurisdictions)
   via robust POST/objectId paging with checkpoint-resume.
2. **Classify** land use (PROPCODE) and base zoning → category + multifamily-supply threat (crosswalk verified
   against the Boise Modern Zoning Code, Meridian UDC, and Ada County Title 8 — **0 unmapped codes**).
3. **Enrich** every parcel with subdivision, homestead (owner-occupancy), assessor value, an HOA/common-lot
   flag from the legal text, and the **adopted Future Land Use** (comp-plan) designation — the "what is it
   planned for" signal.
4. **Inventory** developable vacant land **per parcel** (fixing the prior run's null-owner "mega-blob"
   artifact), removing HOA/common, detention, floodplain, sliver and sub-acre parcels; group contiguous
   blocks without fusing owners.
5. **Research** ownership, tenure, entity identity, and development intent for the material sites.
6. **Build** the workbooks, viewers, and comparison report.

### The owner-data limit (and how it's handled)

Idaho does not publish parcel owner names in the free county GIS, and the county's lookup portal is
reCAPTCHA-gated for reference only — so a bulk owner roll is not possible. "Who owns what, since when, who
they are, and what they'll do with it" is answered by **researching the material developable sites
individually** from development applications, city P&Z/Council staff reports, COMPASS filings, BoiseDev /
Idaho Statesman / KTVB reporting, and the Idaho Secretary of State registry. Owners that could not be
identified from public records are labeled *"not publicly identified"* — never fabricated. Every dossier
carries a confidence rating and its sources; treat "inferred/derived" owners as leads, not title.

## Repo layout

```
comparison/       head-to-head report + comparison data + all dossiers (JSON)
CanyonRidge/      config.json · workbook · viewer · Tables/ · in/ (analysis JSON)
SeasonsMeridian/  config.json · workbook · viewer · Tables/ · in/ (analysis JSON)
research/         per-site research packets + raw dossier JSON
land-use-analysis/ the pipeline (scripts + reference playbooks)
```

Large regenerable intermediates (`in/parcels_*.geojson`, checkpoints) are git-ignored; the interactive
viewers embed their own data and are self-contained.
