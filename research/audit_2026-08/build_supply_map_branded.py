#!/usr/bin/env python3
"""Rebuild the Seasons at Meridian supply map on the ORIGINAL branded template.

Takes the prior skill-built map (--template) verbatim — Milestone navy header,
magenta subject star, gold ring, white-ringed numbered pins — and swaps in the
current roster (supply_map_data.json), preserving the original CoStar-exact
coordinates wherever a property name matches the old PINS array.
Shadow watch sites render as purple dots, documented-dead sites as gray dots.
"""
import json, re, sys, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUCKET = {
    'STABILIZED / STABILIZING': ('Stabilized / stabilizing', '#2E75B6'),
    'LEASING UP': ('Leasing up', '#ED7D31'),
    'UNDER CONSTRUCTION': ('Under construction', '#2FB344'),
    'PROPOSED': ('Proposed pipeline', '#FF0000'),
    'SHADOW': ('Shadow / latent supply', '#7C4DFF'),
    'DEAD': ('Documented dead', '#6F6F70'),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True)
    ap.add_argument('--data', default=str(HERE / 'supply_map_data.json'))
    ap.add_argument('--out', default='/home/user/Boise-Deals/SeasonsMeridian/Seasons at Meridian - Supply Map.html')
    a = ap.parse_args()

    t = Path(a.template).read_text()
    data = json.loads(Path(a.data).read_text())

    old_pins = json.loads(re.search(r'const PINS = (\[.*?\]);\n', t, re.S).group(1))
    old_xy = {p['name']: (p['lat'], p['lng']) for p in old_pins if p.get('num') not in ('S',)}
    subj = data['subject']

    pins = [{
        'num': 'S', 'name': subj['name'], 'bucket': 'SUBJECT', 'color': '#FF00E5',
        'lat': subj['lat'], 'lng': subj['lon'], 'units': 360, 'deliver': 'Q3 2024 (built)',
        'occ': 96, 'rent': 1911, 'owner': 'The Carlyle Group / Morgan Stonehill',
        'typ': 'Garden', 'dist': 0.0, 'notes': 'Subject property — the underwriting target.'}]
    leg = {}
    for d in sorted(data['deals'], key=lambda x: x['row']):
        label, color = BUCKET[d['bucket']]
        xy = old_xy.get(d['name'], (d['lat'], d['lon']))
        occ = d.get('occ')
        occ = int(occ.rstrip('%')) if isinstance(occ, str) and occ.endswith('%') else occ
        pins.append({'num': d['row'], 'name': d['name'], 'bucket': label, 'color': color,
                     'lat': xy[0], 'lng': xy[1], 'units': d.get('units'),
                     'deliver': d.get('est_delivery') or 'TBD', 'occ': occ, 'rent': None,
                     'owner': d.get('owner') or '—', 'typ': d.get('type') or '—',
                     'dist': d.get('dist'), 'notes': d.get('note') or ''})
        k = d['bucket']
        leg.setdefault(k, [0, 0])
        leg[k][0] += 1
        leg[k][1] += int(d.get('units') or 0)
    for s in data.get('shadow', []):
        label, color = BUCKET[s['bucket']]
        pins.append({'num': '•', 'name': s['name'], 'bucket': label, 'color': color,
                     'lat': s['lat'], 'lng': s['lon'], 'units': s.get('units'),
                     'deliver': None, 'occ': None, 'rent': None, 'owner': '—', 'typ': '—',
                     'dist': None, 'notes': s.get('note') or ''})

    leg_rows = [{'key': k.lower()[:5], 'color': BUCKET[k][1], 'label': BUCKET[k][0],
                 'n': v[0], 'u': v[1]} for k, v in leg.items()]
    n_shadow = sum(1 for s in data.get('shadow', []) if s['bucket'] == 'SHADOW')
    n_dead = sum(1 for s in data.get('shadow', []) if s['bucket'] == 'DEAD')

    pins_js = 'const PINS = ' + json.dumps(pins) + ';\n'
    leg_js = 'const LEG = ' + json.dumps(leg_rows) + ';'
    t = re.sub(r'const PINS = \[.*?\];\n', lambda m: pins_js, t, count=1, flags=re.S)
    t = re.sub(r'const LEG = \[.*?\];', lambda m: leg_js, t, count=1, flags=re.S)
    t = t.replace('const HAS_SHADOW = false;', 'const HAS_SHADOW = true;')
    # legend: add dead row next to the shadow row
    t = t.replace(
        '${HAS_SHADOW?`<div class="row"><span class="dot" style="background:#7C4DFF"></span>Shadow / latent supply</div>`:\'\'}',
        '${HAS_SHADOW?`<div class="row"><span class="dot" style="background:#7C4DFF"></span>Shadow / latent supply (' + str(n_shadow) + ')</div>'
        '<div class="row"><span class="dot" style="background:#6F6F70"></span>Documented dead — incl. the denied Seasons II site (' + str(n_dead) + ')</div>`:\'\'}')
    # --- replace the flat marker loop with per-bucket toggleable layer groups
    marker_block = re.search(r'const bounds = \[\];.*?map\.fitBounds\(bounds,\{padding:\[60,60\]\}\);', t, re.S)
    toggle_js = """const bounds = [];
const GROUPS = {};
function iconFor(p){
  if(p.num==='S') return L.divIcon({className:'', html:`<div class="pin sub">\\u2605</div>`, iconSize:[44,44], iconAnchor:[22,38]});
  if(p.num==='\\u2022') return L.divIcon({className:'', html:`<div class="pin" style="background:${p.color};width:16px;height:16px;font-size:9px;opacity:.9;"></div>`, iconSize:[16,16], iconAnchor:[8,8]});
  return L.divIcon({className:'', html:`<div class="pin" style="background:${p.color};width:25px;height:25px;font-size:12px;">${p.num}</div>`, iconSize:[25,25], iconAnchor:[13,13]});
}
PINS.forEach(p=>{
  bounds.push([p.lat,p.lng]);
  const m = L.marker([p.lat,p.lng],{icon:iconFor(p), zIndexOffset:p.num==='S'?1000:0}).bindPopup(popup(p));
  const key = p.num==='S' ? '\\u2605 Subject' : p.bucket;
  (GROUPS[key] = GROUPS[key] || L.layerGroup()).addLayer(m);
});
Object.values(GROUPS).forEach(g=>g.addTo(map));
const overlays = {};
Object.keys(GROUPS).forEach(k=>{
  const col = (PINS.find(p=>(p.num==='S'?'\\u2605 Subject':p.bucket)===k)||{}).color || '#888';
  overlays[`<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${col};margin-right:4px;"></span>${k}`] = GROUPS[k];
});
L.control.layers(null, overlays, {collapsed:false, position:'topleft'}).addTo(map);
map.fitBounds(bounds,{padding:[60,60]});"""
    t = t[:marker_block.start()] + toggle_js + t[marker_block.end():]

    n_deals = len(data['deals'])
    t = re.sub(r'<div class="sub">.*?</div>',
               f'<div class="sub">{n_deals + 1} competitive properties (2022&ndash;2029) · numbered to the Aug 14 2026 supply chart · purple = shadow watch · gray = documented dead · click any pin</div>',
               t, count=1, flags=re.S)
    t = re.sub(r'<footer>.*?</footer>',
               '<footer>Companion to <b>Seasons at Meridian - Supply Chart.xlsx</b> (rev. Aug 14 2026, blind-spot audit). '
               'Positions: CoStar lat/lon where available, else Ada County parcel centroids; shadow/dead pins at named sites or intersections (approx where noted). '
               'Distance is straight-line from the subject.</footer>', t, count=1, flags=re.S)
    Path(a.out).write_text(t)
    print('wrote', a.out, len(t), 'bytes;', len(pins), 'pins;',
          f'{sum(1 for n in old_xy if any(p["name"]==n for p in pins))} CoStar-coord matches')

if __name__ == '__main__':
    main()
