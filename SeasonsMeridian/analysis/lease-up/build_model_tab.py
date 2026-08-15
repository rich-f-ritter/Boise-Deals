#!/usr/bin/env python3
"""Build 'Lease-Up Bridge' — a standalone sheet to drop into the TMG model.

Everything that HAS a source in the model is a live formula against that source,
so a refresh after pasting picks up model changes:

  market / effective rent  HDUnitLevel  (HD Dump)      T90 window, mix-weighted
  contract rent, occupancy 'T12 Dump'   rows keyed by code (Rentinc/ltl/vac)
  projected rents          RRA rows 48/49              monthly GPR / AGPR
  projected expirations    tblRentRoll[Lease Expiration] + RRA tier column
  reconciliation           'Cash Flow (Annual)' rows 4/5/8/14/16

Only the historical lease-activity counts are static: new leases, renewals and
move-outs are reconstructed from rent rolls + the concession burn-off + HelloData
episodes, and the model carries no equivalent. They are flagged in the sheet.

The mix-weighting and the T90 window deliberately mirror Cash Flow (Annual) rows
252-304 so this tab and the model's own HelloData block agree by construction.
"""
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.axis import ChartLines
from datetime import date, timedelta

OUT = 'Lease-Up Bridge (drop into model).xlsx'
SHEET = 'Lease-Up Bridge'
UNITS = 360
T90 = 90
START, END = date(2024, 7, 31), date(2028, 11, 30)

NAVY, ACCENT = '1F3864', 'BF8F00'
HDR = PatternFill('solid', fgColor=NAVY)
PROJ = PatternFill('solid', fgColor='FDF3E3')
STATIC = PatternFill('solid', fgColor='EDEBE4')
BOX = Border(*[Side(style='thin', color='D0CEC7')] * 4)
WB = Font(color='FFFFFF', bold=True, size=9)
SM = Font(size=8, italic=True, color='6B6A64')


def month_ends(a, b):
    out, y, m = [], a.year, a.month
    while True:
        nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
        e = nxt - timedelta(days=1)
        if e > b:
            break
        out.append(e)
        y, m = nxt.year, nxt.month
    return out


MONTHS = month_ends(START, END)
PLANS = ['S1_Seas', 'A1_Seas', 'A2_Seas', 'B1_Seas', 'B2_Seas',
         'B3a_Seas', 'B3b_Seas', 'C1a_Seas', 'C1b_Seas']

# static history — no model source exists for these (see module docstring)
HIST = json.load(open('monthly_activity.json'))

wb = openpyxl.Workbook()
ws = wb.active
ws.title = SHEET

# ---------------------------------------------------------------- header
ws['B2'] = 'Lease-Up Bridge — what happened at the property, and how it becomes Year 1 & Year 2'
ws['B2'].font = Font(bold=True, size=14, color=NAVY)
ws['B3'] = ('Drop this sheet into the model, then Calculate (Ctrl+Alt+F9). Blue cells are live formulas '
            'against HDUnitLevel, T12 Dump, RRA, tblRentRoll and Cash Flow (Annual). Grey cells are static '
            'reconstructed history — the model has no equivalent source for them.')
ws['B3'].font = SM
ws['B4'] = ('Market & effective rent use the SAME T90 window and mix-weighting as Cash Flow (Annual) rows '
            '252-304, so this tab and the model agree by construction. Contract rent = (AGPR − |vacancy|) ÷ '
            'occupied units — vacant units sit in AGPR at market, which overstates contract rent by ~4% at '
            'lease-up occupancy, so they are removed.')
ws['B4'].font = SM
for c in ('B3', 'B4'):
    ws[c].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(f'{c}:M{c[1]}')
ws.row_dimensions[3].height = 26
ws.row_dimensions[4].height = 34

# ---------------------------------------------------------------- unit mix
MIXR = 6
ws.cell(row=MIXR, column=2, value='UNIT MIX (live from tblRentRoll — drives the mix weighting)').font = Font(bold=True, size=9, color=NAVY)
for i, p in enumerate(PLANS):
    ws.cell(row=MIXR + 1, column=3 + i, value=p).font = Font(size=8, bold=True)
    c = ws.cell(row=MIXR + 2, column=3 + i,
                value=f'=COUNTIFS(tblRentRoll[Floor Plan],{get_column_letter(3+i)}{MIXR+1})')
    c.font = Font(size=9)
    c.number_format = '#,##0'
ws.cell(row=MIXR + 2, column=2, value='units').font = SM
ws.cell(row=MIXR + 1, column=12, value='total').font = Font(size=8, bold=True)
ws.cell(row=MIXR + 2, column=12, value=f'=SUM(C{MIXR+2}:K{MIXR+2})').font = Font(size=9, bold=True)

# ---------------------------------------------------------------- table
HROW = 10
COLS = [
    ('Month', 11, 'mmm-yy'), ('Basis', 10, '@'),
    ('Market rent\n(T90 HelloData)', 13, '#,##0'),
    ('Effective rent\n(T90 HelloData)', 13, '#,##0'),
    ('Contract rent\n(per occupied)', 13, '#,##0'),
    ('Physical\noccupancy', 11, '0.0%'),
    ('(LTL)/GTL\n%', 10, '+0.0%;-0.0%'),
    ('New\nleases', 9, '#,##0'),
    ('Renew-\nals', 9, '#,##0.0'),
    ('Move-\nouts', 9, '#,##0'),
    ('Leases\nexpiring', 10, '#,##0.0'),
    ('Expiring\nrent', 11, '#,##0'),
    ('Renews\nat', 11, '#,##0'),
    ('Renewal\nincrease %', 12, '+0.0%;-0.0%'),
    ('New lease\nat', 11, '#,##0'),
]
for i, (lab, w, _f) in enumerate(COLS):
    cc = ws.cell(row=HROW, column=2 + i, value=lab)
    cc.fill, cc.font = HDR, WB
    cc.alignment = Alignment(horizontal='center', vertical='bottom', wrap_text=True)
    cc.border = BOX
    ws.column_dimensions[get_column_letter(2 + i)].width = w
ws.row_dimensions[HROW].height = 40

MIX = f'$C${MIXR+2}:$K${MIXR+2}'
HELP0 = 20                     # first helper column (market by plan)
r0 = HROW + 1
ACQ = date(2026, 10, 31)

for i, me in enumerate(MONTHS):
    r = r0 + i
    proj = me > date(2026, 8, 31)
    ws.cell(row=r, column=2, value=me).number_format = 'mmm-yy'
    ws.cell(row=r, column=3, value=('Projected' if proj else 'Actual'))

    # ---- per-plan T90 helpers: same COUNTIFS-guard pattern as the model ----
    for j, p in enumerate(PLANS):
        for blk, fld in ((HELP0, 'Last Asking Rent'), (HELP0 + 10, 'Last Effective Rent')):
            cl = get_column_letter(blk + j)
            prev = f'{cl}{r-1}' if i else '""'
            ws.cell(row=r, column=blk + j, value=(
                f'=IF(COUNTIFS(HDUnitLevel[Floorplan Mapped],{get_column_letter(3+j)}${MIXR+1},'
                f'HDUnitLevel[Off Market Date],">="&$B{r}-{T90},'
                f'HDUnitLevel[Off Market Date],"<="&$B{r})>0,'
                f'AVERAGEIFS(HDUnitLevel[{fld}],HDUnitLevel[Floorplan Mapped],{get_column_letter(3+j)}${MIXR+1},'
                f'HDUnitLevel[Off Market Date],">="&$B{r}-{T90},'
                f'HDUnitLevel[Off Market Date],"<="&$B{r}),{prev})')
            ).number_format = '#,##0'

    hm = f'{get_column_letter(HELP0)}{r}:{get_column_letter(HELP0+8)}{r}'
    he = f'{get_column_letter(HELP0+10)}{r}:{get_column_letter(HELP0+18)}{r}'
    RRA_M = f"INDEX(RRA!$E$48:$EX$48,MATCH($B{r},RRA!$E$33:$EX$33,0))/{UNITS}"
    RRA_A = f"INDEX(RRA!$E$49:$EX$49,MATCH($B{r},RRA!$E$33:$EX$33,0))/{UNITS}"

    # market — HelloData while actual, the RRA's own market path once projected
    ws.cell(row=r, column=4, value=(f'=IFERROR({RRA_M},"")' if proj
                                    else f'=SUMPRODUCT({hm},{MIX})/SUM({MIX})'))
    # effective — the RRA does not project concessions per unit, so history only
    if not proj:
        ws.cell(row=r, column=5, value=f'=SUMPRODUCT({he},{MIX})/SUM({MIX})')
    # contract — T12 Dump while actual; RRA AGPR restated off the vacant-at-market basis
    if proj:
        ws.cell(row=r, column=6, value=(
            f'=IFERROR(({RRA_A}*{UNITS}-(1-$F{r})*{UNITS}*$D{r})/($F{r}*{UNITS}),"")'))
    else:
        ws.cell(row=r, column=6, value=(
            f'=IFERROR((INDEX(\'T12 Dump\'!$D$9:$O$9,MATCH(EOMONTH($B{r},-1)+1,\'T12 Dump\'!$D$3:$O$3,0))'
            f'-ABS(INDEX(\'T12 Dump\'!$D$11:$O$11,MATCH(EOMONTH($B{r},-1)+1,\'T12 Dump\'!$D$3:$O$3,0))))'
            f'/($F{r}*{UNITS}),"")'))
    # occupancy — 1 - vacancy/market (market denominator: vacancy is booked at market)
    ws.cell(row=r, column=7, value=(
        (f"=IFERROR('Cash Flow (Annual)'!${'K' if me < date(2027,12,1) else 'L'}$14,\"\")") if proj else
        f'=IFERROR(1-ABS(INDEX(\'T12 Dump\'!$D$11:$O$11,MATCH(EOMONTH($B{r},-1)+1,\'T12 Dump\'!$D$3:$O$3,0)))'
        f'/INDEX(\'T12 Dump\'!$D$7:$O$7,MATCH(EOMONTH($B{r},-1)+1,\'T12 Dump\'!$D$3:$O$3,0)),"")'))
    ws.cell(row=r, column=8, value=f'=IFERROR($F{r}/$D{r}-1,"")')

    # ---- lease activity ----
    # RR Dump rows 2:361 are row-aligned with RRA rows 109:468 (verified A101<->A101),
    # so a unit's tier and its lease expiration can be combined in one SUMPRODUCT.
    key = f'{me.year}-{me.month:02d}'
    EXPR = "'RR Dump'!$L$2:$L$361"
    RENT = "'RR Dump'!$I$2:$I$361"
    TIER = 'RRA!$A$109:$A$468'
    if proj:
        yc = 'D' if me < date(2026, 12, 1) else ('E' if me < date(2027, 12, 1) else 'F')
        mnth = f'TEXT($B{r},"yyyy-mm")'
        roll1 = f'(TEXT({EXPR},"yyyy-mm")={mnth})'
        roll2 = f'(TEXT(EDATE(N({EXPR}),RRA!$D$4),"yyyy-mm")={mnth})'

        def wt(base):
            """tier-weighted pick from an RRA input block, without array INDEX"""
            return ('(' + '+'.join(f'({TIER}={t})*RRA!${yc}${base+t}' for t in (1, 2, 3, 4)) + ')')

        ws.cell(row=r, column=12, value=f'=SUMPRODUCT({roll1}*1)+SUMPRODUCT({roll2}*1)')
        ws.cell(row=r, column=9,
                value=f'=SUMPRODUCT({roll1}*{wt(14)})+SUMPRODUCT({roll2}*{wt(14)})')
        ws.cell(row=r, column=10, value=f'=IFERROR($L{r}-$J{r},"")')
        ws.cell(row=r, column=11, value=f'=IFERROR($K{r},"")')
        ws.cell(row=r, column=13,
                value=f'=IFERROR(SUMPRODUCT({roll1}*N({RENT}))/SUMPRODUCT({roll1}*1),"")')
        # cohort-weighted move-to-market and minimum renewal increase for the month
        ws.cell(row=r, column=HELP0 + 20,
                value=f'=IFERROR(SUMPRODUCT({roll1}*{wt(19)})/SUMPRODUCT({roll1}*1),0)')
        ws.cell(row=r, column=HELP0 + 21,
                value=f'=IFERROR(SUMPRODUCT({roll1}*{wt(24)})/SUMPRODUCT({roll1}*1),0)')
        mw = f'{get_column_letter(HELP0+20)}{r}'
        iw = f'{get_column_letter(HELP0+21)}{r}'
        ws.cell(row=r, column=14,
                value=f'=IFERROR(MAX($M{r}+{mw}*($D{r}-$M{r}),$M{r}*(1+{iw})),"")')
        ws.cell(row=r, column=15, value=f'=IFERROR($N{r}/$M{r}-1,"")')
        ws.cell(row=r, column=16, value=f'=IFERROR($D{r},"")')
    else:
        h = HIST.get(key, {})
        for cidx, k in ((9, 'new'), (10, 'ren'), (11, 'out')):
            v = h.get(k)
            cc = ws.cell(row=r, column=cidx, value=v)
            cc.fill = STATIC
        cc = ws.cell(row=r, column=15, value=h.get('ren_inc'))
        cc.fill = STATIC

    for j in range(len(COLS)):
        cc = ws.cell(row=r, column=2 + j)
        cc.number_format = COLS[j][2]
        cc.border = BOX
        cc.font = Font(size=9)
        cc.alignment = Alignment(horizontal='center')
        if proj and j > 0:
            if cc.fill.fgColor.rgb in (None, '00000000'):
                cc.fill = PROJ

LAST = r0 + len(MONTHS) - 1
for j in range(len(PLANS) * 2 + 10):
    ws.column_dimensions[get_column_letter(HELP0 + j)].hidden = True
ws.cell(row=HROW - 1, column=HELP0, value='T90 helper block — market by plan, then effective by plan (hidden)').font = SM

# ---------------------------------------------------------------- recon
R = LAST + 3
ws.cell(row=R, column=2, value='RECONCILIATION — this tab vs Cash Flow (Annual)').font = Font(bold=True, size=10, color=NAVY)
recon = [
    ('Market rent /unit, Y1', f"='Cash Flow (Annual)'!$K$4", f'=AVERAGEIFS($D${r0}:$D${LAST},$B${r0}:$B${LAST},">="&DATE(2026,12,1),$B${r0}:$B${LAST},"<="&DATE(2027,11,30))'),
    ('Market rent /unit, Y2', f"='Cash Flow (Annual)'!$L$4", f'=AVERAGEIFS($D${r0}:$D${LAST},$B${r0}:$B${LAST},">="&DATE(2027,12,1),$B${r0}:$B${LAST},"<="&DATE(2028,11,30))'),
    ('Contract rent /unit, Y1', f"=RRA!$H$4/{UNITS}/12", f'=AVERAGEIFS($F${r0}:$F${LAST},$B${r0}:$B${LAST},">="&DATE(2026,12,1),$B${r0}:$B${LAST},"<="&DATE(2027,11,30))'),
    ('Contract rent /unit, Y2', f"=RRA!$I$4/{UNITS}/12", f'=AVERAGEIFS($F${r0}:$F${LAST},$B${r0}:$B${LAST},">="&DATE(2027,12,1),$B${r0}:$B${LAST},"<="&DATE(2028,11,30))'),
    ('Physical occupancy, Y1', f"='Cash Flow (Annual)'!$K$14", f'=AVERAGEIFS($G${r0}:$G${LAST},$B${r0}:$B${LAST},">="&DATE(2026,12,1),$B${r0}:$B${LAST},"<="&DATE(2027,11,30))'),
    ('(LTL)/GTL %, Y1', '=RRA!$H$6', f'=AVERAGEIFS($H${r0}:$H${LAST},$B${r0}:$B${LAST},">="&DATE(2026,12,1),$B${r0}:$B${LAST},"<="&DATE(2027,11,30))'),
]
for k, (lab, mf, tf) in enumerate(recon):
    ws.cell(row=R + 1 + k, column=2, value=lab).font = Font(size=9)
    a = ws.cell(row=R + 1 + k, column=5, value=mf)
    b = ws.cell(row=R + 1 + k, column=6, value=tf)
    d = ws.cell(row=R + 1 + k, column=7, value=f'=IFERROR($F{R+1+k}-$E{R+1+k},"")')
    for cc, fmt in ((a, '#,##0.00'), (b, '#,##0.00'), (d, '#,##0.00')):
        cc.number_format = '0.0%' if 'occupancy' in lab or 'GTL' in lab else fmt
        cc.font = Font(size=9)
        cc.border = BOX
for lab, cc in (('model', 5), ('this tab', 6), ('diff', 7)):
    h = ws.cell(row=R, column=cc, value=lab)
    h.font = Font(size=8, bold=True, color=NAVY)
    h.alignment = Alignment(horizontal='center')

# ------------------------------------------------------- independent self-check
SC = R + len(recon) + 2
ws.cell(row=SC, column=2, value='SELF-CHECK — expected values computed independently in Python from the raw '
        'documents. If a formula failed to resolve, these will not match.').font = Font(bold=True, size=9, color=ACCENT)
CHECKS = [
    ('Market rent, Jul-2026 (T90 HelloData)', 1893, f'=$D${r0+24}'),
    ('Effective rent, Jul-2026', 1893, f'=$E${r0+24}'),
    ('Contract rent, Jun-2026', 1732, f'=$F${r0+23}'),
    ('Physical occupancy, Jun-2026', 0.963, f'=$G${r0+23}'),
    ('Market rent /unit, Y1 avg (RRA)', 1915, f"='Cash Flow (Annual)'!$K$4"),
    ('Contract rent /unit, Y1 avg (RRA)', 1845, f'=RRA!$H$4/{UNITS}/12'),
    ('Leases expiring, Aug-2027', 58, f'=$L${r0+37}'),
]
for k, (lab, exp, f) in enumerate(CHECKS):
    ws.cell(row=SC + 1 + k, column=2, value=lab).font = Font(size=9)
    e = ws.cell(row=SC + 1 + k, column=5, value=exp)
    a = ws.cell(row=SC + 1 + k, column=6, value=f)
    d = ws.cell(row=SC + 1 + k, column=7, value=f'=IFERROR(ABS($F{SC+1+k}-$E{SC+1+k})<MAX(2,$E{SC+1+k}*0.02),FALSE)')
    for cc in (e, a):
        cc.number_format = '0.0%' if 'occupancy' in lab else '#,##0'
        cc.font = Font(size=9)
        cc.border = BOX
    d.font = Font(size=9, bold=True)
    d.border = BOX
for lab, cc in (('expected', 5), ('this tab', 6), ('within 2%?', 7)):
    hh = ws.cell(row=SC, column=cc, value=lab)
    hh.font = Font(size=8, bold=True, color=ACCENT)
    hh.alignment = Alignment(horizontal='center')

# ---------------------------------------------------------------- charts
def axis(ch, t=None):
    ch.y_axis.majorGridlines = ChartLines()
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    if t:
        ch.y_axis.title = t
    ch.height, ch.width = 7.4, 34


c1 = LineChart(); c1.title = 'Rent per unit / month — market, effective, contract'
for col in (4, 5, 6):
    c1.add_data(Reference(ws, min_col=col, min_row=HROW, max_row=LAST), titles_from_data=True)
c1.set_categories(Reference(ws, min_col=2, min_row=r0, max_row=LAST))
axis(c1, '$ / unit')
for s in c1.series:
    s.smooth = False
ws.add_chart(c1, f'B{SC+12}')

c2 = BarChart(); c2.type, c2.grouping, c2.overlap = 'col', 'clustered', -10
c2.title = 'Lease activity — new leases, renewals, move-outs'
for col in (9, 10, 11):
    c2.add_data(Reference(ws, min_col=col, min_row=HROW, max_row=LAST), titles_from_data=True)
c2.set_categories(Reference(ws, min_col=2, min_row=r0, max_row=LAST))
axis(c2, 'units')
ws.add_chart(c2, f'B{SC+28}')

c3 = LineChart(); c3.title = 'Renewal increase % — achieved vs underwritten'
c3.add_data(Reference(ws, min_col=15, min_row=HROW, max_row=LAST), titles_from_data=True)
c3.set_categories(Reference(ws, min_col=2, min_row=r0, max_row=LAST))
axis(c3, '%')
c3.height = 5.4
ws.add_chart(c3, f'B{SC+44}')

ws.freeze_panes = f'C{r0}'
ws.sheet_view.showGridLines = False
wb.save(OUT)
print(f'wrote {OUT}')
print(f'  months {MONTHS[0]} -> {MONTHS[-1]} ({len(MONTHS)} rows {r0}-{LAST})')
print(f'  reconciliation block at row {R}, charts below')
