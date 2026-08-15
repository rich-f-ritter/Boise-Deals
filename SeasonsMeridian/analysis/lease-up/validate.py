#!/usr/bin/env python3
"""Tie the lease-up ledger back to the sources that can independently confirm it."""
import pandas as pd
from datetime import date

e = pd.read_csv('events.csv', parse_dates=['signed', 'movein_est'])
m = pd.read_csv('monthly.csv')
ok = lambda b: 'PASS' if b else '** FAIL **'

print('=' * 72)
print('1. RENEWAL TRADE-OUT REPORT (5/10/2026 - 7/9/2026), portfolio total row')
print('   report: n=23  prior gross 1762.91 -> new 1793.26 (+1.7%)')
print('           prior eff 1639.44 -> new eff 1789.92 (+9.2%)')
r = e[(e.event == 'Renewal') & (e.signed >= '2026-05-10') & (e.signed <= '2026-07-09')]
exact = r[r.source.str.startswith('Renewal trade-out')]
print(f'\n   ledger, same window:            n={len(r)}  (of which exact-from-report n={len(exact)})')
for lbl, sub in (('exact rows only', exact), ('all rows in window', r)):
    pg, ng = sub.prior_gross.mean(), sub.new_gross.mean()
    pe, ne = sub.prior_eff.mean(), sub.new_eff.mean()
    print(f'   {lbl:22} gross {pg:7.2f} -> {ng:7.2f} ({(ng/pg-1)*100:+.1f}%)   '
          f'eff {pe:7.2f} -> {ne:7.2f} ({(ne/pe-1)*100:+.1f}%)')
print(f'\n   {ok(len(exact) == 23)}  all 23 report renewals present')
print(f'   {ok(abs(exact.prior_gross.mean() - 1762.91) < 0.5)}  prior gross ties to report')
print(f'   {ok(abs(exact.new_gross.mean() - 1793.26) < 0.5)}  new gross ties to report')
print(f'   {ok(abs(exact.prior_eff.mean() - 1639.44) < 0.5)}  prior effective ties to report')
print(f'   {ok(abs(exact.new_eff.mean() - 1789.92) < 0.5)}  new effective ties to report')

print('\n' + '=' * 72)
print('2. UNIT COUNT / OCCUPANCY')
print('   360 units; occupancy 314/360 on 1/1/26, 346/360 on 8/4/26 (DATA_NOTES)')
nl = e[e.event == 'New Lease']
print(f'   distinct units ever leased in ledger: {nl.unit.nunique()}  (property has 360)')
print(f'   {ok(nl.unit.nunique() <= 360)}  no more units leased than exist')
first = nl[nl.generation == 'First lease-up lease']
print(f'   first-generation leases: {len(first)} across {first.unit.nunique()} units')
print(f'   {ok(len(first) <= 360 and first.unit.nunique() == len(first))}  '
      f'at most one first-generation lease per unit')
# Move-outs are only observable from the 1/1/26 roll forward, so a cumulative
# net-lease identity cannot hold across the full period. Test it where it can hold.
w = m[(m.month >= '2026-01') & (m.month <= '2026-08')]
print(f'\n   within the ACTUAL window only (Jan-Aug 2026):')
print(f'   new leases {w.new_leases_signed.sum()}, move-outs {w.move_outs.sum()}, '
      f'net {w.new_leases_signed.sum() - w.move_outs.sum():+d}')
print(f'   occupancy moved 314 -> 346 = +32 over the same window')
print(f'   {ok(abs((w.new_leases_signed.sum() - w.move_outs.sum()) - 32) <= 12)}  '
      f'net leasing reconciles to the occupancy change within tolerance')
print('   (tolerance absorbs leases signed for Aug/Sep move-ins not yet occupied on 8/4)')

print('\n' + '=' * 72)
print('3. RENEWAL COUNT vs CONCESSION BURN-OFF (7/30/26: 64 residents w/ lease start > move-in)')
print(f'   ledger renewals: {(e.event == "Renewal").sum()}')
print(f'   {ok((e.event == "Renewal").sum() == 64)}  matches burn-off renewal count')

print('\n' + '=' * 72)
print('4. FIRST-TURN ANALYSIS CROSS-CHECK (1/1/26 cohort, measured to 8/4/26)')
print('   prior deliverable: 64 renewals, +1.5% gross / +9.5% eff')
print('                      92 re-leases, +5.2% gross / +10.7% eff')
rr = e[e.event == 'Renewal']
print(f'   ledger all renewals:  n={len(rr)}  gross {(rr.new_gross.mean()/rr.prior_gross.mean()-1)*100:+.1f}%'
      f'  eff {(rr.new_eff.mean()/rr.prior_eff.mean()-1)*100:+.1f}%')
rl = e[(e.event == 'New Lease') & (e.generation == 'Re-lease') & (e.signed >= '2026-01-01')]
print(f'   ledger 2026 re-leases: n={len(rl)}  gross {(rl.new_gross.mean()/rl.prior_gross.mean()-1)*100:+.1f}%'
      f'  eff {(rl.new_eff.mean()/rl.prior_eff.mean()-1)*100:+.1f}%')
print('   (ledger covers all re-leases incl. those whose prior tenant left before 1/1/26,')
print('    so n exceeds the prior cohort-limited deliverable — expected)')

print('\n' + '=' * 72)
print('5. COVERAGE / DATA-QUALITY FLAGS')
tot_nl = len(nl)
print(f'   new-lease events: {tot_nl}   with a prior-rent baseline: {nl.prior_gross.notna().sum()}')
print(f'   of those, baseline is a PROXY listing rent: '
      f'{nl.prior_basis.fillna("").str.startswith("PROXY").sum() + len(nl[nl.basis.str.startswith("PROXY")].dropna(subset=["prior_gross"]))}')
print(f'   renewals with exact report detail: {len(exact)} of {(e.event=="Renewal").sum()} '
      f'({len(exact)/(e.event=="Renewal").sum():.0%})')
print(f'   effective rent computable: renewals {rr.new_eff.notna().sum()}/{len(rr)}, '
      f'new leases {nl.new_eff.notna().sum()}/{tot_nl}')
miss = nl[nl.new_eff.isna() & (nl.signed >= '2026-01-01')]
print(f'   2026 new leases missing effective rent: {len(miss)} (no term or concession data)')
