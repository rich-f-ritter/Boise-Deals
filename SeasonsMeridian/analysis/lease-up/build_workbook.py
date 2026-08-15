#!/usr/bin/env python3
"""Seasons at Meridian — Lease-Up Analysis workbook."""
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = 'Seasons at Meridian - Lease-Up Analysis.xlsx'
CUTOFF = '2026-08'
ACTUAL_FROM = '2026-01'

NAVY = '1F3864'
HDR = PatternFill('solid', fgColor=NAVY)
SUBHDR = PatternFill('solid', fgColor='D9E2F3')
PROXY_FILL = PatternFill('solid', fgColor='FFF2CC')      # amber = proxy data
TOTAL_FILL = PatternFill('solid', fgColor='E2EFDA')
WHITE_B = Font(color='FFFFFF', bold=True, size=10)
BOLD = Font(bold=True, size=10)
SMALL = Font(size=9, italic=True, color='595959')
THIN = Side(style='thin', color='BFBFBF')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

ev = pd.read_csv('events.csv')
mo = pd.read_csv('monthly.csv')
wb = openpyxl.Workbook()


def style_header(ws, row, ncols, height=42):
    ws.row_dimensions[row].height = height
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill, cell.font = HDR, WHITE_B
        cell.alignment = Alignment(horizontal='center', vertical='bottom', wrap_text=True)
        cell.border = BOX


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ======================================================================
# 1. SUMMARY
# ======================================================================
ws = wb.active
ws.title = 'Summary'
widths(ws, {'A': 62, 'B': 15, 'C': 15, 'D': 58})
r = 1
ws['A1'] = 'Seasons at Meridian — Lease-Up Analysis'
ws['A1'].font = Font(bold=True, size=15, color=NAVY)
ws['A2'] = ('Month-by-month leasing history from the start of lease-up (Jun 2024) through 8/4/2026: '
            'new leases signed, expirations, renewals and renewal increases, and new-lease trade-outs '
            '— gross and effective.')
ws['A2'].font = SMALL
ws['A3'] = ('DATA BASIS: Jan 2026 forward is Yardi actuals. Jun 2024 – Dec 2025 is HelloData listing data '
            '(amber rows) — no Yardi roster, lease-start, renewal or financial data exists for that window.')
ws['A3'].font = Font(size=9, italic=True, bold=True, color='BF8F00')
for c in ('A2', 'A3'):
    ws[c].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(f'{c}:D{c[1]}')
ws.row_dimensions[2].height = 30
ws.row_dimensions[3].height = 30
r = 5

act = mo[(mo.month >= ACTUAL_FROM) & (mo.month <= CUTOFF)]
prox = mo[mo.month < ACTUAL_FROM]
e_ren = ev[ev.event == 'Renewal']
e_new = ev[ev.event == 'New Lease']
e_rel = e_new[e_new.generation == 'Re-lease']
e_rel_a = e_rel[e_rel.month >= ACTUAL_FROM]


def block(title, rows, note=''):
    global r
    ws.cell(row=r, column=1, value=title).font = Font(bold=True, size=11, color='FFFFFF')
    for c in range(1, 5):
        ws.cell(row=r, column=c).fill = HDR
    r += 1
    for lbl, val, fmt, cmt in rows:
        ws.cell(row=r, column=1, value=lbl).font = Font(size=10)
        cell = ws.cell(row=r, column=2, value=val)
        cell.number_format = fmt
        cell.font = BOLD
        cell.alignment = Alignment(horizontal='center')
        ws.cell(row=r, column=4, value=cmt).font = SMALL
        ws.cell(row=r, column=4).alignment = Alignment(wrap_text=True, vertical='top')
        r += 1
    r += 1


block('LEASE-UP VELOCITY', [
    ('First listing on market', 'Jun 1, 2024', '@', 'HelloData — earliest tracked listing'),
    ('First move-in (estimated)', 'Jul 2024', '@',
     'Two units off-market late Jun 2024; move-in estimated at +15d — those tenants left before any roll'),
    ('First move-in (exact)', 'Aug 21, 2024', '@', 'H210 — earliest move-in on a rent roll'),
    ('Total units', 360, '#,##0', 'A1 120 · A2 45 · B1 30 · B2 75 · B3 45 · C1 30 · S1 15'),
    ('New leases signed, all periods', int(mo[mo.month <= CUTOFF].new_leases_signed.sum()), '#,##0',
     'Includes both first-generation lease-up leases and re-leases of turned units'),
    ('  first-generation (initial lease-up)', int(e_new[e_new.generation == 'First lease-up lease'].shape[0]), '#,##0',
     'Exactly one per unit — all 360 units resolve to a first lease-up lease'),
    ('  re-leases of a turned unit', int(len(e_rel)), '#,##0', 'These are the leases that carry a trade-out'),
    ('Months to lease all 360 units', 21, '#,##0',
     'Jul 2024 first move-in → 4/24/2026 last first-generation lease'),
    ('Occupancy 1/1/2026 → 8/4/2026', '314 → 346 of 360', '@', '87% → 96%'),
])

ren_g = (e_ren.new_gross.mean() / e_ren.prior_gross.mean() - 1)
ren_e = (e_ren.new_eff.mean() / e_ren.prior_eff.mean() - 1)
rel_g = (e_rel_a.new_gross.mean() / e_rel_a.prior_gross.mean() - 1)
rel_e = (e_rel_a.new_eff.mean() / e_rel_a.prior_eff.mean() - 1)
dv = e_rel_a.days_vacant.dropna()
dv = dv[dv >= 0]          # one record shows the new tenant moving in before the prior move-out
tot_exp = int(act.leases_expired.sum())
tot_ren = int(act['  expired -> renewed'].sum())
tot_out = int(act['  expired -> moved out'].sum())
tot_mtm = int(act['  expired -> MTM holdover'].sum())

block('THE FIRST TURN (Yardi actuals, Jan – Aug 2026)', [
    ('Leases reaching expiration', tot_exp, '#,##0', 'The first turn of the rent roll'),
    ('  renewed', tot_ren, '#,##0', ''),
    ('  moved out', tot_out, '#,##0', ''),
    ('  month-to-month holdover', tot_mtm, '#,##0', 'Expired, still in place, no new lease signed'),
    ('RETENTION', tot_ren / max(tot_exp, 1), '0.0%', 'Renewals ÷ leases that came due'),
], )

block('RENEWAL TRADE-OUT (n = 64 renewals)', [
    ('Gross (contract rent → contract rent)', ren_g, '+0.0%;-0.0%',
     f'${e_ren.prior_gross.mean():,.0f} → ${e_ren.new_gross.mean():,.0f}'),
    ('Effective (net of amortized concessions)', ren_e, '+0.0%;-0.0%',
     f'${e_ren.prior_eff.mean():,.0f} → ${e_ren.new_eff.mean():,.0f}'),
    ('Renewals with exact report detail', 23, '#,##0',
     'Renewal trade-out report covers 5/10–7/9/2026 only; the rest are reconstructed'),
    ('Renewals at flat (0.0%) gross', int((e_ren.to_gross_pct.abs() < 0.001).sum()), '#,##0',
     'Flat renewals are invisible without lease-start data — the burn-off is what surfaces them'),
])

block('NEW-LEASE TRADE-OUT (2026 re-leases, n = %d)' % len(e_rel_a), [
    ('Gross (prior tenant → new tenant)', rel_g, '+0.0%;-0.0%',
     f'${e_rel_a.prior_gross.mean():,.0f} → ${e_rel_a.new_gross.mean():,.0f}'),
    ('Effective (net of concessions both sides)', rel_e, '+0.0%;-0.0%',
     f'${e_rel_a.prior_eff.mean():,.0f} → ${e_rel_a.new_eff.mean():,.0f}'),
    ('Avg days vacant between tenants', dv.mean(), '0.0',
     f'Median {dv.median():.0f}d · n={len(dv)} turns with an observed prior move-out date'),
])

block('RECONCILIATION TO THE FIRST-TURN ANALYSIS', [
    ('Retention, Jan–Aug 2026 only (this workbook)', tot_ren / max(tot_exp, 1), '0.0%',
     f'{tot_ren} renewed ÷ {tot_exp} expirations dated in the period'),
    ('Retention, full 1/1/26 cohort (prior deliverable)', 0.4156, '0.0%',
     '64 ÷ 154 — cohort-scoped, and includes expirations that fell in late 2025'),
    ('Renewals, all periods (this workbook)', len(e_ren), '#,##0',
     'The 11 additional renewals are dated Aug–Dec 2025, before this workbook\'s actual window'),
], )

import t12 as t12mod
T = t12mod.load()
t_first, t_last = min(T), max(T)
conc_total = sum(abs(v['concessions']) for v in T.values())
conc_rr = sum(abs(T[k]['concessions']) for k in list(T)[-3:]) / 3 * 12
gap_a = T[t_first]['physical_occupancy_avg'] - T[t_first]['economic_occupancy']
gap_b = T[t_last]['physical_occupancy_avg'] - T[t_last]['economic_occupancy']

block('HOW CONCESSIONS ACTUALLY HIT THE T12', [
    ('Concession burn window (median)', 2.5, '0.0',
     'Months from lease start to concession end date, per the burn-off report itself'),
    ('Lease term (median)', 12, '#,##0',
     'Concessions are NOT amortized over the term in the GL — they are credited over ~2.5 months'),
    ('Longest burn window observed', 4.4, '0.0', 'n=144 leases with a concession and an end date'),
    ('Concessions booked, %s to %s' % (t_first, t_last), conc_total, '$#,##0',
     'GL account 4460 — the actual dollars that hit revenue'),
    ('Run-rate, last 3 months annualized', conc_rr, '$#,##0', 'Apr-Jun 2026 x 4'),
    ('STILL TO BURN OFF at 7/30/2026', 4289, '$#,##0',
     'Only 4 leases carry unburned concession — the in-place rent roll is essentially clean'),
], )

block('WHERE THE REVENUE GAP WENT (T12, %s vs %s)' % (t_first, t_last), [
    ('Vacancy loss, % of market rent', -0.419, '+0.0%;-0.0%', '45.6% → 3.7% — the lease-up filling up'),
    ('Concessions, % of market rent', -0.054, '+0.0%;-0.0%', '7.6% → 2.2% — concessions withdrawn'),
    ('Loss to lease, % of market rent', 0.066, '+0.0%;-0.0%',
     '4.3% → 10.9% — WIDENED. Market rents were pushed up while in-place rents lagged'),
    ('Physical occupancy', T[t_last]['physical_occupancy_avg'] - T[t_first]['physical_occupancy_avg'],
     '+0.0%;-0.0%', f"{T[t_first]['physical_occupancy_avg']:.1%} → {T[t_last]['physical_occupancy_avg']:.1%}"),
    ('Economic occupancy', T[t_last]['economic_occupancy'] - T[t_first]['economic_occupancy'],
     '+0.0%;-0.0%', f"{T[t_first]['economic_occupancy']:.1%} → {T[t_last]['economic_occupancy']:.1%}"),
    ('Physical-to-economic gap', gap_b - gap_a, '+0.0%;-0.0%',
     f'{gap_a:.1%} → {gap_b:.1%}. The gap did NOT close: concession relief was offset by '
     f'loss to lease, so the upside migrated rather than arrived'),
], )

block('CORPORATE BLOCK LEASE — READ BEFORE USING AUG 2026 NUMBERS', [
    ('Murata Machinery Inc units', 8, '#,##0',
     'B106 in place (MI 8/2/26) + 7 committed for Aug 2026: A103, A303, F106, F108, H203, I203, J108'),
    ('Share of the property', 8 / 360, '0.0%',
     'A single corporate user took 2.2% of the units in one month'),
    ('Coleman Environmental Engineering', 1, '#,##0', 'B307 — the other corporate lease'),
], )

def conc_stats(rows):
    """Pooled over leases, not averaged across monthly percentages — a mean of monthly
    rates weights a 2-lease month the same as a 40-lease month. Frequency's denominator
    is leases whose effective rent is computable; depth is the average discount among
    CONCEDING leases only, so it reads as 'how deep when given', not spread over
    everyone."""
    have = rows[rows.new_gross.notna() & rows.new_eff.notna()]
    conc = have[have.new_eff < have.new_gross - 0.01]
    depth = (1 - conc.new_eff / conc.new_gross)
    return dict(n=len(have), k=len(conc), freq=len(conc) / len(have) if len(have) else None,
                depth=depth.mean() if len(conc) else None,
                dollars=conc.new_conc_total.dropna().mean(),
                term=conc.term_mo.dropna().mean())


c_init = conc_stats(e_new[e_new.generation == 'First lease-up lease'])
c_2026 = conc_stats(e_rel_a)
c_ren = conc_stats(e_ren)

block('THE CONCESSION STORY', [
    ('Renewal gross vs effective spread', ren_e - ren_g, '+0.0%;-0.0%',
     'Nearly all renewal economics come from concession burn-off, not rate'),
    ('Initial-lease concession FREQUENCY', c_init['freq'], '0.0%',
     f"{c_init['k']} of {c_init['n']} initial leases carried a concession "
     f"(denominator = leases with a computable effective rent)"),
    ('Initial-lease concession DEPTH', c_init['depth'], '0.0%',
     f"Avg discount among the {c_init['k']} CONCEDING leases only — "
     f"${c_init['dollars']:,.0f} over {c_init['term']:.1f} mo. Spread over all "
     f"{c_init['n']} it would read {c_init['depth'] * c_init['freq']:.1%}"),
    ('2026 new-lease concession FREQUENCY', c_2026['freq'], '0.0%',
     f"{c_2026['k']} of {c_2026['n']} — concessions withdrawn as the asset stabilizes"),
    ('2026 new-lease concession DEPTH', c_2026['depth'], '0.0%',
     f"Avg among the {c_2026['k']} conceding — ${c_2026['dollars']:,.0f} over "
     f"{c_2026['term']:.1f} mo"),
    ('2026 renewal concession FREQUENCY', c_ren['freq'], '0.0%',
     f"{c_ren['k']} of {c_ren['n']} — renewals are written essentially concession-free"),
])

ws.cell(row=r, column=1, value='Sources: Yardi rent rolls (1/1, 7/07, 7/19, 8/04/2026) · Concession Burn Off '
        '(6/21, 7/30/2026) · Renewal Trade-Out report (5/10–7/9/2026) · HelloData Unit Details (8/14/2026) · '
        'T12 (Jun 2025–Jun 2026). Measurement date 8/4/2026.').font = SMALL
ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.row_dimensions[r].height = 28

# ======================================================================
# 2. MONTHLY
# ======================================================================
ws = wb.create_sheet('Monthly')
COLS = [
    ('month', 'Month', 10, '@'),
    ('basis', 'Data basis', 17, '@'),
    ('new_leases_signed', 'NEW LEASES\nSIGNED', 10, '#,##0'),
    ('  of which first lease-up lease', 'of which:\n1st-gen', 9, '#,##0'),
    ('  of which re-lease (turned unit)', 'of which:\nre-lease', 9, '#,##0'),
    ('units_leased_to_date', 'UNITS LEASED\nto date (cum.)', 12, '#,##0'),
    ('leased_to_date_pct', 'LEASED\nto date %', 10, '0.0%'),
    ('units_occupied_eom', 'UNITS\nOCCUPIED', 10, '#,##0'),
    ('units_vacant_eom', 'UNITS\nVACANT', 9, '#,##0'),
    ('physical_occupancy_eom', 'OCCUPANCY\nrent roll, EOM', 12, '0.0%'),
    ('t12_physical_occupancy_avg', 'OCCUPANCY\nT12, mo. avg', 12, '0.0%'),
    ('t12_economic_occupancy', 'ECONOMIC\nOCCUPANCY (T12)', 13, '0.0%'),
    ('t12_concessions', 'CONCESSIONS\n$ (GL 4460)', 12, '#,##0;(#,##0)'),
    ('t12_concession_pct_gpr', 'CONC.\n% of GPR', 9, '0.0%'),
    ('t12_loss_to_lease_pct', 'LOSS TO LEASE\n% of market', 12, '0.0%'),
    ('occupancy_basis', 'Rent-roll occupancy basis', 28, '@'),
    ('new_lease_mixwtd_gross', 'New lease\nmix-wtd gross $', 12, '#,##0'),
    ('new_lease_mixwtd_eff', 'New lease\nmix-wtd eff $', 12, '#,##0'),
    ('leases_expired', 'LEASES\nEXPIRED', 10, '#,##0'),
    ('  expired -> renewed', 'exp →\nrenewed', 9, '#,##0'),
    ('  expired -> moved out', 'exp →\nmoved out', 9, '#,##0'),
    ('  expired -> MTM holdover', 'exp →\nMTM', 8, '#,##0'),
    ('retention_pct', 'RETENTION\n%', 10, '0.0%'),
    ('renewals_survivor_floor', 'Renewals obs.\n(survivors, ≥)', 12, '#,##0'),
    ('renewal_n', 'RENEWALS\n(n)', 10, '#,##0'),
    ('renewal_prior_gross', 'Renewal\nprior gross $', 12, '#,##0'),
    ('renewal_new_gross', 'Renewal\nnew gross $', 12, '#,##0'),
    ('renewal_gross_pct_avg', 'RENEWAL\nGROSS %', 11, '+0.0%;-0.0%'),
    ('renewal_prior_eff', 'Renewal\nprior eff $', 12, '#,##0'),
    ('renewal_new_eff', 'Renewal\nnew eff $', 12, '#,##0'),
    ('renewal_eff_pct_avg', 'RENEWAL\nEFF %', 11, '+0.0%;-0.0%'),
    ('relet_n', 'UNITS RE-LEASED\nto new tenant (n)', 13, '#,##0'),
    ('newlease_prior_gross', 'New lease\nprior gross $', 12, '#,##0'),
    ('newlease_new_gross', 'New lease\nnew gross $', 12, '#,##0'),
    ('newlease_gross_pct_avg', 'NEW-LEASE\nGROSS %', 11, '+0.0%;-0.0%'),
    ('newlease_prior_eff', 'New lease\nprior eff $', 12, '#,##0'),
    ('newlease_new_eff', 'New lease\nnew eff $', 12, '#,##0'),
    ('newlease_eff_pct_avg', 'NEW-LEASE\nEFF %', 11, '+0.0%;-0.0%'),
    ('new_conc_freq', 'Conc.\nfreq %', 9, '0%'),
    ('new_conc_depth', 'Conc.\ndepth %', 9, '0.0%'),
    ('move_outs', 'Move-\nouts', 8, '#,##0'),
]
ws['A1'] = 'Monthly Lease Activity — Seasons at Meridian'
ws['A1'].font = Font(bold=True, size=13, color=NAVY)
ws['A2'] = ('Amber rows are HelloData proxy: leases signed = listings going off-market; trade-outs are '
            'asking→asking, not contract→contract. Expirations and move-outs cannot be observed at all in '
            'that window and are left BLANK — never zero. Renewals are only partly observable (the burn-off '
            'sees residents still in place at 7/30/26), so those months carry a survivor floor "≥ n" instead '
            'of a count. Aug 2026 is a partial month — the roll is as-of 8/4.')
ws['A3'] = ('OCCUPANCY — two independent measures, deliberately not blended. "Rent roll, EOM" counts occupied '
            'units at month end (ties EXACTLY to the rolls at 1/1/26 = 314 and 8/4/26 = 346). "T12, mo. avg" is '
            '1 - vacancy loss / market rent, time-weighted across the month, and is the ONLY source of occupancy '
            'before 2026. Across the six overlapping months the two agree within 2.1 pts with no directional '
            'bias. ECONOMIC occupancy is net residential rent over market rent — the gap to physical occupancy '
            'is concessions + loss to lease + bad debt. Jul 2024 - May 2025 predates both T12s: absorption '
            '(cumulative first-generation leases) is the observable series there.')
for _c in ('A2', 'A3'):
    ws[_c].font = Font(size=9, italic=True, color='BF8F00')
    ws[_c].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=int(_c[1]), start_column=1, end_row=int(_c[1]), end_column=14)
ws.row_dimensions[2].height = 26
ws.row_dimensions[3].height = 26

HROW = 5
for i, (_, label, w, _f) in enumerate(COLS, start=1):
    ws.cell(row=HROW, column=i, value=label)
    ws.column_dimensions[get_column_letter(i)].width = w
style_header(ws, HROW, len(COLS))
ws.freeze_panes = f'C{HROW+1}'

# columns that are structurally unobservable in the proxy window
PROXY_BLANK = {'leases_expired', '  expired -> renewed', '  expired -> moved out',
               '  expired -> MTM holdover', 'retention_pct', 'renewal_n',
               'renewal_prior_gross', 'renewal_new_gross', 'renewal_gross_pct_avg',
               'renewal_prior_eff', 'renewal_new_eff', 'renewal_eff_pct_avg', 'move_outs'}

rw = HROW + 1
disp = mo[mo.month <= CUTOFF].copy()
for _, row in disp.iterrows():
    is_proxy = row['month'] < ACTUAL_FROM
    for i, (key, _lbl, _w, fmt) in enumerate(COLS, start=1):
        v = row.get(key)
        if is_proxy and key in PROXY_BLANK:
            v = None
        if pd.isna(v):
            v = None
        cell = ws.cell(row=rw, column=i, value=v)
        cell.number_format = fmt
        cell.border = BOX
        cell.alignment = Alignment(horizontal='center')
        if is_proxy:
            cell.fill = PROXY_FILL
    rw += 1

# totals / weighted averages
ws.cell(row=rw, column=1, value='TOTAL / AVG')
ws.cell(row=rw, column=2, value='Yardi actuals only')
tot = {
    'new_leases_signed': act.new_leases_signed.sum(),
    '  of which first lease-up lease': act['  of which first lease-up lease'].sum(),
    '  of which re-lease (turned unit)': act['  of which re-lease (turned unit)'].sum(),
    'leases_expired': tot_exp, '  expired -> renewed': tot_ren,
    '  expired -> moved out': tot_out, '  expired -> MTM holdover': tot_mtm,
    'retention_pct': tot_ren / max(tot_exp, 1),
    'renewal_n': len(e_ren), 'renewal_prior_gross': e_ren.prior_gross.mean(),
    'renewal_new_gross': e_ren.new_gross.mean(), 'renewal_gross_pct_avg': ren_g,
    'renewal_prior_eff': e_ren.prior_eff.mean(), 'renewal_new_eff': e_ren.new_eff.mean(),
    'renewal_eff_pct_avg': ren_e,
    'relet_n': len(e_rel_a), 'newlease_prior_gross': e_rel_a.prior_gross.mean(),
    'newlease_new_gross': e_rel_a.new_gross.mean(), 'newlease_gross_pct_avg': rel_g,
    'newlease_prior_eff': e_rel_a.prior_eff.mean(), 'newlease_new_eff': e_rel_a.new_eff.mean(),
    'newlease_eff_pct_avg': rel_e,
    # pooled over leases, matching the Summary tab — not a mean of monthly rates
    'new_conc_freq': c_2026['freq'], 'new_conc_depth': c_2026['depth'],
    'move_outs': act.move_outs.sum(),
    # occupancy is a level, not a flow: the total row carries the latest reading
    'units_leased_to_date': act.units_leased_to_date.dropna().iloc[-1],
    'leased_to_date_pct': act.leased_to_date_pct.dropna().iloc[-1],
    'units_occupied_eom': act.units_occupied_eom.dropna().iloc[-1],
    'units_vacant_eom': act.units_vacant_eom.dropna().iloc[-1],
    'physical_occupancy_eom': act.physical_occupancy_eom.dropna().iloc[-1],
    'occupancy_basis': 'Latest — as of 8/4/2026',
}
for i, (key, _lbl, _w, fmt) in enumerate(COLS, start=1):
    cell = ws.cell(row=rw, column=i)
    if key in tot and pd.notna(tot[key]):
        cell.value = tot[key]
    cell.number_format = fmt
    cell.font = BOLD
    cell.fill = TOTAL_FILL
    cell.border = BOX
    cell.alignment = Alignment(horizontal='center')

rw += 2
for line in [
    'Renewal trade-out is measured contract rent → contract rent for the SAME resident; effective nets '
    'the total concession amortized over the lease term (the Yardi convention used by the 3ps renewal report).',
    'New-lease trade-out is measured against the PRIOR TENANT\'S LAST CONTRACT RENT in the same unit. '
    'For 2026 re-leases whose prior tenant departed before 1/1/2026 the baseline falls back to that unit\'s '
    'prior listing rent — flagged per row on the Lease Events tab.',
    'Rent levels are mix-weighted to the property\'s actual unit mix from the 8/4/26 roll, so a month that '
    'happened to lease mostly 1-beds does not read as a rent decline.',
    'Concession frequency = share of new leases with any concession. Depth = average discount among ONLY '
    'those leases. Blended averages are not shown — they mix conceding and non-conceding leases.',
    'Corporate leases are excluded from all rent statistics. Two are in place (Coleman Environmental B307, '
    'Murata Machinery B106); Murata holds seven MORE units committed for Aug 2026, not yet in this ledger.',
]:
    ws.cell(row=rw, column=1, value='• ' + line).font = SMALL
    ws.cell(row=rw, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=14)
    ws.row_dimensions[rw].height = 24
    rw += 1

# ======================================================================
# 3. T12 REVENUE BRIDGE
# ======================================================================
ws = wb.create_sheet('T12 Revenue Bridge')
widths(ws, {'A': 11, **{get_column_letter(i): 13 for i in range(2, 13)}})
ws['A1'] = 'T12 Residential Revenue Bridge — market rent down to collected'
ws['A1'].font = Font(bold=True, size=13, color=NAVY)
ws['A2'] = ('From the two supplied operating statements (Jun 2025-May 2026 and Jul 2025-Jun 2026); they '
            'overlap and agree exactly, so the later file wins. This is GL truth — the only source of '
            'occupancy before 2026, and the only place the concession dollars can be seen as booked. '
            'Credits are shown as booked (negative).')
ws['A2'].font = Font(size=9, italic=True, color='595959')
ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=12)
ws.row_dimensions[2].height = 28

TCOLS = [('month', 'Month', '@'), ('market_rent', 'Market\nRent', '#,##0'),
         ('loss_to_lease', 'Loss to\nLease', '#,##0;(#,##0)'),
         ('gross_potential', 'GROSS\nPOTENTIAL', '#,##0'),
         ('vacancy_loss', 'Vacancy\nLoss', '#,##0;(#,##0)'),
         ('concessions', 'Concessions\n(4460)', '#,##0;(#,##0)'),
         ('employee_discounts', 'Employee\nDiscounts', '#,##0;(#,##0)'),
         ('write_offs', 'Write\nOffs', '#,##0;(#,##0)'),
         ('net_residential_rent', 'NET RESID.\nRENT', '#,##0'),
         ('physical_occupancy_avg', 'PHYSICAL\nOCC (avg)', '0.0%'),
         ('economic_occupancy', 'ECONOMIC\nOCC', '0.0%'),
         ('concession_pct_gpr', 'CONC.\n% GPR', '0.0%')]
HR = 4
for i, (_, lbl, _f) in enumerate(TCOLS, start=1):
    ws.cell(row=HR, column=i, value=lbl)
style_header(ws, HR, len(TCOLS))
rw = HR + 1
for mo_, d_ in T.items():
    for i, (k, _l, fmt) in enumerate(TCOLS, start=1):
        c = ws.cell(row=rw, column=i, value=(mo_ if k == 'month' else d_.get(k)))
        c.number_format = fmt
        c.border = BOX
        c.alignment = Alignment(horizontal='center')
        c.font = Font(size=10)
    rw += 1
for i, (k, _l, fmt) in enumerate(TCOLS, start=1):
    c = ws.cell(row=rw, column=i)
    if k == 'month':
        c.value = 'TOTAL'
    elif k in ('physical_occupancy_avg', 'economic_occupancy', 'concession_pct_gpr'):
        c.value = T[max(T)][k]           # a rate: show the latest, not a sum
    else:
        c.value = sum(v.get(k, 0) for v in T.values())
    c.number_format, c.font, c.fill, c.border = fmt, BOLD, TOTAL_FILL, BOX
    c.alignment = Alignment(horizontal='center')
rw += 2
for txt in [
    '• PHYSICAL OCCUPANCY = 1 - vacancy loss / market rent. Vacancy loss is booked at market rent for each '
    'vacant day, so this is a time-weighted month average — not the same statistic as the rent-roll count at '
    'month end. Across the six overlapping months the two agree within 2.1 pts, in both directions.',
    '• ECONOMIC OCCUPANCY = net residential rent / market rent. The gap to physical occupancy is what '
    'concessions, loss to lease and bad debt take out of a fully-occupied building.',
    '• CONCESSIONS ARE NOT AMORTIZED OVER THE LEASE TERM IN THE GL. The burn-off report gives each lease a '
    'concession END DATE, and the median gap from lease start to that date is 2.5 months against a median '
    '12-month term; the longest observed is 4.4 months. So a concession lands as a large credit in the first '
    'two or three months of a lease and then stops.',
    '• That timing is why effective rent in this workbook (gross less concession amortized over the full term, '
    'the convention the Yardi renewal report uses) does not tie month-for-month to GL 4460. Same total dollars, '
    'different periods. The amortized figure is the right one for underwriting a lease; the GL timing is the '
    'right one for reading a trailing statement.',
    '• Rebuilding GL 4460 from the burn-off recovers 65% of the dollars. The shortfall is departed residents — '
    'the burn-off lists current residents only, so tenants who left before it was run take their concessions '
    'with them. Months with heavy in-place lease-up (Jul-Sep 2025) reconstruct at 70-118%.',
    '• Only $4,289 of concession remains unburned across 4 leases as of 7/30/2026. The concession drag visible '
    'in this T12 is almost entirely historical, NOT a forward liability on the in-place rent roll.',
    '• Loss to lease widened from 4.3% to 10.9% of market rent over the same period that concessions fell from '
    '7.6% to 2.2%. The physical-to-economic gap therefore did not close. Underwriting the concession burn-off '
    'as pure upside would double-count relief that loss to lease has already absorbed.',
]:
    ws.cell(row=rw, column=1, value=txt).font = SMALL
    ws.cell(row=rw, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=12)
    ws.row_dimensions[rw].height = 30
    rw += 1

# ======================================================================
# 4. LEASE EVENTS (audit trail)
# ======================================================================
ws = wb.create_sheet('Lease Events')
ev_out = ev[ev.month <= CUTOFF].copy()
hdrs = list(ev_out.columns)
ws.append([h.replace('_', ' ').title() for h in hdrs])
style_header(ws, 1, len(hdrs), height=30)
for _, row in ev_out.iterrows():
    ws.append([None if pd.isna(v) else v for v in row.tolist()])
for i, h in enumerate(hdrs, start=1):
    L = get_column_letter(i)
    ws.column_dimensions[L].width = 30 if h in ('source', 'prior_basis') else (
        18 if 'name' in h or h in ('basis', 'generation', 'event') else 12)
    if 'pct' in h:
        for c in range(2, ws.max_row + 1):
            ws.cell(row=c, column=i).number_format = '+0.0%;-0.0%'
    elif 'gross' in h or 'eff' in h or 'conc' in h:
        for c in range(2, ws.max_row + 1):
            ws.cell(row=c, column=i).number_format = '#,##0'
ws.freeze_panes = 'A2'
ws.auto_filter.ref = f'A1:{get_column_letter(len(hdrs))}{ws.max_row}'

# ======================================================================
# 4. EXPIRATION SCHEDULE (forward book)
# ======================================================================
ws = wb.create_sheet('Expiration Schedule')
fwd = mo[mo.month > CUTOFF][['month', 'scheduled_expirations_ahead', 'notices_scheduled_moveout']]
ws['A1'] = 'Forward Expiration Schedule (leases in place at 8/4/2026)'
ws['A1'].font = Font(bold=True, size=13, color=NAVY)
ws['A2'] = ('The second turn. Each resident\'s currently scheduled lease expiration, plus notices already '
            'given for move-outs dated after the 8/4/26 roll.')
ws['A2'].font = SMALL
ws.append([])
ws.append(['Month', 'Scheduled expirations', 'Notices given (scheduled move-out)'])
style_header(ws, 4, 3, height=30)
for _, row in fwd.iterrows():
    ws.append([row['month'], int(row['scheduled_expirations_ahead']), int(row['notices_scheduled_moveout'])])
tr = ws.max_row + 1
ws.cell(row=tr, column=1, value='TOTAL').font = BOLD
ws.cell(row=tr, column=2, value=int(fwd.scheduled_expirations_ahead.sum())).font = BOLD
ws.cell(row=tr, column=3, value=int(fwd.notices_scheduled_moveout.sum())).font = BOLD
for c in range(1, 4):
    ws.cell(row=tr, column=c).fill = TOTAL_FILL
    ws.cell(row=tr, column=c).alignment = Alignment(horizontal='center')
widths(ws, {'A': 14, 'B': 22, 'C': 30})
for row in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=1, max_col=3):
    for cell in row:
        cell.alignment = Alignment(horizontal='center')
        cell.border = BOX

# ======================================================================
# 5. SOURCES & METHOD
# ======================================================================
ws = wb.create_sheet('Sources & Method')
widths(ws, {'A': 118})
notes = [
    ('H', 'Seasons at Meridian — Lease-Up Analysis: sources, conventions and limits'),
    ('T', 'Measurement date 8/4/2026 (latest rent roll). 360 units. Lease-up began Jun 2024 (first listing); '
          'first move-in 8/21/2024.'),
    ('H', 'The two data bases'),
    ('T', 'ACTUAL (Jan 2026 – Aug 2026): Yardi rent rolls, concession burn-off, renewal trade-out report. '
          'Every figure is an observed lease record.'),
    ('T', 'PROXY (Jun 2024 – Dec 2025): HelloData listing episodes only. Shown amber on the Monthly tab. '
          'A listing going off-market stands in for a new lease signed; trade-outs are asking→asking rather '
          'than contract→contract. Expirations, renewals, move-outs and retention are NOT observable in this '
          'window and are left BLANK rather than reported as zero.'),
    ('H', 'Why the pre-2026 window cannot be built on Yardi data'),
    ('T', '• The earliest rent roll is 1/1/2026 — there is no roster snapshot before it, so any tenant who '
          'moved in and out during 2024–2025 appears in no Yardi source.'),
    ('T', '• The concession burn-off is the only source of lease-start dates, and it covers CURRENT residents '
          'only (347 as of 7/30/26). Just 16 of them moved in during 2024, and all 16 have already renewed — '
          'so the burn-off shows their current lease, not their original one.'),
    ('T', '• Several of those residents show ~546-day move-in→lease-start gaps, which could be one renewal off '
          'an 18-month initial lease OR two successive renewals. The sources cannot distinguish these, so '
          'pre-2026 renewal counts are a floor, not a count.'),
    ('T', '• The renewal trade-out report covers 5/10/2026 – 7/9/2026 only (23 renewals). Both T12s begin '
          'Jun 2025, missing the first ten months of lease-up.'),
    ('H', 'Conventions'),
    ('T', 'New leases are counted on MOVE-IN DATE. The 1/1/2026 roll carries real move-in dates back to '
          '8/21/2024, so 314 of the 400 pre-2026 leases are dated exactly; the remaining 86 belong to tenants '
          'who moved in and out before any rent roll was cut, and are dated from their listing\'s off-market '
          'date + 15 days (the validated median lag). Those rows are marked ESTIMATED in Date Basis.'),
    ('T', 'Renewals are counted separately and are never included in "new leases signed".'),
    ('T', 'Renewal trade-out = same resident, contract rent → contract rent. New-lease trade-out = same unit, '
          'prior tenant\'s LAST contract rent → new tenant\'s contract rent.'),
    ('T', 'Effective rent = gross − (total concession ÷ lease term months). This is the Yardi convention used '
          'by the 3ps renewal trade-out report, so these figures tie to the seller\'s own report exactly.'),
    ('T', 'Retention = renewals ÷ leases that reached expiration in the month. MTM holdovers sit in the '
          'denominator as non-renewals until they either sign or leave.'),
    ('T', 'Rent levels are mix-weighted to the actual unit mix from the 8/4/26 roll (A1 120 · A2 45 · B1 30 · '
          'B2 75 · B3 45 · C1 30 · S1 15 = 360) to remove mix bias from month-to-month comparisons.'),
    ('T', 'Concessions are reported as frequency (share of leases with any concession) and depth (average '
          'discount among only those leases), never as a blended average.'),
    ('T', 'Corporate leases excluded from rent statistics: Coleman Environmental Engineering (B307) and '
          'Murata Machinery Inc, which holds EIGHT units — B106 in place (move-in 8/2/26) plus A103, A303, '
          'F106, F108, H203, I203 and J108 committed for August 2026. That is 2.2% of the property to one '
          'user, landing right at the measurement date: the seven future leases are excluded here but will '
          'inflate Aug/Sep 2026 absorption in any later cut. Treat recent leasing velocity accordingly.'),
    ('H', 'Validation performed'),
    ('T', '✓ All 23 renewals in the 5/10–7/9/2026 report are present, and prior/new gross and effective rents '
          'tie to the report\'s portfolio totals to the cent ($1,762.91 → $1,793.26 gross; $1,639.44 → '
          '$1,789.92 effective).'),
    ('T', '✓ Ledger renewal count (64) matches the independent burn-off count of residents whose lease start '
          'post-dates their move-in.'),
    ('T', '✓ Net leasing in the actual window (139 new leases − 105 move-outs = +34) reconciles to the observed '
          'occupancy change (314 → 346 = +32); the residual is leases signed for Aug/Sep move-ins.'),
    ('T', '✓ Exactly one first-generation lease per unit, and all 360 units resolve — the ledger accounts for '
          'every unit in the property.'),
    ('H', 'Known limits'),
    ('T', 'Renewals before 1/1/2026 are survivor-biased: only residents still in place on 7/30/2026 are visible, '
          'so early-period renewal counts are floors.'),
    ('T', '41 of 64 renewals (64%) have reconstructed rather than reported concession detail, because the '
          'renewal report covers only a two-month window.'),
    ('T', '7 of the 2026 new leases have no term or concession data and so carry no effective rent.'),
    ('T', 'The burn-off\'s Lease Rent column is unreliable on some rows (H203 shows $386 and H213 $342 where the '
          '8/4 roll shows $1,600 and $1,995); rent-roll Actual Rent is used as the rent of record throughout.'),
    ('H', 'What would close the gap (in descending order of value)'),
    ('T', '1. Yardi lease history / lease audit — every lease ever written per unit (start, end, term, gross '
          'rent, concession). One report would make the entire pre-2026 period exact.'),
    ('T', '2. Renewal trade-out reports (3ps format) for all windows outside 5/10–7/9/2026.'),
    ('T', '3. Monthly resident activity / box score from Aug 2024 — leases signed, move-ins, move-outs, notices.'),
    ('T', '4. Historical month-end rent rolls, Aug 2024 – Dec 2025.'),
    ('T', '5. Monthly financials for Aug 2024 – May 2025 (pre-dates both T12s).'),
]
r = 1
for kind, text in notes:
    cell = ws.cell(row=r, column=1, value=text)
    if kind == 'H':
        cell.font = Font(bold=True, size=11, color='FFFFFF')
        cell.fill = HDR
        ws.row_dimensions[r].height = 20
    else:
        cell.font = Font(size=10)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 15 + 13 * (len(text) // 115)
    r += 1

for s in wb.worksheets:
    s.sheet_view.showGridLines = False
wb.save(OUT)
print(f'wrote {OUT}')
print(f'  Monthly: {len(disp)} months ({disp.month.min()} → {disp.month.max()})')
print(f'  Lease Events: {len(ev_out)} rows')
print(f'  Expiration Schedule: {len(fwd)} months, {int(fwd.scheduled_expirations_ahead.sum())} leases')
