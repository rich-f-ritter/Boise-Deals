#!/usr/bin/env python3
"""Boise Deals — Normalized Underwriting Workbook builder."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ---------- styles ----------
F = lambda **k: Font(name="Arial", **{"size":10, **k})
TITLE   = F(bold=True, size=14)
H1      = F(bold=True, size=11, color='FFFFFF')
H2      = F(bold=True, size=10)
BLUE    = F(color='0000FF')            # hardcoded inputs / source-extracted
BLACK   = F()
GREEN   = F(color='008000')            # cross-sheet link
NOTE    = F(italic=True, size=9, color='808080')
BOLD    = F(bold=True)
HDRFILL = PatternFill('solid', fgColor='1F3864')
SUBFILL = PatternFill('solid', fgColor='D9E2F2')
YELLOW  = PatternFill('solid', fgColor='FFFF00')
GRAYF   = PatternFill('solid', fgColor='F2F2F2')
THIN    = Border(bottom=Side(style='thin', color='BFBFBF'))

M0  = '$#,##0'
M2  = '$#,##0.00'
PC  = '0.00%'
PC1 = '0.0%'
NUM = '#,##0'
BP  = '0'

def sheet(name, widths):
    ws = wb.create_sheet(name)
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws

def put(ws, cell, val, font=BLACK, fmt=None, fill=None, wrap=False, align=None):
    c = ws[cell]; c.value = val; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap or align: c.alignment = Alignment(wrap_text=wrap, horizontal=align, vertical='top' if wrap else None)
    return c

def header(ws, row, cols, texts):
    for col,t in zip(cols, texts):
        c = ws[f'{col}{row}']; c.value=t; c.font=H1; c.fill=HDRFILL
        c.alignment=Alignment(horizontal='center', wrap_text=True)

def sec(ws, cell, text):
    c = ws[cell]; c.value=text; c.font=H2; c.fill=SUBFILL

# ============================================================
# README
# ============================================================
ws = wb.active; ws.title='README'
for i,w in enumerate([3,110],1): ws.column_dimensions[get_column_letter(i)].width=w
ws.sheet_view.showGridLines=False
put(ws,'B2','Boise MSA — Seasons at Meridian: Deal Comparison & Developer Underwriting Normalization', TITLE)
put(ws,'B3','Prepared 2026-08-13 · All model figures re-extracted programmatically from source workbooks and verified (59/59 checks). Companion: knowledge/Seasons-Meridian-Replacement-Cost-and-Supply-Economics.md', NOTE, wrap=True)
rows = [
 ('LEGEND',''),
 ('','Blue font = hardcoded input extracted from a source model (source cited in Notes/Sources).'),
 ('','Black font = formula computed in this workbook.  Green = link to another sheet.'),
 ('','Yellow fill = key normalization assumption — edit these to flex the analysis.'),
 ('TABS',''),
 ('1_Deals','Five-deal side-by-side: pricing, rents, yields, exits, returns.'),
 ('2_ProFormas','Per-unit stabilized pro formas, one chart of accounts, with other-income component detail.'),
 ('3_Emblem_Norm','Emblem Meridian (Quarterra) underwriting normalized: other income, taxes, exit cap.'),
 ('4_Judy_Norm','The Judy / Maple Grove & Overland (Hawkins) normalized: other income, Boise taxes, land basis.'),
 ('5_Pencil','Rent required for new development to pencil, 2026-2032, vs Seasons UW rent path.'),
 ('6_Exit','Seasons exit-cap sensitivity (UIRR/LIRR) + exit anatomy vs Emblem + vintage evidence.'),
 ('7_Taxes','Meridian vs Boise levy normalization and tax-adjusted cap rates.'),
 ('8_Supply','Apartment-ready land, pipeline roster, and demand/supply base case.'),
 ('9_Sources','File-by-file provenance, key cells, and method notes.'),
 ('KEY CONCLUSIONS',''),
 ('1','Emblem true untrended yield-on-cost is ~6.3%, not the marketed 6.65% — other income is ~$0.8K/unit high; the 5.50% exit cap is sandbagged and roughly offsets, so their exit VALUE is about right at a normalized 5.25% cap, but their YIELD claim deflates.'),
 ('2','The Judy true untrended yield is ~6.0-6.15%, not 6.52% — Boise taxes are ~$750-950/unit light and OI ~$570/unit high; on market-priced land the deal is ~5.9%. This deal only pencils because of its 2024 land basis.'),
 ('3','Corrected pencil rents are HIGHER than the developers show: ~$2.24/SF (their product) to ~$2.30/SF (Seasons-like product) at 6.5% ROC today, vs Seasons at $2.02 — the supply moat is wider than the books imply.'),
 ('4','Normalized new-product exit caps of 5.00-5.25% support underwriting the Seasons exit as a 5.00-5.25% band ($400.6K-$382K/unit); the vintage discount lives in NOI (our exit NOI is 8.9% below new-build), not the cap.'),
 ('5','Meridian vs Boise taxes are worth ~$2,100/unit/yr (~$42K/unit at a 5% cap); always tax-normalize before comparing cap rates across the two cities.'),
]
r=5
for a,b in rows:
    put(ws,f'B{r}', a if not b else f'{a}', H2 if b=='' else (BOLD if a and len(a)<14 else BLACK))
    if b:
        put(ws,f'B{r}', f'{a} — {b}' if a and a not in ('','LEGEND','TABS','KEY CONCLUSIONS') else b, BLACK, wrap=True)
        if a in ('1','2','3','4','5'): ws[f'B{r}'].value = f'{a}. {b}'
    r+=1

# ============================================================
# 1_Deals
# ============================================================
ws = sheet('1_Deals',[2,34,17,17,17,17,17,44])
put(ws,'B2','Five-Deal Comparison', TITLE)
header(ws,4,['B','C','D','E','F','G','H'],
       ['Metric','Seasons at Meridian','Prelude at Paramount','Canyon Ridge','Emblem Meridian','The Judy (MGO)','Notes'])
deals_rows = [
 # label, values (5), fmt, formula?, note
 ('Role',['Acquisition target','Owned (12/2025)','Comp — under contract','Development (equity raise)','Development (equity raise)'],None,'Emblem: Quarterra/Lennar. Judy: Hawkins.'),
 ('Location',['2700 E Overland Rd, Meridian','4909 N Elsinore Ave, Meridian','2552 E Gowen Rd, Boise','Eagle/Overland corridor, Meridian','1770 S Maple Grove Rd, Boise'],None,''),
 ('Vintage / delivery',['2024','2018','2024','2028-29','2027-28'],None,''),
 ('Units',[360,280,288,256,162],NUM,''),
 ('Avg unit SF',[932.46,1016.38,888.94,938.98,907.76],NUM,''),
 ('Price / total dev cost ($)',[118000000,79750000,110000000,77959624,41691719],M0,'Seasons = recommended bid (whisper $125M). CR = award price.'),
 ('$/unit',None,M0,'=C9/C7'),
 ('$/SF (NRSF)',None,M0,'=C10/C8'),
 ('Y1 / stabilized NOI ($)',[5904654,3947625,5027967,5036490,2914298],M0,'Prelude = 4.95% x price (model Y1 cap). Emblem = untrended in-place NOI. Judy = Y3.'),
 ('Going-in yield / untrended ROC',[0.0500,0.0495,0.0457,0.0665,0.0652],PC,'TMG deals: Y1 NOI cap. Developers: marketed untrended ROC — see normalization tabs for corrected.'),
 ('Market rent ($/mo)',[1885,1730,2171,2069,1787],M0,'Each model\'s own UW. Seasons also: contract rent $1,751.'),
 ('Rent $/SF',None,M2,'=C13/C8'),
 ('Other income ($/u/yr)',[2736,2803,3002,4207,3568],M0,'See 2_ProFormas for components; developers run high.'),
 ('RE taxes ($/u/yr)',[1340,1169,3428,1501,2203],M0,'Meridian ~0.45% levy vs Boise ~0.92%. Judy understated — see 4_Judy_Norm.'),
 ('Exit date',['Oct-2031','Dec-2030','Oct-2031 (UW)','Jan-2030','Aug-2030'],None,''),
 ('Exit cap (as modeled)',[0.05,0.05,0.0475,0.055,0.0525],PC,'Developer exit caps sandbagged — see normalization tabs.'),
 ('Exit value ($/unit)',[400563,361232,442763,400467,361642],M0,''),
 ('UIRR / project IRR',[0.0865,0.0894,0.0718,0.3059,0.2506],PC,'Developers = levered project IRR (different metric).'),
 ('LIRR / LP IRR',[0.1214,0.1388,0.0886,0.2229,0.2051],PC,''),
]
r=5
for row in deals_rows:
    label, vals, fmt = row[0], row[1], row[2]
    note = row[3] if len(row)>3 and not (isinstance(row[2],str)) else (row[3] if len(row)>3 else '')
    put(ws,f'B{r}',label,BOLD)
    if vals is None:
        # formula row: pattern given in row[3]... handled below explicitly
        pass
    else:
        for i,v in enumerate(vals):
            col = get_column_letter(3+i)
            put(ws,f'{col}{r}', v, BLUE, fmt)
    if len(row)>3 and isinstance(row[3],str) and not row[3].startswith('='):
        put(ws,f'H{r}', row[3], NOTE, wrap=True)
    ws[f'B{r}'].border=THIN
    r+=1
# formula rows: $/unit (r for '$/unit' = 11), $/SF r=12, rent psf r=17... compute positions:
# rows: 5 Role,6 Location,7 Vintage,8 Units,9 AvgSF,10 Price,11 $/unit,12 $/SF,13 NOI,14 yield,15 rent,16 rentpsf,17 OI,18 taxes,19 exitdate,20 exitcap,21 exit/u,22 UIRR,23 LIRR
# Fix: my loop wrote rows sequentially incl the None rows (they still advanced r). Map:
# r5 Role, r6 Loc, r7 Vint, r8 Units, r9 AvgSF, r10 Price, r11 $/unit(None), r12 $/SF(None), r13 NOI, r14 yield, r15 rent, r16 rent$/SF(None), r17 OI, r18 taxes, r19 exit date, r20 exit cap, r21 exit $/u, r22 UIRR, r23 LIRR
for i in range(5):
    col = get_column_letter(3+i)
    put(ws,f'{col}11', f'={col}10/{col}8', BLACK, M0)
    put(ws,f'{col}12', f'={col}10/({col}8*{col}9)', BLACK, M0)
    put(ws,f'{col}16', f'={col}15/{col}9', BLACK, M2)

# ============================================================
# 2_ProFormas (per unit per year)
# ============================================================
ws = sheet('2_ProFormas',[2,34,15,15,15,15,15,46])
put(ws,'B2','Per-Unit Stabilized Pro Formas ($/unit/yr unless noted)', TITLE)
put(ws,'B3','Seasons & Canyon Ridge = TMG Y1. Prelude = our acquisition UW Y1. Emblem = 2031 stabilized (trended $). Judy = Year 3 (first stabilized).', NOTE, wrap=True)
header(ws,5,['B','C','D','E','F','G','H'],['Line','Seasons Y1','Prelude Y1','Canyon Ridge Y1','Emblem stab. 2031','Judy Y3','Notes'])
pf = [
 ('Market rent ($/mo)',[1885,1730,2171,2443,1787],M0,'Emblem = their 2031 trended rent ($2,069 in 6/2026).'),
 ('Rent $/SF ($/mo)',['=C6/932.46','=D6/1016.38','=E6/888.94','=F6/938.98','=G6/907.76'],M2,''),
 ('OTHER INCOME','SEC',None,''),
 ('Misc / fees',[601,1281,1897,721,None],M0,'CR includes damage-waiver program. Prelude incl. bulk data income. Judy not itemized.'),
 ('RUBS / utility billback',[698,763,581,1149,None],M0,'Seasons ~66% recovery (actual). Emblem assumes 100% billback.'),
 ('Parking / garages',[360,759,520,1041,None],M0,'Prelude has rentable garages (actual). Emblem monetizes all 536 spaces @$41/mo blended.'),
 ('Wifi / revenue share',[1077,0,3,1296,None],M0,'Seasons = bulk internet revenue share (actual). Emblem = mandatory $108/mo wifi.'),
 ('Total other income',['=SUM(C9:C12)','=SUM(D9:D12)','=SUM(E9:E12)','=SUM(F9:F12)',3568],M0,'Judy total from Y3 pro forma (components embedded).'),
 ('OPERATING EXPENSES','SEC',None,''),
 ('Payroll / personnel',[1671,None,1749,1804,0],M0,'Judy payroll bundled in 8%-of-EGI management fee.'),
 ('Marketing',[367,None,346,406,371],M0,''),
 ('G&A / admin',[423,None,660,480,None],M0,''),
 ('Turnover / make-ready',[200,None,152,None,254],M0,'Emblem turnover within R&M.'),
 ('R&M',[175,None,173,541,344],M0,''),
 ('Contracts / services',[619,None,996,972,708],M0,'Judy = contract svcs + wifi + valet + smart-home costs.'),
 ('Utilities',[760,None,470,1405,859],M0,''),
 ('Management fee',[576,None,668,946,2015],M0,'Judy 8% of EGI incl. payroll.'),
 ('Insurance',[525,620,625,496,446],M0,''),
 ('Real estate taxes',[1340,1169,3428,1501,2203],M0,'See 7_Taxes. Judy understated (see 4_Judy_Norm).'),
 ('Total opex',[6656,6013,9267,8779,7200],M0,'Prelude = TMG Y1 total (controllables 3,643 + ins + taxes). Emblem incl. $227 reserves.'),
 ('NOI ($/unit)',[16402,14099,17458,22755,17990],M0,'Prelude = 4.95% Y1 cap x $284.8K.'),
 ('NOI check: expense ratio','SEC',None,''),
]
r=6
for label, vals, fmt, note in pf:
    if vals=='SEC':
        sec(ws,f'B{r}',label); r+=1; continue
    put(ws,f'B{r}',label,BOLD if label.startswith(('Total','NOI')) else BLACK)
    if vals:
        for i,v in enumerate(vals):
            col=get_column_letter(3+i)
            if v is None: continue
            if isinstance(v,str) and v.startswith('='):
                put(ws,f'{col}{r}', v, BLACK, fmt)
            else:
                put(ws,f'{col}{r}', v, BLUE, fmt)
    if note: put(ws,f'H{r}', note, NOTE, wrap=True)
    ws[f'B{r}'].border=THIN
    r+=1

# ============================================================
# 3_Emblem_Norm
# ============================================================
ws = sheet('3_Emblem_Norm',[2,46,16,16,16,60])
put(ws,'B2','Emblem Meridian — Underwriting Normalization', TITLE)
put(ws,'B3','Corrects three things: (1) other income marked to market comps, (2) taxes marked to 95% of normalized value at the Meridian levy, (3) exit cap normalized to observed market. Closed-form tax solve: V = NOI-ex-tax / (cap + levy x reassess).', NOTE, wrap=True)

sec(ws,'B5','A. AS MARKETED (source: Emblem merchant model)')
em = [
 ('Total development cost ($)',77959624,M0,'Summary D25 (at Oct-27 GMP)'),
 ('Financing costs in TDC ($)',1982846,M0,'Constr. interest 1,086,262 + financing 896,583'),
 ('ROC denominator ex-financing ($)','=C6-C7',M0,'Their ROC convention'),
 ('Units',256,NUM,''),
 ('Avg NRSF / unit',938.98,NUM,''),
 ('Untrended NOI, in-place 6/2026 ($)',5036490,M0,'Summary D49'),
 ('Marketed untrended ROC','=C11/C8',PC,'Matches book 6.65%'),
 ('Untrended RE taxes embedded ($, est.)',331600,M0,'2031 taxes $384,319 deflated 3%/yr'),
 ('Sale F12 NOI ($, Jan-2030)',5638571,M0,'gross sale x 5.5% cap'),
 ('Marketed exit cap',0.055,PC,''),
 ('Gross sale ($)','=C14/C15',M0,'Book: $102.5M / $400.5K per home'),
 ('OTHER INCOME AS MARKETED ($/u/yr)','SEC',None,''),
 ('Garage / covered parking',1041,M0,'536 spaces x $41.42/mo blended — every space monetized'),
 ('Managed wifi (mandatory $108/mo)',1296,M0,''),
 ('W/S utility billback (100%)',1149,M0,''),
 ('Pet fees',126,M0,''),
 ('Misc other',595,M0,''),
 ('Total OI as marketed ($/u/yr)','=SUM(C18:C22)',M0,''),
]
r=6
for label,val,fmt,note in em:
    if val=='SEC': sec(ws,f'B{r}',label); r+=1; continue
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

sec(ws,'B25','B. NORMALIZATION ASSUMPTIONS (yellow = edit me)')
nb = [
 ('Garage / parking normalized ($/u/yr)',750,'Prelude ACHIEVES $759 with rentable garages; CR $520; Seasons $360. Attached TH garages are typically in base rent, not separately billed.'),
 ('Wifi / connectivity normalized ($/u/yr)',1077,'Seasons actually collects $1,077 revenue share — the proven number.'),
 ('Utility billback normalized ($/u/yr)',850,'Actual recoveries: Seasons $698, Prelude $763. New-build submetering earns a premium — but not 100%.'),
 ('Pet fees (keep)',126,''),
 ('Misc other (keep)',595,''),
 ('Normalized total OI ($/u/yr)','=SUM(C26:C30)','~$3,400 vs $4,207 marketed vs $2.7-3.0K market actuals'),
 ('OI adjustment ($/u/yr)','=C31-C23',''),
 ('OI adjustment ($/yr)','=C32*C9',''),
 ('Meridian levy (actual)',0.0045,'Seasons & Prelude actuals both 0.4507%'),
 ('Assessment ratio at stabilization',0.95,'TMG convention; Idaho non-disclosure'),
 ('Effective levy on value','=C34*C35',''),
 ('Normalized exit cap',0.0525,'CR award 4.57% (5.12% tax-adj); Seasons bid 5.00%; Prelude closed 4.95%. 5.25% adds forward conservatism.'),
 ('Alt exit cap',0.05,''),
]
r=26
for label,val,note in nb:
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK, PC if 'cap' in label or 'levy' in label.lower() or 'ratio' in label else M0)
    else:
        fmt = PC if val<1 else M0
        put(ws,f'C{r}',val,BLUE,fmt, YELLOW if label.split(' (')[0] not in ('Pet fees','Misc other','OI adjustment') and not isinstance(val,str) else None)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
ws['C36'].number_format=PC; ws['C31'].number_format=M0; ws['C32'].number_format=M0; ws['C33'].number_format=M0

sec(ws,'B40','C. NORMALIZED ECONOMICS (formulas)')
put(ws,'B41','Untrended (2026 dollars)',H2)
nc = [
 ('NOI excl. taxes, OI-adjusted ($)','=C11+C13+C33',M0,'add back embedded taxes; apply OI cut (C33 is negative)'),
 ('Stabilized value @ normalized cap ($)','=C42/(C37+C36)',M0,'closed-form tax solve'),
 ('  per unit','=C43/C9',M0,''),
 ('Normalized RE taxes ($)','=C36*C43',M0,''),
 ('  per unit','=C45/C9',M0,''),
 ('NORMALIZED UNTRENDED NOI ($)','=C42-C45',M0,''),
 ('Normalized untrended ROC (ex-financing)','=C47/C8',PC,'vs 6.65% marketed'),
 ('Normalized untrended ROC (all-in cost)','=C47/C6',PC,''),
 ('Development spread vs normalized cap (bp)','=(C48-C37)*10000',BP,'thin vs the 125-175bp institutional norm'),
]
r=42
for label,f,fmt,note in nc:
    put(ws,f'B{r}',label, BOLD if 'NORMALIZED UNTRENDED' in label or 'ROC' in label else BLACK)
    put(ws,f'C{r}',f,BLACK,fmt); put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

put(ws,'B53','Trended sale (Jan-2030)',H2)
nt = [
 ('Escalation on OI adj to sale (3%/yr, 5 yrs)','=C33*1.03^5',M0,''),
 ('Sale NOI excl. taxes, OI-adjusted ($)','=C14+384319+C54',M0,'384,319 = their 2031 taxes added back'),
 ('Normalized sale value @ C37 ($)','=C55/(C37+C36)',M0,''),
 ('  per unit','=C56/C9',M0,'vs $400.5K marketed'),
 ('  @ alt cap C38','=C55/(C38+C36)',M0,''),
 ('  per unit','=C58/C9',M0,''),
 ('Delta vs marketed gross sale ($)','=C56-C16',M0,'sandbagged cap ~ offsets aggressive OI'),
]
r=54
for label,f,fmt,note in nt:
    put(ws,f'B{r}',label); put(ws,f'C{r}',f,BLACK,fmt); put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

put(ws,'B62','Exit value grid ($/unit) by cap on normalized sale NOI',H2)
caps=[0.0475,0.05,0.0525,0.055]
for i,cp in enumerate(caps):
    col=get_column_letter(3+i)
    put(ws,f'{col}63',cp,BLUE,PC)
    put(ws,f'{col}64',f'=$C$55/({col}63+$C$36)/$C$9',BLACK,M0)
put(ws,'B63','Cap',BOLD); put(ws,'B64','Normalized exit $/unit',BOLD)
put(ws,'B66','TAKEAWAY: The two "errors" offset on exit value (5.50% sandbagged cap ~ cancels aggressive OI), so the $400K/home exit is roughly right at an honest 5.25%. What does NOT survive is the yield: true untrended ROC ~6.3% vs 6.65% marketed — and true pencil rents are higher (see 5_Pencil).', BOLD, wrap=True)
ws.merge_cells('B66:F68')

# ============================================================
# 4_Judy_Norm
# ============================================================
ws = sheet('4_Judy_Norm',[2,46,16,16,16,60])
put(ws,'B2','The Judy (Maple Grove & Overland, Hawkins) — Underwriting Normalization', TITLE)
put(ws,'B3','Corrects: (1) Boise RE taxes (marketed $2,203/u vs ~0.92% levy on 95% of value), (2) other income to market comps, (3) tests market-priced land. Exit cap kept at their 5.25% — after the tax fix it is no longer conservative.', NOTE, wrap=True)
sec(ws,'B5','A. AS MARKETED (source: Hawkins LP model)')
jm = [
 ('Total development cost ($)',41691719,M0,'incl. land at Oct-2024 basis'),
 ('Units',162,NUM,''),
 ('Avg NRSF / unit',907.76,NUM,'147,057 NRSF total'),
 ('Marketed untrended ROC',0.0652,PC,'Exec Summary I11'),
 ('Implied untrended NOI ($)','=C9*C6',M0,''),
 ('Y3 (stabilized) NOI ($)',2914298,M0,''),
 ('Y3 RE taxes ($)',356965,M0,'i.e. $2,203/unit — the problem'),
 ('Y3 other income ($)',578083,M0,'i.e. $3,568/unit'),
 ('Sale F12 NOI ($, Aug-2030)',3075765,M0,''),
 ('Marketed exit cap',0.0525,PC,''),
 ('Gross sale ($)','=C14/C15',M0,'Book: $58.6M / $361.6K per unit'),
 ('Land basis ($, Oct-2024)',2448783,M0,'$15.1K/unit — no mark-to-market'),
 ('Site acres',6.13,'0.00',''),
]
r=6
for label,val,fmt,note in jm:
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

sec(ws,'B20','B. NORMALIZATION ASSUMPTIONS (yellow = edit me)')
jb = [
 ('Normalized other income ($/u/yr)',3000,M0,'CR actual $3,002 (has similar fee programs). Market actuals $2.7-3.0K. Their wifi/valet/smart-home costs are already expensed.'),
 ('OI adjustment ($/yr)','=(C21-C13/C7)*C7',M0,''),
 ('Boise levy (actual)',0.0092,PC,'Canyon Ridge actual: $404,052 / $43.8M taxable = 0.922%'),
 ('Assessment ratio',0.95,PC,'TMG convention'),
 ('Effective levy on value','=C23*C24',PC,''),
 ('Exit cap (kept)',0.0525,PC,'CR award = 4.57% raw for new Boise product today'),
 ('Alt exit cap',0.05,PC,''),
 ('Market land ($/acre)',625000,M0,'Emblem paid $649K/ac in Meridian (2027 close); Boise infill similar'),
]
r=21
for label,val,fmt,note in jb:
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt, YELLOW if label.startswith(('Normalized other','Exit cap (kept)','Market land')) else None)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

sec(ws,'B31','C. NORMALIZED ECONOMICS (formulas)')
jc = [
 ('Sale: NOI excl. taxes, OI-adj ($)','=C14+367674+C22',M0,'367,674 = their Y4 taxes added back; C22 negative'),
 ('Normalized sale value ($)','=C32/(C26+C25)',M0,'closed-form tax solve'),
 ('  per unit','=C33/C7',M0,'vs $361.6K marketed'),
 ('Normalized taxes at sale ($)','=C25*C33',M0,''),
 ('  per unit','=C35/C7',M0,'vs $2,203 marketed'),
 ('Delta vs marketed sale ($)','=C33-C16',M0,''),
 ('Untrended: NOI excl. taxes, OI-adj ($)','=C10+C12+C22',M0,'C12 = Y3 taxes added back (proxy for embedded)'),
 ('Untrended stabilized value ($)','=C38/(C26+C25)',M0,''),
 ('Normalized untrended taxes ($)','=C25*C39',M0,''),
 ('NORMALIZED UNTRENDED NOI ($)','=C38-C40',M0,''),
 ('Normalized untrended ROC','=C41/C6',PC,'vs 6.52% marketed'),
 ('Development spread vs exit cap (bp)','=(C42-C26)*10000',BP,''),
 ('MARKET-LAND SCENARIO','SEC',None,''),
 ('Land at market ($)','=C28*C18',M0,''),
 ('Added land cost ($)','=C45-C17',M0,''),
 ('Adjusted TDC ($)','=C6+C46',M0,''),
 ('ROC on market-land basis','=C41/C47',PC,'what a third party replicating this deal earns'),
]
r=32
for label,f,fmt,note in jc:
    if f=='SEC' or f is None:
        sec(ws,f'B{r}',label); r+=1; continue
    put(ws,f'B{r}',label, BOLD if 'NORMALIZED UNTRENDED NOI' in label or 'ROC' in label else BLACK)
    put(ws,f'C{r}',f,BLACK,fmt); put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
put(ws,'B50','TAKEAWAY: With honest Boise taxes and market other income, The Judy earns ~6.0-6.15% untrended on its stale-land basis and ~5.9% on market land — a 70-90bp spread to its own exit cap. The deal is a land-basis arbitrage; its marketed 6.52% is not comparable to Emblem\'s 6.65% without these fixes.', BOLD, wrap=True)
ws.merge_cells('B50:F52')

# ============================================================
# 5_Pencil
# ============================================================
ws = sheet('5_Pencil',[2,44,13,13,13,13,13,13,13,44])
put(ws,'B2','Rent Required for New Development to Pencil — vs Seasons UW Rent Path', TITLE)
put(ws,'B3','Solves Emblem\'s own operating model for required base rent at a target untrended ROC. All components (cost, opex, OI) escalate at the input rate. Pencil rent/mo = escf x ((ROC x denom + opex)/vacancy-factor − OI/u x units) / units / 12.', NOTE, wrap=True)
sec(ws,'B5','INPUTS')
pin = [
 ('ROC denominator ex-financing ($)',"='3_Emblem_Norm'!C8",GREEN,M0,''),
 ('Untrended opex ($, incl their taxes)',1959830,BLUE,M0,'Emblem in-place opex (Summary D46)'),
 ('Vacancy & collection factor',"=1-0.0587",BLACK,PC,'their 5.87% stack (4.0 vac + 0.5 CL + 1.37 model)'),
 ('Units',256,BLUE,NUM,''),
 ('Avg NRSF',938.98,BLUE,NUM,''),
 ('Escalation (cost & opex & OI)',0.03,BLUE,PC,'their own assumption'),
 ('OI /u/yr — as marketed',"='3_Emblem_Norm'!C23",GREEN,M0,''),
 ('OI /u/yr — normalized',"='3_Emblem_Norm'!C31",GREEN,M0,''),
 ('OI /u/yr — Seasons actual',2736,BLUE,M0,''),
]
r=6
for label,val,font,fmt,note in pin:
    put(ws,f'B{r}',label)
    put(ws,f'C{r}',val,font if isinstance(val,str) else BLUE,fmt)
    if isinstance(val,str) and val.startswith('='): ws[f'C{r}'].font = GREEN if '3_Emblem' in val else BLACK
    put(ws,f'J{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

sec(ws,'B17','PENCIL TABLE ($/mo unless noted)')
years=[2026,2027,2028,2029,2030,2031,2032]
put(ws,'B18','Year',BOLD)
for i,y in enumerate(years):
    put(ws,f'{get_column_letter(3+i)}18',y,BOLD,'0')
put(ws,'B19','Escalation factor',BLACK)
for i,y in enumerate(years):
    col=get_column_letter(3+i)
    put(ws,f'{col}19',f'=(1+$C$11)^{i}',BLACK,'0.000')
put(ws,'B20','Seasons UW market rent',BLACK)
seas={2027:1885,2028:1960,2029:2038,2030:2110,2031:2184,2032:2249}
for i,y in enumerate(years):
    col=get_column_letter(3+i)
    if y in seas: put(ws,f'{col}20',seas[y],BLUE,M0)
def prow(r,label,roc,oiref):
    put(ws,f'B{r}',label)
    for i,y in enumerate(years):
        col=get_column_letter(3+i)
        put(ws,f'{col}{r}',f'={col}$19*(({roc}*$C$6+$C$7)/$C$8-{oiref}*$C$9)/$C$9/12',BLACK,M0)
prow(21,'Pencil @ 6.0% — marketed OI','0.06','$C$12')
prow(22,'Pencil @ 6.5% — marketed OI','0.065','$C$12')
prow(23,'Pencil @ 7.0% — marketed OI','0.07','$C$12')
prow(24,'Pencil @ 6.5% — NORMALIZED OI','0.065','$C$13')
prow(25,'Pencil @ 6.5% — Seasons-actual OI','0.065','$C$14')
put(ws,'B26','Seasons gap vs 6.5% marketed-OI pencil',BOLD)
put(ws,'B27','Seasons gap vs 6.5% NORMALIZED-OI pencil',BOLD)
for i,y in enumerate(years):
    col=get_column_letter(3+i)
    if y in seas:
        put(ws,f'{col}26',f'={col}20/{col}22-1',BLACK,PC1)
        put(ws,f'{col}27',f'={col}20/{col}24-1',BLACK,PC1)
put(ws,'B29','Pencil $/SF @6.5% normalized OI',BLACK)
for i,y in enumerate(years):
    col=get_column_letter(3+i)
    put(ws,f'{col}29',f'={col}24/$C$10',BLACK,M2)
put(ws,'B31','READ: With honest other income, new development needs ~$2.24/SF today at just 6.5% ROC (vs $2.17 on their marketed OI) — Seasons at $2.02 is 10-12% below the corrected pencil at entry, ~9% at exit, and never crosses it.', BOLD, wrap=True)
ws.merge_cells('B31:J33')

# ============================================================
# 6_Exit
# ============================================================
ws = sheet('6_Exit',[2,40,15,15,15,15,15,48])
put(ws,'B2','Seasons Exit — Cap Sensitivity, Anatomy, and Vintage Evidence', TITLE)
sec(ws,'B4','A. EXIT-CAP SENSITIVITY (cash flows from the TMG model; base case reproduces UIRR 8.65% / LIRR 12.14% within ~3bp)')
put(ws,'B5','Model cash-flow inputs',H2)
cfin=[('Initial unlevered outflow ($)',-118493000),('Exit F12 ANOI ($)',7225472),
      ('Selling cost: fixed ($)',25000),('Selling cost: % of value',0.008),('Tax true-up at sale ($)',15345),
      ('Loan proceeds ($)',75811435),('Initial levered equity ($)',-44652663)]
r=6
for label,v in cfin:
    put(ws,f'B{r}',label); put(ws,f'C{r}',v,BLUE,PC if abs(v)<1 else M0); r+=1
put(ws,'B13','Year',BOLD); put(ws,'C13','NOI ($)',BOLD); put(ws,'D13','Capex ($)',BOLD); put(ws,'E13','Debt service ($)',BOLD)
noi=[5904654,6187985,6523187,6841633,7084724]; cap_=[342000,349560,357347,365367,373628]; ds=[4227540,4239123,4239123,4239123,4239123]
for i in range(5):
    put(ws,f'B{14+i}',f'Y{i+1}',BLACK)
    put(ws,f'C{14+i}',noi[i],BLUE,M0); put(ws,f'D{14+i}',cap_[i],BLUE,M0); put(ws,f'E{14+i}',ds[i],BLUE,M0)
put(ws,'B20','Cap grid',H2)
caps=[0.0475,0.05,0.0525,0.055,0.0575]
put(ws,'B21','Exit cap',BOLD)
labels=[('Exit value ($)','=$C$7/{c}21'),('Exit $/unit','={c}22/360'),
        ('Net sale proceeds ($)','={c}22-($C$8+$C$9*{c}22)-$C$10')]
for i,cp in enumerate(caps):
    c=get_column_letter(3+i)
    put(ws,f'{c}21',cp,BLUE,PC)
    put(ws,f'{c}22',f'=$C$7/{c}21',BLACK,M0)
    put(ws,f'{c}23',f'={c}22/360',BLACK,M0)
    put(ws,f'{c}24',f'={c}22-($C$8+$C$9*{c}22)-$C$10',BLACK,M0)
    # unlevered CF rows 25-30 (Y0..Y5)
    put(ws,f'{c}25',f'=$C$6',BLACK,M0)
    for j in range(4):
        put(ws,f'{c}{26+j}',f'=$C${14+j}-$D${14+j}',BLACK,M0)
    put(ws,f'{c}30',f'=$C$18-$D$18+{c}24',BLACK,M0)
    put(ws,f'{c}31',f'=IRR({c}25:{c}30)',BOLD,PC)
    # levered CF rows 32-37
    put(ws,f'{c}32',f'=$C$12',BLACK,M0)
    for j in range(4):
        put(ws,f'{c}{33+j}',f'=$C${14+j}-$D${14+j}-$E${14+j}',BLACK,M0)
    put(ws,f'{c}37',f'=$C$18-$D$18-$E$18+{c}24-$C$11',BLACK,M0)
    put(ws,f'{c}38',f'=IRR({c}32:{c}37)',BOLD,PC)
for rr,lab in [(22,'Exit value ($)'),(23,'Exit $/unit'),(24,'Net proceeds ($)'),(25,'Unlev CF Y0'),(26,'Y1'),(27,'Y2'),(28,'Y3'),(29,'Y4'),(30,'Y5 incl. exit'),(31,'UNLEVERED IRR'),(32,'Lev CF Y0'),(33,'Y1'),(34,'Y2'),(35,'Y3'),(36,'Y4'),(37,'Y5 incl. exit & payoff'),(38,'LEVERED IRR')]:
    put(ws,f'B{rr}',lab,BOLD if 'IRR' in lab else BLACK)
sec(ws,'B40','B. EXIT ANATOMY — the $400.5K "match" decomposed')
put(ws,'B41','',BLACK)
header(ws,41,['B','C','D'],['','Seasons exit (Oct-31, age 7)','Emblem exit (Jan-30, new)'])
an=[('Exit NOI $/unit',20071,22026),('Exit cap',0.05,0.055),('Price $/unit','=C42/C43','=D42/D43'),('Price $/SF','=C44/932.46','=D44/938.98')]
r=42
for label,a,b in an:
    put(ws,f'B{r}',label,BOLD)
    for col,v in (('C',a),('D',b)):
        if isinstance(v,str): put(ws,f'{col}{r}',v,BLACK,M0 if r==44 else M2)
        else: put(ws,f'{col}{r}',v,BLUE,PC if v<1 else M0)
    r+=1
put(ws,'B47','The match is offsetting differences: our NOI is 8.9% BELOW theirs (the vintage discount, in the numerator) while our cap is 50bp TIGHTER (the exposure). Present the exit as a 5.00-5.25% band.',NOTE,wrap=True)
ws.merge_cells('B47:F48')
sec(ws,'B50','C. VINTAGE EVIDENCE (today)')
vin=[('Prelude — age 8 at close (Dec-25)','4.95% Y1 cap','0.94x replacement cost'),
     ('Seasons — age 2 (bid)','5.00% Y1 NOI cap','1.08x replacement cost'),
     ('Canyon Ridge — age 2 (award)','4.57% raw / 5.12% tax-adj','1.25x replacement cost'),
     ('Seasons at exit — age 7 (UW)','5.00% assumed','1.17x forward replacement cost')]
header(ws,51,['B','C','D'],['Asset / age','Cap rate','Price vs replacement cost'])
r=52
for a,b,c in vin:
    put(ws,f'B{r}',a); put(ws,f'C{r}',b,BLUE); put(ws,f'D{r}',c,BLUE); ws[f'B{r}'].border=THIN; r+=1
put(ws,'B57','Caps are age-flat across young vintages today (discount lives in NOI) — supports 5.00% — but a stabilized no-story 7-year-old competing against 2028-29 vintage argues for the wider end. Each 25bp = ~$18-19K/unit = ~90bp UIRR.',NOTE,wrap=True)
ws.merge_cells('B57:F58')

# ============================================================
# 7_Taxes
# ============================================================
ws = sheet('7_Taxes',[2,40,16,16,16,52])
put(ws,'B2','Property Tax Normalization — Meridian vs Boise', TITLE)
header(ws,4,['B','C','D','E','F'],['','Levy (actual)','Taxes $/u/yr (as modeled)','Corrected $/u/yr','Notes'])
tx=[('Seasons (Meridian)',0.004507,1340,None,'Actual: $419,111 / $92.99M taxable = 0.4507%'),
    ('Prelude (Meridian)',0.004507,1169,None,'2025 actual; model reassesses 95% at exit'),
    ('Emblem UW (Meridian)',0.0045,1501,'=\'3_Emblem_Norm\'!C46','Modest understatement (~83% of value assessed)'),
    ('Canyon Ridge (Boise)',0.00922,3428,None,'Actual: $404,052 / $43.8M taxable'),
    ('The Judy UW (Boise)',0.0092,2203,'=\'4_Judy_Norm\'!C36','UNDERSTATED — corrected at right'),]
r=5
for a,b,c,d,e in tx:
    put(ws,f'B{r}',a,BOLD); put(ws,f'C{r}',b,BLUE,'0.000%'); put(ws,f'D{r}',c,BLUE,M0)
    if d: put(ws,f'E{r}',d,GREEN,M0)
    put(ws,f'F{r}',e,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
sec(ws,'B11','TAX-ADJUSTED CAP COMPARISON')
ta=[('Canyon Ridge Y1 NOI ($)',5027967,M0,BLUE),
    ('CR taxes at Boise ($/u)',3428,M0,BLUE),('Seasons taxes ($/u)',1340,M0,BLUE),
    ('Tax delta ($/u)','=C13-C14',M0,BLACK),('CR NOI at Meridian taxes ($)','=C12+C15*288',M0,BLACK),
    ('CR cap as awarded','=C12/110000000',PC,BLACK),('CR cap tax-normalized','=C16/110000000',PC,BLACK),
    ('Seasons Y1 NOI cap',0.05,PC,BLUE),
    ('Capitalized value of Meridian tax advantage ($/u)','=C15/0.05',M0,BLACK)]
r=12
for label,v,fmt,font in ta:
    put(ws,f'B{r}',label)
    if isinstance(v,str): put(ws,f'C{r}',v,font,fmt)
    else: put(ws,f'C{r}',v,font,fmt)
    ws[f'B{r}'].border=THIN; r+=1
put(ws,'B22','Tax-normalized, the CR buyer accepts a THINNER yield (5.12%) than our Seasons bid (5.00%). Never compare Meridian and Boise caps without this adjustment.',BOLD,wrap=True)
ws.merge_cells('B22:F23')

# ============================================================
# 8_Supply
# ============================================================
ws = sheet('8_Supply',[2,44,15,15,15,56])
put(ws,'B2','Supply: Land Inventory & Pipeline', TITLE)
sec(ws,'B4','APARTMENT-READY LAND (5-mile radii — this repo\'s parcel analysis)')
header(ws,5,['B','C','D','E'],['','Seasons at Meridian','Canyon Ridge',''])
sup=[('Apartment-ready acres',1130,143),('Parcels',228,44),('MF-by-right acres',507,102),('Within 2 miles (acres)',309,40)]
r=6
for a,b,c in sup:
    put(ws,f'B{r}',a,BOLD); put(ws,f'C{r}',b,BLUE,NUM); put(ws,f'D{r}',c,BLUE,NUM); ws[f'B{r}'].border=THIN; r+=1
put(ws,'B10','Land is NOT the constraint at Seasons — economics are (see 5_Pencil). At Canyon Ridge, land IS the constraint.',NOTE,wrap=True)
sec(ws,'B12','UNDER CONSTRUCTION (5-mi, from TMG model S&A roster)')
uc=[('Vanguard Village',552,'Q1 2028'),('Centrepoint',213,'Q1 2028'),('Dorado Station',212,'Q3 2027'),('South Ridge II',164,'Q2 2027'),('Summertown (remaining)',72,'Q3 2027')]
header(ws,13,['B','C','D'],['Property','Units','Est. delivery'])
r=14
for a,b,c in uc:
    put(ws,f'B{r}',a); put(ws,f'C{r}',b,BLUE,NUM); put(ws,f'D{r}',c,BLUE); ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r}','TOTAL UC',BOLD); put(ws,f'C{r}','=SUM(C14:C18)',BOLD,NUM); r+=1
sec(ws,f'B{r+1}','PROPOSED (scenario toggle in model)')
prop=[('Record',472),('The Gateway at Ten Mile',390),('Syringa Crossing (Hawkins)',322),('Victory Flats',301),('12565 W Fairview Ave',275),('Pine 43 (Pine & Webb)',270),('Heritage Square (ex-Union 93)',250),('The Cole Denton',200),('Rolling Hill (Assemble)',200),('The Judy (Maple Grove & Overland)',162),('12548 W Overland Rd',156),('Ascent Overland',138),('Meridian OZ Apartments',36),('EMBLEM MERIDIAN — MISSING FROM ROSTER',256)]
r0=r+2
header(ws,r0,['B','C'],['Property','Units'])
r=r0+1
for a,b in prop:
    put(ws,f'B{r}',a, BOLD if 'MISSING' in a else BLACK); put(ws,f'C{r}',b,BLUE,NUM); ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r}','TOTAL PROPOSED (incl. Emblem)',BOLD); put(ws,f'C{r}',f'=SUM(C{r0+1}:C{r-1})',BOLD,NUM)
put(ws,f'B{r+2}','Model base case: 448 units deliver Y1, 765 Y2, zero after. Emblem (deliver Nov-28 to Oct-29 = Y3 bucket) should be added to the roster. Base absorption 500/yr (trailing 3-yr CoStar avg).',NOTE,wrap=True)
ws.merge_cells(f'B{r+2}:F{r+3}')

# ============================================================
# 9_Sources
# ============================================================
ws = sheet('9_Sources',[2,52,90])
put(ws,'B2','Sources & Method', TITLE)
src=[
 ('TMG_Acquisitions_model_7.26 - Seasons_at_Meridian_v3.xlsm','Assumptions (price H5, caps K5/L5, mix B48:T58, exit M33-M40), Cash Flow (Annual) rows 4-59, Supply & Absorption, Rent Roll 8/4/2026.'),
 ('Prelude_at_Paramount_Final_Model.xlsm','Unleveraged tab: price D34, caps B39:D42, exit K39-M42, tax schedule L44-P67 (0.4507% levy), unit mix A46-A67. Closed 12/31/2025.'),
 ('Canyon_Ridge_Model_at_soon_to_be_awarded_price.xlsm','Assumptions C34 ($110M award), caps B39-E41, exit M33-M41; CF (Annual) Y1 taxes $987,197.'),
 ('Emblem_Meridian_Merchant_Model.xlsm','Summary (budget, ROC, exit), Operating Inputs A88-A96 (OI components), A-OperBgt col H (2031), Tax Calcs. Model saved 7/31/2026.'),
 ('Hawkins_MGO_LP_Equity_vF.xlsm + OM','Executive Summary (all-in), Development Budget (land at cost, fees), OM pp.18-24 (rent/sales comps incl. Seasons).'),
 ('Repo: SeasonsMeridian / CanyonRidge / comparison','Parcel-level land-use & MF-threat analysis (5-mi radii).'),
 ('METHOD — normalization','OI marked to market actuals component-by-component; taxes solved closed-form V = NOI-ex-tax/(cap + levy x reassess) to avoid circularity; exit caps normalized to observed prints (CR 4.57% award / 5.12% tax-adj, Seasons 5.00% bid, Prelude 4.95% close).'),
 ('METHOD — pencil rents','Emblem operating model solved for base rent at target untrended ROC; all components escalate 3%/yr (their assumption); ex-financing cost denominator (their convention).'),
 ('VERIFICATION','All 59 source-extracted figures re-derived programmatically from the workbooks 2026-08-13 — 59/59 pass. Seasons exit sensitivity rebuilt from model cash flows; base case reproduces UIRR 8.65%/LIRR 12.14% within ~3bp.'),
]
r=4
for a,b in src:
    put(ws,f'B{r}',a,BOLD,wrap=True); put(ws,f'C{r}',b,BLACK,wrap=True); ws[f'B{r}'].border=THIN; ws[f'C{r}'].border=THIN; r+=1
put(ws,f'B{r+1}','Confidential — internal underwriting work product.',NOTE)

wb.save('Boise_Deals_Normalized_Underwriting.xlsx')
print('saved')
