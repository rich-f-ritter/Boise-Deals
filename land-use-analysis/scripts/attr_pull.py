"""Lightweight attributes-only pull from the Ada County parcels layer (no geometry) to enrich
the classified parcels with fields the normalized schema drops: SUBNM (subdivision — a strong
developer/plat signal), HOMEEXEMPT (owner-occupancy homestead exemption > 0 => owner-occupied,
not an investor/vacant hold), LEGAL1..5 (HOA 'COMMON AREA' detection), ZONING (assessor's own
zone string, cross-check), ACRES (assessor acreage), PROPYEAR, CITY_STATE. Keyed by PARCEL.
Paged by OBJECTID, returnGeometry=false, so it's fast even at 90k+ parcels.
Output: in/parcels_attrs.json  = { PARCEL: {attrs...} }
"""
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import geo  # noqa: E402

FIELDS = ["PARCEL", "SUBNM", "LEGAL1", "LEGAL2", "LEGAL3", "LEGAL4", "LEGAL5",
          "HOMEEXEMPT", "TOTALVALUE", "ZONING", "ACRES", "PROPYEAR", "CITY_STATE", "PROPCODE"]
H = {"User-Agent": "Mozilla/5.0"}


def main():
    cfg = C.load()
    IN = C.indir(cfg)
    url = cfg["parcel_sources"][0]["url"]
    minx, miny, maxx, maxy = geo.bbox(cfg)
    geom = json.dumps({"xmin": minx, "ymin": miny, "xmax": maxx, "ymax": maxy,
                       "spatialReference": {"wkid": 4326}})
    common = {"geometry": geom, "geometryType": "esriGeometryEnvelope",
              "spatialRel": "esriSpatialRelIntersects", "inSR": 4326, "f": "json"}

    ids = requests.post(url, data={**common, "where": "1=1", "returnIdsOnly": "true"},
                        headers=H, timeout=180).json()
    oid_field = ids.get("objectIdFieldName", "OBJECTID")
    oids = ids.get("objectIds") or []
    print(f"{len(oids)} object ids", file=sys.stderr)

    attrs = {}
    for i in range(0, len(oids), 1000):
        batch = oids[i:i + 1000]
        q = {"where": f"{oid_field} IN ({','.join(map(str, batch))})",
             "outFields": ",".join(FIELDS), "returnGeometry": "false", "f": "json"}
        r = requests.post(url, data=q, headers=H, timeout=180).json()
        for ft in r.get("features", []):
            a = ft.get("attributes", {})
            pid = a.get("PARCEL")
            if pid:
                attrs[pid] = {k: a.get(k) for k in FIELDS}
        print(f"  batch {i // 1000 + 1}/{(len(oids) + 999) // 1000}  attrs={len(attrs)}", file=sys.stderr)

    (IN / "parcels_attrs.json").write_text(json.dumps(attrs))
    print(f"wrote {len(attrs)} parcel attribute rows -> in/parcels_attrs.json")


if __name__ == "__main__":
    main()
