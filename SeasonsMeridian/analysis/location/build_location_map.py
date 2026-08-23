#!/usr/bin/env python3
"""Build 'Seasons at Meridian - Location Map.html' — a self-contained labeled
location/amenity map (companion to strength H45, Location).

Data sources:
  - in/SaM__CoStar_5mi_AllTypes_New.xls   (CoStar: all property types, built 2020+, 5-mi)
  - in/Boise__CoStar_Tenant_MoveIns_2yrs.xlsx (CoStar: metro tenant move-ins, last 2 yrs)
  - poi_data.py (verified POIs: employment, retail, schools, parks, roads — sourced Aug 2026)
Leaflet is inlined (same vendored build as the Supply Map) so the file is
self-contained; basemap tiles stream from ArcGIS Online like the other viewers.
"""
import json, math, pathlib, re

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent.parent.parent
SUBJ = (43.592029, -116.360847)

from poi_data import CATEGORIES, POIS, ROADS, RINGS_MI, FOOTER_NOTE

def dist_mi(lat, lon):
    dy = (lat - SUBJ[0]) * 69.0
    dx = (lon - SUBJ[1]) * 69.0 * math.cos(math.radians(SUBJ[0]))
    return math.hypot(dx, dy)

def load_newdev():
    import pandas as pd
    df = pd.ExcelFile(HERE / 'in/SaM__CoStar_5mi_AllTypes_New.xls').parse('Export082326')
    df = df[~df['Property Type'].str.contains('Multifamily', na=False)]
    df = df[df['Building Status'].isin(['Existing', 'Under Construction'])]
    df['RBA'] = pd.to_numeric(df['RBA'], errors='coerce')
    df = df[df['RBA'] >= 20000].dropna(subset=['Latitude', 'Longitude'])
    out = []
    for _, r in df.iterrows():
        name = r['Property Name'] if isinstance(r['Property Name'], str) else r['Property Address']
        typ = str(r['Property Type']).split(' (')[0]
        out.append({
            'n': name, 'a': r['Property Address'], 't': typ,
            'st': r['Building Status'], 'sf': int(r['RBA']), 'yr': int(r['Year Built']),
            'lat': round(float(r['Latitude']), 6), 'lon': round(float(r['Longitude']), 6),
            'd': round(dist_mi(r['Latitude'], r['Longitude']), 2),
        })
    out.sort(key=lambda x: -x['sf'])
    return out

def main():
    newdev = load_newdev()
    supply_map = (REPO / 'SeasonsMeridian' / 'Seasons at Meridian - Supply Map.html').read_text()
    i = supply_map.find('!function(t,e){"object"==typeof exports')
    j = supply_map.find('</script>', i)
    leaflet_js = supply_map[i:j]
    m = re.search(r'<style[^>]*>(.*?)</style>', supply_map, re.S)
    leaflet_css = m.group(1)
    # keep only the vendored leaflet core rules from that style block
    k = leaflet_css.find('.leaflet-')
    leaflet_css = leaflet_css[k:leaflet_css.find('/* custom */')] if '/* custom */' in leaflet_css else leaflet_css[k:]

    html = TEMPLATE
    html = html.replace('__LEAFLET_CSS__', leaflet_css)
    html = html.replace('__LEAFLET_JS__', leaflet_js)
    html = html.replace('__SUBJ__', json.dumps(SUBJ))
    html = html.replace('__CATS__', json.dumps(CATEGORIES))
    html = html.replace('__POIS__', json.dumps(POIS))
    html = html.replace('__ROADS__', json.dumps(ROADS))
    html = html.replace('__RINGS__', json.dumps(RINGS_MI))
    html = html.replace('__NEWDEV__', json.dumps(newdev))
    html = html.replace('__FOOTER__', FOOTER_NOTE)
    out = REPO / 'SeasonsMeridian' / 'Seasons at Meridian - Location Map.html'
    out.write_text(html)
    print('wrote', out, f'{out.stat().st_size/1024:.0f} KB', f'({len(POIS)} POIs, {len(newdev)} new-dev pins)')

TEMPLATE = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seasons at Meridian — Location Map</title>
<style>__LEAFLET_CSS__</style>
<style>
  html,body{height:100%;margin:0;font-family:'Segoe UI',Lato,Calibri,Arial,sans-serif}
  #wrap{display:flex;height:100%;flex-direction:column}
  header{background:#17365D;color:#fff;padding:10px 18px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  header h1{font-size:17px;margin:0;letter-spacing:.04em}
  header .sub{font-size:12.5px;color:#B8C6DC}
  #main{flex:1;display:flex;min-height:0}
  #map{flex:1}
  #panel{width:295px;overflow-y:auto;background:#F6F8FB;border-left:1px solid #C9D4E4;padding:12px 14px;font-size:12.5px;color:#1F3864}
  #panel h2{font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:#17365D;margin:14px 0 6px;border-bottom:2px solid #B8C6DC;padding-bottom:3px}
  .cat{display:flex;align-items:center;gap:7px;margin:4px 0;cursor:pointer;user-select:none}
  .cat input{accent-color:#17365D}
  .sw{width:11px;height:11px;border-radius:50%;border:1.5px solid #fff;box-shadow:0 0 2px rgba(0,0,0,.5);flex:none}
  .poi-row{display:flex;gap:6px;margin:2.5px 0;line-height:1.35;cursor:pointer}
  .poi-row:hover{background:#E8EEF7}
  .poi-row b{font-weight:600}
  .poi-row .d{color:#5A6E92;white-space:nowrap;margin-left:auto;padding-left:6px}
  footer{background:#EAF0F8;color:#44567A;font-size:11px;padding:6px 16px;line-height:1.45;border-top:1px solid #C9D4E4}
  .lbl{background:rgba(23,54,93,.88);color:#fff;border:none;border-radius:3px;padding:1px 6px;font-size:11px;font-weight:600;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,.4)}
  .lbl:before{display:none}
  .roadlbl{background:#B02418;color:#fff;border-radius:3px;padding:2px 7px;font-size:11.5px;font-weight:700;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,.5);border:none}
  .roadlbl:before{display:none}
  .subjlbl{background:#F2C230;color:#17365D;border-radius:3px;padding:2px 8px;font-size:12.5px;font-weight:800;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.5);border:none}
  .subjlbl:before{display:none}
</style>
</head><body><div id="wrap">
<header><h1>SEASONS AT MERIDIAN — LOCATION &amp; AMENITY MAP</h1>
<span class="sub">2700 E Overland Rd, Meridian ID · SE quadrant of Eagle Rd (SH-55) &amp; I-84 · rings at 1 / 3 / 5 mi</span></header>
<div id="main"><div id="map"></div><div id="panel">
<h2>Layers</h2><div id="cats"></div>
<h2>Key places</h2><div id="list"></div>
</div></div>
<footer>__FOOTER__</footer>
</div>
<script>__LEAFLET_JS__</script>
<script>
const SUBJ=__SUBJ__, CATS=__CATS__, POIS=__POIS__, ROADS=__ROADS__, RINGS=__RINGS__, NEWDEV=__NEWDEV__;
const map=L.map('map',{scrollWheelZoom:true});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Imagery &copy; Esri, Maxar, Earthstar Geographics'}).addTo(map);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,opacity:0.9}).addTo(map);
map.setView(SUBJ,13);

// rings
RINGS.forEach(mi=>{
  L.circle(SUBJ,{radius:mi*1609.34,color:'#fff',weight:1.6,opacity:.85,fill:false,dashArray:'6 6'}).addTo(map);
  L.marker([SUBJ[0]-mi/69.0,SUBJ[1]],{icon:L.divIcon({className:'lbl',html:mi+' mi',iconSize:null}),interactive:false}).addTo(map);
});

// roads (labels only; the satellite imagery shows the roads themselves)
ROADS.forEach(r=>{
  L.marker(r.at,{icon:L.divIcon({className:'roadlbl',html:r.label,iconSize:null}),interactive:true})
    .addTo(map).bindPopup('<b>'+r.label+'</b><br>'+r.note);
});

// subject
L.circleMarker(SUBJ,{radius:11,color:'#fff',weight:2.5,fillColor:'#F2C230',fillOpacity:1}).addTo(map)
  .bindPopup('<b>Seasons at Meridian</b><br>2700 E Overland Rd · 360 units · 2024');
L.marker([SUBJ[0]-0.0035,SUBJ[1]],{icon:L.divIcon({className:'subjlbl',html:'SEASONS AT MERIDIAN',iconSize:null}),interactive:false}).addTo(map);

// POI layers
const groups={}, catMeta={};
CATS.forEach(c=>{groups[c.id]=L.layerGroup().addTo(map);catMeta[c.id]=c;});
const ndGroup=L.layerGroup(); groups['newdev']=ndGroup;
POIS.forEach(p=>{
  const c=catMeta[p.cat];
  const mk=L.circleMarker([p.lat,p.lon],{radius:7,color:'#fff',weight:1.8,fillColor:c.color,fillOpacity:.95});
  mk.bindPopup('<b>'+p.name+'</b><br>'+(p.note||'')+(p.d?'<br><i>'+p.d+' mi from subject</i>':''));
  mk.addTo(groups[p.cat]);
  if(p.lbl){
    const off=p.loff||[-0.0028,0];
    L.marker([p.lat+off[0],p.lon+off[1]],{icon:L.divIcon({className:'lbl',html:p.name,iconSize:null}),interactive:false}).addTo(groups[p.cat]);
  }
});
NEWDEV.forEach(p=>{
  const col={'Office':'#3987e5','Industrial':'#9aa7b8','Retail':'#eb6834','Hospitality':'#b06fd6','Health Care':'#1baf7a','Specialty':'#9aa7b8','Flex':'#9aa7b8','Sports & Entertainment':'#b06fd6'}[p.t]||'#9aa7b8';
  L.circleMarker([p.lat,p.lon],{radius:4.5,color:'#fff',weight:1,fillColor:col,fillOpacity:.85})
   .bindPopup('<b>'+(p.n||p.a)+'</b><br>'+p.t+' · '+p.sf.toLocaleString()+' SF · '+(p.st==='Under Construction'?'UC, ':'built ')+p.yr+'<br><i>'+p.d+' mi from subject</i>')
   .addTo(ndGroup);
});

// panel
const catsDiv=document.getElementById('cats');
CATS.concat([{id:'newdev',name:'All new commercial 20K+ SF (CoStar, built 2020+)',color:'#9aa7b8',off:true}]).forEach(c=>{
  const row=document.createElement('label');row.className='cat';
  row.innerHTML='<input type="checkbox" '+(c.off?'':'checked')+'><span class="sw" style="background:'+c.color+'"></span>'+c.name;
  row.querySelector('input').onchange=e=>{e.target.checked?map.addLayer(groups[c.id]):map.removeLayer(groups[c.id]);};
  catsDiv.appendChild(row);
});
const list=document.getElementById('list');
POIS.filter(p=>p.key).forEach(p=>{
  const c=catMeta[p.cat];
  const row=document.createElement('div');row.className='poi-row';
  row.innerHTML='<span class="sw" style="background:'+c.color+';margin-top:3px"></span><span><b>'+p.name+'</b></span><span class="d">'+(p.d?p.d+' mi':'')+'</span>';
  row.onclick=()=>{map.setView([p.lat,p.lon],15);};
  list.appendChild(row);
});
</script></body></html>'''

if __name__ == '__main__':
    main()
