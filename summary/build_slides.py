#!/usr/bin/env python3
"""Build one 4:3 presentation PNG per deal: the 5-mile supply + land-use story.

Layout (1600x1200 CSS px, screenshotted at 2x):
  header   deal name + one-line takeaway + as-of chip
  left     vector map: land-capacity fills (sections.geojson) under
           lifecycle-colored supply pins (supply map PINS), 5-mi ring, subject
  right    KPI tiles -> supply timeline by delivery year -> largest live deals
  footer   sources

Colors follow the dataviz reference palette (validated order):
  stabilized #2a78d6 / leasing #eda100 / UC #008300 / proposed #e34948 /
  latent (land + shadow pins) #4a3aa7. Land fills are muted tints so the
  saturated pins read as the foreground layer.
"""
import json, math, re, sys

SLIDES = [
    dict(
        key="CR", subject="Canyon Ridge",
        supply_map="CanyonRidge/supply/Canyon_Ridge__Map.html",
        out_html="cr_slide.html",
        title="Canyon Ridge — 5-Mile Competitive Supply & Land Capacity",
        takeaway=("Geography caps the competition: 67 ac of apartment-ready ground in the ring — airport, "
                  "Micron and industrial land block the rest; the July 2026 deep-dive left only ~500 live proposed units "
                  "(Roundhouse's Victory, permits filed + Hawkins' upsized 200-unit Bench deal) — the other ~1,500 are stalled or expired paper."),
        landmarks=[("Boise Airport / Gowen Field", 43.5535, -116.2330),
                   ("Micron", 43.5270, -116.1465)],
        tl_note=("no deliveries 2025\u201326", 3.5),
    ),
    dict(
        key="SaM", subject="Seasons at Meridian",
        supply_map="SeasonsMeridian/supply/Seasons_at_Meridian__Map.html",
        out_html="sam_slide.html",
        title="Seasons at Meridian — 5-Mile Competitive Supply & Land Capacity",
        takeaway=("Supply pressure is real and understated by the vendors: 815 units still in lease-up, 1,213 under "
                  "construction, and 1,794 proposed still credible (+1,378 stalled, excluded) — the July 2026 deep-dive "
                  "killed two dead proposals and revived Union 93 as Heritage Square (250u, Ahlquist/Pacific)."),
        landmarks=[("Ten Mile / I-84", 43.5850, -116.4420),
                   ("The Village at Meridian", 43.6335, -116.3230)],
    ),
]

C = {  # validated categorical assignment
    "stab": "#2a78d6", "lease": "#eda100", "uc": "#008300",
    "prop": "#e34948", "latent": "#4a3aa7",
}
INK = {"pri": "#0b0b0b", "sec": "#52514e", "mut": "#898781",
       "grid": "#e1e0d9", "axis": "#c3c2b7", "surface": "#fcfcfb", "page": "#f9f9f7"}
GOLD = "#D4A017"

LAND_FILL = {   # muted background tints (land layer recedes; pins carry saturation)
    "apt_ready": "#dcd8f0",   # latent violet tint
    "mpc_res":   "#f7dbe7",   # light magenta
    "landbank":  "#e9e5d8",   # pale olive-neutral
    "apartments": "#efede7",  # context — projects are shown as pins, not fills
    "established": "#efede7", "commercial": "#efede7", "civic": "#efede7", "rural": "#f3f1ea",
}
OFFLIMITS = {"airport", "airport_land", "industry", "micron"}

def bucket_key(b):
    b = b.lower()
    if "stab" in b: return "stab"
    if "leas" in b: return "lease"
    if "under" in b: return "uc"
    if "propose" in b: return "prop"
    if "shadow" in b: return "latent"
    return None

def load_pins(path):
    s = open(path, encoding="utf-8").read()
    pins = json.loads(re.search(r"const PINS = (\[.*?\]);", s, re.S).group(1))
    leg = json.loads(re.search(r"const LEG = (\[.*?\]);", s, re.S).group(1))
    return pins, leg

def year_of(deliver):
    m = re.search(r"(20\d\d)", str(deliver or ""))
    return int(m.group(1)) if m else None

def fmt(n):
    return f"{n:,.0f}"

def build_slide(cfg, sections, acres_by_subject):
    pins, leg = load_pins(cfg["supply_map"])
    subj = next(p for p in pins if p["bucket"] == "SUBJECT")
    comps = [p for p in pins if p["bucket"] != "SUBJECT"]

    # ---------- map geometry ----------
    lat0, lon0 = subj["lat"], subj["lng"]
    coslat = math.cos(math.radians(lat0))
    R = 5.0 / 69.0
    MW, MH = 850, 918
    pad = 1.10
    scale = min(MW, MH) / (2 * R * pad)
    def xy(lat, lon):
        return (MW / 2 + (lon - lon0) * coslat * scale, MH / 2 - (lat - lat0) * scale)

    svg = [f'<svg viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}" '
           f'font-family="system-ui,-apple-system,\'Segoe UI\',sans-serif">']
    svg.append('<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="7" height="7" '
               'patternTransform="rotate(45)">'
               '<rect width="7" height="7" fill="#dedcd6"/>'
               '<line x1="0" y1="0" x2="0" y2="7" stroke="#c2bfb7" stroke-width="1.6"/></pattern>'
               f'<clipPath id="disc"><circle cx="{MW/2}" cy="{MH/2}" r="{R*scale}"/></clipPath></defs>')
    svg.append(f'<circle cx="{MW/2}" cy="{MH/2}" r="{R*scale}" fill="#f6f4ee"/>')

    def ring_path(rings):
        d = []
        for ring in rings:
            pts = [xy(p[1], p[0]) for p in ring]
            d.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z")
        return " ".join(d)

    svg.append('<g clip-path="url(#disc)">')
    order = ["rural", "established", "commercial", "civic", "apartments",
             "landbank", "mpc_res", "apt_ready"]
    feats = sorted(sections, key=lambda f: (order.index(f["properties"]["cat"])
                                            if f["properties"]["cat"] in order else -1))
    for f in feats:
        cat = f["properties"]["cat"]
        geom = f["geometry"]
        rings = geom["coordinates"] if geom["type"] == "Polygon" else \
                [r for poly in geom["coordinates"] for r in poly]
        fill = "url(#hatch)" if cat in OFFLIMITS else LAND_FILL.get(cat, "#efede7")
        svg.append(f'<path d="{ring_path(rings)}" fill="{fill}" fill-rule="evenodd" '
                   f'stroke="#ffffff" stroke-width="0.5"/>')
    svg.append('</g>')

    svg.append(f'<circle cx="{MW/2}" cy="{MH/2}" r="{R*scale}" fill="none" '
               f'stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="9 7"/>')

    for name, la, lo in cfg["landmarks"]:
        x, y = xy(la, lo)
        if 0 < x < MW and 0 < y < MH:
            svg.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="13" font-weight="600" '
                       f'fill="{INK["sec"]}" text-anchor="middle" letter-spacing=".04em" '
                       f'stroke="#ffffff" stroke-width="3.5" paint-order="stroke" '
                       f'style="text-transform:uppercase">{name}</text>')

    # pins: draw latent first, then pipeline, then delivered on top
    z = {"latent": 0, "prop": 1, "uc": 2, "lease": 3, "stab": 4}
    placed = []   # (x, y, r) — nudge overlapping pins apart so numbers stay legible
    pos = {}
    for p in sorted(comps, key=lambda p: -(p["units"] or 0)):
        x, y = xy(p["lat"], p["lng"])
        r = max(9, min(22, 4.5 * math.sqrt((p["units"] or 40) / 10)))
        for _ in range(40):
            hit = next(((ox, oy, orr) for ox, oy, orr in placed
                        if math.hypot(x - ox, y - oy) < r + orr + 1.5), None)
            if not hit:
                break
            ox, oy, orr = hit
            d = math.hypot(x - ox, y - oy) or 0.1
            push = (r + orr + 1.6 - d)
            x += (x - ox) / d * push
            y += (y - oy) / d * push
        placed.append((x, y, r))
        pos[id(p)] = (x, y, r)
    for p in sorted(comps, key=lambda p: z[bucket_key(p["bucket"])]):
        k = bucket_key(p["bucket"])
        x, y, r = pos[id(p)]
        dash = ' stroke-dasharray="3 2.4"' if k == "latent" else ""
        if k == "latent":
            r = min(r, 12)
        op = ' fill-opacity="0.85"' if k == "latent" else ""
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{C[k]}"{op} '
                   f'stroke="#ffffff" stroke-width="2.2"{dash}/>')
        if p.get("num") not in (None, "•") and r >= 10:
            svg.append(f'<text x="{x:.1f}" y="{y + r*0.38:.1f}" font-size="{max(10, r*0.95):.0f}" '
                       f'font-weight="700" fill="#ffffff" text-anchor="middle">{p["num"]}</text>')
    sx, sy = xy(subj["lat"], subj["lng"])
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 15 if i % 2 == 0 else 6.5
        star.append(f"{sx + rr*math.cos(ang):.1f},{sy + rr*math.sin(ang):.1f}")
    svg.append(f'<polygon points="{" ".join(star)}" fill="{INK["pri"]}" stroke="#ffffff" stroke-width="2.5"/>')
    svg.append(f'<text x="{sx:.0f}" y="{sy - 24:.0f}" font-size="15" font-weight="800" '
               f'fill="{INK["pri"]}" text-anchor="middle" stroke="#ffffff" stroke-width="4" '
               f'paint-order="stroke">{cfg["subject"].upper()}</text>')
    svg.append("</svg>")
    map_svg = "".join(svg)

    # ---------- KPI numbers ----------
    def leg_get(key):
        it = next((l for l in leg if l["key"] == key), None)
        return (it["n"], it["u"]) if it else (0, 0)
    n_stab, u_stab = leg_get("stab"); n_lease, u_lease = leg_get("lease")
    n_uc, u_uc = leg_get("uc"); n_prop, u_prop = leg_get("prop")
    def is_stalled(p):
        return "stalled" in (p.get("notes") or "").lower()
    stalled = [p for p in comps if bucket_key(p["bucket"]) == "prop" and is_stalled(p)]
    u_stall = sum(p["units"] or 0 for p in stalled)
    n_prop -= len(stalled); u_prop -= u_stall
    acres = acres_by_subject[cfg["subject"]]

    kpis = [
        (fmt(u_stab + u_lease), "units delivered since 2022",
         (f"{n_stab + n_lease} communities · {fmt(u_lease)} still leasing up" if u_lease
          else f"{n_stab + n_lease} communities · all stabilized"), C["stab"]),
        (fmt(u_uc), "units under construction",
         f"{n_uc} project{'s' if n_uc != 1 else ''}, ground broken", C["uc"]),
        (fmt(u_prop), "units proposed (live)",
         f"{n_prop} deals after July 2026 diligence"
         + (f" · +{fmt(u_stall)} stalled, excluded" if u_stall else ""), C["prop"]),
        (fmt(acres["ready"]) + " ac", "apartment-ready ground (no active plan)",
         f"+{fmt(acres['behind'])} ac master-planned / land-bank behind it", C["latent"]),
    ]

    # ---------- timeline ----------
    years = list(range(2022, 2030))
    tl = {y: {k: 0 for k in C} for y in years}
    tbd = {k: 0 for k in C}
    for p in comps:
        k = bucket_key(p["bucket"])
        if k == "latent" or not p.get("units"):
            continue
        if k == "prop" and is_stalled(p):
            continue                      # stalled: mapped + tabled, not forecast
        y = year_of(p.get("deliver"))
        if k == "prop" and y and y <= 2026:
            y = None                      # a "proposed" deal can't deliver by as-of
        if y and y in tl:
            tl[y][k] += p["units"]
        else:
            tbd[k] += p["units"]
    cols = [(str(y), tl[y]) for y in years] + [("TBD", tbd)]
    maxu = max(sum(v.values()) for _, v in cols) or 1
    TW, TH, TB = 640, 300, 34
    bw = TW / len(cols) * 0.62
    step = TW / len(cols)
    t = [f'<svg viewBox="0 0 {TW} {TH + TB}" style="width:100%;height:auto;display:block" '
         f'font-family="system-ui,sans-serif">']
    for gy in (0.25, 0.5, 0.75, 1.0):
        yy = TH - gy * (TH - 30)
        t.append(f'<line x1="0" y1="{yy:.0f}" x2="{TW}" y2="{yy:.0f}" stroke="{INK["grid"]}" stroke-width="1"/>')
    note = cfg.get("tl_note")
    if note:
        nx = (note[1] + 0.5) * step
        t.append(f'<text x="{nx:.0f}" y="{TH - 14}" font-size="12" fill="{INK["mut"]}" '
                 f'text-anchor="middle" font-style="italic">{note[0]}</text>')
    asof_x = (2026 - 2022 + 0.86) * step
    t.append(f'<line x1="{asof_x:.0f}" y1="16" x2="{asof_x:.0f}" y2="{TH}" stroke="{INK["axis"]}" '
             f'stroke-width="1.4" stroke-dasharray="4 4"/>')
    t.append(f'<text x="{asof_x - 6:.0f}" y="14" font-size="11.5" fill="{INK["mut"]}" '
             f'text-anchor="end">as-of Q2 2026</text>')
    for i, (lab, v) in enumerate(cols):
        x = i * step + (step - bw) / 2
        y = TH
        total = sum(v.values())
        for k in ("stab", "lease", "uc", "prop"):
            u = v[k]
            if not u:
                continue
            h = u / maxu * (TH - 30)
            y -= h
            if lab == "TBD":
                t.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h-2,2):.1f}" rx="4" '
                         f'fill="none" stroke="{C[k]}" stroke-width="2" stroke-dasharray="5 3"/>')
            else:
                t.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h-2,2):.1f}" rx="4" fill="{C[k]}"/>')
        if total:
            t.append(f'<text x="{x + bw/2:.1f}" y="{y - 7:.1f}" font-size="13" font-weight="700" '
                     f'fill="{INK["pri"]}" text-anchor="middle">{fmt(total)}</text>')
        t.append(f'<line x1="0" y1="{TH}" x2="{TW}" y2="{TH}" stroke="{INK["axis"]}" stroke-width="1.4"/>')
        t.append(f'<text x="{i * step + step/2:.1f}" y="{TH + 22}" font-size="13" '
                 f'fill="{INK["sec"]}" text-anchor="middle">{lab}</text>')
    timeline_svg = "".join(t) + "</svg>"

    # ---------- top live pipeline deals ----------
    live = sorted([p for p in comps if bucket_key(p["bucket"]) in ("uc", "prop")],
                  key=lambda p: -(p["units"] or 0))[:8]
    rows = ('<tr class="hdr"><td>Deal</td><td class="num">Units</td>'
            '<td>Est. delivery</td><td>Status (diligence)</td></tr>')
    for p in live:
        k = bucket_key(p["bucket"])
        status = "Under construction" if k == "uc" else "Proposed"
        note = ""
        nl = (p.get("notes") or "").lower()
        if "stalled" in nl: status, note = "Stalled", " · not in totals"
        elif "analyst-sourced" in nl: note = " · analyst-sourced"
        elif "remand" in nl or "hearings" in nl: note = " · contested"
        rows += (f'<tr><td><span class="dot" style="background:{C[k]}"></span>{p["name"]}</td>'
                 f'<td class="num">{fmt(p["units"])}</td>'
                 f'<td>{p.get("deliver") or "TBD"}</td>'
                 f'<td class="mut">{status}{note}</td></tr>')

    legend = "".join(
        f'<span class="li"><span class="dot" style="background:{c}{";border:1.5px dashed #fff" if k=="latent" else ""}"></span>{lab}</span>'
        for k, c, lab in [
            ("stab", C["stab"], "Stabilized (new construction)"),
            ("lease", C["lease"], "Leasing up"),
            ("uc", C["uc"], "Under construction"),
            ("prop", C["prop"], "Proposed (live)"),
            ("latent", C["latent"], "Latent site (watch list)")])
    land_legend = (
        f'<span class="li"><span class="sw" style="background:{LAND_FILL["apt_ready"]}"></span>Apartment-ready land</span>'
        f'<span class="li"><span class="sw" style="background:{LAND_FILL["mpc_res"]}"></span>Master-planned res.</span>'
        f'<span class="li"><span class="sw" style="background:{LAND_FILL["landbank"]}"></span>Land-bank / future</span>'
        f'<span class="li"><span class="sw hatch"></span>Off-limits (airport · Micron · industry)</span>')

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:1200px;background:{INK['page']};
  font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:{INK['pri']};overflow:hidden}}
.slide{{width:1600px;height:1200px;display:flex;flex-direction:column;padding:34px 40px 20px}}
header h1{{font-size:31px;font-weight:800;letter-spacing:-.01em}}
header .take{{font-size:16.5px;color:{INK['sec']};margin-top:7px;max-width:1230px;line-height:1.4}}
.asof{{position:absolute;top:10px;right:4px;font-size:13px;color:{INK['mut']};
  border:1px solid {INK['grid']};border-radius:14px;padding:4px 12px;background:{INK['surface']}}}
.body{{flex:1;display:flex;gap:26px;margin-top:18px;min-height:0}}
.mapcard{{flex:none;width:882px;background:{INK['surface']};border:1px solid {INK['grid']};border-radius:10px;
  padding:14px 14px 10px;display:flex;flex-direction:column}}
.maplegend{{display:flex;flex-wrap:wrap;gap:5px 16px;font-size:12.5px;color:{INK['sec']};margin-top:6px}}
.maplegend .cap{{font-weight:700;color:{INK['pri']};font-size:11.5px;letter-spacing:.05em;flex-basis:100%}}
.li{{display:inline-flex;align-items:center;gap:6px}}
.dot{{width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #bbb;flex:none}}
.sw{{width:14px;height:14px;border-radius:3px;border:1px solid #d5d2ca;flex:none}}
.sw.hatch{{background:repeating-linear-gradient(45deg,#dedcd6 0 3px,#c2bfb7 3px 4.5px)}}
.right{{flex:1;display:flex;flex-direction:column;gap:16px;min-width:0}}
.kpis{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.kpi{{background:{INK['surface']};border:1px solid {INK['grid']};border-radius:10px;
  padding:12px 16px 10px;border-top:4px solid var(--c)}}
.kpi .v{{font-size:33px;font-weight:800;letter-spacing:-.02em}}
.kpi .l{{font-size:14.5px;font-weight:700;margin-top:1px}}
.kpi .s{{font-size:12.5px;color:{INK['mut']};margin-top:3px}}
.panel{{background:{INK['surface']};border:1px solid {INK['grid']};border-radius:10px;padding:14px 18px}}
.panel h3{{font-size:13px;font-weight:700;letter-spacing:.06em;color:{INK['sec']};
  text-transform:uppercase;margin-bottom:8px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
td{{padding:5.5px 6px;border-top:1px solid {INK['grid']}}}
tr.hdr td{{border-top:none;color:{INK['mut']};font-size:11.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding-bottom:2px}}
td .dot{{margin-right:8px;display:inline-block;vertical-align:-1px}}
td.num{{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}}
td.mut{{color:{INK['mut']};font-size:12.5px}}
footer{{margin-top:12px;font-size:12px;color:{INK['mut']}}}
</style></head><body><div class="slide">
<header style="position:relative">
  <h1>{cfg['title']}</h1>
  <div class="take">{cfg['takeaway']}</div>
  <div class="asof">CoStar Q2 2026 &middot; diligence July 2026</div>
</header>
<div class="body">
  <div class="mapcard">
    {map_svg}
    <div class="maplegend">
      <span class="cap">SUPPLY (numbered = Supply Chart rows · sized by units)</span>
      {legend}
      <span class="cap" style="margin-top:2px">LAND CAPACITY (5-mi ring · Ada County parcels + zoning/FLU)</span>
      {land_legend}
    </div>
  </div>
  <div class="right">
    <div class="kpis">
      {"".join(f'<div class="kpi" style="--c:{c}"><div class="v">{v}</div><div class="l">{l}</div><div class="s">{s}</div></div>' for v, l, s, c in kpis)}
    </div>
    <div class="panel"><h3>New supply by delivery year — units (dashed = timing TBD)</h3>{timeline_svg}</div>
    <div class="panel" style="flex:1"><h3>Largest live pipeline deals</h3><table>{rows}</table></div>
  </div>
</div>
<footer>Sources: CoStar 5-mi exports (Q2 2026) · RealPage · HelloData unit details · Ada County assessor parcels, municipal zoning &amp; future-land-use · city planning records &amp; local reporting (per-deal citations in the Supply Chart Diligence tab) · Hawkins OM (The Judy). Latent watch-list sites are mapped but excluded from unit totals.</footer>
</div></body></html>"""
    return html


def main():
    gj = json.load(open("summary/sections.geojson"))
    ss = json.load(open("summary/sections_summary.json"))
    acres = {}
    for subj in ("Canyon Ridge", "Seasons at Meridian"):
        acres[subj] = {
            "ready": ss["apt_ready"]["by_subject"].get(subj, 0),
            "behind": sum(ss[k]["by_subject"].get(subj, 0) for k in ("mpc_res", "landbank")),
        }
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for cfg in SLIDES:
        secs = [f for f in gj["features"] if f["properties"]["subject"] == cfg["subject"]]
        html = build_slide(cfg, secs, acres)
        path = f"{outdir}/{cfg['out_html']}"
        open(path, "w", encoding="utf-8").write(html)
        print("wrote", path, f"({len(secs)} sections)")


if __name__ == "__main__":
    main()
