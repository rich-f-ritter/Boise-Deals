"""Build the combined 'development-opportunity summary' geometry for BOTH subjects.

Reframes raw parcels into REASONED categories that govern apartment supply, then DISSOLVES
contiguous like-kind parcels into larger labeled sections, each carrying aggregate detail
(acres, parcels, dominant zoning/FLU) and — where researched — owner / project / intent.

Inputs (per subject dir): in/parcels_enriched.geojson, in/developable.json, in/dossiers.json
Global overlays: summary/in/aia.geojson (Airport Influence Area zones), summary/in/micron_i3.geojson
Optional refinements (dropped in by agents): summary/in/micron_extra.geojson, summary/in/airport_property.geojson
Output: summary/sections.geojson  (dissolved sections w/ properties)  + summary/sections_summary.json
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.strtree import STRtree

BASE = Path("/home/user/Boise-Deals")
SUM = BASE / "summary"
SUBJECTS = {"CanyonRidge": "Canyon Ridge", "SeasonsMeridian": "Seasons at Meridian"}

# ── the synthesis taxonomy: category key -> (label, color, tier) ──────────────
#   tier 'feature' = curated opportunity/constraint sections (detailed, kept small)
#   tier 'context' = background fabric (muted, coarsely dissolved)
# colors here mirror build_summary_map.py (the renderer is authoritative; kept in sync)
CATS = {
    "apartments":  ("Competing apartments — built / approved / proposed", "#E12726", "opportunity"),
    "apt_ready":   ("Apartment-ready land — available (no active plan)",   "#FB8C1A", "opportunity"),
    "mpc_res":     ("Active master-planned residential (mostly for-sale)", "#D65DB1", "opportunity"),
    "landbank":    ("Land-bank / future growth (long-term potential)",      "#AFA77E", "longterm"),
    "micron":      ("Micron — semiconductor campus & expansion",            "#7E3F98", "offlimits"),
    "airport_land":("Boise Airport / Gowen Field (aviation)",                "#26406B", "offlimits"),
    "airport":     ("Airport Influence Area — apartment-restricted",         "#5E86C4", "offlimits"),
    "industry":    ("Industrial / employment (non-Micron)",                 "#565B63", "offlimits"),
    "rural":       ("Rural / foothills / protected — not developable",       "#A6A588", "context"),
    "civic":       ("Parks / open space / civic / institutional",          "#A9C6B0", "context"),
    "commercial":  ("Commercial / retail",                                  "#B7BCC2", "context"),
    "established": ("Established neighborhoods (built-out)",                 "#DAD6CE", "context"),
}

# ── reasoned category for each researched dossier site (site_id -> cat) ───────
# Derived from the 30 dossiers: Micron/airport/rural handled mostly by geometry+rules,
# but tagging pins each researched SITE to the right synthesis bucket + carries its detail.
DOSSIER_CAT = {
    # Canyon Ridge
    "CR-1": "airport_land", "CR-4": "airport",
    "CR-6": "industry", "CR-13": "industry", "CR-7": "industry",
    "CR-2": "landbank", "CR-5": "landbank", "CR-14": "rural",
    "CR-16": "civic", "CR-66": "civic", "CR-106": "civic",
    "CR-51": "apartments", "CR-57": "apt_ready",
    "CR-3": None,  # split by geometry: I-3 -> Micron, remainder -> land-bank (rules)
    # Seasons at Meridian
    "SM-4": "apartments", "SM-1": "apartments", "SM-40": "apartments", "SM-76": "apartments",
    "SM-3": "apartments", "SM-15": "apartments", "SM-155": "apartments",
    "SM-31": "mpc_res", "SM-61": "mpc_res",
    "SM-20": "commercial", "SM-9": "civic", "SM-6": "industry",
    "SM-2": "landbank", "SM-12": "landbank", "SM-18": "landbank", "SM-5": "landbank",
}

RURAL_ZONES = {"RUT", "RR", "RP", "A-1", "A-2", "A", "A-R", "R-E"}


def valid(g):
    return g if g.is_valid else g.buffer(0)


def load_overlays():
    aia = json.loads((SUM / "in" / "aia.geojson").read_text())["features"]
    # Boise AI-O overlay: new residential PROHIBITED only in Zones B and C
    # (Zone A = outer, insulation only; B-1 = limited residential w/ density cap).
    restrict = unary_union([valid(shape(f["geometry"])) for f in aia
                            if f["properties"].get("ZONE") in ("B", "C")])
    micron_parts = [valid(shape(f["geometry"]))
                    for f in json.loads((SUM / "in" / "micron_i3.geojson").read_text())["features"]]
    for extra in ("micron_extra.geojson", "airport_property.geojson"):
        p = SUM / "in" / extra
        if p.exists() and extra.startswith("micron"):
            micron_parts += [valid(shape(f["geometry"]))
                             for f in json.loads(p.read_text())["features"]]
    micron = unary_union(micron_parts) if micron_parts else None
    airport_prop = None
    ap = SUM / "in" / "airport_property.geojson"
    if ap.exists():
        airport_prop = unary_union([valid(shape(f["geometry"]))
                                    for f in json.loads(ap.read_text())["features"]])
    return restrict, micron, airport_prop


PROTECT_FLU = ("Parks/Open Space", "Slope Protection", "School", "Civic", "Public/Quasi-Public")


def classify(p, in_micron, in_aia, in_airport, tagged_cat):
    """Reasoned category for one parcel (priority order).

    Order matters: Micron and the airfield itself are absolute; then RESEARCHED sites keep
    their identity (so real approved/built apartments inside the AIA aren't erased); then the
    AIA catch-all repaints only UNTAGGED land (generic MF-zoned vacant in an AIA ban zone is
    moot); then opportunity/constraint/context rules.
    """
    bucket = p.get("bucket") or ""
    zc = p.get("zone_code") or ""
    cat = p.get("zone_category") or ""
    intent = p.get("flu_intent") or ""
    flu = p.get("flu_designation") or ""
    vac = p.get("is_vacant")
    ac = p.get("acres") or 0
    established_home = (bucket == "Single Family Residential" and not vac)
    if in_micron:
        return "micron"
    if in_airport:
        return "airport_land"
    if tagged_cat:                       # researched sites win over the AIA catch-all
        return tagged_cat
    if in_aia and not established_home:   # generic land in AIA zone B/C: new housing barred
        return "airport"
    if p.get("is_hoa_common") or "institutional" in intent or "not developable" in intent \
            or bucket == "Public / Airport / Institutional" or flu in PROTECT_FLU:
        return "civic"
    if p.get("_developable") and ("multifamily" in intent or str(p.get("mf_threat", "")).startswith("High")):
        return "apt_ready"
    if bucket == "Industrial / Service / Auto" or cat == "Industrial / Business Park":
        return "industry"
    # large vacant urban-edge growth land planned for development => future supply (land-bank)
    if vac and ac >= 10 and zc not in ("RP",) and "slope" not in intent \
            and ("multifamily" in intent or "attached" in intent or "single-family" in intent
                 or "master-plan" in intent or "development-ready" in intent
                 or flu in ("Planned Community",) or zc in ("RUT", "PC")):
        return "landbank"
    # genuinely rural / protected foothills (RP, ag, slope) — not near-term developable
    if bucket == "Agricultural / Rural" or zc in RURAL_ZONES or "rural" in intent \
            or "slope" in intent or (vac and ac >= 20):
        return "rural"
    if bucket == "Commercial" or cat in ("Commercial", "Office"):
        return "commercial"
    return "established"


def main():
    restrict, micron, airport_prop = load_overlays()
    ov_geoms = [restrict] + ([micron] if micron else []) + ([airport_prop] if airport_prop else [])
    ov_tree = STRtree(ov_geoms)

    all_sections = []
    per_subject = {}
    for key, disp in SUBJECTS.items():
        d = BASE / key
        feats = json.loads((d / "in" / "parcels_enriched.geojson").read_text())["features"]
        dev = json.loads((d / "in" / "developable.json").read_text())
        dev_by_acct = {r["account"]: r for r in dev}
        # map contig_group -> its dossier site_id (via sites.json numbering == gid)
        doss = {x["gid"]: x for x in json.loads((d / "in" / "dossiers.json").read_text())}
        # accounts belonging to each dossier's contiguous group
        grp_accts = defaultdict(set)
        for r in dev:
            grp_accts[r["contig_group"]].add(r["account"])
        acct_site = {}      # account -> site_id (for tagged parcels)
        acct_doss = {}      # account -> dossier dict
        for gid, dd in doss.items():
            for a in grp_accts.get(gid, ()):
                acct_site[a] = dd["site_id"]
                acct_doss[a] = dd

        pfx = "CR" if key == "CanyonRidge" else "SM"
        rows = []
        for f in feats:
            p = dict(f["properties"])
            acct = p.get("account")
            p["_developable"] = acct in dev_by_acct
            try:
                g = valid(shape(f["geometry"]))
            except Exception:
                continue
            rep = g.representative_point()
            in_micron = bool(micron) and any(micron is ov_geoms[i] and ov_geoms[i].contains(rep)
                                             for i in ov_tree.query(rep))
            in_air = bool(airport_prop) and any(airport_prop is ov_geoms[i] and ov_geoms[i].contains(rep)
                                                for i in ov_tree.query(rep))
            in_aia = any(restrict is ov_geoms[i] and ov_geoms[i].contains(rep) for i in ov_tree.query(rep))
            site = acct_site.get(acct)
            tagged = DOSSIER_CAT.get(site) if site else None
            cat = classify(p, in_micron, in_aia, in_air, tagged)
            rows.append((g, p, cat, site if tagged else None))

        # dissolve by (category, group_key): tagged sites keep their identity; else by contiguity
        site_doss = {dd["site_id"]: dd for dd in doss.values()}
        groups = defaultdict(list)
        for i, (g, p, cat, site) in enumerate(rows):
            gk = site if site else f"={cat}"           # "=cat" marks an untagged contiguity group
            groups[(cat, gk)].append(i)

        counts = Counter()
        subj_sections = []
        for (cat, gk), members in groups.items():
            tier = CATS[cat][2]
            if tier == "context":
                # inflate so neighborhood parcels merge across road gaps into clean fabric
                gg = [rows[i][0].simplify(0.0004, preserve_topology=True).buffer(0.00016) for i in members]
                merged = unary_union(gg).buffer(-0.00018)  # net shrink: never overlap feature sections
            else:
                gg = [rows[i][0].simplify(0.00012, preserve_topology=True).buffer(0.00003) for i in members]
                merged = unary_union(gg).buffer(-0.00004)  # net -1m: adjacent sections don't overlap
            polys = list(merged.geoms) if merged.geom_type.startswith("Multi") else [merged]
            # feature floor 0.75: sections are unions of >=1-ac developable parcels, so any
            # smaller fragment is a shrink/road-split artifact of a legit site — keep it.
            minac = 0.75 if tier == "feature" else 8.0
            mp = [rows[i][1] for i in members]         # group-level parcel props (dominant stats)
            gz = Counter(x.get("zone_plain") for x in mp if x.get("zone_plain")).most_common(3)
            gf = Counter(x.get("flu_plain") for x in mp if x.get("flu_plain")).most_common(2)
            site = None if gk.startswith("=") else gk
            dd = site_doss.get(site) if site else None
            for poly in polys:
                if poly.is_empty:
                    continue
                ac = poly.area * (111320 ** 2) * math.cos(math.radians(43.55)) / 4046.8564224
                if ac < minac:
                    continue
                sect = {
                    "subject": disp, "cat": cat, "cat_label": CATS[cat][0], "color": CATS[cat][1],
                    "tier": tier, "acres": round(ac, 1), "parcels": 0,
                    "zoning": ", ".join(f"{z} ({n})" for z, n in gz),
                    "flu": ", ".join(z for z, n in gf), "site_id": site,
                }
                if dd:
                    sect.update({
                        "title": dd.get("site_id") + " · " + (dd.get("address") or ""),
                        "owner": dd.get("owner_name"), "owner_type": dd.get("owner_type"),
                        "since": dd.get("ownership_since"), "who": dd.get("who_they_are"),
                        "intent": dd.get("intent_summary"), "status": dd.get("project_status"),
                        "sources": dd.get("sources", [])[:4],
                    })
                subj_sections.append((poly, sect))
                counts[cat] += 1

        # one STRtree pass to count parcels per section (cheap vs per-section scan)
        sgeoms = [ps[0] for ps in subj_sections]
        stree = STRtree(sgeoms) if sgeoms else None
        if stree is not None:
            for g, p, cat, site in rows:
                rp = g.representative_point()
                for idx in stree.query(rp):
                    if sgeoms[idx].contains(rp):
                        subj_sections[idx][1]["parcels"] += 1
                        break
        for poly, sect in subj_sections:
            all_sections.append({"type": "Feature",
                                 "geometry": mapping(poly.simplify(0.00008, preserve_topology=True)),
                                 "properties": sect})
        per_subject[disp] = counts
        print(f"{disp}: {sum(counts.values())} sections  {dict(counts)}", file=sys.stderr)

    fc = {"type": "FeatureCollection", "features": all_sections}
    (SUM / "sections.geojson").write_text(json.dumps(fc))
    # summary rollup by category (acres per subject)
    roll = defaultdict(lambda: defaultdict(float))
    for s in all_sections:
        roll[s["properties"]["cat"]][s["properties"]["subject"]] += s["properties"]["acres"]
    summ = {cat: {"label": CATS[cat][0], "color": CATS[cat][1],
                  "by_subject": {k: round(v, 0) for k, v in roll[cat].items()}} for cat in CATS}
    (SUM / "sections_summary.json").write_text(json.dumps(summ, indent=2))
    print(f"\nTOTAL sections: {len(all_sections)} -> summary/sections.geojson")
    for cat in CATS:
        print(f"  {cat:12} {CATS[cat][0][:44]:44} {dict(roll[cat])}")


if __name__ == "__main__":
    main()
