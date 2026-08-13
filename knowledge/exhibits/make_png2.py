#!/usr/bin/env python3
"""Prelude & Seasons: HelloData history -> underwriting -> actuals. Decluttered hi-res PNG."""
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def txt(x,y,s,cls="lbl",anchor="middle",dy=0):
    return f'<text x="{x:.1f}" y="{y+dy:.1f}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>'
def smooth(pts):
    if len(pts)<3: return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    p=[pts[0]]+pts+[pts[-1]]
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1,len(p)-2):
        p0,p1,p2,p3=p[i-1],p[i],p[i+1],p[i+2]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d

W,H=1000,470
x0,x1,y0,y1=80,860,42,382
xmin,xmax=2023.35,2032.2
vmin,vmax=1500,2300
sx=lambda t:x0+(t-xmin)/(xmax-xmin)*(x1-x0)
sy=lambda v:y1-(v-vmin)/(vmax-vmin)*(y1-y0)
P=lambda pts:[(sx(a),sy(v)) for a,v in pts]
out=[f'<svg viewBox="0 0 {W} {H}" class="chart" xmlns="http://www.w3.org/2000/svg">']
for gv in range(1500,2301,150):
    gy=sy(gv)
    out.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" class="grid"/>')
    out.append(txt(x0-10,gy,f"${gv:,}","tick","end",dy=4))
for yr in range(2024,2033):
    out.append(txt(sx(yr),y1+22,str(yr),"tick"))
    out.append(f'<line x1="{sx(yr):.1f}" y1="{y1}" x2="{sx(yr):.1f}" y2="{y1+5}" class="axisline"/>')
out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" class="axisline"/>')

# HelloData mix-weighted asking (thin, translucent)
pre_hd=[(2023.625,1701),(2023.875,1648),(2024.125,1631),(2024.375,1616),(2024.625,1692),(2024.875,1595),(2025.125,1616),(2025.375,1677),(2025.625,1727),(2025.875,1696)]
sea_hd=[(2024.375,1807),(2024.625,1844),(2024.875,1730),(2025.125,1723),(2025.375,1801),(2025.625,1769),(2025.875,1677),(2026.125,1723),(2026.375,1912),(2026.54,1938)]
out.append('<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in P(pre_hd))+'" class="line hd c2hd"/>')
out.append('<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in P(sea_hd))+'" class="line hd c1hd"/>')
out.append(txt(sx(2024.55),sy(1875),"Seasons — HelloData asking","hdlbl c1t"))
out.append(txt(sx(2024.45),sy(1548),"Prelude — HelloData asking","hdlbl c2t"))
# T90 marker
out.append(f'<circle cx="{sx(2026.54):.1f}" cy="{sy(1938):.1f}" r="5" class="dot c1"/>')
out.append(txt(sx(2026.54)-10,sy(1938)-10,"HD T90 $1,938","itemsub c1t","end"))

# Seasons UW (bold smooth)
sea_uw=[(2026.62,1885),(2027.83,1960),(2028.83,2038),(2029.83,2110),(2030.83,2184),(2031.9,2249)]
out.append(f'<path d="{smooth(P(sea_uw))}" class="line seasons"/>')
out.append(f'<circle cx="{sx(2026.62):.1f}" cy="{sy(1885):.1f}" r="5" class="dot c1"/>')
out.append(txt(sx(2026.75)+2,sy(1885)-10,"UW enters $1,885","itemsub c1t","start"))
out.append(f'<circle cx="{sx(2031.9):.1f}" cy="{sy(2249):.1f}" r="5" class="dot c1"/>')
out.append(txt(866,sy(2249),"Seasons UW","seriesnote c1t","start",dy=-3))
out.append(txt(866,sy(2249),"$2,249 in 2032","seriesval c1t","start",dy=13))

# Prelude UW (dashed)
pre_uw=[(2026.5,1668),(2027.5,1745),(2028.5,1808),(2029.5,1883),(2030.5,1952)]
out.append(f'<path d="{smooth(P(pre_uw))}" class="line uwdash c2line"/>')
out.append(f'<circle cx="{sx(2030.5):.1f}" cy="{sy(1952):.1f}" r="5" class="dot c2 hollow"/>')
out.append(txt(sx(2030.62)+2,sy(1952)+4,"Prelude UW $1,952","seriesnote c2t","start"))

# Prelude actuals 2026 (bold short line + one dot)
act=[(2026+(m+0.5)/12,v) for m,v in enumerate([1668,1670,1672,1675,1675,1682,1684])]
out.append(f'<path d="{smooth(P(act))}" class="line actual"/>')
out.append(txt(sx(2026.05)-6,sy(1668)+18,"2026 actuals — in-place $1,680","itemsub c2t","end"))
out.append(f'<circle cx="{sx(2026.62):.1f}" cy="{sy(1811):.1f}" r="5" class="dot c2"/>')
out.append(txt(sx(2026.62)+12,sy(1811)+4,"L5 new leases $1,811","itemsub c2t","start"))
out.append('</svg>')
svg=''.join(out)

html=f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#ffffff;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
.frame{{width:1240px;padding:36px 40px 24px;background:#ffffff}}
h1{{font-family:Georgia,'Times New Roman',serif;font-size:26px;margin:0 0 6px;color:#0b0b0b}}
.sub{{font-size:14px;color:#52514e;margin:0 0 16px;max-width:105ch}}
.src{{font-size:11.5px;color:#898781;margin-top:8px}}
.chart{{width:100%;height:auto;display:block}}
text{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
.tick{{font-size:12.5px;fill:#898781}}
.axisline{{stroke:#c3c2b7;stroke-width:1.5}}
.grid{{stroke:#e1e0d9;stroke-width:1}}
.dot{{stroke:#ffffff;stroke-width:2}}
.dot.c1{{fill:#2a78d6}} .dot.c2{{fill:#eb6834}}
.dot.hollow{{fill:#ffffff}} .dot.hollow.c2{{stroke:#eb6834;stroke-width:2.5}}
.itemsub{{font-size:11.5px;fill:#898781;paint-order:stroke;stroke:#ffffff;stroke-width:3px}}
.hdlbl{{font-size:11.5px;font-weight:600;paint-order:stroke;stroke:#ffffff;stroke-width:3px}}
.line{{fill:none;stroke-linejoin:round}}
.line.seasons{{stroke:#2a78d6;stroke-width:3.2}}
.line.uwdash{{stroke-dasharray:7 5;stroke-width:2.4}}
.line.c2line{{stroke:#eb6834}}
.line.actual{{stroke:#eb6834;stroke-width:3.4}}
.line.hd{{stroke-width:2;opacity:0.5}}
.line.c1hd{{stroke:#2a78d6}} .line.c2hd{{stroke:#eb6834}}
.seriesnote{{font-size:12.5px;font-weight:600}}
.seriesval{{font-size:14px;font-weight:700}}
.c1t{{fill:#2a78d6}} .c2t{{fill:#eb6834}}
</style></head><body>
<div class="frame" id="frame">
<h1>Rents: HelloData history, underwriting, and actuals</h1>
<p class="sub">Mix-weighted asking rent per unit (HelloData, quarterly, thin lines) against each deal's underwriting (bold).
Weighting = per-floor-plan values x rent-roll unit counts (the Seasons model's CF-Annual convention). Prelude's last-5 new
leases average $1,811 (Seasons L5 methodology), 4.7% above its UW market rent; Seasons' UW enters at $1,885 — below the
latest 90-day HelloData asking of $1,938.</p>
{svg}
<p class="src">Blue = Seasons at Meridian (2024, 932 SF avg) · Orange = Prelude at Paramount (2018, 1,016 SF avg). Sources: HelloData mix-weighted asking per each TMG model's Rent Analysis / Market Rent Summary (Seasons pull 8/2026; Prelude pull 11/2025); Prelude accrual statement &amp; rent roll 8/13/26; acquisition models. Confidential — internal work product.</p>
</div></body></html>"""
open('prelude_seasons_hd.html','w').write(html)
print('written')
