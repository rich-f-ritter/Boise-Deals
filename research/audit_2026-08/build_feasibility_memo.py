#!/usr/bin/env python3
"""Build the Development Feasibility executive summary (.docx) for Seasons at Meridian.

Branded to match the supply map / land-use viewer: navy #153D64, gold #B49955,
Georgia headings, Calibri body. All figures come from development_feasibility.json
(which reads the live TMG model) plus the prior audit workstreams.
"""
import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).parent
D = json.loads((HERE / 'development_feasibility.json').read_text())
OUT = Path('/home/user/Boise-Deals/SeasonsMeridian/'
           'Seasons at Meridian - Development Feasibility.docx')

NAVY = RGBColor(0x15, 0x3D, 0x64)
GOLD = RGBColor(0xB4, 0x99, 0x55)
INK = RGBColor(0x1A, 0x2B, 0x3C)
GRAY = RGBColor(0x6F, 0x6F, 0x70)
RED = RGBColor(0xA6, 0x1B, 0x1B)
GREEN = RGBColor(0x1E, 0x6B, 0x33)
HEX_NAVY, HEX_GOLD, HEX_BAND, HEX_BOX = '153D64', 'B49955', 'EDF2F7', 'F7F4EC'

doc = Document()
sec = doc.sections[0]
sec.top_margin = sec.bottom_margin = Inches(0.6)
sec.left_margin = sec.right_margin = Inches(0.7)

st = doc.styles['Normal']
st.font.name = 'Calibri'
st.font.size = Pt(9.5)
st.font.color.rgb = INK
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.05


# WordprocessingML enforces child-element ORDER inside w:pPr / w:tcPr / w:tblPr.
# Appending is not enough — Word/LibreOffice reject the file. Insert before the
# successors declared in the schema instead.
TCPR_AFTER_SHD = ('w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign',
                  'w:hideMark', 'w:headers', 'w:cellIns', 'w:cellDel', 'w:cellMerge',
                  'w:tcPrChange')
PPR_AFTER_PBDR = ('w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
                  'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
                  'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
                  'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
                  'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                  'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
                  'w:pPrChange')


def shade(cell, hexcolor):
    el = OxmlElement('w:shd')
    el.set(qn('w:val'), 'clear')
    el.set(qn('w:color'), 'auto')
    el.set(qn('w:fill'), hexcolor)
    tcPr = cell._tc.get_or_add_tcPr()
    for existing in tcPr.findall(qn('w:shd')):
        tcPr.remove(existing)
    tcPr.insert_element_before(el, *TCPR_AFTER_SHD)


def rule(p, color=HEX_NAVY, size=6, edge='bottom'):
    pPr = p._p.get_or_add_pPr()
    bdr = pPr.find(qn('w:pBdr'))
    if bdr is None:
        bdr = OxmlElement('w:pBdr')
        pPr.insert_element_before(bdr, *PPR_AFTER_PBDR)
    e = OxmlElement(f'w:{edge}')
    e.set(qn('w:val'), 'single')
    e.set(qn('w:sz'), str(size))
    e.set(qn('w:space'), '2')
    e.set(qn('w:color'), color)
    bdr.append(e)


def para(text='', size=9.5, bold=False, italic=False, color=INK, after=4, before=0,
         align=None, indent=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if align is not None:
        p.alignment = align
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = color
    return p


def rich(parts, size=9.5, after=4, indent=None, before=0):
    """parts = [(text, bold, color|None), ...]"""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    for t, b, c in parts:
        r = p.add_run(t)
        r.font.size = Pt(size)
        r.bold = b
        r.font.color.rgb = c or INK
    return p


def h1(text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(1)
    if num:
        r = p.add_run(f'{num}  ')
        r.font.name = 'Georgia'
        r.font.size = Pt(12.5)
        r.bold = True
        r.font.color.rgb = GOLD
    r = p.add_run(text)
    r.font.name = 'Georgia'
    r.font.size = Pt(12.5)
    r.bold = True
    r.font.color.rgb = NAVY
    rule(p)
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.name = 'Georgia'
    r.font.size = Pt(10)
    r.bold = True
    r.font.color.rgb = NAVY
    return p


def bullet(parts, size=9.5, after=2.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.left_indent = Inches(0.22)
    p.paragraph_format.first_line_indent = Inches(-0.13)
    p.paragraph_format.line_spacing = 1.05
    for t, b, c in parts:
        r = p.add_run(t)
        r.font.size = Pt(size)
        r.bold = b
        r.font.color.rgb = c or INK
    return p


def exhibit(label, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f'{label}   ')
    r.font.name = 'Georgia'
    r.font.size = Pt(8.5)
    r.bold = True
    r.font.color.rgb = GOLD
    r = p.add_run(title)
    r.font.size = Pt(8.5)
    r.bold = True
    r.font.color.rgb = NAVY
    return p


def no_split(row):
    """Keep a table row intact rather than letting it break across a page."""
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement('w:cantSplit')
    trPr.append(el)


def table(headers, rows, widths, align=None, fontsize=8.3, highlight=None, note=None):
    """align: list of 'l'/'r'/'c'. highlight: set of row indices to shade gold-tint."""
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    align = align or ['l'] + ['r'] * (len(headers) - 1)
    amap = {'l': WD_ALIGN_PARAGRAPH.LEFT, 'r': WD_ALIGN_PARAGRAPH.RIGHT,
            'c': WD_ALIGN_PARAGRAPH.CENTER}
    hdr = t.rows[0]
    no_split(hdr)
    for i, htxt in enumerate(headers):
        c = hdr.cells[i]
        c.width = Inches(widths[i])
        shade(c, HEX_NAVY)
        p = c.paragraphs[0]
        p.alignment = amap[align[i]]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        r = p.add_run(htxt)
        r.font.size = Pt(fontsize)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for ri, row in enumerate(rows):
        trow = t.add_row()
        no_split(trow)
        cells = trow.cells
        for i, val in enumerate(row):
            c = cells[i]
            c.width = Inches(widths[i])
            if highlight and ri in highlight:
                shade(c, 'F3EFE1')
            elif ri % 2 == 1:
                shade(c, HEX_BAND)
            p = c.paragraphs[0]
            p.alignment = amap[align[i]]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            txt, bold, col = val if isinstance(val, tuple) else (val, False, None)
            r = p.add_run(txt)
            r.font.size = Pt(fontsize)
            r.bold = bold
            r.font.color.rgb = col or INK
    if note:
        para(note, size=7.6, italic=True, color=GRAY, after=2, before=2)
    return t


def callout(title, lines, fill=HEX_BOX, accent=GOLD):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    c.width = Inches(7.1)
    shade(c, fill)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(title)
    r.font.name = 'Georgia'
    r.font.size = Pt(9.5)
    r.bold = True
    r.font.color.rgb = NAVY
    for parts in lines:
        pp = c.add_paragraph()
        pp.paragraph_format.space_after = Pt(2)
        pp.paragraph_format.line_spacing = 1.05
        for tx, b, col in parts:
            r = pp.add_run(tx)
            r.font.size = Pt(9)
            r.bold = b
            r.font.color.rgb = col or INK
    return t


def money(v, dec=0):
    return f'${v:,.{dec}f}'


# ============================================================ MASTHEAD
mast = doc.add_table(rows=1, cols=1)
mc = mast.rows[0].cells[0]
mc.width = Inches(7.1)
shade(mc, HEX_NAVY)
p = mc.paragraphs[0]
p.paragraph_format.space_after = Pt(0)
r = p.add_run('DEVELOPMENT FEASIBILITY  ·  INVESTMENT COMMITTEE')
r.font.size = Pt(7.5)
r.bold = True
r.font.color.rgb = RGBColor(0xB6, 0xD6, 0xEF)
p2 = mc.add_paragraph()
p2.paragraph_format.space_after = Pt(0)
r = p2.add_run('Seasons at Meridian')
r.font.name = 'Georgia'
r.font.size = Pt(19)
r.bold = True
r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
p3 = mc.add_paragraph()
p3.paragraph_format.space_after = Pt(2)
r = p3.add_run('Can anyone build competitive supply in this ring before we sell?\n'
               '2700 E Overland Rd, Meridian, ID  ·  360 units  ·  built 2024  ·  '
               'August 15, 2026')
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(0xCF, 0xE0, 0xEF)

# ============================================================ BOTTOM LINE
q1, q2, bs, su = D['q1'], D['q2'], D['basis'], D['stepup']
callout('BOTTOM LINE', [
    [('New supply in this ring needs about ', False, None),
     (f"{money(q1['required_2026'])}/unit/month", True, NAVY),
     (' of market rent to pencil. We underwrite Year 1 market rent at ', False, None),
     (f"{money(q1['y1_mkt_rent'])}", True, NAVY),
     (f" — a {q1['opening_gap']:.0%} gap. Nothing competitive gets built until that closes.",
      False, None)],
    [('Under our own rent-growth assumptions the gap ', False, None),
     ('narrows but never closes during the hold', True, GREEN),
     (f": still {abs(q1['gap_at_exit_esc']):.0%} short at our October 2031 exit if construction "
      'costs keep escalating at the observed +1.7%/yr, and only reaching breakeven ',
      False, None),
     ('in the exit year itself', True, None),
     (' even if costs stay flat in nominal dollars.', False, None)],
    [('Add the ', False, None), ('four-year lag', True, NAVY),
     (' between "pencils" and "competes" (12–24 months entitlement + 24–30 months construction) '
      'and a competitor would have had to be feasible ', False, None),
     ('today', True, None),
     (' to pressure our Year 4–5 rents. It is not: that would require market rents ', False, None),
     (f"{q1['immediate_step_change_needed']:.0%} above our Year 1 underwriting immediately.",
      True, NAVY)],
    [('We buy at ', False, None), (f"{money(bs['price_pu'])}/unit", True, NAVY),
     (f" against a {money(bs['rc_pu'])}/unit replacement cost — ", False, None),
     (f"{bs['price_vs_rc']:+.1%} on price, {bs['basis_vs_rc']:+.1%} on total basis.", True, None),
     (' We are not buying below replacement cost. The thesis is not a discount to cost; it is '
      'that the cost itself is unfinanceable at today’s rents.', False, None)],
    [('The real exposure is not new supply — it is ', False, None),
     ('our own exit', True, RED),
     (f". We underwrite a 7-year-old asset at a {5.25:.2f}% cap while Quarterra underwrites a "
      f"2-year-old asset at {5.50:.2f}%. Holding our NOI and using Emblem’s cap costs ",
      False, None),
     (f"−{money(142_809_165 - q2['exit_at_emblem_cap'])} of value and "
      f"{abs((q2['lirr_stress']-q2['lirr_base'])*10000):.0f} bp of levered IRR", True, RED),
     (f" ({q2['lirr_base']:.2%} → {q2['lirr_stress']:.2%}).", False, None)],
])

# ============================================================ 1. THE BID IN CONTEXT
h1('The bid in context', '1')
rich([('We are bidding ', False, None), (f"{money(D['basis']['price_pu'])}/unit", True, NAVY),
      (f" ({money(120_000_000)}) against a replacement cost of ", False, None),
      (f"{money(bs['rc_pu'])}/unit", True, NAVY),
      (f" ({money(116_110_721)}). That is a premium, not a discount — and it is the right place "
       'to start, because it frames what this memo is actually testing. We are not underwriting '
       'a below-replacement bargain. We are underwriting the proposition that ', False, None),
      ('no one can finance that replacement cost at today’s rents', True, None),
      (', and therefore that our competitive set is fixed for the hold period.', False, None)])

exhibit('EXHIBIT A', 'Basis vs. cost to build — we pay a premium to replacement cost')
table(
    ['Basis', '$ / unit', 'Total', 'vs. replacement cost'],
    [["Subject's actual 2022 development cost", money(284_658), money(102_476_923),
      ('−11.7%', False, GREEN)],
     ['Replacement cost today (Emblem-anchored)', (money(bs['rc_pu']), True, None),
      (money(116_110_721), True, None), ('—', False, GRAY)],
     ['TMG purchase price', money(bs['price_pu']), money(120_000_000),
      (f"{bs['price_vs_rc']:+.1%}", True, RED)],
     ['TMG total basis (price + closing + capex)', money(bs['basis_pu']), money(122_102_902),
      (f"{bs['basis_vs_rc']:+.1%}", True, RED)]],
    widths=[3.1, 1.1, 1.35, 1.55], align=['l', 'r', 'r', 'r'], highlight={1},
    note='Replacement cost is anchored on the Quarterra Emblem Meridian development budget '
         '($304,530/unit all-in, 55.0% LTC, delivering 2028), adjusted +$14,000/u for the '
         'subject’s amenity package, +$6,000/u for the Eagle/Overland land basis and −$2,000/u '
         'for scale. Sensible range $315,000–$330,000/unit.')

# ============================================================ 2. LENS 1
h1('Lens 1 — Market feasibility: can anyone build here today?', '2')

h2('2.1  Costs plateaued. Capital broke.')
rich([('The common story — "construction costs keep rising" — is ', False, None),
      ('not what the data shows', True, NAVY),
      (', and getting this right matters because it changes what we watch. Costs roughly doubled '
       'between 2014 and 2021 (~+9%/yr), then flattened. Across the 118-loan Boise construction '
       'tape, the Seasons-comparable cohort (market-rate, 100+ units, core submarkets, '
       'garden/mid-rise) plateaued at ~+1.7%/yr from 2022 to the live 2026 Emblem budget. What '
       'broke was ', False, None),
      ('leverage', True, NAVY),
      (': construction LTC fell from ~65% pre-2022 to 55.0% on Emblem’s actual loan. Cost per '
       'unit is roughly flat, but ', False, None),
      ('equity per unit is up 38%', True, RED),
      ('. That is the binding constraint.', False, None)])

exhibit('EXHIBIT B', 'All-in cost per unit by vintage, and the equity break')
eras = D['cost_eras']
rows = []
prev = None
for lab, v in eras:
    chg = f'{v/prev-1:+.0%}' if prev else '—'
    col = RED if prev and v > prev else (GREEN if prev else GRAY)
    ltc = '65%' if lab in ('2012-2016', '2017-2019', '2020-2021', '2022') else (
        '60%' if lab == '2023-2025' else '55%')
    eq = v * (1 - float(ltc.rstrip('%')) / 100)
    rows.append([lab.replace('-', '–'), money(v), (chg, False, col), ltc,
                 (money(eq), lab in ('2022', '2026 (Emblem)'), NAVY if lab in
                  ('2022', '2026 (Emblem)') else None)])
    prev = v
table(['Vintage', 'All-in $ / unit', 'Change', 'Construction LTC', 'Equity $ / unit'],
      rows, widths=[1.45, 1.35, 1.0, 1.5, 1.45],
      align=['l', 'r', 'r', 'c', 'r'], highlight={5},
      note='Derived from the Yardi Boise construction-loan tape (118 loans) grossed to all-in '
           'cost at the vintage LTC, screened to Seasons-comparable product; 2026 is Quarterra’s '
           'actual Emblem Meridian budget. On essentially flat cost, equity per unit rises +34% '
           'against the 2022 cohort median ($101,981 → $137,038) and +38% against the subject’s '
           'own 2022 development basis ($99,630 → $137,038).')

rich([('The lending market confirms it. Ring construction originations ran ', False, None),
      ('5 loans in 2022, then 0 in 2023, 1 in 2024, 2 in 2025 and 0 year-to-date in 2026', True,
       NAVY),
      (' — total volume down 82% from the 2022 peak. There is no financing market for this '
       'product at this basis.', False, None)])

h2('2.2  What rent new supply actually requires')
rich([('Quarterra’s Emblem Meridian book advertises a $2,069/unit/month market rent at a '
       '6.65–6.80% yield on cost. That rent is only achievable because the proforma carries '
       '$350.59/unit/month of ancillary income — ', False, None),
      ('83% more than the subject actually collects', True, RED),
      (' ($191.94). The single largest item is $108/month of managed WiFi billed gross, with the '
       'offsetting ISP cost buried in utilities. Normalizing the ancillary stack to what this '
       'submarket demonstrably supports, and correcting an assessed-value ramp that lags '
       'construction by ~$212k across lease-up, the required ', False, None),
      ('market', True, None),
      (' rent rises to ', False, None), (f"{money(q1['required_2026'])}/unit/month", True, NAVY),
      (' in 2026 dollars. Their expense, insurance and tax-rate assumptions are '
       'defensible-to-conservative; the aggression is entirely on the revenue line.', False, None)])

exhibit('EXHIBIT C', 'Bridge from Emblem’s advertised rent to the rent new supply really needs')
table(['Step', 'Ancillary $/u/mo', 'Required base market rent', 'Comment'],
      [['Emblem, as advertised (2026 $)', '350.59', money(2_069),
        '6.80% YoC on $304,530/u cost'],
       ['Subject’s actual ancillary collection', '191.94', '—', 'T12 to 6/30/2026'],
       ['Normalized defensible ancillary', ('215.50', True, NAVY), '—',
        'garage 45 · RUBS 65 · WiFi 45 net · pet 10.50 · other 50'],
       ['Assessor keeps pace with construction', '—', '—', '−$67,719/yr of deferred tax'],
       [('REQUIRED MARKET RENT', True, NAVY), '—',
        (money(q1['required_2026']), True, NAVY), 'to hold the same 6.80% yield on cost'],
       [('Subject Year 1 market rent (UW)', True, None), '—',
        (money(q1['y1_mkt_rent']), True, None), 'HelloData market rent, TMG model'],
       [('GAP NEW SUPPLY MUST CLOSE', True, RED), '—',
        (f"{q1['opening_gap']:+.1%}", True, RED), 'market-to-market, not contract rent']],
      widths=[2.35, 1.15, 1.55, 2.05], align=['l', 'r', 'r', 'l'], highlight={4, 6},
      note='Comparison is market rent to market rent, since market rent is what drives a '
           'developer’s proforma and is the metric the subject is underwritten on. On a PSF '
           'basis: subject $1.93/SF vs. required $2.37/SF.')

h2('2.3  The approval gauntlet — and the projects it has killed')
rich([('Even when a deal pencils, Meridian and Ada County are a hostile venue for multifamily. '
       'Our census of the ring found ', False, None),
      ('20 dead projects and roughly 4,365 units killed between 2015 and 2026', True, NAVY),
      (', of which ~2,731 units have no successor entitlement. The kills accelerate exactly when '
       'they matter: 1,095 units in 2022, 999 in 2023, 821 in 2024, 625 in 2025.', False, None)])
rich([('The pattern is instructive. Six sites were killed ', False, None),
      ('more than once', True, NAVY),
      (' — Magic View three times, 1475 E Franklin three times, Lake Hazel & Five Mile twice, '
       'Civic Block twice, Tanner Creek twice. Council has overridden its own P&Z in both '
       'directions. And the subject’s own marketed Phase II — ', False, None),
      ('"Overland & Wells II," 351 units on the parcel that touches us', True, NAVY),
      (' — was denied outright by Meridian City Council on 10/25/2022, with findings citing '
       'employment-land loss, failing Overland/Eagle intersections and multifamily '
       'over-concentration next to our Phase 1. WinCo still owns it and has marketed it as retail '
       'pads since January 2024. ', False, None),
      ('That denial is a precedent that protects our node.', True, GREEN)])

exhibit('EXHIBIT D', 'Why projects died — 20 kill events, 2015–2026')
table(['Cause', 'Representative deals', 'Units', 'Read-through'],
      [['Land-use policy / council denial',
        'Overland & Wells II (351), Tanner Creek (272), Lake Hazel ×2 (248)',
        '~1,150', 'Structural. Entitlement risk is real even with staff support.'],
       ['Capital markets / cost',
        'The Bridge at The Village (549), Civic Block (230), Hummingbird (170)',
        '~1,500', 'Dominant cause post-2022. Confirms the financing break.'],
       ['Entitlement lapse (2-yr CUP clock)',
        'The 10 at Meridian (559→516), Andorra (164), Record (472)',
        '~1,200', 'Paper entitlements expire quietly. Do not credit them.'],
       ['Converted to another use',
        'Newkirk (216 → for-sale), Fairview (150 → RV dealer)',
        '~370', 'Land permanently exits the MF pipeline.'],
       ['Affordable / LIHTC financing collapse', 'Centrepoint (239)', '~240',
        'Subsidized supply is not a backstop either.']],
      widths=[1.75, 2.65, 0.7, 2.0], align=['l', 'l', 'r', 'l'], fontsize=8.0,
      note='Full register with file numbers, dates, sources and confidence ratings: '
           'research/audit_2026-08/graveyard_register.md and graveyard_report.md.')

h2('2.4  What is actually coming')
rich([('Against 4,494 headline "proposed" units in the ring, our deal-by-deal probability work '
       'puts ', False, None),
      ('1,221 probability-weighted units (27%)', True, NAVY),
      (' on the ground by year-end 2031. ', False, None),
      ('Exactly one deal in the ring holds a building permit', True, RED),
      (' — Outer Banks (516 units, 3.3 miles west), and only 3 of its ~50 buildings are '
       'permitted. That single deal carries 34% of the entire weighted total. Everything else '
       'is paper.', False, None)])

exhibit('EXHIBIT E', 'Probability-weighted delivery curve vs. the 2022–24 run-rate')
table(['Year', 'Weighted units', 'vs. 2022–24 run-rate (1,000–3,000/yr)', 'Contributors'],
      [['2027', ('0', True, GREEN), 'no deliveries possible', 'None — earliest permit issued 6/2026'],
       ['2028', '165', '6–17%', 'Outer Banks, first tranche only'],
       ['2029', '196', '7–20%', 'Outer Banks (145), The Judy (41), Meridian OZ (11)'],
       ['2030', ('735', True, RED), '25–74%', '12 deals — none holds a permit today'],
       ['2031', '125', '4–13%', 'Vanguard (66), Gateway (59)'],
       [('5-yr total', True, NAVY), ('1,221', True, NAVY), ('~244 units/yr', True, None),
        '27% of the 4,494 proposed']],
      widths=[0.65, 1.15, 2.3, 3.0], align=['l', 'r', 'c', 'l'], highlight={5},
      note='2027–2029 averages 120 weighted units/yr — 4–12% of the 2022–24 run-rate. 2030 is '
           'the only year approaching the historical floor and is the least reliable number here: '
           'every unit in it comes from a deal with no permit today. Near-term entitlement '
           'clocks: The Judy ~9/10/26, Meridian OZ ~10/17/26 and Gateway ~11/19/26 all expire '
           'within 90 days with no extension on file; Record and 12548 W Overland have already '
           'lapsed; Victory Flats is on a second extension request.')

# ============================================================ 3. LENS 2
h1('Lens 2 — The moat, and exactly when it closes', '3')
rich([('This is the question that matters for our hold: ', False, None),
      ('how much rent growth can we capture before new construction pencils again and starts '
       'competing with us?', True, NAVY),
      (' The moat is self-limiting by construction — the very rent growth that drives our returns '
       'is what restores feasibility for a developer. So the analysis is not "is there a moat" '
       'but "does it outlast us."', False, None)])

exhibit('EXHIBIT F', 'When does new construction pencil? — subject market rent vs. required rent')
rows = []
for r in q1['path']:
    fy = int(r['fy'])
    if fy > 2034:
        continue
    is_exit = fy == 2031
    rows.append([
        (f"FY{fy}" + ('  ◄ EXIT' if is_exit else ''), is_exit, NAVY if is_exit else None),
        (money(r['mkt_rent']), is_exit, None),
        money(r['req_esc']),
        (f"{r['gap_esc']:.1%}", is_exit, RED if r['gap_esc'] < 0 else GREEN),
        money(r['req_flat']),
        (f"{r['gap_flat']:+.1%}", is_exit, RED if r['gap_flat'] < 0 else GREEN),
    ])
table(['Fiscal year', 'Subject market rent',
       'Required rent (costs +1.7%/yr)', 'Gap',
       'Required rent (costs flat)', 'Gap'],
      rows, widths=[1.15, 1.25, 1.5, 0.75, 1.35, 0.75],
      align=['l', 'r', 'r', 'r', 'r', 'r'], fontsize=8.0,
      highlight={i for i, r in enumerate(rows) if '◄' in r[0][0]},
      note='Subject market rent is the TMG underwriting path (HelloData market rent, +3.1% in '
           'Y1 then +4.0/4.0/4.0/3.5% — a 3.8%/yr average). Required rent escalates with '
           'construction cost. Two bookends are shown because the cost path is the live variable: '
           'the observed 2022–26 escalation of +1.7%/yr, and a flat-nominal-cost case that is '
           'deliberately generous to the developer.')

callout('READ-THROUGH ON RISK 1 — rent growth vs. the return of supply', [
    [('The gap never closes on our watch. ', True, GREEN),
     (f"With costs escalating at the observed +1.7%/yr, the subject's market rent is still "
      f"{abs(q1['gap_at_exit_esc']):.0%} short of feasibility at our October 2031 exit, "
      f"{abs(next(r['gap_esc'] for r in q1['path'] if int(r['fy']) == 2034)):.0%} short in "
      f"FY2034 and {abs(q1['path'][-1]['gap_esc']):.0%} short even in FY2036. In the flat-cost "
      'case — generous to the developer — feasibility is restored in ', False, None),
     ('FY2031, the exit year itself', True, NAVY),
     ('. Under neither case does a competitor pencil early enough to build and lease against us.',
      False, None)],
    [('The four-year lag is the second line of defense. ', True, NAVY),
     ('A deal that becomes feasible must still clear entitlement (12–24 months in Meridian, and '
      'that assumes it survives — see Exhibit D) and construction (24–30 months for garden). To '
      'suppress our Year 4–5 rents, a competitor had to be feasible in FY2027. That requires '
      'market rents ', False, None),
     (f"{q1['immediate_step_change_needed']:.0%} above our Year 1 underwriting immediately", True,
      NAVY),
     (' — a step-change, not a trend. Our own underwriting has FY2027 growth at +3.1%.',
      False, None)],
    [('The uncomfortable corollary. ', True, RED),
     ('Because the gap is this wide, our rent-growth assumptions are ', False, None),
     ('not', True, None),
     (' constrained by supply — which means they have to be defended on demand alone. If Boise '
      'rent growth disappoints, there is no supply-side story that rescues the exit. The moat '
      'protects us from a supply shock; it does nothing for a demand shock.', False, None)],
])

# ============================================================ 4. LENS 3
h1('Lens 3 — Build vs. buy, and the two $400k exits', '4')

h2('4.1  Build vs. buy')
exhibit('EXHIBIT G', 'Buying Seasons vs. building its replica today')
table(['', 'Buy Seasons (TMG)', 'Build a replica today'],
      [['Basis per unit', (money(bs['basis_pu']), True, NAVY),
        (money(bs['rc_pu']) + ' (+$0 land carry)', True, None)],
       ['Equity per unit', money(127_077), money(137_038)],
       ['Cash flow starts', ('immediately (96.1% occupied)', True, GREEN),
        ('2030–31 after entitlement + build', False, RED)],
       ['Yield on cost / going-in', '4.89% Year 1 cap', '6.80% YoC — but only at $2,224 rent'],
       ['Rent required to achieve it', (money(q1['y1_mkt_rent']) + ' (achieved today)', True, GREEN),
        (money(q1['required_2026']) + f" ({q1['opening_gap']:.0%} above market)", True, RED)],
       ['Entitlement risk', 'none — built and stabilized',
        '20 dead projects, ~4,365 units, 2015–26'],
       ['Construction financing', 'n/a', '0 ring loans YTD 2026; volume −82% from 2022'],
       ['Tax basis at entry', ('steps up to 98% of price', False, RED),
        'assessed on cost, ramps with construction']],
      widths=[1.7, 2.6, 2.8], align=['l', 'l', 'l'], fontsize=8.2,
      note='The replica case is not a live alternative — it is the benchmark that tells us what '
           'our competition would have to accept. No rational developer takes 6.80% YoC risk at a '
           'rent 16% above market when the acquisition market clears at a 4.89% going-in on '
           'stabilized cash flow.')

h2('4.2  The tax step-up we pay — and why our buyer will not')
rich([('Idaho reassesses to ~98% of sale price, and our purchase triggers exactly that. The '
       'subject is assessed at $92,993,300 today — ', False, None),
      ('77% of what we are paying', True, NAVY),
      (', because the developer’s assessment never caught up with construction. On the 2027 roll '
       'it steps to $117,600,000 (98% of price) and our tax bill goes ', False, None),
      (f"{money(su['tax_before'])} → {money(su['tax_after'])}, +{money(su['delta'])}/yr "
       f"({su['delta']/su['tax_before']:+.0%})", True, RED),
      (f" — {money(su['value_effect'])} of value at our 4.89% Year 1 cap, or "
       f"{su['bp_of_yield']:.0f} bp of going-in yield. TMG’s model captures this correctly.",
       False, None)])
rich([('The asymmetry is the interesting part, and it is a genuine ', False, None),
      ('positive', True, GREEN),
      (' for our exit. This toll is paid ', False, None), ('once', True, None),
      (', by the first institutional buyer of merchant-built product. By 2032 our assessed value '
       '— reset in 2027 and grown 3.5%/yr — reaches $139.7M, which is ', False, None),
      ('98% of our own exit price', True, NAVY),
      ('. Our buyer’s step-up is therefore ', False, None),
      (f"{money(q2['seasons_haircut'])} of value (0.01% of price) versus the "
       f"{money(q2['emblem_haircut'])} ({money(q2['emblem_haircut']/256)}/unit, 0.9% of price) "
       'a buyer of Emblem would absorb.', False, None),
      (' We sell a clean tax basis; a merchant developer does not.', True, None)])

h2('4.3  Two ~$400k/unit exits — are they consistent?')
rich([('Quarterra needs roughly $400k/unit in January 2030 on a two-year-old asset. We project '
       'roughly $397k/unit in October 2031 on a seven-year-old asset. Those numbers deserve to be '
       'put side by side, because at first glance they cannot both be right.', False, None)])

exhibit('EXHIBIT H', 'Emblem Meridian vs. Seasons at Meridian — the exit, decomposed')
table(['', 'Emblem (Quarterra)', 'Seasons (TMG)', 'Comment'],
      [['Exit date', 'January 2030', 'October 2031', '21 months apart'],
       ['Age at exit', '2 yrs (2028 vintage)', ('7 yrs (2024 vintage)', True, None),
        '3.5-year age gap'],
       ['Exit cap rate', '5.50%', ('5.25%', True, RED), 'older asset priced tighter — questionable'],
       ['Exit NOI / unit', money(q2['emblem_pu'] * 0.055), money(20_829),
        'Emblem +5.7% on larger units'],
       ['Headline exit / unit', money(q2['emblem_pu']), money(q2['seasons_pu']),
        'the two ~$400k numbers'],
       ['Assessed value at exit', ('87% of price', False, RED), ('98% of price', False, GREEN),
        'Emblem’s buyer inherits a step-up'],
       ['Buyer step-up haircut', f"−{money(q2['emblem_haircut']/256)}/u",
        f"−{money(q2['seasons_haircut']/360)}/u", 'the hidden difference'],
       [('Adjusted exit / unit', True, NAVY), (money(q2['emblem_adj_pu']), True, NAVY),
        (money(396_633), True, NAVY), ('within $154/unit of each other', True, None)]],
      widths=[1.65, 1.6, 1.55, 2.3], align=['l', 'r', 'r', 'l'], fontsize=8.2, highlight={7})

callout('READ-THROUGH ON RISK 2 — the exit-price tension', [
    [('Adjusted for tax basis, the two exits are the same number. ', True, NAVY),
     (f"Emblem’s {money(q2['emblem_pu'])} becomes {money(q2['emblem_adj_pu'])} once its buyer "
      f"prices the step-up; ours is {money(396_633)}. The apparent conflict is not that both "
      'assets are worth ~$400k/unit — it is ', False, None),
     ('when', True, None), (' and ', False, None), ('at what age', True, None),
     ('.', False, None)],
    [('Rolled forward, our exit implies a 6% age discount. ', True, None),
     (f"Growing Emblem’s adjusted {money(q2['emblem_adj_pu'])} for 21 months at our own 3.54% "
      f"appreciation CAGR gives {money(q2['emblem_rolled_to_our_exit'])}/unit for a 3.5-year-old "
      f"asset in October 2031. We underwrite our 7-year-old asset at "
      f"{q2['implied_pct_of_new']:.0%} of that — about 1.7%/yr of relative obsolescence over the "
      'age gap. For garden product that is defensible, but it is an assumption we are making, '
      'not a market fact.', False, None)],
    [('The cap rate is the softer number. ', True, RED),
     ('Exiting a seven-year-old asset at 5.25% while a merchant developer underwrites a '
      'two-year-old asset at 5.50% inverts the normal age/cap relationship. Two readings: either '
      'Quarterra is padding its exit cap to show margin (common, and likely), or we are 25 bp '
      'light. If we are light, the cost is ', False, None),
     (f"{money(142_809_165 - q2['exit_at_emblem_cap'])} of exit value and "
      f"{abs((q2['lirr_stress']-q2['lirr_base'])*10000):.0f} bp of levered IRR — "
      f"{q2['lirr_base']:.2%} falls to {q2['lirr_stress']:.2%}.", True, RED),
     (' We recommend IC see the 5.50% case as the downside, not the 5.25% as the base.',
      False, None)],
    [('The two risks are linked, and they point the same way. ', True, NAVY),
     ('Our exit at $397k/unit requires the NOI growth in Exhibit F. That same rent growth is what '
      'restores development feasibility. The good news from Exhibit F is that our own '
      'underwriting does not generate enough rent growth to restore feasibility before we sell — '
      'so the exit thesis and the moat thesis are ', False, None),
     ('compatible', True, GREEN),
     ('. They stop being compatible only in a high-growth world, where we would earn more rent '
      'but sell into a market that has begun building again.', False, None)],
])

# ============================================================ 5. WHAT WOULD CHANGE OUR MIND
h1('What would change this view', '5')
bullet([('Construction debt reopens at 65% LTC. ', True, NAVY),
        ('The single highest-impact variable. At 65% LTC the equity check falls from $137,038 to '
         '~$106,600/unit and the required rent drops materially. Watch ring construction '
         'originations — zero year-to-date 2026 is the number that matters.', False, None)])
bullet([('Market rents beat underwriting by more than ~5% in any year. ', True, NAVY),
        ('That is the early-warning threshold at which the FY2027–28 required-rent gap starts '
         'closing fast enough to matter before our exit.', False, None)])
bullet([('Outer Banks permits its remaining ~47 buildings. ', True, NAVY),
        ('Today only 3 are permitted. Full permitting would confirm that at least one sponsor has '
         'financing at this basis, and would validate 2028–30 supply we currently discount.',
         False, None)])
bullet([('Any of the three expiring entitlements is extended and financed. ', True, NAVY),
        ('The Judy (~9/10/26), Meridian OZ (~10/17/26), Gateway (~11/19/26). Extension alone is '
         'defensive and means little; extension plus a closed construction loan is the signal.',
         False, None)])
bullet([('The WinCo parcel next door re-files for multifamily. ', True, NAVY),
        ('We assess ~5% probability with an earliest delivery of ~2030, and the 2022 denial '
         'findings still stand. But it touches us, and it is the one site where new supply would '
         'compete directly rather than 3+ miles away.', False, None)])
bullet([('Cap rates for 2024-vintage garden product move. ', True, NAVY),
        ('Our exit assumes 5.25% on a seven-year-old asset. Track every Treasure Valley trade of '
         '2018–2024 vintage garden product and re-test the age/cap relationship in Exhibit H.',
         False, None)])

# ============================================================ FOOTER
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(10)
rule(p, HEX_GOLD, 8, 'top')
para('Sources and method', size=8.5, bold=True, color=NAVY, before=3, after=2)
para('Live TMG Acquisitions model 7.26 — Seasons at Meridian v3 (re-uploaded 8/15/2026: '
     '$120.0M bid, 4.89% Y1 cap, 5.25% exit cap, 10/31/2031 exit, 11.21% LIRR) · Quarterra '
     'Emblem Meridian merchant model and equity book · Yardi Boise construction-loan tape '
     '(118 loans) · Ada County ArcGIS parcel layer (92,790 parcels) · Meridian and Ada County '
     'hearing records, findings, and permit ledgers.',
     size=7.6, color=GRAY, after=2)
para('Supporting workpapers, all in research/audit_2026-08/: replacement_cost_analysis.md (v3) · '
     'emblem_normalization.py · tax_stepup_analysis.py · development_feasibility.py · '
     'pipeline_likelihood_report.md · graveyard_report.md · graveyard_register.md · '
     'seasons_II_overland_wells_II_status.md. Companion deliverables: Supply Chart.xlsx, '
     'Supply Map.html, Land Use Analysis.xlsx, Land Use Viewer.html.',
     size=7.6, color=GRAY, after=2)
para('Known limitations: Emblem’s land is still owned by Baron Properties, so its budget is an '
     'intent, not a commitment. Syringa Crossing’s 8/6/2026 P&Z outcome is unpublished. '
     'Cloverdale Crossing (PLN25-00471) carries no unit count. Owner names for five parcels '
     'require manual assessor lookups. None of these changes the direction of the conclusions.',
     size=7.6, italic=True, color=GRAY, after=0)

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print('wrote', OUT)
