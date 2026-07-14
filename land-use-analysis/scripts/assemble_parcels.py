"""Memory-safe assembler: build in/parcels_all.geojson from cached _ck/*.json checkpoints
by streaming (never holds the whole FeatureCollection as one JSON string). Replicates
pull_parcels' normalization + representative-point in-poly filter + dedupe on PARCEL.
Use when a very dense pull fetched all batches but the final one-shot json.dumps write failed.
"""
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import geo  # noqa: E402
from shapely.geometry import shape  # noqa: E402


def main():
    cfg = C.load()
    IN = C.indir(cfg)
    poly = geo.analysis_polygon(cfg)
    src = cfg["parcel_sources"][0]
    fm = src["fields"]
    county = src.get("county")
    dconf = src.get("data_confidence", "full")
    sname = src.get("name")
    dd = src.get("dedupe_field")  # PARCEL source field

    def norm(p):
        def g(key):
            f = fm.get(key)
            v = p.get(f) if f else None
            return v.strip() if isinstance(v, str) else v
        return {"account": g("account"), "owner": g("owner"), "situs": g("situs"),
                "landuse_code": (g("landuse_code") or ""), "legal": g("legal"),
                "county": county, "impr_value": g("impr_value"),
                "total_value": g("total_value"), "year_built": g("year_built"),
                "data_confidence": dconf, "source": sname}

    files = sorted(glob.glob(str(IN / "_ck" / "*.json")))
    out = IN / "parcels_all.geojson"
    seen = set()
    kept = 0
    scanned = 0
    with open(out, "w", encoding="utf-8") as fh:
        fh.write('{"type": "FeatureCollection", "features": [')
        first = True
        for cf in files:
            try:
                feats = json.load(open(cf))["features"]
            except Exception:
                continue
            for ft in feats:
                scanned += 1
                p = ft.get("properties", {}) or {}
                key = p.get(dd) if dd else None
                if dd and key in seen:
                    continue
                g = ft.get("geometry")
                if not g:
                    continue
                try:
                    if not shape(g).representative_point().within(poly):
                        continue
                except Exception:
                    continue
                if dd:
                    seen.add(key)
                feat = {"type": "Feature", "geometry": g, "properties": norm(p)}
                fh.write(("" if first else ", ") + json.dumps(feat))
                first = False
                kept += 1
        fh.write('], "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}}')
    print(f"scanned {scanned} raw features -> kept {kept} unique in-area parcels -> {out}")


if __name__ == "__main__":
    main()
