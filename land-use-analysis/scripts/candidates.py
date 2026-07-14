"""Granular developable-vacant-land inventory (replaces the prior run's owner-cluster step,
which — because Ada County publishes no owner names — collapsed into adjacency-only mega-blobs
that merged unrelated parcels across a dozen zones). Here we keep PER-PARCEL granularity and
add a contiguity group so contiguous vacant blocks are visible without being falsely fused.

Developable filter (each vacant parcel):
  drop HOA/condo common areas, detention/irrigation/open-space lots (legal-text flag),
  drop data-gap zoning, roads/slivers (Polsby-Popper compactness), sub-min acreage,
  drop Parks/Open Space & Slope-Protection FLU (not buildable).
Kept parcels retain airport/industrial/commercial context (all developable land, not only MF).

Outputs:
  in/developable.json            — per-parcel developable candidates (rich attributes)
  Tables/developable_parcels.csv — same, flat
  Tables/supply_summary.csv      — area-level rollups (the comparison backbone)
"""
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from shapely.geometry import shape
from shapely.ops import transform
from shapely.strtree import STRtree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import geo  # noqa: E402

NON_BUILDABLE_FLU = {"Parks/Open Space", "Slope Protection"}


def main():
    cfg = C.load()
    IN, TBL = C.indir(cfg), C.tables(cfg)
    to_local = geo.local_transform(cfg)
    min_acres = float(cfg.get("min_acres", 1.0))
    min_compact = float(cfg.get("min_compactness", 0.16))

    feats = json.loads((IN / "parcels_enriched.geojson").read_text())["features"]

    kept, drop = [], defaultdict(int)
    total_vacant = 0
    tiny_vacant_ac = 0.0
    tiny_vacant_n = 0
    for f in feats:
        p = f["properties"]
        if not p.get("is_vacant"):
            continue
        total_vacant += 1
        if p.get("is_hoa_common"):
            drop["hoa/common/detention/open-space"] += 1
            continue
        if p.get("zone_category") == cfg.get("data_gap_label", "No public zoning (data gap)"):
            drop["no-zoning"] += 1
            continue
        if p.get("flu_designation") in NON_BUILDABLE_FLU:
            drop["parks/slope-protection FLU"] += 1
            continue
        ac = p.get("acres") or 0
        if ac < min_acres:
            drop[f"under {min_acres} ac"] += 1
            tiny_vacant_n += 1
            tiny_vacant_ac += ac
            continue
        try:
            gp = transform(to_local, shape(f["geometry"]))
            if not gp.is_valid:
                gp = gp.buffer(0)
        except Exception:
            drop["bad-geometry"] += 1
            continue
        compact = 4 * math.pi * gp.area / (gp.length ** 2) if gp.length else 0
        if compact < min_compact:
            drop["road/sliver shape"] += 1
            continue
        p["_compact"] = round(compact, 3)
        kept.append((shape(f["geometry"]), p))

    # contiguity grouping (touch/very-near) — NOT owner-based; just shows contiguous blocks
    geoms = [g for g, _ in kept]
    tree = STRtree(geoms) if geoms else None
    parent = list(range(len(kept)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, (g, _) in enumerate(kept):
        gb = g.buffer(0.0002)  # ~22 m: bridges road-width gaps between commonly-developed tracts
        for j in tree.query(gb):
            if j > i and gb.intersects(geoms[j]):
                parent[find(i)] = find(j)

    groups = defaultdict(list)
    for i in range(len(kept)):
        groups[find(i)].append(i)
    gid_of = {}
    group_acres = {}
    for k, (root, members) in enumerate(sorted(groups.items(),
                                        key=lambda kv: -sum(kept[i][1]["acres"] for i in kv[1])), 1):
        gac = round(sum(kept[i][1]["acres"] for i in members), 2)
        for i in members:
            gid_of[i] = k
        group_acres[k] = (gac, len(members))

    def interest(p, gac):
        s = 0.0
        s += min(gac, 120) * 1.0                       # size of the contiguous block it belongs to
        s += {"High": 40, "Medium": 20, "Low": 5, "Unknown": 15}.get(
            str(p.get("mf_threat")).split("-")[0], 0)
        intent = p.get("flu_intent") or ""
        s += 35 if "multifamily" in intent else 15 if "attached" in intent else \
            8 if "master-plan" in intent or "development-ready" in intent else 0
        s += max(0, 12 - (p.get("dist_mi") or 0) * 2)  # closer = more relevant
        return round(s, 1)

    rows = []
    for i, (g, p) in enumerate(kept):
        gid = gid_of[i]
        gac, gn = group_acres[gid]
        rows.append({
            "account": p.get("account"), "situs": p.get("situs"),
            "subdivision": p.get("subdivision"), "acres": p.get("acres"),
            "assessor_acres": p.get("assessor_acres"), "total_value": p.get("total_value"),
            "jurisdiction": p.get("jurisdiction"), "zone_code": p.get("zone_code"),
            "zone_plain": p.get("zone_plain"), "zone_category": p.get("zone_category"),
            "mf_threat": p.get("mf_threat"), "bucket": p.get("bucket"),
            "flu_source": p.get("flu_source"), "flu_designation": p.get("flu_designation"),
            "flu_plain": p.get("flu_plain"), "flu_intent": p.get("flu_intent"),
            "dist_mi": p.get("dist_mi"), "compactness": p.get("_compact"),
            "contig_group": gid, "contig_group_acres": gac, "contig_group_parcels": gn,
            "lat": p.get("lat"), "lon": p.get("lon"),
            "interest": interest(p, gac),
            "legal": (p.get("legal_full") or "")[:80],
        })
    rows.sort(key=lambda r: -r["interest"])

    (IN / "developable.json").write_text(json.dumps(rows, indent=2))
    with open(TBL / "developable_parcels.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- area-level supply rollups (comparison backbone) ----
    dev_ac = round(sum(r["acres"] for r in rows), 1)
    by_threat = defaultdict(lambda: [0, 0.0])
    by_intent = defaultdict(lambda: [0, 0.0])
    by_juris = defaultdict(lambda: [0, 0.0])
    for r in rows:
        t = str(r["mf_threat"]).split("-")[0]
        by_threat[t][0] += 1; by_threat[t][1] += r["acres"]
        it = r["flu_intent"] or "n/a"
        by_intent[it][0] += 1; by_intent[it][1] += r["acres"]
        by_juris[r["jurisdiction"]][0] += 1; by_juris[r["jurisdiction"]][1] += r["acres"]
    with open(TBL / "supply_summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Metric", "Group", "Parcels", "Acres"])
        w.writerow(["TOTAL developable vacant", "", len(rows), dev_ac])
        w.writerow(["Vacant parcels in area (all)", "", total_vacant, ""])
        w.writerow([f"Dropped: under {min_acres} ac (small lots)", "", tiny_vacant_n, round(tiny_vacant_ac, 1)])
        for t, (n, a) in sorted(by_threat.items(), key=lambda kv: -kv[1][1]):
            w.writerow(["Developable by MF-threat", t, n, round(a, 1)])
        for it, (n, a) in sorted(by_intent.items(), key=lambda kv: -kv[1][1]):
            w.writerow(["Developable by FLU intent", it, n, round(a, 1)])
        for j, (n, a) in sorted(by_juris.items(), key=lambda kv: -kv[1][1]):
            w.writerow(["Developable by jurisdiction", j, n, round(a, 1)])

    print(f"developable vacant parcels: {len(rows)}  ({dev_ac} ac)  from {total_vacant} vacant")
    print("  dropped:", dict(drop))
    print(f"  MF-High developable: {by_threat['High'][0]} parcels / {round(by_threat['High'][1],1)} ac")
    print("  top-10 by research interest:")
    for r in rows[:10]:
        print(f"    int={r['interest']:5}  {r['acres']:6.1f}ac  d={r['dist_mi']:.2f}  "
              f"{str(r['mf_threat'])[:6]:6} {str(r['flu_plain'])[:22]:22} | "
              f"{str(r['situs'])[:24]:24} | grp{r['contig_group']}={r['contig_group_acres']}ac")


if __name__ == "__main__":
    main()
