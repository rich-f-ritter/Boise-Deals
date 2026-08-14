#!/usr/bin/env python3
"""Build Seasons Y1 UW vs Prelude Y1 UW vs Prelude Actuals comparison workbook."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC_T12 = 'prelude_t12.xlsx'
OUT = 'Seasons_Y1_vs_Prelude_UW_vs_Actual.xlsx'

# ---------------------------------------------------------------- category map
# Prelude 12-mo accrual statement (Aug-25..Jul-26): leaf account -> TMG category
CATMAP = {
    # revenue
    '41000-000': 'GPR', '41010-000': 'LTL',
    '41091-000': 'Concessions', '41092-000': 'Concessions',
    '41100-000': 'Vacancy', '41110-000': 'ModelEmp',
    '41150-000': 'BadDebt', '41155-000': 'BadDebt',
    '43010-000': 'OIMisc', '43018-600': 'OIMisc', '43020-000': 'OIMisc',
    '43055-000': 'RevShare', '43060-000': 'OIMisc', '43080-000': 'OIMisc',
    '43090-000': 'OIMisc', '43097-000': 'OIMisc', '43105-000': 'Parking',
    '43125-000': 'OIMisc', '43135-000': 'OIMisc', '43145-000': 'OIMisc',
    '43160-000': 'OIMisc', '43170-000': 'OIMisc', '43180-000': 'OIMisc',
    '43190-000': 'Parking', '43200-000': 'OIMisc', '43201-000': 'OIMisc',
    '43215-000': 'OIMisc', '43225-000': 'RevShare', '43235-000': 'OIMisc',
    '43258-000': 'RUBS', '43259-000': 'RUBS', '43260-000': 'RUBS',
    '43261-000': 'RUBS', '43262-000': 'RUBS', '43263-000': 'RUBS',
    '43264-001': 'RUBS', '43264-010': 'RUBS', '43277-000': 'RUBS',
    '43290-000': 'OIMisc',
    # expenses
    '51010-000': 'Payroll', '51015-000': 'Payroll', '51020-000': 'Payroll',
    '51030-000': 'Payroll', '51030-001': 'Payroll', '51040-000': 'Payroll',
    '51070-000': 'Payroll', '51090-000': 'Payroll', '51100-000': 'Payroll',
    '51110-000': 'Payroll', '51120-000': 'Payroll',
    '52020-000': 'RM', '52057-000': 'RM', '52063-000': 'RM', '52070-000': 'RM',
    '52100-000': 'RM', '52112-000': 'RM', '52125-000': 'RM', '52130-000': 'RM',
    '52140-000': 'RM', '52150-000': 'RM', '52190-000': 'RM', '52195-000': 'RM',
    '52230-000': 'RM', '52231-600': 'RM', '52240-000': 'RM', '52260-000': 'RM',
    '52620-000': 'Turnover', '52650-000': 'Turnover', '52700-000': 'Turnover',
    '52830-000': 'Turnover', '52860-000': 'Turnover', '52880-000': 'Turnover',
    '53060-000': 'Contracts', '53070-000': 'Contracts', '53085-000': 'Contracts',
    '53090-000': 'Contracts', '53105-000': 'Contracts', '53130-000': 'Contracts',
    '53140-000': 'Contracts', '53161-000': 'Contracts', '53180-000': 'Contracts',
    '53182-000': 'Contracts', '53230-000': 'Contracts',
    '54007-000': 'Advertising', '54010-000': 'Advertising', '54012-000': 'Advertising',
    '54025-000': 'Advertising', '54035-000': 'Advertising', '54038-000': 'Advertising',
    '54040-000': 'Advertising', '54046-000': 'Advertising', '54055-000': 'Advertising',
    '54090-000': 'Advertising', '54105-000': 'Advertising', '54110-000': 'Advertising',
    '54122-000': 'Advertising',
    '58025-000': 'GA', '58026-000': 'GA', '58028-000': 'GA', '58070-600': 'GA',
    '58080-000': 'GA', '58090-000': 'GA', '58100-000': 'GA', '58107-000': 'GA',
    '58110-000': 'GA', '58115-000': 'GA',
    '58205-000': 'GA', '58210-000': 'GA', '58225-000': 'GA', '58240-000': 'GA',
    '58247-000': 'GA', '58250-000': 'GA', '58253-000': 'GA', '58260-000': 'GA',
    '58268-600': 'GA', '58275-000': 'GA', '58278-000': 'GA', '58280-000': 'GA',
    '58281-000': 'GA', '58284-000': 'GA', '58290-000': 'GA', '58305-000': 'GA',
    '59020-000': 'Utilities', '59040-000': 'Utilities', '59070-000': 'Utilities',
    '59080-000': 'Utilities', '59100-000': 'Utilities', '59110-000': 'Utilities',
    '61030-000': 'MgmtFee',
    '62010-000': 'RETaxes',
    '63010-000': 'Insurance',
}
EXCLUDED_NOTE = {'41028-000': 'takeover/prorated (Dec-25 close item)',
                 '71010-000': 'below-NOI replacement', '71115-000': 'below-NOI replacement'}

# --------------------------------------------------------- read T12 leaf lines
swb = openpyxl.load_workbook(SRC_T12, read_only=True, data_only=True)
sws = swb['Report1']
detail = []  # (code, name, category, [jan..jul])
for row in sws.iter_rows(min_row=6, max_row=231, max_col=15, values_only=True):
    code, name = row[0], row[1]
    if not code or not isinstance(name, str):
        continue
    code = str(code).strip()
    if code in EXCLUDED_NOTE:
        continue
    months = [v if isinstance(v, (int, float)) else 0 for v in row[7:14]]  # H..N = Jan..Jul 26
    if code in CATMAP:
        if any(abs(m) > 1e-9 for m in months):
            detail.append((code, name.strip(), CATMAP[code], months))
    else:
        # safety: any unmapped non-subtotal leaf with activity?
        nm = name.strip()
        if (not nm.startswith('Total') and not nm.startswith('TOTAL')
                and not code.endswith(('-098', '-099', '-199', '-999', '-090'))
                and any(abs(m) > 1e-9 for m in months)
                and code[:2] not in ('80', '81', '82', '83', '84', '89', '11', '12',
                                     '13', '14', '17', '21', '22', '23', '32', '33', '70', '71', '72')):
            raise SystemExit(f'UNMAPPED ACTIVE LINE: {code} {nm} {months}')
swb.close()

# ------------------------------------------------------------------- constants
SEASONS_UNITS, PRELUDE_UNITS = 360, 280
# Seasons v3 model, Cash Flow (Annual) col K (Y1 = year ending Nov-2027)
SEA = dict(GPR=8272800, VA=0, LTL=-328053.73, Vacancy=-436961.04, BadDebt=-19861.87,
           ModelEmp=-22068.74, Concessions=-79447.46,
           OIMisc=224537.90, RUBS=251187.88, Parking=129687.00, RevShare=387828.00,
           Payroll=601526.12, Advertising=132090.08, GA=125689.44, Turnover=63000.00,
           RM=63000.00, Contracts=228394.37, Utilities=273451.38, MgmtFee=209491.20,
           Insurance=189000.00, RETaxes=484127.45)
# Prelude Final Model, Revenue & Expense col H (Y1 = calendar 2026)
PRE = dict(GPR=5811592.22, VA=4050.00, LTL=-57442.94, Vacancy=-403073.95, BadDebt=-28791.00,
           ModelEmp=-24906.82, Concessions=-143954.98,
           OIMisc=257771.59, RUBS=213628.03, Parking=212637.41, RevShare=0.00,
           Payroll=503138.38, Advertising=97199.92, GA=111629.33, Turnover=63732.61,
           RM=43979.37, Contracts=200393.58, Utilities=154640.80, MgmtFee=146037.74,
           Insurance=173600.00, RETaxes=333465.53)

# ------------------------------------------------------------------ formatting
F_TITLE = Font(name='Arial', size=13, bold=True, color='FFFFFF')
F_SUB = Font(name='Arial', size=9, italic=True, color='555555')
F_HDR = Font(name='Arial', size=9, bold=True, color='FFFFFF')
F_SEC = Font(name='Arial', size=10, bold=True)
F_LBL = Font(name='Arial', size=10)
F_LBLB = Font(name='Arial', size=10, bold=True)
F_IN = Font(name='Arial', size=10, color='0000FF')          # hardcoded input
F_FM = Font(name='Arial', size=10)                          # formula
F_FMB = Font(name='Arial', size=10, bold=True)
F_LNK = Font(name='Arial', size=10, color='008000')         # cross-sheet link
F_LNKB = Font(name='Arial', size=10, bold=True, color='008000')
F_NOTE = Font(name='Arial', size=8.5, color='555555')
FILL_TITLE = PatternFill('solid', fgColor='1F3864')
FILL_HDR = PatternFill('solid', fgColor='2F5496')
FILL_SEC = PatternFill('solid', fgColor='D9E2F3')
FILL_TOT = PatternFill('solid', fgColor='EDF1F9')
FILL_NOI = PatternFill('solid', fgColor='C6E0B4')
THIN = Side(style='thin', color='BFBFBF')
B_TOP = Border(top=THIN)

NUM = '#,##0;(#,##0)'
MON = '$#,##0;($#,##0)'
PCT = '0.0%;(0.0%)'
PU = '#,##0;(#,##0)'

wb = openpyxl.Workbook()

# =============================================================== Detail sheet
wd = wb.create_sheet('Prelude Actuals Detail')
wd['B1'] = 'Prelude at Paramount — Post-Close Actuals Detail (TMG ownership: Jan–Jul 2026)'
wd['B1'].font = Font(name='Arial', size=12, bold=True)
wd['B2'] = ('Source: Yardi 12-month accrual statement (idprepar), period Aug 2025–Jul 2026. Aug–Nov 2025 columns are zero '
            '(pre-acquisition); Dec 2025 contains takeover/proration entries only and is excluded. Category = TMG standardized bucket. '
            'Blue = statement values; black = formulas.')
wd['B2'].font = F_SUB
hdr = ['Acct', 'Line Item', 'Category', 'Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26', 'Jun-26', 'Jul-26',
       '7-Mo Total', 'Annualized (x12/7)', 'T3 Ann. (May-Jul x4)']
for j, h in enumerate(hdr, start=2):
    c = wd.cell(row=4, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(horizontal='center', wrap_text=True)
r = 5
for code, name, cat, months in detail:
    wd.cell(row=r, column=2, value=code).font = F_IN
    wd.cell(row=r, column=3, value=name).font = F_LBL
    wd.cell(row=r, column=4, value=cat).font = F_IN
    for k, m in enumerate(months):
        c = wd.cell(row=r, column=5 + k, value=round(m, 2)); c.font = F_IN; c.number_format = NUM
    c = wd.cell(row=r, column=12, value=f'=SUM(E{r}:K{r})'); c.font = F_FM; c.number_format = NUM
    c = wd.cell(row=r, column=13, value=f'=L{r}*12/7'); c.font = F_FM; c.number_format = NUM
    c = wd.cell(row=r, column=14, value=f'=SUM(I{r}:K{r})*4'); c.font = F_FM; c.number_format = NUM
    r += 1
DLAST = r - 1
wd.cell(row=r, column=3, value='TOTAL (NOI basis: all mapped lines)').font = F_LBLB
for col in (12, 13, 14):
    c = wd.cell(row=r, column=col, value=f'=SUM({get_column_letter(col)}5:{get_column_letter(col)}{DLAST})')
    c.font = F_FMB; c.number_format = NUM; c.border = B_TOP
wd.column_dimensions['B'].width = 11
wd.column_dimensions['C'].width = 38
wd.column_dimensions['D'].width = 12
for col in 'EFGHIJK':
    wd.column_dimensions[col].width = 10.5
for col in ('L', 'M', 'N'):
    wd.column_dimensions[col].width = 13
wd.freeze_panes = 'E5'

DET = "'Prelude Actuals Detail'"
def act(cat, col='M'):   # annualized by default; col='N' for T3
    return f"SUMIF({DET}!$D$5:$D${DLAST},\"{cat}\",{DET}!${col}$5:${col}${DLAST})"

# ============================================================ Comparison sheet
ws = wb.active
ws.title = 'Comparison'
ws.sheet_view.showGridLines = False

ws.merge_cells('B1:M1')
c = ws['B1']; c.value = 'SEASONS AT MERIDIAN Y1 UW  vs  PRELUDE AT PARAMOUNT Y1 UW  vs  PRELUDE ACTUALS'
c.font = F_TITLE; c.fill = FILL_TITLE; c.alignment = Alignment(horizontal='center', vertical='center')
for col in range(2, 14):
    ws.cell(row=1, column=col).fill = FILL_TITLE
ws.row_dimensions[1].height = 22
ws.merge_cells('B2:M2')
c = ws['B2']
c.value = ('Blue = hard-coded from source (Seasons v3 model CF(Annual) col K · Prelude Final Model Rev&Exp col H · Yardi accrual statement) · '
           'Black = formula · Green = link to Detail tab. "Actual" = 7 true post-close months (Jan–Jul 2026) annualized ×12/7; '
           'T3 = May–Jul 2026 ×4. Prepared 2026-08-14.')
c.font = F_SUB; c.alignment = Alignment(horizontal='center')

# column headers
ws['B4'] = ''
heads = [('C', 'Seasons at Meridian\nY1 UW ($/U/yr)'), ('D', 'Prelude\nY1 UW ($/U/yr)'),
         ('E', 'Prelude Actual\n7-mo ann. ($/U/yr)'), ('F', 'Prelude Actual\nT3 ann. ($/U/yr)'),
         ('G', 'Prelude\nAct vs UW ($/U)'), ('H', 'Prelude\nAct vs UW (%)'),
         ('I', 'Seasons UW vs\nPrelude Act ($/U)'),
         ('J', 'Seasons Y1 UW\nTotal ($)'), ('K', 'Prelude Y1 UW\nTotal ($)'), ('L', 'Prelude Actual\nAnn. Total ($)'),
         ('M', 'Notes')]
for col, h in heads:
    c = ws[f'{col}4']; c.value = h; c.font = F_HDR; c.fill = FILL_HDR
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws.row_dimensions[4].height = 42

widths = dict(A=2, B=34, C=13, D=13, E=13, F=13, G=12, H=11, I=13, J=13, K=13, L=13, M=52)
for col, w in widths.items():
    ws.column_dimensions[col].width = w

row = 5
def sec(label):
    global row
    ws.cell(row=row, column=2, value=label).font = F_SEC
    for col in range(2, 14):
        ws.cell(row=row, column=col).fill = FILL_SEC
    row += 1

def put(label, sea_val=None, pre_val=None, cat=None, note='', bold=False, fill=None,
        formula=None, fmt=NUM, pufmt=PU, sign=1):
    """One P&L row. sea_val/pre_val = annual totals (hardcode); cat = detail category for actuals;
       formula = dict of column->formula overriding defaults (totals J,K,L)."""
    global row
    r = row
    lf = F_LBLB if bold else F_LBL
    ws.cell(row=r, column=2, value=label).font = lf
    # totals
    if formula and 'J' in formula:
        c = ws.cell(row=r, column=10, value=formula['J']); c.font = F_FMB if bold else F_FM
    elif sea_val is not None:
        c = ws.cell(row=r, column=10, value=round(sea_val, 2)); c.font = F_IN
    if formula and 'K' in formula:
        c = ws.cell(row=r, column=11, value=formula['K']); c.font = F_FMB if bold else F_FM
    elif pre_val is not None:
        c = ws.cell(row=r, column=11, value=round(pre_val, 2)); c.font = F_IN
    if formula and 'L' in formula:
        c = ws.cell(row=r, column=12, value=formula['L']); c.font = F_FMB if bold else F_FM
    elif cat:
        c = ws.cell(row=r, column=12, value=f'={"-" if sign<0 else ""}{act(cat)}')
        c.font = F_LNKB if bold else F_LNK
    # per-unit + T3
    if ws.cell(row=r, column=10).value is not None:
        ws.cell(row=r, column=3, value=f'=J{r}/$C${UNITS_ROW}').font = F_FMB if bold else F_FM
    if ws.cell(row=r, column=11).value is not None:
        ws.cell(row=r, column=4, value=f'=K{r}/$D${UNITS_ROW}').font = F_FMB if bold else F_FM
    if ws.cell(row=r, column=12).value is not None:
        ws.cell(row=r, column=5, value=f'=L{r}/$E${UNITS_ROW}').font = F_FMB if bold else F_FM
        if cat:
            c = ws.cell(row=r, column=6, value=f'={"-" if sign<0 else ""}{act(cat, "N")}/$E${UNITS_ROW}')
            c.font = F_LNKB if bold else F_LNK
        elif formula and 'F' in formula:
            ws.cell(row=r, column=6, value=formula['F']).font = F_FMB if bold else F_FM
        # variances
        if ws.cell(row=r, column=11).value is not None:
            ws.cell(row=r, column=7, value=f'=E{r}-D{r}').font = F_FMB if bold else F_FM
            ws.cell(row=r, column=8, value=f'=IF(D{r}=0,"n/a",(E{r}-D{r})/ABS(D{r}))').font = F_FMB if bold else F_FM
        if ws.cell(row=r, column=10).value is not None:
            ws.cell(row=r, column=9, value=f'=C{r}-E{r}').font = F_FMB if bold else F_FM
    if formula:
        for colL, f in formula.items():
            if colL in 'CDEFGHI' and ws.cell(row=r, column='ABCDEFGHI'.index(colL) + 1).value is None:
                ws.cell(row=r, column='ABCDEFGHI'.index(colL) + 1, value=f).font = F_FMB if bold else F_FM
    for colL in 'CDEFGI':
        ws.cell(row=r, column='ABCDEFGHI'.index(colL) + 1).number_format = pufmt
    ws.cell(row=r, column=8).number_format = PCT
    for colidx in (10, 11, 12):
        ws.cell(row=r, column=colidx).number_format = fmt
    if note:
        c = ws.cell(row=r, column=13, value=note); c.font = F_NOTE
        c.alignment = Alignment(wrap_text=True, vertical='top')
    if fill:
        for col in range(2, 14):
            ws.cell(row=r, column=col).fill = fill
    if bold:
        for col in range(2, 13):
            ws.cell(row=r, column=col).border = B_TOP
    row += 1
    return r

# ------------------------------------------------------------------- snapshot
sec('PROPERTY SNAPSHOT')
def snap(label, sea, pre, act_v=None, fmt='General', note=''):
    global row
    r = row
    ws.cell(row=r, column=2, value=label).font = F_LBL
    for col, v in ((3, sea), (4, pre), (5, act_v)):
        if v is not None:
            c = ws.cell(row=r, column=col, value=v); c.font = F_IN if not (isinstance(v, str) and v.startswith('=')) else F_FM
            c.number_format = fmt
    if note:
        c = ws.cell(row=r, column=13, value=note); c.font = F_NOTE; c.alignment = Alignment(wrap_text=True, vertical='top')
    row += 1
    return r

r_hdr = row
ws.cell(row=row, column=2, value='').font = F_LBL
for col, v in ((3, 'Seasons at Meridian'), (4, 'Prelude UW'), (5, 'Prelude Actual')):
    c = ws.cell(row=row, column=col, value=v); c.font = F_LBLB; c.alignment = Alignment(horizontal='center')
row += 1
R_UNITS = snap('Units', SEASONS_UNITS, PRELUDE_UNITS, PRELUDE_UNITS, '#,##0')
UNITS_ROW = R_UNITS  # referenced by put() per-unit formulas
snap('Average unit SF', 932.46, 1016.38, 1016.38, '#,##0', 'Seasons: model unit mix wtd avg. Prelude: Rev&Exp tab.')
snap('Year built', 2024, 2018, 2018, '0')
snap('Location', 'Meridian (Overland Rd)', 'Meridian (Paramount)', None)
snap('Status / period', 'UW Y1 (Dec-26 – Nov-27)', 'UW Y1 (CY 2026)', 'Owned; Jan–Jul-26 ann.',
     note='Seasons: acquisition target, close 10/31/26, $118.5M ($329K/U). Prelude: closed 12/31/25, $79.75M ($285K/U).')
R_PRICE = snap('Basis: purchase price ($)', 118500000, 79750000, 79750000, MON)
snap('Price per unit ($)', f'=C{R_PRICE}/C{R_UNITS}', f'=D{R_PRICE}/D{R_UNITS}', f'=E{R_PRICE}/E{R_UNITS}', MON)
R_MRENT = snap('Market rent ($/U/mo)', 1915.00, 1729.64, 1723.50, '$#,##0',
               'Seasons = Y1 UW avg (CF K4). Prelude UW = Y1 avg. Actual = PM market rent, held flat $1,723.50 since close (RR 8/13/26).')
snap('Market rent ($/SF/mo)', f'=C{R_MRENT}/C{R_UNITS+1}', f'=D{R_MRENT}/D{R_UNITS+1}', f'=E{R_MRENT}/E{R_UNITS+1}', '$0.00')
snap('In-place rent ($/U/mo, occupied)', None, 1668.00, 1680.44, '$#,##0',
     'Prelude UW Y1 rent/occupied unit; Actual = RR 8/13/26 (271 of 280 units paying = 96.8%). L5 new leases (May–Aug 26, n=56): $1,731 face; latest L5 $1,811.')

# ---------------------------------------------------------------------- P&L
sec('REVENUE ($/yr)')
r_gpr = put('Market Rent (GPR)', SEA['GPR'], PRE['GPR'], 'GPR',
            'Prelude PM market-rent line flat at $1,723.50/U all 7 months — no pushes taken yet in Yardi.')
r_va = put('Value-Add Revenue', SEA['VA'], PRE['VA'], None,
           formula={'L': 0, 'F': 0}, note='No VA program in either UW (Prelude token $4K).')
r_ltl = put('Gain / (Loss) to Lease', SEA['LTL'], PRE['LTL'], 'LTL',
            'Prelude actual LTL running ~2.8x UW but shrinking monthly (-3.2% of GPR Jan → -2.3% Jul).')
r_agpr = put('Adjusted GPR', bold=True,
             formula={'J': f'=SUM(J{r_gpr}:J{r_ltl})', 'K': f'=SUM(K{r_gpr}:K{r_ltl})',
                      'L': f'=SUM(L{r_gpr}:L{r_ltl})', 'F': f'=SUM(F{r_gpr}:F{r_ltl})'})
r_vac = put('Vacancy', SEA['Vacancy'], PRE['Vacancy'], 'Vacancy',
            'Prelude vacancy burned from ~11% econ (Jan–Apr) to 6.1% T3 — absorption thesis tracking.')
r_bd = put('Bad Debt / Uncollectables', SEA['BadDebt'], PRE['BadDebt'], 'BadDebt',
           'Prelude actual net recovery (+$1.1K) — far better than 0.5% UW allowance.')
r_mod = put('Model / Employee Units', SEA['ModelEmp'], PRE['ModelEmp'], 'ModelEmp')
r_conc = put('Concessions', SEA['Concessions'], PRE['Concessions'], 'Concessions',
             'RED FLAG: Prelude actual ~1.7x UW and accelerating — T3 pace ~$1,154/U (5.6% of GPR) vs $514/U UW. '
             'One-time (upfront) concessions on new signings; winter-cohort burn-off underway. Seasons UW assumes only 1.0% of AGPR in Y1.')
r_nri = put('Net Rental Income', bold=True,
            formula={'J': f'=J{r_agpr}+SUM(J{r_vac}:J{r_conc})', 'K': f'=K{r_agpr}+SUM(K{r_vac}:K{r_conc})',
                     'L': f'=L{r_agpr}+SUM(L{r_vac}:L{r_conc})', 'F': f'=F{r_agpr}+SUM(F{r_vac}:F{r_conc})'})
r_oi = put('Other Income (misc & fees)', SEA['OIMisc'], PRE['OIMisc'], 'OIMisc',
           'Prelude actual incl. smart-home $250/U ann. UW also carried bulk-wifi at $100.8K income offset by $100.8K expense (net $0) — excluded both sides here.')
r_rubs = put('RUBS / Utility Billbacks', SEA['RUBS'], PRE['RUBS'], 'RUBS',
             'Prelude billbacks ramped from ~$0 (Jan) as TMG RUBS program took over billing.')
r_park = put('Parking, Garages & Carports', SEA['Parking'], PRE['Parking'], 'Parking',
             'Prelude UW pushed detached garages $75→$100/mo; actual garage income $609/U ann. vs $759/U UW.')
r_rev = put('Revenue Share (internet/cable)', SEA['RevShare'], PRE['RevShare'], 'RevShare',
            'KEY DELTA: Seasons UW carries $1,077/U bulk-internet revenue share — supported by in-place contract ($834/U in Seasons T12). Prelude has no program (actual $15/U).')
r_toi = put('Total Other Income', bold=True,
            formula={'J': f'=SUM(J{r_oi}:J{r_rev})', 'K': f'=SUM(K{r_oi}:K{r_rev})',
                     'L': f'=SUM(L{r_oi}:L{r_rev})', 'F': f'=SUM(F{r_oi}:F{r_rev})'})
r_egi = put('EFFECTIVE GROSS INCOME', bold=True, fill=FILL_TOT,
            formula={'J': f'=J{r_nri}+J{r_toi}', 'K': f'=K{r_nri}+K{r_toi}',
                     'L': f'=L{r_nri}+L{r_toi}', 'F': f'=F{r_nri}+F{r_toi}'})

sec('OPERATING EXPENSES ($/yr)')
r_pay = put('Payroll & Benefits', SEA['Payroll'], PRE['Payroll'], 'Payroll',
            'Prelude running ~$300/U favorable to UW.')
r_adv = put('Advertising & Promotion', SEA['Advertising'], PRE['Advertising'], 'Advertising',
            'Prelude T3 elevated (~$481/U ann.) — leasing push.')
r_ga = put('General & Administrative', SEA['GA'], PRE['GA'], 'GA')
r_turn = put('Turnover (make-ready & amenities)', SEA['Turnover'], PRE['Turnover'], 'Turnover',
             'Actual favorable; 2018 vintage still young.')
r_rm = put('Repairs & Maintenance', SEA['RM'], PRE['RM'], 'RM')
r_cont = put('Contracts', SEA['Contracts'], PRE['Contracts'], 'Contracts')
r_util = put('Utilities', SEA['Utilities'], PRE['Utilities'], 'Utilities',
             'Seasons UW $760/U vs Prelude $553-600/U — Seasons is a larger-common-area 2024 asset.')
r_mgmt = put('Management Fee', SEA['MgmtFee'], PRE['MgmtFee'], 'MgmtFee',
             'Both ~2.5% of EGI underwritten; Prelude actual ~2.4%.')
r_ctrl = put('Total Controllable', bold=True,
             formula={'J': f'=SUM(J{r_pay}:J{r_mgmt})', 'K': f'=SUM(K{r_pay}:K{r_mgmt})',
                      'L': f'=SUM(L{r_pay}:L{r_mgmt})', 'F': f'=SUM(F{r_pay}:F{r_mgmt})'})
r_ins = put('Insurance', SEA['Insurance'], PRE['Insurance'], 'Insurance',
            'Prelude actual ~$551/U ann. vs $620/U UW — favorable; premium stepped down in Apr-26.')
r_tax = put('Real Estate Taxes', SEA['RETaxes'], PRE['RETaxes'], 'RETaxes',
            'Prelude accruing exactly at the UW 2026 bill ($333.5K) — 95% reassessment step confirmed. Seasons UW = full reassessment on $118.5M.')
r_nc = put('Total Non-Controllable', bold=True,
           formula={'J': f'=J{r_ins}+J{r_tax}', 'K': f'=K{r_ins}+K{r_tax}',
                    'L': f'=L{r_ins}+L{r_tax}', 'F': f'=F{r_ins}+F{r_tax}'})
r_exp = put('TOTAL EXPENSES', bold=True, fill=FILL_TOT,
            formula={'J': f'=J{r_ctrl}+J{r_nc}', 'K': f'=K{r_ctrl}+K{r_nc}',
                     'L': f'=L{r_ctrl}+L{r_nc}', 'F': f'=F{r_ctrl}+F{r_nc}'})
r_noi = put('NET OPERATING INCOME', bold=True, fill=FILL_NOI,
            formula={'J': f'=J{r_egi}-J{r_exp}', 'K': f'=K{r_egi}-K{r_exp}',
                     'L': f'=L{r_egi}-L{r_exp}', 'F': f'=F{r_egi}-F{r_exp}'},
            note='Prelude actual ~3.9% behind UW Y1 pace, converging: gaps are concessions (~$640/U drag) and unimplemented bulk internet; opex ~$500/U favorable.')

sec('RATIOS & MEMO')
r = row
ws.cell(row=r, column=2, value='Economic occupancy (net rental / adj. GPR)').font = F_LBL
for colL in 'CDEF':
    c = ws.cell(row=r, column='ABCDEF'.index(colL) + 1,
                value=f'={colL}{r_nri}/{colL}{r_agpr}')
    c.font = F_FM; c.number_format = PCT
ws.cell(row=r, column=13, value='Prelude improving intra-2026; RR 8/13/26 physical: 271/280 paying (96.8%).').font = F_NOTE
ws.cell(row=r, column=13).alignment = Alignment(wrap_text=True, vertical='top')
row += 1
r = row
ws.cell(row=r, column=2, value='Expense ratio (% of EGI)').font = F_LBL
for colL in 'CDEF':
    c = ws.cell(row=r, column='ABCDEF'.index(colL) + 1, value=f'={colL}{r_exp}/{colL}{r_egi}')
    c.font = F_FM; c.number_format = PCT
row += 1
r = row
ws.cell(row=r, column=2, value='NOI margin').font = F_LBL
for colL in 'CDEF':
    c = ws.cell(row=r, column='ABCDEF'.index(colL) + 1, value=f'={colL}{r_noi}/{colL}{r_egi}')
    c.font = F_FM; c.number_format = PCT
row += 1
r_res = row
ws.cell(row=r_res, column=2, value='Capital reserves ($/U/yr)').font = F_LBL
for colL, v in (('C', 250), ('D', 250)):
    c = ws.cell(row=r_res, column='ABCD'.index(colL) + 1, value=v); c.font = F_IN; c.number_format = PU
ws.cell(row=r_res, column=13, value='Both UWs reserve $250/U/yr below NOI.').font = F_NOTE
row += 1
r_capn = row
ws.cell(row=r_capn, column=2, value='NOI after reserves ($)').font = F_LBL
ws.cell(row=r_capn, column=10, value=f'=J{r_noi}-C{r_res}*C{R_UNITS}').font = F_FM
ws.cell(row=r_capn, column=11, value=f'=K{r_noi}-D{r_res}*D{R_UNITS}').font = F_FM
for colidx in (10, 11):
    ws.cell(row=r_capn, column=colidx).number_format = NUM
row += 1
r_cap = row
ws.cell(row=r_cap, column=2, value='Cap rate on basis (NOI after reserves)').font = F_LBL
ws.cell(row=r_cap, column=3, value=f'=J{r_capn}/C{R_PRICE}').font = F_FM
ws.cell(row=r_cap, column=4, value=f'=K{r_capn}/D{R_PRICE}').font = F_FM
ws.cell(row=r_cap, column=5, value=f'=(L{r_noi}-250*E{R_UNITS})/E{R_PRICE}').font = F_FM
for colL in 'CDE':
    ws.cell(row=r_cap, column='ABCDE'.index(colL) + 1).number_format = '0.00%'
ws.cell(row=r_cap, column=13,
        value='Seasons Y1 cap 5.00% at $118.5M. Prelude UW 4.94% at $79.75M; actual pace 4.73% (reserves deducted at $250/U).').font = F_NOTE
ws.cell(row=r_cap, column=13).alignment = Alignment(wrap_text=True, vertical='top')
row += 2

# verdict block
ws.merge_cells(f'B{row}:M{row+3}')
c = ws.cell(row=row, column=2)
c.value = ('READ: Prelude — the first live test of the Meridian recovery thesis — is ~4% behind its UW Y1 NOI pace but converging: vacancy burned 11%→6% economic in six months, '
           'new leases sign at the UW market rent to the dollar, in-place rent is ahead of UW, and opex runs ~$500/U favorable. The two identified gaps are concessions '
           '(~2x UW, still 5-6% on new leases at 2018-vintage product in mid-2026) and the unimplemented bulk-internet program. For Seasons this supports the occupancy-recovery '
           'and rent-level assumptions, prices the achievable opex, and flags the two UW lines to pressure-test: Y1 concessions (Seasons assumes burn-off to ~1% of AGPR) and the '
           '$1,077/U revenue-share line (Seasons has an in-place contract; Prelude shows what happens when the program is not implemented).')
c.font = Font(name='Arial', size=9, italic=True)
c.alignment = Alignment(wrap_text=True, vertical='top')
row += 5

ws.freeze_panes = 'C5'

# ================================================================ Sources tab
wsrc = wb.create_sheet('Sources & Method')
wsrc.column_dimensions['B'].width = 120
lines = [
    ('Sources & Method', True),
    ('', False),
    ('SEASONS AT MERIDIAN Y1 UW — TMG_Acquisitions_model_7.26___Seasons_at_Meridian_v3.xlsm, Cash Flow (Annual) column K (Year 1 = Dec-2026–Nov-2027, 8/14/26 model refresh: Y1 market-rent basis $1,915/U/mo). '
     'NOI before $250/U capital reserves. Purchase price $118.5M per Assumptions H5.', False),
    ('PRELUDE AT PARAMOUNT Y1 UW — Prelude_at_Paramount_Final_Model.xlsm (Dec-2025 acquisition model), Revenue & Expense tab column H (Y1 = CY 2026). '
     'Bulk-wifi program was modeled at $100,800 income offset by $100,800 expense (net $0 Y1, I&E AA35:AD37); both sides excluded here. '
     'The knowledge-base exhibit (Boise_Deals_Normalized_Underwriting_v2, tab 2b) shows OI at $2,803/U because it moves that gross-up into Other Income — NOI is identical.', False),
    ('PRELUDE ACTUALS — Yardi 12-month accrual statement (idprepar), Aug-2025–Jul-2026, tree ysi_cf. TMG closed 12/31/2025: Aug–Nov-25 columns are zero and Dec-25 contains only takeover/proration '
     'entries (excluded: takeover rents $41.5K, damages $17.2K, tax/insurance stubs). "Actual" = Jan–Jul-2026 (7 months) x 12/7; "T3" = May–Jul-2026 x 4. '
     'Below-NOI routine-replacement lines (-$84 net) excluded. Rent roll w/ lease charges as of 8/13/2026 for occupancy and in-place rent.', False),
    ('', False),
    ('CATEGORY MAPPING (statement → TMG buckets) — see Prelude Actuals Detail tab, column D. Notable choices: smart-home income → Other Income; cable TV commissions + satellite/internet → Revenue Share; '
     'utility set-up/admin fees → RUBS; make-ready + recreational-amenities → Turnover; smart-home WiFi expense stays in G&A; storage rent → Other Income (misc).', False),
    ('ANNUALIZATION CAVEATS — (1) Concessions are one-time credits taken at signing: the 7-mo annualization embeds the heavy winter cohort; T3 shows the current (worse) pace. '
     '(2) RUBS billbacks ramped from ~$0 in January as TMG took over billing — 7-mo annualized understates the run rate; T3 is the better read. '
     '(3) Taxes and insurance accrue at level monthly amounts — annualization is exact.', False),
    ('COMPARABILITY — Assets differ: Seasons is 2024-built, 360 units, 932 SF avg, in lease-up stabilization; Prelude is 2018-built, 280 units, 1,016 SF avg, stabilized-recovering. '
     'Both Meridian (Ada County, ~0.45% levy). Compare $/unit and ratios, not totals. Cap rates are comparable; $/unit price is not (larger avg SF at Prelude).', False),
    ('', False),
    ('Related repo exhibits: knowledge/exhibits/Boise_Deals_Normalized_Underwriting_v2.xlsx (tabs 2_ProFormas, 2b_Prelude_Actuals), knowledge/deal_metrics.json (branch seasons-meridian-underwriting-woep67). '
     'Prepared 2026-08-14 from user-supplied source files.', False),
]
r = 2
for txt, bold in lines:
    c = wsrc.cell(row=r, column=2, value=txt)
    c.font = Font(name='Arial', size=11 if bold else 9.5, bold=bold)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    if txt and not bold:
        wsrc.row_dimensions[r].height = max(28, 14 * (len(txt) // 115 + 1))
    r += 1

wb.save(OUT)
print('saved', OUT, '| detail rows:', DLAST - 4)
