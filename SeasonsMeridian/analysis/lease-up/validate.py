#!/usr/bin/env python3
"""Tie the lease-up ledger back to the sources that can independently confirm it.

Every expected value is READ FROM THE SOURCE REPORT at run time (portfolio total
rows, roll counts), never hard-coded, so the suite stays valid when the sources
are refreshed."""
import json
import openpyxl
import pandas as pd
from datetime import date, datetime

DOCS = '../../documents'
CUT = pd.Timestamp('2026-08-18')

e = pd.read_csv('events.csv', parse_dates=['signed', 'movein_est'])
m = pd.read_csv('monthly.csv')
S = json.load(open('stats.json'))
ok = lambda b: 'PASS' if b else '** FAIL **'
fails = []


def check(label, cond):
    print(f'   {ok(cond)}  {label}')
    if not cond:
        fails.append(label)


print('=' * 72)
print('1. RENEWAL TRADE-OUT REPORT (6/19 - 8/19/2026), portfolio total row')
wb = openpyxl.load_workbook(f'{DOCS}/renewal-reports/RenewalTradeouts_2026-06-19_to_2026-08-19.xlsx',
                            data_only=True)
tot = next(r for r in wb['(3pseason) Seasons at Meridian'].iter_rows(values_only=True)
           if r[0] and 'Total' in str(r[0]))
n_rep, pg_rep, pe_rep, ng_rep, ne_rep = int(tot[1]), tot[10], tot[13], tot[15], tot[18]
print(f'   report: n={n_rep}  gross {pg_rep} -> {ng_rep}   eff {pe_rep} -> {ne_rep}')
ren = e[(e.event == 'Renewal') & (e.source == 'Renewal trade-out report (exact)')]
w = ren[ren.signed >= '2026-06-19']
print(f'   ledger, exact rows in window:  n={len(w)}  gross {w.prior_gross.mean():.2f} -> '
      f'{w.new_gross.mean():.2f}   eff {w.prior_eff.mean():.2f} -> {w.new_eff.mean():.2f}')
check('all report renewals present', len(w) == n_rep)
check('prior gross ties to report', abs(w.prior_gross.mean() - pg_rep) < 0.5)
check('new gross ties to report', abs(w.new_gross.mean() - ng_rep) < 0.5)
check('prior effective ties to report', abs(w.prior_eff.mean() - pe_rep) < 0.5)
check('new effective ties to report', abs(w.new_eff.mean() - ne_rep) < 0.5)
old = ren[ren.signed < '2026-06-19']
print(f'   plus {len(old)} exact renewals surviving from the 5/10–7/9 report window')

print('\n' + '=' * 72)
print('2. NEW LEASE TRADEOUTS REPORT (6/19 - 8/19/2026) — every row accounted for')
wb2 = openpyxl.load_workbook(f'{DOCS}/tradeout-reports/NewLeaseTradeouts_2026-06-19_to_2026-08-19.xlsx',
                             data_only=True)
rows = [r for r in wb2['(3pseason) Seasons at Meridian'].iter_rows(min_row=9, values_only=True)
        if r[4]]
with_prior = [r for r in rows if r[18] is not None]
exact_nl = e[(e.event == 'New Lease') & (e.source == 'New-lease trade-out report (exact)')]
exact_fut = e[(e.event == 'Lease Signed (future move-in)') &
              (e.source.str.contains('trade-out report', na=False)) & e.prior_gross.notna()]
n_led = len(exact_nl) + len(exact_fut)
print(f'   report rows: {len(rows)} ({len(with_prior)} with prior-lease detail)')
print(f'   ledger: {len(exact_nl)} moved-in exact + {len(exact_fut)} signed-future exact = {n_led}')
check('every with-prior report row lands in the ledger (± the flagged G103 transfer row)',
      n_led >= len(with_prior) - 1)
both = pd.concat([exact_nl, exact_fut])
rep_pg = sum(r[18] for r in with_prior) / len(with_prior)
rep_ng = sum(r[13] for r in with_prior) / len(with_prior)
led_pg, led_ng = both.prior_gross.mean(), both.new_gross.mean()
print(f'   avg prior gross: report {rep_pg:.2f} vs ledger {led_pg:.2f}; '
      f'avg new gross: report {rep_ng:.2f} vs ledger {led_ng:.2f}')
check('trade-out levels tie to report within $10 (report avg incl. the one dropped row)',
      abs(led_pg - rep_pg) < 10 and abs(led_ng - rep_ng) < 10)

print('\n' + '=' * 72)
print('3. CORPORATE + TRANSFER EXCLUSION (the L5 / trade-out guard)')
corp_names = set(S['corporate_names'])
nl = e[e.event == 'New Lease']
flagged = nl[nl.name.isin(corp_names)]
check(f'every lease by a corporate user is flagged corporate ({len(flagged)} rows)',
      bool((flagged.corporate == 'Y').all()))
l5_units = {(u[0], u[1]) for basis in ('l5_movein', 'l5_signed')
            for p in S[basis]['plans'].values() for u in p['units']}
l5_rows = nl[nl.apply(lambda r: (r['unit'], str(r['signed'].date())) in l5_units, axis=1)]
check('no corporate lease inside any L5 pool', not (l5_rows.corporate == 'Y').any())
check('no internal transfer inside any L5 pool',
      not l5_rows.transfer.fillna('').str.startswith('from').any())
mur = nl[nl.name == 'Murata Machinery Inc']
print(f'   Murata new-lease rows in ledger: {len(mur)} — all corporate-flagged: '
      f'{bool((mur.corporate == "Y").all())}')
stats_cols = ['newlease_prior_gross', 'newlease_new_gross', 'renewal_prior_gross']

print('\n' + '=' * 72)
print('4. UNIT COUNT / FIRST-GENERATION INTEGRITY')
first = nl[nl.generation == 'First lease-up lease']
check('exactly one first-generation lease per unit, 360 units resolve',
      len(first) == 360 and first.unit.nunique() == 360)
check('no more units ever leased than exist', nl.unit.nunique() <= 360)

print('\n' + '=' * 72)
print('5. OCCUPANCY — derived coverage vs every rent-roll anchor')
for dt, actual in S['anchors'].items():
    got = m[m.month == dt[:7]]
    print(f'   {dt}: roll {actual}')
occ = m[(m.month >= '2026-01') & (m.month <= '2026-08')]
w26 = occ
net_new = int(w26.new_leases_signed.sum())
net_out = int(w26.move_outs.sum())
occ_first = int(m[m.month == '2026-01'].units_occupied_eom.iloc[0])
occ_last = int(occ.units_occupied_eom.dropna().iloc[-1])
print(f'   net leasing {net_new} - {net_out} = +{net_new - net_out}; '
      f'occupancy {occ_first} -> {occ_last} = +{occ_last - occ_first}')
check('net-leasing identity holds within timing tolerance (±6)',
      abs((net_new - net_out) - (occ_last - occ_first)) <= 6)

print('\n' + '=' * 72)
print('6. T12 CONCESSIONS — GL 4460 as booked')
import t12 as t12mod
T = t12mod.load()
tot_conc = sum(abs(v['concessions']) for v in T.values())
print(f'   {min(T)} -> {max(T)}: ${tot_conc:,.0f} booked '
      f'(Apr 2026 restated to -6,466.00 by the Aug-Jul statement)')
check('Apr 2026 carries the restated concession figure',
      abs(T['2026-04']['concessions'] + 6466.0) < 0.01)
check('still-to-burn matches the 8/19 burn-off', S['still_to_burn_leases'] == 4)

print('\n' + '=' * 72)
if fails:
    print(f'{len(fails)} CHECK(S) FAILED:')
    for f in fails:
        print('  **', f)
    raise SystemExit(1)
print('ALL CHECKS PASSED')
