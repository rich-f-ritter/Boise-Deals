#!/usr/bin/env python3
"""Build one 4:3 PNG per deal: satellite map + legend of VACANT parcels colored
by current zoning, with future-land-use rezone flags and coded built areas.

Spec (per user):
- Base: real satellite imagery (Esri World_Imagery, stitched tiles from
  scratchpad — run fetch_geoms_tiles.py first).
- Vacant developable parcels (>=1 ac): semi-transparent (~75%) fills grouped
  into 6 zoning classes; MF-capable classes loud, SF-only/industrial quiet.
- Bright dashed cyan outline = comp-plan FLU invites MF/attached (rezone-likely).
- Top ~10 MF-capable vacant parcels labeled "R-15 · 14 ac".
- Non-vacant: dissolved current-use areas outlined + faint wash (existing
  apartments / commercial / industrial+airport+Micron / built-out SF).
- Supply projects: tiny neutral numbered pins (numbers = Supply Chart rows).
- Gold 5-mi ring, subject star, slim title bar, legend column. 1600x1200 @2x.

Zoning fills validated (dataviz skill, all-pairs, light):
  MF by-right #d03b3b · mixed-use #9085e9 · townhome/duplex #eda100 ·
  commercial-conditional #e87ba4  (+ de-emphasis neutrals for SF-only / ind-ag).
"""
import json, math, re, sys

SP = "/tmp/claude-0/-home-user-Boise-Deals/eeeddfaf-76dc-502a-8545-5bd0f4be9c96/scratchpad"

DEALS = [
    dict(key="cr", deal="CanyonRidge", subject="Canyon Ridge",
         supply_map="CanyonRidge/supply/Canyon_Ridge__Map.html",
         out_html="cr_zoning.html",
         title="Canyon Ridge — Vacant Land by Zoning, 5-Mile Ring",
         landmarks=[("Boise Airport / Gowen Field", 43.5535, -116.2330),
                    ("Micron", 43.5215, -116.1350), ("I-84", 43.5920, -116.2280)]),
    dict(key="sam", deal="SeasonsMeridian", subject="Seasons at Meridian",
         supply_map="SeasonsMeridian/supply/Seasons_at_Meridian__Map.html",
         out_html="sam_zoning.html",
         title="Seasons at Meridian — Vacant Land by Zoning, 5-Mile Ring",
         landmarks=[("The Village at Meridian", 43.6335, -116.3230),
                    ("Downtown Meridian", 43.6115, -116.3970), ("I-84", 43.5965, -116.4310)]),
]

ZG = {   # zoning groups: key -> (label, fill, opacity, loud)
    "mf":  ("Multifamily by-right", "#d03b3b", 0.75, True),
    "mx":  ("Mixed-use (MF allowed)", "#9085e9", 0.75, True),
    "th":  ("Townhome / duplex", "#eda100", 0.75, True),
    "com": ("Commercial (MF conditional)", "#e87ba4", 0.72, True),
    "sf":  ("Single-family only", "#ded6b4", 0.55, False),
    "oth": ("Industrial / ag / other", "#b9bfb3", 0.5, False),
}
FLU_FLAG = "#35e0ff"     # dashed outline: FLU supports MF/attached (rezone-likely)
BUILT = {  # built-area coding: cat(s) -> (label, stroke, wash-opacity)
    "apartments": ("Existing apartments", "#4f9cf0", 0.13),
    "commercial": ("Commercial / retail", "#aab4c8", 0.07),
    "offlimits":  ("Industrial · airport · Micron", "#d6d2c6", 0.12),
    "established": ("Built-out single-family", "#cfc39a", 0.03),
}
OFF_CATS = {"industry", "airport", "airport_land", "micron"}
GOLD, INK, PAGE, SURF = "#D4A017", "#0b0b0b", "#f9f9f7", "#fcfcfb"
GRID, SEC, MUT = "#e1e0d9", "#52514e", "#898781"

def zgroup(row):
    cat, threat = row.get("zone_category") or "", row.get("mf_threat")
    if "Multifamily" in cat: return "mf"
    if "Mixed Use" in cat: return "mx"
    if "Townhouse" in cat or "Two-Family" in cat or "Med-Density" in cat: return "th"
    if "Commercial" in cat: return "com"
    if "Single-Family" in cat or "Single Family" in cat: return "sf"
    if "Planned" in cat or "Overlay" in cat:
        return {"High": "mf", "Medium": "mx"}.get(threat, "oth")
    return "oth"

def flu_flags_mf(row):
    return (row.get("flu_intent") or "") in ("supports multifamily", "supports attached/medium")

def merc(lat, lon, z):
    n = 256 * (2 ** z)
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y

def build(cfg):
    meta = json.load(open(f"{SP}/{cfg['key']}_sat.json"))
    z, tx0, ty0 = meta["z"], meta["tx0"], meta["ty0"]
    parcels = json.load(open(f"{cfg['deal']}/in/developable.json"))
    geoms = json.load(open(f"{cfg['deal']}/in/developable_geoms.json"))
    sections = [f for f in json.load(open("summary/sections.geojson"))["features"]
                if f["properties"]["subject"] == cfg["subject"]]
    s = open(cfg["supply_map"], encoding="utf-8").read()
    pins = json.loads(re.search(r"const PINS = (\[.*?\]);", s, re.S).group(1))
    subj = next(p for p in pins if p["bucket"] == "SUBJECT")
    lat0, lon0 = subj["lat"], subj["lng"]

    # map viewport: ring + 6% pad, square, in tile pixel space
    Rdeg = 5.0 / 69.0
    cx, cy = merc(lat0, lon0, z)
    _, ytop = merc(lat0 + Rdeg * 1.06, lon0, z)
    half = cy - ytop
    MAP = 1122                                     # css px, square
    scale = MAP / (2 * half)
    x0, y0 = cx - half, cy - half                  # viewport origin in world px
    def xy(lat, lon):
        X, Y = merc(lat, lon, z)
        return ((X - x0) * scale, (Y - y0) * scale)
    # satellite <img> placement
    img_x = (tx0 * 256 - x0) * scale
    img_y = (ty0 * 256 - y0) * scale
    img_w = meta["w"] * scale

    def path_of(geom):
        rings = geom["coordinates"] if geom["type"] == "Polygon" else \
                [r for poly in geom["coordinates"] for r in poly]
        d = []
        for ring in rings:
            pts = [xy(p[1], p[0]) for p in ring]
            d.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z")
        return " ".join(d)

    svg = [f'<svg viewBox="0 0 {MAP} {MAP}" width="{MAP}" height="{MAP}" '
           f'style="position:absolute;left:0;top:0" '
           f'font-family="system-ui,-apple-system,\'Segoe UI\',sans-serif">']
    svg.append(f'<defs><clipPath id="disc"><circle cx="{MAP/2}" cy="{MAP/2}" r="{Rdeg/ (2*half/ (256*2**z) * 69/69) if False else 0}"/></clipPath></defs>')

    # ---- built-area coding (outline + faint wash) ----
    def draw_sections(cats, stroke, wash_op, dash=""):
        for f in sections:
            if f["properties"]["cat"] not in cats:
                continue
            sw_ = 1.0 if f["properties"]["cat"] == "established" else 1.6
            so_ = 0.45 if f["properties"]["cat"] == "established" else 0.9
            svg.append(f'<path d="{path_of(f["geometry"])}" fill="{stroke}" '
                       f'fill-opacity="{wash_op}" fill-rule="evenodd" stroke="{stroke}" '
                       f'stroke-width="{sw_}" stroke-opacity="{so_}"{dash}/>')
    draw_sections({"established"}, BUILT["established"][1], BUILT["established"][2])
    draw_sections({"commercial"}, BUILT["commercial"][1], BUILT["commercial"][2])
    draw_sections(OFF_CATS, BUILT["offlimits"][1], BUILT["offlimits"][2])
    draw_sections({"apartments"}, BUILT["apartments"][1], BUILT["apartments"][2])

    # ---- vacant parcels: quiet classes first, loud on top ----
    zcodes = {k: set() for k in ZG}
    order = ["oth", "sf", "com", "th", "mx", "mf"]
    by_group = {k: [] for k in ZG}
    for r in parcels:
        g = zgroup(r)
        zcodes[g].add(r.get("zone_code") or "?")
        by_group[g].append(r)
    for g in order:
        lab, fill, op, loud = ZG[g]
        for r in by_group[g]:
            geom = geoms.get(r["account"])
            if not geom:
                continue
            svg.append(f'<path d="{path_of(geom)}" fill="{fill}" fill-opacity="{op}" '
                       f'fill-rule="evenodd" stroke="#ffffff" stroke-width="0.9" stroke-opacity="0.85"/>')
    # FLU rezone-likely dashed outlines (all groups)
    for r in parcels:
        if not flu_flags_mf(r):
            continue
        geom = geoms.get(r["account"])
        if geom:
            svg.append(f'<path d="{path_of(geom)}" fill="none" stroke="{FLU_FLAG}" '
                       f'stroke-width="2" stroke-dasharray="6 4"/>')

    # ---- 5-mi ring ----
    rpx = (merc(lat0, lon0, z)[1] - merc(lat0 + Rdeg, lon0, z)[1]) * scale
    svg.append(f'<circle cx="{MAP/2}" cy="{MAP/2}" r="{rpx:.0f}" fill="none" '
               f'stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8"/>')

    # ---- landmark labels ----
    for name, la, lo in cfg["landmarks"]:
        x, y = xy(la, lo)
        if 8 < x < MAP - 8 and 8 < y < MAP - 8:
            svg.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="14" font-weight="700" '
                       f'fill="#ffffff" text-anchor="middle" letter-spacing=".05em" '
                       f'stroke="#000000" stroke-width="3" stroke-opacity="0.55" paint-order="stroke" '
                       f'style="text-transform:uppercase">{name}</text>')

    # ---- top-10 MF-capable parcel labels ----
    cands = sorted((r for g in ("mf", "mx") for r in by_group[g]),
                   key=lambda r: -float(r["acres"]))[:10]
    lplaced = [xy(la, lo) for _, la, lo in cfg["landmarks"]]
    lplaced.append((xy(lat0, lon0)[0], xy(lat0, lon0)[1] - 25))   # subject name label
    for r in cands:
        x, y = xy(r["lat"], r["lon"])
        y -= 10                                    # sit above the parcel centroid
        for _ in range(24):                        # push apart colliding labels
            hit = next(((ox, oy) for ox, oy in lplaced
                        if abs(x - ox) < 96 and abs(y - oy) < 18), None)
            if not hit:
                break
            y += 17 if y >= hit[1] else -17
        lplaced.append((x, y))
        svg.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12.5" font-weight="700" '
                   f'fill="#ffffff" text-anchor="middle" stroke="#000000" stroke-width="3" '
                   f'stroke-opacity="0.6" paint-order="stroke">{r["zone_code"]} · {float(r["acres"]):.0f} ac</text>')

    # ---- tiny numbered neutral pins ----
    for p in pins:
        if p["bucket"] == "SUBJECT" or "shadow" in p["bucket"].lower():
            continue
        x, y = xy(p["lat"], p["lng"])
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8.5" fill="#ffffff" fill-opacity="0.92" '
                   f'stroke="{INK}" stroke-width="1.4"/>')
        if p.get("num") not in (None, "•"):
            svg.append(f'<text x="{x:.1f}" y="{y + 3.4:.1f}" font-size="10.5" font-weight="700" '
                       f'fill="{INK}" text-anchor="middle">{p["num"]}</text>')

    # ---- subject star ----
    sx, sy = xy(lat0, lon0)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 16 if i % 2 == 0 else 7
        star.append(f"{sx + rr*math.cos(ang):.1f},{sy + rr*math.sin(ang):.1f}")
    svg.append(f'<polygon points="{" ".join(star)}" fill="{INK}" stroke="#ffffff" stroke-width="2.6"/>')
    svg.append(f'<text x="{sx:.0f}" y="{sy - 25:.0f}" font-size="16" font-weight="800" fill="#ffffff" '
               f'text-anchor="middle" stroke="#000000" stroke-width="3.6" stroke-opacity="0.6" '
               f'paint-order="stroke">{cfg["subject"].upper()}</text>')
    svg.append("</svg>")

    # ---- legend ----
    def sw(fill, op, extra=""):
        return (f'<span class="sw" style="background:{fill};opacity:{max(op,0.55)}{extra}"></span>')
    tot_n = sum(len(v) for v in by_group.values())
    tot_ac = sum(float(r["acres"]) for v in by_group.values() for r in v)
    zrows = f'<div class="li"><div style="font-size:12px;color:{MUT}">{tot_n:,} vacant parcels · {tot_ac:,.0f} ac inside the ring</div></div>'
    for g in ("mf", "mx", "th", "com", "sf", "oth"):
        lab, fill, op, loud = ZG[g]
        n = len(by_group[g]); ac = sum(float(r["acres"]) for r in by_group[g])
        codes = ", ".join(sorted(zcodes[g])[:7]) or "—"
        zrows += (f'<div class="li{"" if loud else " quiet"}">{sw(fill, op)}'
                  f'<div><b>{lab}</b> <span class="m">{n} parcel{"s" if n != 1 else ""} · {ac:,.0f} ac</span>'
                  f'<div class="codes">{codes}</div></div></div>')
    built_rows = "".join(
        f'<div class="li"><span class="sw ol" style="border-color:{v[1]};background:{v[1]}22"></span>{v[0]}</div>'
        for v in BUILT.values())
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:1200px;background:{PAGE};overflow:hidden;
  font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:{INK}}}
.slide{{width:1600px;height:1200px;padding:20px 24px;display:flex;flex-direction:column}}
h1{{font-size:25px;font-weight:800;letter-spacing:-.01em}}
.asof{{font-size:12.5px;color:{MUT}}}
.row{{flex:1;display:flex;gap:20px;margin-top:12px;min-height:0}}
.map{{position:relative;width:{MAP}px;height:{MAP}px;flex:none;border-radius:8px;overflow:hidden;
  border:1px solid {GRID};background:#20241f}}
.map img{{position:absolute;left:{img_x:.1f}px;top:{img_y:.1f}px;width:{img_w:.1f}px}}
.leg{{flex:1;background:{SURF};border:1px solid {GRID};border-radius:8px;padding:16px 18px;
  display:flex;flex-direction:column;gap:6px;font-size:13px;overflow:hidden}}
.leg h3{{font-size:11.5px;font-weight:700;letter-spacing:.07em;color:{SEC};text-transform:uppercase;
  margin:6px 0 2px}}
.li{{display:flex;gap:9px;align-items:flex-start;line-height:1.25;margin:1.5px 0}}
.li.quiet{{color:{SEC}}}
.li .m{{color:{MUT};font-weight:400;font-size:12px}}
.codes{{color:{MUT};font-size:11px}}
.sw{{width:17px;height:17px;border-radius:3px;flex:none;border:1px solid rgba(0,0,0,.25);margin-top:1px}}
.sw.ol{{background:transparent;border-width:2px}}
.sw.dash{{background:transparent;border:2.5px dashed {FLU_FLAG}}}
.pin{{width:17px;height:17px;border-radius:50%;background:#fff;border:1.5px solid {INK};flex:none;
  font:700 10px/14px system-ui;text-align:center}}
.foot{{margin-top:auto;padding-top:8px;font-size:10.5px;color:{MUT};line-height:1.45}}
</style></head><body><div class="slide">
<div style="display:flex;justify-content:space-between;align-items:baseline">
  <h1>{cfg['title']}</h1>
  <div class="asof">Ada County parcels &amp; zoning · CoStar/RealPage + diligence July 2026</div>
</div>
<div class="row">
  <div class="map"><img src="{cfg['key']}_sat.jpg">{''.join(svg)}</div>
  <div class="leg">
    <h3>Vacant developable parcels — current zoning (fill)</h3>
    {zrows}
    <div class="li"><span class="sw dash"></span><div><b>Future land use invites MF / attached</b>
      <span class="m">comp-plan signal — rezone-likely</span></div></div>
    <h3>Built environment today (outline + wash)</h3>
    {built_rows}
    <h3>Reference</h3>
    <div class="li"><span class="pin">7</span>Supply-chart project (number = chart row)</div>
    <div class="li"><span class="sw" style="background:transparent;border:2.5px dashed {GOLD};border-radius:50%"></span>5-mile ring · ★ subject</div>
    <div class="foot">Vacant = Ada County assessor vacant-land parcels ≥1 ac after removing common/HOA,
    non-buildable and road-sliver lots. Zoning grouped from municipal districts (codes listed per class);
    labels mark the largest MF-capable parcels. Satellite: Esri World Imagery.
    Full parcel detail: land-use workbook; project detail: Supply Chart.</div>
  </div>
</div>
</div></body></html>"""
    out = f"{SP}/{cfg['out_html']}"
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, f"| {sum(len(v) for v in by_group.values())} parcels drawn")

if __name__ == "__main__":
    for cfg in DEALS:
        build(cfg)
