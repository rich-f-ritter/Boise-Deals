"""Merge all research/raw/*.json site dossiers, attach each site's authoritative zoning / FLU /
distance / coords from <subject>/in/sites.json, and write per-subject in/dossiers.json (for the
workbook) + comparison/dossiers_all.json (for the comparison report)."""
import glob
import json
from pathlib import Path

BASE = Path("/home/user/Boise-Deals")
SUBJ = {"CR": "CanyonRidge", "SM": "SeasonsMeridian"}


def main():
    sites = {}
    for pref, d in SUBJ.items():
        s = json.load(open(BASE / d / "in" / "sites.json"))
        sites[pref] = {x["gid"]: x for x in s}

    dossiers = []
    for fp in sorted(glob.glob(str(BASE / "research" / "raw" / "*.json"))):
        try:
            arr = json.load(open(fp))
        except Exception as e:
            print(f"  [warn] {fp}: {e}")
            continue
        for d in arr:
            sid = d.get("site_id", "")
            pref = sid.split("-")[0]
            try:
                gid = int(sid.split("-")[1])
            except Exception:
                gid = None
            site = sites.get(pref, {}).get(gid, {})
            zones = site.get("zones", [])
            flus = site.get("flus", [])
            d["subject"] = SUBJ.get(pref, pref)
            d["gid"] = gid
            d["dist_mi"] = round(site.get("min_dist", 0), 2) if site else None
            d["lat"] = site.get("lat")
            d["lon"] = site.get("lon")
            d["parcels_n"] = site.get("parcels")
            d["zoning"] = ", ".join(zones)
            d["future_land_use"] = "; ".join(flus)
            d["zoning_flu"] = (("Zoning: " + ", ".join(zones)) if zones else "") + \
                              (("  |  FLU: " + "; ".join(flus)) if flus else "")
            if not d.get("acres") and site.get("acres"):
                d["acres"] = site["acres"]
            dossiers.append(d)

    # per-subject dossier files (sorted by distance to subject)
    for pref, d in SUBJ.items():
        sub = [x for x in dossiers if x["subject"] == d]
        sub.sort(key=lambda x: (x.get("dist_mi") if x.get("dist_mi") is not None else 9e9))
        (BASE / d / "in" / "dossiers.json").write_text(json.dumps(sub, indent=2))
        print(f"{d}: {len(sub)} dossiers")

    (BASE / "comparison" / "dossiers_all.json").write_text(json.dumps(dossiers, indent=2))
    print(f"total dossiers: {len(dossiers)} -> comparison/dossiers_all.json")


if __name__ == "__main__":
    main()
