#!/usr/bin/env python3
"""Rent_Chart_Data v2 — monthly T90 grid, CF(Annual) methodology, live formulas."""
import openpyxl, json, datetime, calendar
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from dateutil.relativedelta import relativedelta
wb=openpyxl.Workbook()
F=lambda **k: Font(name="Arial", **{"size":10, **k})
TITLE=F(bold=True,size=13); H1=F(bold=True,color='FFFFFF'); BOLD=F(bold=True)
BLUE=F(color='0000FF'); BLACK=F(); GREEN=F(color='008000'); NOTE=F(italic=True,size=9,color='808080')
HDR=PatternFill('solid',fgColor='1F3864'); SUB=PatternFill('solid',fgColor='D9E2F2'); YEL=PatternFill('solid',fgColor='FFFF00')
M0='$#,##0'; D='mm/dd/yy'; DM='mmm-yy'; NUM='#,##0'
def sheet(n,w):
    ws=wb.create_sheet(n)
    for i,x in enumerate(w,1): ws.column_dimensions[get_column_letter(i)].width=x
    ws.sheet_view.showGridLines=False
    return ws
def put(ws,cell,v,f=BLACK,fmt=None,fill=None,wrap=False):
    c=ws[cell]; c.value=v; c.font=f
    if fmt: c.number_format=fmt
    if fill: c.fill=fill
    if wrap: c.alignment=Alignment(wrap_text=True,vertical='top')
def hdr(ws,row,cols,texts):
    for col,t in zip(cols,texts):
        c=ws[f'{col}{row}']; c.value=t; c.font=H1; c.fill=HDR
        c.alignment=Alignment(horizontal='center',wrap_text=True)

# ---------- load Seasons HD records ----------
import openpyxl as _o
U='/root/.claude/uploads/91c04b01-74f7-505b-b8cb-cd8084223f9d/'
_wb=_o.load_workbook(U+'bec225b3-TMG_Acquisitions_model_7.26___Seasons_at_Meridian_v3.xlsm',read_only=True,data_only=True)
_ws=_wb['HD Dump']
_h=[c.value for c in next(_ws.iter_rows(min_row=1,max_row=1,max_col=25))]
iFP=_h.index('Floorplan Mapped'); iOFF=_h.index('Off Market Date'); iASK=_h.index('Last Asking Rent'); iEFF=_h.index('Last Effective Rent'); iU=_h.index('Unit'); iSF=_h.index('SF')
recs=[]
for row in _ws.iter_rows(min_row=2,max_col=25,values_only=True):
    if row[iFP] and isinstance(row[iOFF],datetime.datetime) and isinstance(row[iASK],(int,float)):
        recs.append((str(row[iFP]),row[iOFF],float(row[iASK]),str(row[iU]),row[iSF],float(row[iEFF])))
_wb.close()

# ---------- load Prelude HD unit-details records (lease-level export 8/13/2026) ----------
import csv as _csv
prel_recs=[]
with open(U+'2d7290f1-hellodataunitdetails20260813.csv') as _f:
    for r_ in _csv.DictReader(_f):
        prel_recs.append((r_['Floorplan'], int(r_['SF']),
                          datetime.datetime.fromisoformat(r_['Off Market Date']),
                          float(r_['Last Asking Rent']), float(r_['Last Effective Rent'])))

months=[]
y,m=2024,7
while (y,m)<=(2026,7):
    months.append(datetime.datetime(y,m,calendar.monthrange(y,m)[1])); m+=1
    if m>12: y,m=y+1,1
months.append(datetime.datetime(2026,8,13))
NP=len(months)

SEA=[("S1_Seas",15,1403.07),("A1_Seas",120,1479.41),("A2_Seas",45,1625.41),("B1_Seas",30,1804.87),("B2_Seas",75,1982.81),("B3a_Seas",15,1933.50),("B3b_Seas",30,1940.67),("C1a_Seas",10,2371.00),("C1b_Seas",20,2236.89)]
PRE=[("1x1-pp",106,1431),("2x2a-pp",100,1733),("2x2b-pp",30,1767),("3x2-pp",44,1984)]

# ---------- HD_Seasons data tab ----------
ws=sheet('HD_Seasons',[2,14,14,14,10,8,16])
put(ws,'B1','Floorplan Mapped',BOLD); put(ws,'C1','Off Market Date',BOLD); put(ws,'D1','Last Asking Rent',BOLD); put(ws,'E1','Unit',BOLD); put(ws,'F1','SF',BOLD); put(ws,'G1','Last Effective Rent',BOLD)
r=2
for fp,off,ask,u,sf,eff in recs:
    put(ws,f'B{r}',fp,BLUE); put(ws,f'C{r}',off,BLUE,D); put(ws,f'D{r}',ask,BLUE,M0); put(ws,f'E{r}',u,BLUE); put(ws,f'F{r}',sf,BLUE,NUM); put(ws,f'G{r}',eff,BLUE,M0)
    r+=1
NSEA=r-1
put(ws,'H1',f'{len(recs)} lease records — Seasons model HD Dump (HDUnitLevel), pull 8/2026',NOTE)

# ---------- HD_Prelude data tab ----------
ws=sheet('HD_Prelude',[2,22,10,14,14,16,16,4,60])
put(ws,'B1','Floorplan (raw)',BOLD,fill=YEL); put(ws,'C1','SF',BOLD,fill=YEL); put(ws,'D1','Off Market Date',BOLD,fill=YEL); put(ws,'E1','Last Asking Rent',BOLD,fill=YEL)
put(ws,'F1','Floorplan Mapped',BOLD); put(ws,'G1','Last Effective Rent',BOLD,fill=YEL)
put(ws,'I1',f'{len(prel_recs)} lease records — Prelude HelloData Unit Details export, pull 8/13/2026. Column F maps floor plan by SF (787/1092/1172/1291). Rows below the data are spare mapping formulas so a refreshed export can be pasted over columns B:E and G.',NOTE,wrap=True)
ws.merge_cells('I1:I8')
r=2
for fp,sf,off,ask,eff in prel_recs:
    put(ws,f'B{r}',fp,BLUE); put(ws,f'C{r}',sf,BLUE,NUM); put(ws,f'D{r}',off,BLUE,D); put(ws,f'E{r}',ask,BLUE,M0); put(ws,f'G{r}',eff,BLUE,M0)
    r+=1
for r in range(2,802):
    put(ws,f'F{r}',f'=IF($C{r}="","",IFERROR(INDEX({{"1x1-pp";"2x2a-pp";"2x2b-pp";"3x2-pp"}},MATCH($C{r},{{787;1092;1172;1291}},0)),""))',BLACK)

# ---------- T90_Monthly ----------
ws=sheet('T90_Monthly',[2,13,8,11]+[10]*NP)
put(ws,'B1','Monthly T90 (trailing-90-day) Mix-Weighted HelloData Asking Rent',TITLE)
put(ws,'B2','Methodology = Seasons model Cash Flow (Annual) rows 252-304: per floor plan, AVERAGEIFS of Last Asking Rent where Off Market Date in [EDATE(month-end,-3)+1, month-end]; if no leases in window, carry forward last value (first column falls back to rent-roll contract rent); property = SUMPRODUCT(plan values x rent-roll unit counts)/total units.',NOTE,wrap=True)
ws.merge_cells('B2:R3')
put(ws,'B4','Month end →',BOLD)
for j,dt in enumerate(months):
    put(ws,f'{get_column_letter(5+j)}4',dt,BOLD,DM if j<NP-1 else D)
put(ws,'B5','SEASONS AT MERIDIAN',BOLD,fill=SUB)
hdr(ws,6,['B','C','D'],['Floor plan','Units','Fallback (contract rent)'])
r=7
for p,u,cr in SEA:
    put(ws,f'B{r}',p); put(ws,f'C{r}',u,BLUE,NUM); put(ws,f'D{r}',cr,BLUE,M0)
    for j in range(NP):
        col=get_column_letter(5+j)
        win=f'HD_Seasons!$C:$C,">="&EDATE({col}$4,-3)+1,HD_Seasons!$C:$C,"<="&{col}$4'
        cnt=f'COUNTIFS(HD_Seasons!$B:$B,$B{r},{win})'
        avg=f'AVERAGEIFS(HD_Seasons!$D:$D,HD_Seasons!$B:$B,$B{r},{win})'
        fb = f'$D{r}' if j==0 else f'{get_column_letter(4+j)}{r}'
        put(ws,f'{col}{r}',f'=IF({cnt}>0,{avg},{fb})',BLACK,M0)
    r+=1
put(ws,f'B{r}','SEASONS T90 MIX-WEIGHTED',BOLD)
for j in range(NP):
    col=get_column_letter(5+j)
    put(ws,f'{col}{r}',f'=SUMPRODUCT({col}7:{col}{r-1},$C7:$C{r-1})/SUM($C7:$C{r-1})',BOLD,M0)
SEAW=r
r+=2
put(ws,f'B{r}','SEASONS AT MERIDIAN — EFFECTIVE RENT (net of concessions; model CF(Annual) rows 321-340 convention, HDUnitLevel[Last Effective Rent])',BOLD,fill=SUB)
hdr(ws,r+1,['B','C','D'],['Floor plan','Units','Fallback (contract rent)'])
r0=r+2; r=r0
for p,u,cr in SEA:
    put(ws,f'B{r}',p); put(ws,f'C{r}',u,BLUE,NUM); put(ws,f'D{r}',cr,BLUE,M0)
    for j in range(NP):
        col=get_column_letter(5+j)
        win=f'HD_Seasons!$C:$C,">="&EDATE({col}$4,-3)+1,HD_Seasons!$C:$C,"<="&{col}$4'
        cnt=f'COUNTIFS(HD_Seasons!$B:$B,$B{r},{win})'
        avg=f'AVERAGEIFS(HD_Seasons!$G:$G,HD_Seasons!$B:$B,$B{r},{win})'
        fb = f'$D{r}' if j==0 else f'{get_column_letter(4+j)}{r}'
        put(ws,f'{col}{r}',f'=IF({cnt}>0,{avg},{fb})',BLACK,M0)
    r+=1
put(ws,f'B{r}','SEASONS EFFECTIVE T90 MIX-WEIGHTED',BOLD)
for j in range(NP):
    col=get_column_letter(5+j)
    put(ws,f'{col}{r}',f'=SUMPRODUCT({col}{r0}:{col}{r-1},$C{r0}:$C{r-1})/SUM($C{r0}:$C{r-1})',BOLD,M0)
SEAEW=r
r+=2
put(ws,f'B{r}','PRELUDE AT PARAMOUNT (HD Unit Details, pull 8/13/2026)',BOLD,fill=SUB)
hdr(ws,r+1,['B','C','D'],['Floor plan','Units','Fallback (RR avg rent)'])
r0=r+2; r=r0
for p,u,cr in PRE:
    put(ws,f'B{r}',p); put(ws,f'C{r}',u,BLUE,NUM); put(ws,f'D{r}',cr,BLUE,M0)
    for j in range(NP):
        col=get_column_letter(5+j)
        win=f'HD_Prelude!$D:$D,">="&EDATE({col}$4,-3)+1,HD_Prelude!$D:$D,"<="&{col}$4'
        cnt=f'COUNTIFS(HD_Prelude!$F:$F,$B{r},{win})'
        avg=f'AVERAGEIFS(HD_Prelude!$E:$E,HD_Prelude!$F:$F,$B{r},{win})'
        fb = f'$D{r}' if j==0 else f'{get_column_letter(4+j)}{r}'
        put(ws,f'{col}{r}',f'=IF({cnt}>0,{avg},{fb})',BLACK,M0)
    r+=1
put(ws,f'B{r}','PRELUDE T90 MIX-WEIGHTED',BOLD)
for j in range(NP):
    col=get_column_letter(5+j)
    put(ws,f'{col}{r}',f'=SUMPRODUCT({col}{r0}:{col}{r-1},$C{r0}:$C{r-1})/SUM($C{r0}:$C{r-1})',BOLD,M0)
PREW=r
r+=2
put(ws,f'B{r}','PRELUDE AT PARAMOUNT — EFFECTIVE RENT (net of concessions; HD Unit Details Last Effective Rent, same methodology)',BOLD,fill=SUB)
hdr(ws,r+1,['B','C','D'],['Floor plan','Units','Fallback (RR avg rent)'])
r0=r+2; r=r0
for p,u,cr in PRE:
    put(ws,f'B{r}',p); put(ws,f'C{r}',u,BLUE,NUM); put(ws,f'D{r}',cr,BLUE,M0)
    for j in range(NP):
        col=get_column_letter(5+j)
        win=f'HD_Prelude!$D:$D,">="&EDATE({col}$4,-3)+1,HD_Prelude!$D:$D,"<="&{col}$4'
        cnt=f'COUNTIFS(HD_Prelude!$F:$F,$B{r},{win})'
        avg=f'AVERAGEIFS(HD_Prelude!$G:$G,HD_Prelude!$F:$F,$B{r},{win})'
        fb = f'$D{r}' if j==0 else f'{get_column_letter(4+j)}{r}'
        put(ws,f'{col}{r}',f'=IF({cnt}>0,{avg},{fb})',BLACK,M0)
    r+=1
put(ws,f'B{r}','PRELUDE EFFECTIVE T90 MIX-WEIGHTED',BOLD)
for j in range(NP):
    col=get_column_letter(5+j)
    put(ws,f'{col}{r}',f'=SUMPRODUCT({col}{r0}:{col}{r-1},$C{r0}:$C{r-1})/SUM($C{r0}:$C{r-1})',BOLD,M0)
PREEW=r
put(ws,f'B{r+1}','Data-status flag (count of Prelude lease records loaded):',NOTE)
put(ws,f'D{r+1}','=COUNT(HD_Prelude!$E3:$E802)',BLACK,NUM)
FLAG=f'T90_Monthly!$D${r+1}'

# ---------- L5_New_Leases (same as v1) ----------
ws=sheet('L5_New_Leases',[2,22,14,14,14,50])
put(ws,'B2','Last-5 New Leases — Seasons model methodology',TITLE)
put(ws,'B3','Per floor plan: average of the 5 most recent new leases (by move-in) from the rent roll; total = SUMPRODUCT(plan L5 avg x units)/total units.',NOTE,wrap=True)
put(ws,'B5','PRELUDE — RR w/ lease charges 8/13/2026',BOLD,fill=SUB)
l5=json.load(open('prelude_l5.json'))
mix={'pprA1':106,'pprB1':100,'pprB2':30,'pprC1':44}
r=6; par={}
for p in ['pprA1','pprB1','pprB2','pprC1']:
    hdr(ws,r,['B','C','D'],[f'{p} — unit','Move-in','Rent'])
    r+=1; first=r
    for d,rent,uid in l5[p]:
        put(ws,f'B{r}',uid); put(ws,f'C{r}',datetime.datetime.strptime(d,'%Y-%m-%d'),BLUE,D); put(ws,f'D{r}',rent,BLUE,M0); r+=1
    put(ws,f'B{r}','L5 avg',BOLD); put(ws,f'D{r}',f'=AVERAGE(D{first}:D{r-1})',BOLD,M0)
    par[p]=r; r+=2
put(ws,f'B{r}','WEIGHTED SUMMARY',BOLD,fill=SUB)
hdr(ws,r+1,['B','C','D'],['Floor plan','Units','L5 avg'])
r0=r+2; r=r0
for p in ['pprA1','pprB1','pprB2','pprC1']:
    put(ws,f'B{r}',p); put(ws,f'C{r}',mix[p],BLUE,NUM); put(ws,f'D{r}',f'=D{par[p]}',GREEN,M0); r+=1
put(ws,f'B{r}','PRELUDE L5 MIX-WEIGHTED',BOLD)
put(ws,f'D{r}',f'=SUMPRODUCT(D{r0}:D{r-1},C{r0}:C{r-1})/SUM(C{r0}:C{r-1})',BOLD,M0)
PL5=r; r+=2
put(ws,f'B{r}','SEASONS — model Assumptions L50:L58',BOLD,fill=SUB)
hdr(ws,r+1,['B','C','D'],['Floor plan','Units','L5 avg'])
sl5=[("S1_Seas",15,1495.8),("A1_Seas",120,1679),("A2_Seas",45,1766.4),("B1_Seas",30,1901.8),("B2_Seas",75,2074),("B3a_Seas",15,2012.4),("B3b_Seas",30,2066.2),("C1a_Seas",10,2497.8),("C1b_Seas",20,2266.4)]
r0=r+2; r=r0
for p,u,v in sl5:
    put(ws,f'B{r}',p); put(ws,f'C{r}',u,BLUE,NUM); put(ws,f'D{r}',v,BLUE,M0); r+=1
put(ws,f'B{r}','SEASONS L5 MIX-WEIGHTED',BOLD)
put(ws,f'D{r}',f'=SUMPRODUCT(D{r0}:D{r-1},C{r0}:C{r-1})/SUM(C{r0}:C{r-1})',BOLD,M0)
SL5=r

# ---------- Chart_Data ----------
ws=sheet('Chart_Data',[2,12,16,17,15,15,16,17,15,15,15,46])
put(ws,'B2','Chart Data — monthly',TITLE)
put(ws,'B3','Green = live formulas (T90_Monthly / L5 tabs). Blue = extracted (models/statements). All T90 series computed from lease-level HelloData on HD_Seasons / HD_Prelude.',NOTE,wrap=True)
hdr(ws,5,['B','C','D','E','F','G','H','I','J','K'],
    ['Date','Seasons T90 asking (mix-wtd)','Seasons T90 effective (mix-wtd)','Seasons UW market rent','Seasons L5 executed (8/4/26)','Prelude T90 asking (mix-wtd)','Prelude T90 effective (mix-wtd)','Prelude UW market rent','Prelude actual in-place','Prelude L5 (acq 12/3/25 + 8/13/26)'])
# UW market rents: QUARTERLY averages at mid-quarter through Y1, ANNUAL averages at UW-year midpoints beyond.
# Seasons: Rent & Occ Data row 5 (updated model, Y1 avg $1,933.28); annual Y2+ from CF(Annual) row 4.
uwS={datetime.datetime(2026,11,30):1902.2,datetime.datetime(2027,2,28):1923.1,datetime.datetime(2027,5,31):1946.2,datetime.datetime(2027,8,31):1961.7,
     datetime.datetime(2028,4,30):2010.6,datetime.datetime(2029,4,30):2091.0,datetime.datetime(2030,4,30):2164.2,datetime.datetime(2031,4,30):2240.0,datetime.datetime(2032,4,30):2307.2}
# Prelude: Market Rent Summary row 11 (Q4-25 anchor + TMG Y1 quarters, Y1 avg $1,729.6); annual 2027+ from Cash Flow row 10 /280/12.
uwP={datetime.datetime(2025,11,30):1693.0,datetime.datetime(2026,2,28):1712.3,datetime.datetime(2026,5,31):1732.2,datetime.datetime(2026,8,31):1745.5,datetime.datetime(2026,11,30):1728.5,
     datetime.datetime(2027,7,1):1775.8,datetime.datetime(2028,7,1):1838.2,datetime.datetime(2029,7,1):1906.7,datetime.datetime(2030,7,1):1976.5,datetime.datetime(2031,7,1):2045.2}
act={datetime.datetime(2026,m,15):v for m,v in zip(range(1,8),[1668,1670,1672,1675,1675,1682,1684])}
PL5ACQ=datetime.datetime(2025,12,3)  # acquisition-era L5: Market Rent Summary V11, RR 12/3/25
alld=sorted(set(months)|set(uwS)|set(uwP)|set(act)|{datetime.datetime(2026,8,4),datetime.datetime(2026,8,13),PL5ACQ})
r=6
for dt in alld:
    put(ws,f'B{r}',dt,BLACK,D)
    if dt in months:
        j=months.index(dt); col=get_column_letter(5+j)
        put(ws,f'C{r}',f'=T90_Monthly!{col}{SEAW}',GREEN,M0)
        put(ws,f'D{r}',f'=T90_Monthly!{col}{SEAEW}',GREEN,M0)
        put(ws,f'G{r}',f'=IF({FLAG}=0,"",T90_Monthly!{col}{PREW})',GREEN,M0)
        put(ws,f'H{r}',f'=IF({FLAG}=0,"",T90_Monthly!{col}{PREEW})',GREEN,M0)
    if dt in uwS: put(ws,f'E{r}',uwS[dt],BLUE,M0)
    if dt in uwP: put(ws,f'I{r}',uwP[dt],BLUE,M0)
    if dt in act: put(ws,f'J{r}',act[dt],BLUE,M0)
    if dt==datetime.datetime(2026,8,4): put(ws,f'F{r}',f'=L5_New_Leases!D{SL5}',GREEN,M0)
    if dt==datetime.datetime(2026,8,13): put(ws,f'K{r}',f'=L5_New_Leases!D{PL5}',GREEN,M0)
    if dt==PL5ACQ: put(ws,f'K{r}',1717.5,BLUE,M0)
    r+=1
put(ws,f'B{r+1}','UW market rents are period AVERAGES: quarterly (calendar quarters, plotted mid-quarter) through Y1, annual (plotted at UW-year midpoints) beyond. Seasons = updated model Rent & Occ Data row 5: TMG Y1 = 4Q26-3Q27 avg $1,933.28, then +4/4/3.5/3.5/3%. Prelude = Market Rent Summary row 11 (Q4-25 anchor + TMG Y1 calendar-2026 quarters, avg $1,729.6), then CF Market Rent /280/12. Seasons L5 marker 8/4/26 = executed new-lease spot. Prelude L5 markers: $1,717.5 at acquisition (Market Rent Summary "L5 New" wtd avg, RR 12/3/25) and $1,810.62 current (RR 8/13/26). Actuals: potential rent net LTL /280 from accrual statement.',NOTE,wrap=True)
ws.merge_cells(f'B{r+1}:L{r+2}')

del wb['Sheet']
wb.move_sheet('Chart_Data',offset=-4)
wb.move_sheet('T90_Monthly',offset=-3)
wb.save('Rent_Chart_Data.xlsx')
print('saved v2, months:',NP)
