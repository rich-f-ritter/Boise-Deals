#!/usr/bin/env python3
"""Build the Seasons at Meridian supply-chart companion map (self-contained Leaflet).

Inputs (same dir unless overridden):
  supply_map_data.json  — {"subject": {...}, "deals": [...], "shadow": [...]}
Deal: {name, units, bucket, row, lat, lon, est_delivery, occ, note}
Shadow: {name, units, lat, lon, note, status}
Buckets → colors match the Supply Chart workbook.
"""
import json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE.parent.parent / "land-use-analysis" / "assets" / "vendor"

COLORS = {
    "STABILIZED / STABILIZING": "#1f6fb5",
    "LEASING UP": "#e8862c",
    "UNDER CONSTRUCTION": "#2e8b57",
    "PROPOSED": "#c62828",
    "SHADOW": "#5e35b1",
    "DEAD": "#757575",
}

def ring_coords(lat, lon, miles=5.0, n=180):
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        dlat = miles / 69.0 * math.cos(a)
        dlon = miles / (69.0 * math.cos(math.radians(lat))) * math.sin(a)
        pts.append([lat + dlat, lon + dlon])
    return pts

def main():
    data = json.loads((HERE / "supply_map_data.json").read_text())
    subj = data["subject"]
    leaf_css = (VENDOR / "leaflet.css").read_text()
    leaf_js = (VENDOR / "leaflet.js").read_text()
    ring = ring_coords(subj["lat"], subj["lon"])
    payload = json.dumps({"subject": subj, "deals": data["deals"],
                          "shadow": data.get("shadow", []), "ring": ring},
                         separators=(",", ":"))
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Seasons at Meridian — Supply Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{leaf_css}</style>
<style>
html,body,#map{{height:100%;margin:0}}
.hdr{{position:absolute;z-index:1000;top:10px;left:54px;background:#fff;padding:8px 14px;
 border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.3);font:600 15px system-ui}}
.hdr small{{display:block;font-weight:400;color:#555}}
.lg{{position:absolute;z-index:1000;bottom:14px;left:10px;background:#fff;padding:10px 12px;
 border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.3);font:12px system-ui;line-height:1.7}}
.lg .sw{{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px}}
.pin{{display:flex;align-items:center;justify-content:center;color:#fff;font:700 10px system-ui;
 border-radius:50%;border:2px solid #fff;box-shadow:0 0 3px rgba(0,0,0,.6);width:22px;height:22px}}
.pin.star{{background:#111;font-size:13px;width:26px;height:26px}}
.pin.shadow{{border-radius:4px}}
.leaflet-popup-content{{font:13px system-ui}}
</style></head><body><div id="map"></div>
<div class="hdr">Seasons at Meridian — 5-Mile Competitive Supply<small>2022–2026 new construction + pipeline + shadow watch · as of Aug 2026 · pins numbered to Supply Chart rows</small></div>
<div class="lg">
<span class="sw" style="background:#1f6fb5"></span>Stabilized / stabilizing<br>
<span class="sw" style="background:#e8862c"></span>Leasing up<br>
<span class="sw" style="background:#2e8b57"></span>Under construction<br>
<span class="sw" style="background:#c62828"></span>Proposed pipeline<br>
<span class="sw" style="background:#5e35b1;border-radius:2px"></span>Shadow / latent watch (not in unit totals)<br>
<span class="sw" style="background:#757575;border-radius:2px"></span>Documented dead (incl. Seasons II site)<br>
★ subject &nbsp;·&nbsp; dashed ring = 5 mi
</div>
<script>{leaf_js}</script>
<script>
var D={payload};
var map=L.map('map');
var sat=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:19,attribution:'Esri World Imagery'}});
var streets=L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'OSM'}});
sat.addTo(map);
L.control.layers({{'Satellite':sat,'Streets':streets}}).addTo(map);
L.polyline(D.ring,{{color:'#e8b02c',weight:2.5,dashArray:'8 7',fill:false}}).addTo(map);
var CO={json.dumps(COLORS)};
function pin(d){{
  var cls='pin'+(d.bucket==='SHADOW'||d.bucket==='DEAD'?' shadow':'');
  var lab=d.row||'&#9679;';
  var ic=L.divIcon({{className:'',html:'<div class="'+cls+'" style="background:'+CO[d.bucket]+'">'+lab+'</div>',iconSize:[22,22],iconAnchor:[11,11]}});
  var m=L.marker([d.lat,d.lon],{{icon:ic}}).addTo(map);
  var t='<b>'+(d.row?d.row+'. ':'')+d.name+'</b><br>'+(d.units?d.units+' units · ':'')+d.bucket.toLowerCase();
  if(d.est_delivery)t+='<br>Est. delivery: '+d.est_delivery;
  if(d.occ)t+='<br>Occupancy: '+d.occ;
  if(d.note)t+='<br><i>'+d.note+'</i>';
  m.bindPopup(t);
}}
D.deals.forEach(pin); D.shadow.forEach(pin);
var s=L.divIcon({{className:'',html:'<div class="pin star">★</div>',iconSize:[26,26],iconAnchor:[13,13]}});
L.marker([D.subject.lat,D.subject.lon],{{icon:s}}).addTo(map)
 .bindPopup('<b>★ '+D.subject.name+' (SUBJECT)</b><br>'+D.subject.note);
map.fitBounds(D.ring,{{padding:[8,8]}});
</script></body></html>"""
    out = HERE.parent.parent / "SeasonsMeridian" / "Seasons at Meridian - Supply Map.html"
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])
    out.write_text(html)
    print("wrote", out, len(html), "bytes")

if __name__ == "__main__":
    main()
