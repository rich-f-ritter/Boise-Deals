#!/usr/bin/env python3
"""Merge the supply-chart companion map into a land-use-analysis viewer.

Lifts the PINS/LEG data embedded in the supply map HTML (so numbering, buckets
and popups match the Supply Chart exactly) and injects a self-contained,
toggleable overlay into the land-use viewer: numbered competitive-supply pins,
shadow/latent-site pins, the gold 5-mile ring, and a small legend panel with
checkboxes. Idempotent — re-running replaces the previously injected block.

Usage:
  python inject_into_landuse_viewer.py \
    --viewer "CanyonRidge/Canyon Ridge - Land Use Viewer.html" \
    --supply-map CanyonRidge/supply/Canyon_Ridge__Map.html
"""
import argparse, json, re, sys

START = "<!-- SUPPLY-LAYER-START -->"
END = "<!-- SUPPLY-LAYER-END -->"

BLOCK = """
<style>
 .slx-pin{border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px rgba(0,0,0,.45),0 1px 4px rgba(0,0,0,.55);
   color:#fff;font:700 11px/1 Calibri,Arial;display:flex;align-items:center;justify-content:center;}
 .slx-panel{position:absolute;left:14px;bottom:18px;z-index:1000;background:rgba(255,255,255,.95);
   border:1px solid #bbb;border-radius:6px;padding:9px 12px;font:12px/1.55 Calibri,Arial;color:#222;
   box-shadow:0 1px 4px rgba(0,0,0,.25);max-width:280px}
 .slx-panel h4{margin:0 0 5px;font:700 11px Calibri,Arial;letter-spacing:.06em;color:#0B4F6C}
 .slx-panel .row{display:flex;align-items:center;margin:2px 0;gap:6px}
 .slx-panel .dot{width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #999;flex:none}
 .slx-panel label{cursor:pointer;display:flex;align-items:center;gap:6px;font-weight:700}
 .slx-pop b{font-size:13px}
</style>
<script>
(function(){
  const SUPPLY_PINS = __PINS__;
  const SUPPLY_LEG  = __LEG__;
  const RING_MI = 5.0;
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  function popup(p){
    let h='<div class="slx-pop"><b>'+(p.num!=null&&p.num!=='•'?p.num+'. ':'')+esc(p.name)+'</b><br>';
    h+='<span style="color:'+p.color+';font-weight:700">'+esc(p.bucket)+'</span><br>';
    if(p.units) h+=p.units.toLocaleString()+' units · ';
    if(p.deliver) h+='Delivery: '+esc(p.deliver)+' · ';
    if(p.dist!=null) h+=p.dist+' mi';
    h+='<br>';
    if(p.occ!=null) h+='Occupancy: <b>'+p.occ+'%</b> · ';
    if(p.rent) h+='Avg rent: <b>$'+p.rent.toLocaleString()+'</b>';
    if(p.occ!=null||p.rent) h+='<br>';
    if(p.notes) h+='<i style="font-size:11px">'+esc(p.notes)+'</i>';
    return h+'</div>';
  }
  function pinMarker(p){
    const sz=(p.units||0)>=300?26:(p.units||0)>=100?22:18;
    const icon=L.divIcon({className:'', iconSize:[sz,sz], iconAnchor:[sz/2,sz/2],
      html:'<div class="slx-pin" style="width:'+sz+'px;height:'+sz+'px;background:'+p.color+'">'+ (p.num==null?'':p.num) +'</div>'});
    return L.marker([p.lat,p.lng],{icon:icon,zIndexOffset:600}).bindPopup(popup(p),{maxWidth:340});
  }
  const comps=L.layerGroup(), shadows=L.layerGroup();
  let subjPt=null;
  for(const p of SUPPLY_PINS){
    if(p.bucket==='SUBJECT'){ subjPt=[p.lat,p.lng]; continue; }   // viewer already pins the subject
    (/shadow/i.test(p.bucket)?shadows:comps).addLayer(pinMarker(p));
  }
  const ring = subjPt ? L.circle(subjPt,{radius:RING_MI*1609.34,color:'#D4A017',weight:2,
                                         fill:false,dashArray:'6 6'}) : null;
  // control panel
  const panel=document.createElement('div');
  panel.className='slx-panel';
  let rows='';
  for(const l of SUPPLY_LEG)
    rows+='<div class="row"><span class="dot" style="background:'+l.color+'"></span>'+esc(l.label)+
          ' <span style="color:#666">('+l.n+' / '+l.u.toLocaleString()+' u)</span></div>';
  panel.innerHTML='<h4>COMPETITIVE SUPPLY (5-MI CHART)</h4>'+
    '<label><input type="checkbox" id="slx-c" checked> Supply comps (numbered)</label>'+rows+
    '<label style="margin-top:4px"><input type="checkbox" id="slx-s" checked> '+
    '<span class="dot" style="background:#7C4DFF;margin:0"></span> Shadow / latent (land-use)</label>'+
    '<div style="color:#666;font-size:11px">Pin numbers match the Supply Chart rows; gold dashes = 5-mi ring.</div>';
  document.body.appendChild(panel);
  function sync(){
    const c=document.getElementById('slx-c').checked, s=document.getElementById('slx-s').checked;
    c?comps.addTo(map):map.removeLayer(comps);
    s?shadows.addTo(map):map.removeLayer(shadows);
    if(ring){ (c||s)?ring.addTo(map):map.removeLayer(ring); }
  }
  panel.addEventListener('change',sync);
  sync();
})();
</script>
"""


def extract(supply_map_html):
    s = open(supply_map_html, encoding="utf-8").read()
    pins = re.search(r"const PINS = (\[.*?\]);", s, re.S)
    leg = re.search(r"const LEG = (\[.*?\]);", s, re.S)
    if not pins or not leg:
        sys.exit(f"PINS/LEG not found in {supply_map_html} — is it a supply-chart map?")
    return json.loads(pins.group(1)), json.loads(leg.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--viewer", required=True, help="land-use viewer HTML (updated in place unless --out)")
    ap.add_argument("--supply-map", required=True, help="supply-chart companion map HTML")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    pins, leg = extract(a.supply_map)
    html = open(a.viewer, encoding="utf-8").read()
    # idempotency: strip any previous injection
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
    block = START + BLOCK.replace("__PINS__", json.dumps(pins)).replace("__LEG__", json.dumps(leg)) + END
    anchor = "</body>"
    if anchor not in html:
        sys.exit("</body> not found in viewer")
    html = html.replace(anchor, block + anchor, 1)
    out = a.out or a.viewer
    open(out, "w", encoding="utf-8").write(html)
    n_shadow = sum(1 for p in pins if "shadow" in p["bucket"].lower())
    n_comp = sum(1 for p in pins if p["bucket"] != "SUBJECT") - n_shadow
    print(f"Injected {n_comp} supply pins + {n_shadow} shadow pins into {out}")


if __name__ == "__main__":
    main()
