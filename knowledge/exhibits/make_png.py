#!/usr/bin/env python3
"""Standalone high-res PNG: Prelude actual vs UW vs Seasons UW rents (smooth)."""

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def txt(x,y,s,cls="lbl",anchor="middle",dy=0):
    return f'<text x="{x:.1f}" y="{y+dy:.1f}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>'

def smooth_path(pts):
    """Catmull-Rom -> cubic Bezier."""
    if len(pts)<3: return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    p=[pts[0]]+pts+[pts[-1]]
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1,len(p)-2):
        p0,p1,p2,p3=p[i-1],p[i],p[i+1],p[i+2]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d

W,H=1000,470
x0,x1,y0,y1=80,845,40,380
xmin,xmax=2025.9,2032.15
vmin,vmax=1500,2350
sx=lambda t:x0+(t-xmin)/(xmax-xmin)*(x1-x0)
sy=lambda v:y1-(v-vmin)/(vmax-vmin)*(y1-y0)
out=[f'<svg viewBox="0 0 {W} {H}" class="chart" xmlns="http://www.w3.org/2000/svg">']
for gv in range(1500,2351,150):
    gy=sy(gv)
    out.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" class="grid"/>')
    out.append(txt(x0-10,gy,f"${gv:,}","tick","end",dy=4))
for yr in range(2026,2033):
    out.append(txt(sx(yr+0.5),y1+22,str(yr),"tick"))
    out.append(f'<line x1="{sx(yr):.1f}" y1="{y1}" x2="{sx(yr):.1f}" y2="{y1+5}" class="axisline"/>')
out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" class="axisline"/>')

# Seasons UW asking — smooth curve through annual values
spts=[(sx(t),sy(v)) for t,v in [(2026.62,1885),(2027.83,1960),(2028.83,2038),(2029.83,2110),(2030.83,2184),(2031.9,2249)]]
out.append(f'<path d="{smooth_path(spts)}" class="line seasons"/>')
out.append(f'<circle cx="{sx(2026.62):.1f}" cy="{sy(1885):.1f}" r="6" class="dot c1"/>')
out.append(f'<circle cx="{sx(2031.9):.1f}" cy="{sy(2249):.1f}" r="6" class="dot c1"/>')
out.append(txt(sx(2027.3),sy(2170),"Seasons enters at $1,885 — already executed, not projected","itemsub","start"))
out.append(f'<circle cx="{sx(2026.62):.1f}" cy="{sy(1751):.1f}" r="6" class="dot c1 hollow"/>')
out.append(txt(sx(2026.62)+12,sy(1751)-10,"contract $1,751","itemsub","start"))

# Prelude UW rent/occupied (dashed)
puw=[(2026.5,1668),(2027.5,1745),(2028.5,1808),(2029.5,1883),(2030.5,1952)]
out.append(f'<path d="{smooth_path([(sx(a),sy(v)) for a,v in puw])}" class="line pencil c2line"/>')
for a,v in puw:
    out.append(f'<circle cx="{sx(a):.1f}" cy="{sy(v):.1f}" r="4" class="dot c2 hollow"/>')
out.append(txt(sx(2030.2),sy(1952),"Prelude UW","seriesnote c2t","end",dy=44))
out.append(txt(sx(2030.2),sy(1952),"$1,952 by 2030","seriesval c2t","end",dy=60))

# Prelude actuals
act=[1668,1670,1672,1675,1675,1682,1684]
apts=[(sx(2026+(m+0.5)/12),sy(v)) for m,v in enumerate(act)]
out.append(f'<path d="{smooth_path(apts)}" class="line actual"/>')
out.append(f'<circle cx="{sx(2026.62):.1f}" cy="{sy(1680):.1f}" r="6" class="dot c2"/>')
out.append(txt(sx(2026.62)+10,sy(1680)+24,"actual in-place $1,680","itemsub","start"))
out.append(f'<circle cx="{sx(2026.21):.1f}" cy="{sy(1575):.1f}" r="7" class="dot c2 hollow"/>')
out.append(txt(sx(2026.21)+12,sy(1575)+4,"Jan-Apr signings $1,575 (n=28)","itemsub","start"))
out.append(f'<circle cx="{sx(2026.54):.1f}" cy="{sy(1731):.1f}" r="7" class="dot c2"/>')
out.append(txt(sx(2026.54)+10,sy(1731)+18,"May-Aug signings $1,731","itemname","start"))
out.append(txt(sx(2026.54)+10,sy(1731)+31,"= UW market rent to the dollar","itemsub","start"))

# gap annotations
out.append(f'<line x1="{sx(2027.62):.1f}" y1="{sy(1758)-4:.1f}" x2="{sx(2027.62):.1f}" y2="{sy(1938)+4:.1f}" class="gapline"/>')
out.append(txt(sx(2027.62)+8,(sy(1758)+sy(1938))/2,"+9%/unit · +19%/SF","gaplbl","start",dy=-12))
out.append(txt(sx(2027.62)+8,(sy(1758)+sy(1938))/2,"the 2024-vs-2018 quality spread","itemsub","start",dy=4))
out.append(f'<line x1="{sx(2030.9):.1f}" y1="{sy(1952)-4:.1f}" x2="{sx(2030.9):.1f}" y2="{sy(2192)+4:.1f}" class="gapline"/>')
out.append(txt(sx(2030.9)+8,(sy(1952)+sy(2192))/2,"+8%","gaplbl","start",dy=4))
out.append(txt(850,sy(2249),"Seasons UW asking","seriesnote c1t","start",dy=-4))
out.append(txt(850,sy(2249),"$2,249 in 2032","seriesval c1t","start",dy=12))

# legend
out.append(f'<line x1="{x0}" y1="{H-14}" x2="{x0+26}" y2="{H-14}" class="line seasons"/>')
out.append(txt(x0+32,H-10,"Seasons UW asking rent","legendlbl","start"))
out.append(f'<line x1="{x0+240}" y1="{H-14}" x2="{x0+266}" y2="{H-14}" class="line pencil c2line"/>')
out.append(txt(x0+272,H-10,"Prelude UW rent/occupied","legendlbl","start"))
out.append(f'<line x1="{x0+470}" y1="{H-14}" x2="{x0+496}" y2="{H-14}" class="line actual"/>')
out.append(txt(x0+502,H-10,"Prelude actuals 2026","legendlbl","start"))
out.append('</svg>')
svg=''.join(out)

html=f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#ffffff;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
.frame{{width:1240px;padding:36px 40px 24px;background:#ffffff}}
h1{{font-family:Georgia,'Times New Roman',serif;font-size:26px;margin:0 0 6px;color:#0b0b0b}}
.sub{{font-size:14px;color:#52514e;margin:0 0 18px;max-width:100ch}}
.src{{font-size:11.5px;color:#898781;margin-top:10px}}
.chart{{width:100%;height:auto;display:block}}
text{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
.tick{{font-size:12.5px;fill:#898781}}
.axisline{{stroke:#c3c2b7;stroke-width:1.5}}
.grid{{stroke:#e1e0d9;stroke-width:1}}
.gapline{{stroke:#0b0b0b;stroke-width:1.4}}
.gaplbl{{font-size:15px;font-weight:700;fill:#0b0b0b}}
.dot{{stroke:#ffffff;stroke-width:2}}
.dot.c1{{fill:#2a78d6}} .dot.c2{{fill:#eb6834}}
.dot.hollow{{fill:#ffffff}}
.dot.hollow.c1{{stroke:#2a78d6;stroke-width:2.5}} .dot.hollow.c2{{stroke:#eb6834;stroke-width:2.5}}
.itemname{{font-size:13px;font-weight:600;fill:#0b0b0b}}
.itemsub{{font-size:11.5px;fill:#898781}}
.legendlbl{{font-size:12.5px;fill:#52514e}}
.line{{fill:none;stroke-width:2.5;stroke-linejoin:round}}
.line.seasons{{stroke:#2a78d6;stroke-width:3}}
.line.pencil{{stroke-dasharray:6 5;stroke-width:2}}
.line.pencil.c2line{{stroke:#eb6834}}
.line.actual{{stroke:#eb6834;stroke-width:3.5}}
.seriesnote{{font-size:12.5px;fill:#52514e;font-weight:600}}
.seriesval{{font-size:14px;fill:#0b0b0b;font-weight:700}}
.c1t{{fill:#2a78d6}} .c2t{{fill:#eb6834}}
</style></head><body>
<div class="frame" id="frame">
<h1>Prelude actual vs. plan — and where Seasons enters</h1>
<p class="sub">Monthly rent per unit. Prelude (280 units, 2018, N Meridian) signs new leases at its underwritten market
rent to the dollar; Seasons (360 units, 2024, SE Meridian) enters at the already-executed $1,885 — +9%/unit
(+19%/SF) above Prelude, the 2024-vs-2018 quality spread, held at +8% through 2030.</p>
{svg}
<p class="src">Sources: Prelude accrual statement Aug-25–Jul-26 &amp; rent roll w/ lease charges 8/13/26; Prelude acquisition model (12/2025); Seasons at Meridian TMG model (8/2026). Avg unit: Prelude 1,016 SF, Seasons 932 SF. Confidential — internal work product.</p>
</div></body></html>"""
open('prelude_chart_standalone.html','w').write(html)
print('html written')
