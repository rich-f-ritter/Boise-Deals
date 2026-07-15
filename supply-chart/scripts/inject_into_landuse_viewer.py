#!/usr/bin/env python3
"""Merge supply-chart companion map(s) into a land-use-analysis viewer.

Lifts the PINS/LEG data embedded in each supply map HTML (so numbering, buckets
and popups match the Supply Chart exactly) and injects a self-contained,
toggleable overlay into the target viewer: numbered competitive-supply pins,
shadow/latent-site pins, the gold 5-mile ring(s), and a legend panel with
checkboxes. Supports multiple supply maps (e.g. the two-deal Treasure Valley
summary map) — pass --supply-map/--label pairs. Idempotent: re-running
replaces the previously injected block.

Usage (single deal):
  python inject_into_landuse_viewer.py \
    --viewer "CanyonRidge/Canyon Ridge - Land Use Viewer.html" \
    --supply-map CanyonRidge/supply/Canyon_Ridge__Map.html

Usage (summary map, both deals):
  python inject_into_landuse_viewer.py \
    --viewer "summary/Treasure Valley - Development Opportunity Summary Map.html" \
    --supply-map CanyonRidge/supply/Canyon_Ridge__Map.html --label "Canyon Ridge" \
    --supply-map SeasonsMeridian/supply/Seasons_at_Meridian__Map.html --label "Seasons"
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
   box-shadow:0 1px 4px rgba(0,0,0,.25);max-width:290px}
 .slx-panel h4{margin:0 0 5px;font:700 11px Calibri,Arial;letter-spacing:.06em;color:#0B4F6C}
 .slx-panel h5{margin:5px 0 2px;font:700 11px Calibri,Arial;color:#333}
 .slx-panel .row{display:flex;align-items:center;margin:2px 0;gap:6px}
 .slx-panel .dot{width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #999;flex:none}
 .slx-panel label{cursor:pointer;display:flex;align-items:center;gap:6px;font-weight:700}
 .slx-pop b{font-size:13px}
</style>
<script>
(function(){
  const SETS = __SETS__;   // [{label, pins, leg}]
  const RING_MI = 5.0;
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  function popup(p, lbl){
    let h='<div class="slx-pop"><b>'+(p.num!=null&&p.num!=='•'?p.num+'. ':'')+esc(p.name)+'</b>';
    if(lbl) h+=' <span style="color:#888;font-size:11px">('+esc(lbl)+' chart)</span>';
    h+='<br><span style="color:'+p.color+';font-weight:700">'+esc(p.bucket)+'</span><br>';
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
  function pinMarker(p, lbl){
    const sz=(p.units||0)>=300?26:(p.units||0)>=100?22:18;
    const icon=L.divIcon({className:'', iconSize:[sz,sz], iconAnchor:[sz/2,sz/2],
      html:'<div class="slx-pin" style="width:'+sz+'px;height:'+sz+'px;background:'+p.color+'">'+(p.num==null?'':p.num)+'</div>'});
    return L.marker([p.lat,p.lng],{icon:icon,zIndexOffset:600}).bindPopup(popup(p,lbl),{maxWidth:340});
  }
  const multi = SETS.length > 1;
  const groups = SETS.map(function(set, si){
    const comps=L.layerGroup(), shadows=L.layerGroup();
    let ring=null;
    for(const p of set.pins){
      if(p.bucket==='SUBJECT'){
        ring=L.circle([p.lat,p.lng],{radius:RING_MI*1609.34,color:'#D4A017',weight:2,fill:false,dashArray:'6 6'});
        continue;   // host viewer already marks the subject(s)
      }
      (/shadow/i.test(p.bucket)?shadows:comps).addLayer(pinMarker(p, multi?set.label:null));
    }
    return {set:set, comps:comps, shadows:shadows, ring:ring, ci:'slx-c'+si, siId:'slx-s'+si};
  });
  const panel=document.createElement('div');
  panel.className='slx-panel';
  let h='<h4>COMPETITIVE SUPPLY (5-MI CHARTS)</h4>';
  for(const g of groups){
    if(multi) h+='<h5>'+esc(g.set.label)+'</h5>';
    h+='<label><input type="checkbox" id="'+g.ci+'" checked> Supply comps (numbered)</label>';
    for(const l of g.set.leg)
      h+='<div class="row"><span class="dot" style="background:'+l.color+'"></span>'+esc(l.label)+
         ' <span style="color:#666">('+l.n+' / '+l.u.toLocaleString()+' u)</span></div>';
    h+='<label><input type="checkbox" id="'+g.siId+'" checked> '+
       '<span class="dot" style="background:#7C4DFF;margin:0"></span> Shadow / latent (land-use)</label>';
  }
  h+='<div style="color:#666;font-size:11px">Pin numbers match each Supply Chart\\u2019s rows; gold dashes = 5-mi ring.</div>';
  panel.innerHTML=h;
  document.body.appendChild(panel);
  function sync(){
    for(const g of groups){
      const c=document.getElementById(g.ci).checked, s=document.getElementById(g.siId).checked;
      c?g.comps.addTo(map):map.removeLayer(g.comps);
      s?g.shadows.addTo(map):map.removeLayer(g.shadows);
      if(g.ring){ (c||s)?g.ring.addTo(map):map.removeLayer(g.ring); }
    }
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
    ap.add_argument("--viewer", required=True, help="target viewer HTML (updated in place unless --out)")
    ap.add_argument("--supply-map", action="append", required=True,
                    help="supply-chart companion map HTML (repeatable)")
    ap.add_argument("--label", action="append", default=None,
                    help="deal label per --supply-map (required when more than one)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    labels = a.label or []
    if len(a.supply_map) > 1 and len(labels) != len(a.supply_map):
        sys.exit("--label required for each --supply-map when passing more than one")
    sets = []
    for i, sm in enumerate(a.supply_map):
        pins, leg = extract(sm)
        sets.append({"label": labels[i] if i < len(labels) else "", "pins": pins, "leg": leg})

    html = open(a.viewer, encoding="utf-8").read()
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
    block = START + BLOCK.replace("__SETS__", json.dumps(sets)) + END
    # anchor before </body>, else </html>, else append (single-file viewers vary)
    for anchor in ("</body>", "</html>"):
        if anchor in html:
            html = html.replace(anchor, block + anchor, 1)
            break
    else:
        html += block
    out = a.out or a.viewer
    open(out, "w", encoding="utf-8").write(html)
    for s_ in sets:
        n_shadow = sum(1 for p in s_["pins"] if "shadow" in p["bucket"].lower())
        n_comp = sum(1 for p in s_["pins"] if p["bucket"] != "SUBJECT") - n_shadow
        print(f"  {s_['label'] or '(single)'}: {n_comp} supply pins + {n_shadow} shadow pins")
    print(f"Injected into {out}")


if __name__ == "__main__":
    main()
