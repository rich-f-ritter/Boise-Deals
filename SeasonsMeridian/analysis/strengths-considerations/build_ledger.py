#!/usr/bin/env python3
"""Render 'Seasons at Meridian - Strengths & Considerations.md' into the styled
ledger HTML (published as the Claude artifact), including the H39 migration
exhibit built from employment-drivers/data/placerai (figures recomputed from
the CSVs 8/22/2026 — they tie to the IC-slides exhibit exactly)."""
import re, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, 'Seasons at Meridian - Strengths & Considerations.md')
OUT = os.path.join(HERE, 'seasons_ledger.html')

md = open(MD).read()

def esc(s): return html.escape(s, quote=False)

def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    s = s.replace('ⓦ', '<span class="wtag" title="materially dependent on 8/22/2026 web research">w</span>')
    return s

# ---------------------------------------------------------------- parse md
lines = md.split('\n')
mode = None
header_paras, bottom = [], []
in_bottom = False
sections = {'S': [], 'C': []}
cur = None
for ln in lines:
    t = ln.strip()
    if not t or t == '---' or t.startswith('# '):
        continue
    if t == '## STRENGTHS':
        mode = 'S'; continue
    if t == '## CONSIDERATIONS':
        mode = 'C'; continue
    if t.startswith('### Bottom line'):
        in_bottom = True; continue
    if in_bottom:
        bottom.append(t); continue
    if t.startswith('### '):
        cur = (t[4:], []); sections[mode].append(cur); continue
    if mode and t.startswith('**'):
        m = re.match(r'\*\*(\S+?)\.\s(.+)$', t)
        if m:
            iid, rest = m.group(1), m.group(2)
            src = ''
            sm = re.search(r'\[([^\[\]]+)\]\s*$', rest)
            if sm:
                src = sm.group(1); rest = rest[:sm.start()].rstrip()
            cm = re.match(r'(.+?)\*\*\s*(.*)$', rest)
            claim, body = (cm.group(1), cm.group(2)) if cm else (rest, '')
            cur[1].append((iid, claim, body, src))
            continue
    if mode is None:
        header_paras.append(t)

# ---------------------------------------------------------------- H39 exhibit
# All figures recomputed from employment-drivers/data/placerai CSVs:
#   growth components = Boise_MSA_Growth_Breakdown_Jun21Jun26.csv, summed on YE-June windows
#   ZIP rows          = population_change_by_zip_Jun25Jun26.csv (+ Jun24Jun26 for prior-yr accel)
#   origin metros     = Boise_MSA_Origin_Destination_Jun25Jun26.csv (+ Jun24Jun26 for prior yr)
YEARS = [('YE Jun-22', 10347, 3469, 1574, 15390, '+2.0%'),
         ('YE Jun-23', 6795, 3320, 2467, 12582, '+1.6%'),
         ('YE Jun-24', 5298, 4071, 2820, 12189, '+1.5%'),
         ('YE Jun-25', 6051, 4130, 2861, 13042, '+1.6%'),
         ('YE Jun-26', 11647, 4208, 2914, 18769, '+2.2%')]
ZIPS = [('83642 · S. Meridian — the subject', '+2,417', '+3.5%', '+1,077 accel.', True),
        ('83687 · N. Nampa', '+1,604', '+3.4%', '+815 accel.', False),
        ('83706 · Boise Bench/BSU', '+1,025', '+2.8%', '+1,095 accel.', False),
        ('83669 · Star', '+836', '+3.6%', '−206', False),
        ('83709 · SW Boise', '+709', '+1.2%', '+835 accel.', False)]
ORIGINS = [('Los Angeles', '+670', '+980', '$96k', 'slowing', False),
           ('San Francisco', '+600', '+229', '$136k', '2.6×', True),
           ('Riverside–San Bern.', '+523', '+541', '$90k', 'steady', False),
           ('Washington DC', '+338', '+166', '$127k', '2.0× — federal exodus', True),
           ('Seattle · Portland · Sacramento', '+801', '+310', '$97–115k', '2.6× combined', True)]

def bars_svg():
    W, H, PADT, PADB = 640, 300, 46, 26
    n = len(YEARS)
    maxv = 19500
    gw = W / n
    bw = 64
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Boise MSA population growth by component, years ending June, 2022 to 2026" style="width:100%;height:auto;display:block">']
    scale = (H - PADT - PADB) / maxv
    for gi, (yr, dom, intl, nat, tot, pct) in enumerate(YEARS):
        x = gi * gw + (gw - bw) / 2
        y = H - PADB
        em = gi == n - 1
        for val, cls in ((dom, 'dom'), (intl, 'intl'), (nat, 'nat')):
            h = val * scale
            y -= h
            parts.append(
                f'<rect class="seg {cls}" x="{x:.1f}" y="{y + 1:.1f}" width="{bw}" height="{max(h - 2, 1):.1f}" rx="2">'
                f'<title>{yr} · {dict(dom="Net domestic migration", intl="International", nat="Natural increase")[cls]}: {val:,}</title></rect>')
        parts.append(f'<text class="tot{" em" if em else ""}" x="{x + bw/2:.1f}" y="{y - 18:.0f}" text-anchor="middle">{tot:+,}</text>')
        parts.append(f'<text class="pct{" em" if em else ""}" x="{x + bw/2:.1f}" y="{y - 6:.0f}" text-anchor="middle">({pct})</text>')
        parts.append(f'<text class="axis" x="{x + bw/2:.1f}" y="{H - 8:.0f}" text-anchor="middle">{yr}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def exhibit():
    zrows = ''.join(
        f'<tr class="{"hl" if hl else ""}"><td class="rank">{i+1}</td><td>{z}</td>'
        f'<td class="num">{net}</td><td class="num">{rate}</td><td class="num">{acc}</td></tr>'
        for i, (z, net, rate, acc, hl) in enumerate(ZIPS))
    orows = ''.join(
        f'<tr><td>{o}</td><td class="num">{net}</td><td class="num">{prior}</td>'
        f'<td class="num">{hhi}</td><td class="{"acc" if acc else ""}">{tr}</td></tr>'
        for o, net, prior, hhi, tr, acc in ORIGINS)
    return f'''<figure class="exhibit">
<figcaption class="ex-head">Exhibit — the H39 migration evidence <span class="ex-sub">recomputed from the Placer.ai device panel CSVs, 8/22/2026</span></figcaption>
<div class="ex-block">
<div class="ex-title">Population growth by component — Boise MSA, years ending June</div>
{bars_svg()}
<div class="legend">
<span><i class="sw dom"></i>Net domestic migration</span>
<span><i class="sw intl"></i>International</span>
<span><i class="sw nat"></i>Natural increase</span>
</div>
<p class="ex-note">The YE Jun-26 re-acceleration (+18,769, the five-year high) is domestic-migration-driven: +11,647 net domestic vs +5,298–+6,795 in the three soft years. Natural increase and international inflow are steady ballast (~7,000/yr combined).</p>
</div>
<div class="ex-block">
<div class="ex-title">Top in-migration ZIPs, Treasure Valley — YE Jun-26</div>
<div class="tbl-wrap"><table>
<thead><tr><th>#</th><th>ZIP · Area</th><th class="num">Net in-mig.</th><th class="num">Rate</th><th class="num">vs prior yr</th></tr></thead>
<tbody>{zrows}</tbody></table></div>
<p class="ex-note">The subject’s own ZIP (83642) is the metro’s #1 net in-migration ZIP by volume — and its inflow nearly doubled year-over-year.</p>
</div>
<div class="ex-block">
<div class="ex-title">Where they come from — top origin metros, net YE Jun-26 vs prior year</div>
<div class="tbl-wrap"><table>
<thead><tr><th>Origin</th><th class="num">Net</th><th class="num">Prior yr</th><th class="num">Origin MHHI</th><th>Trend</th></tr></thead>
<tbody>{orows}</tbody></table></div>
<p class="ex-note">The accelerating feeders are the high-cost coasts and DC (San Francisco 2.6×, DC 2.0×, Seattle/Portland/Sacramento 2.6× combined) — housing-cost-arbitrage in-migration with origin incomes at or above local. Outflows are small and aimed at cheap metros (Nashville −159, Oklahoma City −139).</p>
</div>
<div class="src">employment-drivers/data/placerai/&#123;Boise_MSA_Growth_Breakdown, population_change_by_zip, Boise_MSA_Origin_Destination&#125; · figures recomputed from the CSVs and tied to the IC-slides exhibit</div>
</figure>'''

# ---------------------------------------------------------------- render
def render_side(key, label, cls):
    h = [f'<section class="side {cls}"><div class="side-head"><h2>{label}</h2><span class="count">{sum(len(s[1]) for s in sections[key])} items</span></div>']
    for title, items in sections[key]:
        h.append(f'<h3>{inline(title)}</h3>')
        for iid, claim, body, src in items:
            h.append('<article class="item">')
            h.append(f'<div class="iid">{esc(iid)}</div>')
            h.append(f'<div class="itext"><p><strong class="claim">{inline(claim)}</strong> {inline(body)}</p>')
            if src: h.append(f'<div class="src">{esc(src)}</div>')
            h.append('</div></article>')
            if iid == 'H39':
                h.append(exhibit())
    h.append('</section>')
    return '\n'.join(h)

hdr_html = '\n'.join(f'<p>{inline(p)}</p>' for p in header_paras[:3])
meth = inline(header_paras[3]) if len(header_paras) > 3 else ''
bottom_html = '\n'.join(f'<p>{inline(p)}</p>' for p in bottom)
nS = sum(len(s[1]) for s in sections['S'])
nC = sum(len(s[1]) for s in sections['C'])

page = f'''<title>Seasons at Meridian Ledger</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@500;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --paper:#FAFAF7; --ink:#1B2823; --muted:#5C6963; --line:#DCE1DB;
  --pine:#1E5C45; --pine-soft:#EAF1ED; --oxide:#96482D; --oxide-soft:#F5EDE8;
  --card:#FFFFFF; --mono-bg:#F1F3EF;
  --s-dom:#2a78d6; --s-intl:#eb6834; --s-nat:#1baf7a;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper:#131917; --ink:#E4E9E4; --muted:#93A099; --line:#2A332E;
    --pine:#63B893; --pine-soft:#1A2721; --oxide:#D98B67; --oxide-soft:#271C17;
    --card:#181F1C; --mono-bg:#1C2420;
    --s-dom:#3987e5; --s-intl:#d95926; --s-nat:#199e70;
  }}
}}
:root[data-theme="dark"] {{
  --paper:#131917; --ink:#E4E9E4; --muted:#93A099; --line:#2A332E;
  --pine:#63B893; --pine-soft:#1A2721; --oxide:#D98B67; --oxide-soft:#271C17;
  --card:#181F1C; --mono-bg:#1C2420;
  --s-dom:#3987e5; --s-intl:#d95926; --s-nat:#199e70;
}}
* {{ box-sizing:border-box; }}
body {{ background:var(--paper); color:var(--ink); margin:0;
  font-family:'Source Serif 4', Georgia, serif; font-size:16px; line-height:1.55; }}
.wrap {{ max-width:52rem; margin:0 auto; padding:3rem 1.25rem 5rem; }}
.eyebrow {{ font-family:'IBM Plex Mono', monospace; font-size:.72rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); margin:0 0 .75rem; }}
h1 {{ font-family:'Libre Franklin', system-ui, sans-serif; font-weight:800; font-size:2.3rem;
  line-height:1.08; margin:0 0 1.25rem; text-wrap:balance; letter-spacing:-.015em; }}
.deal-strip {{ font-family:'IBM Plex Mono', monospace; font-size:.8rem; line-height:1.7;
  background:var(--mono-bg); border:1px solid var(--line); border-radius:6px;
  padding:.9rem 1.1rem; margin:0 0 1.5rem; color:var(--ink); overflow-x:auto; }}
.deal-strip b {{ font-weight:500; color:var(--pine); }}
.intro p {{ margin:.6rem 0; max-width:65ch; }}
.meth {{ font-size:.85rem; color:var(--muted); border-left:2px solid var(--line);
  padding-left:1rem; margin:1.5rem 0 0; max-width:65ch; }}
.scorecard {{ display:flex; gap:.75rem; flex-wrap:wrap; margin:2rem 0 0; }}
.scorecard .tile {{ flex:1 1 9rem; background:var(--card); border:1px solid var(--line);
  border-radius:6px; padding:.8rem 1rem; }}
.tile .n {{ font-family:'Libre Franklin', sans-serif; font-weight:800; font-size:1.6rem;
  font-variant-numeric:tabular-nums; }}
.tile .l {{ font-family:'IBM Plex Mono', monospace; font-size:.68rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); margin-top:.15rem; }}
.tile.s .n {{ color:var(--pine); }} .tile.c .n {{ color:var(--oxide); }}
.side {{ margin-top:3.5rem; }}
.side-head {{ display:flex; align-items:baseline; gap:1rem; border-bottom:3px solid var(--edge);
  padding-bottom:.5rem; }}
.side.s {{ --edge:var(--pine); --soft:var(--pine-soft); }}
.side.c {{ --edge:var(--oxide); --soft:var(--oxide-soft); }}
.side h2 {{ font-family:'Libre Franklin', sans-serif; font-weight:800; font-size:1.6rem;
  margin:0; letter-spacing:-.01em; color:var(--edge); }}
.side .count {{ font-family:'IBM Plex Mono', monospace; font-size:.75rem; color:var(--muted); }}
.side h3 {{ font-family:'Libre Franklin', sans-serif; font-weight:700; font-size:1.02rem;
  margin:2.2rem 0 .9rem; text-wrap:balance; }}
.item {{ display:flex; gap:.9rem; padding:.85rem .9rem; background:var(--card);
  border:1px solid var(--line); border-left:3px solid var(--edge); border-radius:4px;
  margin-bottom:.6rem; }}
.iid {{ font-family:'IBM Plex Mono', monospace; font-size:.72rem; font-weight:500;
  color:var(--edge); background:var(--soft); border-radius:3px; padding:.15rem .4rem;
  height:fit-content; white-space:nowrap; }}
.itext {{ min-width:0; }}
.itext p {{ margin:0; }}
.claim {{ font-weight:600; }}
.src {{ font-family:'IBM Plex Mono', monospace; font-size:.68rem; color:var(--muted);
  margin-top:.45rem; }}
.wtag {{ font-family:'IBM Plex Mono', monospace; font-size:.62rem; font-weight:500;
  color:var(--oxide); border:1px solid var(--oxide); border-radius:50%;
  padding:0 .28em; margin:0 .1em; vertical-align:super; cursor:help; }}
.bottom {{ margin-top:3.5rem; background:var(--card); border:1px solid var(--line);
  border-radius:6px; padding:1.4rem 1.6rem; }}
.bottom h2 {{ font-family:'Libre Franklin', sans-serif; font-weight:800; font-size:1.25rem;
  margin:0 0 .8rem; }}
.bottom p {{ margin:.6rem 0; max-width:68ch; }}
a {{ color:var(--pine); }}
/* ------- H39 exhibit ------- */
.exhibit {{ margin:.4rem 0 1.2rem; padding:1.1rem 1.2rem 1rem; background:var(--card);
  border:1px solid var(--line); border-left:3px solid var(--pine); border-radius:4px; }}
.ex-head {{ font-family:'Libre Franklin', sans-serif; font-weight:800; font-size:1rem;
  margin:0 0 .3rem; }}
.ex-sub {{ font-family:'IBM Plex Mono', monospace; font-weight:400; font-size:.68rem;
  color:var(--muted); margin-left:.5rem; }}
.ex-block {{ margin-top:1.3rem; }}
.ex-title {{ font-family:'IBM Plex Mono', monospace; font-size:.72rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); border-bottom:1px solid var(--line);
  padding-bottom:.35rem; margin-bottom:.7rem; }}
.seg {{ transition:opacity .12s; }}
.seg:hover {{ opacity:.82; }}
.seg.dom {{ fill:var(--s-dom); }} .seg.intl {{ fill:var(--s-intl); }} .seg.nat {{ fill:var(--s-nat); }}
.exhibit text {{ font-family:'IBM Plex Mono', monospace; fill:var(--muted); font-size:11px; }}
.exhibit text.tot {{ fill:var(--ink); font-size:12.5px; font-weight:500; }}
.exhibit text.em {{ fill:var(--pine); font-weight:500; }}
.legend {{ display:flex; gap:1.2rem; flex-wrap:wrap; font-family:'IBM Plex Mono', monospace;
  font-size:.7rem; color:var(--muted); margin-top:.5rem; }}
.legend .sw {{ display:inline-block; width:.7em; height:.7em; border-radius:2px;
  margin-right:.4em; }}
.sw.dom {{ background:var(--s-dom); }} .sw.intl {{ background:var(--s-intl); }} .sw.nat {{ background:var(--s-nat); }}
.ex-note {{ font-size:.85rem; color:var(--muted); margin:.6rem 0 0; max-width:65ch; }}
.tbl-wrap {{ overflow-x:auto; }}
.exhibit table {{ border-collapse:collapse; width:100%; font-size:.85rem; }}
.exhibit th {{ font-family:'IBM Plex Mono', monospace; font-size:.66rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--muted); text-align:left; font-weight:500;
  padding:.3rem .6rem; border-bottom:1px solid var(--line); }}
.exhibit td {{ padding:.42rem .6rem; border-bottom:1px solid var(--line); }}
.exhibit td.num, .exhibit th.num {{ text-align:right; font-variant-numeric:tabular-nums;
  font-family:'IBM Plex Mono', monospace; font-size:.8rem; }}
.exhibit td.rank {{ font-family:'IBM Plex Mono', monospace; color:var(--muted); font-size:.75rem; }}
.exhibit tr.hl td {{ background:var(--pine-soft); font-weight:600; }}
.exhibit td.acc {{ font-weight:600; }}
@media (max-width:560px) {{ .item {{ flex-direction:column; gap:.4rem; }} h1 {{ font-size:1.8rem; }} }}
@media (prefers-reduced-motion: reduce) {{ .seg {{ transition:none; }} }}
</style>
<div class="wrap">
<p class="eyebrow">Investment diligence · Meridian, Idaho · 8/22/2026</p>
<h1>Seasons at Meridian — Strengths &amp; Considerations</h1>
<div class="deal-strip">360 units · 2024 build · 2700 E Overland Rd (Eagle Rd &amp; I-84) · Broker <b>CBRE</b> · First-round bids <b>8/19/2026</b><br>
Model v3 (8/15): <b>$120.0M</b> · 5-yr hold · 5.25% exit · 11.21% LIRR &nbsp;|&nbsp; IC exec summary (8/17): <b>$122.0M</b> · 4-yr hold · 5.00% exit · 11.9% LIRR</div>
<div class="intro">{hdr_html}</div>
<div class="scorecard">
<div class="tile s"><div class="n">{nS}</div><div class="l">Strengths</div></div>
<div class="tile c"><div class="n">{nC}</div><div class="l">Considerations</div></div>
<div class="tile"><div class="n">50/50</div><div class="l">Numeric tie-outs</div></div>
<div class="tile"><div class="n">38</div><div class="l">Agents · 4 passes</div></div>
</div>
<p class="meth">{meth}</p>
{render_side('S', 'Strengths', 's')}
{render_side('C', 'Considerations', 'c')}
<div class="bottom"><h2>Bottom line</h2>{bottom_html}</div>
</div>'''

open(OUT, 'w').write(page)
print(f'wrote {OUT} ({os.path.getsize(OUT):,} bytes); S={nS} C={nC}')
