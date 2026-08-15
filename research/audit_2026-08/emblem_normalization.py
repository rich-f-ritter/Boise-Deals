#!/usr/bin/env python3
"""Vet the Emblem Meridian proforma and solve for the market rent new supply REALLY needs.

Emblem's own book advertises $2,069/mo market rent and a 6.65-6.80% yield on cost. That
rent is only achievable because the proforma carries ~$351/unit/month of ancillary income —
roughly 83% more than the subject actually collects. Normalize the ancillary stack to what
the submarket demonstrably supports and the required BASE MARKET RENT rises materially.

Comparison is MARKET rent vs MARKET rent (not contract/effective) because market rent is
what drives a developer's proforma and is the metric Seasons is underwritten on.

Sources: Emblem Meridian merchant model (A-OperBgt, Operating Inputs, Tax Study Input, S&U);
TMG Acquisitions model 7.26 - Seasons at Meridian v3 (Operating Proforma, Taxes, One Pager).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------- inputs (hard-coded from the two models)
EMBLEM = {
    'units': 256, 'avg_sf': 939, 'total_cost': 77_959_624,
    'input_date': '2026-06-01',
    # at input date (2026 dollars)
    'base_rent_2026': 2068.81,
    'recurring_2026': 301.01,          # garage 86.72 + pet 10.50 + RUBS 95.79 + wifi 108.00
    'other_income_2026': 49.58,
    'recurring_detail_2026': {'garage_parking': 86.72, 'pet_fees': 10.50,
                              'rubs_utility_billback': 95.79, 'managed_wifi': 108.00},
    # stabilized year 2030 (first full year), from A-OperBgt
    'y2030': {'base_rent': 7_174_539, 'recurring': 1_034_405, 'other': 170_391,
              'ltl': -185_781, 'vacancy': -639_489, 'concessions': -131_083,
              'egi': 7_422_981, 'opex': 2_119_931, 'noi': 5_303_051},
    'exit_value': 102_500_000, 'exit_cap': 0.0550,
    # Tax Study Input tab: (tax_year, assumed % complete, ACTUAL cumulative construction %, assumed improvement value)
    'tax_study': {
        'improvement_value_complete': 78_038_600,
        'ramp': [(2029, 0.27, 0.4659, 14_797_000), (2030, 0.73, 0.9900, 51_731_000)],
        'assessed_stabilized': 89_670_000, 'taxes_stabilized': 423_134,
        'direct_assessments': 19_000, 'sale_reassessment_pct': 0.98,
        # normalized stabilized-year tax if the assessor kept pace with construction
        'normalized_stab_year_delta': 67_719,
    },
    'opex_2030_detail': {'taxes': 338_975, 'insurance': 123_184, 'personnel': 448_377,
                         'utilities': 349_208, 'contracts': 241_564, 'admin': 119_228,
                         'marketing': 100_864, 'r_and_m': 123_659, 'mgmt_fee': 222_689,
                         'reserves': 51_901},
}

SEASONS = {
    'units': 360, 'avg_sf': 931,
    # TMG Operating Proforma, T12 ending 6/30/2026 and trailing-6 annualized
    'market_rent_t12': 1752, 'market_rent_t6': 1796, 'market_rent_ye2026': 1818,
    'other_income_t12': 829_157, 'other_income_t6_ann': 921_526,
    'other_income_detail_t12': {'other_income': 220_096, 'rubs': 197_042,
                                'parking': 111_765, 'revenue_share': 300_254},
    'opex_t12': 2_018_751, 'taxes_t12': 384_244, 'insurance_t12': 117_993,
    'noi_t12': 4_725_317, 'expense_ratio_t12': 0.2993,
    # TMG Taxes tab + One Pager
    'assessed_2026': 92_993_300, 'reassessed_2027': 115_640_000,   # = 98% of price
    'purchase_price': 118_000_000,
    'tax_rate_uw': 0.0045, 'total_basis': 120_100_902,
    'actual_cost_2022': 102_476_923,   # $66.61M loan / 0.65 — ties to reported "$100M-plus"
}

# ---------------------------------------------------------------- 1. normalize the ancillary stack
# Each component: what Emblem assumes, what Seasons actually collects, what is defensible.
NORMALIZATION = [
    {'item': 'Garage / covered parking', 'emblem': 86.72, 'seasons': 25.87, 'normalized': 45.00,
     'why': 'Emblem charges 536 spaces (2.09/unit) at $41.42 — i.e. nearly every stall is paid. '
            'Suburban Meridian garden competes against free surface parking; defensible is '
            'detached/tuck-under garages at ~$100/mo with ~45% penetration.'},
    {'item': 'RUBS / utility billback', 'emblem': 95.79, 'seasons': 45.61, 'normalized': 65.00,
     'why': '$95.79 is ~100% recovery of a ~$114/unit utility load. New construction with full '
            'submetering can beat the subject, but 100% recovery is not achievable; 55-70% is market.'},
    {'item': 'Managed WiFi (bulk internet)', 'emblem': 108.00, 'seasons': 0.00, 'normalized': 45.00,
     'why': 'Gross bulk-internet charge carries an offsetting ISP cost sitting in utilities '
            '(Emblem utilities run $114/u/mo vs the subject $66). Only the net margin is comparable; '
            'the subject books its cable/internet economics inside Revenue Share.'},
    {'item': 'Pet fees', 'emblem': 10.50, 'seasons': 0.00, 'normalized': 10.50,
     'why': 'Market; the subject books pet income inside Other Income.'},
    {'item': 'Other income (fees, admin, storage)', 'emblem': 49.58, 'seasons': 50.95, 'normalized': 50.00,
     'why': 'In line with the subject already.'},
    {'item': '— subject Revenue Share (cable/internet/etc.)', 'emblem': 0.00, 'seasons': 69.50, 'normalized': 0.00,
     'why': "Shown for completeness: the subject's Revenue Share is the analogue of Emblem's WiFi line, "
            'already reflected in the normalized WiFi figure.'},
]


def main():
    e, s = EMBLEM, SEASONS
    u = e['units']

    emblem_anc_2026 = e['recurring_2026'] + e['other_income_2026']
    seasons_anc_t12 = s['other_income_t12'] / s['units'] / 12
    seasons_anc_t6 = s['other_income_t6_ann'] / s['units'] / 12
    normalized_anc_2026 = sum(n['normalized'] for n in NORMALIZATION)

    print("=" * 78)
    print("1. ANCILLARY INCOME — Emblem vs the subject's actuals ($/unit/month)")
    print("=" * 78)
    print(f"{'component':<42}{'Emblem':>9}{'Seasons':>9}{'Norm.':>9}")
    for n in NORMALIZATION:
        print(f"{n['item']:<42}{n['emblem']:>9.2f}{n['seasons']:>9.2f}{n['normalized']:>9.2f}")
    print(f"{'TOTAL':<42}{emblem_anc_2026:>9.2f}{seasons_anc_t12:>9.2f}{normalized_anc_2026:>9.2f}")
    print(f"\nEmblem ancillary is {emblem_anc_2026/seasons_anc_t12-1:+.0%} vs the subject's T12 "
          f"(${seasons_anc_t12:,.0f}/u/mo) and {emblem_anc_2026/seasons_anc_t6-1:+.0%} vs T6 "
          f"(${seasons_anc_t6:,.0f}/u/mo).")
    print(f"Normalized haircut: ${emblem_anc_2026 - normalized_anc_2026:,.2f}/unit/month (2026 dollars)")

    # ---------------------------------------------------------------- 2. expenses sanity check
    print("\n" + "=" * 78)
    print("2. EXPENSES — is Emblem aggressive? (per unit per year, stabilized)")
    print("=" * 78)
    emb_opex_pu = e['y2030']['opex'] / u
    sea_opex_pu = s['opex_t12'] / s['units']
    emb_tax_pu = e['opex_2030_detail']['taxes'] / u
    sea_tax_uw_pu = s['reassessed_2027'] * s['tax_rate_uw'] / s['units']
    print(f"  Total opex     Emblem ${emb_opex_pu:>7,.0f}   Seasons T12 ${sea_opex_pu:>7,.0f}"
          f"   -> Emblem is {emb_opex_pu/sea_opex_pu-1:+.0%} (CONSERVATIVE)")
    print(f"  Taxes          Emblem ${emb_tax_pu:>7,.0f}   Seasons UW  ${sea_tax_uw_pu:>7,.0f}"
          f"   -> both use a ~0.45% rate on market value; NOT a normalization item")
    print(f"  Insurance      Emblem ${e['opex_2030_detail']['insurance']/u:>7,.0f}"
          f"   Seasons T12 ${s['insurance_t12']/s['units']:>7,.0f}   -> Emblem conservative")
    print("  VERDICT: the expense side is defensible-to-conservative. The aggression is all on")
    print("           the revenue side, and it is concentrated in ancillary income.")

    # ---------------------------------------------------------------- 2b. assessed VALUE, not just rate
    print("\n" + "=" * 78)
    print("2b. TAXES — testing the ASSESSED VALUE (the rate checks out; does the value?)")
    print("=" * 78)
    tx = e['tax_study']
    full_imp = tx['improvement_value_complete']
    print("  (a) Construction-completion lag — assessor assumed to recognize less than is built:")
    lag_total = 0
    for ty, assumed_pct, actual_pct, assumed_imp in tx['ramp']:
        if actual_pct <= assumed_pct:
            continue
        should = full_imp * actual_pct
        extra = (should - assumed_imp) * s['tax_rate_uw']
        lag_total += extra
        print(f"      tax yr {ty}: assumes {assumed_pct:.0%} complete (${assumed_imp:,}) but "
              f"~{actual_pct:.0%} is actually built (${should:,.0f}) -> tax understated ${extra:,.0f}")
    print(f"      TOTAL deferred across construction/lease-up: ${lag_total:,.0f}")

    stab_assessed = tx['assessed_stabilized']
    print(f"\n  (b) Stabilized assessed value ${stab_assessed:,} = ${stab_assessed/u:,.0f}/unit")
    print(f"      = {stab_assessed/e['total_cost']:.0%} of its own cost, "
          f"{stab_assessed/e['exit_value']:.0%} of its own exit value (${e['exit_value']/u:,.0f}/u)")
    print(f"      BENCHMARK: the subject sits at {s['assessed_2026']/s['reassessed_2027']:.0%} of market "
          f"while UNSOLD (${s['assessed_2026']/s['units']:,.0f}/u assessed vs ${s['reassessed_2027']/s['units']:,.0f}/u price)")
    print("      -> 87% of value on a no-sale hold is CONSISTENT with Idaho practice. Not the smoking gun.")

    buyer_assessed = e['exit_value'] * tx['sale_reassessment_pct']
    buyer_tax = buyer_assessed * s['tax_rate_uw'] + tx['direct_assessments']
    step_up = buyer_tax - tx['taxes_stabilized']
    print(f"\n  (c) THE REAL EXPOSURE — the sale-triggered step-up Emblem never bears:")
    print(f"      Idaho reassesses to ~{tx['sale_reassessment_pct']:.0%} of sale price (TMG models exactly this for the subject).")
    print(f"      Buyer's post-sale assessed: ${buyer_assessed:,.0f} = ${buyer_assessed/u:,.0f}/u -> tax ${buyer_tax:,.0f} (${buyer_tax/u:,.0f}/u)")
    print(f"      Emblem's terminal assumption:                             tax ${tx['taxes_stabilized']:,} (${tx['taxes_stabilized']/u:,.0f}/u)")
    print(f"      Delta the BUYER eats: ${step_up:,.0f}/yr -> at a {e['exit_cap']:.2%} cap that is "
          f"${step_up/e['exit_cap']:,.0f} of value (${step_up/e['exit_cap']/u:,.0f}/unit)")
    print(f"\n  (d) Sanity check: Emblem stabilized tax ${tx['taxes_stabilized']/u:,.0f}/unit is still ABOVE the")
    print(f"      subject's post-reassessment run-rate of ${s['reassessed_2027']*0.0044/s['units']:,.0f}/unit. Per-unit burden is fine;")
    print("      the aggression is in TIMING (the lag), not the level.")

    # ---------------------------------------------------------------- 3. solve required market rent
    print("\n" + "=" * 78)
    print("3. WHAT MARKET RENT DOES NEW SUPPLY REALLY NEED?")
    print("=" * 78)
    y = e['y2030']
    pgi = y['base_rent'] + y['recurring'] + y['other'] + y['ltl']
    egi_ratio = y['egi'] / pgi                       # keeps vacancy + concession load intact
    yoc_target = y['noi'] / e['total_cost']

    anc_growth = ((y['recurring'] / u / 12) / e['recurring_2026']) ** (1 / 4) - 1
    normalized_anc_2030 = normalized_anc_2026 * (1 + anc_growth) ** 4
    emblem_anc_2030 = (y['recurring'] + y['other']) / u / 12
    anc_shortfall_annual = (emblem_anc_2030 - normalized_anc_2030) * u * 12

    tax_norm_delta = e['tax_study']['normalized_stab_year_delta']
    noi_norm = y['noi'] - anc_shortfall_annual * egi_ratio - tax_norm_delta
    yoc_norm = noi_norm / e['total_cost']
    extra_rent_annual = anc_shortfall_annual + tax_norm_delta / egi_ratio  # gross revenue to restore NOI
    extra_rent_pu_mo_2030 = extra_rent_annual / u / 12
    base_2030 = y['base_rent'] / u / 12
    required_2030 = base_2030 + extra_rent_pu_mo_2030
    rent_growth_factor = base_2030 / e['base_rent_2026']
    required_2026 = required_2030 / rent_growth_factor

    print(f"  Emblem stabilized (2030): NOI ${y['noi']:,} on ${e['total_cost']:,} = {yoc_target:.2%} YoC")
    print(f"  Ancillary, normalized:    ${normalized_anc_2030:,.2f}/u/mo vs Emblem ${emblem_anc_2030:,.2f}"
          f"  -> revenue shortfall ${anc_shortfall_annual:,.0f}/yr")
    print(f"  Tax normalization (assessor keeps pace w/ construction): -${tax_norm_delta:,.0f}/yr")
    print(f"  NOI at normalized ancillary: ${noi_norm:,.0f}  ->  YoC falls to {yoc_norm:.2%}")
    print(f"\n  To hold {yoc_target:.2%} YoC, base market rent must rise "
          f"${extra_rent_pu_mo_2030:,.0f}/u/mo (2030 $)")
    print(f"  Required base market rent 2030: ${required_2030:,.0f}/u/mo "
          f"(Emblem shows ${base_2030:,.0f})")
    print(f"  Required base market rent TODAY (2026 $): ${required_2026:,.0f}/u/mo "
          f"(Emblem advertises ${e['base_rent_2026']:,.0f} = {required_2026/e['base_rent_2026']-1:+.1%} understated)")
    print(f"  Required rent PSF today: ${required_2026/e['avg_sf']:.2f}/SF")

    print("\n  GAP VS THE SUBJECT'S MARKET RENTS (market-to-market, per HelloData in the TMG model):")
    for lab, mr in [('T12 (6/30/26)', s['market_rent_t12']), ('T6 annualized', s['market_rent_t6']),
                    ('YE2026', s['market_rent_ye2026'])]:
        print(f"    vs {lab:<16} ${mr:,}/u/mo  ->  new supply needs {required_2026/mr-1:+.1%}")
    print(f"    (PSF: subject ${s['market_rent_t6']/s['avg_sf']:.2f}/SF vs required "
          f"${required_2026/e['avg_sf']:.2f}/SF)")

    # ---------------------------------------------------------------- 4. Seasons replacement cost
    print("\n" + "=" * 78)
    print("4. SEASONS REPLACEMENT COST — the case for MORE than the raw Emblem number")
    print("=" * 78)
    base_ppu = e['total_cost'] / u
    adjustments = [
        ('Emblem all-in cost per unit (base)', base_ppu),
        ('+ Amenity/spec premium: subject has a 10,000 SF clubhouse and 30,000+ SF of '
         'community space (golf sim, resort pool, dog parks) vs Emblem\'s 7,300 SF clubhouse '
         '— roughly 55 extra SF/unit of amenity at $250-300/SF', 14_000),
        ('+ Land premium: Eagle/Overland node (I-84 frontage, Village/Topgolf adjacency) vs '
         'Emblem\'s Eagle/Victory site; the touching WinCo parcel is being marketed for RETAIL '
         'ground lease, which prices above MF land', 6_000),
        ('- Density/scale efficiency: 360 units at 23/acre vs Emblem 256 at ~20/acre', -2_000),
    ]
    total = 0
    for lab, v in adjustments:
        total += v
        print(f"  {'':2}{lab[:96]}")
        print(f"  {'':2}{'':<96}{v:>+12,.0f}")
    print(f"\n  SEASONS REPLICA COST TODAY: ${total:,.0f}/unit  ->  ${total*s['units']:,.0f} for 360 units")
    print(f"  Sensible range: $315,000-$330,000/unit  ->  ${315_000*s['units']:,.0f}-${330_000*s['units']:,.0f}")

    print("\n  BASIS COMPARISON:")
    rows = [
        ("Subject's ACTUAL 2022 development cost", s['actual_cost_2022'] / s['units'], s['actual_cost_2022']),
        ('Replacement cost today (this model)', total, total * s['units']),
        ('TMG purchase price', s['purchase_price'] / s['units'], s['purchase_price']),
        ('TMG total basis (price + closing + capex)', s['total_basis'] / s['units'], s['total_basis']),
    ]
    for lab, ppu, tot in rows:
        print(f"    {lab:<46} ${ppu:>9,.0f}/u   ${tot:>13,.0f}")
    print(f"\n    -> We are acquiring at ~{s['purchase_price']/s['units']/total-1:+.1%} vs replacement cost; "
          f"total basis is {s['total_basis']/s['units']/total-1:+.1%} vs replacement.")

    out = {
        'ancillary_normalization': NORMALIZATION,
        'emblem_ancillary_2026': round(emblem_anc_2026, 2),
        'seasons_ancillary_t12': round(seasons_anc_t12, 2),
        'seasons_ancillary_t6': round(seasons_anc_t6, 2),
        'normalized_ancillary_2026': round(normalized_anc_2026, 2),
        'required_market_rent_2026': round(required_2026),
        'emblem_advertised_rent_2026': e['base_rent_2026'],
        'understatement_pct': round(required_2026 / e['base_rent_2026'] - 1, 4),
        'gap_vs_subject': {
            't12': round(required_2026 / s['market_rent_t12'] - 1, 4),
            't6': round(required_2026 / s['market_rent_t6'] - 1, 4),
            'ye2026': round(required_2026 / s['market_rent_ye2026'] - 1, 4)},
        'yoc_target': round(yoc_target, 4), 'yoc_normalized': round(yoc_norm, 4),
        'seasons_replacement_cost_per_unit': round(total),
        'seasons_replacement_cost_total': round(total * s['units']),
        'basis_vs_replacement': round(s['purchase_price'] / s['units'] / total - 1, 4),
    }
    (HERE / 'emblem_normalization.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
