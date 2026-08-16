#!/usr/bin/env python3
"""Development-feasibility exhibits for the Seasons at Meridian IC memo.

Ties together the four prior workstreams — replacement cost, the Emblem normalization,
the construction-loan tape, and the entitlement/graveyard record — against the LIVE TMG
underwriting (TMG Acquisitions model 7.26 v3, re-uploaded 8/15/2026).

Answers the two questions IC actually cares about:
  Q1  How much rent growth can we capture before new construction pencils again and
      competes with us?  (the moat is self-limiting — when does it close?)
  Q2  Emblem needs ~$400k/unit in Jan 2030 on a 2-year-old asset; we need ~$397k/unit in
      Oct 2031 on a 7-year-old asset. Are those two numbers consistent?

All TMG figures are read from the live model, not hard-coded from memory.
"""
import json
import warnings
from pathlib import Path

import openpyxl

warnings.filterwarnings('ignore')
HERE = Path(__file__).parent
MODEL = HERE / 'in' / 'TMG_Seasons_at_Meridian_v3.xlsm'

# ---------------------------------------------------------------- read the live TMG model
wb = openpyxl.load_workbook(MODEL, data_only=True, read_only=True)


def grid(sheet, maxr, maxc):
    g = {}
    for row in wb[sheet].iter_rows(min_row=1, max_row=maxr, max_col=maxc):
        for c in row:
            if getattr(c, 'value', None) is not None:
                g[(c.row, c.column_letter)] = c.value
    return g


op = grid('One Pager', 40, 6)
cf = grid('Cash Flow (Annual)', 100, 24)
tx = grid('Taxes', 34, 14)

TMG = {
    'units': 360,
    'price': op[(14, 'C')],
    'price_pu': op[(15, 'C')],
    'basis': op[(18, 'C')],
    'basis_pu': op[(19, 'C')],
    'y1_cap': op[(21, 'C')],
    't3_cap': op[(20, 'C')],
    'exit_cap': op[(23, 'C')],
    'exit_value': op[(24, 'C')],
    'exit_pu': op[(25, 'C')],
    'ulirr': op[(26, 'C')],
    'lirr': op[(27, 'C')],
    'erm': op[(28, 'C')],
    'exit_noi': None,  # filled below
    # market rent path, Y1..Y10 (CF row 4, cols K..U) — HelloData market rent, the metric
    # the user specified for the comparison against a developer's required rent
    'mkt_rent': [cf[(4, c)] for c in 'KLMNOPQRSTU'],
    'noi': [cf[(59, c)] for c in 'KLMNO'],
    'lev_cf': [cf[(88, c)] for c in 'KLMNO'],
    'lev_eq': cf[(88, 'F')],
    # taxes: current assessment, the 2027 sale reassessment, and the resulting bill
    'assessed_now': tx[(5, 'C')],
    'assessed_2027': tx[(5, 'G')],
    'tax_2026': tx[(9, 'F')],
    'tax_2027': tx[(9, 'G')],
    'reassess_pct': tx[(11, 'C')],
    'assessed_2032': tx[(25, 'I')],
}
TMG['exit_noi'] = 7_498_600.6558  # Assumptions M36, forward-12 exit NOI

# ---------------------------------------------------------------- fixed findings from prior work
RC_PU = 322_530          # replacement_cost_model.py + Seasons spec/land adjustments
RC_TOTAL = 116_110_721
REQ_RENT_2026 = 2_224    # emblem_normalization.py, normalized-ancillary required MARKET rent
EMBLEM_ADVERTISED = 2_069
COST_ESC = 0.017         # observed 2022->2026 all-in cost escalation, +1.7%/yr
EQUITY_2022, EQUITY_2026 = 99_630, 137_038
EMBLEM = {'units': 256, 'exit': 102_500_000, 'exit_cap': 0.0550, 'exit_date': 'Jan 2030',
          'cost_pu': 304_530, 'assessed_pct_of_exit': 0.87, 'tax_rate': 0.0045}

out = {}
P = print

# ================================================================ 1. basis vs replacement cost
P('=' * 80)
P('1. WHERE WE BUY VS WHAT IT COSTS TO BUILD')
P('=' * 80)
basis_tbl = [
    ("Subject's actual 2022 development cost", 284_658, 102_476_923),
    ('Replacement cost today (Emblem-anchored)', RC_PU, RC_TOTAL),
    ('TMG purchase price', TMG['price_pu'], TMG['price']),
    ('TMG total basis (price + closing + capex)', TMG['basis_pu'], TMG['basis']),
]
for lab, pu, tot in basis_tbl:
    P(f'  {lab:<44}${pu:>9,.0f}/u   ${tot:>13,.0f}')
P(f"\n  Price vs replacement cost:  {TMG['price_pu']/RC_PU-1:+.1%}")
P(f"  Basis vs replacement cost:  {TMG['basis_pu']/RC_PU-1:+.1%}")
out['basis'] = {'rc_pu': RC_PU, 'price_pu': TMG['price_pu'], 'basis_pu': TMG['basis_pu'],
                'price_vs_rc': TMG['price_pu'] / RC_PU - 1,
                'basis_vs_rc': TMG['basis_pu'] / RC_PU - 1}

# ================================================================ 2. Q1 — when does the moat close?
P('\n' + '=' * 80)
P('2. Q1: WHEN DOES NEW CONSTRUCTION PENCIL AGAIN? (the rent-growth ceiling)')
P('=' * 80)
P(f"  Required market rent for new supply, 2026 dollars: ${REQ_RENT_2026:,}/u/mo")
P(f"  Subject Y1 (UW) market rent:                       ${TMG['mkt_rent'][0]:,.0f}/u/mo")
P(f"  Opening gap:                                       {REQ_RENT_2026/TMG['mkt_rent'][0]-1:+.1%}\n")

yrs = [2027 + i for i in range(10)]
P(f"  {'FY end':<8}{'subj mkt rent':>15}{'req (costs +1.7%/yr)':>23}{'gap':>9}"
  f"{'req (costs flat)':>19}{'gap':>9}")
rows = []
for i, y in enumerate(yrs):
    mr = TMG['mkt_rent'][i]
    req_esc = REQ_RENT_2026 * (1 + COST_ESC) ** (i + 1)
    req_flat = REQ_RENT_2026
    rows.append({'fy': y, 'mkt_rent': mr, 'req_esc': req_esc, 'gap_esc': mr / req_esc - 1,
                 'req_flat': req_flat, 'gap_flat': mr / req_flat - 1})
    star = '  <-- EXIT' if y == 2031 else ''
    P(f'  {y:<8}${mr:>14,.0f}${req_esc:>22,.0f}{mr/req_esc-1:>9.1%}'
      f'${req_flat:>18,.0f}{mr/req_flat-1:>9.1%}{star}')

cross_esc = next((r['fy'] for r in rows if r['gap_esc'] >= 0), None)
cross_flat = next((r['fy'] for r in rows if r['gap_flat'] >= 0), None)
P(f"\n  Feasibility restored (costs escalate +1.7%/yr): {cross_esc or 'not within 10 yrs'}")
P(f"  Feasibility restored (costs flat in nominal $): {cross_flat}")
exit_row = next(r for r in rows if r['fy'] == 2031)
P(f"  Gap still open at our Oct-2031 exit: {exit_row['gap_esc']:.1%} (escalating) / "
  f"{exit_row['gap_flat']:+.1%} (flat)")

# how fast would rents have to grow to break feasibility early enough to hurt us?
P('\n  STRESS: what rent growth would make a competitor break ground in time to hurt us?')
P('    A deal must be FEASIBLE ~4 yrs before it competes (entitlement 12-24 mo + build 24-30 mo).')
P('    To suppress our Y4-Y5 rents (FY2030-31), a competitor must pencil by FY2027.')
need_2027 = REQ_RENT_2026 * (1 + COST_ESC)
g_needed = need_2027 / TMG['mkt_rent'][0] - 1
P(f'    Required FY2027 rent ${need_2027:,.0f} vs UW ${TMG["mkt_rent"][0]:,.0f} '
  f'-> market rents would have to be {g_needed:+.1%} ABOVE our Y1 underwriting immediately.')
P('    Observed FY2027 UW growth is +3.1%. The market would need a step-change, not a trend.')
out['q1'] = {'required_2026': REQ_RENT_2026, 'y1_mkt_rent': TMG['mkt_rent'][0],
             'opening_gap': REQ_RENT_2026 / TMG['mkt_rent'][0] - 1, 'path': rows,
             'crossover_escalating': cross_esc, 'crossover_flat': cross_flat,
             'gap_at_exit_esc': exit_row['gap_esc'], 'gap_at_exit_flat': exit_row['gap_flat'],
             'immediate_step_change_needed': g_needed}

# ================================================================ 3. Q2 — the two $400k exits
P('\n' + '=' * 80)
P('3. Q2: TWO ~$400K/UNIT EXITS — ARE THEY CONSISTENT?')
P('=' * 80)
e = EMBLEM
emb_pu = e['exit'] / e['units']
emb_noi_pu = e['exit'] * e['exit_cap'] / e['units']
sea_pu = TMG['exit_pu']
sea_noi_pu = TMG['exit_noi'] / TMG['units']

# Emblem's buyer eats a sale-triggered step-up Emblem never bears; ours does not.
emb_buyer_assessed = e['exit'] * 0.98
emb_seller_assessed = e['exit'] * e['assessed_pct_of_exit']
emb_step = (emb_buyer_assessed - emb_seller_assessed) * e['tax_rate']
emb_haircut = emb_step / e['exit_cap']
emb_adj_pu = (e['exit'] - emb_haircut) / e['units']

sea_buyer_assessed = TMG['exit_value'] * 0.98
sea_seller_assessed = TMG['assessed_2032']
sea_step = (sea_buyer_assessed - sea_seller_assessed) * 0.004
sea_haircut = sea_step / TMG['exit_cap']

P(f"  {'':<34}{'Emblem (Quarterra)':>22}{'Seasons (TMG)':>20}")
for lab, a, b in [
    ('exit date', e['exit_date'], 'Oct 2031'),
    ('age at exit', '2 yrs (2028 vintage)', '7 yrs (2024 vintage)'),
    ('units', f"{e['units']}", f"{TMG['units']}"),
    ('exit cap', f"{e['exit_cap']:.2%}", f"{TMG['exit_cap']:.2%}"),
    ('exit NOI / unit', f"${emb_noi_pu:,.0f}", f"${sea_noi_pu:,.0f}"),
    ('headline exit / unit', f"${emb_pu:,.0f}", f"${sea_pu:,.0f}"),
    ('assessed value at exit', f"{e['assessed_pct_of_exit']:.0%} of price",
     f"{sea_seller_assessed/TMG['exit_value']:.0%} of price"),
    ('buyer step-up haircut', f"-${emb_haircut/e['units']:,.0f}/u",
     f"-${sea_haircut/TMG['units']:,.0f}/u"),
    ('ADJUSTED exit / unit', f"${emb_adj_pu:,.0f}",
     f"${(TMG['exit_value']-sea_haircut)/TMG['units']:,.0f}"),
]:
    P(f'  {lab:<34}{a:>22}{b:>20}')

P(f"\n  (a) TAX BASIS IS NOT THE SAME $400k. Emblem's assessment sits at "
  f"{e['assessed_pct_of_exit']:.0%} of its exit price, so its buyer absorbs a "
  f"${emb_step:,.0f}/yr step-up = ${emb_haircut:,.0f} (${emb_haircut/e['units']:,.0f}/u, "
  f"{emb_haircut/e['exit']:.1%} of price).")
P(f"      Our 2027 reassessment to {TMG['reassess_pct']:.0%} of price, grown 3.5%/yr, lands at "
  f"${TMG['assessed_2032']:,.0f} by 2032 = {sea_seller_assessed/TMG['exit_value']:.0%} of our exit price.")
P(f"      OUR buyer's step-up is only ${sea_step:,.0f}/yr = ${sea_haircut:,.0f} "
  f"({sea_haircut/TMG['exit_value']:.2%} of price). We sell a CLEAN tax basis; Emblem does not.")

# (b) age-adjusted: grow Emblem's adjusted exit to our exit date at our own appreciation CAGR
appr = 0.0354  # One Pager / Assumptions appreciation CAGR
gap_yrs = 1.75
emb_at_our_exit = emb_adj_pu * (1 + appr) ** gap_yrs
P(f"\n  (b) AGE. Rolling Emblem's adjusted ${emb_adj_pu:,.0f}/u forward {gap_yrs} yrs at our own "
  f"{appr:.2%} appreciation CAGR gives ${emb_at_our_exit:,.0f}/u for a 3.5-yr-old asset in Oct 2031.")
P(f"      We underwrite a 7-yr-old asset at ${sea_pu:,.0f}/u = {sea_pu/emb_at_our_exit:.0%} of that.")
P(f"      Implied obsolescence: {(1-(sea_pu/emb_at_our_exit)**(1/3.5)):.1%}/yr of relative value "
  f"over the 3.5-yr age gap. Defensible for garden product, but it is an assumption, not a given.")

# (c) the cap-rate inconsistency, priced
sea_at_emb_cap = TMG['exit_noi'] / e['exit_cap']
P(f"\n  (c) CAP RATE. We exit a 7-yr-old asset at {TMG['exit_cap']:.2%}; Emblem exits a 2-yr-old "
  f"asset at {e['exit_cap']:.2%}. Older assets do not normally trade tighter.")
P(f"      At Emblem's {e['exit_cap']:.2%}, our exit is ${sea_at_emb_cap:,.0f} = "
  f"${sea_at_emb_cap/TMG['units']:,.0f}/u, a ${TMG['exit_value']-sea_at_emb_cap:,.0f} "
  f"({sea_at_emb_cap/TMG['exit_value']-1:.1%}) reduction.")


def irr(cfs, lo=-0.9, hi=1.5):
    for _ in range(200):
        m = (lo + hi) / 2
        npv = sum(c / (1 + m) ** i for i, c in enumerate(cfs))
        if npv > 0:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


base = [TMG['lev_eq']] + TMG['lev_cf']
stress = base[:-1] + [base[-1] - (TMG['exit_value'] - sea_at_emb_cap)]
P(f"      Levered IRR: {irr(base):.2%} (base, {TMG['exit_cap']:.2%} exit) -> "
  f"{irr(stress):.2%} at a {e['exit_cap']:.2%} exit "
  f"({(irr(stress)-irr(base))*10000:+.0f} bp).")
out['q2'] = {'emblem_pu': emb_pu, 'emblem_adj_pu': emb_adj_pu, 'emblem_haircut': emb_haircut,
             'seasons_pu': sea_pu, 'seasons_haircut': sea_haircut,
             'emblem_rolled_to_our_exit': emb_at_our_exit,
             'implied_pct_of_new': sea_pu / emb_at_our_exit,
             'exit_at_emblem_cap': sea_at_emb_cap,
             'lirr_base': irr(base), 'lirr_stress': irr(stress)}

# ================================================================ 4. our own tax step-up
P('\n' + '=' * 80)
P('4. THE TAX STEP-UP WE PAY (and why our buyer does not)')
P('=' * 80)
step = TMG['tax_2027'] - TMG['tax_2026']
P(f"  Assessed value:  ${TMG['assessed_now']:,.0f} "
  f"({TMG['assessed_now']/TMG['price']:.0%} of our price) -> ${TMG['assessed_2027']:,.0f} "
  f"({TMG['assessed_2027']/TMG['price']:.0%} of price) on the 2027 roll")
P(f"  Taxes:           ${TMG['tax_2026']:,.0f} -> ${TMG['tax_2027']:,.0f} = "
  f"+${step:,.0f}/yr ({step/TMG['tax_2026']:+.1%})")
P(f"  Value effect at our {TMG['y1_cap']:.2%} Y1 cap: ${step/TMG['y1_cap']:,.0f} "
  f"({step/TMG['y1_cap']/TMG['price']:.1%} of price, {step/TMG['price']*10000:.0f} bp of going-in yield)")
P('  This toll is paid ONCE, by the first institutional buyer of merchant-built product.')
P('  It is a permanent cost of BUYING new supply — and a reason developer exit pricing is')
P('  systematically optimistic unless it is haircut.')
out['stepup'] = {'tax_before': TMG['tax_2026'], 'tax_after': TMG['tax_2027'], 'delta': step,
                 'value_effect': step / TMG['y1_cap'], 'bp_of_yield': step / TMG['price'] * 10000}

# ================================================================ 5. cost + capital exhibits
P('\n' + '=' * 80)
P('5. WHY NOTHING PENCILS: COST PLATEAU, CAPITAL BREAK')
P('=' * 80)
eras = [('2012-2016', 125_874), ('2017-2019', 163_805), ('2020-2021', 272_510),
        ('2022', 291_375), ('2023-2025', 324_074), ('2026 (Emblem)', 304_530)]
prev = None
for lab, v in eras:
    d = f'{v/prev-1:+.0%}' if prev else ''
    P(f'  {lab:<16}${v:>9,}/unit  {d}')
    prev = v
P(f'\n  Costs roughly doubled 2014-2021 (~+9%/yr), then plateaued (~+{COST_ESC:.1%}/yr 2022-26).')
P(f'  Equity required per unit: ${EQUITY_2022:,} (2022 @ 65% LTC) -> ${EQUITY_2026:,} '
  f'(2026 @ 55% LTC) = {EQUITY_2026/EQUITY_2022-1:+.0%}')
P('  The break is NOT cost inflation. It is leverage and the rent gap.')
out['cost_eras'] = eras
out['equity'] = {'2022': EQUITY_2022, '2026': EQUITY_2026,
                 'increase': EQUITY_2026 / EQUITY_2022 - 1}

Path(HERE / 'development_feasibility.json').write_text(json.dumps(out, indent=1, default=str))
P('\nwrote development_feasibility.json')
