"""Enrich classified parcels with (a) the extra assessor attributes (SUBNM subdivision,
HOMEEXEMPT owner-occupancy, full LEGAL text, assessor ACRES/ZONING) and (b) the adopted
Future Land Use / Comprehensive Plan designation (Boise, Meridian, Ada County) joined by
representative point. FLU answers "what is this land PLANNED for" at the policy level — a
vacant parcel designated High Density / Mixed Use is a rezone-likely apartment site even if
its current base zoning is Low. Also derives:
  is_hoa_common  — legal/subdivision text marks it an HOA/condo common area (not developable)
  owner_occupied — homestead exemption > 0 (an occupied home, not an investor/vacant hold)
  flu_intent     — coarse residential-intensification signal from the FLU designation
Writes in/parcels_enriched.geojson (adds fields; geometry unchanged) + Tables/flu_summary.csv.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

import requests
from shapely.geometry import shape
from shapely.strtree import STRtree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import geo  # noqa: E402

ORG = "https://services2.arcgis.com/dgGjZc6xAH5m5JyP/arcgis/rest/services"
FLU_LAYERS = [  # (source label, service, field, priority) — city plans beat the coarse county layer
    ("Boise", f"{ORG}/Boise_Future_Land_Use/FeatureServer/0/query", "LandUse", 1),
    ("Meridian", f"{ORG}/Meridian_Future_Land_Use/FeatureServer/0/query", "class2", 1),
    ("Eagle", f"{ORG}/Eagle_Future_Land_Use/FeatureServer/0/query", None, 1),
    ("Ada County", f"{ORG}/Ada_County_Future_Land_Use/FeatureServer/0/query", "CATEGORY", 3),
]
H = {"User-Agent": "Mozilla/5.0"}

# FLU designation -> (plain, residential-intensification intent)
FLU_INTENT = {
    # Boise
    "High Density": ("High-Density Residential (planned)", "supports multifamily"),
    "Downtown Mixed Use": ("Downtown Mixed Use", "supports multifamily"),
    "Mixed Use": ("Mixed Use", "supports multifamily"),
    "Compact": ("Compact / walkable neighborhood", "supports attached/medium"),
    "Suburban": ("Suburban Residential", "single-family oriented"),
    "Buildable": ("Buildable (future growth)", "development-ready, use TBD"),
    "Large Lot/Rural": ("Large Lot / Rural", "low-density / rural"),
    "Commercial": ("Commercial", "non-residential (MF only if mixed)"),
    "Office": ("Office", "non-residential (MF only if mixed)"),
    "Industrial": ("Industrial", "non-residential"),
    "Parks/Open Space": ("Parks / Open Space", "not developable"),
    "Slope Protection": ("Slope Protection (foothills)", "not developable"),
    "School": ("School", "institutional"),
    "Public/Quasi-Public": ("Public / Quasi-Public", "institutional"),
    "Airport": ("Airport", "airport — residential restricted"),
    "PC": ("Planned Community", "master-plan (use TBD)"),
    "BSU Master Plan": ("BSU Master Plan", "institutional"),
    # Meridian
    "High Density Residential": ("High-Density Residential (planned)", "supports multifamily"),
    "Med-High Density Residential": ("Med-High-Density Residential (planned)", "supports multifamily"),
    "Medium Density Residential": ("Medium-Density Residential (planned)", "supports attached/medium"),
    "Low Density Residential": ("Low-Density Residential (planned)", "single-family oriented"),
    "MU-C": ("Mixed Use – Community", "supports multifamily"),
    "MU-RG": ("Mixed Use – Regional", "supports multifamily"),
    "MU-Com": ("Mixed Use – Commercial", "supports multifamily"),
    "MU-N": ("Mixed Use – Neighborhood", "supports attached/medium"),
    "MU-NR": ("Mixed Use – Non-Residential", "non-residential"),
    "MU-Res": ("Mixed Use – Residential", "supports multifamily"),
    "Mixed Use - Interchange": ("Mixed Use – Interchange", "supports multifamily"),
    "Ten Mile Interchange Specific": ("Ten Mile Interchange (specific area plan)", "master-plan (use TBD)"),
    "Old Town": ("Old Town", "supports multifamily"),
    "Civic": ("Civic", "institutional"),
    "General Industrial": ("General Industrial", "non-residential"),
    "Mixed Employment": ("Mixed Employment", "non-residential"),
    "Low Density Employment": ("Low-Density Employment", "non-residential"),
    "High Density Employment": ("High-Density Employment", "non-residential"),
    # Ada County
    "Rural": ("Rural (county)", "low-density / rural"),
    "Incorporated Cities and Areas of City Impact": ("City Impact Area", "see city plan"),
}


def load_flu(cfg):
    minx, miny, maxx, maxy = geo.bbox(cfg)
    geom = json.dumps({"xmin": minx, "ymin": miny, "xmax": maxx, "ymax": maxy,
                       "spatialReference": {"wkid": 4326}})
    geoms, props = [], []
    for label, url, field, prio in FLU_LAYERS:
        if field is None:
            continue
        try:
            r = requests.post(url, headers=H, timeout=180, data={
                "geometry": geom, "geometryType": "esriGeometryEnvelope",
                "spatialRel": "esriSpatialRelIntersects", "inSR": 4326,
                "outFields": field, "returnGeometry": "true", "outSR": 4326, "f": "geojson"})
            feats = r.json().get("features", [])
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] FLU {label} failed: {e}", file=sys.stderr)
            continue
        n = 0
        for ft in feats:
            g = ft.get("geometry")
            if not g:
                continue
            try:
                sg = shape(g)
                if not sg.is_valid:
                    sg = sg.buffer(0)
            except Exception:
                continue
            desig = str((ft.get("properties") or {}).get(field) or "").strip()
            geoms.append(sg)
            props.append((label, desig, prio))
            n += 1
        print(f"  FLU {label}: {n} polys", file=sys.stderr)
    tree = STRtree(geoms) if geoms else None
    return tree, geoms, props


HOA_RE = re.compile(r"COMMON\s*(AREA|LOT|OPEN|SPACE)|\bCOMMON\b|H\.?O\.?A\.?|OWNERS ASSOC|"
                    r"COMMON DRIVE|PRIVATE (RD|ROAD|ST|STREET|DRIVE|LANE|COMMON)|PATHWAY|"
                    r"LANDSCAP|OPEN SPACE|GREENBELT|DETENTION|PRESSURE IRRIG|LIFT STATION|"
                    r"WELL LOT|PUMP|SEWER|STORMWATER|PONDING|DRAINAGE|BUFFER LOT", re.I)


def main():
    cfg = C.load()
    IN, TBL = C.indir(cfg), C.tables(cfg)
    parcels = json.loads((IN / "parcels_classified.geojson").read_text())["features"]
    attrs = json.loads((IN / "parcels_attrs.json").read_text()) if (IN / "parcels_attrs.json").exists() else {}

    print("loading Future Land Use layers ...", file=sys.stderr)
    tree, fgeoms, fprops = load_flu(cfg)

    flu_count = Counter()
    out = []
    for f in parcels:
        p = dict(f["properties"])
        acct = p.get("account")
        a = attrs.get(acct, {})
        legal_full = " ".join(str(a.get(k) or "").strip() for k in
                              ("LEGAL1", "LEGAL2", "LEGAL3", "LEGAL4", "LEGAL5")).strip()
        subnm = str(a.get("SUBNM") or "").strip()
        homeexempt = a.get("HOMEEXEMPT") or 0
        p["subdivision"] = subnm
        p["legal_full"] = legal_full
        p["assessor_zoning"] = str(a.get("ZONING") or "").strip()
        p["assessor_acres"] = a.get("ACRES")
        p["total_value"] = a.get("TOTALVALUE")
        p["homeexempt"] = homeexempt
        # Idaho homestead exemption is stored as a negative amount (e.g. -125000);
        # any non-zero value => an owner-occupied primary residence (not a redevelopment hold).
        try:
            p["owner_occupied"] = bool(homeexempt and float(homeexempt) != 0)
        except (TypeError, ValueError):
            p["owner_occupied"] = False
        blob = f"{legal_full} {subnm}"
        p["is_hoa_common"] = bool(p.get("is_vacant") and HOA_RE.search(blob))

        # FLU join by representative point (city designation beats county by priority)
        flu_src, flu_desig, best_prio = "", "", 99
        if tree is not None:
            try:
                rep = shape(f["geometry"]).representative_point()
                for idx in tree.query(rep):
                    if fgeoms[idx].contains(rep):
                        lbl, desig, prio = fprops[idx]
                        if prio < best_prio and desig:
                            best_prio, flu_src, flu_desig = prio, lbl, desig
            except Exception:
                pass
        plain, intent = FLU_INTENT.get(flu_desig, (flu_desig or "(no FLU)", "" if flu_desig else "n/a"))
        p["flu_source"] = flu_src
        p["flu_designation"] = flu_desig
        p["flu_plain"] = plain
        p["flu_intent"] = intent
        if p.get("is_vacant"):
            flu_count[f"{flu_src}: {flu_desig}" if flu_desig else "(no FLU)"] += 1
        out.append({"type": "Feature", "geometry": f["geometry"], "properties": p})

    (IN / "parcels_enriched.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": out,
         "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}}))

    with open(TBL / "flu_summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["FLU (source: designation)", "Vacant parcels in area"])
        for k, n in flu_count.most_common():
            w.writerow([k, n])

    hoa = sum(1 for f in out if f["properties"].get("is_hoa_common"))
    oo = sum(1 for f in out if f["properties"].get("owner_occupied"))
    print(f"enriched {len(out)} parcels -> in/parcels_enriched.geojson")
    print(f"  vacant HOA/common flagged: {hoa} | owner-occupied: {oo}")
    print("  vacant-land FLU designations:", dict(flu_count.most_common(12)))


if __name__ == "__main__":
    main()
