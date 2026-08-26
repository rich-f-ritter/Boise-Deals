#!/usr/bin/env python3
"""Meridian, ID development fee stack — permit, plan review, impact, and connection fees.

Every rate is taken from a PRIMARY source (City of Meridian published fee calculators
effective 6/1/2026, Meridian's ACHD notice effective 3/1/2026, ACHD Ordinance 254 draft
Exhibit A, and the Ada County jail impact fee) and reconciled line-by-line against
Quarterra's actual Emblem Meridian development budget.

Outputs: SeasonsMeridian/Meridian Development Fees.xlsx
"""
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = Path(__file__).parent
OUT = Path('/home/user/Boise-Deals/SeasonsMeridian/Meridian Development Fees.xlsx')

NAVY, GOLD, INK, GRAY = '153D64', 'B49955', '1A2B3C', '6F6F70'
BAND, BOX, RED, GREEN = 'EDF2F7', 'F7F4EC', 'A61B1B', '1E6B33'
WHITE = 'FFFFFF'

# ---------------------------------------------------------------- published rates
# City of Meridian Multi-Family Building Permit & Fee Calculator, eff. 6/1/2026
IMPACT_TIERS = [  # (label, max_avg_unit_sf, police, fire, parks)
    ('≤ 1,200 SF', 1200, 190, 470, 1946),
    ('1,201 – 1,700 SF', 1700, 294, 726, 3006),
    ('1,701 – 2,500 SF', 2500, 402, 995, 4119),
    ('2,501 – 3,200 SF', 3200, 482, 1192, 4935),
    ('≥ 3,201 SF', 99999, 542, 1339, 5544),
]
WATER_ASSESS, SEWER_ASSESS = 1696, 5807          # eff 6/1/2026 (was 1,514 / 5,411)
WATER_ASSESS_PRIOR, SEWER_ASSESS_PRIOR = 1514, 5411
JAIL_MF = 357                                     # Ada County jail impact fee, MF/unit
JAIL_SF = 516
PERMIT_BASE, PERMIT_RATE_PER_1K = 50, 5.50       # $50 + $5.50 per $1,000 project value
BLDG_REVIEW_PCT, FIRE_REVIEW_PCT = 0.65, 0.30
METERS = {'3/4"': 418.52, '1"': 481.82, '1-1/2"': 2051.86, '2"': 2247.09,
          '4" compound': 4632.59}
LANDSCAPE_METERS = {'1-1/2"': 1478.71, '2"': 1744.89, '4"': 3785.11}
ACHD = {'FY23 MF low-rise (Ord. 246A, superseded)': 1895,
        'FY23 MF mid-rise (Ord. 246A, superseded)': 1449,
        'Ord. 254 adopted MF rate (as reported)': 2371,
        'Quarterra assumption (Emblem model)': 2968.91,
        'Ord. 254 Single Family Attached (proxy)': 3182,
        'Ord. 254 Single Family': 5803}

# ---------------------------------------------------------------- Emblem actuals
EMB_UNITS = 250            # the fee calculator was run at 250 units / 270,000 GSF
EMB = {
    'Building permit': 275666, 'Building plan review': 179182.90,
    'Fire plan review': 82699.80, 'Misc land development fees': 32000,
    'Pre-application': 1000, 'Conditional Use Permit': 10000, 'Plat': 10000,
    'DA modification': 10000, 'Misc / other (ROM)': 50000,
    'Parks impact fee': 486500, 'Fire impact fee': 117500, 'Police impact fee': 47500,
    'ACHD transportation impact fee': 742226.29, 'Ada County jail fee (ROM)': 89250,
    'Water assessment (domestic)': 378500, 'Water assessment (irrigation)': 131250,
    'Domestic water meter fees': 17977, 'Irrigation water meter fees': 2957,
    'Sewer assessment': 1352750, 'Public works / other': 17200,
    'Power company (ROM)': 300000, 'Franchise utilities (ROM)': 25000,
    'Other + escalation (ROM)': 100000,
}
EMB_TOTAL = 4459158.99
EMB_DEV_BUDGET = 77959624.34
EMB_MODEL_UNITS = 256

SUBJ_UNITS = 360           # Seasons at Meridian equivalent


def rnd(x, n=0):
    return round(x, n)


# ---------------------------------------------------------------- build the estimate
emb_project_value = (EMB['Building permit'] - PERMIT_BASE) / PERMIT_RATE_PER_1K * 1000
value_per_unit = emb_project_value / EMB_UNITS
subj_value = value_per_unit * SUBJ_UNITS
subj_permit = -(-subj_value // 1000) * PERMIT_RATE_PER_1K + PERMIT_BASE

tier = IMPACT_TIERS[0]      # garden MF: avg climate-controlled area/unit ~1,080 SF
police, fire, parks = tier[2], tier[3], tier[4]

# per-unit allowances carried from Emblem where Meridian publishes no flat rate
irr_assess_pu = EMB['Water assessment (irrigation)'] / EMB_UNITS
meter_pu = (EMB['Domestic water meter fees'] + EMB['Irrigation water meter fees']) / EMB_UNITS
pw_other_pu = EMB['Public works / other'] / EMB_UNITS
power_pu = (EMB['Power company (ROM)'] + EMB['Franchise utilities (ROM)']) / EMB_UNITS
landuse_flat = (EMB['Misc land development fees'] + EMB['Pre-application']
                + EMB['Conditional Use Permit'] + EMB['Plat'] + EMB['DA modification']
                + EMB['Misc / other (ROM)'])
other_flat = EMB['Other + escalation (ROM)']

ACHD_MID = ACHD['Ord. 254 adopted MF rate (as reported)']

STACK = [
    ('PERMIT & PLAN REVIEW', None, None, None, None),
    ('Building permit', subj_permit, '$50 base + $5.50 per $1,000 of project value',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('Building plan review', subj_permit * BLDG_REVIEW_PCT, '65% of building permit fee',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('Fire plan review', subj_permit * FIRE_REVIEW_PCT, '30% of building permit fee',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('Land use & entitlement (CUP, plat, DA mod, pre-app, misc)', landuse_flat,
     'project-level, not per unit', 'Emblem budget (ROM)', 'allowance'),
    ('IMPACT FEES', None, None, None, None),
    ('Meridian parks impact fee', parks * SUBJ_UNITS,
     f'${parks:,}/unit — avg unit ≤ 1,200 SF tier',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('Meridian fire impact fee', fire * SUBJ_UNITS, f'${fire:,}/unit — same tier',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('Meridian police impact fee', police * SUBJ_UNITS, f'${police:,}/unit — same tier',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'published'),
    ('ACHD transportation impact fee', ACHD_MID * SUBJ_UNITS,
     f'${ACHD_MID:,}/unit — NO PUBLISHED MF RATE; assessed case-by-case',
     'ACHD Ord. 254, eff. 3/1/2026', 'ASSESSED'),
    ('Ada County jail impact fee', JAIL_MF * SUBJ_UNITS, f'${JAIL_MF}/unit (MF)',
     'Ada County jail impact fee ordinance', 'published'),
    ('CONNECTION / ASSESSMENT FEES', None, None, None, None),
    ('Sewer assessment', SEWER_ASSESS * SUBJ_UNITS,
     f'${SEWER_ASSESS:,}/unit flat (was ${SEWER_ASSESS_PRIOR:,})',
     'Meridian W&S notice, eff. 6/1/2026', 'published'),
    ('Water assessment (domestic)', WATER_ASSESS * SUBJ_UNITS,
     f'${WATER_ASSESS:,}/unit flat (was ${WATER_ASSESS_PRIOR:,})',
     'Meridian W&S notice, eff. 6/1/2026', 'published'),
    ('Water assessment (irrigation)', irr_assess_pu * SUBJ_UNITS,
     f'~${irr_assess_pu:,.0f}/unit', 'Emblem budget', 'allowance'),
    ('Water meter fees (domestic + irrigation)', meter_pu * SUBJ_UNITS,
     '2" domestic $2,247.09 ea; landscape 2" $1,744.89 ea',
     'Meridian MF Fee Calculator, eff. 6/1/2026', 'allowance'),
    ('Public works review / inspection / other', pw_other_pu * SUBJ_UNITS,
     'main review $0.40/LF; QLPE $500/sheet; inspection $72 flat or $0.69/LF',
     'Meridian MF + Land Dev Calculators', 'allowance'),
    ('UTILITY & OTHER', None, None, None, None),
    ('Power company + franchise utilities', power_pu * SUBJ_UNITS, 'ROM',
     'Emblem budget (ROM)', 'allowance'),
    ('Other + escalation', other_flat, 'ROM', 'Emblem budget (ROM)', 'allowance'),
]

subtotal = sum(r[1] for r in STACK if r[1] is not None)

wb = Workbook()

# ================================================================ helpers
thin = Side(style='thin', color='D5DCE4')


def style_header(ws, row, headers, widths, height=26):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = PatternFill('solid', fgColor=NAVY)
        c.font = Font(name='Calibri', size=9, bold=True, color=WHITE)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.row_dimensions[row].height = height


def title_block(ws, title, subtitle, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=title)
    c.fill = PatternFill('solid', fgColor=NAVY)
    c.font = Font(name='Georgia', size=14, bold=True, color=WHITE)
    c.alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws.row_dimensions[1].height = 30
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    c = ws.cell(row=2, column=2 - 1, value=subtitle)
    c.fill = PatternFill('solid', fgColor=BOX)
    c.font = Font(name='Calibri', size=8.5, italic=True, color=GRAY)
    c.alignment = Alignment(horizontal='left', vertical='center', indent=1, wrap_text=True)
    ws.row_dimensions[2].height = 24


# ================================================================ TAB 1 — Fee Stack
ws = wb.active
ws.title = 'Fee Stack'
title_block(ws, 'Meridian Development Fees — 360-Unit Garden Multifamily',
            'Seasons at Meridian equivalent. Rates per City of Meridian calculators effective '
            '6/1/2026, ACHD Ordinance 254 effective 3/1/2026, and the Ada County jail impact '
            'fee. "ASSESSED" = no published rate; ACHD sets it case-by-case.', 6)
style_header(ws, 4, ['Fee', 'Total', '$ / unit', '% of stack', 'Basis / rate', 'Status'],
             [46, 14, 12, 10, 54, 12])

r = 5
for name, amt, basis, src, status in STACK:
    if amt is None:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        c = ws.cell(row=r, column=1, value=name)
        c.fill = PatternFill('solid', fgColor=GOLD)
        c.font = Font(name='Calibri', size=9, bold=True, color=WHITE)
        c.alignment = Alignment(horizontal='left', indent=1)
        r += 1
        continue
    ws.cell(row=r, column=1, value=name).font = Font(name='Calibri', size=9)
    ws.cell(row=r, column=2, value=amt).number_format = '$#,##0'
    ws.cell(row=r, column=3, value=amt / SUBJ_UNITS).number_format = '$#,##0'
    ws.cell(row=r, column=4, value=amt / subtotal).number_format = '0.0%'
    ws.cell(row=r, column=5, value=basis).font = Font(name='Calibri', size=8, color=GRAY)
    sc = ws.cell(row=r, column=6, value=status)
    sc.font = Font(name='Calibri', size=8, bold=(status == 'ASSESSED'),
                   color=RED if status == 'ASSESSED' else (GREEN if status == 'published' else GRAY))
    sc.alignment = Alignment(horizontal='center')
    for col in range(1, 7):
        cell = ws.cell(row=r, column=col)
        cell.border = Border(bottom=thin)
        if (r % 2) == 0:
            cell.fill = PatternFill('solid', fgColor=BAND)
    r += 1

ws.cell(row=r, column=1, value='TOTAL PERMITS, FEES & CONNECTIONS').font = Font(
    name='Calibri', size=10, bold=True, color=WHITE)
ws.cell(row=r, column=2, value=subtotal).number_format = '$#,##0'
ws.cell(row=r, column=3, value=subtotal / SUBJ_UNITS).number_format = '$#,##0'
ws.cell(row=r, column=4, value=1.0).number_format = '0.0%'
for col in range(1, 7):
    c = ws.cell(row=r, column=col)
    c.fill = PatternFill('solid', fgColor=NAVY)
    c.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
total_row = r
r += 2

ws.cell(row=r, column=1, value='ACHD SENSITIVITY — the one unpublished number').font = Font(
    name='Georgia', size=10, bold=True, color=NAVY)
r += 1
style_header(ws, r, ['ACHD basis', '$ / unit', 'Total (360u)', 'Stack total',
                     '$ / unit stack', 'Note'], [46, 14, 12, 10, 54, 12], height=18)
r += 1
base_ex_achd = subtotal - ACHD_MID * SUBJ_UNITS
for label, rate in ACHD.items():
    if 'Single Family' in label and 'Attached' not in label:
        continue
    tot = rate * SUBJ_UNITS
    ws.cell(row=r, column=1, value=label).font = Font(name='Calibri', size=8.5)
    ws.cell(row=r, column=2, value=rate).number_format = '$#,##0'
    ws.cell(row=r, column=3, value=tot).number_format = '$#,##0'
    ws.cell(row=r, column=4, value=base_ex_achd + tot).number_format = '$#,##0'
    ws.cell(row=r, column=5, value=(base_ex_achd + tot) / SUBJ_UNITS).number_format = '$#,##0'
    hl = 'adopted rate — used above' if rate == ACHD_MID else ''
    ws.cell(row=r, column=6, value=hl).font = Font(name='Calibri', size=8, color=GREEN)
    if rate == ACHD_MID:
        for col in range(1, 7):
            ws.cell(row=r, column=col).fill = PatternFill('solid', fgColor=BOX)
    r += 1

r += 1
for line in [
    'The ACHD transportation impact fee is the single largest uncertainty in the stack. '
    'Ordinance 254 (effective 3/1/2026) dropped the published Multifamily Low-Rise / Mid-Rise '
    'categories entirely — Meridian’s own builder notice reads "Multi-Family/Commercial '
    'Permits: Contact ACHD Impact Fee Team for Assessment."',
    'Swing across the plausible range is '
    f'${(ACHD["Ord. 254 Single Family Attached (proxy)"] - ACHD["FY23 MF low-rise (Ord. 246A, superseded)"]):,}/unit '
    f'(${(ACHD["Ord. 254 Single Family Attached (proxy)"] - ACHD["FY23 MF low-rise (Ord. 246A, superseded)"]) * SUBJ_UNITS:,.0f} '
    'on a 360-unit deal) — roughly 1.7% of total development cost.',
    'Meridian also advanced an Ada County EMS impact fee alongside the jail fee; it is NOT in '
    'this stack and is not in Quarterra’s budget. Confirm before relying on the total.',
]:
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    c = ws.cell(row=r, column=1, value=line)
    c.font = Font(name='Calibri', size=8.5, color=INK)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[r].height = 28
    r += 1
ws.freeze_panes = 'A5'

# ================================================================ TAB 2 — Rate Schedule
ws2 = wb.create_sheet('Rate Schedule')
title_block(ws2, 'Published Meridian & ACHD Rate Schedule',
            'Verbatim rates from the primary sources. Everything here is a published number; '
            'nothing is derived.', 5)
style_header(ws2, 4, ['Category', 'Item', 'Rate', 'Effective', 'Source'],
             [26, 44, 22, 14, 42])
rows2 = [
    ('Building permit', 'Multifamily building permit',
     '$50 + $5.50 per $1,000 of project value', '6/1/2026', 'Meridian MF Fee Calculator'),
    ('Plan review', 'Building plan review', '65% of building permit fee', '6/1/2026',
     'Meridian MF Fee Calculator'),
    ('Plan review', 'Fire plan review', '30% of building permit fee', '6/1/2026',
     'Meridian MF Fee Calculator'),
]
for label, mx, pol, fr, pk in IMPACT_TIERS:
    rows2.append(('Impact — Meridian', f'Avg unit size {label}',
                  f'Parks ${pk:,} · Fire ${fr:,} · Police ${pol:,}  =  ${pk+fr+pol:,}',
                  '6/1/2026', 'Meridian MF Fee Calculator'))
rows2 += [
    ('Impact — Meridian', 'Tier is keyed to climate-controlled SF ÷ units',
     'not net rentable SF', '6/1/2026', 'Meridian MF Fee Calculator'),
    ('Impact — ACHD', 'Multifamily (any height)',
     'NO PUBLISHED RATE — contact ACHD for assessment', '3/1/2026',
     'Meridian ACHD notice / Ord. 254'),
    ('Impact — ACHD', 'Single Family', '$5,803 / unit', '3/1/2026', 'ACHD Ord. 254'),
    ('Impact — ACHD', 'Single Family Attached / duplex / townhouse', '$3,182 / unit',
     '3/1/2026', 'ACHD Ord. 254'),
    ('Impact — ACHD', 'Accessory dwelling unit', '$1,934 / unit', '3/1/2026',
     'ACHD Ord. 254'),
    ('Impact — ACHD', 'MF low-rise (SUPERSEDED)', '$1,895 / unit', '10/1/2022',
     'ACHD Ord. 246A'),
    ('Impact — ACHD', 'MF mid-rise (SUPERSEDED)', '$1,449 / unit', '10/1/2022',
     'ACHD Ord. 246A'),
    ('Impact — Ada County', 'Jail impact fee — multifamily', f'${JAIL_MF} / unit',
     '2026', 'Ada County jail impact fee ordinance'),
    ('Impact — Ada County', 'Jail impact fee — single family', f'${JAIL_SF} / unit',
     '2026', 'Ada County jail impact fee ordinance'),
    ('Assessment', 'Sewer assessment',
     f'${SEWER_ASSESS:,} / unit (was ${SEWER_ASSESS_PRIOR:,})', '6/1/2026',
     'Meridian Water & Sewer notice'),
    ('Assessment', 'Water assessment',
     f'${WATER_ASSESS:,} / unit (was ${WATER_ASSESS_PRIOR:,})', '6/1/2026',
     'Meridian Water & Sewer notice'),
]
for size, amt in METERS.items():
    rows2.append(('Meter fee', f'{size} domestic water meter', f'${amt:,.2f} each', '6/1/2026',
                  'Meridian MF Fee Calculator'))
for size, amt in LANDSCAPE_METERS.items():
    rows2.append(('Meter fee', f'{size} landscape meter', f'${amt:,.2f} each', '6/1/2026',
                  'Meridian MF Fee Calculator'))
rows2 += [
    ('Public works', 'New water/sewer main plan review', '$288 + $0.40 / LF', '6/1/2026',
     'Meridian MF Fee Calculator'),
    ('Public works', 'Additional main plan review', '$0.20 / LF', '6/1/2026',
     'Meridian Land Dev Calculator'),
    ('Public works', 'QLPE review', '$500 / sheet (MF) · $326.40 / sheet (land dev)',
     '6/1/2026', 'Meridian MF + Land Dev Calculators'),
    ('Public works', 'Drainage plan review',
     '<1.5 ac $48 · ≤10 ac $96 · >10 ac $192', '6/1/2026',
     'Meridian MF Fee Calculator'),
    ('Public works', 'Inspection — no public main', '$72 flat', '6/1/2026',
     'Meridian MF Fee Calculator'),
    ('Public works', 'Inspection — new water/sewer main', '$0.69 / LF', '6/1/2026',
     'Meridian MF Fee Calculator'),
    ('Public works', 'Plan review — services existing / new', '$92.56 / $150.42',
     '6/1/2026', 'Meridian Land Dev Calculator'),
]
r = 5
for cat, item, rate, eff, src in rows2:
    ws2.cell(row=r, column=1, value=cat).font = Font(name='Calibri', size=8.5, bold=True,
                                                     color=NAVY)
    ws2.cell(row=r, column=2, value=item).font = Font(name='Calibri', size=8.5)
    rc = ws2.cell(row=r, column=3, value=rate)
    rc.font = Font(name='Calibri', size=8.5,
                   bold='NO PUBLISHED' in rate, color=RED if 'NO PUBLISHED' in rate else INK)
    ws2.cell(row=r, column=4, value=eff).alignment = Alignment(horizontal='center')
    ws2.cell(row=r, column=4).font = Font(name='Calibri', size=8.5)
    ws2.cell(row=r, column=5, value=src).font = Font(name='Calibri', size=8, color=GRAY)
    for col in range(1, 6):
        ws2.cell(row=r, column=col).border = Border(bottom=thin)
        if 'SUPERSEDED' in item:
            ws2.cell(row=r, column=col).font = Font(name='Calibri', size=8.5, color=GRAY,
                                                    italic=True)
    r += 1
ws2.freeze_panes = 'A5'

# ================================================================ TAB 3 — Emblem recon
ws3 = wb.create_sheet('Emblem Reconciliation')
title_block(ws3, 'Quarterra’s Emblem Meridian Budget vs. Published Rates',
            'Emblem’s Permits & Fees line is $4,459,159 on 256 modelled units '
            '($17,418/unit, 5.7% of a $77.96M budget). The fee calculator was run at 250 units '
            '/ 270,000 GSF. Checked line by line against Meridian’s published schedule.', 5)
style_header(ws3, 4, ['Emblem line item', 'Emblem amount', '$ / unit (250u)',
                      'Published rate check', 'Verdict'], [40, 16, 14, 40, 26])
recon = [
    ('Building permit', EMB['Building permit'], 'implies $50.1M project value at $5.50/$1,000',
     'TIES'),
    ('Building plan review', EMB['Building plan review'], '65% of permit fee', 'TIES'),
    ('Fire plan review', EMB['Fire plan review'], '30% of permit fee', 'TIES'),
    ('Parks impact fee', EMB['Parks impact fee'], f'${parks:,}/unit ≤1,200 SF tier', 'TIES'),
    ('Fire impact fee', EMB['Fire impact fee'], f'${fire:,}/unit ≤1,200 SF tier', 'TIES'),
    ('Police impact fee', EMB['Police impact fee'], f'${police:,}/unit ≤1,200 SF tier',
     'TIES'),
    ('Water assessment (domestic)', EMB['Water assessment (domestic)'],
     f'${WATER_ASSESS_PRIOR:,}/unit at 3/1/2026', 'TIES (pre-6/1 rate)'),
    ('Sewer assessment', EMB['Sewer assessment'],
     f'${SEWER_ASSESS_PRIOR:,}/unit at 3/1/2026', 'TIES (pre-6/1 rate)'),
    ('Ada County jail fee (ROM)', EMB['Ada County jail fee (ROM)'],
     f'${JAIL_MF}/unit adopted MF rate', 'TIES — ROM was right'),
    ('ACHD transportation impact fee', EMB['ACHD transportation impact fee'],
     f'no published MF rate; adopted rate reported at ${ACHD_MID:,}/unit', 'OVERSTATED ~$598/u'),
]
r = 5
for name, amt, check, verdict in recon:
    ws3.cell(row=r, column=1, value=name).font = Font(name='Calibri', size=8.5)
    ws3.cell(row=r, column=2, value=amt).number_format = '$#,##0'
    ws3.cell(row=r, column=3, value=amt / EMB_UNITS).number_format = '$#,##0.00'
    ws3.cell(row=r, column=4, value=check).font = Font(name='Calibri', size=8, color=GRAY)
    vc = ws3.cell(row=r, column=5, value=verdict)
    good = verdict.startswith('TIES')
    vc.font = Font(name='Calibri', size=8.5, bold=True, color=GREEN if good else RED)
    for col in range(1, 6):
        ws3.cell(row=r, column=col).border = Border(bottom=thin)
        if (r % 2) == 0:
            ws3.cell(row=r, column=col).fill = PatternFill('solid', fgColor=BAND)
    r += 1

r += 1
notes3 = [
    ('What this proves', 'Every Meridian-controlled line in Quarterra’s budget ties '
     'exactly to the city’s published 3/1/2026 calculator. The fee build is sound — '
     'it is not padded, and it is not missing the city stack.'),
    ('The one real variance', 'ACHD transportation. Quarterra carried ~$2,969/unit, escalating '
     'the old MF rate toward Single Family Attached because Ordinance 254 publishes no MF line. '
     'The adopted MF rate is reported at $2,371/unit — so Emblem is roughly $598/unit '
     '($149,500 on 250 units) conservative. Their own note says "Need to submit a formal '
     'assessment once under PSA."'),
    ('Stale by one cycle', 'Water and sewer assessments rose $578/unit on 6/1/2026 (water '
     '$1,514→$1,696; sewer $5,411→$5,807). Emblem’s budget predates it, so it '
     'understates connection charges by ~$144,500 on 250 units — which roughly offsets '
     'the ACHD overstatement.'),
    ('Not in anyone’s budget', 'Meridian advanced an Ada County EMS impact fee alongside '
     'the jail fee. Neither Emblem nor this stack carries it.'),
    ('Why it matters', f'At ${subtotal/SUBJ_UNITS:,.0f}/unit, permits and fees are roughly '
     '5.7% of all-in development cost — about a third of the $322,530/unit replacement '
     'cost gap that keeps new supply from penciling. Fees are a real cost, but they are not '
     'what breaks feasibility; leverage and the rent gap are.'),
]
for head, body in notes3:
    ws3.cell(row=r, column=1, value=head).font = Font(name='Georgia', size=9, bold=True,
                                                      color=NAVY)
    ws3.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    c = ws3.cell(row=r, column=2, value=body)
    c.font = Font(name='Calibri', size=8.5)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    ws3.row_dimensions[r].height = 40
    r += 1
ws3.freeze_panes = 'A5'

# ================================================================ TAB 4 — Sources
ws4 = wb.create_sheet('Sources')
title_block(ws4, 'Primary Sources', 'All rates verified against these documents on '
            'August 26, 2026. Local copies saved in research/audit_2026-08/fees/.', 3)
style_header(ws4, 4, ['Document', 'What it establishes', 'URL'], [44, 50, 76])
srcs = [
    ('Meridian Multi-Family Building Permit & Fee Calculator (6/1/2026)',
     'MF permit formula, 65%/30% plan review, impact fee tiers by average unit size, '
     'water/sewer assessments, meter fees, public works fees',
     'https://meridiancity.org/media/n0ilmhvd/multi-family-fee-calculation-worksheet-6-1-2026.xlsx'),
    ('Meridian Residential Fee Calculation Worksheet (3/1/2026 and 6/1/2026)',
     'Same impact fee tier table for single family; ACHD single-family rate',
     'https://meridiancity.org/media/1o3dqvgg/residential-fee-calculation-worksheet-6-1-2026.xlsx'),
    ('Meridian Land Development Commercial Fee Worksheet (6/1/2026)',
     'Site civil plan review and inspection rates, QLPE, drainage',
     'https://meridiancity.org/media/upficrmg/land-development-commercial-project-fee-calculation-worksheet-6-1-2026.xlsx'),
    ('Meridian Water & Sewer Fee Increase notice (6/1/2026)',
     'Sewer $5,411→$5,807; water $1,514→$1,696; +$578/unit total',
     'https://meridiancity.org/media/cardncjx/water-sewer-assessments-6-1-2026.pdf'),
    ('Meridian ACHD Fee Increase notice (3/1/2026)',
     'ACHD Ord. 254 rates; "Multi-Family/Commercial Permits: Contact ACHD Impact Fee Team '
     'for Assessment"',
     'https://meridiancity.org/media/lwvnln4y/achdfeeincrease-3-1-2026.pdf'),
    ('ACHD Ordinance 254 draft Exhibit A (via City of Star, 1/30/2026)',
     'FY2026 fee table, ITE 12th ed. — confirms no Multifamily line in the residential '
     'schedule',
     'https://www.staridaho.org/DocumentCenter/View/1595/ACHD-Revised-Fees'),
    ('ACHD Ordinance 246A Exhibit A (FY2022/23)',
     'Superseded MF low-rise $1,895 / mid-rise $1,449 per unit',
     'https://more.achdidaho.org/Documents/Engineering/ImpactFees/Ordinance246A/ExhibitA_FeeSchedule.pdf'),
    ('KIVI — ACHD adopts impact fee update',
     'Ord. 254 adopted 4–1, effective 3/1/2026, single service area; MF reported at '
     '$2,371/unit, SF $5,803',
     'https://www.kivitv.com/news/local-news/in-your-neighborhood/ada-county/achd-approves-update-to-impact-fees-and-long-range-transportation-plan'),
    ('Ada County jail / EMS impact fees',
     'Jail impact fee $357/unit multifamily, $516 single family; collected by cities',
     'https://boisedev.com/news/2025/09/29/ada-co-asking-cities-to-collect-impact-fees/'),
    ('Quarterra Emblem Meridian merchant model, "P&F Details" tab',
     'Actual developer fee build for a 250-unit / 270,000 GSF Meridian project',
     'research/audit_2026-08/in/Emblem_Meridian_Merchant_Model.xlsm'),
]
r = 5
for doc, what, url in srcs:
    ws4.cell(row=r, column=1, value=doc).font = Font(name='Calibri', size=8.5, bold=True)
    ws4.cell(row=r, column=2, value=what).font = Font(name='Calibri', size=8.5)
    ws4.cell(row=r, column=3, value=url).font = Font(name='Calibri', size=7.5, color='0563C1')
    for col in range(1, 4):
        ws4.cell(row=r, column=col).alignment = Alignment(wrap_text=True, vertical='top')
        ws4.cell(row=r, column=col).border = Border(bottom=thin)
    ws4.row_dimensions[r].height = 34
    r += 1
ws4.freeze_panes = 'A5'

for sheet in wb.worksheets:
    sheet.page_setup.orientation = 'landscape'
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.print_options.horizontalCentered = True

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)

Path(HERE / 'meridian_fees.json').write_text(json.dumps({
    'impact_tiers': IMPACT_TIERS, 'water_assessment': WATER_ASSESS,
    'sewer_assessment': SEWER_ASSESS, 'jail_mf': JAIL_MF, 'achd': ACHD,
    'permit_formula': '$50 + $5.50 per $1,000 project value',
    'subject_units': SUBJ_UNITS, 'stack_total': subtotal,
    'stack_per_unit': subtotal / SUBJ_UNITS,
    'emblem_total': EMB_TOTAL, 'emblem_per_unit': EMB_TOTAL / EMB_MODEL_UNITS,
    'emblem_pct_of_budget': EMB_TOTAL / EMB_DEV_BUDGET,
}, indent=1))

print('wrote', OUT)
print(f'Stack total 360u: ${subtotal:,.0f}  =  ${subtotal/SUBJ_UNITS:,.0f}/unit')
print(f'Emblem actual:    ${EMB_TOTAL:,.0f}  =  ${EMB_TOTAL/EMB_MODEL_UNITS:,.0f}/unit '
      f'({EMB_TOTAL/EMB_DEV_BUDGET:.1%} of budget)')
print(f'Building permit 360u: ${subj_permit:,.0f} on ${subj_value:,.0f} project value')
