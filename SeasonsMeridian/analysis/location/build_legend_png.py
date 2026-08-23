#!/usr/bin/env python3
"""Render 'Seasons at Meridian - Location Map Legend.png' — the map legend as a
standalone TMG-exec-format exhibit (write-up above, map middle, this below).
Reads the same poi_data.py the map is built from, so numbering always matches."""
import pathlib, html as H
from poi_data import CATEGORIES, POIS, ROADS

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
  <div class="ds">{H.escape(r["note"])}</div></span></div>''')

cat_blocks = []
for c in CATEGORIES:
    items = [p for p in POIS if p['cat'] == c['id']]
    rows = []
    for p in items:
        d = f'<span class="dd">{p["d"]} mi</span>' if p.get('d') else ''
        rows.append(f'''<div class="item">{chip(c["color"], p["n"])}
  <span class="body">{d}<span class="nm">{H.escape(p["name"])}</span>
  <div class="ds">{H.escape(p.get("note",""))}</div></span></div>''')
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
  .catblk {{ margin-bottom:14px; }}
  .cathead {{ break-after:avoid; font-size:13px; font-weight:900; letter-spacing:.06em; color:#17365D;
    display:flex; align-items:center; gap:7px; margin:0 0 6px; padding-bottom:3px; border-bottom:1.5px solid #C9D4E4; }}
  .sw {{ width:13px; height:13px; border-radius:50%; border:1.5px solid #fff; box-shadow:0 0 2px rgba(0,0,0,.45); flex:none; }}
  .item {{ display:flex; gap:9px; margin:0 0 8px; break-inside:avoid; }}
  .item.subj {{ margin-bottom:10px; }}
  .body {{ flex:1; line-height:1.32; font-size:13px; }}
  .nm {{ font-weight:900; color:#17365D; font-size:13.5px; }}
  .dd {{ float:right; color:#8592AA; font-size:11.5px; font-weight:700; white-space:nowrap; padding-left:6px; }}
  .ds {{ color:#44567A; font-size:12px; margin-top:1px; }}
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
    Numbers restart at 1 within each colour &mdash; read colour first, then number. Distances are straight-line from the subject.
    POIs verified Aug 23, 2026 (ITD/ACHD/COMPASS traffic counts; city, district and press sources; CoStar exports incl. the 3-mi &ge;10K-SF tenant roster &mdash; employee counts are CoStar-reported).
    School assignments verified point-in-polygon against West Ada's own ArcGIS attendance layers (current zones and the adopted 2026-27 redraw agree).
    Area outlines on the map are true parcel lines from the Ada County parcels layer, dissolved per campus.
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
