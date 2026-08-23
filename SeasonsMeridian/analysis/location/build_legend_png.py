#!/usr/bin/env python3
"""Render 'Seasons at Meridian - Location Map Legend.png' — the map legend as a
standalone TMG-exec-format exhibit (write-up above, map middle, this below).
Reads the same poi_data.py the map is built from, so numbering always matches."""
import pathlib, html as H
from poi_data import CATEGORIES, POIS, ROADS

# Legend-only condensed descriptions (the interactive map keeps the full notes).
SHORTS = {
  "Eagle View Landing": "Ahlquist campus, Overland Rd to I-84: ICCU Building, POWER building, Topgolf, Hyatt Place + Holiday Inn, Norco HQ. Combined node: 49 tenants \u226510K SF / ~4,900 jobs; 914K SF of offices built since 2020 within 1.25 mi.",
  "Silverstone Business Campus": "~90-ac park south of Overland: T-Mobile call center (~500 jobs), Amazon's PillPack pharmacy (~548), UPS, Disco Hi-Tec America.",
  "St. Luke's Meridian": "550,000-SF full-service hospital (Level IV trauma, Level II NICU); the subject's #1 resident employer.",
  "POWER Engineers HQ bldg": "150K-SF office (2023); POWER Engineers took 90K SF in Aug 2025.",
  "El Dorado Business Campus": "85-ac office/medical campus directly across from the subject: Cottonwood Creek Behavioral Hospital (2025), Veranda Plaza & Catalina Place medical.",
  "ICOM medical school": "Idaho College of Osteopathic Medicine \u2014 $34M / 94K-SF campus, 220+ seats/class, growing toward ~650 students.",
  "ISU Meridian Health Science Center": "ISU's Treasure Valley health-sciences campus (pharmacy, PA, nursing, dental).",
  "West Ada School District HQ": "HQ of Idaho's largest school district (~39K students).",
  "Scentsy Commons (HQ)": "70-acre HQ campus; ~1,100 employees.",
  "Blue Cross of Idaho HQ": "238K-SF HQ; ~600-850 employees.",
  "Franklin\u2013Pine employment corridor": "Rail-served industrial/flex corridor, Franklin Rd to Pine: 68 tenants \u226510K SF / ~5,400 jobs (incl. Scentsy & Blue Cross) \u2014 Albertsons' 253K-SF DC, Shamrock Foods, RC Willey, Coca-Cola.",
  "Micron \u2014 Meridian facility": "61K SF, ~300 employees \u2014 in-ring Micron operations; the subject's #3 resident employer.",
  "Touchmark / Meadow Lake Village (master-plan refresh)": "121-ac master plan being rewritten (H-2025-0012): medical office, ~126-room hotel, retail + ~500 proposed apartments (tracked as shadow supply); nothing permitted.",
  "Ten Mile Crossing": "I-84 & Ten Mile business park: Paylocity, AmeriBen (2nd bldg underway), Scheels, 270K-SF medical office complex.",
  "The District at Ten Mile (UC)": "220-ac mixed-use, broke ground May 2026: Target (May 2027), $50.7M Life Time (spring 2027), In-N-Out, hotels.",
  "Amazon DID3 delivery station": "180K-SF last-mile delivery station; FedEx Ground adjacent.",
  "The Village at Meridian": "~1M-SF lifestyle center: Village Cinema, Idaho's first In-N-Out; 80K-SF Phase II opens Sept 2026\u2013Feb 2027 (The Capital Grille, Williams Sonoma, Pottery Barn...).",
  "Scheels (2024)": "240K-SF flagship (Apr 2024) \u2014 Idaho's largest sporting-goods store; ~500 employees.",
  "WinCo Foods (24-hr)": "Nearest full grocery, open 24 hours.",
  "Adjacent 18-ac retail site (WinCo-owned)": "Touches the subject's west line; WinCo-owned, marketed for big-box + pad ground leases; nothing permitted (the denied 'Seasons II' parcel).",
  "Costco (Boise, Cole Rd)": "Nearest Costco \u2014 straight shot east on Overland/I-84.",
  "Hawkins big-box site (proposed)": "~150K-SF warehouse retailer + fuel proposed at I-84 & Meridian Rd (tenant undisclosed); watch item.",
  "Topgolf": "Idaho's first Topgolf (2022) \u2014 walkable from the subject.",
  "Cinemark Majestic Cinemas": "69K-SF multiplex, a 0.4-mi walk from the subject.",
  "Roaring Springs & Wahooz": "The Northwest's largest waterpark + Wahooz family fun center \u2014 on the subject's own road, 2 mi west.",
  "The Flying Pickle": "Idaho's largest indoor pickleball club \u2014 18 courts + restaurant (2023).",
  "Urban Air Adventure Park": "Indoor trampoline/adventure park.",
  "JumpTime Meridian": "Trampoline park \u2014 with Urban Air and Flying Pickle, the warehouse belt doubles as a family-entertainment strip.",
  "Mountain View High School (assigned)": "Zoned high school (verified vs West Ada GIS) \u00b7 2,463 students \u00b7 GreatSchools 8/10.",
  "Lewis & Clark Middle School (assigned)": "Zoned middle school (verified) \u00b7 ~900 students \u00b7 GreatSchools 7/10.",
  "Pepper Ridge Elementary (assigned)": "Zoned elementary (verified) \u00b7 GreatSchools 8/10 / Niche A-.",
  "The Goddard School of Meridian": "Idaho's first Goddard School \u2014 premium preschool, 2 minutes from the subject.",
  "Primrose School of South Meridian": "New national-brand preschool (opened late 2025).",
  "Cole Valley Christian (private)": "Private K-12 option.",
  "Julius M. Kleiner Park": "58-acre flagship park: amphitheater, splash pad, ponds, pickleball.",
  "Bear Creek Park": "19-acre neighborhood park.",
  "Storey Park & Bark Park": "14-acre park + 2.25-acre dog park.",
  "Downtown Boise": "~15 min via I-84/I-184 \u2014 state capital + Simplot, Idaho Power and Clearwater Analytics HQs.",
  "Boise Airport (BOI)": "~14 min east on I-84.",
  "Boise State University": "~20 min.",
  "Saint Alphonsus Regional Medical Center": "Trinity Health's Idaho flagship (~6,000+ system employees); the subject's #2 resident employer.",
  "Micron Boise campus": "$50B ID1/ID2 fab buildout (first wafers 2027/2028, ~3,500 direct jobs) + reported $10B research campus; ~15 min via I-84.",
  "Meta Kuna data center": "$800M / 960K-SF data center, completion expected end of 2026.",
}
ROAD_SHORTS = {
  "I-84 \u00b7 132-142K vehicles/day": "The metro's busiest freeway corridor at the subject's interchange (COMPASS); subject sits at Exit 46.",
  "EAGLE RD (SH-55) \u00b7 60-65K vehicles/day": "ITD: Idaho's busiest non-interstate highway; the Eagle/Overland corner carries 76,500+ vehicles/day combined.",
  "Eagle & Fairview \u2014 Idaho's busiest intersection": "Idaho's #1 intersection by traffic count since 2005 (ACHD), 2 mi north.",
}

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent.parent.parent
OUT_HTML = HERE / '_legend_render.html'
OUT_PNG = REPO / 'SeasonsMeridian' / 'Seasons at Meridian - Location Map Legend.png'

# assign numbers exactly like the map builder does
seq = {}
for p in POIS:
    seq[p['cat']] = seq.get(p['cat'], 0) + 1
    p['n'] = seq[p['cat']]

def chip(color, txt, big=False):
    s = 30 if big else 24
    return (f'<span style="display:inline-flex;flex:none;width:{s}px;height:{s}px;border-radius:50%;'
            f'background:{color};color:#fff;font-weight:800;font-size:{15 if big else 13}px;'
            f'align-items:center;justify-content:center;border:2px solid #fff;'
            f'box-shadow:0 0 3px rgba(0,0,0,.35)">{txt}</span>')

blocks = []
# subject block
blocks.append(f'''<div class="item subj">
  <span style="display:inline-flex;flex:none;width:24px;height:24px;border-radius:50%;background:#F2C230;border:3px solid #B02418;box-shadow:0 0 3px rgba(0,0,0,.35)"></span>
  <span class="body"><span class="nm">Seasons at Meridian (subject)</span>
  <div class="ds">2700 E Overland Rd &middot; 360 units &middot; 2024 &middot; SE quadrant of Eagle Rd (SH-55) &amp; I-84.</div></span></div>''')
# road chips
for r in ROADS:
    blocks.append(f'''<div class="item">
  <span class="roadchip">&#9632;</span>
  <span class="body"><span class="nm">{H.escape(r["label"])}</span>
  <div class="ds">{H.escape(ROAD_SHORTS.get(r["label"], r["note"]))}</div></span></div>''')

cat_blocks = []
for c in CATEGORIES:
    items = [p for p in POIS if p['cat'] == c['id']]
    rows = []
    for p in items:
        d = f'<span class="dd">{p["d"]} mi</span>' if p.get('d') else ''
        rows.append(f'''<div class="item">{chip(c["color"], p["n"])}
  <span class="body">{d}<span class="nm">{H.escape(p["name"])}</span>
  <div class="ds">{H.escape(SHORTS.get(p["name"], p.get("note","")))}</div></span></div>''')
    cat_blocks.append(f'''<div class="catblk">
  <div class="cathead"><span class="sw" style="background:{c["color"]}"></span>{H.escape(c["name"]).upper()}</div>
  {''.join(rows)}</div>''')

page = f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap">
<style>
  body {{ margin:0; background:#fff; font-family:'Lato','Segoe UI',Calibri,Arial,sans-serif; color:#1F3864; }}
  .exh {{ width:2360px; padding:26px 30px 24px; }}
  .title {{ font-size:19px; font-weight:900; letter-spacing:.06em; text-transform:uppercase;
    color:#17365D; padding-bottom:8px; border-bottom:2.5px solid #B8C6DC; margin-bottom:14px; }}
  .cols {{ column-count:4; column-gap:26px; }}
  .catblk {{ margin-bottom:9px; }}
  .cathead {{ break-after:avoid; font-size:13px; font-weight:900; letter-spacing:.06em; color:#17365D;
    display:flex; align-items:center; gap:7px; margin:0 0 6px; padding-bottom:3px; border-bottom:1.5px solid #C9D4E4; }}
  .sw {{ width:13px; height:13px; border-radius:50%; border:1.5px solid #fff; box-shadow:0 0 2px rgba(0,0,0,.45); flex:none; }}
  .item {{ display:flex; gap:9px; margin:0 0 5px; break-inside:avoid; }}
  .item.subj {{ margin-bottom:10px; }}
  .body {{ flex:1; line-height:1.25; font-size:13px; }}
  .nm {{ font-weight:900; color:#17365D; font-size:13.5px; }}
  .dd {{ float:right; color:#8592AA; font-size:11.5px; font-weight:700; white-space:nowrap; padding-left:6px; }}
  .ds {{ color:#44567A; font-size:11.5px; margin-top:0; }}
  .roadchip {{ display:inline-flex; flex:none; width:24px; height:24px; border-radius:4px; background:#B02418;
    color:#B02418; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 0 3px rgba(0,0,0,.35); }}
  .foot {{ font-size:11.5px; color:#5A6E92; margin-top:10px; line-height:1.45; border-top:1px solid #C9D4E4; padding-top:8px; }}
</style></head><body>
<div class="exh" id="legend">
  <div class="title">Seasons at Meridian &mdash; Location Map Legend</div>
  <div class="cols">
    <div class="catblk">
      <div class="cathead">SUBJECT &amp; ROAD CALLOUTS</div>
      {''.join(blocks)}
    </div>
    {''.join(cat_blocks)}
  </div>
  <div class="foot">
    Numbers restart at 1 within each colour &mdash; colour first, then number. Distances straight-line from the subject. Verified Aug 23, 2026: ITD/ACHD/COMPASS traffic counts; CoStar (employee counts CoStar-reported); school zones point-in-polygon vs West Ada's own GIS; area outlines = Ada County parcel lines.
  </div>
</div>
</body></html>'''

OUT_HTML.write_text(page)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(device_scale_factor=2, viewport={'width': 2500, 'height': 2200})
    pg.goto(OUT_HTML.resolve().as_uri())
    pg.wait_for_timeout(800)
    pg.locator('#legend').screenshot(path=str(OUT_PNG))
    b.close()
print('wrote', OUT_PNG)
