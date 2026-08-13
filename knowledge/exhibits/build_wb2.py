#!/usr/bin/env python3
"""Boise Deals — Normalized Underwriting Workbook v2 (per user feedback)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
F = lambda **k: Font(name="Arial", **{"size":10, **k})
TITLE=F(bold=True,size=14); H1=F(bold=True,size=11,color='FFFFFF'); H2=F(bold=True)
BLUE=F(color='0000FF'); BLACK=F(); GREEN=F(color='008000'); NOTE=F(italic=True,size=9,color='808080'); BOLD=F(bold=True)
HDRFILL=PatternFill('solid',fgColor='1F3864'); SUBFILL=PatternFill('solid',fgColor='D9E2F2')
YELLOW=PatternFill('solid',fgColor='FFFF00'); THIN=Border(bottom=Side(style='thin',color='BFBFBF'))
M0='$#,##0'; M2='$#,##0.00'; PC='0.00%'; PC1='0.0%'; NUM='#,##0'; BP='0'

def sheet(name,widths):
    ws=wb.create_sheet(name)
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.sheet_view.showGridLines=False
    return ws
def put(ws,cell,val,font=BLACK,fmt=None,fill=None,wrap=False):
    c=ws[cell]; c.value=val; c.font=font
    if fmt: c.number_format=fmt
    if fill: c.fill=fill
    if wrap: c.alignment=Alignment(wrap_text=True,vertical='top')
    return c
def header(ws,row,cols,texts):
    for col,t in zip(cols,texts):
        c=ws[f'{col}{row}']; c.value=t; c.font=H1; c.fill=HDRFILL
        c.alignment=Alignment(horizontal='center',wrap_text=True)
def sec(ws,cell,text):
    c=ws[cell]; c.value=text; c.font=H2; c.fill=SUBFILL

# ================= README =================
ws=wb.active; ws.title='README'
ws.column_dimensions['A'].width=3; ws.column_dimensions['B'].width=112
ws.sheet_view.showGridLines=False
put(ws,'B2','Boise MSA — Deal Comparison & Developer Underwriting Normalization (v2)',TITLE)
put(ws,'B3','Prepared 2026-08-13 (v2 per IC feedback). All model figures re-extracted from source workbooks; levy rates verified against Ada County 2024 certified levies.',NOTE,wrap=True)
txt=[
 ('LEGEND','Blue = input extracted from a source model or public record (cited). Black = formula. Green = cross-sheet link. Yellow fill = normalization assumption — edit to flex.'),
 ('1_Deals','Five-deal side-by-side.'),
 ('2_ProFormas','Per-unit stabilized pro formas — complete for all five deals, incl. full Prelude opex from our acquisition model.'),
 ('3_Dev_Feasibility','THE CENTERPIECE: construction cost build-up, operating pro forma build-up (marketed vs normalized), and the pencil-rent grid (YoC 5.75-7.25% x three OI bases) with the 2026-2032 trajectory vs Seasons.'),
 ('4_Emblem_Norm','Emblem normalization detail (OI, taxes, exit cap).'),
 ('5_Judy_Norm','Judy normalization detail (verified Boise levy, OI, market land).'),
 ('6_Sensitivities','Development-side sensitivities: YoC vs hard cost x rent; pencil $/SF vs YoC x TDC; Judy YoC vs land basis x levy.'),
 ('7_Taxes','Verified levy build-up (Ada County 2024 certified) and the correct comparability principle: CAP RATES ARE COMPARABLE ACROSS JURISDICTIONS (taxes are already in NOI); PRICE PER UNIT IS NOT — identical product carries ~$42K/unit more value in Meridian.'),
 ('8_Supply','Land inventory & pipeline roster.'),
 ('9_Sources','Provenance, method, corrections log.'),
 ('KEY CONCLUSIONS',''),
 ('1.','Emblem true untrended YoC ~6.3% (marketed 6.65%): OI ~$0.8K/unit high; 5.50% exit cap sandbagged — the two roughly offset on exit VALUE (their $400K/home is about right at an honest 5.25%), but the yield claim deflates.'),
 ('2.','Judy true untrended YoC ~6.0-6.1% (marketed 6.52%): Boise taxes ~$750-950/unit light (VERIFIED: Boise code areas levy 0.906-0.914% in 2024 vs Meridian ~0.45%; driver is Boise SD 0.280% vs West Ada 0.033%), OI ~$570/unit high. On market-priced land: ~5.9%. A land-basis arbitrage.'),
 ('3.','Pencil rents (normalized OI & taxes): $1,991/mo ($2.12/SF) at 6.0% YoC, $2,122 ($2.26/SF) at 6.5% — vs Seasons at $1,885 ($2.02/SF). Even at a thin 6.0% hurdle Seasons sits 5-8% below pencil through the whole hold (frozen ~-5%); at 6.5%, 11-14% below.'),
 ('4.','Tax comparability (corrected from v1): cap rates compare directly across Boise/Meridian; $/unit does not. CR at $381.9K/u in Boise is ~$428K/u Meridian-equivalent at its own 4.57% cap — Seasons at $327.8K is ~23% below its jurisdiction-adjusted 2024-vintage comp.'),
 ('5.','True development spreads (normalized YoC minus normalized exit cap) are ~75-105bp vs the 125-175bp institutional requirement — the marginal developer is out of the money; both live deals proceed only on cost advantages (Lennar GC / stale land).'),
]
r=5
for a,b in txt:
    if b=='' or a in('LEGEND',): put(ws,f'B{r}', f'{a} — {b}' if b else a, H2 if not b else BLACK, wrap=True)
    else: put(ws,f'B{r}', f'{a} {b}' if a.endswith('.') else f'{a} — {b}', BLACK, wrap=True)
    r+=1

# ================= 1_Deals =================
ws=sheet('1_Deals',[2,34,17,17,17,17,17,44])
put(ws,'B2','Five-Deal Comparison',TITLE)
header(ws,4,['B','C','D','E','F','G','H'],['Metric','Seasons at Meridian','Prelude at Paramount','Canyon Ridge','Emblem Meridian','The Judy (MGO)','Notes'])
rows=[
 ('Role',['Acquisition target','Owned (12/2025)','Comp — under contract','Development (equity raise)','Development (equity raise)'],None,'Emblem: Quarterra/Lennar. Judy: Hawkins.'),
 ('Location',['2700 E Overland Rd, Meridian','4909 N Elsinore Ave, Meridian','2552 E Gowen Rd, Boise','Eagle/Overland corridor, Meridian','1770 S Maple Grove Rd, Boise'],None,''),
 ('Vintage / delivery',['2024','2018','2024','2028-29','2027-28'],None,''),
 ('Units',[360,280,288,256,162],NUM,''),
 ('Avg unit SF',[932.46,1016.38,888.94,938.98,907.76],NUM,''),
 ('Price / total dev cost ($)',[118000000,79750000,110000000,77959624,41691719],M0,'Seasons = recommended bid (whisper $125M). CR = award.'),
 ('$/unit',None,M0,''),
 ('$/SF (NRSF)',None,M0,''),
 ('Y1 / stabilized NOI ($)',[5904654,4013692,5027967,5036490,2914298],M0,'Prelude = Y1 from Revenue & Expense tab. Emblem = untrended in-place. Judy = Y3.'),
 ('Going-in yield / untrended ROC',[0.0500,0.0503,0.0457,0.0665,0.0652],PC,'TMG: Y1 NOI / price. Developers: marketed — see normalization tabs (true: ~6.3% / ~6.0%).'),
 ('Market rent ($/mo)',[1885,1730,2171,2069,1787],M0,'Each model\'s own UW. Seasons contract rent $1,751.'),
 ('Rent $/SF',None,M2,''),
 ('Other income ($/u/yr)',[2736,2803,3002,4207,3568],M0,'Components on 2_ProFormas; developers high by $0.6-0.8K.'),
 ('RE taxes ($/u/yr)',[1340,1191,3428,1501,2203],M0,'Verified levies: Meridian ~0.45%, Boise ~0.91%. Judy understated — see 5_Judy_Norm.'),
 ('Exit date',['Oct-2031','Dec-2030','Oct-2031 (UW)','Jan-2030','Aug-2030'],None,''),
 ('Exit cap (as modeled)',[0.05,0.05,0.0475,0.055,0.0525],PC,'Developer caps sandbagged vs today\'s prints (CR 4.57%).'),
 ('Exit value ($/unit)',[400563,361232,442763,400467,361642],M0,''),
 ('UIRR / project IRR',[0.0865,0.0894,0.0718,0.3059,0.2506],PC,'Developers = levered project IRR (different metric).'),
 ('LIRR / LP IRR',[0.1214,0.1388,0.0886,0.2229,0.2051],PC,''),
]
r=5
for row in rows:
    label,vals,fmt=row[0],row[1],row[2]; note=row[3]
    put(ws,f'B{r}',label,BOLD)
    if vals:
        for i,v in enumerate(vals): put(ws,f'{get_column_letter(3+i)}{r}',v,BLUE,fmt)
    if note: put(ws,f'H{r}',note,NOTE,wrap=True)
    ws[f'B{r}'].border=THIN; r+=1
for i in range(5):
    c=get_column_letter(3+i)
    put(ws,f'{c}11',f'={c}10/{c}8',BLACK,M0)
    put(ws,f'{c}12',f'={c}10/({c}8*{c}9)',BLACK,M0)
    put(ws,f'{c}16',f'={c}15/{c}9',BLACK,M2)

# ================= 2_ProFormas =================
ws=sheet('2_ProFormas',[2,34,15,15,15,15,15,46])
put(ws,'B2','Per-Unit Stabilized Pro Formas ($/unit/yr unless noted)',TITLE)
put(ws,'B3','Seasons & CR = TMG Y1. Prelude = our acquisition UW Y1 (I&E + Revenue & Expense tabs). Emblem = 2031 stabilized (trended $). Judy = Year 3.',NOTE,wrap=True)
header(ws,5,['B','C','D','E','F','G','H'],['Line','Seasons Y1','Prelude Y1','Canyon Ridge Y1','Emblem stab. 2031','Judy Y3','Notes'])
pf=[
 ('Market rent ($/mo)',[1885,1730,2171,2443,1787],M0,'Emblem = their 2031 trended rent ($2,069 at 6/2026).'),
 ('Rent $/SF ($/mo)',['=C6/932.46','=D6/1016.38','=E6/888.94','=F6/938.98','=G6/907.76'],M2,''),
 ('OTHER INCOME','SEC',None,''),
 ('Misc / fees',[601,1281,1897,721,None],M0,'CR incl. damage waiver. Prelude incl. bulk-data income. Judy not itemized in OM/model.'),
 ('RUBS / utility billback',[698,763,581,1149,None],M0,'Seasons ~66% recovery actual; Emblem assumes 100%.'),
 ('Parking / garages',[360,759,520,1041,None],M0,'Prelude actual with rentable garages. Emblem monetizes all 536 spaces.'),
 ('Wifi / revenue share',[1077,0,3,1296,None],M0,'Seasons = bulk internet rev share. Emblem = mandatory $108/mo.'),
 ('Total other income',['=SUM(C9:C12)','=SUM(D9:D12)','=SUM(E9:E12)','=SUM(F9:F12)',3568],M0,'Judy total from Y3 pro forma.'),
 ('EFFECTIVE GROSS INCOME',[23057,20862,26725,31534,25189],M0,'After vacancy/concessions/bad debt.'),
 ('OPERATING EXPENSES','SEC',None,''),
 ('Payroll / personnel',[1671,1797,1749,1804,0],M0,'Judy payroll bundled in mgmt fee.'),
 ('Marketing',[367,347,346,406,371],M0,''),
 ('G&A / admin',[423,399,660,480,None],M0,'Judy G&A within mgmt fee.'),
 ('Turnover / make-ready',[200,228,152,None,254],M0,'Emblem turnover within R&M.'),
 ('R&M',[175,157,173,541,344],M0,''),
 ('Contracts / services',[619,716,996,972,708],M0,'Judy = contract svcs + wifi + valet + smart-home costs.'),
 ('Utilities',[760,559,470,1405,859],M0,''),
 ('Management fee',[576,522,668,946,2015],M0,'Judy 8% of EGI incl. payroll/G&A.'),
 ('Insurance',[525,620,625,496,446],M0,''),
 ('Real estate taxes',[1340,1191,3428,1501,2203],M0,'Prelude = 2026 taxes $333,466/280. Judy understated (5_Judy_Norm).'),
 ('Total opex',['=SUM(C16:C25)','=SUM(D16:D25)','=SUM(E16:E25)',8779,7200],M0,'Emblem incl. $227/u reserves + $1/u other (their categories).'),
 ('NOI ($/unit)',['=C14-C26','=D14-D26','=E14-E26','=F14-F26','=G14-G26'],M0,'Cross-check: Seasons $16,402; Prelude $14,335; CR $17,458; Emblem $22,755; Judy $17,990.'),
 ('Expense ratio',['=C26/C14','=D26/D14','=E26/E14','=F26/F14','=G26/G14'],PC1,''),
]
r=6
for label,vals,fmt,note in pf:
    if vals=='SEC': sec(ws,f'B{r}',label); r+=1; continue
    put(ws,f'B{r}',label,BOLD if label.startswith(('Total','NOI','EFFECTIVE')) else BLACK)
    for i,v in enumerate(vals):
        col=get_column_letter(3+i)
        if v is None: put(ws,f'{col}{r}',0,BLUE,fmt); continue
        if isinstance(v,str): put(ws,f'{col}{r}',v,BLACK,fmt)
        else: put(ws,f'{col}{r}',v,BLUE,fmt)
    if note: put(ws,f'H{r}',note,NOTE,wrap=True)
    ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r+1}','Prelude reconciliation: EGI $20,862 (Rev&Exp H27/280) − opex $6,536 = NOI $14,326 ≈ $14,335 (H53/280; rounding). Old-model note: its "Total Controllable" excludes utilities; utilities+insurance+mgmt+taxes reconcile to total.',NOTE,wrap=True)
ws.merge_cells(f'B{r+1}:H{r+2}')

# ================= 3_Dev_Feasibility =================
ws=sheet('3_Dev_Feasibility',[2,40,15,15,15,15,15,15,46])
put(ws,'B2','Development Feasibility — Cost Build-Up, Pro Forma, and Pencil Rents',TITLE)
put(ws,'B3','One tab, whole story: what it costs to build, what the operations look like (as marketed vs normalized), and the rent required at each yield-on-cost hurdle vs where Seasons sits.',NOTE,wrap=True)

sec(ws,'B5','A. CONSTRUCTION COST BUILD-UP')
header(ws,6,['B','C','D','E','F','G','H'],['Component','Emblem ($)','Emblem $/unit','Emblem $/NRSF','Judy ($)','Judy $/unit','Judy $/NRSF'])
cost=[
 ('Land & acquisition',9092960,2448783,'Emblem $649K/ac (13.63 ac). Judy at Oct-2024 basis $399K/ac — market ~$625K/ac adds ~$1.4M (see 5_Judy_Norm).'),
 ('Hard costs incl. contingency',54579077,31439373,'Both ~$214-227/NRSF — two independent GCs triangulate hard cost.'),
 ('A&E',1500605,None,'Judy A&E inside soft costs below.'),
 ('Permits & impact fees',4459159,None,'Meridian P&F $17.4K/u vs Judy (Boise) ~$6.1K/u impact fees within soft.'),
 ('Other soft (ins, FF&E, start-up, op deficits, contingency)',3686917,3714573,'Judy soft = all soft ex-interest (incl. A&E and fees).'),
 ('Developer fee / overhead',2658062,638854,'Emblem 4% dev fee. Judy fees partly outside LP budget ("other development costs" shown).'),
 ('Financing & interest',1982845,3450136,'Judy = financing/contingencies 2,372,940 + interest reserve 1,058,670 + op deficit 18,526.'),
]
r=7
for label,e,j,note in cost:
    put(ws,f'B{r}',label)
    put(ws,f'C{r}',e,BLUE,M0); put(ws,f'D{r}',f'=C{r}/256',BLACK,M0); put(ws,f'E{r}',f'=C{r}/240380',BLACK,M2)
    if j is not None:
        put(ws,f'F{r}',j,BLUE,M0); put(ws,f'G{r}',f'=F{r}/162',BLACK,M0); put(ws,f'H{r}',f'=F{r}/147057',BLACK,M2)
    put(ws,f'I{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r}','TOTAL DEVELOPMENT COST',BOLD)
put(ws,f'C{r}','=SUM(C7:C13)',BOLD,M0); put(ws,f'D{r}',f'=C{r}/256',BOLD,M0); put(ws,f'E{r}',f'=C{r}/240380',BOLD,M2)
put(ws,f'F{r}','=SUM(F7:F13)',BOLD,M0); put(ws,f'G{r}',f'=F{r}/162',BOLD,M0); put(ws,f'H{r}',f'=F{r}/147057',BOLD,M2)
put(ws,f'I{r}','Checks: Emblem $77.96M / $304.5K/u / $324/SF. Judy $41.69M / $257.4K/u / $283.5/SF.',NOTE,wrap=True)
r+=2
put(ws,f'B{r}','Emblem ROC denominator (ex-financing)',BOLD); put(ws,f'C{r}','=C14-C13',BLACK,M0)
put(ws,f'I{r}','Their yield convention divides by cost ex-financing.',NOTE,wrap=True)
DENOM=f'$C${r}'
r+=2

sec(ws,f'B{r}','B. OPERATING PRO FORMA BUILD-UP (per unit per year, untrended 2026$, Emblem basis)')
r+=1
hdr_r=r
header(ws,hdr_r,['B','C','D','E'],['Line','As marketed','Normalized','Notes'])
r+=1
base=r
op=[
 ('Base rent ($/mo)',2069,2069,'Rent level NOT normalized — their $2.20/SF vs comp set is defensible; the pencil grid below solves for it anyway.'),
 ('Base rent ($/yr)',f'=C{base}*12',f'=D{base}*12',''),
 ('Other income ($/yr)',4207,"='4_Emblem_Norm'!C29",'Normalized: garages 750, wifi 1,077, billback 850, pets 126, misc 595.'),
 ('Potential gross income',f'=C{base+1}+C{base+2}',f'=D{base+1}+D{base+2}',''),
 ('Less vacancy & collections (5.87%)',f'=-C{base+3}*0.0587',f'=-D{base+3}*0.0587','Their stack: 4.0% vac + 0.5% CL + 1.37% model units.'),
 ('Effective gross income',f'=C{base+3}+C{base+4}',f'=D{base+3}+D{base+4}',''),
 ('Opex ex-taxes',f'=-6360',f'=-6360','(1,959,830 − 331,600 embedded taxes)/256.'),
 ('RE taxes',-1295,"=-'4_Emblem_Norm'!C46",'Marketed: embedded est. Normalized: 0.45% x 95% of closed-form value.'),
 ('NOI ($/unit)',f'=SUM(C{base+5}:C{base+7})',f'=SUM(D{base+5}:D{base+7})',''),
 ('NOI ($, project)',f'=C{base+8}*256',f'=D{base+8}*256',''),
 ('UNTRENDED YIELD-ON-COST (ex-fin)',f'=C{base+9}/{DENOM}',f'=D{base+9}/{DENOM}','Marketed ~6.6% vs normalized ~6.3%.'),
 ('YoC on all-in cost',f'=C{base+9}/$C$14',f'=D{base+9}/$C$14',''),
]
for label,cv,dv,note in op:
    put(ws,f'B{r}',label,BOLD if 'YoC' in label or 'YIELD' in label or label.startswith('NOI') else BLACK)
    for col,v in (('C',cv),('D',dv)):
        fmt = PC if 'YoC' in label or 'YIELD' in label else (M0 if 'mo' not in label else M0)
        if isinstance(v,str): put(ws,f'{col}{r}',v,GREEN if 'Norm' in v else BLACK,fmt)
        else: put(ws,f'{col}{r}',v,BLUE,fmt)
    put(ws,f'E{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
NOI_MKT=f'C{base+8}'
r+=1

sec(ws,f'B{r}','C. PENCIL RENT GRID — base rent required ($/mo and $/SF) by yield-on-cost hurdle x other-income basis')
r+=1
put(ws,f'B{r}','Convention: opex ex-tax + NORMALIZED taxes ($1,518/u) held fixed; vacancy 5.87%; cost = ex-financing denominator. Formula: rent/yr = (YoC x denom + opex)/0.9413 − OI x units, per unit.',NOTE,wrap=True)
ws.merge_cells(f'B{r}:I{r}')
r+=1
grid_hdr=r
header(ws,grid_hdr,['B','C','D','E','F','G','H'],['YoC hurdle','Marketed OI ($4,207/u) $/mo','Normalized OI ($3,398/u) $/mo','Seasons-actual OI ($2,736/u) $/mo','Normalized OI $/SF','Premium vs Seasons $1,885','Premium vs Seasons $2.02/SF'])
r+=1
OPEXTAX = "((1959830-331600)+'4_Emblem_Norm'!C45)"   # opex ex-tax ($) + normalized taxes ($)
yocs=[0.0575,0.06,0.0625,0.065,0.0675,0.07,0.0725]
gr0=r
for y in yocs:
    put(ws,f'B{r}',y,BLUE,PC)
    for col,oi in (('C',4207),('D',"'4_Emblem_Norm'!C29"),('E',2736)):
        oiref = oi if isinstance(oi,str) else str(oi)
        put(ws,f'{col}{r}',f'=((B{r}*{DENOM}+{OPEXTAX})/0.9413-{oiref}*256)/256/12',BLACK,M0)
    put(ws,f'F{r}',f'=D{r}/938.98',BLACK,M2)
    put(ws,f'G{r}',f'=D{r}/1885-1',BLACK,PC1)
    put(ws,f'H{r}',f'=F{r}/2.021-1',BLACK,PC1)
    ws[f'B{r}'].border=THIN; r+=1
r+=1
sec(ws,f'B{r}','D. TRAJECTORY 2026-2032 — normalized-OI pencil vs Seasons UW rent path (all components escalate 3%/yr)')
r+=1
tr0=r
put(ws,f'B{r}','Year',BOLD)
for i,y in enumerate(range(2026,2033)): put(ws,f'{get_column_letter(3+i)}{r}',y,BOLD,'0')
r+=1
put(ws,f'B{r}','Seasons UW market rent ($/mo)')
seas={2027:1885,2028:1960,2029:2038,2030:2110,2031:2184,2032:2249}
for i,y in enumerate(range(2026,2033)):
    if y in seas: put(ws,f'{get_column_letter(3+i)}{r}',seas[y],BLUE,M0)
r+=1
put(ws,f'B{r}','Pencil @6.0% (normalized OI)')
for i,y in enumerate(range(2026,2033)):
    put(ws,f'{get_column_letter(3+i)}{r}',f'=$D${gr0+1}*1.03^{i}',BLACK,M0)
r+=1
put(ws,f'B{r}','Pencil @6.5% (normalized OI)')
for i,y in enumerate(range(2026,2033)):
    put(ws,f'{get_column_letter(3+i)}{r}',f'=$D${gr0+3}*1.03^{i}',BLACK,M0)
r+=1
put(ws,f'B{r}','Seasons gap vs 6.0% pencil',BOLD)
for i,y in enumerate(range(2026,2033)):
    c=get_column_letter(3+i)
    if y in seas: put(ws,f'{c}{r}',f'={c}{tr0+1}/{c}{tr0+2}-1',BLACK,PC1)
r+=1
put(ws,f'B{r}','Seasons gap vs 6.5% pencil',BOLD)
for i,y in enumerate(range(2026,2033)):
    c=get_column_letter(3+i)
    if y in seas: put(ws,f'{c}{r}',f'={c}{tr0+1}/{c}{tr0+3}-1',BLACK,PC1)
r+=2
put(ws,f'B{r}','READ: At a 6.0% hurdle — the thinnest plausible go-decision vs a 5.0-5.25% exit cap — new supply needs ~$1,991/mo ($2.12/SF) today, 5.6% above Seasons; the gap runs -8% (2027) to -5.4% (2031) and freezes. At 6.5%, Seasons is 11-14% below pencil throughout. The moat is economic and durable under our own rent growth.',BOLD,wrap=True)
ws.merge_cells(f'B{r}:I{r+2}')

# ================= 4_Emblem_Norm =================
ws=sheet('4_Emblem_Norm',[2,46,16,16,16,60])
put(ws,'B2','Emblem Meridian — Normalization Detail',TITLE)
sec(ws,'B4','A. AS MARKETED')
em=[
 ('Total development cost ($)',77959624,M0,'Summary D25 (Oct-27 GMP)'),
 ('Financing costs in TDC ($)',1982846,M0,'Constr interest + financing fees'),
 ('ROC denominator ex-financing ($)','=C5-C6',M0,''),
 ('Units',256,NUM,''),('Avg NRSF / unit',938.98,NUM,''),
 ('Untrended NOI in-place 6/2026 ($)',5036490,M0,'Summary D49'),
 ('Marketed untrended ROC','=C10/C7',PC,'Book: 6.65%'),
 ('Untrended taxes embedded ($, est)',331600,M0,'2031 taxes deflated 3%/yr'),
 ('Sale F12 NOI ($, Jan-30)',5638571,M0,''),('Marketed exit cap',0.055,PC,''),
 ('Gross sale ($)','=C13/C14',M0,'$400.5K/home'),
 ('OI as marketed: garage',266400,M0,'$1,041/u'),('wifi',331776,M0,'$1,296/u'),
 ('billback',294267,M0,'$1,149/u'),('pets',32256,M0,''),('misc',152320,M0,''),
 ('Total OI ($/yr)','=SUM(C16:C20)',M0,'$4,207/u'),
]
r=5
for label,val,fmt,note in em:
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
sec(ws,'B23','B. NORMALIZATION ASSUMPTIONS (yellow = edit)')
nb=[
 ('Garage / parking ($/u/yr)',750,'Prelude achieves $759 WITH rentable garages; CR $520; Seasons $360; attached TH garages usually in rent.'),
 ('Wifi / connectivity ($/u/yr)',1077,'Seasons proven revenue share.'),
 ('Utility billback ($/u/yr)',850,'Actuals $698-763; submetered new build earns premium, not 100%.'),
 ('Pet fees ($/u/yr)',126,''),('Misc ($/u/yr)',595,''),
 ('Normalized OI ($/u/yr)','=SUM(C24:C28)','vs $4,207 marketed'),
 ('OI adjustment ($/yr)','=(C29-C21/C8)*C8',''),
 ('Meridian levy',0.0045,'VERIFIED: Ada Cty 2024 certified — City of Meridian 0.2033% + West Ada SD 0.0332% + county/common ~0.21% = ~0.45%; matches Seasons/Prelude actuals 0.4507%.'),
 ('Assessment ratio',0.95,'TMG convention; ID non-disclosure'),
 ('Effective levy','=C31*C32',''),
 ('Normalized exit cap',0.0525,'Today\'s new-product prints: CR award 4.57%; Seasons bid 5.00%; Prelude 4.95%. 5.25% = +25-70bp forward conservatism.'),
 ('Alt exit cap',0.05,''),
]
r=24
for label,val,note in nb:
    put(ws,f'B{r}',label)
    fmt=PC if isinstance(val,float) and val<1 else M0
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt,YELLOW if label.split(' (')[0] in('Garage / parking','Wifi / connectivity','Utility billback','Normalized exit cap') else None)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
ws['C29'].number_format=M0; ws['C30'].number_format=M0; ws['C33'].number_format=PC
sec(ws,'B37','C. NORMALIZED ECONOMICS')
nc=[
 ('Untrended NOI excl taxes, OI-adj ($)','=C10+C12+C30*0.9413',M0,'OI adj x (1-5.87%) since OI sits inside PGI'),
 ('Stabilized value @ C34 ($)','=C38/(C34+C33)',M0,'closed-form tax solve'),
 ('  per unit','=C39/C8',M0,''),
 ('Normalized taxes ($)','=C33*C39',M0,''),
 ('  per unit','=C41/C8',M0,''),
 ('NORMALIZED UNTRENDED NOI ($)','=C38-C41',M0,''),
 ('Normalized untrended ROC (ex-fin)','=C43/C7',PC,'vs 6.65% marketed'),
 ('Normalized taxes ($) [link for feasibility tab]','=C41',M0,''),
 ('Normalized taxes ($/u) [link]','=C41/C8',M0,''),
 ('Sale NOI excl tax, OI-adj ($)','=C13+384319+C30*1.03^5*0.9413',M0,'their 2031 taxes added back; OI adj escalated & vacancy-adjusted'),
 ('Normalized sale value @C34 ($)','=C47/(C34+C33)',M0,''),
 ('  per unit','=C48/C8',M0,'vs $400.5K marketed — the sandbagged cap ~offsets the aggressive OI'),
 ('  @ alt cap','=C47/(C35+C33)',M0,''),
 ('  per unit','=C50/C8',M0,''),
]
r=38
for label,f,fmt,note in nc:
    put(ws,f'B{r}',label,BOLD if 'NORMALIZED UNTRENDED NOI' in label or 'ROC' in label else BLACK)
    put(ws,f'C{r}',f,BLACK,fmt); put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
# aliases used by other tabs: C31=NormOI/u? keep mapping: C29 normalized OI/u; C45 taxes $; C46 taxes /u
# For 3_Dev_Feasibility references: '4_Emblem_Norm'!C31 (norm OI /u) -> actually C29. Fix links there instead.

# ================= 5_Judy_Norm =================
ws=sheet('5_Judy_Norm',[2,46,16,16,16,60])
put(ws,'B2','The Judy (Hawkins) — Normalization Detail',TITLE)
put(ws,'B3','Boise levy VERIFIED against Ada County 2024 certified rates: City of Boise 0.4053% + Boise SD#1 0.2797% + county/common ~0.22% = 0.906-0.914% combined; CR actual bill = 0.9217% (2025). Judy\'s $2,203/u UW is ~0.63% — not a Boise reality.',NOTE,wrap=True)
sec(ws,'B5','A. AS MARKETED')
jm=[
 ('Total development cost ($)',41691719,M0,''),
 ('Units',162,NUM,''),('Avg NRSF / unit',907.76,NUM,''),
 ('Marketed untrended ROC',0.0652,PC,''),
 ('Implied untrended NOI ($)','=C9*C6',M0,''),
 ('Y3 NOI ($)',2914298,M0,''),('Y3 RE taxes ($)',356965,M0,'$2,203/u'),
 ('Untrended embedded taxes est ($)','=C12/1.03^3',M0,'Y3 deflated to 2026$'),
 ('Y3 other income ($)',578083,M0,'$3,568/u'),
 ('Sale F12 NOI ($)',3075765,M0,''),('Marketed exit cap',0.0525,PC,''),
 ('Gross sale ($)','=C15/C16',M0,'$361.6K/u'),
 ('Land basis ($, Oct-24)',2448783,M0,'$15.1K/u, $399K/ac'),('Site acres',6.13,'0.00',''),
]
r=6
for label,val,fmt,note in jm:
    put(ws,f'B{r}',label)
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,fmt)
    else: put(ws,f'C{r}',val,BLUE,fmt)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
sec(ws,'B21','B. ASSUMPTIONS (yellow = edit)')
jb=[
 ('Normalized OI ($/u/yr)',3000,'CR actual $3,002 with similar fee programs; their program costs already expensed.'),
 ('OI adjustment ($/yr)','=(C22-C14/C7)*C7',''),
 ('Boise levy',0.0092,'Ada Cty 2024 certified 0.906-0.914%; CR actual 0.9217%.'),
 ('Assessment ratio',0.95,''),
 ('Effective levy','=C24*C25',''),
 ('Exit cap (kept)',0.0525,'CR clears 4.57% today; 5.25% is already conservative post-tax-fix.'),
 ('Market land ($/acre)',625000,'Emblem Meridian print $649K/ac.'),
]
r=22
for label,val,note in jb:
    put(ws,f'B{r}',label)
    fmt=PC if isinstance(val,float) and val<1 else M0
    if isinstance(val,str): put(ws,f'C{r}',val,BLACK,M0)
    else: put(ws,f'C{r}',val,BLUE,fmt,YELLOW if label.startswith(('Normalized OI','Exit cap','Market land')) else None)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
ws['C26'].number_format=PC
sec(ws,'B30','C. NORMALIZED ECONOMICS')
jc=[
 ('Untrended NOI excl tax, OI-adj ($)','=C10+C13+C23*0.9413',M0,'deflated embedded taxes; OI adj vacancy-adjusted'),
 ('Untrended stabilized value ($)','=C31/(C27+C26)',M0,''),
 ('Normalized untrended taxes ($)','=C26*C32',M0,''),
 ('  per unit','=C33/C7',M0,'vs $2,203 marketed'),
 ('NORMALIZED UNTRENDED NOI ($)','=C31-C33',M0,''),
 ('Normalized untrended ROC','=C35/C6',PC,'vs 6.52% marketed'),
 ('Sale NOI excl tax, OI-adj ($)','=C15+367674+C23*1.03*0.9413',M0,'Y4 taxes added back; OI adj vacancy-adjusted'),
 ('Normalized sale value ($)','=C37/(C27+C26)',M0,''),
 ('  per unit','=C38/C7',M0,'vs $361.6K marketed'),
 ('MARKET-LAND SCENARIO','SEC',None,''),
 ('Land at market ($)','=C28*C19',M0,''),
 ('Added land cost ($)','=C41-C18',M0,''),
 ('Adjusted TDC ($)','=C6+C42',M0,''),
 ('ROC on market-land basis','=C35/C43',PC,'third-party replication'),
]
r=31
for label,f,fmt,note in jc:
    if f=='SEC' or f is None: sec(ws,f'B{r}',label); r+=1; continue
    put(ws,f'B{r}',label,BOLD if 'NORMALIZED UNTRENDED NOI' in label or 'ROC' in label else BLACK)
    put(ws,f'C{r}',f,BLACK,fmt); put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1

# ================= 6_Sensitivities =================
ws=sheet('6_Sensitivities',[2,34,13,13,13,13,13,13,13,46])
put(ws,'B2','Development Sensitivities (normalized bases)',TITLE)
put(ws,'B3','What actually moves feasibility: construction cost, rent, land, taxes. All grids formula-driven off the normalization tabs.',NOTE,wrap=True)

sec(ws,'B5','GRID 1 — EMBLEM NORMALIZED UNTRENDED YoC: hard cost x rent  (base rent $2,069; normalized OI & taxes held at base)')
put(ws,'B6','Rows = hard-cost change; Cols = rent change',NOTE)
rents=[-0.05,-0.025,0,0.025,0.05]; hards=[-0.10,-0.05,0,0.05,0.10]
for j,dr in enumerate(rents):
    put(ws,f'{get_column_letter(3+j)}7',dr,BLUE,PC1)
for i,dh in enumerate(hards):
    rr=8+i
    put(ws,f'B{rr}',dh,BLUE,PC1)
    for j,dr in enumerate(rents):
        c=get_column_letter(3+j)
        f=(f"=((6355373*(1+{c}$7)+'4_Emblem_Norm'!$C$29*256)*0.9413"
           f"-(1959830-331600)-'4_Emblem_Norm'!$C$41)"
           f"/('4_Emblem_Norm'!$C$7+54579077*$B{rr})")
        put(ws,f'{c}{rr}',f,BLACK,PC)
put(ws,'J8','Center = normalized base ~6.3%. Their marketed 6.65% requires BOTH their OI and their tax line.',NOTE,wrap=True)

sec(ws,'B15','GRID 2 — PENCIL RENT $/SF (normalized OI & taxes): YoC hurdle x total-cost change')
tdcs=[-0.10,-0.05,0,0.05,0.10]
for j,dt in enumerate(tdcs):
    put(ws,f'{get_column_letter(3+j)}16',dt,BLUE,PC1)
yocs2=[0.0575,0.06,0.0625,0.065,0.0675,0.07]
for i,y in enumerate(yocs2):
    rr=17+i
    put(ws,f'B{rr}',y,BLUE,PC)
    for j,dt in enumerate(tdcs):
        c=get_column_letter(3+j)
        f=(f"=(($B{rr}*'4_Emblem_Norm'!$C$7*(1+{c}$16)+(1959830-331600)+'4_Emblem_Norm'!$C$41)/0.9413"
           f"-'4_Emblem_Norm'!$C$29*256)/256/12/938.98")
        put(ws,f'{c}{rr}',f,BLACK,M2)
put(ws,'J17','Seasons market rent today = $2.02/SF. Every cell above $2.02 = supply shut off at that hurdle/cost combination.',NOTE,wrap=True)

sec(ws,'B24','GRID 3 — JUDY NORMALIZED UNTRENDED YoC: land basis x Boise levy')
levies=[0.0070,0.0078,0.0085,0.0092,0.0100]
for j,lv in enumerate(levies):
    put(ws,f'{get_column_letter(3+j)}25','%.2f%%'%(lv*100),BLUE)
lands=[399000,500000,625000,750000,850000]
for i,ld in enumerate(lands):
    rr=26+i
    put(ws,f'B{rr}',ld,BLUE,M0)
    for j,lv in enumerate(levies):
        c=get_column_letter(3+j)
        f=(f"=('5_Judy_Norm'!$C$31-({lv}*0.95)*('5_Judy_Norm'!$C$31/('5_Judy_Norm'!$C$27+{lv}*0.95)))"
           f"/('5_Judy_Norm'!$C$6+MAX(0,$B{rr}*6.13-2448783))")
        put(ws,f'{c}{rr}',f,BLACK,PC)
put(ws,'J26','Row 1 = their actual land basis ($399K/ac). At the verified 0.92% levy and market land, YoC ~5.9% — the deal is a land-basis arbitrage.',NOTE,wrap=True)
put(ws,'B33','Note: grids hold normalized taxes fixed w.r.t. rent/cost changes (taxes actually scale with value — second-order).',NOTE,wrap=True)

# ================= 7_Taxes =================
ws=sheet('7_Taxes',[2,42,16,16,16,54])
put(ws,'B2','Property Taxes — Verified Levies & the Right Comparability Principle',TITLE)
sec(ws,'B4','A. VERIFIED LEVY BUILD-UP (Ada County 2024 certified rates)')
header(ws,5,['B','C','D','E'],['District','Boise code area','Meridian code area','Source / note'])
lv=[('City levy',0.004053,0.002033,'Ada Cty 2024 Levy Rates by Tax District'),
    ('School district',0.002797,0.000332,'Boise SD #1 vs West Ada (Joint SD #2) — THE structural driver'),
    ('County + ACHD + EMS + CWI + misc',0.002209,0.002142,'Balance to observed totals'),
    ('TOTAL (approx)',0.009059,0.004507,'Boise code areas 0.9059-0.9143%. Empirical: CR bill 0.9217% (2025); Seasons & Prelude 0.4507%.')]
r=6
for a,b,c,d in lv:
    put(ws,f'B{r}',a,BOLD if 'TOTAL' in a else BLACK)
    put(ws,f'C{r}',b,BLUE,'0.000%'); put(ws,f'D{r}',c,BLUE,'0.000%'); put(ws,f'E{r}',d,NOTE,wrap=True)
    ws[f'B{r}'].border=THIN; r+=1
sec(ws,'B11','B. THE COMPARABILITY PRINCIPLE (corrected from v1)')
put(ws,'B12','Taxes are an operating expense INSIDE NOI. A cap rate (NOI/price) is therefore directly comparable across jurisdictions — the market capitalizes the tax burden into PRICE, not into the cap. What is NOT comparable is price per unit: an identical building carries more value in Meridian because its NOI is higher.',BLACK,wrap=True)
ws.merge_cells('B12:F14')
sec(ws,'B16','C. JURISDICTION-ADJUSTED PRICE PER UNIT (identical-building thought experiment)')
ja=[
 ('Tax delta, Boise vs Meridian ($/u/yr)','=3428-1340',M0,'CR vs Seasons actual UW lines'),
 ('Capitalized value of Meridian advantage ($/u @5% cap)','=C17/0.05',M0,'~$42K/unit for identical product'),
 ('CR award ($/u, Boise)',381944,M0,''),
 ('CR NOI + tax delta ($)','=5027967+C17*288',M0,'same building, Meridian taxes'),
 ('CR Meridian-equivalent value ($/u) at its own 4.57% cap','=C20/0.045709/288',M0,''),
 ('Seasons bid ($/u)',327778,M0,''),
 ('Seasons discount to jurisdiction-adjusted CR','=C22/C21-1',PC1,'~-23% for same-vintage product'),
 ('Seasons Boise-equivalent ($/u) at 5.00%','=(5904654-C17*360)/0.05/360',M0,'the reverse check'),
]
r=17
for label,v,fmt,note in ja:
    put(ws,f'B{r}',label)
    if isinstance(v,str): put(ws,f'C{r}',v,BLACK,fmt)
    else: put(ws,f'C{r}',v,BLUE,fmt)
    put(ws,f'F{r}',note,NOTE,wrap=True); ws[f'B{r}'].border=THIN; r+=1
put(ws,'B26','v1 of this workbook presented a "tax-normalized cap rate" for CR (5.12%) and said caps should not be compared across jurisdictions without it. That was backwards and is retracted: caps compare directly; $/unit requires the adjustment above.',NOTE,wrap=True)
ws.merge_cells('B26:F27')

# ================= 8_Supply =================
ws=sheet('8_Supply',[2,44,15,15,15,56])
put(ws,'B2','Supply: Land Inventory & Pipeline',TITLE)
sec(ws,'B4','APARTMENT-READY LAND (5-mile radii — repo parcel analysis)')
header(ws,5,['B','C','D'],['','Seasons at Meridian','Canyon Ridge'])
for i,(a,b,c) in enumerate([('Apartment-ready acres',1130,143),('Parcels',228,44),('MF-by-right acres',507,102),('Within 2 miles (acres)',309,40)]):
    r=6+i; put(ws,f'B{r}',a,BOLD); put(ws,f'C{r}',b,BLUE,NUM); put(ws,f'D{r}',c,BLUE,NUM); ws[f'B{r}'].border=THIN
sec(ws,'B11','UNDER CONSTRUCTION (5-mi, model S&A roster)')
header(ws,12,['B','C','D'],['Property','Units','Est. delivery'])
uc=[('Vanguard Village',552,'Q1 2028'),('Centrepoint',213,'Q1 2028'),('Dorado Station',212,'Q3 2027'),('South Ridge II',164,'Q2 2027'),('Summertown (remaining)',72,'Q3 2027')]
r=13
for a,b,c in uc:
    put(ws,f'B{r}',a); put(ws,f'C{r}',b,BLUE,NUM); put(ws,f'D{r}',c,BLUE); ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r}','TOTAL UC',BOLD); put(ws,f'C{r}','=SUM(C13:C17)',BOLD,NUM)
sec(ws,f'B{r+2}','PROPOSED (model toggle) + EMBLEM (missing from roster)')
prop=[('Record',472),('The Gateway at Ten Mile',390),('Syringa Crossing (Hawkins)',322),('Victory Flats',301),('12565 W Fairview Ave',275),('Pine 43 (Pine & Webb)',270),('Heritage Square (ex-Union 93)',250),('The Cole Denton',200),('Rolling Hill (Assemble)',200),('The Judy (Maple Grove & Overland)',162),('12548 W Overland Rd',156),('Ascent Overland',138),('Meridian OZ Apartments',36),('EMBLEM MERIDIAN — ADD TO ROSTER (Y3 bucket)',256)]
r0=r+3
header(ws,r0,['B','C'],['Property','Units'])
r=r0+1
for a,b in prop:
    put(ws,f'B{r}',a,BOLD if 'EMBLEM' in a else BLACK); put(ws,f'C{r}',b,BLUE,NUM); ws[f'B{r}'].border=THIN; r+=1
put(ws,f'B{r}','TOTAL PROPOSED',BOLD); put(ws,f'C{r}',f'=SUM(C{r0+1}:C{r-1})',BOLD,NUM)
put(ws,f'B{r+2}','Model base case: 448 units Y1, 765 Y2, zero after; absorption 500/yr. Conversion of the proposed roster is governed by the pencil math on 3_Dev_Feasibility.',NOTE,wrap=True)
ws.merge_cells(f'B{r+2}:F{r+3}')

# ================= 9_Sources =================
ws=sheet('9_Sources',[2,50,92])
put(ws,'B2','Sources, Method & Corrections Log',TITLE)
src=[
 ('TMG Seasons model v3','Assumptions, Cash Flow (Annual), S&A, RR 8/4/2026.'),
 ('Prelude Final Model (closed 12/31/25)','Unleveraged; Income & Expense Analysis (full Y1 opex per category); Revenue & Expense (mgmt fee $146,038, EGI $5,841,510, NOI $4,013,692); tax schedule (0.4507% levy, -2%/yr rate drift).'),
 ('Canyon Ridge model at award','$110M; Y1 taxes $987,197 (0.92% levy on 95% x price).'),
 ('Emblem merchant model (7/31/26)','Summary budget; Operating Inputs OI components; A-OperBgt 2031; Tax Calcs.'),
 ('Hawkins LP model + OM','Exec Summary; Development Budget; comps.'),
 ('Ada County Treasurer — 2024 Levy Rates by Tax District / by Tax Code Area','City of Boise 0.4053%; Boise SD#1 0.2797%; City of Meridian 0.2033%; West Ada (Joint SD 2) 0.0332%; Boise code-area totals 0.9059-0.9143%. adacounty.id.gov/treasurer.'),
 ('Idaho State Tax Commission','2025 approved levy rates by county/district (tax.idaho.gov).'),
 ('METHOD — normalization','OI to market actuals component-by-component; taxes closed-form V = NOI-ex-tax/(cap + levy x reassess); exit caps to observed prints. Pencil convention: opex ex-tax + normalized taxes, vacancy 5.87%, cost ex-financing, all escalating 3%/yr.'),
 ('CORRECTIONS LOG','v2: (1) Prelude opex completed from source model. (2) Tax comparability principle corrected — caps comparable across jurisdictions; $/unit is not (v1 had it backwards). (3) Judy Boise levy verified against county records. (4) Exit-cap IRR grid removed (redundant with TMG model); replaced with development-side sensitivities. (5) Pencil convention now uses normalized taxes (v1 used marketed embedded taxes; ~+$20/mo effect).'),
]
r=4
for a,b in src:
    put(ws,f'B{r}',a,BOLD,wrap=True); put(ws,f'C{r}',b,BLACK,wrap=True)
    ws[f'B{r}'].border=THIN; ws[f'C{r}'].border=THIN; r+=1
put(ws,f'B{r+1}','Confidential — internal underwriting work product.',NOTE)

wb.save('Boise_Deals_Normalized_Underwriting_v2.xlsx')
print('saved v2')
