# Seasons at Meridian — Replication-Cost Reconstruction (~$328K/u, quality-of-product basis)

> **ORIGINAL RECOVERED (2026-08-20).** The prior work was NOT lost — it lives in
> `research/audit_2026-08/replacement_cost_analysis.md` (v3) + `replacement_cost_model.py` +
> `emblem_normalization.py`, merged into this branch via the audit branch (PR #9's content).
> **Canonical figure: Seasons-specific replication ≈ $322,530/unit (~$116.1M)** — above the generic
> ~$306K/u ($110M) Seasons-scale replacement, with the premium attributed to **the subject's amenity
> package AND superior land** (so RR's quality recollection and this file's earlier land guess were each
> half of the original attribution). Canonical required rent for new supply: **$2,224/u/mo normalized
> (+16.1% vs the $1,915 Y1 UW market rent)**, on Emblem ancillary income normalized $350.59 →
> $215.50/u/mo and observed cost escalation of +1.7%/yr. **Use the recovered figures, not this file's
> ~$328K, wherever one number is quoted.** This reconstruction is retained below as a convergence check —
> it landed within 1.7% of the original ($328K vs $322.5K) from independent components.

**Status: RECONSTRUCTION, 2026-08-16 — superseded by the recovered original above.** Prior work landed
near **~$328K/unit to replicate Seasons specifically**, with the delta vs. the generic Meridian benchmark
attributed to **quality of product** (per RR recollection, 2026-08-16 session). This file rebuilt the
arithmetic from captured components while the original was believed lost.
(An earlier draft of this file guessed the delta was land — the recovered original attributes the premium
to amenity package *and* land. Note also the numeric proximity to the $118M bid per unit, $327.8K —
coincidental.)

## The arithmetic

| | $/unit | Basis |
|---|---|---|
| Emblem all-in TDC (merchant-grade benchmark) | $304.5K | $77.96M / 256u; hard $227/NRSF incl. contingency ($216 GMP escalated) |
| **Quality premium to replicate Seasons** | **+$23.5K** | ≈ **+$25/NRSF** on 932 SF — hard cost $227 → **~$252/NRSF (+11%)** |
| **Seasons replication cost** | **~$328K/u** | |

The claim: the $214–216/NRSF GMP triangulation prices *merchant-grade* product (Emblem BTR / Judy). Seasons
is a higher-spec 2024 institutional build — evidence in the deal file: unit finishes (wood floors,
fireplaces in select homes per the rent-roll unit descriptions in the v3 model), full amenity package
(clubhouse/pool, property-wide managed-wifi infrastructure monetized at $1,077/u/yr — an install the
merchant books do not carry), and the finish level implied by Seasons' rent premium over same-vintage
merchant product. Replicating *that* asset runs ~+11% on hard cost ≈ **~$252/NRSF hard / ~$328K/u all-in**.

## Framing implications

1. **Basis:** at $122M ($338.9K/u) the bid is **~1.03x the cost of replicating this quality of product**,
   vs 1.11x the merchant-grade benchmark. The "below replacement cost" ban stands (we are above both),
   but "approximately at replication cost for like-quality product" is defensible once the premium is
   evidenced. At the prior $118M basis ($327.8K/u), the bid was ~1.00x — at parity with like-quality
   replication cost.
2. **Moat sharpener:** the pencil rents ($1,991–$2,122/mo at 6.0–6.5% YoC) are computed on the *merchant*
   cost basis. A developer building to **Seasons' quality** carries ~$328K/u and needs
   **~8% higher rents still** to hit the same yield — i.e., the true like-for-like competitor pencil is
   further out of the money than the headline gap. (Compounds with, and is distinct from, the
   product-matched OI adjustment that puts the Seasons-like pencil at ~$2.30–2.35/SF.)

## Open items to harden

- [ ] Recover the original analysis if any artifact exists (slide, workbook, email) and reconcile — the
  specific quality line items (finish schedule, amenity build-out, wifi infrastructure cost) were
  presumably itemized there.
- [ ] Evidence the +$25/NRSF premium independently: e.g., GC finish-level pricing tiers, Aren (0.62 mi,
  2024, 396u) cost data if obtainable, or the wifi-infrastructure install cost implied by the $1,077/u/yr
  revenue share.
- [ ] Secondary: Seasons' I-84/Eagle hard-corner land basis vs Emblem's $649K/ac corridor site — additive
  to the quality premium if the corner carries a land premium (kept out of the ~$328K to stay faithful to
  the recalled quality-of-product basis).
- [ ] If hardened: add as `7_Seasons_Replication` tab in `Boise_Deals_Normalized_Underwriting_v2.xlsx`
  (extend `build_wb2.py`).

**Provenance:** Emblem components from `knowledge/exhibits/build_wb2.py` (land $9,092,960; hard incl.
contingency $54,579,077; A&E $1,500,605; dev fee $2,658,062; financing $1,982,846; TDC $77,959,624 /
256u). Seasons NRSF 335,685 / 932.46 SF avg and unit-finish descriptions from the v3 model. Wifi revenue
share $1,077/u/yr from Assumptions other-income block. Escalation 3%/yr per both dev models.
