"""4:3 ring-comparison slide — Canyon Ridge vs Seasons at Meridian.

Every number is read from the two supply-chart companion maps (PINS/LEG —
the same JSON the workbooks and slides are built from) plus the land-use
sections summary, so the comparison ties to the charts by construction.
Subject properties are INCLUDED in delivered totals and timelines (marked ★),
matching the workbook rosters. Latent/shadow watch sites are shown per ring,
excluded from unit totals (same convention as the charts).

Colors: session lifecycle palette, validated (dataviz six checks; CVD 7.2
floor-band pair prop/uc carries 2px surface gaps + direct labels; orange
contrast WARN relieved by visible value labels).
"""
import json, math, re, sys

C = {"stab": "#2a78d6", "lease": "#eda100", "uc": "#008300",
     "prop": "#e34948", "latent": "#4a3aa7"}
INK = {"pri": "#0b0b0b", "sec": "#52514e", "mut": "#898781",
       "grid": "#e1e0d9", "axis": "#c3c2b7", "surface": "#fcfcfb", "page": "#f9f9f7"}

DEALS = [
    dict(key="CR", subject="Canyon Ridge",
         supply_map="CanyonRidge/supply/Canyon_Ridge__Map.html",
         chart="CanyonRidge/supply/Canyon_Ridge__Supply_Chart.xlsx"),
    dict(key="SaM", subject="Seasons at Meridian",
         supply_map="SeasonsMeridian/supply/Seasons_at_Meridian__Map.html",
         chart="SeasonsMeridian/supply/Seasons_at_Meridian__Supply_Chart.xlsx"),
]

def bucket_key(b):
    b = b.lower()
    if "stab" in b: return "stab"
    if "leas" in b: return "lease"
    if "under" in b: return "uc"
    if "propose" in b: return "prop"
    if "shadow" in b: return "latent"
    return None

def fmt(n): return f"{n:,.0f}"

def year_of(deliver):
    m = re.search(r"(20\d\d)", str(deliver or ""))
    return int(m.group(1)) if m else None

def load(cfg):
    s = open(cfg["supply_map"], encoding="utf-8").read()
    pins = json.loads(re.search(r"const PINS = (\[.*?\]);", s, re.S).group(1))
    leg = json.loads(re.search(r"const LEG = (\[.*?\]);", s, re.S).group(1))
    subj = next(p for p in pins if p["bucket"] == "SUBJECT")
    comps = [p for p in pins if p["bucket"] != "SUBJECT"]
    import openpyxl
    ca = openpyxl.load_workbook(cfg["chart"])["Competitive Analysis"]
    occ = rent = None
    for r in range(1, ca.max_row + 1):
        v = ca.cell(r, 3).value
        if isinstance(v, str) and "(SUBJECT)" in v:
            occ, rent = ca.cell(r, 6).value, ca.cell(r, 7).value
    return subj, comps, {l["key"]: (l["n"], l["u"]) for l in leg}, occ, rent

def main():
    ss = json.load(open("summary/sections_summary.json"))
    data = {}
    for cfg in DEALS:
        subj, comps, leg, occ, rent = load(cfg)
        stalled = [p for p in comps if bucket_key(p["bucket"]) == "prop"
                   and "stalled" in (p.get("notes") or "").lower()]
        latent = [p for p in comps if bucket_key(p["bucket"]) == "latent"]
        u_stall = sum(p["units"] or 0 for p in stalled)
        n_stab, u_stab = leg.get("stab", (0, 0)); n_lease, u_lease = leg.get("lease", (0, 0))
        n_uc, u_uc = leg.get("uc", (0, 0)); n_prop, u_prop = leg.get("prop", (0, 0))
        data[cfg["key"]] = dict(
            cfg=cfg, subj=subj, comps=comps, occ=occ, rent=rent,
            delivered_u=u_stab + u_lease + (subj["units"] or 0),
            delivered_n=n_stab + n_lease + 1,
            lease_u=u_lease, lease_n=n_lease, uc_u=u_uc, uc_n=n_uc,
            live_u=u_prop - u_stall, live_n=n_prop - len(stalled),
            stall_u=u_stall, stall_n=len(stalled),
            latent=latent,
            latent_u=sum(p["units"] or 0 for p in latent),
            latent_sized=[p for p in latent if p.get("units")],
            acres_ready=ss["apt_ready"]["by_subject"].get(cfg["subject"], 0),
            acres_behind=sum(ss[k]["by_subject"].get(cfg["subject"], 0)
                             for k in ("mpc_res", "landbank")),
        )

    # ---------- shared-scale timelines (subject included, marked) ----------
    years = list(range(2022, 2030))
    cols_by = {}
    for k, d in data.items():
        tl = {y: {c: 0 for c in C} for y in years}
        tbd = {c: 0 for c in C}
        sy = year_of(d["subj"].get("deliver")) or 2024
        tl[sy]["stab"] += d["subj"]["units"] or 0          # ★ subject counts
        for p in d["comps"]:
            bk = bucket_key(p["bucket"])
            if bk == "latent" or not p.get("units"):
                continue
            if bk == "prop" and "stalled" in (p.get("notes") or "").lower():
                continue
            y = year_of(p.get("deliver"))
            if bk == "prop" and y and y <= 2026:
                y = None
            if y and y in tl:
                tl[y][bk] += p["units"]
            else:
                tbd[bk] += p["units"]
        cols_by[k] = [(str(y), tl[y]) for y in years] + [("TBD", tbd)]
    maxu = max(sum(v.values()) for cols in cols_by.values() for _, v in cols) or 1

    TW, TH, TB = 780, 236, 30
    def timeline(k):
        d = data[k]
        cols = cols_by[k]
        step = TW / len(cols)
        bw = step * 0.60
        sy = str(year_of(d["subj"].get("deliver")) or 2024)
        t = [f'<svg viewBox="0 0 {TW} {TH + TB}" width="{TW}" height="{TH + TB}" '
             f'font-family="system-ui,sans-serif">']
        for gy in (0.25, 0.5, 0.75):
            t.append(f'<line x1="0" y1="{TH * gy:.0f}" x2="{TW}" y2="{TH * gy:.0f}" '
                     f'stroke="{INK["grid"]}" stroke-width="1"/>')
        for i, (lab, v) in enumerate(cols):
            x = i * step + (step - bw) / 2
            y = TH
            total = sum(v.values())
            dash = ' stroke-dasharray="6 4"' if lab == "TBD" and total else ""
            if lab == "TBD" and total:
                h = total / maxu * (TH - 26)
                t.append(f'<rect x="{x:.1f}" y="{TH - h:.1f}" width="{bw:.1f}" height="{h:.1f}" '
                         f'fill="none" stroke="{C["prop"]}" stroke-width="2"{dash} rx="4"/>')
            else:
                for bk in ("stab", "lease", "uc", "prop"):
                    u = v[bk]
                    if not u:
                        continue
                    h = u / maxu * (TH - 26)
                    y -= h
                    t.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h - 2, 1.5):.1f}" '
                             f'fill="{C[bk]}" rx="3"/>')
            if total:
                star = " ★" if lab == sy else ""
                t.append(f'<text x="{x + bw / 2:.1f}" y="{min(y, TH - (total / maxu) * (TH - 26)) - 7:.1f}" '
                         f'font-size="14" font-weight="700" fill="{INK["pri"]}" '
                         f'text-anchor="middle">{fmt(total)}{star}</text>')
            t.append(f'<text x="{i * step + step / 2:.1f}" y="{TH + 21}" font-size="13.5" '
                     f'fill="{INK["sec"]}" text-anchor="middle">{lab}</text>')
        t.append(f'<line x1="0" y1="{TH}" x2="{TW}" y2="{TH}" stroke="{INK["axis"]}" stroke-width="1.4"/>')
        t.append("</svg>")
        return "".join(t)

    # ---------- comparison table ----------
    def row(label, f, sub=None, dot=None):
        cells = ""
        for k in ("CR", "SaM"):
            val, small = f(data[k])
            cells += (f'<td class="num"><b>{val}</b>'
                      + (f'<div class="small">{small}</div>' if small else "") + "</td>")
        d = f'<span class="dot" style="background:{dot}"></span>' if dot else ""
        s = f'<div class="small">{sub}</div>' if sub else ""
        return f'<tr><td>{d}{label}{s}</td>{cells}</tr>'

    table = row("Delivered since 2022", lambda d: (fmt(d["delivered_u"]),
                f'{d["delivered_n"]} communities, incl. ★ subject'), dot=C["stab"])
    table += row("Still in lease-up", lambda d: (fmt(d["lease_u"]),
                 f'{d["lease_n"]} communities' if d["lease_n"] else "—"), dot=C["lease"])
    table += row("Under construction", lambda d: (fmt(d["uc_u"]), f'{d["uc_n"]} projects'), dot=C["uc"])
    table += row("Proposed — live", lambda d: (fmt(d["live_u"]), f'{d["live_n"]} deals'),
                 sub="credible after July 2026 deep-dive", dot=C["prop"])
    table += row("Proposed — stalled", lambda d: (fmt(d["stall_u"]), f'{d["stall_n"]} deals'),
                 sub="flagged &amp; excluded from totals/timeline")
    table += row("Latent / shadow watch", lambda d: (
                 f'{fmt(d["latent_u"])}+' if d["latent_u"] else f'{len(d["latent"])} sites',
                 f'{len(d["latent"])} sites mapped' if d["latent_u"] else "unsized"),
                 sub="land-use watch list — NOT in totals", dot=C["latent"])
    table += row("Apartment-ready land", lambda d: (f'{fmt(d["acres_ready"])} ac',
                 f'+{fmt(d["acres_behind"])} ac MPC / land-bank'))
    table += row("Subject today", lambda d: (
                 f'{d["occ"] * 100:.1f}%' if d["occ"] else "—",
                 f'${d["rent"]:,.0f} mkt rent · {d["subj"]["units"]}u' if d["rent"] else ""))

    # ---------- latent site lists ----------
    def latent_list(k):
        d = data[k]
        lis = ""
        for p in sorted(d["latent"], key=lambda p: -(p["units"] or 0))[:6]:
            u = f'&nbsp;·&nbsp;~{p["units"]}u' if p.get("units") else ""
            nm = p["name"].split("(")[0].strip()
            lis += f'<li>{nm}{u}</li>'
        more = len(d["latent"]) - 6
        if more > 0:
            lis += f'<li class="mut">+ {more} more unsized sites</li>'
        return lis

    legend = "".join(
        f'<span class="li"><span class="dot" style="background:{c}"></span>{lab}</span>'
        for c, lab in [(C["stab"], "Stabilized"), (C["lease"], "Leasing up"),
                       (C["uc"], "Under construction"), (C["prop"], "Proposed (live)")]) + \
        f'<span class="li"><span class="dot" style="background:none;border:2px dashed {C["prop"]}"></span>Timing TBD (live, undated)</span>'

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:1200px;background:{INK["page"]};overflow:hidden;
  font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:{INK["pri"]}}}
.slide{{width:1600px;height:1200px;padding:34px 42px 24px;display:flex;flex-direction:column}}
h1{{font-size:30px;font-weight:800;letter-spacing:-.01em}}
.sub{{font-size:15.5px;color:{INK["sec"]};margin-top:6px;max-width:1220px;line-height:1.45}}
.chip{{font-size:12.5px;color:{INK["mut"]};background:{INK["surface"]};border:1px solid {INK["grid"]};
  border-radius:14px;padding:4px 12px;white-space:nowrap}}
.cols{{flex:1;display:flex;gap:26px;margin-top:20px;min-height:0}}
.card{{background:{INK["surface"]};border:1px solid {INK["grid"]};border-radius:10px;padding:18px 20px}}
h3{{font-size:12px;font-weight:700;letter-spacing:.07em;color:{INK["sec"]};text-transform:uppercase;margin-bottom:8px}}
table{{border-collapse:collapse;width:100%;font-size:14.5px}}
td{{padding:9px 10px;border-bottom:1px solid {INK["grid"]};vertical-align:top}}
td.num{{text-align:right;font-size:17px;white-space:nowrap}}
tr.hdr td{{font-size:12px;font-weight:700;color:{INK["sec"]};text-transform:uppercase;letter-spacing:.05em;border-bottom:1.6px solid {INK["axis"]}}}
.small{{font-size:11.5px;color:{INK["mut"]};font-weight:400;margin-top:1px}}
.dot{{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:8px;vertical-align:-1px}}
.li{{display:inline-flex;align-items:center;gap:6px;margin-right:16px;font-size:12.5px;color:{INK["sec"]}}}
.tl-h{{font-size:14px;font-weight:700;margin:10px 0 2px}}
ul{{list-style:none;font-size:12.5px;line-height:1.75;color:{INK["sec"]}}}
ul li::before{{content:"◆";color:{C["latent"]};font-size:9px;margin-right:7px;vertical-align:1px}}
ul li.mut{{color:{INK["mut"]}}} ul li.mut::before{{content:""}}
.foot{{margin-top:12px;font-size:10.5px;color:{INK["mut"]};line-height:1.5}}
</style></head><body><div class="slide">
<div style="display:flex;justify-content:space-between;align-items:baseline">
  <h1>Canyon Ridge vs. Seasons at Meridian — 5-Mile Ring Supply</h1>
  <div class="chip">CoStar Q2 2026 · pipeline deep-dive verified 7/16/2026</div>
</div>
<div class="sub">Same underwriting lens, opposite supply pictures: the Canyon Ridge ring is geography-constrained
  ({fmt(data["CR"]["delivered_u"])} units delivered since 2022 and only {fmt(data["CR"]["live_u"])} live proposed units left after diligence),
  while the Seasons ring absorbed {fmt(data["SaM"]["delivered_u"])} units with {fmt(data["SaM"]["uc_u"])} more under construction,
  {fmt(data["SaM"]["live_u"])} credibly proposed, and ~{fmt(data["SaM"]["latent_u"])}+ latent units watch-listed behind them.</div>
<div class="cols">
  <div style="flex:1.12;display:flex;flex-direction:column">
    <div class="card" style="flex:1">
      <h3>New supply by delivery year — units (shared scale, stalled excluded)</h3>
      <div class="tl-h">Canyon Ridge ring <span class="small" style="display:inline">★ = subject delivery ({data["CR"]["subj"]["units"]}u, Q3 2024)</span></div>
      {timeline("CR")}
      <div class="tl-h">Seasons at Meridian ring <span class="small" style="display:inline">★ = subject delivery ({data["SaM"]["subj"]["units"]}u, Q3 2024)</span></div>
      {timeline("SaM")}
      <div style="margin-top:10px">{legend}</div>
    </div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:18px;min-width:0">
    <div class="card">
      <table>
        <tr class="hdr"><td></td><td class="num">Canyon Ridge</td><td class="num">Seasons at Meridian</td></tr>
        {table}
      </table>
    </div>
    <div class="card" style="display:flex;gap:22px">
      <div style="flex:1"><h3>Latent / shadow — Canyon Ridge</h3><ul>{latent_list("CR")}</ul></div>
      <div style="flex:1"><h3>Latent / shadow — Seasons</h3><ul>{latent_list("SaM")}</ul></div>
    </div>
  </div>
</div>
<div class="foot">Ties to the Supply Chart workbooks (July 16, 2026 build): delivered/lease-up/UC/proposed counts are the chart rosters
  (subjects included, marked ★); stalled deals are the deep-dive-flagged rows excluded from chart forecasts; latent/shadow sites are the
  Diligence watch list (mapped, never in unit totals). Land acres: Ada County parcels + zoning/FLU land-use analysis.
  Sources: CoStar 5-mi exports (Q2 2026), RealPage, HelloData, city permit/hearing records — per-deal citations in each workbook's Diligence tab.</div>
</div></body></html>"""
    out = sys.argv[1] if len(sys.argv) > 1 else "summary/Treasure Valley - Ring Comparison.html"
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)

if __name__ == "__main__":
    main()
