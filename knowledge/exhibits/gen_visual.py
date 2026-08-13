#!/usr/bin/env python3
"""Generate the Seasons Pencil Test visual brief (self-contained HTML artifact)."""

W = 1000  # viewBox width for all charts

# ---------- helpers ----------
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def svg_open(h, cls=""):
    return f'<svg viewBox="0 0 {W} {h}" class="chart {cls}" role="img" xmlns="http://www.w3.org/2000/svg">'

def txt(x,y,s,cls="lbl",anchor="middle",dy=0):
    return f'<text x="{x:.1f}" y="{y+dy:.1f}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>'

# ============================================================
# 1. NUMBER-LINE LADDER (generic)
# ============================================================
def ladder(h, axis_y, vmin, vmax, x0, x1, ticks, tickfmt, items, vlines=None, zones=None, tip_fmt=None):
    """items: list of dicts: v, name, sub, cls(color class), lane ('a1','a2','b1','b2'), big(bool), hollow(bool)"""
    sx = lambda v: x0 + (v-vmin)/(vmax-vmin)*(x1-x0)
    out = [svg_open(h)]
    # zones (washes under axis area)
    if zones:
        for z in zones:
            zx0, zx1 = sx(z['v0']), sx(z['v1'])
            out.append(f'<rect x="{zx0:.1f}" y="{axis_y-46}" width="{zx1-zx0:.1f}" height="92" class="zone {z.get("cls","")}" rx="6"/>')
            out.append(txt((zx0+zx1)/2, axis_y+38, z['label'], "zonelbl"))
    # axis
    out.append(f'<line x1="{x0}" y1="{axis_y}" x2="{x1}" y2="{axis_y}" class="axisline"/>')
    for t in ticks:
        tx = sx(t)
        out.append(f'<line x1="{tx:.1f}" y1="{axis_y-4}" x2="{tx:.1f}" y2="{axis_y+4}" class="axisline"/>')
        out.append(txt(tx, axis_y+20, tickfmt(t), "tick"))
    # vertical threshold lines
    if vlines:
        for vl in vlines:
            vx = sx(vl['v'])
            out.append(f'<line x1="{vx:.1f}" y1="{vl.get("y0",30)}" x2="{vx:.1f}" y2="{axis_y}" class="threshold"/>')
            for i,l in enumerate(vl['label']):
                out.append(txt(vx+vl.get('dx',0), vl.get("y0",30)-22+i*14, l, "threshlbl", vl.get('anchor','middle')))
    # items
    lane_y = {'a1':(-58,-1),'a2':(-104,-1),'b1':(62,1),'b2':(108,1)}
    for it in items:
        x = sx(it['v']); ly,_sgn = lane_y[it['lane']]
        r = 9 if it.get('big') else 7
        stem_end = axis_y+ly+ (16 if ly>0 else 4)
        out.append(f'<line x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" y2="{stem_end:.1f}" class="stem"/>')
        fillcls = it['cls'] + (' hollow' if it.get('hollow') else '')
        tip = tip_fmt(it) if tip_fmt else f"{it['name']}: {it['sub']}"
        out.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="{r}" class="dot {fillcls}" data-tip="{esc(tip)}"/>')
        nm_cls = "itemname big" if it.get('big') else "itemname"
        dx = it.get('dx',0); anchor = it.get('anchor','middle')
        out.append(txt(x+dx, axis_y+ly, it['name'], nm_cls, anchor))
        out.append(txt(x+dx, axis_y+ly+15, it['sub'], "itemsub", anchor))
    out.append('</svg>')
    return ''.join(out)

fmtK = lambda v: f"${v:.0f}K"
fmtSF = lambda v: f"${v:.2f}"

# --- Chart 1: value ladder today ($K/unit) ---
c1 = ladder(
    h=300, axis_y=160, vmin=266, vmax=400, x0=45, x1=955,
    ticks=[280,300,320,340,360,380,400], tickfmt=fmtK,
    zones=[
        dict(v0=266, v1=304.5, label="below build cost", cls="zone1"),
        dict(v0=304.5, v1=357.7, label="THE WINDOW — above cost, below what induces supply", cls="zone2"),
        dict(v0=357.7, v1=400, label="induces new supply", cls="zone3"),
    ],
    items=[
        dict(v=284.8, name="Prelude (we own)", sub="$284.8K · 2018 build", cls="c2", lane='a1'),
        dict(v=304.5, name="Replacement cost", sub="$304.5K · Emblem TDC", cls="ink", lane='b1'),
        dict(v=327.8, name="SEASONS BID", sub="$327.8K · $118M", cls="c1", lane='a1', big=True),
        dict(v=347.2, name="Whisper", sub="$347.2K · $125M", cls="c1", lane='b1', hollow=True),
        dict(v=357.7, name="Replacement value", sub="$357.7K · cost + margin", cls="ink", lane='a1', hollow=True),
        dict(v=381.9, name="Canyon Ridge award", sub="$381.9K · $110M", cls="c3", lane='b1'),
    ])

# --- Chart 2: rent ladder today ($/SF) ---
c2 = ladder(
    h=310, axis_y=175, vmin=1.60, vmax=2.55, x0=45, x1=955,
    ticks=[1.60,1.80,2.00,2.20,2.40], tickfmt=fmtSF,
    vlines=[
        dict(v=2.17, label=["PENCIL @ 6.5% ROC","$2.17/SF"], y0=52),
        dict(v=2.30, label=["PENCIL, Seasons-like product","$2.30/SF"], y0=52, dx=4, anchor='start'),
    ],
    items=[
        dict(v=1.70, name="Prelude", sub="$1,730 · 1,016 SF", cls="c2", lane='a1'),
        dict(v=1.88, name="Seasons contract", sub="$1,751/mo", cls="c1", lane='b2', hollow=True),
        dict(v=1.97, name="The Judy UW", sub="$1,787 · 908 SF", cls="c5", lane='b1'),
        dict(v=2.02, name="SEASONS MARKET", sub="$1,885 · 932 SF", cls="c1", lane='a1', big=True),
        dict(v=2.20, name="Emblem UW", sub="$2,069 · 939 SF", cls="c4", lane='b1', dx=6),
        dict(v=2.44, name="Canyon Ridge", sub="$2,171 · 889 SF", cls="c3", lane='a1'),
    ])

# --- Chart 3: trajectory line chart ---
def trajectory():
    h=430; x0,x1,y0,y1 = 80,845,40,340
    years=[2027,2028,2029,2030,2031,2032]
    seasons=[1885,1960,2038,2110,2184,2249]
    p65=[2096,2159,2224,2290,2359,2430]
    p60=[1961,2020,2080,2143,2207,2273]
    p70=[2231,2298,2367,2438,2511,2587]
    vmin,vmax=1800,2700
    sx=lambda i: x0+i/(len(years)-1)*(x1-x0)
    sy=lambda v: y1-(v-vmin)/(vmax-vmin)*(y1-y0)
    out=[svg_open(h)]
    # grid + y labels
    for gv in range(1800,2701,150):
        gy=sy(gv)
        out.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" class="grid"/>')
        out.append(txt(x0-10, gy, f"${gv:,}", "tick", "end", dy=4))
    for i,yr in enumerate(years):
        out.append(txt(sx(i), y1+22, str(yr), "tick"))
    # band 6.0–7.0
    band_pts = ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i,v in enumerate(p60)) + ' ' + \
               ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i,v in reversed(list(enumerate(p70))))
    out.append(f'<polygon points="{band_pts}" class="band"/>')
    # pencil 6.5 line (dashed)
    pts65=' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i,v in enumerate(p65))
    out.append(f'<polyline points="{pts65}" class="line pencil"/>')
    # seasons line
    ptsS=' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i,v in enumerate(seasons))
    out.append(f'<polyline points="{ptsS}" class="line seasons"/>')
    # exit marker
    ex=sx(4)
    out.append(f'<line x1="{ex:.1f}" y1="{y0-8}" x2="{ex:.1f}" y2="{y1}" class="threshold"/>')
    out.append(txt(ex, y0-16, "EXIT · Oct 2031", "threshlbl"))
    # endpoint dots + direct labels
    out.append(f'<circle cx="{sx(5):.1f}" cy="{sy(2249):.1f}" r="6" class="dot c1"/>')
    out.append(f'<circle cx="{sx(0):.1f}" cy="{sy(1885):.1f}" r="6" class="dot c1"/>')
    out.append(txt(857, sy(2249), "Seasons UW rent", "seriesnote c1t", "start", dy=14))
    out.append(txt(857, sy(2249), "$2,249", "seriesval c1t", "start", dy=30))
    out.append(txt(857, sy(2430), "Pencil @ 6.5%", "seriesnote", "start", dy=-4))
    out.append(txt(857, sy(2430), "$2,430", "seriesval", "start", dy=12))
    out.append(txt(857, sy(2610), "Band:", "zonelbl", "start"))
    out.append(txt(857, sy(2610), "6.0–7.0% ROC", "zonelbl", "start", dy=15))
    # gap annotations
    for i,glab,gv in [(0,"−10.1%",None),(4,"−7.4%",None)]:
        gx=sx(i); ya,yb=sy(seasons[i]),sy(p65[i])
        out.append(f'<line x1="{gx:.1f}" y1="{ya-8:.1f}" x2="{gx:.1f}" y2="{yb+8:.1f}" class="gapline"/>')
        out.append(txt(gx+8 if i==0 else gx-8, (ya+yb)/2, glab, "gaplbl", "start" if i==0 else "end", dy=4))
    out.append(txt(sx(4)-8, (sy(seasons[4])+sy(p65[4]))/2+18, "frozen from here", "itemsub", "end"))
    # hover columns
    for i,yr in enumerate(years):
        cw=(x1-x0)/(len(years)-1)
        cx0=sx(i)-cw/2 if i>0 else x0-20
        cwid=cw if 0<i<len(years)-1 else cw/2+20
        gap=seasons[i]/p65[i]-1
        tip=f"{yr} — Seasons ${seasons[i]:,} vs pencil ${p65[i]:,} (gap {gap:+.1%})"
        out.append(f'<rect x="{cx0:.1f}" y="{y0}" width="{cwid:.1f}" height="{y1-y0}" class="hovercol" data-tip="{esc(tip)}"/>')
    out.append('</svg>')
    return ''.join(out)
c3 = trajectory()

# --- Chart 4: exit ladder ---
c4 = ladder(
    h=320, axis_y=170, vmin=330, vmax=455, x0=45, x1=955,
    ticks=[340,360,380,400,420,440], tickfmt=fmtK,
    vlines=[dict(v=342.8, label=["Forward replacement cost","$342.8K (3%/yr)"], y0=56)],
    items=[
        dict(v=360.4, name="Prelude exit UW", sub="$361.2K · Dec-30 @5.00%", cls="c2", lane='a1', dx=-8, anchor='end'),
        dict(v=362.4, name="Judy required exit", sub="$361.6K · Aug-30 @5.25%", cls="c5", lane='b1', dx=8, anchor='start'),
        dict(v=399.7, name="Emblem required exit", sub="$400.5K · Jan-30 @5.50%", cls="c4", lane='b1', dx=8, anchor='start'),
        dict(v=401.5, name="SEASONS EXIT UW", sub="$400.6K · Oct-31 @5.00%", cls="c1", lane='a1', big=True, dx=-8, anchor='end'),
        dict(v=442.8, name="Canyon Ridge exit UW", sub="$442.8K · Oct-31 @4.75%", cls="c3", lane='a1', dx=-35),
    ])

c4 = c4.replace('</svg>',
  txt(500, 288, "Same price, different equations — Seasons: $20.1K NOI ÷ 5.00% · Emblem: $22.0K NOI ÷ 5.50%.", "cap")
  + txt(500, 305, "The age discount is in the NOI; the price match comes entirely from the cap-rate assumption.", "cap")
  + '</svg>')

# --- Chart 5a: taxes per unit bars ---
def taxbars():
    h=360; y1=290; y0=60
    vmax=3600
    sy=lambda v: y1-(v/vmax)*(y1-y0)
    bars=[  # (x, val, cls, name, note, ghost_to)
        (120,1169,'c2',"Prelude","actual 0.4507%",None),
        (250,1340,'c1',"Seasons","UW Y1",None),
        (380,1501,'c4',"Emblem","UW stabilized",None),
        (610,2203,'c5',"The Judy","as marketed",3161),
        (740,3428,'c3',"Canyon Ridge","UW Y1 on $110M",None),
    ]
    out=[svg_open(h)]
    out.append(f'<rect x="70" y="{y0-30}" width="380" height="{y1-y0+70}" class="zone zone2" rx="8"/>')
    out.append(f'<rect x="560" y="{y0-30}" width="310" height="{y1-y0+70}" class="zone zone3" rx="8"/>')
    out.append(txt(260, y0-12, "MERIDIAN — levy ≈ 0.45%", "zonelbl"))
    out.append(txt(715, y0-12, "BOISE — levy ≈ 0.92%", "zonelbl"))
    out.append(f'<line x1="70" y1="{y1}" x2="930" y2="{y1}" class="axisline"/>')
    bw=62
    for x,v,cls,name,note,ghost in bars:
        by=sy(v)
        if ghost:
            gy=sy(ghost)
            out.append(f'<rect x="{x}" y="{gy:.1f}" width="{bw}" height="{by-gy:.1f}" class="bar ghost" rx="4" data-tip="Corrected at Boise levy: ${ghost:,}/unit"/>')
            out.append(txt(x+bw/2, gy-24, "corrected", "itemsub"))
            out.append(txt(x+bw/2, gy-10, f"${ghost:,}", "itemsub"))
        out.append(f'<rect x="{x}" y="{by:.1f}" width="{bw}" height="{y1-by:.1f}" class="bar {cls}" rx="4" data-tip="{name}: ${v:,}/unit/yr — {note}"/>')
        out.append(txt(x+bw/2, by-8, f"${v:,}", "itemname"))
        out.append(txt(x+bw/2, y1+20, name, "itemname"))
        out.append(txt(x+bw/2, y1+35, note, "itemsub"))
    out.append(txt(500, 345, "Real estate taxes underwritten, $/unit/yr — same-vintage product, ~$2,100/unit apart on jurisdiction alone", "cap"))
    return ''.join(out)+'</svg>'
c5a = taxbars()

# --- Chart 5b: cap rate dumbbell ---
def capdumb():
    h=170; x0,x1=250,860
    vmin,vmax=4.4,5.3
    sx=lambda v: x0+(v-vmin)/(vmax-vmin)*(x1-x0)
    out=[svg_open(h)]
    for t in [4.5,4.75,5.0,5.25]:
        tx=sx(t)
        out.append(f'<line x1="{tx:.1f}" y1="40" x2="{tx:.1f}" y2="120" class="grid"/>')
        out.append(txt(tx,140,f"{t:.2f}%","tick"))
    ya,yb=60,100
    out.append(txt(230, ya, "Canyon Ridge", "itemname", "end", dy=4))
    out.append(f'<line x1="{sx(4.57):.1f}" y1="{ya}" x2="{sx(5.12):.1f}" y2="{ya}" class="dumbline"/>')
    out.append(f'<circle cx="{sx(4.57):.1f}" cy="{ya}" r="8" class="dot c3 hollow" data-tip="CR as awarded: 4.57% Y1 NOI cap"/>')
    out.append(f'<circle cx="{sx(5.12):.1f}" cy="{ya}" r="8" class="dot c3" data-tip="CR at Meridian tax burden: 5.12%"/>')
    out.append(txt(sx(4.57), ya-16, "4.57% as awarded", "itemsub"))
    out.append(txt(sx(5.12), ya-16, "5.12% tax-normalized", "itemsub"))
    out.append(txt(230, yb, "Seasons bid", "itemname", "end", dy=4))
    out.append(f'<circle cx="{sx(5.00):.1f}" cy="{yb}" r="8" class="dot c1" data-tip="Seasons at $118M: 5.00% Y1 NOI cap"/>')
    out.append(txt(sx(5.00), yb+24, "5.00%", "itemsub"))
    return ''.join(out)+'</svg>'
c5b = capdumb()

# --- Chart 6: other income stacked ---
def oistack():
    h=400; y1=310; y0=50; vmax=4500
    sy=lambda v: y1-(v/vmax)*(y1-y0)
    comps=[("Misc / fees","k1"),("RUBS / billback","k2"),("Parking / garages","k3"),("Wifi / rev share","k4")]
    deals=[
        ("Seasons","actual Y1",[601,698,360,1077]),
        ("Prelude","our UW Y1",[1281,763,759,0]),
        ("Canyon Ridge","UW Y1",[1897,581,520,3]),
        ("The Judy","UW Y3 (not itemized)",None),
        ("Emblem","developer UW",[721,1149,1041,1296]),
    ]
    judy_total=3568
    out=[svg_open(h)]
    out.append(f'<line x1="70" y1="{y1}" x2="930" y2="{y1}" class="axisline"/>')
    for gv in range(0,4501,1000):
        gy=sy(gv)
        out.append(f'<line x1="70" y1="{gy:.1f}" x2="930" y2="{gy:.1f}" class="grid"/>')
        out.append(txt(60, gy, f"${gv:,}", "tick", "end", dy=4))
    bw=90; xs=[120,290,460,630,800]
    for (name,note,vals),x in zip(deals,xs):
        if vals is None:
            by=sy(judy_total)
            out.append(f'<rect x="{x}" y="{by:.1f}" width="{bw}" height="{y1-by:.1f}" class="bar ghost" rx="4" data-tip="The Judy: ${judy_total:,}/unit total — components not itemized in OM"/>')
            out.append(txt(x+bw/2, by-8, f"${judy_total:,}", "itemname"))
        else:
            acc=0
            for (cname,ccls),v in zip(comps,vals):
                if v<=2: acc+=v; continue
                ty0=sy(acc+v); ty1=sy(acc)
                out.append(f'<rect x="{x}" y="{ty0:.1f}" width="{bw}" height="{max(ty1-ty0-2,1):.1f}" class="bar {ccls}" data-tip="{name} — {cname}: ${v:,}/unit/yr"/>')
                acc+=v
            out.append(txt(x+bw/2, sy(acc)-8, f"${acc:,}", "itemname"))
        out.append(txt(x+bw/2, y1+20, name, "itemname"))
        out.append(txt(x+bw/2, y1+35, note, "itemsub"))
    # reference line: stabilized actuals
    ry=sy(2847)
    out.append(f'<line x1="70" y1="{ry:.1f}" x2="930" y2="{ry:.1f}" class="threshold"/>')
    out.append(txt(925, ry-8, "stabilized actuals ≈ $2,850", "threshlbl", "end"))
    # legend
    lx=110
    for cname,ccls in comps:
        out.append(f'<rect x="{lx}" y="{h-28}" width="14" height="14" class="bar {ccls}" rx="3"/>')
        out.append(txt(lx+20, h-17, cname, "legendlbl", "start"))
        lx+=len(cname)*7.2+70
    return ''.join(out)+'</svg>'
c6 = oistack()

# --- Chart 7: two moats quadrant ---
def moats():
    h=440; x0,x1,y0,y1=110,930,50,370
    import math
    xmin,xmax=math.log10(60),math.log10(1600)
    ymin,ymax=-12,16
    sx=lambda a: x0+(math.log10(a)-xmin)/(xmax-xmin)*(x1-x0)
    sy=lambda p: y1-(p-ymin)/(ymax-ymin)*(y1-y0)
    out=[svg_open(h)]
    zero=sy(0)
    # quadrant washes
    out.append(f'<rect x="{x0}" y="{y0}" width="{(x1-x0)/2:.0f}" height="{zero-y0:.1f}" class="zone zone2"/>')
    out.append(f'<rect x="{x0+(x1-x0)/2:.0f}" y="{y0}" width="{(x1-x0)/2:.0f}" height="{zero-y0:.1f}" class="zone zoneRisk"/>')
    out.append(f'<rect x="{x0+(x1-x0)/2:.0f}" y="{zero:.1f}" width="{(x1-x0)/2:.0f}" height="{y1-zero:.1f}" class="zone zone1"/>')
    out.append(f'<line x1="{x0}" y1="{zero:.1f}" x2="{x1}" y2="{zero:.1f}" class="threshold"/>')
    out.append(txt(x0+8, zero-8, "development pencils above this line (rents ≥ 6.5% ROC rent)", "threshlbl", "start"))
    for a in [100,300,1000]:
        ax=sx(a)
        out.append(f'<line x1="{ax:.1f}" y1="{y0}" x2="{ax:.1f}" y2="{y1}" class="grid"/>')
        out.append(txt(ax, y1+22, f"{a:,} ac", "tick"))
    out.append(txt((x0+x1)/2, y1+44, "Apartment-ready land within 5 miles (log scale) — from this repo's parcel analysis", "cap"))
    out.append(f'<text x="26" y="{(y0+y1)/2}" class="cap" text-anchor="middle" transform="rotate(-90 26 {(y0+y1)/2})">Market rent vs 6.5% pencil rent</text>')
    # quadrant labels
    out.append(txt(x0+16, y0+26, "PHYSICAL MOAT", "quad", "start"))
    out.append(txt(x0+16, y0+44, "rents pencil, but no land", "itemsub", "start"))
    out.append(txt(x1-16, y0+26, "SUPPLY INCOMING", "quadRisk", "end"))
    out.append(txt(x1-16, y0+44, "rents pencil + land available", "itemsub", "end"))
    out.append(txt(x1-16, y1-30, "ECONOMIC MOAT", "quad", "end"))
    out.append(txt(x1-16, y1-12, "land abundant, rents don't pencil", "itemsub", "end"))
    # points
    crx,cry=sx(143),sy(12.4)
    out.append(f'<circle cx="{crx:.1f}" cy="{cry:.1f}" r="11" class="dot c3" data-tip="Canyon Ridge: 143 apartment-ready acres · rents +12.4% above pencil · awarded $381.9K/u @ 4.57% Y1"/>')
    out.append(txt(crx, cry-36, "Canyon Ridge", "itemname big"))
    out.append(txt(crx, cry-21, "$381.9K/u · 4.57% Y1", "itemsub"))
    ssx,ssy=sx(1130),sy(-6.9)
    out.append(f'<circle cx="{ssx:.1f}" cy="{ssy:.1f}" r="13" class="dot c1" data-tip="Seasons: 1,130 apartment-ready acres · rents −6.9% below pencil · bid $327.8K/u @ 5.00% Y1"/>')
    out.append(txt(ssx-24, ssy-2, "Seasons", "itemname big", "end"))
    out.append(txt(ssx-24, ssy+14, "$327.8K/u · 5.00% Y1", "itemsub", "end"))
    return ''.join(out)+'</svg>'
c7 = moats()

# --- Chart 8: cost stacks vs price lines ---
def coststack():
    h=430; y1=360; y0=40; vmax=400
    sy=lambda v: y1-(v/vmax)*(y1-y0)
    out=[svg_open(h)]
    for gv in range(0,401,100):
        gy=sy(gv)
        out.append(f'<line x1="90" y1="{gy:.1f}" x2="760" y2="{gy:.1f}" class="grid"/>')
        out.append(txt(80, gy, f"${gv}K", "tick", "end", dy=4))
    out.append(f'<line x1="90" y1="{y1}" x2="760" y2="{y1}" class="axisline"/>')
    stacks=[
        (170,"Emblem Meridian","Lennar GC · Oct-27 GMP",[("Land $34.6K",34.6,"q1"),("Hard $213.2K",213.2,"q2"),("Soft/fees $56.7K",56.7,"q3")]),
        (470,"The Judy (Hawkins)","land at 2024 basis",[("Land $15.1K",15.1,"q1"),("Hard $194.1K",194.1,"q2"),("Soft/fin $48.2K",48.2,"q3")]),
    ]
    bw=150
    for x,name,note,parts in stacks:
        acc=0
        for pname,v,cls in parts:
            ty0=sy(acc+v); ty1=sy(acc)
            out.append(f'<rect x="{x}" y="{ty0:.1f}" width="{bw}" height="{max(ty1-ty0-2,1):.1f}" class="bar {cls}" data-tip="{name} — {pname}/unit"/>')
            if v>25: out.append(txt(x+bw/2,(ty0+ty1)/2+4,pname,"stacklbl"))
            acc+=v
        out.append(txt(x+bw/2, sy(acc)-10, f"${acc:.1f}K/unit", "itemname"))
        out.append(txt(x+bw/2, y1+20, name, "itemname"))
        out.append(txt(x+bw/2, y1+35, note, "itemsub"))
    for v,lab,cls in [(327.8,"Seasons bid $327.8K","c1t"),(357.7,"Replacement value $357.7K",""),(381.9,"Canyon Ridge award $381.9K","c3t")]:
        ly=sy(v)
        out.append(f'<line x1="90" y1="{ly:.1f}" x2="760" y2="{ly:.1f}" class="threshold"/>')
        out.append(txt(770, ly, lab, f"threshlbl {cls}", "start", dy=4))
    return ''.join(out)+'</svg>'
c8 = coststack()

# ============================================================
# PAGE
# ============================================================
CSS = """
:root{
  --paper:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --border:rgba(11,11,11,.10);
  --c1:#2a78d6; --c2:#eb6834; --c3:#1baf7a; --c4:#eda100; --c5:#e87ba4;
  --k1:#2a78d6; --k2:#eb6834; --k3:#1baf7a; --k4:#eda100;
  --q1:#184f95; --q2:#3987e5; --q3:#86b6ef;
  --wash1:rgba(42,120,214,.07); --wash2:rgba(27,175,122,.10); --wash3:rgba(235,104,52,.08);
  --washRisk:rgba(227,73,72,.07);
  --band:rgba(137,135,129,.16); --ghost:rgba(137,135,129,.35);
  --tipbg:#0b0b0b; --tipink:#fcfcfb;
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    --paper:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,.10);
    --c1:#3987e5; --c2:#d95926; --c3:#199e70; --c4:#c98500; --c5:#d55181;
    --k1:#3987e5; --k2:#d95926; --k3:#199e70; --k4:#c98500;
    --q1:#184f95; --q2:#3987e5; --q3:#86b6ef;
    --wash1:rgba(57,135,229,.10); --wash2:rgba(25,158,112,.13); --wash3:rgba(217,89,38,.12);
    --washRisk:rgba(230,103,103,.10);
    --band:rgba(137,135,129,.22); --ghost:rgba(137,135,129,.4);
    --tipbg:#fcfcfb; --tipink:#0b0b0b;
  }
}
:root[data-theme="dark"]{
  --paper:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,.10);
  --c1:#3987e5; --c2:#d95926; --c3:#199e70; --c4:#c98500; --c5:#d55181;
  --k1:#3987e5; --k2:#d95926; --k3:#199e70; --k4:#c98500;
  --q1:#184f95; --q2:#3987e5; --q3:#86b6ef;
  --wash1:rgba(57,135,229,.10); --wash2:rgba(25,158,112,.13); --wash3:rgba(217,89,38,.12);
  --washRisk:rgba(230,103,103,.10);
  --band:rgba(137,135,129,.22); --ghost:rgba(137,135,129,.4);
  --tipbg:#fcfcfb; --tipink:#0b0b0b;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;}
.wrap{max-width:1080px;margin:0 auto;padding:40px 28px 80px}
.masthead{border-bottom:3px solid var(--ink);padding-bottom:22px;margin-bottom:8px}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);margin:0 0 10px}
h1{font-family:Georgia,"Times New Roman",serif;font-size:clamp(30px,4.6vw,46px);line-height:1.08;margin:0 0 12px;text-wrap:balance}
.dek{font-size:17px;color:var(--ink2);max-width:62ch;margin:0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:26px 0 8px}
.kpi{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.kpi .v{font-size:24px;font-weight:700;letter-spacing:-.01em}
.kpi .l{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink2);margin-bottom:4px}
.kpi .s{font-size:12.5px;color:var(--muted);margin-top:3px}
section{margin-top:46px}
.secno{font-size:12px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase}
h2{font-family:Georgia,"Times New Roman",serif;font-size:26px;margin:4px 0 8px;text-wrap:balance}
.take{font-size:16.5px;color:var(--ink);max-width:74ch;margin:0 0 6px}
.take b{background:linear-gradient(transparent 65%, var(--wash1) 65%)}
.note{font-size:14px;color:var(--ink2);max-width:78ch;margin:6px 0 14px}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px 14px 10px;overflow-x:auto}
.chart{width:100%;height:auto;display:block;min-width:720px}
.src{font-size:12px;color:var(--muted);margin:8px 4px 0}
.duo{display:grid;grid-template-columns:1fr;gap:14px}
@media(min-width:900px){.duo.cols{grid-template-columns:3fr 2fr}}
/* svg */
text{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.tick{font-size:12.5px;fill:var(--muted)}
.axisline{stroke:var(--axis);stroke-width:1.5}
.grid{stroke:var(--grid);stroke-width:1}
.stem{stroke:var(--axis);stroke-width:1.5}
.threshold{stroke:var(--ink2);stroke-width:1.6;stroke-dasharray:5 4}
.threshlbl{font-size:12px;fill:var(--ink2);font-weight:600}
.gapline{stroke:var(--ink);stroke-width:1.4}
.gaplbl{font-size:15px;font-weight:700;fill:var(--ink)}
.dot{stroke:var(--surface);stroke-width:2}
.dot.c1{fill:var(--c1)} .dot.c2{fill:var(--c2)} .dot.c3{fill:var(--c3)} .dot.c4{fill:var(--c4)} .dot.c5{fill:var(--c5)} .dot.ink{fill:var(--ink2)}
.dot.hollow{fill:var(--surface)}
.dot.hollow.c1{stroke:var(--c1);stroke-width:2.5} .dot.hollow.c3{stroke:var(--c3);stroke-width:2.5} .dot.hollow.ink{stroke:var(--ink2);stroke-width:2.5}
.bar.c1{fill:var(--c1)} .bar.c2{fill:var(--c2)} .bar.c3{fill:var(--c3)} .bar.c4{fill:var(--c4)} .bar.c5{fill:var(--c5)}
.bar.k1{fill:var(--k1)} .bar.k2{fill:var(--k2)} .bar.k3{fill:var(--k3)} .bar.k4{fill:var(--k4)}
.bar.q1{fill:var(--q1)} .bar.q2{fill:var(--q2)} .bar.q3{fill:var(--q3)}
.bar.ghost{fill:var(--ghost)}
.itemname{font-size:13px;font-weight:600;fill:var(--ink)}
.itemname.big{font-size:14.5px;font-weight:800}
.itemsub{font-size:11.5px;fill:var(--muted)}
.legendlbl{font-size:12.5px;fill:var(--ink2)}
.stacklbl{font-size:12px;fill:#fff;font-weight:600;text-anchor:middle}
.bar.q3+text.stacklbl{fill:var(--ink)}
.zone{fill:none}
.zone.zone1{fill:var(--wash1)} .zone.zone2{fill:var(--wash2)} .zone.zone3{fill:var(--wash3)} .zone.zoneRisk{fill:var(--washRisk)}
.zonelbl{font-size:11.5px;letter-spacing:.08em;fill:var(--ink2);font-weight:700;text-transform:uppercase}
.quad{font-size:13.5px;letter-spacing:.08em;fill:var(--ink);font-weight:800}
.quadRisk{font-size:13.5px;letter-spacing:.08em;fill:var(--ink2);font-weight:800}
.cap{font-size:12.5px;fill:var(--muted)}
.band{fill:var(--band)}
.line{fill:none;stroke-width:2.5;stroke-linejoin:round}
.line.seasons{stroke:var(--c1)}
.line.pencil{stroke:var(--ink2);stroke-dasharray:6 5;stroke-width:2}
.seriesnote{font-size:12.5px;fill:var(--ink2);font-weight:600}
.seriesval{font-size:14px;fill:var(--ink);font-weight:700}
.c1t{fill:var(--c1)} .c3t{fill:var(--c3)}
.hovercol{fill:transparent}
.hovercol:hover{fill:var(--wash1)}
[data-tip]{cursor:default}
#tip{position:fixed;z-index:50;background:var(--tipbg);color:var(--tipink);font-size:13px;
  padding:7px 11px;border-radius:8px;pointer-events:none;opacity:0;transition:opacity .12s;max-width:340px}
@media (prefers-reduced-motion:reduce){#tip{transition:none}}
table{border-collapse:collapse;width:100%;font-size:13.5px;background:var(--surface)}
th,td{border:1px solid var(--grid);padding:7px 10px;text-align:right;font-variant-numeric:tabular-nums}
th:first-child,td:first-child{text-align:left}
thead th{background:var(--wash1);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
.swatch{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:7px;vertical-align:baseline}
.footer{margin-top:52px;padding-top:18px;border-top:1px solid var(--grid);font-size:13px;color:var(--muted)}
.footer p{max-width:90ch}
"""

JS = """
<script>
(function(){
  var tip=document.getElementById('tip');
  document.querySelectorAll('[data-tip]').forEach(function(el){
    el.addEventListener('mousemove',function(e){
      tip.textContent=el.getAttribute('data-tip');
      tip.style.opacity=1;
      var x=Math.min(e.clientX+14, window.innerWidth-tip.offsetWidth-10);
      var y=e.clientY+16; if(y+tip.offsetHeight>window.innerHeight-8) y=e.clientY-tip.offsetHeight-10;
      tip.style.left=x+'px'; tip.style.top=y+'px';
    });
    el.addEventListener('mouseleave',function(){tip.style.opacity=0;});
  });
})();
</script>
"""

def sw(c): return f'<span class="swatch" style="background:var(--{c})"></span>'

html = f"""<title>Seasons Pencil Test</title>
<style>{CSS}</style>
<div id="tip" role="tooltip"></div>
<div class="wrap">

<header class="masthead">
  <p class="eyebrow">Milestone · Boise MSA underwriting brief · August 13, 2026</p>
  <h1>Seasons at Meridian and the price of new supply</h1>
  <p class="dek">Five interlocking books — our Seasons bid, our Prelude acquisition, the Canyon Ridge award,
  and the Emblem &amp; Hawkins development equity raises — drawn as one picture. Every figure re-derived from
  the source models (59/59 checks passed).</p>
  <div class="kpis">
    <div class="kpi"><div class="l">Seasons bid</div><div class="v">$118M</div><div class="s">$327.8K/unit · $351.5/SF · 5.00% Y1 NOI cap</div></div>
    <div class="kpi"><div class="l">vs replacement cost</div><div class="v">+7.6%</div><div class="s">above Emblem's $304.5K/unit build cost</div></div>
    <div class="kpi"><div class="l">vs replacement value</div><div class="v">−8.4%</div><div class="s">below the ~$357.7K that induces new supply</div></div>
    <div class="kpi"><div class="l">Rent gap to pencil</div><div class="v">−7 to −10%</div><div class="s">below the 6.5%-ROC rent, entire hold</div></div>
    <div class="kpi"><div class="l">Exit sensitivity</div><div class="v">$400.6K @ 5.00%</div><div class="s">$382K @ 5.25% · $365K @ 5.50% — each 25bp ≈ 90bp UIRR</div></div>
  </div>
</header>

<section>
  <p class="secno">01 · Price</p>
  <h2>The window between cost and replacement value</h2>
  <p class="take"><b>$327.8K/unit is above what it costs to build — and below what it takes to get paid for building.</b></p>
  <p class="note">"Below replacement cost" is not our story: the bid sits 7.6% above Emblem's all-in budget. The defensible claim
  is the window — above raw cost, below the ~$357.7K/unit stabilized value a developer must believe in before starting
  (Emblem's own untrended NOI at their own 5.5% exit cap), and well below the live Canyon Ridge award.</p>
  <div class="panel">{c1}</div>
  <p class="src">Sources: TMG Seasons model (Assumptions), Emblem merchant model (Summary), Canyon Ridge model at award, Prelude closing model.</p>
</section>

<section>
  <p class="secno">02 · Rents today</p>
  <h2>Every new build must underwrite above us</h2>
  <p class="take"><b>Seasons' $2.02/SF market rent sits below the pencil line — and below both developers' own underwriting.</b></p>
  <p class="note">At today's costs a new project needs ~$2.17/SF to reach a 6.5% untrended return on cost — and ~$2.30/SF if it
  carries Seasons-like (garden, modest-fee) income instead of Emblem's garage-and-wifi program. New supply cannot undercut us;
  it can only deliver above us. Both books confirm it: Emblem's comp table shows Seasons as the <em>lowest</em> $/SF of its five comps.</p>
  <div class="panel">{c2}</div>
  <p class="src">Rents from each model's own underwriting; pencil rents solved on Emblem's operating model &amp; cost basis (their 5.87% vacancy stack, opex, other income).</p>
</section>

<section>
  <p class="secno">03 · Rents through the hold</p>
  <h2>The gap never closes — by our own underwriting</h2>
  <p class="take"><b>Seasons' modeled rent stays 7–10% below the 6.5% pencil rent every year of the hold, freezing at −7.4% as
  rent growth converges to cost inflation.</b> It never even crosses the 6.0% line.</p>
  <p class="note">Costs, opex and developer income all escalate 3%/yr (the developers' own assumption); our rent path is the model's
  (7.6% Y1, then 4/4/3.5/3.5/3). The exit buyer in Oct-2031 still inherits a market where development doesn't pencil at our rents —
  Emblem's own model needs $2,443/mo that year, 8% above our exit-year $2,249.</p>
  <div class="panel">{c3}</div>
  <p class="src">Corrected in the 2026-08-13 verification pass (an earlier draft compared Y6 rents to a 2031 pencil, understating the exit gap as −4.3%).</p>
</section>

<section>
  <p class="secno">04 · Exits</p>
  <h2>Same exit price, different anatomy</h2>
  <p class="take"><b>Our Seasons exit ($400.6K) matches Emblem's required sale ($400.5K) — but that is not a validation:
  it means 7-year-old product selling at the same $/unit as brand-new product.</b> The match is manufactured by the cap
  rates — our exit NOI is 8.9% <em>below</em> the new build's ($20.1K vs $22.0K/unit); the equality comes from assuming
  aged product trades 50bp tighter (5.00%) in 2031 than the merchant assumes new product does in 2030 (5.50%).</p>
  <p class="note">The vintage discount is real, and it lives in the NOI: our exit rents sit 8% below Emblem's own 2031 rent —
  the same relative position as today. The exposure is the cap-rate <em>level</em>. For 5.00%: today's prints show age-flat caps
  for young vintages (Prelude closed at 4.95% at 8 years old; CR 5.12% tax-adjusted) and merchant books pad exit caps for LP
  optics. Against: a stabilized no-story 7-year-old argues for the wider end of any curve. Sensitivity (rebuilt from the model's
  cash flows): 5.25% → $382K/unit, UIRR ~7.8% / LIRR ~10.0%; 5.50% (Emblem's own) → $365K, UIRR ~6.9% / LIRR ~8.0%.
  $382K in 2031 is what 2-year-old Canyon Ridge fetches today — the most defensible aged-product anchor. Present the exit
  as a 5.00–5.25% band.</p>
  <div class="panel">{c4}</div>
  <p class="src">Exit values from each model. Forward replacement cost = Emblem $304.5K/unit escalated 3%/yr to 2031.</p>
</section>

<section>
  <p class="secno">05 · Two moats</p>
  <h2>What Canyon Ridge's price actually buys</h2>
  <p class="take"><b>Canyon Ridge's rents already pencil — its protection is that there's no land. Seasons' land is abundant —
  its protection is that the rents don't pencil.</b> The market just paid +$54K/unit and ~45bp for the physical version.</p>
  <div class="panel">{c7}</div>
  <p class="src">Land inventory from this repo's parcel-level analysis (5-mi radii; MF-zoned or comp-plan multifamily, ≥1 ac, developable).</p>
</section>

<section>
  <p class="secno">06 · Taxes</p>
  <h2>Same product, $2,100/unit apart on taxes</h2>
  <p class="take"><b>Meridian's ~0.45% levy vs Boise's ~0.92% is worth ≈ $42K/unit of capitalized value at a 5% cap — and it flips
  the cap-rate comparison.</b> Tax-normalized, the Canyon Ridge buyer is accepting a thinner real-estate yield than our Seasons bid.
  The Judy's marketed 6.52% ROC also rests on a Boise tax line ~$1,000/unit light.</p>
  <div class="duo cols">
    <div class="panel">{c5a}</div>
    <div class="panel">{c5b}<p class="note" style="margin:0 8px 8px">Y1 NOI cap rates. Adding the Meridian-vs-Boise
    tax difference back to Canyon Ridge's NOI moves its cap from 4.57% to 5.12% — wider than Seasons' 5.00%.
    Idaho is a non-disclosure state; all three TMG models reassess at 95% of price.</p></div>
  </div>
  <p class="src">Tax lines from each model's Y1/stabilized pro forma; levies implied by actuals (Seasons &amp; Prelude 0.4507%; Canyon Ridge 0.92%).</p>
</section>

<section>
  <p class="secno">07 · Other income</p>
  <h2>Other income is a product choice — and a quiet stretch</h2>
  <p class="take"><b>Developers underwrite $3.6–4.2K/unit of non-rent income; stabilized assets in this market actually collect
  $2.7–3.0K.</b> The delta is garages and mandatory wifi — product that also raises their build cost — plus recovery-rate optimism.</p>
  <p class="note">Correcting other income toward market pushes true pencil rents even higher (a wider moat), and Prelude's $759/unit of
  garage income against Seasons' $360 flags a possible revenue-capture opportunity at Seasons worth a diligence look.</p>
  <div class="panel">{c6}</div>
  <p class="src">Per-unit per-year. Seasons/CR from TMG Y1; Prelude from our closing UW; Emblem from Operating Inputs (garage $41/space on 536 spaces, wifi $108/mo, 100% W/S billback); Judy total from Y3 pro forma.</p>
</section>

<section>
  <p class="secno">08 · Cost anatomy</p>
  <h2>What a unit costs to build — and where prices sit against it</h2>
  <p class="take"><b>Two independent GCs land on the same hard cost (~$214–216/SF). The differences are land basis, fees, and soft
  costs</b> — which is why Hawkins' $257K is a floor that doesn't generalize, and Emblem's $305K is the institutional benchmark.</p>
  <div class="panel">{c8}</div>
  <p class="src">Emblem: Summary tab budget at Oct-27 GMP. Hawkins: S&amp;U (land at Oct-2024 purchase basis, no mark-to-market). Lines: Seasons bid; replacement value; Canyon Ridge award.</p>
</section>

<section>
  <p class="secno">Appendix</p>
  <h2>The five books, one table</h2>
  <div class="panel" style="padding:0;overflow-x:auto">
  <table>
    <thead><tr><th>Deal</th><th>Role</th><th>Units</th><th>$/unit</th><th>$/SF</th><th>Rent /mo</th><th>Rent /SF</th><th>Yield</th><th>Exit $/unit</th><th>Exit cap</th><th>Taxes /u</th><th>Other inc /u</th></tr></thead>
    <tbody>
      <tr><td>{sw('c1')}Seasons at Meridian (bid)</td><td>Target · 2024</td><td>360</td><td>$327.8K</td><td>$351.5</td><td>$1,885</td><td>$2.02</td><td>5.00% Y1</td><td>$400.6K</td><td>5.00%</td><td>$1,340</td><td>$2,736</td></tr>
      <tr><td>{sw('c2')}Prelude at Paramount (own)</td><td>Owned · 2018</td><td>280</td><td>$284.8K</td><td>$280.2</td><td>$1,730</td><td>$1.70</td><td>4.95% Y1</td><td>$361.2K</td><td>5.00%</td><td>$1,169</td><td>$2,803</td></tr>
      <tr><td>{sw('c3')}Canyon Ridge (award)</td><td>Comp · 2024</td><td>288</td><td>$381.9K</td><td>$429.7</td><td>$2,171</td><td>$2.44</td><td>4.57% Y1</td><td>$442.8K</td><td>4.75%</td><td>$3,428</td><td>$3,002</td></tr>
      <tr><td>{sw('c4')}Emblem Meridian (Quarterra)</td><td>Dev · 2028–29</td><td>256</td><td>$304.5K cost</td><td>$324.3</td><td>$2,069</td><td>$2.20</td><td>6.65% ROC</td><td>$400.5K</td><td>5.50%</td><td>$1,501</td><td>$4,207</td></tr>
      <tr><td>{sw('c5')}The Judy / MGO (Hawkins)</td><td>Dev · 2027–28</td><td>162</td><td>$257.4K cost</td><td>$283.5</td><td>$1,787</td><td>$1.97</td><td>6.52% ROC*</td><td>$361.6K</td><td>5.25%</td><td>$2,203*</td><td>$3,568</td></tr>
    </tbody>
  </table>
  </div>
  <p class="src">*As marketed; ~6.15% ROC and ~$3,161/unit at the Boise levy on 95% of their own exit value.
  Yields: TMG deals = Y1 NOI ÷ price; developments = untrended return on cost (sponsor convention).</p>
</section>

<div class="footer">
  <p><strong>Method.</strong> All model figures re-extracted programmatically from the five source workbooks and re-verified 2026-08-13
  (59/59 checks). Pencil rents solve Emblem's operating pro forma for the base rent required at a target untrended return on cost,
  holding their vacancy stack, opex, and other income; all components escalate 3%/yr. Land inventory from this repo's
  parcel-level land-use pipeline. Companion knowledge base: <em>knowledge/Seasons-Meridian-Replacement-Cost-and-Supply-Economics.md</em>
  and <em>knowledge/deal_metrics.json</em>.</p>
  <p>Confidential — internal underwriting work product. Not for distribution.</p>
</div>

</div>
{JS}
"""

open('seasons-pencil-test.html','w').write(html)
print("written", len(html), "bytes")
