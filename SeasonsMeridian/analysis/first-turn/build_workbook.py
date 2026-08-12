#!/usr/bin/env python3
"""Build 'Seasons at Meridian - First Turn Analysis.xlsx' from ledger.csv.

Tabs: Summary (headline metrics, all formulas over the ledger), Unit Ledger
(314-row audit trail), By Floor Plan, By Month, Notes (methodology/caveats).
"""
import csv
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ARIAL = 'Arial'
NAVY = '1F3864'
LIGHT = 'D9E2F3'
GREY = 'F2F2F2'
H_FILL = PatternFill('solid', fgColor=NAVY)
H_FONT = Font(name=ARIAL, size=9, bold=True, color='FFFFFF')
BASE = Font(name=ARIAL, size=10)
BOLD = Font(name=ARIAL, size=10, bold=True)
TITLE = Font(name=ARIAL, size=14, bold=True, color=NAVY)
SUB = Font(name=ARIAL, size=9, italic=True, color='595959')
THIN = Border(bottom=Side(style='thin', color='BFBFBF'))

FMT_D = 'mm/dd/yyyy'
FMT_C = '$#,##0'
FMT_C2 = '$#,##0.00'
FMT_P = '+0.0%;-0.0%;0.0%'
FMT_P0 = '0.0%'
FMT_N = '#,##0'


def fd(s):
    return datetime.strptime(s, '%Y-%m-%d').date() if s else None


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


rows = list(csv.DictReader(open('ledger.csv')))
NR = len(rows)
FIRST, LAST = 2, NR + 1

BEDS = {'S1_Seas': 'Studio', 'A1_Seas': '1x1', 'A2_Seas': '1x1',
        'B1_Seas': '2x2', 'B2_Seas': '2x2', 'B3a_Seas': '2x2', 'B3b_Seas': '2x2',
        'C1a_Seas': '3x2', 'C1b_Seas': '3x2'}

wb = openpyxl.Workbook()

# ============================= UNIT LEDGER =============================
ws = wb.active
ws.title = 'Unit Ledger'
headers = [
    ('Unit', 7), ('Unit Type', 9), ('Beds', 7), ('SF', 6), ('Resident ID', 10),
    ('Resident', 20), ('Move In', 10), ('Initial Term (mo)', 8),
    ('Orig. First Expiration', 11), ('Exp Month', 9), ('Orig. Exp Source', 22),
    ('Initial Gross Rent', 10), ('Initial Concession ($)', 10),
    ('Initial Effective Rent', 10), ('Initial Rent Source', 24), ('Concession Source', 22),
    ('Outcome', 15), ('Expired by 8/4/26', 8), ('In Retention Denom', 8),
    ('Early Term', 7), ('Notice', 7), ('Exclude', 7),
    ('Renewal Date', 10), ('Renewal Term (mo)', 8), ('Renewal Gross Rent', 10),
    ('Renewal Concession ($)', 10), ('Renewal Effective Rent', 10), ('In Renewal Report', 8),
    ('Renewal Trade-Out Gross %', 9), ('Renewal Trade-Out Eff %', 9),
    ('Vacated Date', 10), ('New Resident ID', 10), ('New Resident', 20),
    ('New Move In', 10), ('New Lease Term (mo)', 8), ('New Gross Rent', 10),
    ('New Concession ($)', 10), ('New Effective Rent', 10),
    ('New-Lease Trade-Out Gross %', 9), ('New-Lease Trade-Out Eff %', 9),
    ('Days Vacant', 7), ('Re-Lease Month', 9),
]
for j, (h, w) in enumerate(headers, 1):
    c = ws.cell(row=1, column=j, value=h)
    c.font, c.fill = H_FONT, H_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    ws.column_dimensions[get_column_letter(j)].width = w
ws.row_dimensions[1].height = 42

for i, r in enumerate(rows):
    rn = i + 2
    vals = [
        r['unit'], r['unit_type'], BEDS.get(r['unit_type'], '?'), fnum(r['sf']),
        r['resident_id'], r['name'], fd(r['move_in']), fnum(r['initial_term_mo']),
        fd(r['orig_expiration']),
        r['orig_expiration'][:7] if r['orig_expiration'] else None,
        r['orig_exp_source'],
        fnum(r['initial_gross']), fnum(r['initial_conc_total']),
        f'=IF(OR($L{rn}="",$H{rn}="",$H{rn}=0),"",$L{rn}-N($M{rn})/$H{rn})',
        r['initial_gross_source'], r['initial_conc_source'],
        r['outcome'], r['expired_by_cutoff'], r['in_retention_denom'],
        r['early_term'], r['notice'], r['exclude'],
        fd(r['renewal_date']), fnum(r['renewal_term_mo']), fnum(r['renewal_gross']),
        fnum(r['renewal_conc_total']),
        f'=IF(OR($Y{rn}="",$X{rn}="",$X{rn}=0),"",$Y{rn}-N($Z{rn})/$X{rn})',
        r['renewal_in_report'],
        f'=IF(OR($Y{rn}="",$L{rn}="",$L{rn}=0),"",$Y{rn}/$L{rn}-1)',
        f'=IF(OR($AA{rn}="",$N{rn}="",$N{rn}=0),"",$AA{rn}/$N{rn}-1)',
        fd(r['vacated_date']), r['new_resident_id'], r['new_name'],
        fd(r['new_move_in']), fnum(r['new_lease_term_mo']), fnum(r['new_gross']),
        fnum(r['new_conc_total']),
        f'=IF(OR($AJ{rn}="",$AI{rn}="",$AI{rn}=0),"",$AJ{rn}-N($AK{rn})/$AI{rn})',
        f'=IF(OR($AJ{rn}="",$L{rn}="",$L{rn}=0),"",$AJ{rn}/$L{rn}-1)',
        f'=IF(OR($AL{rn}="",$N{rn}="",$N{rn}=0),"",$AL{rn}/$N{rn}-1)',
        fnum(r['days_vacant']),
        r['new_move_in'][:7] if r['new_move_in'] else None,
    ]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=rn, column=j, value=v)
        c.font = BASE
    for col, fmt in (('G', FMT_D), ('I', FMT_D), ('W', FMT_D), ('AE', FMT_D), ('AH', FMT_D),
                     ('L', FMT_C), ('M', FMT_C), ('N', FMT_C2), ('Y', FMT_C), ('Z', FMT_C),
                     ('AA', FMT_C2), ('AJ', FMT_C), ('AK', FMT_C), ('AL', FMT_C2),
                     ('AC', FMT_P), ('AD', FMT_P), ('AM', FMT_P), ('AN', FMT_P),
                     ('D', FMT_N), ('AO', FMT_N)):
        ws[f'{col}{rn}'].number_format = fmt
    if i % 2 == 1:
        for j in range(1, len(headers) + 1):
            ws.cell(row=rn, column=j).fill = PatternFill('solid', fgColor=GREY)
ws.freeze_panes = 'G2'
ws.auto_filter.ref = f'A1:AP{LAST}'

L = "'Unit Ledger'!"
def rng(col):
    return f'{L}${col}${FIRST}:${col}${LAST}'

# ============================= SUMMARY =============================
sm = wb.create_sheet('Summary', 0)
sm.sheet_view.showGridLines = False
for w, cw in zip('ABCDEFG', (44, 12, 12, 12, 12, 12, 12)):
    sm.column_dimensions[w].width = cw

sm['A1'] = 'Seasons at Meridian — First Turn of the Rent Roll'
sm['A1'].font = TITLE
sm['A2'] = ('Initial tenant cohort = 314 residents in place on the 1/1/2026 rent roll, tracked to the '
            '8/4/2026 rent roll. Measurement date: 8/4/2026.')
sm['A2'].font = SUB
sm['A3'] = ('Convention: Retention = renewals ÷ initial leases whose first expiration came due by 8/4/26. '
            'Early terminations (left before expiration) are excluded from the ratio until their expiration '
            'passes, and shown separately. Early renewals count as renewed at their original expiration.')
sm['A3'].font = SUB

def put(cell, label, formula, fmt=FMT_N, bold=False, note=None):
    sm[cell] = label
    sm[cell].font = BOLD if bold else BASE
    v = sm.cell(row=sm[cell].row, column=2, value=formula)
    v.font = BOLD if bold else BASE
    v.number_format = fmt
    if note:
        n = sm.cell(row=sm[cell].row, column=3, value=note)
        n.font = SUB
        n.alignment = Alignment(horizontal='left')

def hdr(cell, text):
    sm[cell] = text
    sm[cell].font = Font(name=ARIAL, size=11, bold=True, color='FFFFFF')
    sm[cell].fill = H_FILL
    for col in 'BCDEFG':
        sm[f'{col}{sm[cell].row}'].fill = H_FILL

hdr('A5', 'RETENTION — FIRST TURN')
put('A6', 'Initial cohort (residents on 1/1/26 roll)', f'=COUNTA({rng("A")})')
put('A7', 'First expirations come due by 8/4/26', f'=COUNTIF({rng("S")},"Y")', bold=True)
put('A8', '    Renewed', f'=COUNTIFS({rng("S")},"Y",{rng("Q")},"Renewed")')
put('A9', '    Moved out', f'=COUNTIFS({rng("S")},"Y",{rng("Q")},"Moved Out")')
put('A10', '    Month-to-month holdover (no new lease yet)', f'=COUNTIFS({rng("S")},"Y",{rng("Q")},"MTM Holdover")')
put('A11', 'RETENTION RATIO (renewed ÷ expirations)', '=B8/B7', FMT_P0, bold=True)
put('A12', 'Retention if MTM holdovers ultimately renew', '=(B8+B10)/B7', FMT_P0,
    note='Upper bound — 7 tenants expired but still in place without a new lease')
put('A14', 'Early terminations, expiration not yet due', f'=COUNTIFS({rng("Q")},"Moved Out",{rng("S")},"<>Y")',
    note='Lease-breaks/skips; real attrition but no renewal decision yet')
put('A15', 'All-in retention (early terms counted as lost)', '=B8/(B7+B14)', FMT_P0)
put('A16', 'Not yet expired (first turn still ahead)', f'=COUNTIFS({rng("Q")},"Not Yet Expired")')

hdr('A18', 'RENEWAL TRADE-OUT (n = renewed; corporate excluded)')
sm['B19'], sm['C19'], sm['D19'] = 'Average', 'Median', 'n'
for c in ('B19', 'C19', 'D19'):
    sm[c].font = Font(name=ARIAL, size=9, bold=True, color='595959')
put('A20', 'Gross trade-out (contract rent → contract rent)',
    f'=AVERAGEIFS({rng("AC")},{rng("Q")},"Renewed",{rng("V")},"<>Y")', FMT_P, bold=True)
sm['C20'] = f'=MEDIAN({rng("AC")})'
sm['C20'].number_format = FMT_P
sm['D20'] = f'=COUNTIFS({rng("Q")},"Renewed",{rng("V")},"<>Y",{rng("Y")},">0")'
put('A21', 'Effective trade-out (net of concessions, amortized)',
    f'=AVERAGEIFS({rng("AD")},{rng("Q")},"Renewed",{rng("V")},"<>Y")', FMT_P, bold=True)
sm['C21'] = f'=MEDIAN({rng("AD")})'
sm['C21'].number_format = FMT_P
sm['D21'] = '=D20'
put('A22', 'Avg prior gross rent → avg renewal gross rent',
    f'=AVERAGEIFS({rng("L")},{rng("Q")},"Renewed",{rng("V")},"<>Y")', FMT_C)
sm['C22'] = f'=AVERAGEIFS({rng("Y")},{rng("Q")},"Renewed",{rng("V")},"<>Y")'
sm['C22'].number_format = FMT_C
put('A23', 'Renewals signing at flat/zero gross increase',
    f'=COUNTIFS({rng("Q")},"Renewed",{rng("AC")},"<=0",{rng("V")},"<>Y")',
    note='Flat renewals are invisible without lease-start data — see Notes')

hdr('A25', 'NEW-LEASE TRADE-OUT (turned units re-leased; corporate excluded)')
sm['B26'], sm['C26'], sm['D26'] = 'Average', 'Median', 'n'
for c in ('B26', 'C26', 'D26'):
    sm[c].font = Font(name=ARIAL, size=9, bold=True, color='595959')
put('A27', 'Gross trade-out (prior tenant → new tenant)',
    f'=AVERAGEIFS({rng("AM")},{rng("Q")},"Moved Out",{rng("V")},"<>Y")', FMT_P, bold=True)
sm['C27'] = f'=MEDIAN({rng("AM")})'
sm['C27'].number_format = FMT_P
sm['D27'] = f'=COUNTIFS({rng("Q")},"Moved Out",{rng("V")},"<>Y",{rng("AJ")},">0")'
put('A28', 'Effective trade-out (net of concessions both sides)',
    f'=AVERAGEIFS({rng("AN")},{rng("Q")},"Moved Out",{rng("V")},"<>Y")', FMT_P, bold=True)
sm['C28'] = f'=MEDIAN({rng("AN")})'
sm['C28'].number_format = FMT_P
sm['D28'] = f'=SUMPRODUCT(({rng("Q")}="Moved Out")*({rng("V")}<>"Y")*ISNUMBER({rng("AN")}))'
put('A29', 'Avg prior tenant gross → avg new tenant gross',
    f'=AVERAGEIFS({rng("L")},{rng("Q")},"Moved Out",{rng("AJ")},">0",{rng("V")},"<>Y")', FMT_C)
sm['C29'] = f'=AVERAGEIFS({rng("AJ")},{rng("Q")},"Moved Out",{rng("AJ")},">0",{rng("V")},"<>Y")'
sm['C29'].number_format = FMT_C
put('A30', 'Avg days vacant between tenants',
    f'=AVERAGEIFS({rng("AO")},{rng("Q")},"Moved Out")', FMT_N)

hdr('A32', 'CONCESSION BURN-OFF (the real story)')
put('A33', 'Initial leases with a concession (where known)',
    f'=COUNTIF({rng("M")},">0")/(COUNTIF({rng("M")},">0")+COUNTIF({rng("M")},"0"))', FMT_P0,
    note='Denominator = leases with concession data')
put('A34', 'Avg initial concession (leases w/ concession)',
    f'=AVERAGEIF({rng("M")},">0")', FMT_C)
put('A35', 'Avg initial concession in months free',
    f'=AVERAGEIF({rng("M")},">0")/AVERAGEIFS({rng("L")},{rng("M")},">0")', '0.0 "mo"')
put('A36', 'Avg concession on renewal leases',
    f'=AVERAGEIFS({rng("Z")},{rng("Q")},"Renewed")', FMT_C,
    note='Concessions largely disappear at renewal — hence eff >> gross trade-out')
put('A37', 'Avg concession on replacement (new) leases',
    f'=AVERAGEIFS({rng("AK")},{rng("Q")},"Moved Out",{rng("AJ")},">0")', FMT_C)

sm['A39'] = ('Sources: Yardi rent rolls (1/1, 7/07, 7/19, 8/4/2026), Concession Burn Off (6/21, 7/30/2026 — lease start dates), '
             'Renewal Tradeouts report (5/10–7/9/2026), HelloData unit details (8/12/2026). See Notes tab for methodology and caveats.')
sm['A39'].font = SUB

# ============================= BY FLOOR PLAN =============================
fp = wb.create_sheet('By Floor Plan')
fp.sheet_view.showGridLines = False
cols = [('Group', 12), ('Cohort Units', 9), ('Expirations Due', 10), ('Renewed', 9),
        ('Moved Out', 9), ('MTM', 7), ('Retention %', 10),
        ('Avg Initial Gross', 10), ('Renewal TO Gross %', 10), ('Renewal TO Eff %', 10),
        ('New-Lease TO Gross %', 10), ('New-Lease TO Eff %', 10)]
for j, (h, w) in enumerate(cols, 1):
    c = fp.cell(row=1, column=j, value=h)
    c.font, c.fill = H_FONT, H_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    fp.column_dimensions[get_column_letter(j)].width = w
fp.row_dimensions[1].height = 30

types = sorted({r['unit_type'] for r in rows})
beds_order = ['Studio', '1x1', '2x2', '3x2']

def fp_row(rn, label, crit_col, crit_val, bold=False):
    K = f'{L}${crit_col}${FIRST}:${crit_col}${LAST}'
    if crit_val is None:
        cnt_all = f'=COUNTA({rng("A")})'
        base = [f'({rng("S")}="Y")']
        crit = ''
    else:
        cnt_all = f'=COUNTIF({K},"{crit_val}")'
        crit = f',{K},"{crit_val}"'
    def cifs(qval, extra=''):
        cv = f'{K},"{crit_val}",' if crit_val is not None else ''
        return f'=COUNTIFS({cv}{rng("S")},"Y",{rng("Q")},"{qval}"{extra})'
    def aifs(acol, qval, extra=''):
        cv = f',{K},"{crit_val}"' if crit_val is not None else ''
        return f'=IFERROR(AVERAGEIFS({rng(acol)},{rng("Q")},"{qval}",{rng("V")},"<>Y"{cv}{extra}),"")'
    vals = [label, cnt_all, None, cifs('Renewed'), cifs('Moved Out'), cifs('MTM Holdover'),
            f'=IF(C{rn}=0,"",D{rn}/C{rn})',
            (f'=IFERROR(AVERAGEIFS({rng("L")},{rng("Q")},"<>zz"' +
             (f',{K},"{crit_val}"' if crit_val is not None else '') + '),"")'),
            aifs('AC', 'Renewed'), aifs('AD', 'Renewed'),
            aifs('AM', 'Moved Out'), aifs('AN', 'Moved Out')]
    vals[2] = f'=D{rn}+E{rn}+F{rn}'
    for j, v in enumerate(vals, 1):
        c = fp.cell(row=rn, column=j, value=v)
        c.font = BOLD if bold else BASE
    fp[f'G{rn}'].number_format = FMT_P0
    fp[f'H{rn}'].number_format = FMT_C
    for col in ('I', 'J', 'K', 'L'):
        fp[f'{col}{rn}'].number_format = FMT_P

rn = 2
for t in types:
    fp_row(rn, t, 'B', t)
    rn += 1
rn += 1
for b in beds_order:
    fp_row(rn, b, 'C', b, bold=True)
    rn += 1
rn += 1
fp_row(rn, 'TOTAL', 'C', None, bold=True)
fp.freeze_panes = 'B2'

# ============================= BY MONTH =============================
bm = wb.create_sheet('By Month')
bm.sheet_view.showGridLines = False
cols = [('Month', 14), ('Expirations Due', 9), ('Renewed', 8), ('Moved Out', 8),
        ('MTM', 6), ('Retention %', 9),
        ('Renewal: Prior Gross $', 10), ('Renewal: New Gross $', 10), ('Renewal TO Gross %', 9),
        ('Renewal: Prior Eff $', 10), ('Renewal: New Eff $', 10), ('Renewal TO Eff %', 9),
        ('Units Re-Leased (n)', 9),
        ('New Lease: Prior Gross $', 10), ('New Lease: New Gross $', 10), ('New-Lease TO Gross %', 9),
        ('New Lease: Prior Eff $', 10), ('New Lease: New Eff $', 10), ('New-Lease TO Eff %', 9),
        ('Coming Due (not yet expired)', 10)]
for j, (h, w) in enumerate(cols, 1):
    c = bm.cell(row=1, column=j, value=h)
    c.font, c.fill = H_FONT, H_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    bm.column_dimensions[get_column_letter(j)].width = w
bm.row_dimensions[1].height = 42

exp_months = {r['orig_expiration'][:7] for r in rows if r['orig_expiration']}
rel_months = {r['new_move_in'][:7] for r in rows if r['new_move_in'] and r['outcome'] == 'Moved Out'}
months = sorted(exp_months | rel_months)
PCT_COLS = ('F', 'I', 'L', 'P', 'S')
USD_COLS = ('G', 'H', 'J', 'K', 'N', 'O', 'Q', 'R')
rn = 2
for m in months:
    MK = f'{rng("J")},"{m}"'                      # original first-expiration month
    RK = f'{rng("AP")},"{m}"'                     # re-lease (new tenant move-in) month
    def cifs(qval):
        return f'=COUNTIFS({MK},{rng("S")},"Y",{rng("Q")},"{qval}")'
    def aifs(acol):                               # renewal metrics, keyed to exp month
        return (f'=IFERROR(AVERAGEIFS({rng(acol)},{MK},{rng("Q")},"Renewed",'
                f'{rng("V")},"<>Y"),"")')
    def aifs_rel(acol):                           # new-lease metrics, keyed to re-lease month
        return (f'=IFERROR(AVERAGEIFS({rng(acol)},{RK},{rng("Q")},"Moved Out",'
                f'{rng("V")},"<>Y"),"")')
    vals = [m, f'=C{rn}+D{rn}+E{rn}', cifs('Renewed'), cifs('Moved Out'), cifs('MTM Holdover'),
            f'=IF(B{rn}=0,"",C{rn}/B{rn})',
            aifs('L'), aifs('Y'), aifs('AC'),
            aifs('N'), aifs('AA'), aifs('AD'),
            f'=COUNTIFS({RK},{rng("Q")},"Moved Out")',
            aifs_rel('L'), aifs_rel('AJ'), aifs_rel('AM'),
            aifs_rel('N'), aifs_rel('AL'), aifs_rel('AN'),
            f'=COUNTIFS({MK},{rng("Q")},"Not Yet Expired")']
    for j, v in enumerate(vals, 1):
        c = bm.cell(row=rn, column=j, value=v)
        c.font = BASE
    bm[f'F{rn}'].number_format = FMT_P0
    for col in ('I', 'L', 'P', 'S'):
        bm[f'{col}{rn}'].number_format = FMT_P
    for col in USD_COLS:
        bm[f'{col}{rn}'].number_format = FMT_C
    rn += 1
tot = rn
bm.cell(row=tot, column=1, value='TOTAL / AVG').font = BOLD
for j, col in enumerate('BCDE', 2):
    c = bm.cell(row=tot, column=j, value=f'=SUM({col}2:{col}{tot-1})')
    c.font = BOLD
c = bm.cell(row=tot, column=6, value=f'=IF(B{tot}=0,"",C{tot}/B{tot})')
c.font, c.number_format = BOLD, FMT_P0
tot_ren = [('G', 'L'), ('H', 'Y'), ('I', 'AC'), ('J', 'N'), ('K', 'AA'), ('L', 'AD')]
for col, acol in tot_ren:
    c = bm.cell(row=tot, column=ord(col) - 64,
                value=f'=IFERROR(AVERAGEIFS({rng(acol)},{rng("Q")},"Renewed",{rng("V")},"<>Y"),"")')
    c.font = BOLD
    c.number_format = FMT_P if col in ('I', 'L') else FMT_C
c = bm.cell(row=tot, column=13, value=f'=SUM(M2:M{tot-1})')
c.font = BOLD
tot_nl = [(14, 'L'), (15, 'AJ'), (16, 'AM'), (17, 'N'), (18, 'AL'), (19, 'AN')]
for coln, acol in tot_nl:
    c = bm.cell(row=tot, column=coln,
                value=f'=IFERROR(AVERAGEIFS({rng(acol)},{rng("Q")},"Moved Out",{rng("V")},"<>Y"),"")')
    c.font = BOLD
    c.number_format = FMT_P if coln in (16, 19) else FMT_C
c = bm.cell(row=tot, column=20, value=f'=SUM(T2:T{tot-1})')
c.font = BOLD
note = bm.cell(row=tot + 2, column=1,
               value=('Columns B–L are keyed to each initial lease\'s ORIGINAL first-expiration month (the '
                      'renewal decision). Columns M–S are keyed to the month the replacement tenant moved in, '
                      'so re-leases after early lease-breaks appear when they actually happened — not at the '
                      'broken lease\'s future expiration date. Column T counts initial leases whose first '
                      'expiration is still ahead. $ columns are simple averages of the leases in that month, '
                      'so the % columns (avg of per-lease trade-outs) won\'t exactly equal the ratio of the '
                      '$ averages. Prior-lease $ for new leases = the departed initial tenant\'s rent on the '
                      'same unit. TOTAL/AVG row: counts are sums; $ and % are averages across all leases.'))
note.font = SUB
note.alignment = Alignment(wrap_text=True, vertical='top')
bm.merge_cells(start_row=tot + 2, start_column=1, end_row=tot + 5, end_column=20)
bm.freeze_panes = 'B2'

# ============================= NOTES =============================
nt = wb.create_sheet('Notes')
nt.sheet_view.showGridLines = False
nt.column_dimensions['A'].width = 130
notes = [
    ('Seasons at Meridian — First Turn Analysis: Methodology & Caveats', TITLE),
    ('', None),
    ('COHORT & CONVENTION', BOLD),
    ('• Cohort = 314 residents in place on the 1/1/2026 rent roll (360 units, 87% occupied). Tracked by Yardi Resident ID into the 8/4/2026 rent roll.', None),
    ('• Retention = renewals ÷ initial leases whose first expiration came due by 8/4/2026. MTM holdovers stay in the denominator (not renewed, not gone).', None),
    ('• Early terminations (moved out before first expiration) are excluded from the ratio until their expiration month passes; shown separately and in the all-in ratio.', None),
    ('• Early renewals count as renewed as of their original expiration date. One corporate lease (B307, Coleman Environmental) is excluded from all trade-out averages.', None),
    ('', None),
    ('RENEWAL IDENTIFICATION', BOLD),
    ('• Primary: Concession Burn Off reports (6/21 & 7/30/2026) — the only source with Lease Start Date. Current lease start > move-in +45 days = renewal.', None),
    ('• The Renewal Tradeouts report (5/10–7/9/2026) supplies exact prior/new concession and term detail for the 23 renewals in its window (all 23 reconcile with the ledger).', None),
    ('• 10 tenants renewed before 1/1/2026 (moved in Aug 2024–early 2025). Their initial rent comes from their HelloData leasing episode, since the Jan roll already shows renewal rent.', None),
    ('', None),
    ('RENT & CONCESSION SOURCES (priority order, per lease)', BOLD),
    ('• Initial gross rent: 1/1/2026 rent roll Actual Rent (validated = as-of-January charge). Fallbacks for Yardi zero-charge rows: 6/21 burn-off Lease Rent, then HelloData last asking.', None),
    ('• Initial concessions: Renewal report prior-lease detail > Burn-off current-lease concessions (tenants still on initial lease) > HelloData (ask − effective) × term. 21 leases have no concession data; effective = gross for those (conservative).', None),
    ('• Renewal / new-lease concessions: Burn-off exact dollars (current lease), Renewal report for in-window renewals. Effective rent = gross − concession ÷ lease term (report convention).', None),
    ('• New-lease rents: 8/4/2026 rent roll. HelloData cross-validation: 64 of 71 matched 2026 move-ins have Last Asking = contract rent to the dollar; units go off-market a median 15 days before move-in.', None),
    ('', None),
    ('DATA CAVEATS', BOLD),
    ('• The "1/1/2026" rent roll is BACKDATED (generated ~Aug 2026): its roster and rents are as-of-January and reliable, but its lease-expiration and move-out columns carry current data. Original first expirations for renewed tenants are reconstructed from the renewal report (Old Expiration) or the renewal lease start −1 day.', None),
    ('• Blind spot: a tenant who renewed AND moved out before 6/21/2026 would be misread as a move-out on their initial lease. Bounded small: first expirations only began ~Aug 2025 and rent-change cross-checks caught none.', None),
    ('• Initial lease terms were staggered on purpose (12mo ×173, 18mo ×63, plus 9–17mo tranches per the burn-off), so expiration timing, not move-in timing, drives when the first turn hits.', None),
    ('• Trade-out percentages compare monthly rent levels; they do not annualize term differences. Effective trade-outs amortize upfront concessions over the lease term.', None),
    ('', None),
    ('SOURCE FILES (../../documents/)', BOLD),
    ('• rent-rolls/: RentRoll_AsOf_2026-01-01_BACKDATED, _07-07, _07-19, _08-04, withLeaseCharges_07-09', None),
    ('• concession-burnoff/: 6/21 & 7/30/2026 · renewal-reports/: 5/10–7/9/2026 · hellodata/: 8/12/2026 export · t12/: Jun25–May26, Jul25–Jun26', None),
    ('• Rebuild: python3 build_ledger.py && python3 build_workbook.py (analysis/first-turn/)', None),
]
for i, (txt, fnt) in enumerate(notes, 1):
    c = nt.cell(row=i, column=1, value=txt)
    c.font = fnt or BASE
    c.alignment = Alignment(wrap_text=True, vertical='top')

for s, color in ((sm, '1F3864'), (ws, '4472C4'), (fp, '4472C4'), (bm, '4472C4'), (nt, 'A6A6A6')):
    s.sheet_properties.tabColor = color

out = 'Seasons at Meridian - First Turn Analysis.xlsx'
wb.save(out)
print('wrote', out)
