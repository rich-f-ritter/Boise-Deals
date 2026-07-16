#!/usr/bin/env python3
"""Build one 4:3 PNG per deal: satellite map + legend of VACANT parcels colored
by current zoning, with future-land-use rezone flags and coded built/area classes.

Spec (per user, v2):
- Satellite base (Esri World_Imagery tiles; run fetch_geoms_tiles.py first).
- Vacant developable parcels colored by zoning (6 groups, MF loudest, ~75% fill);
  cyan dashed outline = FLU invites MF/attached (rezone-likely).
- Built single-family = UNCODED (pure satellite — you can see it's houses).
- Every other area class coded distinctly: existing apartments (blue),
  commercial (slate), industrial (umber), AIRPORT OPS (steel hatch),
  MICRON (purple) — bifurcated, not lumped — plus ag/rural-preservation and
  land-bank ground (the 'vacant-looking' land that isn't assessor-vacant),
  and the Airport Influence Area as a dashed restriction BOUNDARY (an overlay,
  not a land use).
- Supply pins: only deals >=100 units, numbered = Supply Chart rows, colored
  with the Supply Chart's own lifecycle bucket colors (from the map PINS).
- Top ~10 MF-capable parcel labels, gold 5-mi ring, subject star, slim title.

Vacant palette validated (dataviz skill, all-pairs): #d03b3b / #9085e9 /
#eda100 / #e87ba4 + de-emphasis neutrals (straw / concrete).
"""
import json, math, re

SP = "/tmp/claude-0/-home-user-Boise-Deals/eeeddfaf-76dc-502a-8545-5bd0f4be9c96/scratchpad"

DEALS = [
    dict(key="cr", deal="CanyonRidge", subject="Canyon Ridge",
         supply_map="CanyonRidge/supply/Canyon_Ridge__Map.html",
         out_html="cr_zoning.html",
         title="Canyon Ridge — Vacant Land by Zoning, 5-Mile Ring",
         rural_label="Rural preservation / foothills — comp-plan blocked",
         landmarks=[("Boise Airport / Gowen Field", 43.5535, -116.2330),
                    ("Micron", 43.5215, -116.1350), ("I-84", 43.5920, -116.2280)]),
    dict(key="sam", deal="SeasonsMeridian", subject="Seasons at Meridian",
         supply_map="SeasonsMeridian/supply/Seasons_at_Meridian__Map.html",
         out_html="sam_zoning.html",
         title="Seasons at Meridian — Vacant Land by Zoning, 5-Mile Ring",
         rural_label="Unincorporated county ag — annexation required",
         landmarks=[("The Village at Meridian", 43.6335, -116.3230),
                    ("Downtown Meridian", 43.6115, -116.3970), ("I-84", 43.5965, -116.4310)]),
]

ZG = {   # vacant zoning groups: key -> (label, fill, opacity, loud)
    "mf":  ("Multifamily by-right", "#d03b3b", 0.78, True),
    "mx":  ("Mixed-use (MF allowed)", "#9085e9", 0.78, True),
    "th":  ("Townhome / duplex", "#eda100", 0.78, True),
    "com": ("Commercial (MF conditional)", "#e87ba4", 0.75, True),
    "sf":  ("Single-family only", "#e3d9a8", 0.60, False),
    "ind": ("Industrial vacant", "#b99d78", 0.55, False),
    "ag":  ("Vacant, zoned ag/rural (rezone candidate)", "#a8b28c", 0.50, False),
    "oth": ("Other / overlay", "#a9b0ba", 0.55, False),
}
FLU_FLAG = "#35e0ff"

# area classes over satellite — each visually distinct family
AREA = {   # cat(s) -> (label, color, wash, stroke_w, style)
    "apartments": ("Existing apartments", "#2f7fe0", 0.16, 1.8, "solid"),
    "commercial": ("Commercial / retail", "#64748b", 0.10, 1.4, "solid"),
    "industry":   ("Industrial / employment", "#8a5a2b", 0.13, 1.6, "solid"),
    "airport_land": ("Airport ops (Gowen Field)", "#46586b", None, 1.6, "hatch"),
    "micron":     ("Micron — campus & expansion", "#7E3F98", 0.15, 2.0, "solid"),
    "rural":      ("Ag / rural preservation — not developable", "#7c8a5f", 0.10, 0.7, "solid"),
    "landbank":   ("Land-bank / future growth (long-term)", "#b0a36e", 0.13, 1.2, "dotted"),
}
AIA = ("Airport Influence Area — apartments restricted", "#33424f")   # dashed boundary only
GOLD, INK, PAGE, SURF = "#D4A017", "#0b0b0b", "#f9f9f7", "#fcfcfb"
GRID, SEC, MUT = "#e1e0d9", "#52514e", "#898781"

def zgroup(row):
    cat, threat = row.get("zone_category") or "", row.get("mf_threat")
    if "Multifamily" in cat: return "mf"
    if "Mixed Use" in cat: return "mx"
    if "Townhouse" in cat or "Two-Family" in cat or "Med-Density" in cat: return "th"
    if "Commercial" in cat: return "com"
    if "Single-Family" in cat or "Single Family" in cat: return "sf"
    if "Industrial" in cat: return "ind"
    if "Agricultural" in cat or "Rural" in cat: return "ag"
    if "Planned" in cat or "Overlay" in cat:
        return {"High": "mf", "Medium": "mx"}.get(threat, "oth")
    return "oth"

def flu_flags_mf(row):
    return (row.get("flu_intent") or "") in ("supports multifamily", "supports attached/medium")

def merc(lat, lon, z):
    n = 256 * (2 ** z)
    return ((lon + 180) / 360 * n,
            (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)

def build(cfg):
    meta = json.load(open(f"{SP}/{cfg['key']}_sat.json"))
    z, tx0, ty0 = meta["z"], meta["tx0"], meta["ty0"]
    parcels = json.load(open(f"{cfg['deal']}/in/developable.json"))
    geoms = json.load(open(f"{cfg['deal']}/in/developable_geoms.json"))
    occ = json.load(open(f"{cfg['deal']}/in/farm_ranchette_parcels.json"))
    sections = [f for f in json.load(open("summary/sections.geojson"))["features"]
                if f["properties"]["subject"] == cfg["subject"]]
    s = open(cfg["supply_map"], encoding="utf-8").read()
    pins = json.loads(re.search(r"const PINS = (\[.*?\]);", s, re.S).group(1))
    leg_chart = json.loads(re.search(r"const LEG = (\[.*?\]);", s, re.S).group(1))
    subj = next(p for p in pins if p["bucket"] == "SUBJECT")
    lat0, lon0 = subj["lat"], subj["lng"]

    Rdeg = 5.0 / 69.0
    cx, cy = merc(lat0, lon0, z)
    _, ytop = merc(lat0 + Rdeg * 1.06, lon0, z)
    half = cy - ytop
    MAP = 1122
    scale = MAP / (2 * half)
    x0, y0 = cx - half, cy - half
    def xy(lat, lon):
        X, Y = merc(lat, lon, z)
        return ((X - x0) * scale, (Y - y0) * scale)
    img_x, img_y = (tx0 * 256 - x0) * scale, (ty0 * 256 - y0) * scale
    img_w = meta["w"] * scale

    def path_of(geom):
        rings = geom["coordinates"] if geom["type"] == "Polygon" else \
                [r for poly in geom["coordinates"] for r in poly]
        return " ".join("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in
                        (xy(p[1], p[0]) for p in ring)) + " Z" for ring in rings)

    layers = {}          # layer_id -> [svg elements]
    layer_order = []
    def L(lid):
        if lid not in layers:
            layers[lid] = []
            layer_order.append(lid)
        return layers[lid]
    svg_head = (f'<svg viewBox="0 0 {MAP} {MAP}" width="{MAP}" height="{MAP}" '
                f'style="position:absolute;left:0;top:0" '
                f'font-family="system-ui,-apple-system,\'Segoe UI\',sans-serif">')
    svg = []
    svg_defs = ('<defs><pattern id="aphatch" patternUnits="userSpaceOnUse" width="9" height="9" '
               'patternTransform="rotate(45)">'
               f'<line x1="0" y1="0" x2="0" y2="9" stroke="{AREA["airport_land"][1]}" '
               'stroke-width="2.2" stroke-opacity="0.55"/></pattern>'
               '<pattern id="farmhatch" patternUnits="userSpaceOnUse" width="10" height="10" '
               'patternTransform="rotate(45)">'
               '<rect width="10" height="10" fill="#71875a" fill-opacity="0.42"/>'
               '<line x1="0" y1="0" x2="0" y2="10" stroke="#43552c" stroke-width="1.6" '
               'stroke-opacity="0.65"/></pattern></defs>')

    # ---- area classes (each into its own toggleable layer) ----
    def draw(cats, color, wash, sw, style, lid):
        dash = ' stroke-dasharray="2 4"' if style == "dotted" else ""
        fill = "url(#aphatch)" if style == "hatch" else color
        fo = 1 if style == "hatch" else (wash or 0)
        for f in sections:
            if f["properties"]["cat"] not in (cats if isinstance(cats, set) else {cats}):
                continue
            L(lid).append(f'<path d="{path_of(f["geometry"])}" fill="{fill}" fill-opacity="{fo}" '
                          f'fill-rule="evenodd" stroke="{color}" stroke-width="{sw}" '
                          f'stroke-opacity="0.85"{dash}/>')
    draw("rural", *AREA["rural"][1:], "lyr-rural")
    draw("landbank", *AREA["landbank"][1:], "lyr-landbank")
    draw("commercial", *AREA["commercial"][1:], "lyr-commercial")
    draw("industry", *AREA["industry"][1:], "lyr-industry")
    draw("apartments", *AREA["apartments"][1:], "lyr-apartments")

    # ---- occupied-but-open land ----
    for pr in occ["ranchette"]:
        L("lyr-ranchette").append(f'<path d="{path_of(pr["geometry"])}" fill="#cbbd8f" fill-opacity="0.48" '
                   f'fill-rule="evenodd" stroke="#8f8050" stroke-width="1.0" stroke-opacity="0.85"/>')
    for pr in occ["farm"]:
        L("lyr-farm").append(f'<path d="{path_of(pr["geometry"])}" fill="url(#farmhatch)" '
                   f'fill-rule="evenodd" stroke="#43552c" stroke-width="1.3" stroke-opacity="0.85"/>')

    # ---- vacant parcels ----
    zcodes = {k: set() for k in ZG}
    by_group = {k: [] for k in ZG}
    for r in parcels:
        g = zgroup(r)
        zcodes[g].add(r.get("zone_code") or "?")
        by_group[g].append(r)
    for g in ["ag", "ind", "oth", "sf", "com", "th", "mx", "mf"]:
        _, fill, op, _ = ZG[g]
        for r in by_group[g]:
            geom = geoms.get(r["account"])
            if geom:
                L(f"lyr-vac-{g}").append(f'<path d="{path_of(geom)}" fill="{fill}" fill-opacity="{op}" '
                           f'fill-rule="evenodd" stroke="#ffffff" stroke-width="0.9" stroke-opacity="0.85"/>')
    for r in parcels:
        if flu_flags_mf(r):
            geom = geoms.get(r["account"])
            if geom:
                L("lyr-flu").append(f'<path d="{path_of(geom)}" fill="none" stroke="{FLU_FLAG}" '
                           f'stroke-width="2" stroke-dasharray="6 4"/>')
    # restriction overlays ABOVE the parcel fills (so Micron/airport/AIA stay visible)
    draw("airport_land", *AREA["airport_land"][1:], "lyr-airport")
    draw("micron", *AREA["micron"][1:], "lyr-micron")
    for f in sections:
        if f["properties"]["cat"] == "airport":
            d_ = path_of(f["geometry"])
            L("lyr-aia").append(f'<path d="{d_}" fill="none" stroke="#0b0b0b" stroke-width="4.2" '
                       f'stroke-dasharray="12 6" stroke-opacity="0.5"/>')
            L("lyr-aia").append(f'<path d="{d_}" fill="none" stroke="#dce8f8" stroke-width="2" '
                       f'stroke-dasharray="12 6" stroke-opacity="0.95"/>')

    # ---- ring ----
    rpx = (merc(lat0, lon0, z)[1] - merc(lat0 + Rdeg, lon0, z)[1]) * scale
    L("lyr-ref").append(f'<circle cx="{MAP/2}" cy="{MAP/2}" r="{rpx:.0f}" fill="none" '
               f'stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8"/>')

    # ---- landmarks ----
    lplaced = []
    for name, la, lo in cfg["landmarks"]:
        x, y = xy(la, lo)
        if 8 < x < MAP - 8 and 8 < y < MAP - 8:
            lplaced.append((x, y))
            L("lyr-ref").append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="14" font-weight="700" '
                       f'fill="#ffffff" text-anchor="middle" letter-spacing=".05em" '
                       f'stroke="#000000" stroke-width="3" stroke-opacity="0.55" paint-order="stroke" '
                       f'style="text-transform:uppercase">{name}</text>')

    # ---- top-10 MF-capable parcel labels ----
    lplaced.append((xy(lat0, lon0)[0], xy(lat0, lon0)[1] - 25))
    for r in sorted((r for g in ("mf", "mx") for r in by_group[g]),
                    key=lambda r: -float(r["acres"]))[:10]:
        x, y = xy(r["lat"], r["lon"])
        y -= 10
        for _ in range(24):
            hit = next(((ox, oy) for ox, oy in lplaced if abs(x - ox) < 96 and abs(y - oy) < 18), None)
            if not hit:
                break
            y += 17 if y >= hit[1] else -17
        lplaced.append((x, y))
        L("lyr-labels").append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12.5" font-weight="700" '
                   f'fill="#ffffff" text-anchor="middle" stroke="#000000" stroke-width="3" '
                   f'stroke-opacity="0.6" paint-order="stroke">{r["zone_code"]} · {float(r["acres"]):.0f} ac</text>')

    # ---- supply pins: >=100u only, chart bucket colors, numbered ----
    for p in pins:
        if p["bucket"] == "SUBJECT" or "shadow" in p["bucket"].lower():
            continue
        if (p.get("units") or 0) < 100:
            continue
        x, y = xy(p["lat"], p["lng"])
        L("lyr-pins").append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10.5" fill="{p["color"]}" '
                   f'stroke="#ffffff" stroke-width="2.2"/>')
        if p.get("num") not in (None, "•"):
            L("lyr-pins").append(f'<text x="{x:.1f}" y="{y + 3.8:.1f}" font-size="11.5" font-weight="700" '
                       f'fill="#ffffff" text-anchor="middle">{p["num"]}</text>')

    # ---- subject ----
    sx, sy = xy(lat0, lon0)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 16 if i % 2 == 0 else 7
        star.append(f"{sx + rr*math.cos(ang):.1f},{sy + rr*math.sin(ang):.1f}")
    L("lyr-ref").append(f'<polygon points="{" ".join(star)}" fill="{INK}" stroke="#ffffff" stroke-width="2.6"/>')
    L("lyr-ref").append(f'<text x="{sx:.0f}" y="{sy - 25:.0f}" font-size="16" font-weight="800" fill="#ffffff" '
               f'text-anchor="middle" stroke="#000000" stroke-width="3.6" stroke-opacity="0.6" '
               f'paint-order="stroke">{cfg["subject"].upper()}</text>')
    # assemble: layers in creation order, labels/pins/ref last
    tail = [l for l in ("lyr-flu", "lyr-airport", "lyr-micron", "lyr-aia",
                        "lyr-labels", "lyr-pins", "lyr-ref") if l in layers]
    body = [l for l in layer_order if l not in tail] + tail
    svg = [svg_head, svg_defs] + \
          [f'<g id="{lid}">' + "".join(layers[lid]) + "</g>" for lid in body] + ["</svg>"]

    # ---- legend ----
    tot_n = sum(len(v) for v in by_group.values())
    tot_ac = sum(float(r["acres"]) for v in by_group.values() for r in v)
    zrows = (f'<div class="li"><div style="font-size:12px;color:{MUT}">{tot_n:,} vacant parcels · '
             f'{tot_ac:,.0f} ac inside the ring</div></div>')
    for g in ("mf", "mx", "th", "com", "sf", "ind", "ag", "oth"):
        lab, fill, op, loud = ZG[g]
        n = len(by_group[g]); ac = sum(float(r["acres"]) for r in by_group[g])
        codes = ", ".join(sorted(zcodes[g])[:7]) or "—"
        zrows += (f'<div class="li{"" if loud else " quiet"}" data-lyr="lyr-vac-{g}"><span class="sw" '
                  f'style="background:{fill};opacity:{max(op,0.6)}"></span>'
                  f'<div><b>{lab}</b> <span class="m">{n} parcel{"s" if n != 1 else ""} · {ac:,.0f} ac</span>'
                  f'<div class="codes">{codes}</div></div></div>')
    # area rows — only classes present in this ring
    present = {f["properties"]["cat"] for f in sections}
    arows = ""
    LYR_OF = {"apartments": "lyr-apartments", "commercial": "lyr-commercial",
              "industry": "lyr-industry", "airport_land": "lyr-airport",
              "micron": "lyr-micron", "rural": "lyr-rural", "landbank": "lyr-landbank"}
    for cat, (lab, color, wash, sw, style) in AREA.items():
        if cat == "rural":
            lab = cfg.get("rural_label", lab)
        if cat not in present:
            continue
        if style == "hatch":
            swd = f'<span class="sw" style="background:repeating-linear-gradient(45deg,transparent 0 3px,{color} 3px 5px)"></span>'
        elif style == "dotted":
            swd = f'<span class="sw" style="background:{color}33;border:2px dotted {color}"></span>'
        else:
            swd = f'<span class="sw" style="background:{color}33;border:2px solid {color}"></span>'
        arows += f'<div class="li" data-lyr="{LYR_OF[cat]}">{swd}{lab}</div>'
    if "airport" in present:
        arows += (f'<div class="li" data-lyr="lyr-aia"><span class="sw" style="background:#5b6b7d;'
                  f'border:2.5px dashed #dce8f8"></span>{AIA[0]}</div>')
    f_n, f_ac = len(occ["farm"]), sum(p["acres"] for p in occ["farm"])
    r_n, r_ac = len(occ["ranchette"]), sum(p["acres"] for p in occ["ranchette"])
    arows += (f'<div class="li" data-lyr="lyr-farm"><span class="sw" style="background:repeating-linear-gradient(45deg,'
              f'#7f925e55 0 4px,#5d7040aa 4px 5.5px)"></span><div><b>Working farms — ag-exempt</b> '
              f'<span class="m">{f_n} parcels · {f_ac:,.0f} ac</span><div class="codes">occupied ag '
              f'(assessor PROPCODE F) — sell-and-develop candidates; NOT assessor-vacant</div></div></div>')
    arows += (f'<div class="li" data-lyr="lyr-ranchette"><span class="sw" style="background:#cbbd8f59;border:1.5px solid #a89a68">'
              f'</span><div><b>Large-lot homesteads (5+ ac)</b> <span class="m">{r_n} parcels · '
              f'{r_ac:,.0f} ac</span><div class="codes">one home on acreage — same sell-and-develop path'
              f'</div></div></div>')
    arows += (f'<div class="li quiet"><span class="sw" style="background:transparent;'
              f'border:1px solid {GRID}"></span>Uncoded = built-out single-family; bare dirt with '
              f'street grids = platted SF subdivisions building out</div>')
    # pin status mini-legend from the chart's own colors
    prow = "".join(f'<span class="pli"><span class="pdot" style="background:{l["color"]}"></span>{l["label"]}</span>'
                   for l in leg_chart)
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
.leg{{flex:1;background:{SURF};border:1px solid {GRID};border-radius:8px;padding:15px 17px;
  display:flex;flex-direction:column;gap:5px;font-size:12.5px;overflow:hidden}}
.leg h3{{font-size:11px;font-weight:700;letter-spacing:.07em;color:{SEC};text-transform:uppercase;
  margin:6px 0 2px}}
.li{{display:flex;gap:9px;align-items:flex-start;line-height:1.25;margin:1.5px 0}}
.li.quiet{{color:{SEC}}}
.li .m{{color:{MUT};font-weight:400;font-size:11.5px}}
.codes{{color:{MUT};font-size:10.5px}}
.sw{{width:17px;height:17px;border-radius:3px;flex:none;border:1px solid rgba(0,0,0,.2);margin-top:1px}}
.pli{{display:inline-flex;align-items:center;gap:5px;margin-right:10px;font-size:11.5px}}
.pdot{{width:11px;height:11px;border-radius:50%;border:1.5px solid #fff;box-shadow:0 0 0 1px #999}}
.dash{{background:transparent;border:2.5px dashed {FLU_FLAG}}}
.foot{{margin-top:auto;padding-top:8px;font-size:10px;color:{MUT};line-height:1.45}}
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
    <div class="li" data-lyr="lyr-flu"><span class="sw dash"></span><div><b>Future land use invites MF / attached</b>
      <span class="m">comp-plan signal — rezone-likely</span></div></div>
    <h3>Everything else — what it is today</h3>
    {arows}
    <h3>Supply-chart deals ≥100 units (number = chart row)</h3>
    <div style="line-height:1.9" class="li" data-lyr="lyr-pins">{prow}</div>
    <div class="li quiet" data-lyr="lyr-labels" style="font-size:11.5px">Parcel labels (largest MF-capable)</div>
    <div class="li quiet" style="font-size:11px">Deals under 100 units stay in the Supply Chart but are not pinned here.</div>
    <div class="li"><span class="sw" style="background:transparent;border:2.5px dashed {GOLD};border-radius:50%"></span>5-mile ring · ★ subject</div>
    <div class="foot">Vacant = Ada County assessor vacant-land parcels (PROPCODE L) ≥1 ac after removing
    common/HOA, non-buildable and road-sliver lots. Green-hatched farms (PROPCODE F) and tan large-lot
    homesteads look vacant on imagery and CAN sell &amp; develop — Syringa Crossing, Graycliff and the
    Brighton master plans all started as this class — but they carry improvements, so they sit outside
    the assessor-vacant screen. Airport ops, the AIA overlay, Micron, and non-Micron industrial are coded
    separately. Satellite: Esri World Imagery. Full parcel detail: land-use workbook.</div>
  </div>
</div>
</div></body></html>"""
    open(f"{SP}/{cfg['out_html']}", "w", encoding="utf-8").write(html)
    print("wrote", cfg["out_html"])
    # interactive variant: self-contained, per-layer checkboxes
    import base64
    b64 = base64.b64encode(open(f"{SP}/{cfg['key']}_sat.jpg", "rb").read()).decode()
    inter = html.replace(f'src="{cfg["key"]}_sat.jpg"', f'src="data:image/jpeg;base64,{b64}"')
    inter = inter.replace("</h1>", " <span style='font-size:13px;font-weight:400;color:#898781'>"
                          "&mdash; interactive: use the legend checkboxes to toggle layers</span></h1>")
    script = '''<script>
document.querySelectorAll('[data-lyr]').forEach(function(row){
  var lid = row.getAttribute('data-lyr');
  var g = document.getElementById(lid);
  if(!g) return;
  var cb = document.createElement('input');
  cb.type = 'checkbox'; cb.checked = true;
  cb.style.cssText = 'margin:2px 4px 0 0;flex:none;cursor:pointer';
  cb.addEventListener('change', function(){ g.style.display = cb.checked ? '' : 'none'; });
  row.style.cursor = 'pointer';
  row.insertBefore(cb, row.firstChild);
});
</script>'''
    inter = inter.replace("</body>", script + "</body>")
    out_i = f"{cfg['deal']}/{cfg['subject']} - Vacant Land by Zoning (interactive).html"
    open(out_i, "w", encoding="utf-8").write(inter)
    print("wrote", out_i)

if __name__ == "__main__":
    for cfg in DEALS:
        build(cfg)
