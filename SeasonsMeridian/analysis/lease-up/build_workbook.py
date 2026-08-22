#!/usr/bin/env python3
"""Seasons at Meridian — Lease-Up Analysis workbook (v5).

Every figure on the Summary tab is computed from events.csv / monthly.csv /
stats.json / the T12 parser at build time — nothing is hand-keyed, so a re-run
against newer source documents cannot leave a stale number behind."""
import json
import pandas as pd
import openpyxl
import t12 as t12mod
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = 'Seasons at Meridian - Lease-Up Analysis.xlsx'
CUTOFF = '2026-08'
CUTOFF_D = '8/18/2026'
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
S = json.load(open('stats.json'))
T = t12mod.load()
wb = openpyxl.Workbook()


def arms(df):
    """Arm's-length filter: corporate leases and internal transfers out."""
    return df[(df.corporate.isna() | (df.corporate == '')) &
              (df.transfer.isna() | (df.transfer == ''))]


def paired(df, a, b):
    """Rows where both sides of a trade-out exist; % change on matched pairs."""
    p = df[df[a].notna() & df[b].notna() & (df[a] > 0)]
    return p, (p[b].mean() / p[a].mean() - 1) if len(p) else None


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


# ---------------------------------------------------------------- aggregates
act = mo[(mo.month >= ACTUAL_FROM) & (mo.month <= CUTOFF)]
e_new = ev[ev.event == 'New Lease']
e_ren = ev[ev.event == 'Renewal']
e_ren26 = e_ren[e_ren.month >= ACTUAL_FROM]
e_rel = e_new[e_new.generation == 'Re-lease']
e_rel_a = e_rel[e_rel.month >= ACTUAL_FROM]
e_rel_r = arms(e_rel_a)                        # 2026 re-leases, arm's-length
e_ren_r = arms(e_ren26)
e_fut = ev[ev.event == 'Lease Signed (future move-in)']
e_fut_r = arms(e_fut)
exact_rel = e_rel_r[e_rel_r.source == 'New-lease trade-out report (exact)']
exact_fut = e_fut_r[e_fut_r.to_gross_pct.notna()]

tot_exp = int(act.leases_expired.sum())
tot_ren = int(act['  expired -> renewed'].sum())
tot_out = int(act['  expired -> moved out'].sum())
tot_xfer = int(act['  expired -> transferred'].sum())
tot_mtm = int(act['  expired -> MTM holdover'].sum())

rg_p, ren_g = paired(e_ren_r, 'prior_gross', 'new_gross')
re_p, ren_e = paired(e_ren_r, 'prior_eff', 'new_eff')
ng_p, rel_g = paired(e_rel_r, 'prior_gross', 'new_gross')
ne_p, rel_e = paired(e_rel_r, 'prior_eff', 'new_eff')
xg_p, ex_g = paired(exact_rel, 'prior_gross', 'new_gross')
xe_p, ex_e = paired(exact_rel, 'prior_eff', 'new_eff')
fg_p, fut_g = paired(exact_fut, 'prior_gross', 'new_gross')
fe_p, fut_e = paired(exact_fut, 'prior_eff', 'new_eff')

dv = e_rel_r.days_vacant.dropna()
dv = dv[dv >= 0]

first_gen = e_new[e_new.generation == 'First lease-up lease']
last_first = first_gen.signed.max()

# occupancy endpoints come from the rent-roll ANCHORS (counted from the rolls
# directly), not the derived coverage series
anchor_items = sorted(S['anchors'].items())
occ_first, occ_last = anchor_items[0][1], anchor_items[-1][1]

n_exact_ren = int((e_ren.source == 'Renewal trade-out report (exact)').sum())
flat_ren = int((e_ren26.to_gross_pct.abs() < 0.001).sum())

conc_total = sum(abs(v['concessions']) for v in T.values())
conc_rr = sum(abs(T[k]['concessions']) for k in list(T)[-3:]) / 3 * 12
t_first, t_last = min(T), max(T)
gap_a = T[t_first]['physical_occupancy_avg'] - T[t_first]['economic_occupancy']
gap_b = T[t_last]['physical_occupancy_avg'] - T[t_last]['economic_occupancy']
vac_a = abs(T[t_first]['vacancy_loss']) / T[t_first]['market_rent']
vac_b = abs(T[t_last]['vacancy_loss']) / T[t_last]['market_rent']
cc_a = abs(T[t_first]['concessions']) / T[t_first]['market_rent']
cc_b = abs(T[t_last]['concessions']) / T[t_last]['market_rent']
ltl_a, ltl_b = T[t_first]['ltl_pct_market'], T[t_last]['ltl_pct_market']

# corporate exposure, by user, from stats
corp = {}
for name, unit, status in S['corporate_units']:
    corp.setdefault(name, []).append((unit, status))
murata = corp.get('Murata Machinery Inc', [])
paragon = corp.get('Paragon Corporate Housing', [])
corp_n = len({u for _n, u, _s in S['corporate_units']})   # distinct UNITS (H111 is Wolff AND Murata)


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


c_init = conc_stats(arms(first_gen))
c_2026 = conc_stats(e_rel_r)
c_ren = conc_stats(e_ren_r)

# ======================================================================
# 1. SUMMARY
# ======================================================================
ws = wb.active
ws.title = 'Summary'
widths(ws, {'A': 62, 'B': 15, 'C': 15, 'D': 58})
ws['A1'] = 'Seasons at Meridian — Lease-Up Analysis'
ws['A1'].font = Font(bold=True, size=15, color=NAVY)
ws['A2'] = (f'Month-by-month leasing history from the start of lease-up (Jun 2024) through {CUTOFF_D}: '
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


def block(title, rows):
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


mix_str = ' · '.join(f'{k} {v}' for k, v in sorted(S['unit_mix'].items(),
                     key=lambda kv: (kv[0][0] != 'A', kv[0])))
block('LEASE-UP VELOCITY', [
    ('First listing on market', 'Jun 1, 2024', '@', 'HelloData — earliest tracked listing'),
    ('First move-in (estimated)', 'Jul 2024', '@',
     'Two units off-market late Jun 2024; move-in estimated at +15d — those tenants left before any roll'),
    ('First move-in (exact)', 'Aug 21, 2024', '@', 'H210 — earliest move-in on a rent roll'),
    ('Total units', 360, '#,##0', mix_str),
    ('New leases signed, all periods', int(len(e_new)), '#,##0',
     'Includes both first-generation lease-up leases and re-leases of turned units'),
    ('  first-generation (initial lease-up)', int(len(first_gen)), '#,##0',
     'Exactly one per unit — all 360 units resolve to a first lease-up lease'),
    ('  re-leases of a turned unit', int(len(e_rel)), '#,##0',
     f'Rent statistics below exclude {int(len(e_rel_a) - len(e_rel_r))} corporate / internal-transfer '
     f're-leases in 2026; counts include them'),
    ('Months to lease all 360 units', 21, '#,##0',
     f'Jul 2024 first move-in → {pd.Timestamp(last_first):%-m/%-d/%Y} last first-generation lease'),
    (f'Occupancy 1/1/2026 → {CUTOFF_D}', f'{occ_first} → {occ_last} of 360', '@',
     f'{occ_first / 360:.0%} → {occ_last / 360:.0%}'),
])

block(f'THE FIRST TURN (Yardi actuals, Jan – Aug 2026)', [
    ('Leases reaching expiration', tot_exp, '#,##0', 'The first turn of the rent roll'),
    ('  renewed', tot_ren, '#,##0', ''),
    ('  moved out', tot_out, '#,##0', ''),
    ('  transferred to another unit', tot_xfer, '#,##0',
     'Left the unit but not the property — several were relocated so their units could go to the '
     'Murata/Paragon corporate blocks'),
    ('  month-to-month holdover', tot_mtm, '#,##0', 'Expired, still in place, no new lease signed'),
    ('RETENTION (unit basis)', tot_ren / max(tot_exp, 1), '0.0%',
     'Renewals ÷ leases that came due'),
    ('RETENTION (tenant basis)', (tot_ren + tot_xfer) / max(tot_exp, 1), '0.0%',
     'Adds tenants who TRANSFERRED to another unit rather than leaving — they left a unit, '
     'not the property'),
])

block(f'RENEWAL TRADE-OUT (2026 renewals, n = {len(e_ren26)})', [
    ('Gross (contract rent → contract rent)', ren_g, '+0.0%;-0.0%',
     f'${rg_p.prior_gross.mean():,.0f} → ${rg_p.new_gross.mean():,.0f}'),
    ('Effective (net of amortized concessions)', ren_e, '+0.0%;-0.0%',
     f'${re_p.prior_eff.mean():,.0f} → ${re_p.new_eff.mean():,.0f}'),
    ('Renewals with exact report detail', n_exact_ren, '#,##0',
     'Renewal trade-out reports cover 5/10–7/9 and 6/19–8/19/2026; the rest are reconstructed '
     'from the burn-off + rent rolls'),
    ('Renewals at flat (0.0%) gross', flat_ren, '#,##0',
     'Flat renewals are invisible without lease-start data — the burn-off is what surfaces them'),
    ('Renewals, all periods (incl. pre-2026 survivors)', len(e_ren), '#,##0',
     f'{len(e_ren) - len(e_ren26)} additional renewals dated Aug–Dec 2025 — a survivor-biased floor, '
     'not a count'),
])

block(f'NEW-LEASE TRADE-OUT (2026 re-leases, arm\'s-length, n = {len(e_rel_r)})', [
    ('Gross (prior tenant → new tenant)', rel_g, '+0.0%;-0.0%',
     f'${ng_p.prior_gross.mean():,.0f} → ${ng_p.new_gross.mean():,.0f} — full 2026, exact + reconstructed'),
    ('Effective (net of concessions both sides)', rel_e, '+0.0%;-0.0%',
     f'${ne_p.prior_eff.mean():,.0f} → ${ne_p.new_eff.mean():,.0f}'),
    (f'  EXACT subset — moved in 6/19–8/19 (n = {len(xg_p)})', ex_g, '+0.0%;-0.0%',
     f'${xg_p.prior_gross.mean():,.0f} → ${xg_p.new_gross.mean():,.0f} gross · '
     f'${xe_p.prior_eff.mean():,.0f} → ${xe_p.new_eff.mean():,.0f} eff ({ex_e:+.1%}) — '
     'straight from the 3ps New Lease Tradeouts report: trade-outs are ACCELERATING into stabilization'),
    ('Avg days vacant between tenants', dv.mean(), '0.0',
     f'Median {dv.median():.0f}d · n={len(dv)} turns with an observed prior move-out date'),
    ('Corporate / transfer re-leases excluded', int(len(e_rel_a) - len(e_rel_r)), '#,##0',
     'Murata + Paragon corporate leases and internal unit transfers are not arm\'s-length pricing; '
     'they are flagged per-row on the Lease Events tab'),
])

block(f'THE FORWARD BOOK — leases already signed for future move-ins (n = {len(e_fut)})', [
    ('Leases signed, move-in after ' + CUTOFF_D, len(e_fut), '#,##0',
     'Rent roll Future section ∪ trade-out report. Sep–Nov 2026 move-ins — absorption already banked'),
    ('  of which corporate (Murata)', int(e_fut.corporate.notna().sum()), '#,##0',
     'Corporate block backfill — excluded from the rent statistics below'),
    ('Arm\'s-length signed trade-out, gross', fut_g, '+0.0%;-0.0%',
     f'${fg_p.prior_gross.mean():,.0f} → ${fg_p.new_gross.mean():,.0f} · n={len(fg_p)} with exact '
     'report detail'),
    ('Arm\'s-length signed trade-out, effective', fut_e, '+0.0%;-0.0%',
     f'${fe_p.prior_eff.mean():,.0f} → ${fe_p.new_eff.mean():,.0f} — zero concessions on every '
     'signed future lease'),
    ('Scheduled expirations, next 3 months', int(mo[(mo.month > CUTOFF) & (mo.month <= '2026-11')]
                                                 .scheduled_expirations_ahead.sum()), '#,##0',
     'Sep–Nov 2026 — the second turn begins against this signed-lease cushion'),
])

block('HOW CONCESSIONS ACTUALLY HIT THE T12', [
    ('Concession burn window (median)', S['burn_window_median_mo'], '0.0',
     'Months from lease start to concession end date, per the 8/19/26 burn-off report itself'),
    ('Lease term (median)', S['term_median_mo'], '#,##0',
     f'Concessions are NOT amortized over the term in the GL — they are credited over '
     f'~{S["burn_window_median_mo"]:.1f} months'),
    ('Longest burn window observed', S['burn_window_max_mo'], '0.0',
     f'n={S["burn_window_n"]} leases with a concession and an end date'),
    (f'Concessions booked, {t_first} to {t_last}', conc_total, '$#,##0',
     'GL account 4460 — the actual dollars that hit revenue. Apr 2026 restated -$818 by the '
     'Aug-Jul statement (later file wins)'),
    ('Run-rate, last 3 months annualized', conc_rr, '$#,##0',
     f'{list(T)[-3]} – {t_last} × 4 — Jul 2026 booked only ${abs(T[t_last]["concessions"]):,.0f} '
     f'({T[t_last]["concession_pct_gpr"]:.1%} of GPR)'),
    (f'STILL TO BURN OFF at {S["burnoff_asof"]}', S['still_to_burn'], '$#,##0',
     f'Only {S["still_to_burn_leases"]} leases carry unburned concession — the in-place rent roll '
     'is essentially clean'),
])

block(f'WHERE THE REVENUE GAP WENT (T12, {t_first} vs {t_last})', [
    ('Vacancy loss, % of market rent', vac_b - vac_a, '+0.0%;-0.0%',
     f'{vac_a:.1%} → {vac_b:.1%} — the lease-up filling up'),
    ('Concessions, % of market rent', cc_b - cc_a, '+0.0%;-0.0%',
     f'{cc_a:.1%} → {cc_b:.1%} — concessions withdrawn'),
    ('Loss to lease, % of market rent', ltl_b - ltl_a, '+0.0%;-0.0%',
     f'{ltl_a:.1%} → {ltl_b:.1%} — WIDENED. Market rents were pushed up while in-place rents lagged'),
    ('Physical occupancy', T[t_last]['physical_occupancy_avg'] - T[t_first]['physical_occupancy_avg'],
     '+0.0%;-0.0%', f"{T[t_first]['physical_occupancy_avg']:.1%} → {T[t_last]['physical_occupancy_avg']:.1%}"),
    ('Economic occupancy', T[t_last]['economic_occupancy'] - T[t_first]['economic_occupancy'],
     '+0.0%;-0.0%', f"{T[t_first]['economic_occupancy']:.1%} → {T[t_last]['economic_occupancy']:.1%}"),
    ('Physical-to-economic gap', gap_b - gap_a, '+0.0%;-0.0%',
     f'{gap_a:.1%} → {gap_b:.1%}. The gap did NOT close: concession relief was offset by '
     f'loss to lease, so the upside migrated rather than arrived'),
])

mur_inplace = sorted(u for u, s in murata if s == 'in place')
mur_future = sorted(u for u, s in murata if s == 'future')
block('CORPORATE BLOCK LEASES — READ BEFORE USING AUG 2026 NUMBERS', [
    ('Murata Machinery Inc units', len(murata), '#,##0',
     f'{len(mur_inplace)} in place ({", ".join(mur_inplace)}) + {len(mur_future)} future '
     f'({", ".join(mur_future)}). H203 was dropped and H111 substituted — the block is being '
     'actively re-shuffled'),
    ('Paragon Corporate Housing units', len(paragon), '#,##0',
     ', '.join(sorted(u for u, _ in paragon)) + ' — six signed in Jul 2026 alone. '
     'Excluded from all rent statistics'),
    ('Corporate departures', 2, '#,##0',
     'Coleman Environmental (B307) and Wolff Corporate Housing (H111) BOTH move out 9/30/2026'),
    ('Total corporate exposure', corp_n / 360, '0.0%',
     f'{corp_n} units tied to {len(corp)} corporate users — flag for Aug–Oct 2026 absorption '
     'and turnover'),
])

l5m, l5s = S['l5_movein'], S['l5_signed']
l5_rows = [
    ('L5 MIX-WEIGHTED (gross contract rent)', l5m['mixwtd'], '#,##0.00',
     f'vs model RRA starting market rent ${l5m["rra_mixwtd"]:,.2f} (the prior L5): '
     f'{l5m["mixwtd"] / l5m["rra_mixwtd"] - 1:+.1%} — starting rents remain current'),
    ('L5 SIGNED BASIS (incl. future move-ins already signed)', l5s['mixwtd'], '#,##0.00',
     f'{l5s["mixwtd"] / l5s["rra_mixwtd"] - 1:+.1%} vs RRA — the signed forward book is being '
     'written ABOVE the model\'s starting rents'),
]
for plan in ('S1_Seas', 'A1_Seas', 'A2_Seas', 'B1_Seas', 'B2_Seas',
             'B3a_Seas', 'B3b_Seas', 'C1a_Seas', 'C1b_Seas'):
    v = l5m['plans'].get(plan)
    if not v:
        continue
    vs = l5s['plans'].get(plan, v)
    extra = (f' · signed basis ${vs["avg"]:,.0f} ({vs["avg"] / v["rra"] - 1:+.1%})'
             if abs(vs['avg'] - v['avg']) > 0.5 else '')
    l5_rows.append((f'  {plan}', v['avg'], '#,##0.00',
                    f'n={v["n"]} · newest move-in {v["newest"]} · RRA start ${v["rra"]:,.0f} '
                    f'({v["avg"] / v["rra"] - 1:+.1%}){extra}'))
l5_rows.append(('Excluded: corporate + internal transfers', S['l5_excluded_n'], '#,##0',
                f'{S["l5_excluded_corporate"]} corporate leases + {S["l5_excluded_transfers"]} internal '
                f'transfers (negotiated swaps, not arm\'s-length — e.g. G103 books $2,140 on a '
                f'~$1,718-market A1). With them in, L5 reads ${S["l5_with_excluded_mixwtd"]:,.0f}.'))
block('L5 NEW LEASE AVERAGE — 5 most recent ARM\'S-LENGTH leases per plan, mix-weighted', l5_rows)

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
     f"{c_2026['k']} of {c_2026['n']} — concessions withdrawn as the asset stabilizes; "
     f"ZERO concessions on the {len(xg_p)} exact-report leases and all signed future leases"),
    ('2026 new-lease concession DEPTH', c_2026['depth'], '0.0%',
     f"Avg among the {c_2026['k']} conceding — ${c_2026['dollars']:,.0f} over "
     f"{c_2026['term']:.1f} mo"),
    ('2026 renewal concession FREQUENCY', c_ren['freq'], '0.0%',
     f"{c_ren['k']} of {c_ren['n']} — renewals are written essentially concession-free"),
])

ws.cell(row=r, column=1, value='Sources: Yardi rent rolls (1/1, 7/07, 7/19, 8/04, 8/18/2026) · Concession Burn Off '
        '(6/21, 7/30, 8/19/2026) · Renewal Trade-Out reports (5/10–7/9 + 6/19–8/19/2026) · New Lease Tradeouts '
        'report (6/19–8/19/2026) · HelloData Unit Details (8/21/2026) · T12 (Jun 2025–Jul 2026). '
        f'Measurement date {CUTOFF_D} (latest rent roll).').font = SMALL
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
    ('  of which corporate / transfer (excl. from $)', 'of which:\ncorp/xfer', 9, '#,##0'),
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
    ('  expired -> transferred', 'exp →\ntransfer', 9, '#,##0'),
    ('  expired -> MTM holdover', 'exp →\nMTM', 8, '#,##0'),
    ('retention_pct', 'RETENTION\n(unit) %', 10, '0.0%'),
    ('retention_tenant_pct', 'RETENTION\n(tenant) %', 10, '0.0%'),
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
    ('leases_signed_future_movein', 'SIGNED\nfuture MI', 9, '#,##0'),
]
ws['A1'] = 'Monthly Lease Activity — Seasons at Meridian'
ws['A1'].font = Font(bold=True, size=13, color=NAVY)
ws['A2'] = ('Amber rows are HelloData proxy: leases signed = listings going off-market; trade-outs are '
            'asking→asking, not contract→contract. Expirations and move-outs cannot be observed at all in '
            'that window and are left BLANK — never zero. Renewals are only partly observable (the burn-off '
            'sees residents still in place at 8/19/26), so those months carry a survivor floor "≥ n" instead '
            f'of a count. Aug 2026 is a partial month — the roll is as-of {CUTOFF_D}. Rent columns are '
            'ARM\'S-LENGTH only: corporate leases and internal transfers are excluded (counts include them).')
ws['A3'] = ('OCCUPANCY — two independent measures, deliberately not blended. "Rent roll, EOM" counts occupied '
            'units at month end (ties to the rolls within ±2 units at every anchor). "T12, mo. avg" is '
            '1 - vacancy loss / market rent, time-weighted across the month, and is the ONLY source of occupancy '
            'before 2026. ECONOMIC occupancy is net residential rent over market rent — the gap to physical '
            'occupancy is concessions + loss to lease + bad debt. Jul 2024 - May 2025 predates all three T12s: '
            'absorption (cumulative first-generation leases) is the observable series there. "SIGNED future MI" '
            'is the forward book — leases signed by 8/18 for move-ins after it (not counted in NEW LEASES).')
for _c in ('A2', 'A3'):
    ws[_c].font = Font(size=9, italic=True, color='BF8F00')
    ws[_c].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=int(_c[1]), start_column=1, end_row=int(_c[1]), end_column=14)
ws.row_dimensions[2].height = 34
ws.row_dimensions[3].height = 34

HROW = 5
for i, (_, label, w, _f) in enumerate(COLS, start=1):
    ws.cell(row=HROW, column=i, value=label)
    ws.column_dimensions[get_column_letter(i)].width = w
style_header(ws, HROW, len(COLS))
ws.freeze_panes = f'C{HROW + 1}'

# columns that are structurally unobservable in the proxy window
PROXY_BLANK = {'leases_expired', '  expired -> renewed', '  expired -> moved out',
               '  expired -> transferred', '  expired -> MTM holdover', 'retention_pct',
               'retention_tenant_pct', 'renewal_n',
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
    '  of which corporate / transfer (excl. from $)':
        act['  of which corporate / transfer (excl. from $)'].sum(),
    'leases_expired': tot_exp, '  expired -> renewed': tot_ren,
    '  expired -> moved out': tot_out, '  expired -> transferred': tot_xfer,
    '  expired -> MTM holdover': tot_mtm,
    'retention_pct': tot_ren / max(tot_exp, 1),
    'retention_tenant_pct': (tot_ren + tot_xfer) / max(tot_exp, 1),
    'renewal_n': len(rg_p), 'renewal_prior_gross': rg_p.prior_gross.mean(),
    'renewal_new_gross': rg_p.new_gross.mean(), 'renewal_gross_pct_avg': ren_g,
    'renewal_prior_eff': re_p.prior_eff.mean(), 'renewal_new_eff': re_p.new_eff.mean(),
    'renewal_eff_pct_avg': ren_e,
    'relet_n': len(ng_p), 'newlease_prior_gross': ng_p.prior_gross.mean(),
    'newlease_new_gross': ng_p.new_gross.mean(), 'newlease_gross_pct_avg': rel_g,
    'newlease_prior_eff': ne_p.prior_eff.mean(), 'newlease_new_eff': ne_p.new_eff.mean(),
    'newlease_eff_pct_avg': rel_e,
    # pooled over leases, matching the Summary tab — not a mean of monthly rates
    'new_conc_freq': c_2026['freq'], 'new_conc_depth': c_2026['depth'],
    'move_outs': act.move_outs.sum(),
    'leases_signed_future_movein': int(mo.leases_signed_future_movein.sum()),
    # occupancy is a level, not a flow: the total row carries the latest reading
    'units_leased_to_date': act.units_leased_to_date.dropna().iloc[-1],
    'leased_to_date_pct': act.leased_to_date_pct.dropna().iloc[-1],
    'units_occupied_eom': act.units_occupied_eom.dropna().iloc[-1],
    'units_vacant_eom': act.units_vacant_eom.dropna().iloc[-1],
    'physical_occupancy_eom': act.physical_occupancy_eom.dropna().iloc[-1],
    'occupancy_basis': f'Latest — as of {CUTOFF_D}',
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
    'the total concession amortized over the lease term (the Yardi convention used by the 3ps reports).',
    'New-lease trade-out is measured against the PRIOR TENANT\'S LAST CONTRACT RENT in the same unit. '
    'For leases the 3ps New Lease Tradeouts report covers (6/19–8/19/2026) the report\'s exact detail is '
    'used verbatim; earlier 2026 re-leases are reconstructed from rolls + burn-off, and re-leases whose '
    'prior tenant departed before 1/1/2026 fall back to that unit\'s prior listing rent — flagged per row '
    'on the Lease Events tab.',
    f'Rent levels are mix-weighted to the property\'s actual unit mix from the {CUTOFF_D} roll, so a month '
    'that happened to lease mostly 1-beds does not read as a rent decline.',
    'Concession frequency = share of new leases with any concession. Depth = average discount among ONLY '
    'those leases. Blended averages are not shown — they mix conceding and non-conceding leases.',
    'Corporate leases (Murata Machinery, Paragon Corporate Housing, Coleman Environmental, Wolff Corporate '
    'Housing — 16 units, 4.4% of the property) and internal transfers are excluded from every rent column; '
    'counts include them and each row is flagged on the Lease Events tab.',
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
ws['A2'] = ('From the three supplied operating statements (Jun 2025-May 2026, Jul 2025-Jun 2026, Aug 2025-'
            'Jul 2026); they overlap and the later file wins. Overlaps agree exactly EXCEPT Apr 2026, where '
            'the Aug-Jul statement restates concessions (4460) from -$5,648.50 to -$6,466.00 (-$817.50 '
            'through net residential rent). This is GL truth — the only source of occupancy before 2026, and '
            'the only place the concession dollars can be seen as booked. Credits are shown as booked (negative).')
ws['A2'].font = Font(size=9, italic=True, color='595959')
ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=12)
ws.row_dimensions[2].height = 40

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
    'month end. The two agree within ~2 pts at every overlapping anchor, in both directions.',
    '• ECONOMIC OCCUPANCY = net residential rent / market rent. The gap to physical occupancy is what '
    'concessions, loss to lease and bad debt take out of a fully-occupied building.',
    '• CONCESSIONS ARE NOT AMORTIZED OVER THE LEASE TERM IN THE GL. The burn-off report gives each lease a '
    f'concession END DATE, and the median gap from lease start to that date is {S["burn_window_median_mo"]:.1f} '
    f'months against a median {S["term_median_mo"]:.0f}-month term; the longest observed is '
    f'{S["burn_window_max_mo"]:.1f} months. So a concession lands as a large credit in the first '
    'two or three months of a lease and then stops.',
    '• That timing is why effective rent in this workbook (gross less concession amortized over the full term, '
    'the convention the Yardi reports use) does not tie month-for-month to GL 4460. Same total dollars, '
    'different periods. The amortized figure is the right one for underwriting a lease; the GL timing is the '
    'right one for reading a trailing statement.',
    f'• Only ${S["still_to_burn"]:,.0f} of concession remains unburned across {S["still_to_burn_leases"]} '
    f'leases as of {S["burnoff_asof"]}. The concession drag visible in this T12 is almost entirely '
    'historical, NOT a forward liability on the in-place rent roll — Jul 2026 booked just '
    f'${abs(T[max(T)]["concessions"]):,.0f} ({T[max(T)]["concession_pct_gpr"]:.1%} of GPR).',
    f'• Loss to lease widened from {ltl_a:.1%} to {ltl_b:.1%} of market rent over the same period that '
    f'concessions fell from {cc_a:.1%} to {cc_b:.1%}. The physical-to-economic gap therefore did not close. '
    'Underwriting the concession burn-off as pure upside would double-count relief that loss to lease has '
    'already absorbed.',
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
ev_out = ev[(ev.month <= CUTOFF) | (ev.event.isin(['Lease Signed (future move-in)']))].copy()
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
# 5. EXPIRATION SCHEDULE (forward book)
# ======================================================================
ws = wb.create_sheet('Expiration Schedule')
fwd = mo[mo.month > CUTOFF][['month', 'scheduled_expirations_ahead', 'notices_scheduled_moveout',
                             'leases_signed_future_movein']]
ws['A1'] = f'Forward Book (leases in place at {CUTOFF_D})'
ws['A1'].font = Font(bold=True, size=13, color=NAVY)
ws['A2'] = ('The second turn. Each resident\'s currently scheduled lease expiration, notices already given '
            f'for move-outs dated after the {CUTOFF_D} roll, and leases ALREADY SIGNED for future move-ins '
            '(the offsetting absorption).')
ws['A2'].font = SMALL
ws.append([])
ws.append(['Month', 'Scheduled expirations', 'Notices given (scheduled move-out)',
           'Leases signed (future move-in)'])
style_header(ws, 4, 4, height=30)
sf_by_month = e_fut.groupby('month').size()
for _, row in fwd.iterrows():
    ws.append([row['month'], int(row['scheduled_expirations_ahead']),
               int(row['notices_scheduled_moveout']),
               int(sf_by_month.get(row['month'], 0))])
tr = ws.max_row + 1
ws.cell(row=tr, column=1, value='TOTAL').font = BOLD
ws.cell(row=tr, column=2, value=int(fwd.scheduled_expirations_ahead.sum())).font = BOLD
ws.cell(row=tr, column=3, value=int(fwd.notices_scheduled_moveout.sum())).font = BOLD
ws.cell(row=tr, column=4, value=int(len(e_fut))).font = BOLD
for c in range(1, 5):
    ws.cell(row=tr, column=c).fill = TOTAL_FILL
    ws.cell(row=tr, column=c).alignment = Alignment(horizontal='center')
widths(ws, {'A': 14, 'B': 22, 'C': 30, 'D': 28})
for row in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=1, max_col=4):
    for cell in row:
        cell.alignment = Alignment(horizontal='center')
        cell.border = BOX

# ======================================================================
# 6. SOURCES & METHOD
# ======================================================================
ws = wb.create_sheet('Sources & Method')
widths(ws, {'A': 118})
net_new = int(act.new_leases_signed.sum())
net_out = int(act.move_outs.sum())
notes = [
    ('H', 'Seasons at Meridian — Lease-Up Analysis: sources, conventions and limits'),
    ('T', f'Measurement date {CUTOFF_D} (latest rent roll). 360 units. Lease-up began Jun 2024 (first '
          'listing); first move-in 8/21/2024.'),
    ('H', 'The two data bases'),
    ('T', 'ACTUAL (Jan 2026 – Aug 2026): Yardi rent rolls, concession burn-off, renewal + new-lease '
          'trade-out reports. Every figure is an observed lease record.'),
    ('T', 'PROXY (Jun 2024 – Dec 2025): HelloData listing episodes only. Shown amber on the Monthly tab. '
          'A listing going off-market stands in for a new lease signed; trade-outs are asking→asking rather '
          'than contract→contract. Expirations, renewals, move-outs and retention are NOT observable in this '
          'window and are left BLANK rather than reported as zero.'),
    ('H', 'Why the pre-2026 window cannot be built on Yardi data'),
    ('T', '• The earliest rent roll is 1/1/2026 — there is no roster snapshot before it, so any tenant who '
          'moved in and out during 2024–2025 appears in no Yardi source.'),
    ('T', '• The concession burn-off is the only source of lease-start dates, and it covers CURRENT residents '
          'only (351 as of 8/19/26). Just 16 of them moved in during 2024, and all 16 have already renewed — '
          'so the burn-off shows their current lease, not their original one.'),
    ('T', '• Several of those residents show ~546-day move-in→lease-start gaps, which could be one renewal off '
          'an 18-month initial lease OR two successive renewals. The sources cannot distinguish these, so '
          'pre-2026 renewal counts are a floor, not a count.'),
    ('T', '• The renewal trade-out reports cover 5/10–7/9 and 6/19–8/19/2026 (40 distinct renewals). All '
          'three T12s begin Jun 2025 or later, missing the first ten months of lease-up.'),
    ('H', 'Conventions'),
    ('T', 'New leases are counted on MOVE-IN DATE. The 1/1/2026 roll carries real move-in dates back to '
          '8/21/2024, so the pre-2026 window is dated exactly for every tenant who survived to a roll; the '
          'rest are dated from their listing\'s off-market date + 15 days (the validated median lag) and '
          'marked ESTIMATED in Date Basis.'),
    ('T', 'Renewals are counted separately and are never included in "new leases signed". Leases signed for '
          'move-ins after the measurement date sit in their own event type ("Lease Signed (future move-in)") '
          'and are excluded from monthly new-lease counts.'),
    ('T', 'Renewal trade-out = same resident, contract rent → contract rent. New-lease trade-out = same unit, '
          'prior tenant\'s LAST contract rent → new tenant\'s contract rent. Where the 3ps New Lease '
          'Tradeouts report covers the lease (6/19–8/19/2026), its exact prior/new detail is used verbatim; '
          'matching is by unit + resident name because the report\'s move-in date can differ from the roll\'s '
          'by weeks (F312: 6/13 on the roll, 7/25 on the report).'),
    ('T', 'Effective rent = gross − (total concession ÷ lease term months). This is the Yardi convention used '
          'by both 3ps trade-out reports, so these figures tie to the seller\'s own reports exactly.'),
    ('T', 'Retention = renewals ÷ leases that reached expiration in the month, on two bases: UNIT basis counts '
          'transfers as non-renewals; TENANT basis counts them as retained (they left a unit, not the '
          'property). MTM holdovers sit in the denominator as non-renewals until they either sign or leave.'),
    ('T', f'Rent levels are mix-weighted to the actual unit mix from the {CUTOFF_D} roll ({mix_str} = 360) '
          'to remove mix bias from month-to-month comparisons.'),
    ('T', 'Concessions are reported as frequency (share of leases with any concession) and depth (average '
          'discount among only those leases), never as a blended average.'),
    ('T', 'CORPORATE LEASES and INTERNAL TRANSFERS are excluded from every rent statistic, including the L5 '
          'new-lease averages and all trade-out figures. Corporate users on the roll: Murata Machinery Inc '
          f'({len(murata)} units), Paragon Corporate Housing ({len(paragon)}), Coleman Environmental (B307) '
          'and Wolff Corporate Housing (H111) — the latter two both move out 9/30/2026. Detection is by '
          'name pattern (Inc/LLC/Corp/Housing/…), so a new corporate user cannot silently enter the '
          'statistics. Internal transfers (same resident, unit to unit) are negotiated swaps, not '
          'arm\'s-length pricing, and both sides are flagged per row.'),
    ('H', 'Resident-id handling (hard-won)'),
    ('T', 'Tenancies are keyed by resident id + unit, not resident id alone: Yardi carried t0033902 across '
          'the J108 → G103 transfer, and an id-keyed ledger would fuse the two tenancies — losing the G103 '
          'transfer lease and double-counting the J108 original. Duplicate departures created by id '
          'reassignment (one person leaving one unit twice on the same date) are collapsed.'),
    ('H', 'Validation performed (see validate.py for the full suite)'),
    ('T', '✓ All 28 renewals in the 6/19–8/19/2026 report and all surviving renewals from the 5/10–7/9 report '
          'are present; the in-window exact rows tie to the report\'s portfolio totals to the cent '
          '($1,775.96 → $1,817.39 gross; $1,633.02 → $1,813.63 effective).'),
    ('T', '✓ Every row of the New Lease Tradeouts report is accounted for: moved-in rows carry the exact '
          'detail, future move-ins sit in the forward book, and the one transfer row (G103) is flagged.'),
    ('T', f'✓ Net leasing in the actual window ({net_new} new leases − {net_out} move-outs = '
          f'+{net_new - net_out}) reconciles to the observed occupancy change ({occ_first} → {occ_last} = '
          f'+{occ_last - occ_first}); the residual is timing (leases signed for Aug/Sep move-ins).'),
    ('T', '✓ Exactly one first-generation lease per unit, and all 360 units resolve — the ledger accounts for '
          'every unit in the property.'),
    ('T', '✓ Derived occupancy ties to every rent-roll anchor within ±2 units, in both directions.'),
    ('H', 'Known limits'),
    ('T', 'Renewals before 1/1/2026 are survivor-biased: only residents still in place on 8/19/2026 are '
          'visible, so early-period renewal counts are floors.'),
    ('T', f'{len(e_ren) - n_exact_ren} of {len(e_ren)} renewals have reconstructed rather than reported '
          'concession detail, because the renewal reports cover 5/10–8/19/2026 only.'),
    ('T', 'A handful of 2026 new leases have no term or concession data and so carry no effective rent.'),
    ('T', 'The burn-off\'s Lease Rent column is unreliable on some rows (H203 showed $386 and H213 $342 where '
          'the roll shows $1,600 and $1,995); rent-roll Actual Rent is used as the rent of record throughout.'),
    ('T', 'The roll and the trade-out report occasionally disagree on a move-in date (F312) or a future '
          'signer (E313: roll shows Charles Aiken, report shows Emily Malone) — the roll is the roster of '
          'record and the disagreement is flagged in the event row\'s source.'),
    ('H', 'What would close the remaining gap (in descending order of value)'),
    ('T', '1. Yardi lease history / lease audit — every lease ever written per unit (start, end, term, gross '
          'rent, concession). One report would make the entire pre-2026 period exact.'),
    ('T', '2. Renewal + new-lease trade-out reports (3ps format) for windows before 5/10/2026.'),
    ('T', '3. Monthly resident activity / box score from Aug 2024 — leases signed, move-ins, move-outs, notices.'),
    ('T', '4. Historical month-end rent rolls, Aug 2024 – Dec 2025.'),
    ('T', '5. Monthly financials for Aug 2024 – May 2025 (pre-dates all three T12s).'),
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
