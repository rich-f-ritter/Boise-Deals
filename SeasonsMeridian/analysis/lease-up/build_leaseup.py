#!/usr/bin/env python3
"""
Seasons at Meridian — Lease-Up Analysis: monthly lease-event series.

Builds a month-by-month series from the start of lease-up (Jun 2024) through
Aug 2026 covering, for each month:
  - new leases signed (and of those, how many were re-leases of a turned unit)
  - leases expired
  - renewals + renewal increase (gross and effective)
  - units leased to a new tenant + new-lease trade-out (gross and effective)

Two data bases, kept visibly separate (never blended in one number):
  ACTUAL  Jan 2026 - Aug 2026 : Yardi rent rolls + concession burn-off +
                                renewal trade-out report
  PROXY   Jun 2024 - Dec 2025 : HelloData listing episodes only. No Yardi
                                roster, lease-start, renewal or financial
                                data exists for this window.

Conventions (per RFR 2026-08-14):
  - New leases counted on lease-start date; move-in used as fallback, and
    HelloData off-market date stands in for the proxy window.
  - New-lease trade-out baseline = prior tenant's LAST contract rent, same unit.
  - Effective rent = gross - (total concession / lease term months), the Yardi
    convention used by the 3ps renewal trade-out report, so figures tie out.
  - Corporate leases excluded from all rent statistics.

Output: events.csv, monthly.csv + a validation report to stdout.
"""
import csv
import openpyxl
import pandas as pd
from datetime import datetime, date, timedelta
from collections import defaultdict

DOCS = '../../documents'
RENEWAL_GAP_DAYS = 45              # lease start > move-in + gap => renewal
CORPORATE = {'Coleman Environmental Engineering', 'Murata Machinery Inc'}
HD_TO_MOVEIN_LAG = 15              # median days: off-market -> move-in (validated in DATA_NOTES)
MIN_TENANCY_DAYS = 120             # shortest lease term seen in the burn-off is 4 months;
                                   # closer listing episodes are one lease-up, not a turn
ACTUAL_START = date(2026, 1, 1)    # Yardi-actual window begins at the 1/1/26 roll
CUTOFF = date(2026, 8, 4)          # measurement date = latest rent roll
TOTAL_UNITS = 360

ROLLS = [('2026-01-01', 'rent-rolls/RentRoll_AsOf_2026-01-01_BACKDATED-see-notes.xlsx'),
         ('2026-07-07', 'rent-rolls/RentRoll_AsOf_2026-07-07.xlsx'),
         ('2026-07-19', 'rent-rolls/RentRoll_AsOf_2026-07-19.xlsx'),
         ('2026-08-04', 'rent-rolls/RentRoll_AsOf_2026-08-04.xlsx')]


# ---------------------------------------------------------------- parsing
def d(x):
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    if isinstance(x, str):
        s = x.replace('*', '').strip()
        for fmt in ('%m/%d/%Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                pass
    return None


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_rent_roll(fname):
    wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)
    ws = wb['Report1']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    section, recs = None, []
    for r in rows[6:]:
        c0 = r[0]
        if isinstance(c0, str) and ('Current' in c0 or 'Future' in c0 or 'Total' in c0):
            section = c0.strip()
        if c0 is None or r[1] is None:
            continue
        recs.append({'section': section, 'unit': str(c0).strip(), 'type': str(r[1]).strip(),
                     'sf': fnum(r[2]), 'res': str(r[3]).strip() if r[3] else '',
                     'name': str(r[4]).strip() if r[4] else '',
                     'mkt': fnum(r[5]), 'actual': fnum(r[6]),
                     'movein': d(r[9]), 'leaseexp': d(r[10]), 'moveout': d(r[11])})
    return [r for r in recs if r['res'].startswith('t')]


def parse_burnoff(fname):
    """Section 1 only; section 2 ('Projection by Unit') is a different layout."""
    wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)
    ws = wb['Report1']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    recs = {}
    for r in rows[6:]:
        if isinstance(r[0], str) and 'Projection by Unit' in str(r[0]):
            break
        if r[0] is None or r[2] is None or not str(r[2]).startswith('t'):
            continue
        recs[str(r[2]).strip()] = {
            'unit': str(r[0]).strip(), 'name': r[3], 'movein': d(r[4]), 'leasestart': d(r[5]),
            'tot_conc': fnum(r[6]), 'cur_conc': fnum(r[7]), 'term': fnum(r[10]),
            'mkt': fnum(r[11]), 'leaserent': fnum(r[12])}
    return recs


def parse_renewal_report(fname):
    wb = openpyxl.load_workbook(fname, data_only=True)
    ws = wb['(3pseason) Seasons at Meridian']
    recs = {}
    for row in ws.iter_rows(min_row=8, values_only=True):
        if row[4] is None or str(row[4]).strip() == '':
            continue
        recs[str(row[4]).strip()] = {
            'name': row[6], 'old_exp': d(row[7]), 'new_start': d(row[8]),
            'prior_term': fnum(row[9]), 'prior_gross': fnum(row[10]),
            'prior_conc': fnum(row[11]), 'prior_eff': fnum(row[13]),
            'new_term': fnum(row[14]), 'new_gross': fnum(row[15]),
            'new_conc': fnum(row[16]), 'new_eff': fnum(row[18])}
    wb.close()
    return recs


def parse_hellodata(fname):
    with open(fname) as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append({'unit': r['Unit'].strip(), 'fp': r['Floorplan'],
                    'sf': fnum(r['SF']), 'bd': fnum(r['Bedrooms']),
                    'on': d(r['On Market Date']), 'off': d(r['Off Market Date']),
                    'avail': d(r['Available On']),
                    'ask': fnum(r['Last Asking Rent']), 'eff': fnum(r['Last Effective Rent']),
                    'term': fnum(r['Term']), 'dom': fnum(r['Days on Market']),
                    'dvac': fnum(r['Days Vacant'])})
    return out


# ---------------------------------------------------------------- helpers
def mkey(dt):
    return f'{dt.year:04d}-{dt.month:02d}' if dt else None


def add_months(dt, n):
    if dt is None or n is None:
        return None
    y, m = divmod((dt.year * 12 + dt.month - 1) + int(round(n)), 12)
    day = min(dt.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28,
                       31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m])
    return date(y, m + 1, day)


def month_end(mo):
    y, m = int(mo[:4]), int(mo[5:7])
    return date(y + (m == 12), 1 if m == 12 else m + 1, 1) - timedelta(days=1)


def effective(gross, conc_total, term):
    """Yardi convention: gross less the concession amortized over the lease term."""
    if gross is None or not term:
        return None
    return gross - abs(conc_total or 0) / term


def pct(a, b):
    return (b - a) / a if a and b else None


def concession_split(rows):
    """Frequency and depth, never blended — a blended average mixes conceding and
    non-conceding leases and reads as 'light concessions' when in fact most leases
    signed at full price and a few were deeply discounted."""
    have = [r for r in rows if r.get('new_gross') and r.get('new_eff') is not None]
    if not have:
        return dict(n=0, freq=None, depth=None, avg_conc=None)
    conc = [r for r in have if r['new_eff'] < r['new_gross'] - 0.01]
    depth = [1 - r['new_eff'] / r['new_gross'] for r in conc]
    amts = [r['new_conc_total'] for r in conc if r.get('new_conc_total')]
    return dict(n=len(have), freq=len(conc) / len(have),
                depth=sum(depth) / len(depth) if depth else None,
                avg_conc=sum(amts) / len(amts) if amts else None)


import re

# HelloData labels floor plans "S1" / "Studio | S1"; the rent roll calls the same
# plan "S1_Seas". Both collapse to a canonical plan code so mix-weighting binds
# across the proxy and actual layers. (Mapping per DATA_NOTES.)
PLAN_RE = re.compile(r'\b([ABCS])(\d)[a-z]?', re.I)


def plan_code(unit_type):
    if not unit_type:
        return None
    m = PLAN_RE.search(str(unit_type).split('|')[-1].strip())
    return f'{m.group(1).upper()}{m.group(2)}' if m else None


def mix_weighted(rows, key, mix):
    """Average rent weighted by the property's actual unit mix, not by how many of
    each floor plan happened to lease that month (which creates mix bias)."""
    by_fp = defaultdict(list)
    for r in rows:
        pc = plan_code(r.get('unit_type'))
        if r.get(key) and pc:
            by_fp[pc].append(r[key])
    if not by_fp:
        return None
    num = den = 0.0
    for fp, vals in by_fp.items():
        w = mix.get(fp, len(vals))
        num += (sum(vals) / len(vals)) * w
        den += w
    return num / den if den else None


def agg(pairs):
    """(prior, new) pairs -> n, avg prior $, avg new $, avg %, median %."""
    p = [(a, b) for a, b in pairs if a and b]
    if not p:
        return dict(n=0, prior=None, new=None, avg=None, med=None)
    ch = sorted((b - a) / a for a, b in p)
    n = len(ch)
    return dict(n=n, prior=sum(a for a, _ in p) / n, new=sum(b for _, b in p) / n,
                avg=sum(ch) / n, med=ch[n // 2] if n % 2 else (ch[n // 2 - 1] + ch[n // 2]) / 2)


# ---------------------------------------------------------------- build
def main():
    rolls = {tag: parse_rent_roll(f'{DOCS}/{p}') for tag, p in ROLLS}
    bo_jun = parse_burnoff(f'{DOCS}/concession-burnoff/ConcessionBurnOff_AsOf_2026-06-21.xlsx')
    bo_jul = parse_burnoff(f'{DOCS}/concession-burnoff/ConcessionBurnOff_AsOf_2026-07-30.xlsx')
    renew = parse_renewal_report(f'{DOCS}/renewal-reports/RenewalTradeouts_2026-05-10_to_2026-07-09.xlsx')
    hd = parse_hellodata(f'{DOCS}/hellodata/HelloData_UnitDetails_2026-08-14.csv')

    # ---- resident master: union of every resident seen on any roll --------
    res = {}
    for tag, _ in ROLLS:
        for r in rolls[tag]:
            m = res.setdefault(r['res'], {'res': r['res'], 'unit': r['unit'], 'type': r['type'],
                                          'sf': r['sf'], 'name': r['name'], 'movein': r['movein'],
                                          'seen': [], 'rent': {}, 'exp': {}, 'moveout': None,
                                          'future': False})
            m['seen'].append(tag)
            m['unit'] = r['unit']
            if r['actual']:
                m['rent'][tag] = r['actual']
            if r['leaseexp']:
                m['exp'][tag] = r['leaseexp']
            if r['moveout']:
                m['moveout'] = r['moveout']
            if r['movein'] and (m['movein'] is None or r['movein'] < m['movein']):
                m['movein'] = r['movein']
            if r['section'] and 'Future' in r['section']:
                m['future'] = True
            else:
                m['future'] = False

    # burn-off supplies the only lease-start dates in the dataset
    for src in (bo_jun, bo_jul):
        for rid, b in src.items():
            m = res.setdefault(rid, {'res': rid, 'unit': b['unit'], 'type': None, 'sf': None,
                                     'name': b['name'], 'movein': b['movein'], 'seen': [],
                                     'rent': {}, 'exp': {}, 'moveout': None, 'future': False})
            m.setdefault('bo', {})
            m['bo'] = b            # 7/30 overwrites 6/21 — the later view wins
            if m['movein'] is None:
                m['movein'] = b['movein']

    for m in res.values():
        m['corporate'] = m['name'] in CORPORATE
        b = m.get('bo')
        m['leasestart'] = b['leasestart'] if b else None
        m['term'] = b['term'] if b else None
        m['conc'] = b['cur_conc'] if b else None
        m['renewed'] = bool(b and b['leasestart'] and b['movein']
                            and (b['leasestart'] - b['movein']).days > RENEWAL_GAP_DAYS)
        # rent of record: latest roll actual (burn-off Lease Rent is unreliable — see DATA_COVERAGE)
        m['last_rent'] = next((m['rent'][t] for t, _ in reversed(ROLLS) if t in m['rent']), None)
        m['first_rent'] = next((m['rent'][t] for t, _ in ROLLS if t in m['rent']), None)
        m['last_exp'] = next((m['exp'][t] for t, _ in reversed(ROLLS) if t in m['exp']), None)

    # ---- HelloData episodes, chained per unit ----------------------------
    hd_by_unit = defaultdict(list)
    for e in hd:
        if e['off']:
            hd_by_unit[e['unit']].append(e)
    for u in hd_by_unit:
        hd_by_unit[u].sort(key=lambda e: e['off'])
        for i, e in enumerate(hd_by_unit[u]):
            e['seq'] = i                                    # 0 = first-generation lease-up lease
            e['prev'] = hd_by_unit[u][i - 1] if i else None

    def hd_episode(unit, movein, lo=-30, hi=120):
        """Best HelloData episode for a move-in: off-market from lo..hi days before."""
        best = None
        for e in hd_by_unit.get(unit, []):
            if movein is None:
                continue
            lag = (movein - e['off']).days
            if lo <= lag <= hi:
                if best is None or abs(lag - HD_TO_MOVEIN_LAG) < abs((movein - best['off']).days - HD_TO_MOVEIN_LAG):
                    best = e
        return best

    def hd_prior_episode(unit, signed):
        """Latest HelloData episode evidencing a REAL prior tenancy in this unit.

        Departed tenants who left before 1/1/2026 appear on no rent roll, so a prior
        listing is the only way to know a later lease was a re-lease rather than a
        first-generation lease-up lease.

        The gap threshold matters. During lease-up a unit is often listed, drops off
        market briefly (a fallen-through application, or the scraper losing it), then
        re-lists at the SAME price and leases — one lease, two episodes. Treating that
        as a turn invents re-leases and a spurious 0.0% trade-out. A genuine intervening
        tenancy needs at least the shortest lease term the burn-off shows (4 months),
        so episodes closer than MIN_TENANCY_DAYS are treated as the same lease-up.
        """
        prev = [e for e in hd_by_unit.get(unit, [])
                if e['off'] < signed - timedelta(days=MIN_TENANCY_DAYS)]
        return prev[-1] if prev else None

    def hd_effective(e):
        """Concession-adjusted rent for an episode, using its advertised term."""
        if not e or e['ask'] is None or e['eff'] is None:
            return None, None
        term = e['term']
        conc = (e['ask'] - e['eff']) * term if term else None
        return e['eff'], (abs(conc) if conc else None)

    # ==================================================================
    # EVENT LEDGER
    # ==================================================================
    events = []

    # The ACTUAL layer is built first (below) so the PROXY layer can defer to it at
    # the seam: a unit listed in late Dec 2025 whose Yardi lease starts in Jan 2026 is
    # ONE lease, and the Yardi record is the better one.
    # New leases are counted on MOVE-IN DATE (per RFR). The 1/1/26 roll carries real
    # move-in dates back to 8/21/2024, so the pre-2026 window is built resident-first
    # and falls back to HelloData only for tenants who had already left by then.
    residents_all = [m for m in res.values() if not m['future'] and m['movein']]

    def initial_gross(m, hde):
        """A resident's ORIGINAL lease rent. For anyone who renewed before the first
        rent roll, the roll already carries the renewed rent, so the listing is the
        only surviving record of what they originally signed at."""
        if m['renewed'] and m['leasestart'] and m['leasestart'] < ACTUAL_START:
            return (hde['ask'] if hde else None), 'HelloData ask (renewed before 1/1/26 roll)'
        if m['first_rent']:
            return m['first_rent'], 'Rent roll contract rent'
        return (hde['ask'] if hde else None), 'HelloData ask (no roll rent)'

    # ---------- PROXY window: Jun 2024 - Dec 2025 -------------------------
    matched_eps = set()
    for m in residents_all:
        mi = m['movein']
        if mi >= ACTUAL_START:
            continue
        hde = hd_episode(m['unit'], mi)
        if hde:
            matched_eps.add((m['unit'], hde['off']))
        hd_prev = hd_prior_episode(m['unit'], mi)
        ig, ig_src = initial_gross(m, hde)
        term = (hde['term'] if hde else None) or (m['term'] if not m['renewed'] else None)
        _, conc = hd_effective(hde)
        row = {'basis': 'PROXY (HelloData-era, real move-in date)', 'month': mkey(mi),
               'event': 'New Lease', 'unit': m['unit'], 'unit_type': m['type'], 'sf': m['sf'],
               'resident_id': m['res'], 'name': m['name'],
               'corporate': 'Y' if m['corporate'] else '',
               'signed': mi, 'movein_est': mi,
               'generation': 'Re-lease' if hd_prev else 'First lease-up lease',
               'term_mo': term, 'new_gross': ig,
               'new_conc_total': conc, 'new_eff': effective(ig, conc, term),
               'date_basis': 'Rent roll move-in date (exact)',
               'source': f'Rent roll roster + {ig_src}'}
        if hd_prev:
            peff, pconc = hd_effective(hd_prev)
            row.update({'prior_gross': hd_prev['ask'], 'prior_eff': peff,
                        'prior_term_mo': hd_prev['term'], 'prior_conc_total': pconc,
                        'prior_moveout': hd_prev['off'],
                        'prior_basis': 'PROXY — prior listing asking rent (no roll covers that tenant)'})
        row['to_gross_pct'] = pct(row.get('prior_gross'), row.get('new_gross'))
        row['to_eff_pct'] = pct(row.get('prior_eff'), row.get('new_eff'))
        events.append(row)

    # Episodes with no surviving resident: the tenant moved in AND out before any rent
    # roll was cut, so only the listing remains. Move-in is estimated from off-market.
    for u, eps in hd_by_unit.items():
        for e in eps:
            if e['off'] >= ACTUAL_START or (u, e['off']) in matched_eps:
                continue
            mi_est = e['off'] + timedelta(days=HD_TO_MOVEIN_LAG)
            if mi_est >= ACTUAL_START:
                continue
            prev = e['prev']
            row = {'basis': 'PROXY (HelloData, estimated move-in)', 'month': mkey(mi_est),
                   'event': 'New Lease', 'unit': u, 'unit_type': e['fp'], 'sf': e['sf'],
                   'signed': mi_est, 'movein_est': mi_est,
                   'generation': 'First lease-up lease' if prev is None else 'Re-lease',
                   'term_mo': e['term'], 'new_gross': e['ask'], 'new_eff': e['eff'],
                   'days_on_market': e['dom'],
                   'date_basis': f'ESTIMATED — off-market + {HD_TO_MOVEIN_LAG}d (median lag)',
                   'source': 'HelloData episode; tenant left before any rent roll'}
            if prev is not None:
                row.update({'prior_gross': prev['ask'], 'prior_eff': prev['eff'],
                            'prior_moveout': prev['off'],
                            'prior_basis': 'PROXY — prior listing asking rent',
                            'to_gross_pct': pct(prev['ask'], e['ask']),
                            'to_eff_pct': pct(prev['eff'], e['eff'])})
            events.append(row)

    # ---------- ACTUAL window: Jan 2026 - Aug 2026 (Yardi) ---------------
    # (a) new leases: lease start ~= move-in, starting in the actual window
    for m in res.values():
        if m['future']:
            continue
        start = m['movein']            # new leases counted on move-in date (per RFR)
        if start is None or start < ACTUAL_START or start > CUTOFF:
            continue
        # find the outgoing tenant of this unit for the trade-out baseline
        prior = None
        for o in res.values():
            if o['unit'] != m['unit'] or o['res'] == m['res'] or o['future']:
                continue
            if o['moveout'] and o['moveout'] <= start + timedelta(days=5):
                if prior is None or (o['moveout'] > prior['moveout']):
                    prior = o
        hde = hd_episode(m['unit'], m['movein'])
        term = m['term'] or (hde['term'] if hde else None)
        conc = m['conc']
        if conc is None and hde and hde['ask'] and hde['eff'] is not None and term:
            conc = (hde['ask'] - hde['eff']) * term
        # A unit listed before this lease was signed had an earlier tenant, whether or
        # not that tenant is on any rent roll. That is what makes this a re-lease.
        hd_prev = hd_prior_episode(m['unit'], start)
        row = {'basis': 'ACTUAL (Yardi)', 'month': mkey(start), 'event': 'New Lease',
               'unit': m['unit'], 'unit_type': m['type'], 'sf': m['sf'],
               'resident_id': m['res'], 'name': m['name'], 'corporate': 'Y' if m['corporate'] else '',
               'signed': start, 'movein_est': m['movein'],
               'generation': 'Re-lease' if (prior or hd_prev) else 'First lease-up lease',
               'term_mo': term, 'new_gross': m['last_rent'],
               'new_conc_total': abs(conc) if conc is not None else None,
               'new_eff': effective(m['last_rent'], conc, term),
               'date_basis': 'Rent roll move-in date (exact)',
               'source': 'Rent roll + burn-off'}
        # prior-rent baseline, best source first
        if prior and prior['last_rent']:
            pterm, pconc = prior['term'], prior['conc']
            if pconc is None:                      # departed tenant: fall back to their listing
                pe = hd_episode(prior['unit'], prior['movein'])
                if pe:
                    pterm = pterm or pe['term']
                    _, pconc = hd_effective(pe)
            row.update({'prior_resident': prior['res'], 'prior_name': prior['name'],
                        'prior_gross': prior['last_rent'],
                        'prior_eff': effective(prior['last_rent'], pconc, pterm),
                        'prior_term_mo': pterm,
                        'prior_conc_total': abs(pconc) if pconc else None,
                        'prior_moveout': prior['moveout'],
                        'prior_basis': 'Prior tenant contract rent (Yardi)',
                        'days_vacant': (m['movein'] - prior['moveout']).days
                        if m['movein'] and prior['moveout'] else None})
        elif hd_prev:
            peff, pconc = hd_effective(hd_prev)
            row.update({'prior_gross': hd_prev['ask'], 'prior_eff': peff,
                        'prior_term_mo': hd_prev['term'],
                        'prior_conc_total': pconc,
                        'prior_moveout': hd_prev['off'],
                        'prior_basis': 'PROXY — prior listing asking rent (tenant left before 1/1/26)'})
            # HelloData's Days Vacant is not turn downtime (it runs to 511 days on units
            # that were never occupied in between), so no vacancy figure on this path.
        row['to_gross_pct'] = pct(row.get('prior_gross'), row.get('new_gross'))
        row['to_eff_pct'] = pct(row.get('prior_eff'), row.get('new_eff'))
        events.append(row)

    # (b) renewals
    for m in res.values():
        if not m['renewed'] or m['leasestart'] is None:
            continue
        rr = renew.get(m['unit'])
        if rr and rr.get('name') and m['name'] and rr['name'] != m['name']:
            rr = None
        rd = m['leasestart']
        if rr:                                     # exact prior/new detail available
            row = {'prior_gross': rr['prior_gross'], 'prior_eff': rr['prior_eff'],
                   'prior_term_mo': rr['prior_term'], 'prior_conc_total': rr['prior_conc'],
                   'new_gross': rr['new_gross'], 'new_eff': rr['new_eff'],
                   'term_mo': rr['new_term'], 'new_conc_total': rr['new_conc'],
                   'prior_expiration': rr['old_exp'],
                   'source': 'Renewal trade-out report (exact)'}
            rd = rr['new_start'] or rd
        else:                                      # reconstruct from rolls + burn-off
            hde = hd_episode(m['unit'], m['movein'])
            pterm = hde['term'] if hde else None
            _, pconc = hd_effective(hde)
            if rd < ACTUAL_START:
                # Renewed before the 1/1/26 snapshot, so the Jan roll already carries the
                # RENEWED rent. Using it as the prior would force a spurious 0.0% trade-out.
                prior_g = hde['ask'] if hde else None
                psrc = 'Burn-off lease start + HelloData initial ask (renewed pre-1/1/26)'
            else:
                prior_g = m['first_rent']
                psrc = 'Burn-off lease start + rent rolls (reconstructed)'
            row = {'prior_gross': prior_g,
                   'prior_eff': effective(prior_g, pconc, pterm),
                   'prior_term_mo': pterm, 'prior_conc_total': abs(pconc) if pconc else None,
                   'new_gross': m['last_rent'],
                   'new_eff': effective(m['last_rent'], m['conc'], m['term']),
                   'term_mo': m['term'],
                   'new_conc_total': abs(m['conc']) if m['conc'] is not None else None,
                   'prior_expiration': rd - timedelta(days=1),
                   'source': psrc}
        row.update({'basis': 'ACTUAL (Yardi)' if rd >= ACTUAL_START else 'ACTUAL (Yardi, survivors only)',
                    'month': mkey(rd), 'event': 'Renewal', 'unit': m['unit'],
                    'unit_type': m['type'], 'sf': m['sf'], 'resident_id': m['res'],
                    'name': m['name'], 'corporate': 'Y' if m['corporate'] else '',
                    'signed': rd, 'movein_est': m['movein'], 'generation': 'Renewal',
                    'to_gross_pct': pct(row['prior_gross'], row['new_gross']),
                    'to_eff_pct': pct(row['prior_eff'], row['new_eff'])})
        events.append(row)

    # (c) move-outs / expirations
    for m in res.values():
        if m['moveout']:
            # A move-out dated after the last rent roll is a notice, not a departure.
            future = m['moveout'] > CUTOFF
            events.append({'basis': 'ACTUAL (Yardi)', 'month': mkey(m['moveout']),
                           'event': 'Notice (scheduled move-out)' if future else 'Move Out',
                           'unit': m['unit'], 'unit_type': m['type'],
                           'resident_id': m['res'], 'name': m['name'],
                           'corporate': 'Y' if m['corporate'] else '',
                           'signed': m['moveout'], 'movein_est': m['movein'],
                           'prior_gross': m['last_rent'],
                           'source': 'Rent roll move-out date' if not future
                                     else 'Rent roll notice — move-out scheduled after 8/4/26'})
        # The lease that actually came due, and what the tenant did about it.
        if m['renewed'] and m['leasestart']:
            exp, src = m['leasestart'] - timedelta(days=1), 'Renewal lease start - 1d'
        else:
            exp, src = m['last_exp'], 'Rent roll lease expiration'
        if exp and exp <= CUTOFF:
            events.append({'basis': 'ACTUAL (Yardi)', 'month': mkey(exp), 'event': 'Lease Expiration',
                           'unit': m['unit'], 'unit_type': m['type'], 'resident_id': m['res'],
                           'name': m['name'], 'corporate': 'Y' if m['corporate'] else '',
                           'signed': exp, 'movein_est': m['movein'],
                           'outcome': 'Renewed' if m['renewed'] else
                                      ('Moved Out' if m['moveout'] else 'MTM holdover'),
                           'source': src})
        # Forward book: the expiration each in-place resident is currently scheduled to hit.
        if m['last_exp'] and m['last_exp'] > CUTOFF and not m['moveout']:
            events.append({'basis': 'ACTUAL (Yardi)', 'month': mkey(m['last_exp']),
                           'event': 'Scheduled Expiration', 'unit': m['unit'],
                           'unit_type': m['type'], 'resident_id': m['res'], 'name': m['name'],
                           'corporate': 'Y' if m['corporate'] else '',
                           'signed': m['last_exp'], 'movein_est': m['movein'],
                           'outcome': 'Not yet due',
                           'source': 'Rent roll lease expiration (current lease)'})

    # One tenancy can appear under two resident ids (Yardi reassigned the id on J108),
    # which would otherwise count the same lease twice.
    # Collapse new-lease rows that describe the SAME lease: an identical unit+move-in
    # (Yardi reassigned a resident id on J108), or two listing episodes closer together
    # than the shortest possible tenancy (one lease-up split by the scraper). Keeping
    # the later row keeps the episode that actually leased.
    new_rows = sorted((e for e in events if e['event'] == 'New Lease'),
                      key=lambda e: (e['unit'], e['signed']))
    keep, n_dupes = [], 0
    for e in new_rows:
        if keep and keep[-1]['unit'] == e['unit'] and \
                (e['signed'] - keep[-1]['signed']).days < MIN_TENANCY_DAYS:
            n_dupes += 1
            keep[-1] = e if e['basis'].startswith('ACTUAL') or \
                not keep[-1]['basis'].startswith('ACTUAL') else keep[-1]
            continue
        keep.append(e)
    # generation follows the surviving sequence, so it cannot contradict the counts
    per_unit = defaultdict(int)
    for e in keep:
        per_unit[e['unit']] += 1
        e['generation'] = 'First lease-up lease' if per_unit[e['unit']] == 1 else 'Re-lease'
        if e['generation'] == 'First lease-up lease':
            for k in ('prior_gross', 'prior_eff', 'to_gross_pct', 'to_eff_pct',
                      'prior_basis', 'prior_moveout', 'prior_conc_total', 'prior_term_mo'):
                e.pop(k, None)
    events = [e for e in events if e['event'] != 'New Lease'] + keep
    print(f'collapsed {n_dupes} duplicate new-lease row(s) '
          f'(same unit within {MIN_TENANCY_DAYS}d = one lease)')

    # ==================================================================
    # MONTHLY ROLL-UP
    # ==================================================================
    # actual unit mix from the latest rent roll, for mix-weighting the rent levels
    # Every unit in the Current section, occupied or not — vacant units carry no
    # resident id and so are filtered out of the parsed roll, but they are still
    # part of the mix.
    wb = openpyxl.load_workbook(f'{DOCS}/rent-rolls/RentRoll_AsOf_2026-08-04.xlsx',
                                read_only=True, data_only=True)
    sec, all_units = None, {}
    for r in wb['Report1'].iter_rows(values_only=True):
        c0 = r[0]
        if isinstance(c0, str) and ('Current' in c0 or 'Future' in c0 or 'Total' in c0):
            sec = c0.strip()
            continue
        if c0 is None or r[1] is None or not (sec and 'Current' in sec):
            continue
        all_units.setdefault(str(c0).strip(), str(r[1]).strip())
    wb.close()
    unit_mix = defaultdict(int)
    for t in all_units.values():
        pc = plan_code(t)
        if pc:
            unit_mix[pc] += 1
    unit_mix = dict(unit_mix)
    print(f'unit mix (canonical plan codes, 8/4/26 roll): {unit_mix} = {sum(unit_mix.values())} units')

    # ==================================================================
    # OCCUPANCY
    # ==================================================================
    # Built as tenancy-interval coverage, not as a running sum of move-ins less
    # move-outs: a flow accumulator compounds every missed event, while coverage
    # is re-derived independently at each month-end and can be checked against the
    # rent rolls. A tenancy runs from move-in to whichever end date is known first —
    # a recorded move-out, or (for tenants who left before any roll existed) the
    # date the unit came back on market. Failing both, it runs to the next move-in
    # in that unit, which cannot overstate occupancy because the unit is occupied
    # by someone throughout.
    roll_dates = [date(*map(int, t.split('-'))) for t, _ in ROLLS]
    FIRST_ROLL = roll_dates[0]
    spans = defaultdict(list)
    for m in res.values():
        if m['future'] or not m['movein']:
            continue
        end = m['moveout']
        if end is None:
            # A resident on one roll and gone from a later one has moved out, even
            # when no move-out date was ever written. Without this the tenancy runs
            # forever and occupancy drifts high.
            later = [rd for rd, (t, _) in zip(roll_dates, ROLLS)
                     if rd > m['movein'] and t not in m['seen']]
            if later:
                end = later[0]
        spans[m['unit']].append([m['movein'], end, 'roll'])
    for e in events:
        if e['event'] == 'New Lease' and e['basis'].startswith('PROXY (HelloData,'):
            spans[e['unit']].append([e['signed'], None, 'hd', e.get('term_mo')])
    for u, lst in spans.items():
        lst.sort(key=lambda x: x[0])
        eps = hd_by_unit.get(u, [])
        for i, sp in enumerate(lst):
            if sp[1] is None and sp[2] == 'hd':
                # Same MIN_TENANCY_DAYS test used to classify re-leases: a unit that
                # re-lists a few weeks after going off-market never turned over, so
                # that re-listing must not be read as the tenant moving out.
                nxt = [x['on'] for x in eps
                       if x['on'] and (x['on'] - sp[0]).days >= MIN_TENANCY_DAYS]
                # Every listing-only tenant is gone by the first roll (that is what
                # makes them listing-only), so the span must close by then. Expiring
                # them on their own lease term rather than all at once on the roll
                # date is what keeps the curve from stepping off a cliff at 1/1/26.
                term_end = sp[0] + timedelta(days=round((sp[3] or 12) * 30.44))
                sp[1] = min([d for d in (nxt[0] if nxt else None, term_end, FIRST_ROLL) if d])
            if sp[1] is None and i + 1 < len(lst):
                sp[1] = lst[i + 1][0]

    def occupied_on(d):
        return sum(1 for lst in spans.values() for s in lst
                   if s[0] <= d and (s[1] is None or s[1] > d))

    ANCHORS = {date(2026, 1, 1): 314, date(2026, 7, 7): 341,
               date(2026, 7, 19): 338, date(2026, 8, 4): 346}
    print('\noccupancy check vs rent rolls (derived / actual):')
    for d, actual in sorted(ANCHORS.items()):
        got = occupied_on(d)
        print(f'  {d}  derived {got:3}  actual {actual:3}  diff {got - actual:+d}')

    months = sorted({e['month'] for e in events if e['month']})
    monthly = []
    for mo in months:
        ev = [e for e in events if e['month'] == mo]
        rent_ev = [e for e in ev if not e.get('corporate')]     # corporate excluded from $ stats

        new = [e for e in ev if e['event'] == 'New Lease']
        new_r = [e for e in rent_ev if e['event'] == 'New Lease']
        rel = [e for e in new if e['generation'] == 'Re-lease']
        rel_r = [e for e in new_r if e['generation'] == 'Re-lease']
        ren = [e for e in ev if e['event'] == 'Renewal']
        ren_r = [e for e in rent_ev if e['event'] == 'Renewal']
        exp = [e for e in ev if e['event'] == 'Lease Expiration']
        sched = [e for e in ev if e['event'] == 'Scheduled Expiration']
        out = [e for e in ev if e['event'] == 'Move Out']
        notice = [e for e in ev if e['event'] == 'Notice (scheduled move-out)']

        rs = agg([(e.get('prior_gross'), e.get('new_gross')) for e in ren_r])
        re_ = agg([(e.get('prior_eff'), e.get('new_eff')) for e in ren_r])
        ns = agg([(e.get('prior_gross'), e.get('new_gross')) for e in rel_r])
        ne = agg([(e.get('prior_eff'), e.get('new_eff')) for e in rel_r])

        ng = [e['new_gross'] for e in new_r if e.get('new_gross')]
        nef = [e['new_eff'] for e in new_r if e.get('new_eff')]
        bases = sorted({e['basis'] for e in ev})
        cs_new = concession_split(new_r)
        cs_ren = concession_split(ren_r)

        exp_ren = sum(1 for e in exp if e.get('outcome') == 'Renewed')
        exp_out = sum(1 for e in exp if e.get('outcome') == 'Moved Out')
        exp_mtm = sum(1 for e in exp if e.get('outcome') == 'MTM holdover')
        denom = exp_ren + exp_out + exp_mtm

        # the final month is partial — report it at the measurement date, not month-end
        eom = min(month_end(mo), CUTOFF)
        in_range = month_end(mo) <= CUTOFF or mo == mkey(CUTOFF)
        # Physical occupancy is only reported where it is observable. Pre-2026 the data
        # shows move-ins but no move-outs, so a curve there would be driven by imputed
        # lease terms (58% of listing-only tenancies have no term at all) rather than by
        # the property. Absorption below is observable throughout and carries that story.
        occ_n = occupied_on(eom) if (in_range and mo >= mkey(FIRST_ROLL)) else None
        # only claim a rent roll when the reported date IS the roll date; a roll merely
        # falling somewhere inside the month does not make the month-end figure exact
        roll_in_month = next((t for t, _ in ROLLS if t == eom.isoformat()), None)
        leased_cum = sum(1 for e in events
                         if e['event'] == 'New Lease'
                         and e['generation'] == 'First lease-up lease'
                         and e['month'] <= mo)

        monthly.append({
            'month': mo,
            'basis': 'ACTUAL (Yardi)' if all(b.startswith('ACTUAL') for b in bases) else
                     ('PROXY (pre-2026)' if all(b.startswith('PROXY') for b in bases) else 'MIXED'),
            'units_leased_to_date': leased_cum if in_range else None,
            'leased_to_date_pct': (leased_cum / TOTAL_UNITS) if in_range else None,
            'units_occupied_eom': occ_n,
            'units_vacant_eom': (TOTAL_UNITS - occ_n) if occ_n is not None else None,
            'physical_occupancy_eom': (occ_n / TOTAL_UNITS) if occ_n is not None else None,
            'occupancy_basis': ('Rent roll ' + roll_in_month + ' (exact)' if roll_in_month else
                                ('Derived — tenancy coverage' if occ_n is not None else
                                 'Not derivable — no pre-2026 move-out data')),
            'new_leases_signed': len(new),
            '  of which first lease-up lease': sum(1 for e in new if e['generation'] == 'First lease-up lease'),
            '  of which re-lease (turned unit)': len(rel),
            'new_lease_avg_gross': sum(ng) / len(ng) if ng else None,
            'new_lease_avg_eff': sum(nef) / len(nef) if nef else None,
            'new_lease_mixwtd_gross': mix_weighted(new_r, 'new_gross', unit_mix),
            'new_lease_mixwtd_eff': mix_weighted(new_r, 'new_eff', unit_mix),
            'new_conc_freq': cs_new['freq'], 'new_conc_depth': cs_new['depth'],
            'new_conc_avg_dollars': cs_new['avg_conc'],
            'renewal_conc_freq': cs_ren['freq'], 'renewal_conc_depth': cs_ren['depth'],
            'renewal_conc_avg_dollars': cs_ren['avg_conc'],
            'leases_expired': len(exp),
            '  expired -> renewed': exp_ren,
            '  expired -> moved out': exp_out,
            '  expired -> MTM holdover': exp_mtm,
            'renewals': len(ren),
            # Pre-2026 the burn-off only sees residents still in place at 7/30/26, so this
            # is a floor on renewals that month, not a count.
            'renewals_survivor_floor': len(ren) if mo < '2026-01' else None,
            'move_outs': len(out),
            'retention_pct': exp_ren / denom if denom else None,
            'scheduled_expirations_ahead': len(sched),
            'notices_scheduled_moveout': len(notice),
            'renewal_n': rs['n'],
            'renewal_prior_gross': rs['prior'], 'renewal_new_gross': rs['new'],
            'renewal_gross_pct_avg': rs['avg'], 'renewal_gross_pct_med': rs['med'],
            'renewal_prior_eff': re_['prior'], 'renewal_new_eff': re_['new'],
            'renewal_eff_pct_avg': re_['avg'], 'renewal_eff_pct_med': re_['med'],
            'relet_n': ns['n'],
            'newlease_prior_gross': ns['prior'], 'newlease_new_gross': ns['new'],
            'newlease_gross_pct_avg': ns['avg'], 'newlease_gross_pct_med': ns['med'],
            'newlease_prior_eff': ne['prior'], 'newlease_new_eff': ne['new'],
            'newlease_eff_pct_avg': ne['avg'], 'newlease_eff_pct_med': ne['med'],
        })

    # ---------------------------------------------------------------- out
    cols = sorted({k for e in events for k in e})
    order = ['basis', 'month', 'event', 'generation', 'unit', 'unit_type', 'sf', 'resident_id',
             'name', 'corporate', 'signed', 'movein_est', 'term_mo', 'prior_term_mo',
             'prior_gross', 'new_gross', 'to_gross_pct', 'prior_eff', 'new_eff', 'to_eff_pct',
             'prior_conc_total', 'new_conc_total', 'prior_expiration', 'prior_resident',
             'prior_name', 'prior_moveout', 'outcome', 'days_vacant', 'days_on_market', 'source']
    cols = [c for c in order if c in cols] + [c for c in cols if c not in order]
    events.sort(key=lambda e: (e['month'] or '', e['event'], e['unit']))
    with open('events.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(events)
    pd.DataFrame(monthly).to_csv('monthly.csv', index=False)

    # ---------------------------------------------------------------- validation
    print(f'events: {len(events)}   months: {months[0]} -> {months[-1]}')
    print('\nevent counts by basis:')
    for b in sorted({e['basis'] for e in events}):
        sub = [e for e in events if e['basis'] == b]
        print(f'  {b:35} {len(sub):4}  ' +
              ', '.join(f'{k}={sum(1 for e in sub if e["event"] == k)}'
                        for k in ('New Lease', 'Renewal', 'Lease Expiration', 'Move Out')))
    print(f'\nrenewals total: {sum(1 for e in events if e["event"] == "Renewal")} '
          f'(exact from report: {sum(1 for e in events if e.get("source", "").startswith("Renewal trade-out"))})')
    missed = [u for u in renew if not any(e['unit'] == u and e['event'] == 'Renewal' for e in events)]
    print(f'renewal-report units missing from ledger: {missed or "none"}')
    tot_new = sum(1 for e in events if e['event'] == 'New Lease')
    print(f'new leases signed, all periods: {tot_new}')
    print(f'  first lease-up leases: {sum(1 for e in events if e.get("generation") == "First lease-up lease")}')
    print(f'  re-leases:             {sum(1 for e in events if e.get("generation") == "Re-lease")}')
    print('\nwrote events.csv, monthly.csv')


if __name__ == '__main__':
    main()
