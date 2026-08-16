#!/usr/bin/env python3
"""The Idaho sale-triggered tax step-up — a buyer-to-seller transfer every developer
proforma in this market ignores, and why it makes new development harder still.

THE MECHANIC. Idaho reassesses to ~98% of sale price on transfer. So:
  * the SELLER's proforma caps an NOI carrying the OLD (under-assessed) tax load;
  * the BUYER inherits a stepped-up tax bill that permanently reduces NOI;
  * therefore a rational buyer pays LESS than the seller's headline value, and the
    seller's exit assumption is systematically optimistic.

This is not theoretical — it is exactly what we are doing at Seasons: buying at
$118.0M and taking the assessment to $115.64M (98%), which raises our own taxes by
$126,510/yr and comes straight out of OUR NOI and OUR going-in cap rate.

The same arithmetic, applied to Emblem Meridian's exit, shows its $102.5M exit is
overstated because no buyer will pay for an NOI they cannot achieve. Solving the
circularity (price -> assessment -> taxes -> NOI -> price) gives the honest number.

Sources: TMG Acquisitions model 7.26 - Seasons v3 (Taxes, CF S&U, Assumptions, One Pager);
Emblem Meridian merchant model (Tax Study Input, A-OperBgt).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

SEASONS = {
    'units': 360,
    'purchase_price': 118_000_000,          # CF S&U + Assumptions
    'whisper_price': 125_000_000,
    'closing_costs': 2_337_200,
    'total_basis': 120_100_902,
    'assessed_presale': 92_993_300,         # 2026, as assessed today
    'taxes_presale_t12': 384_244,           # Operating Proforma T12 ending 6/30/26
    'reassessment_pct': 0.98,               # Taxes tab: "Reassmnt (%)"
    'assessed_postsale': 115_640_000,       # = 98% x $118.0M
    'taxes_postsale': 510_754,              # Taxes tab, 2027
    'y1_cap_on_basis': 0.050073,            # One Pager
    't3_adj_cap': 0.046938,
}

EMBLEM = {
    'units': 256,
    'total_cost': 77_959_624,
    'exit_value_stated': 102_500_000,       # equity book: Jan-2030 exit
    'exit_cap': 0.0550,
    'terminal_taxes': 423_134,              # Tax Study Input, tax yr 2031
    'direct_assessments': 19_000,
    'tax_rate': 0.0045,
    'reassessment_pct': 0.98,
    'egi_ratio': 0.906,                     # EGI / PGI at stabilization
    'rent_growth_26_to_30': 1.1288,
    'equity': 35_081_831,
}


def solve_buyer_price(noi_before_tax, cap, tax_rate, reassess_pct, direct):
    """Price where the buyer earns `cap` on an NOI that already carries the
    reassessed tax bill. Circular: price -> assessment -> tax -> NOI -> price."""
    # cap*P = noi_before_tax - (reassess_pct*P*tax_rate + direct)
    return (noi_before_tax - direct) / (cap + reassess_pct * tax_rate)


def main():
    s, e = SEASONS, EMBLEM

    print("=" * 78)
    print("1. THE WORKED EXAMPLE — what WE are absorbing at Seasons")
    print("=" * 78)
    step = s['taxes_postsale'] - s['taxes_presale_t12']
    print(f"  Purchase price                 ${s['purchase_price']:>13,}  (${s['purchase_price']/s['units']:,.0f}/unit)")
    print(f"  Assessed BEFORE sale           ${s['assessed_presale']:>13,}  "
          f"= {s['assessed_presale']/s['purchase_price']:.0%} of what we are paying")
    print(f"  Assessed AFTER sale ({s['reassessment_pct']:.0%} of price) ${s['assessed_postsale']:>13,}")
    print(f"  Taxes T12 (seller's load)      ${s['taxes_presale_t12']:>13,}  (${s['taxes_presale_t12']/s['units']:,.0f}/unit)")
    print(f"  Taxes post-reassessment        ${s['taxes_postsale']:>13,}  (${s['taxes_postsale']/s['units']:,.0f}/unit)")
    print(f"  >> STEP-UP WE ABSORB           ${step:>13,}/yr  (+{step/s['taxes_presale_t12']:.0%}, "
          f"${step/s['units']:,.0f}/unit)")
    val_lost = step / s['y1_cap_on_basis']
    print(f"\n  That step-up is permanent and comes straight out of OUR NOI:")
    print(f"    capitalized at our Y1 cap of {s['y1_cap_on_basis']:.2%}  ->  ${val_lost:,.0f} of value "
          f"(${val_lost/s['units']:,.0f}/unit)")
    y1_noi = s['total_basis'] * s['y1_cap_on_basis']
    print(f"    Y1 NOI ${y1_noi:,.0f}; without the step-up it would be ${y1_noi+step:,.0f}")
    print(f"    -> going-in yield on basis: {s['y1_cap_on_basis']:.3%} actual vs "
          f"{(y1_noi+step)/s['total_basis']:.3%} un-stepped = "
          f"{((y1_noi+step)/s['total_basis']-s['y1_cap_on_basis'])*10000:.0f} bp we hand over")
    print("\n  The seller (Carlyle/Morgan Stonehill) capitalized an NOI carrying the OLD tax load.")
    print("  We pay for the step-up in perpetuity. This is the transfer, and it is real money.")

    print("\n" + "=" * 78)
    print("2. THE SAME ARITHMETIC APPLIED TO EMBLEM'S EXIT")
    print("=" * 78)
    stated_noi = e['exit_value_stated'] * e['exit_cap']
    noi_before_tax = stated_noi + e['terminal_taxes']
    print(f"  Emblem's stated exit           ${e['exit_value_stated']:>13,} @ {e['exit_cap']:.2%} cap")
    print(f"    implied exit NOI             ${stated_noi:>13,.0f}  (carries Emblem's terminal tax "
          f"${e['terminal_taxes']:,})")
    print(f"    NOI before property tax      ${noi_before_tax:>13,.0f}")
    buyer_price = solve_buyer_price(noi_before_tax, e['exit_cap'], e['tax_rate'],
                                    e['reassessment_pct'], e['direct_assessments'])
    buyer_assessed = buyer_price * e['reassessment_pct']
    buyer_tax = buyer_assessed * e['tax_rate'] + e['direct_assessments']
    buyer_noi = noi_before_tax - buyer_tax
    overstatement = e['exit_value_stated'] - buyer_price
    print(f"\n  Solving price -> assessment -> tax -> NOI -> price:")
    print(f"    Buyer's price at a true {e['exit_cap']:.2%}   ${buyer_price:>13,.0f}  "
          f"(${buyer_price/e['units']:,.0f}/unit)")
    print(f"    Buyer's assessed value       ${buyer_assessed:>13,.0f}")
    print(f"    Buyer's taxes                ${buyer_tax:>13,.0f}  (vs Emblem's ${e['terminal_taxes']:,})")
    print(f"    Buyer's NOI                  ${buyer_noi:>13,.0f}")
    print(f"  >> EMBLEM'S EXIT IS OVERSTATED BY ${overstatement:,.0f}  "
          f"(${overstatement/e['units']:,.0f}/unit, {overstatement/e['exit_value_stated']:.1%})")
    print(f"\n  If Emblem holds its $102.5M price, the buyer's real going-in cap is "
          f"{(noi_before_tax - (e['exit_value_stated']*e['reassessment_pct']*e['tax_rate']+e['direct_assessments']))/e['exit_value_stated']:.3%}, not {e['exit_cap']:.2%}.")

    print("\n" + "=" * 78)
    print("3. WHAT IT DOES TO THE DEVELOPER'S RETURN — and therefore to feasibility")
    print("=" * 78)
    m_stated = e['exit_value_stated'] / e['total_cost'] - 1
    m_adj = buyer_price / e['total_cost'] - 1
    print(f"  Development margin on stated exit : {m_stated:+.1%}  "
          f"(${e['exit_value_stated']-e['total_cost']:,.0f} profit)")
    print(f"  Development margin, buyer-adjusted: {m_adj:+.1%}  "
          f"(${buyer_price-e['total_cost']:,.0f} profit)")
    print(f"  Profit erased by the step-up      : ${overstatement:,.0f} = "
          f"{overstatement/e['equity']:.1%} of the ${e['equity']:,.0f} equity check")
    extra_noi = overstatement * e['exit_cap']
    extra_rev = extra_noi / e['egi_ratio']
    extra_rent_2030 = extra_rev / e['units'] / 12
    extra_rent_2026 = extra_rent_2030 / e['rent_growth_26_to_30']
    print(f"\n  To restore the lost exit value, the deal needs ${extra_noi:,.0f} more NOI")
    print(f"    = ${extra_rev:,.0f} more revenue = ${extra_rent_2030:,.2f}/unit/mo (2030$) "
          f"= ${extra_rent_2026:,.2f}/unit/mo in 2026 dollars")
    print("    -> stack this on top of the ancillary and tax-lag normalizations.")

    print("\n" + "=" * 78)
    print("4. THE GENERAL RULE (for every deal in the supply chart)")
    print("=" * 78)
    print("  In Idaho, a merchant developer's exit proforma is structurally optimistic:")
    print("  it capitalizes an NOI carrying a development-era assessment, while the buyer")
    print("  is reassessed to ~98% of the price paid. Roughly 0.8-1.0% of exit value, or")
    print("  ~2-3% of the equity check, is transferred to the buyer at closing.")
    print("  For OUR underwriting the same rule cuts the other way and we already model it:")
    print(f"  Seasons' taxes rise {step/s['taxes_presale_t12']:.0%} on day one and we hold that forever.")

    out = {
        'seasons': {'purchase_price': s['purchase_price'],
                    'price_per_unit': round(s['purchase_price']/s['units']),
                    'assessed_presale': s['assessed_presale'],
                    'assessed_postsale': s['assessed_postsale'],
                    'tax_stepup_annual': step,
                    'tax_stepup_pct': round(step/s['taxes_presale_t12'], 4),
                    'value_impact_at_y1_cap': round(val_lost),
                    'bp_of_going_in_yield': round(((y1_noi+step)/s['total_basis']-s['y1_cap_on_basis'])*10000)},
        'emblem': {'stated_exit': e['exit_value_stated'],
                   'buyer_adjusted_exit': round(buyer_price),
                   'overstatement': round(overstatement),
                   'overstatement_per_unit': round(overstatement/e['units']),
                   'margin_stated': round(m_stated, 4), 'margin_adjusted': round(m_adj, 4),
                   'extra_rent_needed_2026': round(extra_rent_2026, 2)},
    }
    (HERE / 'tax_stepup_analysis.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
