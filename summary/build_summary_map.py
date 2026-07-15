"""Build the combined 'Development-Opportunity Summary' interactive map (self-contained HTML)
covering BOTH subjects. Sections colored by synthesis category, grouped into OPPORTUNITY /
LONG-TERM / OFF-LIMITS / CONTEXT so go-vs-no-go reads instantly (off-limits categories are
hatched). Headline stat + CR-vs-SM bar + interactive grouped legend + click-through detail."""
import json
from pathlib import Path

BASE = Path("/home/user/Boise-Deals")
SUM = BASE / "summary"
VENDOR = BASE / "land-use-analysis" / "assets" / "vendor"

# key, label, color, group, why
CATS = [
    ("apartments", "Competing apartments — built / approved / proposed", "#E12726", "opportunity",
     "New multifamily that competes directly with the subject for renters. Click for the project, developer and status."),
    ("apt_ready", "Apartment-ready land — available now", "#FB8C1A", "opportunity",
     "Vacant land that can host apartments by-right or via a likely rezone, with no active project yet — the latent competitive supply."),
    ("mpc_res", "Active master-planned residential", "#D65DB1", "opportunity",
     "Large communities under construction — mostly for-sale, but they add rooftops and some attached / multifamily."),
    ("landbank", "Land-bank / future growth (long-term)", "#AFA77E", "longterm",
     "Large vacant urban-edge tracts planned for growth but not near-term — future supply that is currently constrained or stalled."),
    ("micron", "Micron — campus & expansion", "#7E3F98", "offlimits",
     "Micron's semiconductor campus & expansion. Removes land from housing AND is the metro's #1 apartment DEMAND driver (thousands of jobs)."),
    ("airport_land", "Boise Airport / Gowen Field (aviation)", "#26406B", "offlimits",
     "The city-owned airfield itself (~5,100 ac, joint civil / military) — aviation use, never housing."),
    ("airport", "Airport Influence Area — apartment-restricted", "#5E86C4", "offlimits",
     "Land inside Boise Airport Influence Area zones B & C, where new housing is prohibited by code — a policy 'moat' that this land can never cross to become competing apartments."),
    ("industry", "Industrial / employment (non-Micron)", "#565B63", "offlimits",
     "Industrial / employment land — not available for housing."),
    ("rural", "Rural / foothills / protected", "#A6A588", "context",
     "Rural, foothills, or protected open space — not developable for housing."),
    ("commercial", "Commercial / retail", "#B7BCC2", "context",
     "Retail / commercial — could add apartments only if it redevelops as mixed-use."),
    ("civic", "Parks / civic / institutional", "#A9C6B0", "context",
     "Parks, open space, schools, HOA commons — not developable."),
    ("established", "Established neighborhoods", "#DAD6CE", "context",
     "Built-out neighborhoods — existing rooftops, not new competitive supply."),
]
GROUPS = [("opportunity", "Where new apartments can go"),
          ("longterm", "Long-term / future supply"),
          ("offlimits", "Off-limits to new housing"),
          ("context", "Context")]
OFFLIMITS = {"micron", "airport_land", "airport", "industry"}
SUBJECTS = [("Canyon Ridge", 43.541734, -116.151198, "Southeast Boise · by the airport"),
            ("Seasons at Meridian", 43.591935, -116.360877, "Southeast Meridian")]

TEMPLATE = r"""<title>Treasure Valley — Development-Opportunity Summary Map</title>
<style>__LEAFLET_CSS__</style>
<style>
:root{--ink:#16202b;--muted:#59636f;--pane:#ffffff;--hair:#e3e8ed;--bg:#e9edf1;--cr:#3E6E9C;--sm:#C0692A;}
*{box-sizing:border-box} html,body{height:100%;margin:0}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
#app{position:fixed;inset:0;display:grid;grid-template-columns:1fr 384px;grid-template-rows:auto 1fr}
header{grid-column:1/3;background:#0e1620;color:#fff;padding:9px 18px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;z-index:1000}
header h1{font-family:Charter,"Iowan Old Style",Palatino,Georgia,serif;font-size:17px;margin:0;font-weight:700}
header .sub{font-size:12px;color:#a9b4bf;max-width:58ch}
header .toggles{margin-left:auto;display:flex;gap:6px}
header button{background:#1d2733;color:#cdd6df;border:1px solid #2b3947;border-radius:6px;padding:5px 11px;font-size:12px;cursor:pointer;font-family:inherit}
header button.on{background:#fff;color:#0e1620;border-color:#fff}
#map{grid-column:1;grid-row:2;height:100%;background:#dfe5ea}
#side{grid-column:2;grid-row:2;background:var(--pane);border-left:1px solid var(--hair);overflow-y:auto}
@media(max-width:860px){#app{grid-template-columns:1fr} #side{position:absolute;right:0;top:0;bottom:0;width:92%;max-width:384px;box-shadow:-8px 0 24px #0003;transform:translateX(102%);transition:.25s;z-index:1200} #side.open{transform:none} #openside{display:block!important}}
#openside{display:none;position:absolute;right:12px;top:64px;z-index:1100;background:#0e1620;color:#fff;border:none;border-radius:8px;padding:8px 12px;font-size:12px;cursor:pointer}
.pad{padding:14px 16px}
.headline{background:linear-gradient(180deg,#f6f8fa,#fff);border-bottom:1px solid var(--hair)}
.headline .lead{font-size:12.5px;color:var(--muted);margin:0 0 8px}
.headline .take{font-size:12.5px;color:var(--ink);background:#eef3f7;border-left:3px solid var(--sm);padding:8px 11px;border-radius:0 8px 8px 0;margin:10px 0 2px}
.headline .take{font-weight:500}
.barkey{font-size:11px;color:var(--muted);margin:0 0 6px;display:flex;align-items:center;gap:5px}
.barkey .ks{display:inline-block;width:10px;height:10px;border-radius:2px;margin-left:8px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:4px}
.cmp .box{border:1px solid var(--hair);border-radius:10px;padding:10px 12px;position:relative;overflow:hidden}
.cmp .box::before{content:"";position:absolute;inset:0 auto 0 0;width:4px}
.cmp .box.cr::before{background:var(--cr)} .cmp .box.sm::before{background:var(--sm)}
.cmp .box .nm{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.cmp .box.cr .nm{color:var(--cr)} .cmp .box.sm .nm{color:var(--sm)}
.cmp .box .v{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.1;margin-top:3px}
.cmp .box .u{font-size:11px;color:var(--muted)}
.barwrap{margin-top:10px}
.barwrap h3{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.legend h2{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:12px 0 3px}
.legend .hint{font-size:11.5px;color:var(--muted);margin:2px 0 8px}
.row{display:flex;align-items:center;gap:9px;padding:5px 6px;border-radius:7px;cursor:pointer;user-select:none}
.row:hover{background:#f2f5f8} .row.off{opacity:.4}
.sw{width:16px;height:16px;border-radius:4px;flex:0 0 auto;border:1px solid #00000022}
.row .lab{font-size:12.5px;line-height:1.16;flex:1}
.row .ac{font-size:10.5px;color:var(--muted);font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap;line-height:1.15}
.row .ac b{color:var(--ink)}
.detail{padding:16px 18px;display:none;border-top:3px solid var(--hair);background:#fbfcfd}
.detail.show{display:block}
.detail .cat{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:#fff;padding:3px 10px;border-radius:20px}
.detail h3{font-family:Charter,Palatino,Georgia,serif;font-size:18px;margin:12px 0 2px;line-height:1.24}
.detail .subj{font-size:12px;color:var(--muted);margin-bottom:12px}
.detail .big{display:flex;gap:22px;margin:6px 0 12px}
.detail .big div{font-size:12px;color:var(--muted)}
.detail .big b{display:block;font-size:20px;color:var(--ink);font-variant-numeric:tabular-nums}
.detail .why{font-size:12.5px;color:var(--ink);background:#eef3f7;border-left:3px solid var(--hair);padding:9px 12px;border-radius:0 8px 8px 0;margin-bottom:12px}
.detail dl{margin:0;font-size:13px;display:grid;grid-template-columns:82px 1fr;gap:6px 10px}
.detail dt{color:var(--muted);font-weight:600} .detail dd{margin:0}
.detail .kv{font-size:12.5px;margin:6px 0} .detail .kv b{color:var(--muted);font-weight:600}
.detail .src{margin-top:12px;padding-top:10px;border-top:1px solid var(--hair);font-size:11px;color:var(--muted);word-break:break-word}
.detail .src a{color:#2f6fb0;text-decoration:none}
.detail .close{float:right;cursor:pointer;color:var(--muted);font-size:22px;line-height:1;border:none;background:none}
.leaflet-tooltip.tt{font-size:12px;font-weight:600;background:#0e1620;color:#fff;border:none;box-shadow:0 2px 8px #0004;padding:4px 8px}
.leaflet-tooltip.tt:before{display:none}
.leaflet-tooltip.ring{font-family:Charter,Palatino,Georgia,serif;font-size:14px;font-weight:700;background:#ffffffd8;color:#0e1620;border:1px solid #0e162033;box-shadow:0 2px 8px #0003;padding:3px 9px}
.leaflet-tooltip.ring:before{display:none}
.status-chip{display:inline-block;font-size:10.5px;font-weight:700;text-transform:uppercase;color:#fff;padding:2px 8px;border-radius:20px;margin-left:8px;vertical-align:middle}
</style>
<svg width="0" height="0" style="position:absolute"><defs>__HATCH_DEFS__</defs></svg>
<div id="app">
  <header>
    <h1>Treasure Valley — Development-Opportunity Summary</h1>
    <span class="sub">Where new apartments can &amp; can't go around two communities · like-kind parcels dissolved into sections · click any section for detail</span>
    <div class="toggles">
      <button id="b-sat">Satellite</button>
      <button id="b-light" class="on">Light</button>
      <button id="b-cr">Canyon Ridge</button>
      <button id="b-sm">Seasons</button>
      <button id="b-both">Both</button>
    </div>
  </header>
  <div id="map"></div>
  <button id="openside" onclick="document.getElementById('side').classList.toggle('open')">Legend / detail</button>
  <aside id="side">
    <div class="headline pad" id="headline"></div>
    <div class="legend pad" id="legend"></div>
    <div class="detail" id="detail"></div>
  </aside>
</div>
<script>__LEAFLET_JS__</script>
<script>
const CATS=__CATS__, GROUPS=__GROUPS__, TOT=__TOT__, SUBJ=__SUBJ__, DATA=__DATA__, OFFL=__OFFL__;
const catByK={}; CATS.forEach(function(c,i){catByK[c.k]={label:c.label,color:c.color,group:c.group,why:c.why,i:i};});
const off=new Set();
const map=L.map('map',{renderer:L.svg({padding:0.5}),zoomControl:true}).setView([43.567,-116.255],11);
const TILES={sat:['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}','Esri, Maxar'],
 light:['https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}','Esri']};
let base=null;
function setBase(k){ if(base)map.removeLayer(base); base=L.tileLayer(TILES[k][0],{maxZoom:19,attribution:TILES[k][1],opacity:k==='light'?1:0.9}).addTo(map); base.bringToBack();
  document.getElementById('b-sat').classList.toggle('on',k==='sat'); document.getElementById('b-light').classList.toggle('on',k==='light'); }
setBase('light');
function fillFor(k){ return OFFL.indexOf(k)>=0 ? 'url(#hx-'+k+')' : catByK[k].color; }
function style(f){ const k=f.properties.cat, c=catByK[k], g=c.group;
  const w = g==='opportunity'?1.3 : g==='offlimits'?0.5 : g==='longterm'?0.6 : 0.2;
  const op = off.has(k)?0 : g==='opportunity'?0.92 : g==='longterm'?0.6 : g==='offlimits'?0.95 : 0.34;
  const bc = g==='opportunity'?'#3a1400' : g==='offlimits'?'#20262e' : g==='longterm'?'#5c4611' : '#8a929b';
  return {color:bc, weight:w, fillColor:fillFor(k), fillOpacity:op}; }
const STCOL={approved:'#2e8259',construction:'#2f6fb0',proposed:'#c08a16',built:'#6e7a88',denied:'#ab4630',dormant:'#8a8f98'};
function stChip(s){ if(!s)return''; const t=s.toLowerCase(); let k='dormant';
  if(t.indexOf('approv')>=0)k='approved'; else if(t.indexOf('constr')>=0||t.indexOf('under')>=0)k='construction';
  else if(t.indexOf('propos')>=0||t.indexOf('plan')>=0||t.indexOf('entitl')>=0||t.indexOf('pre-app')>=0)k='proposed';
  else if(t.indexOf('denied')>=0)k='denied'; else if(t.indexOf('built')>=0)k='built';
  return '<span class="status-chip" style="background:'+STCOL[k]+'">'+s.split(/[;(]/)[0].trim().slice(0,24)+'</span>'; }
const layer=L.geoJSON(DATA,{style:style, onEachFeature:function(f,l){
  l.bindTooltip(catByK[f.properties.cat].label.split('—')[0].trim()+' · '+Math.round(f.properties.acres).toLocaleString()+' ac',{className:'tt',sticky:true});
  l.on('click',function(){showDetail(f.properties);});
}}).addTo(map);
SUBJ.forEach(function(s){
  L.circleMarker([s.lat,s.lon],{radius:8,color:'#fff',weight:3,fillColor:'#101820',fillOpacity:1,className:'subjpin'}).addTo(map).bringToFront();
  L.tooltip({permanent:true,direction:'top',className:'ring',offset:[0,-10]}).setLatLng([s.lat,s.lon]).setContent(s.name).addTo(map);
});
function fnum(n){return n==null?'—':Number(n).toLocaleString(undefined,{maximumFractionDigits:0});}
function sumCats(subj,keys){ let t=0; keys.forEach(function(k){ t+=(TOT[k]&&TOT[k][subj])||0; }); return t; }
const CRC='#3E6E9C', SMC='#C0692A';
function drawHeadline(){
  const S=['Canyon Ridge','Seasons at Meridian'];
  const crApt=sumCats(S[0],['apartments','apt_ready']), smApt=sumCats(S[1],['apartments','apt_ready']);
  const ratio = crApt>0 ? Math.round(smApt/crApt) : null;
  const h='<p class="lead">Existing + pipeline <b>apartment competition</b> — built, approved &amp; apartment-ready land — within 5 miles of each community:</p>'+
    '<div class="cmp"><div class="box cr"><div class="nm">Canyon Ridge</div><div class="v">'+fnum(crApt)+' ac</div><div class="u">apartment-capable land</div></div>'+
    '<div class="box sm"><div class="nm">Seasons</div><div class="v">'+fnum(smApt)+' ac</div><div class="u">apartment-capable land</div></div></div>'+
    (ratio?'<p class="take">≈'+ratio+'× more competing supply around Seasons. Canyon Ridge is boxed in by the airport, Micron and industry.</p>':'')+
    '<div class="barwrap"><h3>Apartment-supply roles — CR vs Seasons <span style="font-weight:400;text-transform:none;letter-spacing:0">(each row scaled to its own max)</span></h3>'+
    '<div class="barkey"><span class="ks" style="background:'+CRC+'"></span>Canyon Ridge <span class="ks" style="background:'+SMC+'"></span>Seasons</div><div id="bars"></div></div>';
  document.getElementById('headline').innerHTML=h;
  drawBars();
}
function drawBars(){
  const rows=[['apartments','Competing apartments'],['apt_ready','Apartment-ready'],['mpc_res','Master-planned res'],['landbank','Land-bank / future']];
  function val(subj,k){ return (TOT[k]&&TOT[k][subj])||0; }
  const W=344, bh=12, gap=3, lh=39, x0=146, bw=W-x0-32;
  let svg='<svg width="'+W+'" height="'+(rows.length*lh)+'" font-size="11" font-family="ui-sans-serif,system-ui">';
  rows.forEach(function(r,i){
    const y=i*lh, cr=val('Canyon Ridge',r[0]), sm=val('Seasons at Meridian',r[0]), mx=Math.max(cr,sm,1);
    svg+='<text x="0" y="'+(y+11)+'" fill="#59636f">'+r[1]+'</text>';
    svg+='<rect x="'+x0+'" y="'+(y+2)+'" width="'+(cr/mx*bw)+'" height="'+bh+'" rx="2" fill="'+CRC+'"/>';
    svg+='<text x="'+(x0+cr/mx*bw+4)+'" y="'+(y+11)+'" fill="#16202b" font-variant-numeric="tabular-nums">'+fnum(cr)+'</text>';
    svg+='<rect x="'+x0+'" y="'+(y+2+bh+gap)+'" width="'+(sm/mx*bw)+'" height="'+bh+'" rx="2" fill="'+SMC+'"/>';
    svg+='<text x="'+(x0+sm/mx*bw+4)+'" y="'+(y+11+bh+gap)+'" fill="#16202b" font-variant-numeric="tabular-nums">'+fnum(sm)+'</text>';
  });
  svg+='</svg>';
  document.getElementById('bars').innerHTML=svg;
}
function showDetail(p){
  const c=catByK[p.cat], d=document.getElementById('detail');
  let h='<button class="close" onclick="hideDetail()">&times;</button>';
  h+='<span class="cat" style="background:'+c.color+'">'+c.label+'</span>';
  h+='<h3>'+(p.title? p.title : c.label.split('—')[0].trim())+(p.status?stChip(p.status):'')+'</h3>';
  h+='<div class="subj">'+p.subject+(p.site_id?' · researched site '+p.site_id:'')+'</div>';
  h+='<div class="big"><div>Area<b>'+fnum(p.acres)+' ac</b></div><div>Parcels<b>'+fnum(p.parcels)+'</b></div></div>';
  h+='<div class="why">'+c.why+'</div>';
  if(p.owner){ h+='<dl>';
    h+='<dt>Owner</dt><dd>'+p.owner+'</dd>';
    if(p.owner_type)h+='<dt>Type</dt><dd>'+p.owner_type+'</dd>';
    if(p.since)h+='<dt>Owned since</dt><dd>'+p.since+'</dd>';
    if(p.who)h+='<dt>Who</dt><dd>'+p.who+'</dd>';
    if(p.intent)h+='<dt>Intent</dt><dd>'+p.intent+'</dd>';
    h+='</dl>'; }
  if(p.zoning)h+='<div class="kv"><b>Zoning:</b> '+p.zoning+'</div>';
  if(p.flu)h+='<div class="kv"><b>Future land use:</b> '+p.flu+'</div>';
  if(p.sources&&p.sources.length)h+='<div class="src">Sources: '+p.sources.map(function(u){return '<a href="'+u+'" target="_blank" rel="noopener">'+(u.split('/')[2]||u)+'</a>';}).join(' · ')+'</div>';
  d.innerHTML=h; d.classList.add('show'); document.getElementById('side').classList.add('open');
  d.scrollIntoView({behavior:'smooth',block:'nearest'});
}
function hideDetail(){ document.getElementById('detail').classList.remove('show'); }
function swatch(k){ const c=catByK[k].color;
  return OFFL.indexOf(k)>=0 ? 'background:repeating-linear-gradient(45deg,'+c+','+c+' 3px,rgba(0,0,0,.42) 3px,rgba(0,0,0,.42) 4.5px)'
    : 'background:'+c; }
function drawLegend(){
  let h='<h2>Legend — click a row to hide/show</h2><p class="hint">Acres shown per area · CR = Canyon Ridge, SM = Seasons.</p>';
  GROUPS.forEach(function(g){
    h+='<h2>'+g[1]+'</h2>';
    CATS.filter(function(c){return c.group===g[0];}).forEach(function(c){
      const t=TOT[c.k]||{}, cr=t['Canyon Ridge']||0, sm=t['Seasons at Meridian']||0;
      h+='<div class="row'+(off.has(c.k)?' off':'')+'" data-k="'+c.k+'"><span class="sw" style="'+swatch(c.k)+'"></span>'+
        '<span class="lab">'+c.label+'</span><span class="ac">CR <b>'+fnum(cr)+'</b><br>SM <b>'+fnum(sm)+'</b></span></div>';
    });
  });
  document.getElementById('legend').innerHTML=h;
  Array.prototype.forEach.call(document.querySelectorAll('.row'),function(r){ r.onclick=function(){
    const k=r.getAttribute('data-k'); if(off.has(k))off.delete(k); else off.add(k); r.classList.toggle('off'); layer.setStyle(style); }; });
}
drawHeadline(); drawLegend();
document.getElementById('b-sat').onclick=function(){setBase('sat');};
document.getElementById('b-light').onclick=function(){setBase('light');};
document.getElementById('b-cr').onclick=function(){map.setView([SUBJ[0].lat,SUBJ[0].lon],13);};
document.getElementById('b-sm').onclick=function(){map.setView([SUBJ[1].lat,SUBJ[1].lon],13);};
document.getElementById('b-both').onclick=function(){map.fitBounds(layer.getBounds(),{padding:[20,20]});};
map.fitBounds(layer.getBounds(),{padding:[20,20]});
</script>"""


def hatch_defs():
    dark = {"micron": "#3f1f52", "airport_land": "#12213b", "airport": "#2a4c86", "industry": "#2a2e34"}
    out = []
    for k in ("micron", "airport_land", "airport", "industry"):
        c = next(x[2] for x in CATS if x[0] == k)
        out.append(
            f'<pattern id="hx-{k}" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(45)">'
            f'<rect width="7" height="7" fill="{c}" fill-opacity="0.6"/>'
            f'<line x1="0" y1="0" x2="0" y2="7" stroke="{dark[k]}" stroke-width="2.4"/></pattern>')
    return "".join(out)


def main():
    fc = json.loads((SUM / "sections.geojson").read_text())
    summ = json.loads((SUM / "sections_summary.json").read_text())
    totals = {c[0]: summ.get(c[0], {}).get("by_subject", {}) for c in CATS}
    repl = {
        "__LEAFLET_CSS__": (VENDOR / "leaflet.css").read_text(),
        "__LEAFLET_JS__": (VENDOR / "leaflet.js").read_text(),
        "__HATCH_DEFS__": hatch_defs(),
        "__CATS__": json.dumps([{"k": c[0], "label": c[1], "color": c[2], "group": c[3], "why": c[4]} for c in CATS]),
        "__GROUPS__": json.dumps(GROUPS),
        "__TOT__": json.dumps(totals),
        "__SUBJ__": json.dumps([{"name": s[0], "lat": s[1], "lon": s[2], "note": s[3]} for s in SUBJECTS]),
        "__OFFL__": json.dumps(sorted(OFFLIMITS)),
        "__DATA__": json.dumps(fc, separators=(",", ":")),
    }
    html = TEMPLATE
    for k, v in repl.items():
        html = html.replace(k, v)
    out = SUM / "Treasure Valley - Development Opportunity Summary Map.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.name}  ({len(html.encode())/1048576:.1f} MB, {len(fc['features'])} sections)")


if __name__ == "__main__":
    main()
