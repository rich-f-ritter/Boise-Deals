#!/usr/bin/env python3
"""T12 operating-statement parser for Seasons at Meridian.

Three statements are supplied and they overlap (Jun 2025-May 2026, Jul 2025-
Jun 2026, Aug 2025-Jul 2026); together they cover Jun 2025 - Jul 2026. The
later file wins on overlap. Overlapping months agree exactly EXCEPT Apr 2026,
which the Aug-Jul statement restates: concessions (4460) -5,648.50 ->
-6,466.00, carrying -$817.50 through net residential rent and total revenue.

The T12 is the only source that carries OCCUPANCY for 2025. Vacancy Loss is
charged at market rent for the days a unit stands empty, so 1 - VacancyLoss /
MarketRent is physical occupancy, time-weighted across the month. That is a
different statistic from the rent-roll figure (a point-in-time count at month
end) and the two are reported side by side rather than blended.
"""
import openpyxl
from datetime import datetime

DOCS = '../../documents'
FILES = ['T12_Jun2025-May2026.xlsx', 'T12_Jul2025-Jun2026.xlsx',
         'T12_Aug2025-Jul2026.xlsx']

# GL accounts that make up the residential rent bridge
ACCT = {
    '4410-0000': 'market_rent',
    '4415-0000': 'loss_to_lease',
    '4419-0000': 'gross_potential',
    '4435-0000': 'mtm_fees',
    '4450-0000': 'vacancy_loss',
    '4455-0000': 'non_revenue_units',
    '4460-0000': 'concessions',
    '4465-0000': 'employee_discounts',
    '4475-0000': 'write_offs',
    '4480-0000': 'rent_adjustment',
    '4499-0000': 'net_residential_rent',
    '4990-0000': 'other_income',
    '5999-0000': 'total_revenue',
}


def load():
    """month key 'YYYY-MM' -> {line: value}, signs as booked (credits negative)."""
    out = {}
    for fn in FILES:
        wb = openpyxl.load_workbook(f'{DOCS}/t12/{fn}', read_only=True, data_only=True)
        rows = list(wb['Report1'].iter_rows(values_only=True))
        wb.close()
        hdr = []
        for cell in rows[4][2:14]:
            hdr.append(datetime.strptime(str(cell), '%b %Y').strftime('%Y-%m'))
        for r in rows:
            key = str(r[0] or '')[:9]
            if key in ACCT:
                for mo, v in zip(hdr, r[2:14]):
                    out.setdefault(mo, {})[ACCT[key]] = float(v or 0)
    for mo, d in out.items():
        mkt = d.get('market_rent') or 0
        gpr = d.get('gross_potential') or 0
        # Vacancy loss is booked at market rent for the vacant days, so this is
        # physical occupancy averaged over the month, not an end-of-month count.
        d['physical_occupancy_avg'] = (1 - abs(d.get('vacancy_loss', 0)) / mkt) if mkt else None
        # What actually landed as residential revenue, against the same market
        # denominator: the gap to physical occupancy IS concessions + loss-to-lease
        # + bad debt, which is the number that matters for underwriting.
        d['economic_occupancy'] = (d.get('net_residential_rent', 0) / mkt) if mkt else None
        d['concession_pct_gpr'] = (abs(d.get('concessions', 0)) / gpr) if gpr else None
        d['ltl_pct_market'] = (abs(d.get('loss_to_lease', 0)) / mkt) if mkt else None
    return dict(sorted(out.items()))


if __name__ == '__main__':
    s = load()
    print(f'T12 coverage: {min(s)} -> {max(s)}  ({len(s)} months)')
    hdr = f"{'month':9}{'market':>11}{'GPR':>11}{'vac loss':>10}{'conc':>9}{'net res':>11}"
    print(hdr + f"{'phys occ':>10}{'econ occ':>10}{'conc%GPR':>10}")
    for mo, d in s.items():
        print(f"{mo:9}{d['market_rent']:11,.0f}{d['gross_potential']:11,.0f}"
              f"{d['vacancy_loss']:10,.0f}{d['concessions']:9,.0f}"
              f"{d['net_residential_rent']:11,.0f}"
              f"{d['physical_occupancy_avg']:10.1%}{d['economic_occupancy']:10.1%}"
              f"{d['concession_pct_gpr']:10.1%}")
