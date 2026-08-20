#!/usr/bin/env python3
"""Back into all-in development cost from Yardi construction-loan data at an assumed LTC.

Input : Yardi "Boise Construction Loans" export (property-level loans, 1 row per loan).
Method: aggregate the loan stack per property -> implied all-in cost = total loan / LTC
        (default 65%) -> cost per unit; segment market-rate vs subsidized (LIHTC/gov
        lenders distort LTC), screen implausible outliers, then trend by origination year.
Output: construction_loan_analysis.json + printed tables.

Usage: python construction_loan_cost_analysis.py <xlsx> [--ltc 0.65]

NOTE on the LTC assumption: Yardi reports the loan, not the budget. 65% LTC is the
analyst's assumption for market-rate construction debt in this era; the ESCALATION TREND
is insensitive to the assumption (it scales every year identically) — only the absolute
cost level moves. Subsidized deals are excluded from the trend because their capital
stacks are not 65% LTC.
"""
import argparse, collections, datetime, json, math, re, statistics as st, zipfile
from pathlib import Path

SUBJ = (43.591935, -116.360877)          # Seasons at Meridian
SUBSIDIZED_LENDERS = {'Local Government', 'Federal Government'}
PLAUSIBLE = (90_000, 600_000)            # $/unit @LTC band for a garden/mid-rise deal


def load_rows(path):
    """Yardi exports can carry invalid style colors that break openpyxl — sanitize first."""
    import openpyxl
    fixed = Path(path).with_suffix('.fixed.xlsx')
    zin = zipfile.ZipFile(path)
    with zipfile.ZipFile(fixed, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'xl/styles.xml':
                data = re.sub(rb'rgb="[^"]*"', b'rgb="FF000000"', data)
            zout.writestr(item, data)
    ws = openpyxl.load_workbook(fixed, data_only=True)['Results']
    hdr = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    rows = [dict(zip(hdr, [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]))
            for r in range(2, ws.max_row + 1)]
    return [r for r in rows if r.get('Property Name')]


def pdate(v):
    if isinstance(v, datetime.datetime):
        return v
    if isinstance(v, str) and v.strip():
        for f in ('%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.datetime.strptime(v.strip(), f)
            except ValueError:
                pass
    return None


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def dist_mi(la, lo):
    if la is None or lo is None:
        return None
    dy = (la - SUBJ[0]) * 69.0
    dx = (lo - SUBJ[1]) * 69.0 * math.cos(math.radians(SUBJ[0]))
    return round(math.hypot(dx, dy), 2)


def build(rows, ltc):
    props = collections.defaultdict(lambda: {'loans': []})
    for r in rows:
        p = props[(r['Property Name'], r['Address'])]
        p.update(name=r['Property Name'], city=r['City'], units=num(r['Units']),
                 owner=r['Owner'], completion=pdate(r['Completion Date']),
                 lat=num(r['Latitude']), lon=num(r['Longitude']))
        p['loans'].append({'amt': num(r['Loan Amount (MM)']) or 0,
                           'orig': pdate(r['Loan Origination Date']),
                           'lender_type': r['Lender Type'], 'lender': r['Lender']})
    out = []
    for p in props.values():
        loans = [l for l in p['loans'] if l['amt'] > 0 and l['orig']]
        if not loans or not p['units']:
            continue
        total = sum(l['amt'] for l in loans)
        subsid = sum(l['amt'] for l in loans if l['lender_type'] in SUBSIDIZED_LENDERS)
        first = min(l['orig'] for l in loans)
        units = int(p['units'])
        out.append({
            'name': p['name'], 'city': p['city'], 'units': units, 'owner': p['owner'],
            'completion': p['completion'].date().isoformat() if p['completion'] else None,
            'lat': p['lat'], 'lon': p['lon'], 'dist_mi': dist_mi(p['lat'], p['lon']),
            'loan_total_mm': round(total, 3), 'subsidized_mm': round(subsid, 3),
            'n_loans': len(loans), 'first_orig': first.date().isoformat(),
            'orig_year': first.year, 'is_affordable': subsid > 0.20 * total,
            'loan_per_unit': round(total * 1e6 / units),
            'implied_cost_mm': round(total / ltc, 3),
            'cost_per_unit': round(total * 1e6 / ltc / units),
        })
    return sorted(out, key=lambda x: x['first_orig'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xlsx')
    ap.add_argument('--ltc', type=float, default=0.65)
    ap.add_argument('--out', default=str(Path(__file__).parent / 'construction_loan_analysis.json'))
    a = ap.parse_args()

    props = build(load_rows(a.xlsx), a.ltc)
    market = [x for x in props if not x['is_affordable']]
    clean = [x for x in market if PLAUSIBLE[0] <= x['cost_per_unit'] <= PLAUSIBLE[1]]
    excluded = [x for x in market if x not in clean]

    by_year = collections.defaultdict(list)
    for x in clean:
        by_year[x['orig_year']].append(x['cost_per_unit'])
    trend = {y: {'n': len(v), 'median': int(st.median(v))} for y, v in sorted(by_year.items())}

    vol = collections.defaultdict(lambda: {'deals': 0, 'units': 0, 'loan_mm': 0.0,
                                           'ring_deals': 0, 'ring_units': 0})
    for x in props:
        b = vol[x['orig_year']]
        b['deals'] += 1; b['units'] += x['units']; b['loan_mm'] = round(b['loan_mm'] + x['loan_total_mm'], 1)
        if x['dist_mi'] is not None and x['dist_mi'] <= 5.0:
            b['ring_deals'] += 1; b['ring_units'] += x['units']

    eras = {}
    for lo, hi, lab in [(2012, 2016, '2012-2016'), (2017, 2019, '2017-2019'),
                        (2020, 2021, '2020-2021'), (2022, 2023, '2022-2023'),
                        (2024, 2026, '2024-2026')]:
        v = [x['cost_per_unit'] for x in clean if lo <= x['orig_year'] <= hi]
        eras[lab] = {'n': len(v), 'median': int(st.median(v)) if v else None}

    res = {'ltc_assumption': a.ltc, 'properties': props, 'trend_by_year': trend,
           'volume_by_year': dict(sorted(vol.items())), 'eras': eras,
           'excluded_outliers': [{'name': x['name'], 'year': x['orig_year'],
                                  'cost_per_unit': x['cost_per_unit']} for x in excluded],
           'ring_market_rate': [x for x in clean if x['dist_mi'] is not None and x['dist_mi'] <= 5.0]}
    Path(a.out).write_text(json.dumps(res, indent=1))

    print(f"properties={len(props)}  market-rate={len(market)}  clean={len(clean)}  LTC={a.ltc:.0%}")
    print("\nyear  n  median $/unit @LTC | deals units  loan$MM | ring deals/units")
    for y in sorted(set(list(trend) + list(vol))):
        t = trend.get(y, {}); v = vol.get(y, {})
        print(f"{y}  {t.get('n',0):>2}  ${t.get('median',0):>8,} | "
              f"{v.get('deals',0):>3} {v.get('units',0):>5} {v.get('loan_mm',0):>8.1f} | "
              f"{v.get('ring_deals',0):>2}/{v.get('ring_units',0)}")
    print("\nERAS:", {k: v['median'] for k, v in eras.items()})
    if 2014 in trend and 2024 in trend:
        a14, a24 = trend[2014]['median'], trend[2024]['median']
        print(f"2014->2024: ${a14:,} -> ${a24:,} = {a24/a14-1:+.0%} ({(a24/a14)**0.1-1:.1%} CAGR)")


if __name__ == '__main__':
    main()
