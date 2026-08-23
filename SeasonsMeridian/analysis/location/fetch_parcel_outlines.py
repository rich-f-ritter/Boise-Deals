#!/usr/bin/env python3
"""Fetch true parcel-contoured outlines for the location map's large key places
from the Ada County Parcels FeatureServer, dissolve per campus with shapely,
and cache to parcel_outlines.json (keyed by the POI's parcel_key).

Campus membership is by subdivision name (SUBNM) and/or explicit parcel numbers,
established by point-sampling the anchor buildings (Aug 23, 2026).
"""
import urllib.request, urllib.parse, json, pathlib
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

BASE = "https://services2.arcgis.com/dgGjZc6xAH5m5JyP/arcgis/rest/services/Parcels/FeatureServer/5/query?"
HERE = pathlib.Path(__file__).parent

CAMPUSES = {
    # parcel_key: dict(subnm_like=[...], parcels=[...])
    "village":     dict(subnm_like=["CENTERCAL SUB%"]),
    "kleiner":     dict(parcels=["S1104314807"]),
    "roaring":     dict(parcels=["R4239771050", "R4239770510"]),
    "district":    dict(subnm_like=["VANGUARD VILLAGE SUB%"], parcels=["S1215131410"]),
    "tmcrossing":  dict(subnm_like=["TM CROSSING SUB%", "TM CENTER EAST SUB%"]),
    "silverstone": dict(subnm_like=["RACKHAM SUB%", "ROLLING HILL SUB%", "SILVERSTONE SUB%"],
                        parcels=["S1116233803"]),   # + St. Luke's campus parcel
    "eldorado":    dict(subnm_like=["BONITO SUB%", "EL DORADO SUB%"]),
    "scentsy":     dict(subnm_like=["SCENTSY COMMONS SUB%"]),
    "wincowells2": dict(parcels=["S1117438630"]),  # adjacent 18-ac WinCo retail site (plat not yet in GIS layer)
    "touchmark":   dict(parcels=["S1116120662", "S1116131260"]),  # Touchmark Meadow Lake Village campus + undeveloped land
}

def query(where):
    feats, offset = [], 0
    while True:
        params = {'f': 'json', 'where': where, 'outFields': 'PARCEL,ACRES,SUBNM',
                  'returnGeometry': 'true', 'outSR': '4326', 'resultOffset': offset,
                  'resultRecordCount': 200}
        d = json.load(urllib.request.urlopen(BASE + urllib.parse.urlencode(params), timeout=40))
        f = d.get('features', [])
        feats += f
        if len(f) < 200:
            return feats
        offset += 200

def outline(spec):
    clauses = []
    for s in spec.get('subnm_like', []):
        clauses.append(f"SUBNM LIKE '{s}'")
    for p in spec.get('parcels', []):
        clauses.append(f"PARCEL = '{p}'")
    feats = query(' OR '.join(clauses))
    polys = []
    for f in feats:
        for ring in f.get('geometry', {}).get('rings', []):
            if len(ring) >= 4:
                polys.append(Polygon([(x, y) for x, y in ring]).buffer(0))
    if not polys:
        return None, 0, 0
    # small buffer closes slivers between adjacent parcels (roads/ROW stay holes if wide)
    u = unary_union([p.buffer(3e-5) for p in polys]).buffer(-3e-5).simplify(1.5e-5)
    acres = sum(f['attributes']['ACRES'] or 0 for f in feats)
    geoms = list(u.geoms) if isinstance(u, MultiPolygon) else [u]
    # drop crumbs, keep exterior rings only (holes are parcel-data slivers at this scale)
    geoms = [g for g in geoms if g.area > 2e-7]
    rings = [[[round(y, 6), round(x, 6)] for x, y in g.exterior.coords] for g in geoms]
    return rings, len(feats), round(acres, 1)

def main():
    out = {}
    for key, spec in CAMPUSES.items():
        rings, n, acres = outline(spec)
        if rings:
            out[key] = rings
            print(f"{key}: {n} parcels, {acres} ac, {len(rings)} ring(s), "
                  f"{sum(len(r) for r in rings)} pts")
        else:
            print(f"{key}: NO PARCELS FOUND")
    (HERE / 'parcel_outlines.json').write_text(json.dumps(out))
    print('wrote parcel_outlines.json')

if __name__ == '__main__':
    main()
