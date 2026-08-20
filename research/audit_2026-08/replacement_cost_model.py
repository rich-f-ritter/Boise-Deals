#!/usr/bin/env python3
"""Seasons at Meridian replacement-cost model.

v2 (Aug 2026) — rebuilt after the Emblem Meridian proforma showed the v1 flat-65%-LTC
assumption was wrong for recent years.

TWO HARD ANCHORS calibrate the model:
  * Emblem Meridian (Quarterra, 256u garden+BTR, Meridian, UW 2026 / deliver 2028):
    total cost $77,959,624 = $304,530/unit = $324/SF; construction loan $42,877,793
    => **55.0% LTC**.  [source: Emblem Meridian merchant model, S&U + A-DevBdgt tabs]
  * Seasons at Meridian (subject, 360u, loan $66.61M orig 12/2022): press reported the
    project at "$100 million-plus" (Multifamily Dive / REBusinessOnline). $66.61M / 0.65
    = $102.5M => **~65% LTC** held in the 2022 vintage.

So construction leverage fell ~65% -> ~55% after the 2022-23 rate shock. A flat 65% LTC
understates post-2022 cost by ~18%. This model applies a time-varying LTC.

COMP SCREEN (to make the tape Seasons-comparable): market-rate only; 100+ units;
core submarkets (Boise/Meridian/Eagle/Garden City — Nampa/Caldwell/Kuna/Star carry
materially cheaper land and lower rents); conventional garden/mid-rise rental only
(excludes student, BTR-only, downtown mixed-use high-rise, adaptive reuse); and
excludes loans that are phase-level or partial artifacts.

Usage: python replacement_cost_model.py [--loans construction_loan_analysis.json]
"""
import argparse, collections, json, statistics as st
from pathlib import Path

HERE = Path(__file__).parent

# LTC by origination year — calibrated to the two anchors above.
def ltc_for(year):
    if year <= 2022:
        return 0.65
    if year == 2023:
        return 0.60          # transition vintage
    return 0.55              # 2024+, per Emblem

# Deals excluded from the cost trend, with the reason (documented, not silent).
EXCLUDE = {
    'Regency at River Valley, The': 'partial/assumption loan ($30k/u) — not a full construction facility',
    'Jules on 3rd': 'downtown Boise mixed-use high-rise — different product & cost basis',
    'BB Living at The Oaks': 'build-to-rent single-family — different product',
    'LOCAL Boise': 'purpose-built student housing (Subtext) — different product',
    'Dovetail': 'phase-level loan against a 480-unit count — understates whole-project cost',
    'Gem, The': 'small adaptive/workforce infill — not garden comparable',
    'Tauri': 'townhome product (Brighton) — lower cost/SF than garden',
    'Stonesthrow Townhomes': 'townhome product',
    'Modern Craftsman Black Cat': 'BTR/garden hybrid — flagged, not garden comparable',
    'Cimarron Townhomes, The': 'townhome product',
    'Alpine Landing Townhomes': 'townhome product',
    # --- urban infill / structured-parking product: real deals, but NOT Seasons-comparable.
    # Leaving them in the post-2022 cohort produced a $483k/unit "median" off n=2 per year.
    'Denton': 'Boise urban infill, structured parking — higher cost basis than suburban garden',
    'North End Lofts': 'Boise North End small infill — not garden comparable',
    'Wesley Phase II': 'loan likely spans both phases/other collateral ($508k/u implied) — artifact',
    'Boardwalk, The': 'Garden City urban/mixed — higher basis than suburban garden',
    'Crosshatch': 'Garden City urban infill',
    'Mill at Loggers Creek, The': 'Boise urban infill',
    'Timbers at Harris Ranch, The': 'Harris Ranch premium submarket',
}
CORE = {'Boise', 'Meridian', 'Eagle', 'Garden City'}

# Emblem Meridian — the live 2026 underwriting anchor.
EMBLEM = {
    'name': 'Emblem Meridian (Quarterra)', 'units': 256, 'avg_sf': 939,
    'total_cost': 77_959_624, 'land': 9_092_960, 'hard': 54_579_077,
    'soft': 14_287_587, 'loan': 42_877_793, 'equity': 35_081_831,
    'deliver': 2028, 'uw_year': 2026,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--loans', default=str(HERE / 'construction_loan_analysis.json'))
    ap.add_argument('--out', default=str(HERE / 'replacement_cost_model.json'))
    a = ap.parse_args()

    props = json.loads(Path(a.loans).read_text())['properties']

    cohort = []
    for x in props:
        if x['is_affordable'] or x['units'] < 100 or x['city'] not in CORE:
            continue
        if x['name'] in EXCLUDE:
            continue
        ltc = ltc_for(x['orig_year'])
        cost = x['loan_total_mm'] * 1e6 / ltc
        cohort.append({**x, 'ltc': ltc, 'total_cost': round(cost),
                       'cost_per_unit': round(cost / x['units'])})
    cohort.sort(key=lambda z: z['first_orig'])

    by_year = collections.defaultdict(list)
    for x in cohort:
        by_year[x['orig_year']].append(x['cost_per_unit'])

    eras = {}
    for lo, hi, lab in [(2012, 2016, '2012-2016'), (2017, 2019, '2017-2019'),
                        (2020, 2021, '2020-2021'), (2022, 2022, '2022'),
                        (2023, 2025, '2023-2025')]:
        v = [x['cost_per_unit'] for x in cohort if lo <= x['orig_year'] <= hi]
        eras[lab] = {'n': len(v), 'median': int(st.median(v)) if v else None}

    emb_ppu = EMBLEM['total_cost'] / EMBLEM['units']
    emb_psf = EMBLEM['total_cost'] / (EMBLEM['units'] * EMBLEM['avg_sf'])

    # Seasons replacement cost today, three independent routes.
    SEASONS = {'units': 360, 'avg_sf': 931, 'loan': 66_610_000, 'orig_year': 2022}
    seasons_actual = SEASONS['loan'] / 0.65
    routes = {
        'A_emblem_per_unit': {
            'basis': 'Emblem $/unit applied to 360 units',
            'per_unit': round(emb_ppu), 'total': round(emb_ppu * SEASONS['units'])},
        'B_emblem_per_sf': {
            'basis': "Emblem $/SF x Seasons' 931 avg SF (size-adjusted)",
            'per_unit': round(emb_psf * SEASONS['avg_sf']),
            'total': round(emb_psf * SEASONS['avg_sf'] * SEASONS['units'])},
        'C_tape_2022_escalated': {
            'basis': "2022 garden-cohort median escalated at the Seasons->Emblem rate (+1.7%/yr)",
            'per_unit': round((eras['2022']['median'] or 0) * 1.017 ** 4),
            'total': round((eras['2022']['median'] or 0) * 1.017 ** 4 * SEASONS['units'])},
    }
    vals = [r['per_unit'] for r in routes.values() if r['per_unit']]
    concl = {'low': min(vals), 'high': max(vals), 'midpoint': round(sum(vals) / len(vals)),
             'seasons_actual_2022_per_unit': round(seasons_actual / SEASONS['units']),
             'seasons_actual_2022_total': round(seasons_actual)}
    concl['premium_vs_actual'] = round(concl['midpoint'] / concl['seasons_actual_2022_per_unit'] - 1, 3)

    res = {'ltc_schedule': {'<=2022': 0.65, '2023': 0.60, '2024+': 0.55},
           'anchors': {'emblem': {**EMBLEM, 'cost_per_unit': round(emb_ppu),
                                  'cost_per_sf': round(emb_psf), 'ltc': round(EMBLEM['loan'] / EMBLEM['total_cost'], 3)},
                       'seasons_2022': {'loan': SEASONS['loan'], 'implied_total_at_65': round(seasons_actual),
                                        'per_unit': round(seasons_actual / SEASONS['units'])}},
           'excluded': EXCLUDE, 'cohort': cohort,
           'trend_by_year': {y: {'n': len(v), 'median': int(st.median(v))} for y, v in sorted(by_year.items())},
           'eras': eras, 'seasons_replacement_routes': routes, 'conclusion': concl}
    Path(a.out).write_text(json.dumps(res, indent=1))

    print(f"Seasons-comparable cohort: n={len(cohort)}  (market-rate, 100u+, core submarket, garden/mid-rise)")
    print("\nyear  n  median $/unit  (LTC)")
    for y, v in sorted(by_year.items()):
        print(f"{y}  {len(v):>2}  ${int(st.median(v)):>8,}   {ltc_for(y):.0%}")
    print("\nERA medians:", {k: (f"${v['median']:,}" if v['median'] else None) for k, v in eras.items()})
    print(f"\nEMBLEM ANCHOR: ${emb_ppu:,.0f}/unit  ${emb_psf:.0f}/SF  LTC {EMBLEM['loan']/EMBLEM['total_cost']:.1%}")
    print("\nSEASONS REPLACEMENT COST TODAY:")
    for k, r in routes.items():
        print(f"  {k}: ${r['per_unit']:,}/unit  -> ${r['total']:,.0f} total   [{r['basis']}]")
    print(f"\n  CONCLUSION: ${concl['low']:,}-${concl['high']:,}/unit, midpoint ${concl['midpoint']:,}/unit")
    print(f"  vs Seasons' own 2022 basis ${concl['seasons_actual_2022_per_unit']:,}/unit "
          f"= {concl['premium_vs_actual']:+.1%}")

    # --- the equity story: cost plateaued, but leverage fell, so equity per unit jumped
    e22 = concl['seasons_actual_2022_per_unit'] * (1 - 0.65)
    e26 = round(emb_ppu) * (1 - 0.55)
    print("\nEQUITY REQUIRED PER UNIT (the real feasibility break):")
    print(f"  2022 vintage: ${concl['seasons_actual_2022_per_unit']:,}/u cost x 35% equity = ${e22:,.0f}/unit")
    print(f"  2026 vintage: ${round(emb_ppu):,}/u cost x 45% equity = ${e26:,.0f}/unit  ({e26/e22-1:+.0%})")
    res['equity_per_unit'] = {'2022': round(e22), '2026': round(e26),
                              'increase_pct': round(e26 / e22 - 1, 3)}
    Path(a.out).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
