"""Build the combined 'Development-Opportunity Summary' interactive map (self-contained HTML)
covering BOTH subjects. Sections colored by synthesis category; click any section for detail
(acres, zoning, FLU, and — where researched — owner / since / who / intent / status / sources);
interactive legend with per-subject acre totals; two subject pins; satellite/light basemaps."""
import json
from pathlib import Path

BASE = Path("/home/user/Boise-Deals")
SUM = BASE / "summary"
VENDOR = BASE / "land-use-analysis" / "assets" / "vendor"

CATS = [  # key, label, color, tier, why-it-matters
    ("apartments", "Competing apartments — built / approved / proposed", "#E22726", "feature",
     "New multifamily that competes directly with the subject for renters."),
    ("apt_ready", "Apartment-ready land — available", "#F6851F", "feature",
     "Vacant land where apartments could be built by-right or via a likely rezone — latent competitive supply."),
    ("mpc_res", "Active master-planned residential", "#E0559E", "feature",
     "Large communities under construction — mostly for-sale, but they add rooftops and some attached/MF."),
    ("micron", "Micron — campus & expansion", "#8E44AD", "feature",
     "Micron's semiconductor campus & expansion — removes land from housing and drives rental demand."),
    ("airport", "Airport & Influence Area — no new housing", "#3E6DAE", "feature",
     "Boise Airport / Influence Area Zones B & C, where new housing is prohibited — this land can never become apartments."),
    ("industry", "Industrial / employment (non-Micron)", "#4B4F57", "feature",
     "Industrial / employment land — not available for housing."),
    ("rural", "Rural / foothills / land-bank — long-term", "#B9964A", "feature",
     "Rural, foothills, or land-banked ground — constrained or long-term; not near-term apartment supply."),
    ("commercial", "Commercial / retail", "#8FA6B8", "context",
     "Retail / commercial — apartments only if it redevelops as mixed-use."),
    ("civic", "Parks / open space / civic / institutional", "#8FB89A", "context",
     "Parks, open space, schools, HOA commons — not developable."),
    ("established", "Established neighborhoods (built-out)", "#DED9CB", "context",
     "Built-out neighborhoods — existing rooftops, not new competitive supply."),
]
SUBJECTS = [("Canyon Ridge", 43.541734, -116.151198, "#3E6E9C"),
            ("Seasons at Meridian", 43.591935, -116.360877, "#C0692A")]

TEMPLATE = r"""<title>Treasure Valley — Development-Opportunity Summary Map</title>
<style>__LEAFLET_CSS__</style>
<style>
:root{--ink:#15202b;--muted:#5b6673;--pane:#ffffff;--hair:#e2e7ec;--bg:#eef1f4;}
*{box-sizing:border-box} html,body{height:100%;margin:0}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
#app{position:fixed;inset:0;display:grid;grid-template-columns:1fr 380px;grid-template-rows:auto 1fr}
header{grid-column:1/3;background:#0f1720;color:#fff;padding:10px 18px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;z-index:1000}
header h1{font-family:Charter,"Iowan Old Style",Palatino,Georgia,serif;font-size:18px;margin:0;font-weight:700}
header .sub{font-size:12.5px;color:#aeb9c4;max-width:60ch}
header .toggles{margin-left:auto;display:flex;gap:6px}
header button{background:#1e2a36;color:#cdd6df;border:1px solid #2c3a48;border-radius:6px;padding:5px 11px;font-size:12px;cursor:pointer;font-family:inherit}
header button.on{background:#fff;color:#0f1720;border-color:#fff}
#map{grid-column:1;grid-row:2;height:100%}
#side{grid-column:2;grid-row:2;background:var(--pane);border-left:1px solid var(--hair);overflow-y:auto}
@media(max-width:820px){#app{grid-template-columns:1fr} #side{position:absolute;right:0;top:0;bottom:0;width:90%;max-width:380px;box-shadow:-8px 0 24px #0003;transform:translateX(102%);transition:.25s;z-index:1200} #side.open{transform:none}}
.legend{padding:14px 16px}
.legend h2{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
.legend .hint{font-size:11.5px;color:var(--muted);margin:0 0 10px}
.row{display:flex;align-items:center;gap:9px;padding:6px;border-radius:7px;cursor:pointer;user-select:none}
.row:hover{background:#f2f5f8} .row.off{opacity:.4}
.sw{width:15px;height:15px;border-radius:4px;flex:0 0 auto;border:1px solid #0002}
.row .lab{font-size:12.6px;line-height:1.15;flex:1}
.row .ac{font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.row .ac b{color:var(--ink)}
.legdiv{height:1px;background:var(--hair);margin:8px 4px}
.detail{padding:16px 18px;display:none;border-top:3px solid var(--hair)}
.detail.show{display:block}
.detail .cat{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:#fff;padding:3px 10px;border-radius:20px}
.detail h3{font-family:Charter,Palatino,Georgia,serif;font-size:18px;margin:12px 0 2px;line-height:1.24}
.detail .subj{font-size:12px;color:var(--muted);margin-bottom:12px}
.detail .big{display:flex;gap:22px;margin:6px 0 12px}
.detail .big div{font-size:12px;color:var(--muted)}
.detail .big b{display:block;font-size:20px;color:var(--ink);font-variant-numeric:tabular-nums}
.detail .why{font-size:12.5px;color:var(--ink);background:#f4f7fa;border-left:3px solid var(--hair);padding:9px 12px;border-radius:0 8px 8px 0;margin-bottom:12px}
.detail dl{margin:0;font-size:13px;display:grid;grid-template-columns:80px 1fr;gap:6px 10px}
.detail dt{color:var(--muted);font-weight:600} .detail dd{margin:0}
.detail .kv{font-size:12.5px;margin:6px 0} .detail .kv b{color:var(--muted);font-weight:600}
.detail .src{margin-top:12px;padding-top:10px;border-top:1px solid var(--hair);font-size:11px;color:var(--muted);word-break:break-word}
.detail .src a{color:#2f6fb0;text-decoration:none}
.detail .close{float:right;cursor:pointer;color:var(--muted);font-size:22px;line-height:1;border:none;background:none}
.leaflet-tooltip.tt{font-size:12px;font-weight:600;background:#0f1720;color:#fff;border:none;box-shadow:0 2px 8px #0004;padding:4px 8px}
.leaflet-tooltip.tt:before{display:none}
.status-chip{display:inline-block;font-size:10.5px;font-weight:700;text-transform:uppercase;color:#fff;padding:2px 8px;border-radius:20px;margin-left:8px;vertical-align:middle}
</style>
<div id="app">
  <header>
    <h1>Treasure Valley — Development-Opportunity Summary</h1>
    <span class="sub">Canyon Ridge (SE Boise) &amp; Seasons at Meridian · like-kind parcels dissolved into sections · click any section for full detail</span>
    <div class="toggles">
      <button id="b-sat" class="on">Satellite</button>
      <button id="b-light">Light</button>
      <button id="b-cr">Canyon Ridge</button>
      <button id="b-sm">Seasons</button>
    </div>
  </header>
  <div id="map"></div>
  <aside id="side"><div class="legend" id="legend"></div><div class="detail" id="detail"></div></aside>
</div>
<script>__LEAFLET_JS__</script>
<script>
const CATS=__CATS__, TOT=__TOT__, SUBJ=__SUBJ__, DATA=__DATA__;
const catByK={}; CATS.forEach((c,i)=>{catByK[c.k]={label:c.label,color:c.color,tier:c.tier,why:c.why,i:i};});
const off=new Set();
const map=L.map('map',{preferCanvas:true,zoomControl:true}).setView([43.567,-116.255],12);
const TILES={sat:['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}','Esri, Maxar'],
 light:['https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}','Esri']};
let base=null;
function setBase(k){ if(base)map.removeLayer(base); base=L.tileLayer(TILES[k][0],{maxZoom:19,attribution:TILES[k][1]}).addTo(map); base.bringToBack();
  document.getElementById('b-sat').classList.toggle('on',k==='sat'); document.getElementById('b-light').classList.toggle('on',k==='light'); }
setBase('sat');
function style(f){ const c=catByK[f.properties.cat], feat=c.tier==='feature';
  return {color:feat?'#101d29':'#6b7883', weight:feat?0.8:0.3, fillColor:c.color,
   fillOpacity: off.has(f.properties.cat)?0:(feat?0.88:0.40)}; }
const STCOL={approved:'#2e8259',construction:'#2f6fb0',proposed:'#c08a16',built:'#6e7a88',denied:'#ab4630',dormant:'#8a8f98'};
function stChip(s){ if(!s)return''; const t=s.toLowerCase(); let k='dormant';
  if(t.indexOf('approv')>=0)k='approved'; else if(t.indexOf('constr')>=0||t.indexOf('under')>=0)k='construction';
  else if(t.indexOf('propos')>=0||t.indexOf('plan')>=0||t.indexOf('entitl')>=0||t.indexOf('pre-app')>=0)k='proposed';
  else if(t.indexOf('denied')>=0)k='denied'; else if(t.indexOf('built')>=0)k='built';
  return '<span class="status-chip" style="background:'+STCOL[k]+'">'+s.split(/[;(]/)[0].trim().slice(0,24)+'</span>'; }
const layer=L.geoJSON(DATA,{style, onEachFeature:function(f,l){
  l.bindTooltip(catByK[f.properties.cat].label.split('—')[0].trim()+' · '+Math.round(f.properties.acres).toLocaleString()+' ac',{className:'tt',sticky:true});
  l.on('click',function(){showDetail(f.properties);});
}}).addTo(map);
SUBJ.forEach(function(s){ L.circleMarker([s.lat,s.lon],{radius:9,color:'#fff',weight:3,fillColor:s.color,fillOpacity:1})
  .addTo(map).bindTooltip('<b>'+s.name+'</b>',{permanent:true,direction:'top',className:'tt',offset:[0,-8]}); });
function fnum(n){return n==null?'—':Number(n).toLocaleString(undefined,{maximumFractionDigits:0});}
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
function hideDetail(){ document.getElementById('detail').classList.remove('show'); document.getElementById('side').classList.remove('open'); }
function drawLegend(){
  function rowsFor(list){ return list.map(function(c){
    const t=TOT[c.k]||{}, cr=t['Canyon Ridge']||0, sm=t['Seasons at Meridian']||0;
    return '<div class="row'+(off.has(c.k)?' off':'')+'" data-k="'+c.k+'"><span class="sw" style="background:'+c.color+'"></span>'+
      '<span class="lab">'+c.label+'</span><span class="ac">CR <b>'+fnum(cr)+'</b><br>SM <b>'+fnum(sm)+'</b></span></div>'; }).join(''); }
  const feats=CATS.filter(function(c){return c.tier==='feature';}), ctx=CATS.filter(function(c){return c.tier==='context';});
  document.getElementById('legend').innerHTML='<h2>What governs apartment supply</h2>'+
    '<p class="hint">Acres per area (CR = Canyon Ridge, SM = Seasons). Click a row to hide/show; click a section on the map for detail.</p>'+
    rowsFor(feats)+'<div class="legdiv"></div><h2 style="margin-top:4px">Context</h2>'+rowsFor(ctx);
  Array.prototype.forEach.call(document.querySelectorAll('.row'),function(r){ r.onclick=function(){
    const k=r.getAttribute('data-k'); if(off.has(k))off.delete(k); else off.add(k); r.classList.toggle('off'); layer.setStyle(style); }; });
}
drawLegend();
document.getElementById('b-sat').onclick=function(){setBase('sat');};
document.getElementById('b-light').onclick=function(){setBase('light');};
document.getElementById('b-cr').onclick=function(){map.setView([SUBJ[0].lat,SUBJ[0].lon],13);};
document.getElementById('b-sm').onclick=function(){map.setView([SUBJ[1].lat,SUBJ[1].lon],13);};
map.fitBounds(layer.getBounds(),{padding:[20,20]});
</script>"""


def main():
    fc = json.loads((SUM / "sections.geojson").read_text())
    summ = json.loads((SUM / "sections_summary.json").read_text())
    totals = {c[0]: summ.get(c[0], {}).get("by_subject", {}) for c in CATS}
    repl = {
        "__LEAFLET_CSS__": (VENDOR / "leaflet.css").read_text(),
        "__LEAFLET_JS__": (VENDOR / "leaflet.js").read_text(),
        "__CATS__": json.dumps([{"k": c[0], "label": c[1], "color": c[2], "tier": c[3], "why": c[4]} for c in CATS]),
        "__TOT__": json.dumps(totals),
        "__SUBJ__": json.dumps([{"name": s[0], "lat": s[1], "lon": s[2], "color": s[3]} for s in SUBJECTS]),
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
