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
iFP=_h.index('Floorplan Mapped'); iOFF=_h.index('Off Market Date'); iASK=_h.index('Last Asking Rent'); iU=_h.index('Unit'); iSF=_h.index('SF')
recs=[]
for row in _ws.iter_rows(min_row=2,max_col=25,values_only=True):
    if row[iFP] and isinstance(row[iOFF],datetime.datetime) and isinstance(row[iASK],(int,float)):
        recs.append((str(row[iFP]),row[iOFF],float(row[iASK]),str(row[iU]),row[iSF]))
_wb.close()

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
ws=sheet('HD_Seasons',[2,14,14,14,10,8])
put(ws,'B1','Floorplan Mapped',BOLD); put(ws,'C1','Off Market Date',BOLD); put(ws,'D1','Last Asking Rent',BOLD); put(ws,'E1','Unit',BOLD); put(ws,'F1','SF',BOLD)
r=2
for fp,off,ask,u,sf in recs:
    put(ws,f'B{r}',fp,BLUE); put(ws,f'C{r}',off,BLUE,D); put(ws,f'D{r}',ask,BLUE,M0); put(ws,f'E{r}',u,BLUE); put(ws,f'F{r}',sf,BLUE,NUM)
    r+=1
NSEA=r-1
put(ws,'H1',f'{len(recs)} lease records — Seasons model HD Dump (HDUnitLevel), pull 8/2026',NOTE)

# ---------- HD_Prelude paste tab ----------
ws=sheet('HD_Prelude',[2,22,10,14,14,16,4,60])
put(ws,'B1','Floorplan (raw)',BOLD,fill=YEL); put(ws,'C1','SF',BOLD,fill=YEL); put(ws,'D1','Off Market Date',BOLD,fill=YEL); put(ws,'E1','Last Asking Rent',BOLD,fill=YEL)
put(ws,'F1','Floorplan Mapped',BOLD)
put(ws,'H1','PASTE the Prelude HelloData UNIT DETAILS export (lease-level) into columns B:E starting row 2 — floorplan, SF, off-market date, last asking rent. Column F maps by SF (787/1092/1172/1291). The T90_Monthly Prelude grid and Chart_Data populate automatically. The unit-TYPE table export (aggregates) cannot be used — it has no dates.',NOTE,wrap=True)
ws.merge_cells('H1:H8')
put(ws,'B2','example: A1- 1 Bedroom 1 Bath',NOTE); put(ws,'C2','787',NOTE); put(ws,'D2','01/15/26',NOTE); put(ws,'E2','1,450',NOTE)
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
put(ws,f'B{r}','PRELUDE AT PARAMOUNT (populates when Unit Details pasted on HD_Prelude)',BOLD,fill=SUB)
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
put(ws,f'B{r+1}','Data-status flag (0 = no Prelude unit details pasted yet):',NOTE)
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
ws=sheet('Chart_Data',[2,12,16,15,15,16,15,15,15,46])
put(ws,'B2','Chart Data — monthly',TITLE)
put(ws,'B3','Green = live formulas (T90_Monthly / L5 tabs). Blue = extracted (models/statements). Prelude T90 column stays blank until the Unit Details export is pasted on HD_Prelude.',NOTE,wrap=True)
hdr(ws,5,['B','C','D','E','F','G','H','I'],
    ['Date','Seasons T90 (mix-wtd)','Seasons UW asking','Seasons L5 / UW entry','Prelude T90 (mix-wtd)','Prelude UW rent/occ','Prelude actual in-place','Prelude L5 (8/13/26)'])
uwS={datetime.datetime(2026,8,4):1885,datetime.datetime(2027,11,1):1960,datetime.datetime(2028,11,1):2038,datetime.datetime(2029,11,1):2110,datetime.datetime(2030,11,1):2184,datetime.datetime(2031,11,1):2249}
uwP={datetime.datetime(2026,7,1):1668,datetime.datetime(2027,7,1):1745,datetime.datetime(2028,7,1):1808,datetime.datetime(2029,7,1):1883,datetime.datetime(2030,7,1):1952}
act={datetime.datetime(2026,m,15):v for m,v in zip(range(1,8),[1668,1670,1672,1675,1675,1682,1684])}
alld=sorted(set(months)|set(uwS)|set(uwP)|set(act)|{datetime.datetime(2026,8,13)})
r=6
for dt in alld:
    put(ws,f'B{r}',dt,BLACK,D)
    if dt in months:
        j=months.index(dt); col=get_column_letter(5+j)
        put(ws,f'C{r}',f'=T90_Monthly!{col}{SEAW}',GREEN,M0)
        put(ws,f'F{r}',f'=IF({FLAG}=0,"",T90_Monthly!{col}{PREW})',GREEN,M0)
    if dt in uwS: put(ws,f'D{r}',uwS[dt],BLUE,M0)
    if dt in uwP: put(ws,f'G{r}',uwP[dt],BLUE,M0)
    if dt in act: put(ws,f'H{r}',act[dt],BLUE,M0)
    if dt==datetime.datetime(2026,8,4): put(ws,f'E{r}',f'=L5_New_Leases!D{SL5}',GREEN,M0)
    if dt==datetime.datetime(2026,8,13): put(ws,f'I{r}',f'=L5_New_Leases!D{PL5}',GREEN,M0)
    r+=1
put(ws,f'B{r+1}','Seasons UW path: $1,885 (executed L5, flat through Y1) then annual steps +4/4/3.5/3.5/3% each Nov. Prelude UW: rent/occupied path from acquisition model. Actuals: potential rent net LTL /280 from accrual statement.',NOTE,wrap=True)
ws.merge_cells(f'B{r+1}:J{r+2}')

del wb['Sheet']
wb.move_sheet('Chart_Data',offset=-4)
wb.move_sheet('T90_Monthly',offset=-3)
wb.save('Rent_Chart_Data.xlsx')
print('saved v2, months:',NP)
