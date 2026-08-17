# Seasons at Meridian — Replication-Cost Reconstruction (~$328K/u)

**Status: RECONSTRUCTION, 2026-08-16 — not the original analysis.** Prior work (recalled as landing near
~$328K/unit to replicate Seasons specifically) is not in this repo and appears to have been chat-only in
an earlier session; it predates the CLAUDE.md knowledge-capture protocol. This file rebuilds the estimate
from captured components so the number has a defensible basis until/unless the original is recovered.
Note the numeric proximity to the $118M bid per unit ($327.8K) — confirm the recalled figure is the
replication cost, not the bid, before quoting history.

## Build-up (per unit, 360u garden, 932.46 SF avg, 335,685 NRSF)

| Component | Emblem basis | Seasons replication | Basis for difference |
|---|---|---|---|
| Hard cost incl. contingency | $213.2K ($54.58M/256; $227/NRSF on 939 SF) | **~$218K** | $227/NRSF × 932.46 SF = $211.7K, escalated 3%/yr to a mid-2027 start |
| A&E + dev fee + soft costs + P&F | $48.1K ($12.31M/256) | **~$48K** | Same jurisdiction; Meridian P&F ~$17.4K/u inside |
| Land & acquisition | $35.5K ($9.09M; $649K/ac × 13.63 ac, 18.8 u/ac corridor site) | **~$50–56K** | Hard-corner I-84/Eagle Rd interchange land is retail-priced — placeholder ~$900K–1.0M/ac at ~18 u/ac garden density. **The one input needing real comps.** |
| Financing costs (in TDC) | $7.7K ($1.98M/256) | ~$8K | Same convention |
| **All-in TDC** | **$304.5K** | **~$325–330K/u** | |

**Reconstruction lands at ~$328K/u ± the land assumption.** The delta vs. the Emblem benchmark is almost
entirely land: a like-for-like Seasons cannot be built at Emblem's corridor land basis.

## Why this matters (framing implications)

- At $122M ($338.9K/u), the bid is ~**1.03–1.05x** Seasons-specific replication cost — vs 1.11x the
  generic Emblem benchmark ($304.5K). Materially friendlier framing, and it is location-honest: the
  banned "below replacement cost" claim stays banned, but "at approximately replication cost for this
  site" may be defensible once land is evidenced.
- Consistency check: knowledge base carries "Seasons at 1.08x replacement cost" (vs $305K at the $118M
  bid) and replacement *value* ~$355–400K/u. This reconstruction sits between: cost to build *this asset
  on this corner* > generic Meridian garden cost, < replacement value.

## Open items to harden

- [ ] Land comps for the I-84/Eagle interchange quadrants ($/ac, 2025–26 prints) — replaces the placeholder.
- [ ] Confirm Seasons site acreage (Ada County parcel) → actual units/acre for the land line.
- [ ] Amenity/clubhouse scope differential vs Emblem BTR (Seasons has wifi infrastructure, pool, clubhouse;
  Emblem has attached garages in hard cost) — sign ambiguous, likely small.
- [ ] Recover the original analysis if any artifact exists (slide, workbook, email) and reconcile.
- [ ] If hardened: add as `7_Seasons_Replication` tab in `Boise_Deals_Normalized_Underwriting_v2.xlsx`
  (extend `build_wb2.py`).

**Provenance:** Emblem components from `knowledge/exhibits/build_wb2.py` cost build-up (Summary D25 /
3_Dev_Feasibility): land $9,092,960; hard incl. contingency $54,579,077; A&E $1,500,605; dev fee
$2,658,062; financing $1,982,846; TDC $77,959,624 / 256u. Seasons NRSF/mix from v3 model Assumptions.
Escalation 3%/yr per both dev models.
