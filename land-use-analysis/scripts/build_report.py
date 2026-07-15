"""Generate the head-to-head developable-land comparison report (self-contained HTML) from
comparison/report_data.json. A professional land-intelligence brief: verdict, scorecard,
supply charts, and all researched ownership/intent dossiers. Theme-aware; no external assets."""
import html
import json
from pathlib import Path

BASE = Path("/home/user/Boise-Deals")
D = json.load(open(BASE / "comparison" / "report_data.json"))
comp, dossiers = D["comp"], D["dossiers"]
CR, SM = comp["CanyonRidge"], comp["SeasonsMeridian"]
# synthesis-map category rollup (acres by subject) + the interactive map's URL (if published)
_ss = BASE / "summary" / "sections_summary.json"
SECT = json.load(open(_ss)) if _ss.exists() else {}
_mu = BASE / "summary" / "map_url.txt"
MAP_URL = _mu.read_text().strip() if _mu.exists() else ""


def sect_ac(cat, subj):
    return (SECT.get(cat, {}).get("by_subject", {}) or {}).get(subj, 0) or 0


def esc(s):
    return html.escape(str(s if s is not None else ""))


def status_bucket(s):
    t = str(s or "").lower()
    if "denied" in t:
        return ("denied", "Denied")
    if "under_constr" in t or "under constr" in t or "under-constr" in t:
        return ("uc", "Under construction")
    if "approv" in t:
        return ("approved", "Approved")
    if "propos" in t or "pre-app" in t or "planned" in t or "entitled" in t:
        return ("proposed", "Proposed / planned")
    if "built" in t:
        return ("built", "Built / existing")
    return ("dormant", "Dormant / none")


def fnum(x):
    try:
        return f"{float(x):,.0f}"
    except (TypeError, ValueError):
        return "—"


# ---- derived headline metrics ----
def m(sub, key):
    return sub[key]


cr_ar, sm_ar = CR["apartment_ready"], SM["apartment_ready"]
cr_ar2, sm_ar2 = CR["apartment_ready_2mi"], SM["apartment_ready_2mi"]
ratio_ar = round(sm_ar["acres"] / cr_ar["acres"], 1) if cr_ar["acres"] else 0
ratio_2mi = round(sm_ar2["acres"] / cr_ar2["acres"], 1) if cr_ar2["acres"] else 0

# ---- FLU-intent bars (residential-intensification acreage) ----
INTENT_ORDER = [
    ("supports multifamily", "Planned for multifamily", "mf"),
    ("supports attached/medium", "Planned attached / medium-density", "med"),
    ("single-family oriented", "Single-family oriented", "sf"),
    ("master-plan (use TBD)", "Master-plan (use TBD)", "tbd"),
    ("development-ready, use TBD", "Development-ready (use TBD)", "tbd"),
    ("non-residential (MF only if mixed)", "Commercial (MF only if mixed-use)", "com"),
    ("non-residential", "Industrial / employment", "ind"),
    ("airport — residential restricted", "Airport — residential restricted", "air"),
    ("low-density / rural", "Rural / low-density", "rur"),
    ("institutional", "Institutional / civic", "inst"),
]


def intent_ac(sub, key):
    return sub["by_intent"].get(key, {}).get("acres", 0) or 0


maxbar = max(max(intent_ac(CR, k), intent_ac(SM, k)) for k, _, _ in INTENT_ORDER)


def bar_rows():
    out = []
    for key, label, cls in INTENT_ORDER:
        cav, sav = intent_ac(CR, key), intent_ac(SM, key)
        cw = round(100 * cav / maxbar, 2) if maxbar else 0
        sw = round(100 * sav / maxbar, 2) if maxbar else 0
        out.append(f"""<div class="bar-row">
      <div class="bar-label">{esc(label)}</div>
      <div class="bar-track"><div class="bar cr" style="width:{cw}%"></div><span class="bar-val">{fnum(cav)} ac</span></div>
      <div class="bar-track"><div class="bar sm" style="width:{sw}%"></div><span class="bar-val">{fnum(sav)} ac</span></div>
    </div>""")
    return "\n".join(out)


# ---- dossier cards ----
def card(d):
    b, blabel = status_bucket(d.get("project_status"))
    subj = "CR" if d["subject"] == "CanyonRidge" else "SM"
    acres = fnum(d.get("acres"))
    srcs = d.get("sources") or []
    src_html = ""
    if isinstance(srcs, list) and srcs:
        links = " · ".join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(u.split("/")[2] if "//" in u else u)}</a>'
                           for u in srcs[:5])
        src_html = f'<div class="src">Sources: {links}</div>'
    dist = d.get("dist_mi")
    dist_s = f"{dist} mi" if dist is not None else "—"
    return f"""<article class="card {subj.lower()}" data-status="{b}" data-subj="{subj}">
    <header>
      <span class="chip subj {subj.lower()}">{('Canyon Ridge' if subj=='CR' else 'Seasons')}</span>
      <span class="chip status {b}">{esc(blabel)}</span>
      <span class="dist">{dist_s} from subject</span>
    </header>
    <h3>{esc(d.get('address'))}</h3>
    <div class="meta">{acres} ac · {esc(d.get('zoning') or '—')} · FLU: {esc(d.get('future_land_use') or '—')}</div>
    <dl>
      <dt>Owner</dt><dd>{esc(d.get('owner_name'))}</dd>
      <dt>Type</dt><dd>{esc(d.get('owner_type'))}</dd>
      <dt>Owned since</dt><dd>{esc(d.get('ownership_since'))}</dd>
      <dt>Who they are</dt><dd>{esc(d.get('who_they_are'))}</dd>
      <dt>Intent</dt><dd>{esc(d.get('intent_summary'))}</dd>
    </dl>
    {src_html}
  </article>"""


cr_cards = "\n".join(card(d) for d in sorted([x for x in dossiers if x["subject"] == "CanyonRidge"],
                     key=lambda x: (x.get("dist_mi") or 9)))
sm_cards = "\n".join(card(d) for d in sorted([x for x in dossiers if x["subject"] == "SeasonsMeridian"],
                     key=lambda x: (x.get("dist_mi") or 9)))

CSS = """
:root{
  --paper:#f3f5f7; --surface:#ffffff; --ink:#161b22; --muted:#5b6672; --hair:#dce1e7;
  --cr:#40639e; --cr-soft:#40639e1a; --sm:#c0692a; --sm-soft:#c0692a1a; --brass:#957327;
  --g:#2f7d57; --b:#2f6fb0; --a:#b7860f; --gray:#6e7a88; --red:#ab4630;
  --shadow:0 1px 2px #0b153008,0 6px 20px #0b153010;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0e141a; --surface:#161d26; --ink:#e7edf3; --muted:#93a0ae; --hair:#26313f;
  --cr:#8aa9e6; --cr-soft:#8aa9e622; --sm:#e6a05a; --sm-soft:#e6a05a22; --brass:#c8a555;
  --g:#4bb487; --b:#5b9ad8; --a:#d8ab48; --gray:#8c99a8; --red:#d9745c;
  --shadow:0 1px 2px #0000004d,0 8px 30px #00000040;
}}
:root[data-theme="light"]{
  --paper:#f3f5f7; --surface:#ffffff; --ink:#161b22; --muted:#5b6672; --hair:#dce1e7;
  --cr:#40639e; --cr-soft:#40639e1a; --sm:#c0692a; --sm-soft:#c0692a1a; --brass:#957327;
  --g:#2f7d57; --b:#2f6fb0; --a:#b7860f; --gray:#6e7a88; --red:#ab4630;
}
:root[data-theme="dark"]{
  --paper:#0e141a; --surface:#161d26; --ink:#e7edf3; --muted:#93a0ae; --hair:#26313f;
  --cr:#8aa9e6; --cr-soft:#8aa9e622; --sm:#e6a05a; --sm-soft:#e6a05a22; --brass:#c8a555;
  --g:#4bb487; --b:#5b9ad8; --a:#d8ab48; --gray:#8c99a8; --red:#d9745c;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Söhne",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.5;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums;}
.wrap{max-width:1080px;margin:0 auto;padding:clamp(20px,4vw,56px) clamp(16px,4vw,40px)}
.serif{font-family:Charter,"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);font-weight:600}
h1{font-family:Charter,"Iowan Old Style",Palatino,Georgia,serif;font-weight:700;
  font-size:clamp(30px,5vw,50px);line-height:1.06;margin:.3em 0 .2em;text-wrap:balance;letter-spacing:-.01em}
.standfirst{font-size:clamp(17px,2.2vw,21px);color:var(--ink);max-width:64ch;margin:.4em 0 0;line-height:1.45}
.standfirst b{color:var(--sm)}
.dateline{color:var(--muted);font-size:13px;margin-top:18px;border-top:1px solid var(--hair);padding-top:14px}
h2{font-family:Charter,"Iowan Old Style",Palatino,Georgia,serif;font-size:clamp(22px,3vw,30px);
  margin:2.4em 0 .1em;letter-spacing:-.01em}
.sec-intro{color:var(--muted);max-width:70ch;margin:.2em 0 1.4em}
section{border-top:1px solid var(--hair);margin-top:2.2em;padding-top:.6em}
/* scorecard */
.score{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:1.2em 0}
@media(max-width:640px){.score{grid-template-columns:1fr}}
.col{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:20px 22px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.col::before{content:"";position:absolute;inset:0 auto 0 0;width:5px}
.col.cr::before{background:var(--cr)}.col.sm::before{background:var(--sm)}
.col h3{margin:.1em 0 .1em;font-size:19px;font-family:Charter,Palatino,Georgia,serif}
.col.cr h3{color:var(--cr)}.col.sm h3{color:var(--sm)}
.col .sub{color:var(--muted);font-size:13px;margin-bottom:14px}
.stat{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:9px 0;border-top:1px dotted var(--hair)}
.stat .k{color:var(--muted);font-size:13.5px}
.stat .v{font-weight:650;font-size:16px;font-variant-numeric:tabular-nums;text-align:right}
.stat .v small{color:var(--muted);font-weight:500;font-size:12px}
.hero-stat .v{font-size:22px}.col.cr .hero-stat .v{color:var(--cr)}.col.sm .hero-stat .v{color:var(--sm)}
/* verdict callout */
.callout{background:var(--sm-soft);border:1px solid var(--sm);border-radius:12px;padding:18px 22px;margin:1.4em 0;font-size:16px}
.callout .big{font-family:Charter,Palatino,Georgia,serif;font-size:clamp(20px,3vw,26px);color:var(--sm);font-weight:700;display:block;margin-bottom:.2em}
/* bar chart */
.legend{display:flex;gap:18px;align-items:center;margin:.4em 0 1.1em;font-size:13px;color:var(--muted);flex-wrap:wrap}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:6px}
.sw.cr{background:var(--cr)}.sw.sm{background:var(--sm)}
.chart{display:flex;flex-direction:column;gap:12px;overflow-x:auto}
.bar-row{display:grid;grid-template-columns:210px 1fr 1fr;gap:10px;align-items:center;min-width:560px}
@media(max-width:640px){.bar-row{grid-template-columns:130px 1fr 1fr}}
.bar-label{font-size:13px;color:var(--ink);text-align:right;line-height:1.2}
.bar-track{position:relative;background:var(--hair);border-radius:5px;height:26px;overflow:hidden;display:flex;align-items:center}
.bar{height:100%;border-radius:5px 0 0 5px;min-width:2px}
.bar.cr{background:var(--cr)}.bar.sm{background:var(--sm)}
.bar-val{position:absolute;right:8px;font-size:12px;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:600;mix-blend-mode:normal}
/* filters */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:1em 0 1.4em}
.filt{border:1px solid var(--hair);background:var(--surface);color:var(--muted);border-radius:20px;
  padding:6px 14px;font-size:13px;cursor:pointer;font-family:inherit;transition:.15s}
.filt[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.filt:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
/* dossier grid */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.grid{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:18px 20px;
  box-shadow:var(--shadow);border-left:4px solid var(--gray)}
.card.cr{border-left-color:var(--cr)}.card.sm{border-left-color:var(--sm)}
.card header{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.card h3{margin:.1em 0 .2em;font-size:16.5px;font-family:Charter,Palatino,Georgia,serif;line-height:1.25}
.card .meta{font-size:12.5px;color:var(--muted);margin-bottom:12px;line-height:1.4}
.chip{font-size:11px;letter-spacing:.03em;padding:3px 9px;border-radius:20px;font-weight:600;text-transform:uppercase}
.chip.subj.cr{background:var(--cr-soft);color:var(--cr)}.chip.subj.sm{background:var(--sm-soft);color:var(--sm)}
.chip.status{color:#fff}
.chip.status.approved{background:var(--g)}.chip.status.uc{background:var(--b)}
.chip.status.proposed{background:var(--a)}.chip.status.built{background:var(--gray)}
.chip.status.dormant{background:var(--gray);opacity:.75}.chip.status.denied{background:var(--red)}
.dist{margin-left:auto;font-size:11.5px;color:var(--muted);font-variant-numeric:tabular-nums}
dl{margin:0;display:grid;grid-template-columns:88px 1fr;gap:5px 12px;font-size:13.5px}
dt{color:var(--muted);font-weight:600}dd{margin:0}
.src{margin-top:12px;padding-top:10px;border-top:1px dotted var(--hair);font-size:11.5px;color:var(--muted);word-break:break-word}
.src a{color:var(--brass);text-decoration:none}.src a:hover{text-decoration:underline}
.note{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:16px 20px;font-size:13.5px;color:var(--muted);margin-top:1.2em}
.note b{color:var(--ink)}
footer{margin-top:3em;padding-top:1.2em;border-top:1px solid var(--hair);color:var(--muted);font-size:12.5px}
a.inline{color:var(--brass)}
.hide{display:none!important}
.maplink{display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px;margin:0 0 16px}
.maplink a{font-size:15px;font-weight:650;color:#fff;background:var(--sm);padding:9px 16px;border-radius:9px;text-decoration:none}
.maplink a:hover{filter:brightness(1.06)}
.maplink span{font-size:12.5px;color:var(--muted)}
table.synth{border-collapse:collapse;width:100%;font-size:13.5px;margin:.4em 0}
table.synth th,table.synth td{border-bottom:1px solid var(--hair);padding:8px 10px;text-align:left}
table.synth th.cr,table.synth td.cr{color:var(--cr)} table.synth th.sm,table.synth td.sm{color:var(--sm)}
table.synth th.cr,table.synth th.sm{text-align:right} table.synth td.n{text-align:right;font-variant-numeric:tabular-nums;font-weight:650}
table.synth thead th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
table.synth .rh{display:block;font-size:11px;color:var(--muted);font-weight:400}
table.synth tr:has(td:first-child) td:first-child{font-weight:500}
"""


def _srow(label, cr, sm, hint=""):
    return (f'<tr><td>{esc(label)}<span class="rh">{esc(hint)}</span></td>'
            f'<td class="n cr">{fnum(cr)}</td><td class="n sm">{fnum(sm)}</td></tr>')


CRc = "Canyon Ridge"
SMc = "Seasons at Meridian"
apt_cr = sect_ac("apartments", CRc) + sect_ac("apt_ready", CRc)
apt_sm = sect_ac("apartments", SMc) + sect_ac("apt_ready", SMc)
offl_cr = sum(sect_ac(k, CRc) for k in ("micron", "airport_land", "airport", "industry"))
offl_sm = sum(sect_ac(k, SMc) for k in ("micron", "airport_land", "airport", "industry"))
summary_html = (f'''
<section>
<h2 class="serif">One map: where apartments can &amp; can't go</h2>
<p class="sec-intro">The same parcels, reframed. Instead of raw zoning, every parcel is sorted into what actually
governs apartment supply — competing/ready apartment land, Micron's campus, the airport &amp; its influence-area
"moat" where new housing is barred, industrial land, long-term land-bank, and context — then like-kind parcels are
dissolved into labeled sections you can click for owner &amp; intent. It makes the difference between the two areas
legible at a glance.</p>
<div class="maplink">
  <a href="{esc(MAP_URL) if MAP_URL else '#'}" target="_blank" rel="noopener">Open the interactive summary map →</a>
  <span>Both study areas · click any section for detail · toggle categories</span>
</div>
<table class="synth"><thead><tr><th>Land role (acres, 5-mi radius)</th><th class="cr">Canyon&nbsp;Ridge</th><th class="sm">Seasons</th></tr></thead>
<tbody>
{_srow("Competing apartments (built / approved / proposed)", sect_ac("apartments", CRc), sect_ac("apartments", SMc))}
{_srow("Apartment-ready land (available now)", sect_ac("apt_ready", CRc), sect_ac("apt_ready", SMc))}
{_srow("Active master-planned residential", sect_ac("mpc_res", CRc), sect_ac("mpc_res", SMc))}
{_srow("→ Apartment-capable subtotal", apt_cr, apt_sm, "built + ready")}
{_srow("Land-bank / future growth (long-term)", sect_ac("landbank", CRc), sect_ac("landbank", SMc))}
{_srow("Off-limits to new housing", offl_cr, offl_sm, "Micron + airport + industry")}
</tbody></table>
<p class="sec-intro" style="margin-top:.8em">Canyon Ridge sits behind ~{fnum(offl_cr)} acres of off-limits land (airport, Micron,
industry) with only <b style="color:var(--cr)">{fnum(apt_cr)} acres</b> that can host new apartments; Seasons has
<b>{fnum(apt_sm)} acres</b> — roughly <b>{round(apt_sm / apt_cr) if apt_cr else '—'}×</b> more.</p>
</section>
''')

HTMLDOC = f"""<title>Canyon Ridge vs Seasons — Developable Land</title>
<style>{CSS}</style>
<div class="wrap">
<header>
  <div class="eyebrow">Competitive Land-Use Intelligence · Treasure Valley, Idaho</div>
  <h1 class="serif">Where the developable land is — and who controls it</h1>
  <p class="standfirst">A parcel-level comparison of buildable land around two apartment communities:
  <b style="color:var(--cr)">Canyon Ridge</b> (SE Boise, by the airport) and
  <b>Seasons at Meridian</b>. Both sit inside a 5-mile radius; only one sits inside the region's
  apartment-building machine.</p>
  <div class="dateline">Prepared 14 July 2026 · 5.0-mi radius each · {fnum(CR['total_parcels'])} + {fnum(SM['total_parcels'])} parcels classified ·
  Ada County Assessor + 7-jurisdiction zoning + adopted Future Land Use + per-site ownership research</div>
</header>

<div class="callout">
  <span class="big">Seasons has ~{ratio_ar}× the apartment-ready land — and it's already being built.</span>
  Within 5 miles, <b>{fnum(sm_ar['acres'])} acres</b> of developable land near Seasons is zoned or planned for
  multifamily, versus <b>{fnum(cr_ar['acres'])} acres</b> near Canyon Ridge. Within 2 miles the gap is starker
  ({fnum(sm_ar2['acres'])} vs {fnum(cr_ar2['acres'])} ac, ~{ratio_2mi}×). Canyon Ridge's larger <i>raw</i> vacant
  acreage is Micron's fabs, the Boise Airport, city-owned industrial parks and rural rangeland — almost none of it
  can legally or practically become competing apartments.
</div>
{summary_html}
<section>
<h2 class="serif">Scorecard</h2>
<p class="sec-intro">"Developable" here means genuinely buildable vacant land — after removing HOA/common lots,
detention & irrigation parcels, floodplain, road slivers, sub-1-acre lots and non-buildable open space.
"Apartment-ready" = base zoning permits multifamily <i>or</i> the adopted comprehensive plan designates the
parcel for multifamily.</p>
<div class="score">
  <div class="col cr">
    <h3>Canyon Ridge</h3>
    <div class="sub">2552 E Gowen Rd, SE Boise · inside the Airport Influence Area</div>
    <div class="stat hero-stat"><span class="k">Apartment-ready developable land</span><span class="v">{fnum(cr_ar['acres'])} ac <small>/ {cr_ar['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">…within 2 miles</span><span class="v">{fnum(cr_ar2['acres'])} ac <small>/ {cr_ar2['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">Total developable vacant</span><span class="v">{fnum(CR['total_dev']['acres'])} ac <small>/ {CR['total_dev']['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">MF by-right (High) land</span><span class="v">{fnum(CR['by_threat'].get('High',{}).get('acres',0))} ac</span></div>
    <div class="stat"><span class="k">Owner-occupied homes</span><span class="v">{fnum(CR['owner_occupied'])}</span></div>
    <div class="stat"><span class="k">Active residential/apartment pipeline</span><span class="v">Minimal</span></div>
  </div>
  <div class="col sm">
    <h3>Seasons at Meridian</h3>
    <div class="sub">2700 E Overland Rd, SE Meridian · no airport overlay</div>
    <div class="stat hero-stat"><span class="k">Apartment-ready developable land</span><span class="v">{fnum(sm_ar['acres'])} ac <small>/ {sm_ar['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">…within 2 miles</span><span class="v">{fnum(sm_ar2['acres'])} ac <small>/ {sm_ar2['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">Total developable vacant</span><span class="v">{fnum(SM['total_dev']['acres'])} ac <small>/ {SM['total_dev']['parcels']} parcels</small></span></div>
    <div class="stat"><span class="k">MF by-right (High) land</span><span class="v">{fnum(SM['by_threat'].get('High',{}).get('acres',0))} ac</span></div>
    <div class="stat"><span class="k">Owner-occupied homes</span><span class="v">{fnum(SM['owner_occupied'])}</span></div>
    <div class="stat"><span class="k">Active residential/apartment pipeline</span><span class="v">Heavy &amp; ongoing</span></div>
  </div>
</div>
</section>

<section>
<h2 class="serif">Developable land, by what it can actually become</h2>
<p class="sec-intro">Total acreage misleads. Sorting each area's developable vacant land by its comprehensive-plan
intent shows the real difference: Seasons' supply is weighted toward multifamily and attached housing;
Canyon Ridge's is weighted toward airport-restricted, industrial and rural land that cannot host apartments.</p>
<div class="legend"><span><span class="sw cr"></span>Canyon Ridge</span><span><span class="sw sm"></span>Seasons at Meridian</span><span>· acres of developable vacant land</span></div>
<div class="chart">
{bar_rows()}
</div>
</section>

<section>
<h2 class="serif">Ownership &amp; development intent — every material site</h2>
<p class="sec-intro">Who owns each developable site, since when, who they are, and what they plan. Idaho does not
publish parcel owner names in the public GIS, so ownership and intent are researched per site from development
applications, city staff reports, COMPASS filings, local reporting and the Idaho business registry — each card
cites its sources. Filter by status:</p>
<div class="filters" id="filters">
  <button class="filt" data-f="all" aria-pressed="true">All 30 sites</button>
  <button class="filt" data-f="CR" aria-pressed="false">Canyon Ridge (14)</button>
  <button class="filt" data-f="SM" aria-pressed="false">Seasons (16)</button>
  <button class="filt" data-f="approved" aria-pressed="false">Approved</button>
  <button class="filt" data-f="uc" aria-pressed="false">Under construction</button>
  <button class="filt" data-f="proposed" aria-pressed="false">Proposed</button>
  <button class="filt" data-f="dormant" aria-pressed="false">Dormant</button>
</div>

<h3 class="serif" style="color:var(--cr);margin:.6em 0 .2em">Canyon Ridge — SE Boise</h3>
<div class="grid" id="cr-grid">
{cr_cards}
</div>

<h3 class="serif" style="color:var(--sm);margin:1.6em 0 .2em">Seasons at Meridian</h3>
<div class="grid" id="sm-grid">
{sm_cards}
</div>
</section>

<section>
<h2 class="serif">What this means</h2>
<p class="sec-intro" style="max-width:74ch;color:var(--ink)">
Near <b style="color:var(--cr)">Canyon Ridge</b>, the "developable land" is dominated by uses that will never
compete for renters: Micron's expanding chip fabs and the surrounding Simplot/rangeland (planned for ~20,000 future
homes but <i>stalled</i> for lack of a second wildfire-evacuation road), the Boise Airport and its
Airport-Influence-Area overlay that <i>prohibits</i> new housing, city-owned Gateway East industrial parks
(Boyer, Flint), and foothills land now being converted to open space. The handful of genuinely multifamily-zoned
vacant parcels are mostly false positives — an existing apartment complex's pond, an HOA common lot — with the one
real opportunity being the Barber Valley / Harris Ranch town center, ~4 miles north.</p>
<p class="sec-intro" style="max-width:74ch;color:var(--ink)">
Near <b style="color:var(--sm)">Seasons at Meridian</b>, the developable land is the Treasure Valley's actual
housing engine. It is controlled by active master developers — <b>Brighton Corporation</b> (Ten Mile Crossing and
the 800-acre Pinnacle/Apex community with a rumored Costco town center), <b>Ball Ventures Ahlquist</b>,
<b>Hawkins Companies</b>, <b>Quarterra/Lennar</b>, <b>CBH Homes</b>, <b>Star Development</b> and others — with
thousands of homes and a stack of apartment projects already built, approved, or in the pipeline (Aren 396 units,
The Flats 235, Outer Banks 516, Graycliff 224, Tanner Creek 280, Emblem 250, the Overland/Assemble 200, and more).
For an apartment owner, Seasons faces materially more competitive new-supply risk; Canyon Ridge is unusually
insulated by the airport, industry and terrain.</p>
</section>

<section>
<h2 class="serif">Method &amp; data</h2>
<div class="note">
<b>Coverage.</b> Ada County Assessor parcels (28,026 near Canyon Ridge; 92,773 near Seasons), classified by land use
(PROPCODE) and joined to a 7-jurisdiction base-zoning crosswalk (Boise, Meridian, Ada County, Kuna, Eagle, Garden
City, Star — 0 unmapped codes) and to the adopted Future Land Use / comprehensive-plan designation (Boise, Meridian,
Ada County). Each parcel carries land-use bucket, base zoning + multifamily-supply threat, comp-plan designation +
intent, assessor value, homestead (owner-occupancy) and HOA-common flags — see the per-subject Excel workbooks and
interactive map viewers.<br><br>
<b>The owner-data limit (and how it's handled).</b> Idaho does not publish parcel owner names in the free county GIS,
and the county's lookup portal is reCAPTCHA-gated for reference only — so a bulk owner roll is not possible. This
report answers "who owns what, since when, who they are, and what they'll do with it" by <b>researching the material
developable sites individually</b> from development applications, city P&amp;Z / Council staff reports, COMPASS filings,
BoiseDev / Idaho Statesman / KTVB reporting and the Idaho Secretary of State registry. Where an owner could not be
identified from public records, it is labeled "not publicly identified" — never fabricated. Confidence and sources are
noted per site.<br><br>
<b>Correction of a prior artifact.</b> An earlier version of this study clustered vacant parcels by owner; because owner
is null, that collapsed into adjacency-only "mega-blobs" (e.g. a single 8,600- and 14,100-acre cluster spanning a dozen
zones). This analysis uses a per-parcel developable inventory with contiguous blocks grouped but not fused, and it
removes HOA/common, detention, floodplain and sliver parcels via the assessor legal text.
</div>
</section>

<footer>
Competitive land-use / developable-land analysis · Canyon Ridge vs Seasons at Meridian · Treasure Valley, ID ·
Sources: AdaCountyGIS (parcels, zoning, future land use), city/county development records, BoiseDev, COMPASS, Idaho SOS.
Ownership/intent findings carry per-site confidence ratings; treat "inferred/derived" owners as leads, not title.
</footer>
</div>
<script>
(function(){{
  var F=document.getElementById('filters');
  var cards=[].slice.call(document.querySelectorAll('.card'));
  F.addEventListener('click',function(e){{
    var b=e.target.closest('.filt'); if(!b) return;
    [].forEach.call(F.children,function(x){{x.setAttribute('aria-pressed', x===b?'true':'false');}});
    var f=b.getAttribute('data-f');
    cards.forEach(function(c){{
      var show = f==='all' || c.getAttribute('data-subj')===f || c.getAttribute('data-status')===f;
      c.classList.toggle('hide', !show);
    }});
    document.querySelectorAll('.grid').forEach(function(g){{
      var any=[].some.call(g.children,function(c){{return !c.classList.contains('hide');}});
      g.previousElementSibling && g.previousElementSibling.tagName==='H3' &&
        (g.previousElementSibling.style.display = any?'':'none');
      g.style.display = any?'':'none';
    }});
  }});
}})();
</script>
"""

out = BASE / "comparison" / "Canyon Ridge vs Seasons - Developable Land Comparison.html"
out.write_text(HTMLDOC, encoding="utf-8")
print(f"wrote {out.name}  ({len(HTMLDOC)//1024} KB)")
